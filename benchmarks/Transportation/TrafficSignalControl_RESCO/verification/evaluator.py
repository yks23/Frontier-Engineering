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


def simulate(instance: dict, plan: dict) -> dict:
    phases = plan.get('phases')
    if not isinstance(phases, list) or len(phases) != int(instance['horizon']):
        raise ValueError('phases must match horizon length')
    ns_q = 0
    ew_q = 0
    throughput = 0
    total_wait = 0
    total_queue = 0
    for t, phase in enumerate(phases):
        phase = int(phase)
        if phase not in (0,1):
            raise ValueError('phase must be 0 or 1')
        ns_q += int(instance['ns_arrivals'][t])
        ew_q += int(instance['ew_arrivals'][t])
        served = min(int(instance['service_rate']), ns_q if phase == 0 else ew_q)
        if phase == 0:
            ns_q -= served
        else:
            ew_q -= served
        throughput += served
        total_wait += ns_q + ew_q
        total_queue += ns_q + ew_q
    mean_wait = total_wait / int(instance['horizon'])
    mean_queue = total_queue / int(instance['horizon'])
    score = throughput - 0.5 * mean_wait - 0.2 * mean_queue
    return {'combined_score': score, 'throughput': throughput, 'mean_waiting': mean_wait, 'mean_queue': mean_queue}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='traffic_eval_') as tmp:
        out = Path(tmp) / 'signal_plan.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = simulate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'throughput': float(scored['throughput']), 'mean_waiting': float(scored['mean_waiting']), 'mean_queue': float(scored['mean_queue'])}
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
