from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def detect_events(instance: dict) -> dict:
    alarms = []
    for zone_id, values in instance['zones'].items():
        base = sum(values[:10]) / 10.0
        in_alarm = False
        start = 0
        for t, v in enumerate(values):
            if v < base - 2.0 and not in_alarm:
                in_alarm = True
                start = t
            if in_alarm and v >= base - 1.0:
                alarms.append({'start': start, 'end': t - 1, 'zone_id': zone_id, 'confidence': 0.8})
                in_alarm = False
        if in_alarm:
            alarms.append({'start': start, 'end': len(values) - 1, 'zone_id': zone_id, 'confidence': 0.8})
    return {'alarms': alarms, 'method': 'zone_pressure_drop_threshold'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    result=detect_events(load_instance(args.instance))
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)


if __name__ == '__main__':
    main()
