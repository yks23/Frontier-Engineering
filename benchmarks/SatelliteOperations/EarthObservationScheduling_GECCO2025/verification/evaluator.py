from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def slew_time(a1: float, a2: float, scale: float) -> int:
    return int(abs(a1 - a2) * scale)


def validate(instance: dict, plan: dict) -> dict:
    selected = plan.get('selected_observations')
    if not isinstance(selected, list):
        raise ValueError('selected_observations must be a list')
    table = {o['obs_id']: o for o in instance['opportunities']}
    seen = set()
    prev_end = 0
    prev_angle = 0.0
    total_reward = 0.0
    total_slew = 0.0
    for item in selected:
        obs_id = item['obs_id']
        start = int(item['start'])
        if obs_id not in table:
            raise ValueError('unknown observation id')
        if obs_id in seen:
            raise ValueError('duplicate observation')
        seen.add(obs_id)
        obs = table[obs_id]
        need_slew = slew_time(prev_angle, float(obs['angle']), float(instance['slew_scale']))
        if start < prev_end + need_slew:
            raise ValueError('slew time violated')
        if start < int(obs['earliest']) or start > int(obs['latest']):
            raise ValueError('time window violated')
        end = start + int(obs['duration'])
        if end > int(instance['horizon']):
            raise ValueError('horizon exceeded')
        prev_end = end
        prev_angle = float(obs['angle'])
        total_reward += float(obs['reward'])
        total_slew += float(need_slew)
    score = max(0.0, total_reward - 0.1 * total_slew)
    return {'combined_score': score, 'total_reward': total_reward, 'slew_cost': total_slew}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='sat_eval_') as tmp:
        out = Path(tmp) / 'plan.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(
                f"candidate failed\\nSTDOUT:\\n{proc.stdout}\\nSTDERR:\\n{proc.stderr}"
            )
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'total_reward': float(scored['total_reward']), 'slew_cost': float(scored['slew_cost'])}
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
