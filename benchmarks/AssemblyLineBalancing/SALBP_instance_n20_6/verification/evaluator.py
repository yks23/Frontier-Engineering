from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

BEST_KNOWN_STATIONS = 3


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def station_count(instance: dict, priority: list[int]) -> int:
    n = int(instance['n'])
    cycle = int(instance['cycle_time'])
    times = {int(k): int(v) for k, v in instance['task_times'].items()}
    preds = {int(k): [int(x) for x in v] for k, v in instance['predecessors'].items()}
    assigned = set()
    remaining = list(priority)
    stations = 0
    while remaining:
        stations += 1
        used = 0
        progress = True
        while progress:
            progress = False
            for job in list(remaining):
                if any(p not in assigned for p in preds[job]):
                    continue
                dur = times[job]
                if used + dur > cycle:
                    continue
                used += dur
                assigned.add(job)
                remaining.remove(job)
                progress = True
        if used == 0:
            raise ValueError('failed to build feasible station assignment')
    return stations


def validate(instance: dict, submission: dict) -> dict:
    priority = submission.get('priority_order')
    n = int(instance['n'])
    if not isinstance(priority, list) or len(priority) != n:
        raise ValueError('priority_order length mismatch')
    p = [int(x) for x in priority]
    if set(p) != set(range(1, n + 1)):
        raise ValueError('priority_order must be a permutation of tasks')
    used = station_count(instance, p)
    return {'combined_score': BEST_KNOWN_STATIONS / used, 'used_stations': float(used), 'best_known_stations': float(BEST_KNOWN_STATIONS)}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='salbp_eval_') as tmp:
        out = Path(tmp) / 'solution.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'used_stations': float(scored['used_stations']), 'best_known_stations': float(scored['best_known_stations'])}
        artifacts = {'submission': load_json(out)}
        return metrics, artifacts


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument('candidate'); args = parser.parse_args()
    try:
        metrics, artifacts = evaluate(args.candidate)
    except subprocess.TimeoutExpired as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 1.0, 'runtime_s': 0.0}; artifacts = {'error': f'timeout: {exc}'}
    except Exception as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 0.0, 'runtime_s': 0.0}; artifacts = {'error': str(exc), 'traceback': traceback.format_exc()}
    with open(Path.cwd() / 'metrics.json', 'w', encoding='utf-8') as f: json.dump(metrics, f, indent=2)
    with open(Path.cwd() / 'artifacts.json', 'w', encoding='utf-8') as f: json.dump(artifacts, f, indent=2)
    print(json.dumps(metrics))


if __name__ == '__main__':
    main()
