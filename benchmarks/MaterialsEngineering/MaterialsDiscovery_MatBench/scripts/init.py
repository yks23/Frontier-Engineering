from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_data(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def score_proxy(features: list[float]) -> float:
    return 0.5 * features[0] + 0.3 * features[1] + 0.2 * features[2]


def select_candidates(data: dict) -> dict:
    ranked = sorted(data['candidates'], key=lambda c: score_proxy(c['features']), reverse=True)
    query_order = [c['candidate_id'] for c in ranked[: data['budget']]]
    selected = [c['candidate_id'] for c in ranked[:3]]
    return {'task_id': data['task_id'], 'query_order': query_order, 'selected_candidates': selected, 'method': 'proxy_ranking'}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--instance', required=True); parser.add_argument('--output', required=True); args=parser.parse_args()
    result=select_candidates(load_data(args.instance))
    out=Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,'w',encoding='utf-8') as f: json.dump(result,f,indent=2)


if __name__ == '__main__':
    main()
