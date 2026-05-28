from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

BEST_KNOWN_COST = 1150.0


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate(instance: dict, submission: dict) -> dict:
    perm = submission.get('assignment')
    n = int(instance['n'])
    if not isinstance(perm, list) or len(perm) != n:
        raise ValueError('assignment length mismatch')
    p = [int(x) for x in perm]
    if set(p) != set(range(1, n + 1)):
        raise ValueError('assignment must be a permutation of 1..n')
    flow = instance['flow']
    dist = instance['distance']
    obj = 0
    for i in range(n):
        for j in range(n):
            obj += int(flow[i][j]) * int(dist[p[i]-1][p[j]-1])
    return {'combined_score': BEST_KNOWN_COST / obj, 'candidate_cost': float(obj), 'best_known_cost': BEST_KNOWN_COST}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='qap_eval_') as tmp:
        out = Path(tmp) / 'solution.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=60)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'candidate_cost': float(scored['candidate_cost']), 'best_known_cost': float(scored['best_known_cost'])}
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
