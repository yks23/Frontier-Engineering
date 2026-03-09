from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_cost(instance: dict, assignment: list[int]) -> int:
    n = int(instance['n'])
    flow = instance['flow']
    dist = instance['distance']
    total = 0
    for i in range(n):
        ai = assignment[i] - 1
        for j in range(n):
            aj = assignment[j] - 1
            total += int(flow[i][j]) * int(dist[ai][aj])
    return total


def initial_assignment(n: int) -> list[int]:
    # Modifiable: deliberately weak permutation to leave room for search improvements.
    odds = list(range(1, n + 1, 2))
    evens = list(range(2, n + 1, 2))
    return odds + evens


def best_neighbor_swap(instance: dict, assignment: list[int]) -> list[int]:
    # Modifiable: one-step local improvement baseline.
    best = list(assignment)
    best_cost = compute_cost(instance, best)
    n = len(assignment)
    for i in range(n):
        for j in range(i + 1, n):
            cand = list(best)
            cand[i], cand[j] = cand[j], cand[i]
            cand_cost = compute_cost(instance, cand)
            if cand_cost < best_cost:
                best, best_cost = cand, cand_cost
    return best


def build_assignment(instance: dict) -> dict:
    n = int(instance['n'])
    assign = initial_assignment(n)
    return {'instance_name': instance['instance_name'], 'assignment': assign, 'method': 'weak_permutation_baseline'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(build_assignment(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
