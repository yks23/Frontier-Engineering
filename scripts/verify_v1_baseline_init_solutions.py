#!/usr/bin/env python3
"""
Run initial-program evaluation for every task in a v1 batch YAML (e.g. generated_v1_g87_shinka_abmcts_baseline0.yaml).

Usage (from repo root, with FRONTIER_ENGINEERING_ROOT set):
  python scripts/verify_v1_baseline_init_solutions.py \\
    frontier_eval/conf/batch/generated_v1_g87_shinka_abmcts_baseline0.yaml

Env:
  FRONTIER_ENGINEERING_ROOT — repo root (required)
  FRONTIER_EVAL_EVALUATOR_TIMEOUT_S — per-task wall clock (default 3600)
  FRONTIER_EVAL_KERNEL_FORCE_CPU — 1 to force CPU for MLA / FlashAttention on crowded GPU nodes
  FRONTIER_EVAL_UNIFIED_CONDA_ACTIVATE — 1 on clusters where `conda run -n env` does not put env
    bin on PATH
  ENGDESIGN_EVAL_MODE — local | docker (default local for smoke)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def _repo_root() -> Path:
    root = os.environ.get("FRONTIER_ENGINEERING_ROOT", "").strip()
    if not root:
        print("ERROR: set FRONTIER_ENGINEERING_ROOT", file=sys.stderr)
        sys.exit(2)
    return Path(root).expanduser().resolve()


def _coerce_value(raw: str) -> bool | str:
    t = raw.strip()
    low = t.lower()
    if low in ("true", "yes", "on", "1"):
        return True
    if low in ("false", "no", "off", "0"):
        return False
    return t


def _apply_task_override(cfg, line: str) -> None:
    if not line.strip() or "=" not in line:
        return
    key, _, val = line.partition("=")
    key = key.strip()
    if not key.startswith("task."):
        return
    from omegaconf import OmegaConf

    path = key[len("task.") :].strip()
    OmegaConf.update(cfg, path, _coerce_value(val), merge=False)


def _coerce_hydra_oc_env_defaults(node: dict) -> dict:
    """Resolve ``${oc.env:VAR,default}`` strings left after yaml.safe_load (no Hydra)."""
    import re
    from typing import Any

    pat = re.compile(r"^\$\{oc\.env:([^,{}]+),\s*([^}]*)\}\s*$")

    def subst(s: str) -> str:
        m = pat.match(s.strip())
        if not m:
            return s
        var = m.group(1).strip()
        default = m.group(2).strip().strip("'\"")
        return (os.environ.get(var) or default or "").strip()

    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        if isinstance(obj, str):
            return subst(obj)
        return obj

    out = walk(node)
    return out if isinstance(out, dict) else {}


def _load_yaml_file(path: Path) -> dict:
    try:
        import yaml
    except ImportError as e:
        raise SystemExit("PyYAML required: pip install pyyaml") from e
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}
    resolved = _resolve_task_interpolations_dict(raw, raw)
    return _coerce_hydra_oc_env_defaults(resolved) if isinstance(resolved, dict) else {}


def _resolve_task_interpolations_dict(node: dict, task_root: dict):
    """Resolve ${task.field} strings the way Hydra task= would (no full config root)."""
    from typing import Any

    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        if isinstance(obj, str) and obj.startswith("${task.") and obj.endswith("}"):
            sub = obj[len("${task.") : -1].strip()
            cur: Any = task_root
            for part in sub.split("."):
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    return obj
            return cur
        return obj

    return walk(node)


def _load_batch(path: Path) -> list[dict]:
    try:
        import yaml
    except ImportError as e:
        raise SystemExit("PyYAML required: pip install pyyaml") from e
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "tasks" not in data:
        raise SystemExit("batch yaml must be a dict with key 'tasks'")
    tasks = data["tasks"]
    if not isinstance(tasks, list):
        raise SystemExit("'tasks' must be a list")
    return tasks


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "batch_yaml",
        type=Path,
        help="Path to batch yaml (e.g. frontier_eval/conf/batch/generated_v1_g87_shinka_abmcts_baseline0.yaml)",
    )
    p.add_argument("--timeout-s", type=int, default=None, help="Override FRONTIER_EVAL_EVALUATOR_TIMEOUT_S")
    args = p.parse_args()

    repo = _repo_root()
    sys.path.insert(0, str(repo))

    if args.timeout_s is not None:
        os.environ["FRONTIER_EVAL_EVALUATOR_TIMEOUT_S"] = str(args.timeout_s)
    os.environ.setdefault("FRONTIER_EVAL_EVALUATOR_TIMEOUT_S", "3600")
    os.environ.setdefault("ENGDESIGN_EVAL_MODE", "local")

    from omegaconf import OmegaConf

    from frontier_eval.registry_tasks import get_task

    batch_path = args.batch_yaml.expanduser().resolve()
    if not batch_path.is_file():
        # allow relative to repo
        alt = repo / args.batch_yaml
        if alt.is_file():
            batch_path = alt
        else:
            raise SystemExit(f"batch yaml not found: {args.batch_yaml}")

    task_conf_dir = repo / "frontier_eval" / "conf" / "task"
    entries = _load_batch(batch_path)

    print(
        "label\tregistry\tvalid\tcombined_score\truntime_s\terror_snip",
        flush=True,
    )
    fail = 0
    for raw in entries:
        entry: dict
        if isinstance(raw, str):
            text = raw.strip()
            if not text or text.startswith("#"):
                continue
            entry = {"name": text, "label": text}
        elif isinstance(raw, dict):
            entry = raw
        else:
            continue
        label = str(entry.get("label") or entry.get("name") or "unknown")
        hydra_task_name = str(entry.get("name") or "").strip()
        if not hydra_task_name:
            continue

        task_yaml = task_conf_dir / f"{hydra_task_name}.yaml"
        if task_yaml.is_file():
            task_cfg = OmegaConf.create(_load_yaml_file(task_yaml))
        else:
            task_cfg = OmegaConf.create({"name": hydra_task_name})

        for ov in entry.get("overrides") or []:
            if isinstance(ov, str):
                _apply_task_override(task_cfg, ov)

        reg_name = str(task_cfg.get("name") or hydra_task_name)
        os.environ["FRONTIER_EVAL_TASK_NAME"] = reg_name
        # Mirror batch / Hydra: JSON cfg for consumers that read env only
        plain = OmegaConf.to_container(task_cfg, resolve=True)
        if isinstance(plain, dict):
            os.environ["FRONTIER_EVAL_TASK_CFG_JSON"] = json.dumps(plain, ensure_ascii=False)
        else:
            os.environ.pop("FRONTIER_EVAL_TASK_CFG_JSON", None)

        t0 = time.time()
        err_snip = ""
        valid = -1.0
        combined = float("nan")
        try:
            Task = get_task(reg_name)
            task = Task(cfg=OmegaConf.create({"task": task_cfg}), repo_root=repo)
            prog = task.initial_program_path()
            res = task.evaluate_program(prog)
            metrics = getattr(res, "metrics", res) or {}
            valid = float(metrics.get("valid", 0.0) or 0.0)
            combined = float(metrics.get("combined_score", float("nan")))
            art = getattr(res, "artifacts", None) or {}
            err_snip = str(art.get("error_message") or "")[:120].replace("\n", " ")
        except Exception as e:
            err_snip = str(e)[:120]
            valid = 0.0

        rt = time.time() - t0
        print(
            f"{label}\t{reg_name}\t{valid}\t{combined}\t{rt:.1f}\t{err_snip}",
            flush=True,
        )
        if valid < 1.0:
            fail += 1

    print(f"# done fail_count={fail} total={len(entries)}", flush=True)
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
