from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_schedule(instance: dict) -> dict:
    low, high = map(float, instance['power_bounds'])
    indoor = float(instance['initial_temp'])
    schedule = []
    for tout in instance['outdoor_temp']:
        if indoor > instance['comfort_band'][1]:
            power = min(high, 3.0)
        elif indoor > 24.5:
            power = min(high, 2.0)
        else:
            power = low
        schedule.append(power)
        indoor = indoor + 0.15 * (tout - indoor) - 0.9 * power
    return {'hvac_power_kw': schedule, 'method': 'threshold_cooling'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(build_schedule(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
