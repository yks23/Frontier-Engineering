from __future__ import annotations

import argparse
import json
from pathlib import Path

DEPOT_ID = 1


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_naive_routes(instance: dict) -> dict:
    customers = instance['customers']
    capacity = int(instance['capacity'])
    others = [c for c in customers if int(c['id']) != DEPOT_ID]
    routes = []
    current = [DEPOT_ID]
    current_demand = 0
    ordered = sorted(others, key=lambda c: int(c['id']))
    for customer in ordered:
        demand = int(customer['demand'])
        if current_demand + demand > capacity and len(current) > 1:
            current.append(DEPOT_ID)
            routes.append(current)
            current = [DEPOT_ID]
            current_demand = 0
        current.append(int(customer['id']))
        current_demand += demand
    current.append(DEPOT_ID)
    routes.append(current)
    return {'instance_name': instance['instance_name'], 'routes': routes, 'method': 'naive_id_order_split'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = build_naive_routes(load_instance(args.instance))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
