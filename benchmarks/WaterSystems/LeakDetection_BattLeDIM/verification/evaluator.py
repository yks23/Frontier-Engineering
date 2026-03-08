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


def overlap(a: dict, b: dict) -> bool:
    return not (a['end'] < b['start'] or b['end'] < a['start'])


def evaluate_alarms(events: list[dict], pred: dict) -> dict:
    alarms = pred.get('alarms')
    if not isinstance(alarms, list):
        raise ValueError('alarms must be a list')
    truth = events
    used = set()
    tp = 0
    location_hits = 0
    delay_scores = []
    for alarm in alarms:
        zone = alarm['zone_id']
        start = int(alarm['start']); end = int(alarm['end'])
        if start > end:
            raise ValueError('alarm start must be <= end')
        match_idx = None
        for i, ev in enumerate(truth):
            if i in used:
                continue
            if overlap({'start': start, 'end': end}, ev):
                match_idx = i
                break
        if match_idx is not None:
            used.add(match_idx)
            tp += 1
            ev = truth[match_idx]
            if zone == ev['zone_id']:
                location_hits += 1
            delay = max(0, start - ev['start'])
            delay_scores.append(1.0 / (1.0 + delay))
    fp = len(alarms) - tp
    precision = tp / len(alarms) if alarms else 0.0
    recall = tp / len(truth) if truth else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
    location_score = location_hits / tp if tp > 0 else 0.0
    delay_score = sum(delay_scores) / len(delay_scores) if delay_scores else 0.0
    false_alarm_score = max(0.0, 1.0 - fp / max(1, len(alarms)))
    combined = 0.45 * f1 + 0.25 * location_score + 0.20 * delay_score + 0.10 * false_alarm_score
    return {'combined_score': combined, 'f1': f1, 'location_score': location_score, 'delay_score': delay_score, 'false_alarm_score': false_alarm_score}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance_public.json'
    hidden_path = task_root / 'references' / 'events_hidden.json'
    source_root_raw = os.environ.get('FRONTIER_EVAL_UNIFIED_SOURCE_BENCHMARK_DIR', '').strip()
    if source_root_raw:
        candidate_hidden = Path(source_root_raw) / 'references' / 'events_hidden.json'
        if candidate_hidden.is_file():
            hidden_path = candidate_hidden
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='water_eval_') as tmp:
        out = Path(tmp) / 'alarms.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = evaluate_alarms(load_json(hidden_path)['events'], load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'f1': float(scored['f1']), 'location_score': float(scored['location_score']), 'delay_score': float(scored['delay_score']), 'false_alarm_score': float(scored['false_alarm_score'])}
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
