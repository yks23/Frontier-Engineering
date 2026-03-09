from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_control(instance: dict) -> dict:
    target = float(instance['target'])
    x = float(instance['initial_x'])
    low, high = map(float, instance['control_bounds'])
    control = []
    for d in instance['disturbance']:
        u = max(low, min(high, 0.8 + 1.2 * max(0.0, x - target)))
        control.append(u)
        x = x + 0.25 * (target - x) - 0.18 * (u - 0.8) + float(d)
    return {'control': control, 'method': 'proportional_cooling'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(build_control(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
