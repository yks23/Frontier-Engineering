from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

DEPOT_ID = 1
BEST_KNOWN_COST = 778.0


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def euclidean(a: dict, b: dict) -> float:
    return math.hypot(float(a['x']) - float(b['x']), float(a['y']) - float(b['y']))


def route_cost(route: list[int], nodes: dict[int, dict]) -> float:
    total = 0.0
    for u, v in zip(route, route[1:]):
        total += euclidean(nodes[u], nodes[v])
    return total


def validate(instance: dict, submission: dict) -> dict:
    routes = submission.get('routes')
    if not isinstance(routes, list) or not routes:
        raise ValueError('routes must be a non-empty list')
    nodes = {int(c['id']): c for c in instance['customers']}
    capacity = int(instance['capacity'])
    all_customers = {nid for nid in nodes if nid != DEPOT_ID}
    seen: set[int] = set()
    total_cost = 0.0
    for route in routes:
        if not isinstance(route, list) or len(route) < 2:
            raise ValueError('each route must contain at least depot-depot')
        if int(route[0]) != DEPOT_ID or int(route[-1]) != DEPOT_ID:
            raise ValueError('route must start and end at depot')
        demand = 0
        for nid_raw in route:
            nid = int(nid_raw)
            if nid not in nodes:
                raise ValueError('unknown node id')
        for nid_raw in route[1:-1]:
            nid = int(nid_raw)
            if nid == DEPOT_ID:
                raise ValueError('depot cannot appear inside route body')
            if nid in seen:
                raise ValueError('customer visited more than once')
            seen.add(nid)
            demand += int(nodes[nid]['demand'])
        if demand > capacity:
            raise ValueError('route exceeds capacity')
        total_cost += route_cost([int(x) for x in route], nodes)
    if seen != all_customers:
        missing = sorted(all_customers - seen)
        raise ValueError(f'missing customers: {missing[:10]}')
    score = BEST_KNOWN_COST / total_cost
    return {'combined_score': float(score), 'candidate_cost': float(total_cost), 'best_known_cost': float(BEST_KNOWN_COST)}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='cvrp_eval_') as tmp:
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
