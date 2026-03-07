from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any


def _resolve_task_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _resolve_candidate_path(candidate: str) -> Path:
    raw = Path(candidate).expanduser()
    if raw.is_absolute():
        return raw.resolve()

    cwd_candidate = (Path.cwd() / raw).resolve()
    if cwd_candidate.is_file():
        return cwd_candidate

    task_candidate = (_resolve_task_root() / raw).resolve()
    return task_candidate


def _load_seed_specs(task_root: Path) -> list[dict[str, Any]]:
    with open(task_root / "references" / "taillard_seeds.json", "r", encoding="utf-8") as f:
        return json.load(f)["instances"]


def _unif(seed: int, low: int, high: int) -> tuple[int, int]:
    m = 2147483647
    a = 16807
    b = 127773
    c = 2836
    k = seed // b
    seed = a * (seed % b) - k * c
    if seed < 0:
        seed += m
    value_0_1 = seed / m
    value = low + int(value_0_1 * (high - low + 1))
    return seed, value


def generate_taillard_instance(spec: dict[str, Any]) -> dict[str, Any]:
    num_jobs = int(spec["num_jobs"])
    num_machines = int(spec["num_machines"])
    time_seed = int(spec["time_seed"])
    machine_seed = int(spec["machine_seed"])

    jobs: list[list[dict[str, int]]] = []

    for _job in range(num_jobs):
        durations: list[int] = []
        for _op in range(num_machines):
            time_seed, duration = _unif(time_seed, 1, 99)
            durations.append(int(duration))

        machines = list(range(num_machines))
        for i in range(num_machines):
            machine_seed, swap_idx = _unif(machine_seed, i, num_machines - 1)
            machines[i], machines[swap_idx] = machines[swap_idx], machines[i]

        job_ops = [
            {"machine": int(machines[i]), "duration": int(durations[i])}
            for i in range(num_machines)
        ]
        jobs.append(job_ops)

    return {
        "instance_id": spec["instance_id"],
        "num_jobs": num_jobs,
        "num_machines": num_machines,
        "jobs": jobs,
    }


def compute_lower_bound(instance: dict[str, Any]) -> int:
    job_bounds = [sum(int(op["duration"]) for op in job) for job in instance["jobs"]]
    machine_bounds = [0] * int(instance["num_machines"])
    for job in instance["jobs"]:
        for op in job:
            machine_bounds[int(op["machine"])] += int(op["duration"])
    return max(max(job_bounds), max(machine_bounds))


def _coerce_nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer, got bool")
    if isinstance(value, int):
        if value < 0:
            raise ValueError(f"{field_name} must be non-negative")
        return value
    if isinstance(value, float) and value.is_integer() and value >= 0:
        return int(value)
    raise ValueError(f"{field_name} must be a non-negative integer")


def validate_submission(instance: dict[str, Any], submission: dict[str, Any]) -> dict[str, Any]:
    jobs = instance["jobs"]
    num_jobs = int(instance["num_jobs"])
    num_machines = int(instance["num_machines"])
    total_ops = sum(len(job) for job in jobs)

    operations = submission.get("operations")
    if not isinstance(operations, list):
        raise ValueError("submission.operations must be a list")
    if len(operations) != total_ops:
        raise ValueError(f"expected {total_ops} operations, got {len(operations)}")

    seen: set[tuple[int, int]] = set()
    job_schedule: list[list[tuple[int, int]]] = [[] for _ in range(num_jobs)]
    machine_schedule: list[list[tuple[int, int, int, int]]] = [[] for _ in range(num_machines)]
    makespan = 0

    for item in operations:
        if not isinstance(item, dict):
            raise ValueError("each operation entry must be an object")
        job = _coerce_nonnegative_int(item.get("job"), "job")
        op = _coerce_nonnegative_int(item.get("op"), "op")
        machine = _coerce_nonnegative_int(item.get("machine"), "machine")
        start = _coerce_nonnegative_int(item.get("start"), "start")

        if job >= num_jobs:
            raise ValueError(f"job out of range: {job}")
        if op >= len(jobs[job]):
            raise ValueError(f"op out of range for job {job}: {op}")

        expected_machine = int(jobs[job][op]["machine"])
        duration = int(jobs[job][op]["duration"])
        if machine != expected_machine:
            raise ValueError(
                f"operation ({job}, {op}) must use machine {expected_machine}, got {machine}"
            )

        key = (job, op)
        if key in seen:
            raise ValueError(f"duplicate operation entry: {key}")
        seen.add(key)

        end = start + duration
        makespan = max(makespan, end)
        job_schedule[job].append((op, start, end))
        machine_schedule[machine].append((start, end, job, op))

    if len(seen) != total_ops:
        raise ValueError("not all operations were scheduled")

    for job, intervals in enumerate(job_schedule):
        intervals.sort(key=lambda item: item[0])
        for idx, (op, start, end) in enumerate(intervals):
            if op != idx:
                raise ValueError(f"job {job} missing operation {idx}")
            if idx > 0:
                prev_end = intervals[idx - 1][2]
                if start < prev_end:
                    raise ValueError(f"job precedence violated for job {job} at operation {idx}")

    for machine, intervals in enumerate(machine_schedule):
        intervals.sort(key=lambda item: (item[0], item[1], item[2], item[3]))
        for idx in range(1, len(intervals)):
            prev = intervals[idx - 1]
            cur = intervals[idx]
            if cur[0] < prev[1]:
                raise ValueError(
                    f"machine overlap on machine {machine}: ({prev[2]}, {prev[3]}) and ({cur[2]}, {cur[3]})"
                )

    return {
        "makespan": makespan,
        "lower_bound": compute_lower_bound(instance),
    }


