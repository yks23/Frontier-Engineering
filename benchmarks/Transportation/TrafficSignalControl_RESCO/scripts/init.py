from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_plan(instance: dict) -> dict:
    ns_q = 0
    ew_q = 0
    phases = []
    for ns_a, ew_a in zip(instance['ns_arrivals'], instance['ew_arrivals']):
        ns_q += ns_a
        ew_q += ew_a
        phase = 0 if ns_q >= ew_q else 1
        phases.append(phase)
        if phase == 0:
            ns_q = max(0, ns_q - int(instance['service_rate']))
        else:
            ew_q = max(0, ew_q - int(instance['service_rate']))
    return {'phases': phases, 'method': 'greedy_queue_balancing'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(build_plan(load_instance(args.instance)), f, indent=2)


if __name__ == '__main__':
    main()
