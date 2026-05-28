from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_priority(instance: dict) -> dict:
    n = int(instance['n'])
    # Deliberately weak but feasible baseline.
    return {'instance_name': instance['instance_name'], 'priority_order': list(range(n, 0, -1)), 'method': 'reverse_job_id_priority'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(build_priority(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
