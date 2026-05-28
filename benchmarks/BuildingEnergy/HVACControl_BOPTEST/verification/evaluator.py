from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

INVALID_SCORE = -1e18


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def simulate(instance: dict, schedule: dict) -> dict:
    powers = schedule.get('hvac_power_kw')
    if not isinstance(powers, list) or len(powers) != int(instance['horizon']):
        raise ValueError('hvac_power_kw length mismatch')
    low, high = map(float, instance['power_bounds'])
    lo_c, hi_c = map(float, instance['comfort_band'])
    indoor = float(instance['initial_temp'])
    energy_cost = 0.0
    comfort_penalty = 0.0
    peak = 0.0
    for p, tout, price in zip(powers, instance['outdoor_temp'], instance['price']):
        p = float(p)
        if not (low <= p <= high):
            raise ValueError('power out of bounds')
        indoor = indoor + 0.15 * (float(tout) - indoor) - 0.9 * p
        if indoor < lo_c:
            comfort_penalty += (lo_c - indoor) * 4.0
        elif indoor > hi_c:
            comfort_penalty += (indoor - hi_c) * 4.0
        energy_cost += p * float(price)
        peak = max(peak, p)
    peak_penalty = peak * 0.5
    score = -(energy_cost + comfort_penalty + peak_penalty)
    return {'combined_score': score, 'energy_cost': energy_cost, 'comfort_penalty': comfort_penalty, 'peak_power_kw': peak}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='hvac_eval_') as tmp:
        out = Path(tmp) / 'control_schedule.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = simulate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'energy_cost': float(scored['energy_cost']), 'comfort_penalty': float(scored['comfort_penalty']), 'peak_power_kw': float(scored['peak_power_kw'])}
        artifacts = {'submission': load_json(out)}
        return metrics, artifacts


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('candidate'); args=parser.parse_args()
    try:
        metrics, artifacts = evaluate(args.candidate)
    except subprocess.TimeoutExpired as exc:
        metrics = {'combined_score': INVALID_SCORE, 'valid': 0.0, 'timeout': 1.0, 'runtime_s': 0.0}; artifacts = {'error': f'timeout: {exc}'}
    except Exception as exc:
        metrics = {'combined_score': INVALID_SCORE, 'valid': 0.0, 'timeout': 0.0, 'runtime_s': 0.0}; artifacts = {'error': str(exc), 'traceback': traceback.format_exc()}
    with open(Path.cwd() / 'metrics.json', 'w', encoding='utf-8') as f: json.dump(metrics, f, indent=2)
    with open(Path.cwd() / 'artifacts.json', 'w', encoding='utf-8') as f: json.dump(artifacts, f, indent=2)
    print(json.dumps(metrics))


if __name__ == '__main__':
    main()