def run_candidate(candidate_path: Path, instance: dict[str, Any], time_budget_s: float) -> tuple[dict[str, Any], float, str, str]:
    with tempfile.TemporaryDirectory(prefix="jobshop_eval_") as tmp_dir_raw:
        tmp_dir = Path(tmp_dir_raw)
        instance_path = tmp_dir / f"{instance['instance_id']}.json"
        output_path = tmp_dir / "submission.json"

        with open(instance_path, "w", encoding="utf-8") as f:
            json.dump(instance, f)

        cmd = [
            sys.executable,
            str(candidate_path),
            "--instance",
            str(instance_path),
            "--output",
            str(output_path),
            "--time-budget",
            str(time_budget_s),
        ]

        t0 = time.time()
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=max(5.0, time_budget_s + 5.0),
        )
        runtime_s = time.time() - t0

        if proc.returncode != 0:
            raise RuntimeError(
                f"candidate exited with code {proc.returncode}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
        if not output_path.is_file():
            raise RuntimeError("candidate did not create the required output file")

        with open(output_path, "r", encoding="utf-8") as f:
            submission = json.load(f)

        return submission, runtime_s, proc.stdout, proc.stderr


def evaluate(candidate: str) -> tuple[dict[str, float], dict[str, Any]]:
    start = time.time()
    task_root = _resolve_task_root()
    candidate_path = _resolve_candidate_path(candidate)
    seed_specs = _load_seed_specs(task_root)

    if not candidate_path.is_file():
        raise FileNotFoundError(f"candidate not found: {candidate_path}")

    instance_results: list[dict[str, Any]] = []
    ratios: list[float] = []
    runtimes: list[float] = []

    for spec in seed_specs:
        instance = generate_taillard_instance(spec)
        submission, runtime_s, stdout_text, stderr_text = run_candidate(
            candidate_path=candidate_path,
            instance=instance,
            time_budget_s=0.75,
        )
        validated = validate_submission(instance, submission)
        makespan = int(validated["makespan"])
        lower_bound = int(validated["lower_bound"])
        ratio = lower_bound / makespan
        ratios.append(float(ratio))
        runtimes.append(float(runtime_s))
        instance_results.append(
            {
                "instance_id": instance["instance_id"],
                "num_jobs": instance["num_jobs"],
                "num_machines": instance["num_machines"],
                "lower_bound": lower_bound,
                "makespan": makespan,
                "score_ratio": ratio,
                "candidate_runtime_s": runtime_s,
                "stdout_tail": stdout_text[-1000:],
                "stderr_tail": stderr_text[-1000:],
                "algorithm": submission.get("algorithm", ""),
            }
        )

    metrics = {
        "combined_score": float(statistics.fmean(ratios)) if ratios else 0.0,
        "valid": 1.0,
        "timeout": 0.0,
        "runtime_s": float(time.time() - start),
        "mean_instance_ratio": float(statistics.fmean(ratios)) if ratios else 0.0,
        "mean_candidate_runtime_s": float(statistics.fmean(runtimes)) if runtimes else 0.0,
        "instance_count": float(len(instance_results)),
        "mean_makespan": float(statistics.fmean([r["makespan"] for r in instance_results]))
        if instance_results
        else 0.0,
    }
    artifacts = {
        "candidate_path": str(candidate_path),
        "instance_results": instance_results,
    }
    return metrics, artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", help="Path to candidate program")
    args = parser.parse_args()

    metrics_path = Path.cwd() / "metrics.json"
    artifacts_path = Path.cwd() / "artifacts.json"

    try:
        metrics, artifacts = evaluate(args.candidate)
    except subprocess.TimeoutExpired as exc:
        metrics = {
            "combined_score": 0.0,
            "valid": 0.0,
            "timeout": 1.0,
            "runtime_s": 0.0,
        }
        artifacts = {"error": f"timeout: {exc}"}
    except Exception as exc:  # pragma: no cover - error path
        metrics = {
            "combined_score": 0.0,
            "valid": 0.0,
            "timeout": 0.0,
            "runtime_s": 0.0,
        }
        artifacts = {
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    with open(artifacts_path, "w", encoding="utf-8") as f:
        json.dump(artifacts, f, indent=2)

    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
