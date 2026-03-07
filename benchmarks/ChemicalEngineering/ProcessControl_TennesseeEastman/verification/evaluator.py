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


def simulate(instance: dict, submission: dict) -> dict:
    control = submission.get('control')
    if not isinstance(control, list) or len(control) != int(instance['horizon']):
        raise ValueError('control length mismatch')
    low, high = map(float, instance['control_bounds'])
    safe_lo, safe_hi = map(float, instance['safe_range'])
    target = float(instance['target'])
    x = float(instance['initial_x'])
    tracking_error = 0.0
    control_effort = 0.0
    recovery_time = int(instance['horizon'])
    recovered = False
    for t, (u, d) in enumerate(zip(control, instance['disturbance'])):
        u = float(u)
        if not (low <= u <= high):
            raise ValueError('control out of bounds')
        x = x + 0.25 * (target - x) - 0.18 * (u - 0.8) + float(d)
        if not (safe_lo <= x <= safe_hi):
            raise ValueError('safety range violated')
        tracking_error += abs(x - target)
        control_effort += abs(u - 0.8)
        if not recovered and abs(x - target) < 0.05:
            recovery_time = t
            recovered = True
    score = -(tracking_error + 0.1 * control_effort + 0.2 * recovery_time)
    return {'combined_score': score, 'tracking_error': tracking_error, 'control_effort': control_effort, 'recovery_time': recovery_time}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='te_eval_') as tmp:
        out = Path(tmp) / 'control.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = simulate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'tracking_error': float(scored['tracking_error']), 'control_effort': float(scored['control_effort']), 'recovery_time': float(scored['recovery_time'])}
        artifacts = {'submission': load_json(out)}
        return metrics, artifacts


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('candidate'); args=parser.parse_args()
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
