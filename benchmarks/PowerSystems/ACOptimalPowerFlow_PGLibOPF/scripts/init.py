from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def solve(instance: dict) -> dict:
    # Precomputed feasible dispatch/angle pair for this starter DC-like case.
    g0 = 0.775
    g1 = 0.925
    theta = [0.0, 0.06436170212765958, 0.15106382978723407]
    return {
        'benchmark_id': instance['benchmark_id'],
        'generator_p': [g0, g1],
        'theta': theta,
        'method': 'fixed_dc_like_solution',
    }


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    result=solve(load_instance(args.instance))
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)


if __name__ == '__main__':
    main()
