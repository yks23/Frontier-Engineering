from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_cycle(instance: dict) -> dict:
    ids = [int(n['id']) for n in instance['coords']]
    return {'instance_name': instance['instance_name'], 'tour': ids, 'method': 'naive_id_order'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(build_cycle(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
