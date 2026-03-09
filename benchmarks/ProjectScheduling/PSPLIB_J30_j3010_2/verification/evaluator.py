from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def serial_sgs(instance: dict, priority: list[int]) -> int:
    n = int(instance['n'])
    durations = {int(k): int(v) for k, v in instance['durations'].items()}
    demands = {int(k): [int(x) for x in v] for k, v in instance['demands'].items()}
    preds = {int(k): [int(x) for x in v] for k, v in instance['predecessors'].items()}
    caps = [int(x) for x in instance['capacities']]
    horizon = int(instance['horizon']) + sum(durations.values())
    usage = [[0 for _ in caps] for _ in range(horizon + 1)]
    start = {}
    finish = {}
    unscheduled = set(priority)
    # keep scheduling until all jobs are placed
    while unscheduled:
        progress = False
        for job in priority:
            if job not in unscheduled:
                continue
            if any(p not in finish for p in preds[job]):
                continue
            earliest = max((finish[p] for p in preds[job]), default=0)
            dur = durations[job]
            need = demands[job]
            t = earliest
            while True:
                feasible = True
                for tau in range(t, t + dur):
                    for r in range(len(caps)):
                        if usage[tau][r] + need[r] > caps[r]:
                            feasible = False
                            break
                    if not feasible:
                        break
                if feasible:
                    break
                t += 1
            start[job] = t
            finish[job] = t + dur
            for tau in range(t, t + dur):
                for r in range(len(caps)):
                    usage[tau][r] += need[r]
            unscheduled.remove(job)
            progress = True
        if not progress:
            raise ValueError('failed to construct feasible schedule')
    sink = n
    return finish[sink]


def validate(instance: dict, submission: dict) -> dict:
    priority = submission.get('priority_order')
    n = int(instance['n'])
    if not isinstance(priority, list) or len(priority) != n:
        raise ValueError('priority_order length mismatch')
    p = [int(x) for x in priority]
    if set(p) != set(range(1, n + 1)):
        raise ValueError('priority_order must be a permutation of jobs')
    makespan = serial_sgs(instance, p)
    best = int(instance['best_known_makespan'])
    return {'combined_score': best / makespan, 'candidate_makespan': float(makespan), 'best_known_makespan': float(best)}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='psp_eval_') as tmp:
        out = Path(tmp) / 'solution.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'candidate_makespan': float(scored['candidate_makespan']), 'best_known_makespan': float(scored['best_known_makespan'])}
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
