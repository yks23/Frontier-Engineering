from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


def load_json(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def distance(a: dict, b: dict) -> float:
    return math.hypot(float(a['x']) - float(b['x']), float(a['y']) - float(b['y']))


def compute_aep(site: dict, turbines: list[dict]) -> float:
    base_power = 100.0 * len(turbines)
    penalty = 0.0
    angles = site['wind_directions']
    weights = site['wind_weights']
    for angle, weight in zip(angles, weights):
        rad = math.radians(angle)
        ux, uy = math.cos(rad), math.sin(rad)
        for i, a in enumerate(turbines):
            for j, b in enumerate(turbines):
                if i == j:
                    continue
                dx = float(b['x']) - float(a['x'])
                dy = float(b['y']) - float(a['y'])
                downwind = dx * ux + dy * uy
                lateral = abs(-dx * uy + dy * ux)
                if downwind > 0 and lateral < 12.0:
                    penalty += weight * (20.0 / (20.0 + downwind))
    return max(0.0, base_power - penalty)


def validate(site: dict, layout: dict) -> dict:
    turbines = layout.get('turbines')
    if not isinstance(turbines, list):
        raise ValueError('turbines must be a list')
    if len(turbines) != int(site['num_turbines']):
        raise ValueError('wrong number of turbines')
    for t in turbines:
        x = float(t['x']); y = float(t['y'])
        if not (0.0 <= x <= float(site['width']) and 0.0 <= y <= float(site['height'])):
            raise ValueError('turbine outside site')
    for i in range(len(turbines)):
        for j in range(i + 1, len(turbines)):
            if distance(turbines[i], turbines[j]) < float(site['min_spacing']) - 1e-9:
                raise ValueError('minimum spacing violated')
    aep = compute_aep(site, turbines)
    return {'combined_score': float(aep), 'aep_score': float(aep)}


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    site_path = task_root / 'references' / 'site.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='wind_eval_') as tmp:
        out = Path(tmp) / 'layout.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(site_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(
                f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
        site = load_json(site_path)
        layout = load_json(out)
        scored = validate(site, layout)
        metrics = {'combined_score': scored['combined_score'], 'aep_score': scored['aep_score'], 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0}
        artifacts = {'layout': layout, 'site_id': site['site_id']}
        return metrics, artifacts


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument('candidate'); args = parser.parse_args()
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
