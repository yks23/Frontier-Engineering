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


def surrogate(params: dict) -> dict:
    lp = float(params['laser_power']); ss = float(params['scan_speed']); hs = float(params['hatch_spacing']); lt = float(params['layer_thickness'])
    energy_density = lp / max(ss * hs * lt, 1e-6)
    distortion = abs(energy_density - 85.0) / 20.0
    residual_stress = abs(lp - 230.0) / 80.0 + abs(ss - 820.0) / 400.0
    defect_risk = abs(hs - 0.11) / 0.05 + abs(lt - 0.04) / 0.03
    productivity = ss * hs * lt * 100.0
    combined = productivity - 40.0 * distortion - 25.0 * residual_stress - 20.0 * defect_risk
    return {'combined_score': combined, 'distortion': distortion, 'residual_stress': residual_stress, 'defect_risk': defect_risk, 'productivity': productivity}


def validate(instance: dict, params: dict) -> dict:
    b = instance['bounds']
    for key in ['laser_power','scan_speed','hatch_spacing','layer_thickness']:
        v = float(params[key]); lo, hi = map(float, b[key])
        if not (lo <= v <= hi):
            raise ValueError(f'{key} out of bounds')
    return surrogate(params)


def evaluate(candidate: str):
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    with tempfile.TemporaryDirectory(prefix='am_eval_') as tmp:
        out = Path(tmp) / 'process_params.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(out)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        scored = validate(load_json(instance_path), load_json(out))
        metrics = {'combined_score': float(scored['combined_score']), 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'distortion': float(scored['distortion']), 'residual_stress': float(scored['residual_stress']), 'defect_risk': float(scored['defect_risk']), 'productivity': float(scored['productivity'])}
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
