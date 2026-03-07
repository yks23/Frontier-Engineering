from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_site(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_layout(site: dict) -> dict:
    n = int(site['num_turbines'])
    spacing = float(site['min_spacing'])
    width = float(site['width'])
    height = float(site['height'])
    cols = 3
    rows = 2
    xs = [spacing + i * ((width - 2 * spacing) / max(1, cols - 1)) for i in range(cols)]
    ys = [spacing + j * ((height - 2 * spacing) / max(1, rows - 1)) for j in range(rows)]
    coords = []
    for j in range(rows):
        for i in range(cols):
            coords.append({'x': xs[i], 'y': ys[j]})
    coords = coords[:n]
    return {'site_id': site['site_id'], 'method': 'grid_layout', 'turbines': coords}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = build_layout(load_site(args.instance))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
