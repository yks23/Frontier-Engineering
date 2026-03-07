from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate(instance: dict, solution: dict) -> dict:
    gen_p = solution.get('generator_p'); theta = solution.get('theta')
    if not (isinstance(gen_p, list) and isinstance(theta, list)):
        raise ValueError('generator_p and theta must be lists')
    if len(gen_p) != len(instance['generators']) or len(theta) != len(instance['loads']):
        raise ValueError('dimension mismatch')
    if abs(float(theta[0])) > 1e-9:
        raise ValueError('slack bus angle must be zero')
    injections = [0.0] * len(instance['loads'])
    cost = 0.0
    for i, (g, spec) in enumerate(zip(gen_p, instance['generators'])):
        g = float(g)
        if not (float(spec['p_min']) <= g <= float(spec['p_max'])):
            raise ValueError('generator out of bounds')
        bus = int(spec['bus'])
        injections[bus] += g
        cost += float(spec['a']) * g * g + float(spec['b']) * g
    for i, load in enumerate(instance['loads']):
        injections[i] -= float(load)
    residuals = [0.0] * len(instance['loads'])
    for line in instance['lines']:
        i = int(line['from']); j = int(line['to']); b = float(line['b']); limit = float(line['limit'])
        flow = b * (float(theta[i]) - float(theta[j]))
        if abs(flow) > limit + 1e-9:
            raise ValueError('line limit violated')
        residuals[i] -= flow
        residuals[j] += flow
    max_res = 0.0
    for i in range(len(residuals)):
        max_res = max(max_res, abs(residuals[i] - injections[i]))
    if max_res > float(instance['tolerance']) + 1e-6:
        raise ValueError(f'power balance residual too high: {max_res}')
    score = 1.0 / (1.0 + cost)
    return {'combined_score': score, 'generation_cost': cost, 'max_balance_residual': max_res}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='opf_eval_') as tmp:
        out = Path(tmp) / 'solution.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'generation_cost': float(scored['generation_cost']), 'max_balance_residual': float(scored['max_balance_residual'])}
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
