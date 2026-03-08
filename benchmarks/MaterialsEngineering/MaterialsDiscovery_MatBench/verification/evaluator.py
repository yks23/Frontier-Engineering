from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate(data: dict, labels: dict, submission: dict) -> dict:
    table = {c['candidate_id']: c for c in data['candidates']}
    budget = int(data['budget'])
    query_order = submission.get('query_order')
    selected = submission.get('selected_candidates')
    if not isinstance(query_order, list) or not isinstance(selected, list) or not selected:
        raise ValueError('query_order and selected_candidates must be lists, selected non-empty')
    if len(query_order) > budget:
        raise ValueError('query budget exceeded')
    if len(set(query_order)) != len(query_order) or len(set(selected)) != len(selected):
        raise ValueError('duplicate ids are not allowed')
    for cid in query_order + selected:
        if cid not in table:
            raise ValueError('unknown candidate id')
    vals = [float(labels[c]) for c in selected]
    best = max(vals)
    mean = sum(vals) / len(vals)
    eff = 1.0 - len(query_order) / budget
    score = 0.6 * best + 0.3 * mean + 0.1 * eff
    return {'combined_score': score, 'best_property_found': best, 'topk_mean_property': mean, 'query_efficiency': eff}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'candidates_public.json'
    hidden_path = task_root / 'references' / 'candidates_hidden.json'
    source_root_raw = os.environ.get('FRONTIER_EVAL_UNIFIED_SOURCE_BENCHMARK_DIR', '').strip()
    if source_root_raw:
        candidate_hidden = Path(source_root_raw) / 'references' / 'candidates_hidden.json'
        if candidate_hidden.is_file():
            hidden_path = candidate_hidden
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='mat_eval_') as tmp:
        out = Path(tmp) / 'submission.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(
                f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
        scored = validate(load_json(instance_path), load_json(hidden_path)['labels'], load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'best_property_found': float(scored['best_property_found']), 'topk_mean_property': float(scored['topk_mean_property']), 'query_efficiency': float(scored['query_efficiency'])}
        artifacts = {'submission': load_json(out)}
        return metrics, artifacts


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('candidate'); args=parser.parse_args()
    try:
        metrics, artifacts = evaluate(args.candidate)
    except subprocess.TimeoutExpired as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 1.0, 'runtime_s': 0.0}; artifacts = {'error': f'timeout: {exc}'}
    except Exception as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 0.0, 'runtime_s': 0.0}; artifacts = {'error': str(exc), 'traceback': traceback.format_exc()}
    with open(Path.cwd() / 'metrics.json', 'w', encoding='utf-8') as f: json.dump(metrics, f, indent=2)
    with open(Path.cwd() / 'artifacts.json', 'w', encoding='utf-8') as f: json.dump(artifacts, f, indent=2)
    print(json.dumps(metrics))


if __name__ == '__main__':
    main()
