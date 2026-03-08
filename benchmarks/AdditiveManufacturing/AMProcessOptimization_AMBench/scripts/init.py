from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def choose_params(instance: dict) -> dict:
    b = instance['bounds']
    mid = {k: (float(v[0]) + float(v[1])) / 2.0 for k, v in b.items()}
    return {'material': instance['material'], 'laser_power': mid['laser_power'], 'scan_speed': mid['scan_speed'], 'hatch_spacing': mid['hatch_spacing'], 'layer_thickness': mid['layer_thickness'], 'method': 'midpoint_rule'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    result=choose_params(load_instance(args.instance))
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)


if __name__ == '__main__':
    main()
