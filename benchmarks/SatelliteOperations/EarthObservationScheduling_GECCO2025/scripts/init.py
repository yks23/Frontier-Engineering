from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def slew_time(a1: float, a2: float, scale: float) -> int:
    return int(abs(a1 - a2) * scale)


def build_plan(instance: dict) -> dict:
    horizon = int(instance['horizon'])
    scale = float(instance['slew_scale'])
    opps = sorted(instance['opportunities'], key=lambda x: (x['latest'], -x['reward']))
    selected = []
    t = 0
    prev_angle = 0.0
    for obs in opps:
        start = max(t + slew_time(prev_angle, float(obs['angle']), scale), int(obs['earliest']))
        end = start + int(obs['duration'])
        if start <= int(obs['latest']) and end <= horizon:
            selected.append({'obs_id': obs['obs_id'], 'start': start})
            t = end
            prev_angle = float(obs['angle'])
    return {'horizon': horizon, 'method': 'earliest_deadline_greedy', 'selected_observations': selected}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    result=build_plan(load_instance(args.instance))
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)


if __name__ == '__main__':
    main()
