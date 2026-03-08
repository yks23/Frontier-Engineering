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


def is_adj(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 1


def validate(instance: dict, submission: dict) -> dict:
    grid = instance['grid']
    h, w = len(grid), len(grid[0])
    agent_specs = {a['name']: a for a in instance['agents']}
    paths = submission.get('paths')
    if not isinstance(paths, dict):
        raise ValueError('paths must be an object')
    if set(paths) != set(agent_specs):
        raise ValueError('paths keys must match all agents')
    norm: dict[str, list[tuple[int, int]]] = {}
    for name, seq in paths.items():
        if not isinstance(seq, list) or not seq:
            raise ValueError(f'{name} path must be non-empty list')
        cells = []
        for item in seq:
            if not (isinstance(item, list) and len(item) == 2):
                raise ValueError(f'{name} path items must be [r,c]')
            r, c = int(item[0]), int(item[1])
            if not (0 <= r < h and 0 <= c < w):
                raise ValueError(f'{name} path leaves grid')
            if grid[r][c] == '#':
                raise ValueError(f'{name} path hits obstacle')
            cells.append((r, c))
        spec = agent_specs[name]
        if cells[0] != tuple(spec['start']):
            raise ValueError(f'{name} start mismatch')
        if cells[-1] != tuple(spec['goal']):
            raise ValueError(f'{name} goal mismatch')
        for i in range(1, len(cells)):
            if not is_adj(cells[i - 1], cells[i]):
                raise ValueError(f'{name} has illegal jump')
        norm[name] = cells
    horizon = max(len(v) for v in norm.values())
    extended = {}
    for name, cells in norm.items():
        last = cells[-1]
        extended[name] = cells + [last] * (horizon - len(cells))
    for t in range(horizon):
        occ = {}
        for name, cells in extended.items():
            cell = cells[t]
            if cell in occ:
                raise ValueError(f'vertex collision at time {t}')
            occ[cell] = name
        if t == 0:
            continue
        for name_a, path_a in extended.items():
            prev_a, curr_a = path_a[t - 1], path_a[t]
            for name_b, path_b in extended.items():
                if name_a >= name_b:
                    continue
                prev_b, curr_b = path_b[t - 1], path_b[t]
                if prev_a == curr_b and prev_b == curr_a:
                    raise ValueError(f'edge swap collision at time {t}')
    makespan = max(len(cells) - 1 for cells in norm.values())
    sum_of_costs = sum(len(cells) - 1 for cells in norm.values())
    score = 0.6 / (1 + makespan) + 0.4 / (1 + sum_of_costs)
    return {'makespan': float(makespan), 'sum_of_costs': float(sum_of_costs), 'combined_score': float(score)}


def evaluate(candidate: str) -> tuple[dict, dict]:
    task_root = Path(__file__).resolve().parent.parent
    instance_path = task_root / 'references' / 'instance.json'
    candidate_path = (Path.cwd() / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate)
    if not candidate_path.is_file():
        candidate_path = (task_root / candidate).resolve()
    if not candidate_path.is_file():
        raise FileNotFoundError(candidate)
    with tempfile.TemporaryDirectory(prefix='mapf_eval_') as tmp:
        tmp = Path(tmp)
        output_path = tmp / 'paths.json'
        proc = subprocess.run([sys.executable, str(candidate_path), '--instance', str(instance_path), '--output', str(output_path)], capture_output=True, text=True, timeout=30)
        if proc.returncode != 0:
            raise RuntimeError(
                f"candidate failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
        submission = load_json(output_path)
        instance = load_json(instance_path)
        scored = validate(instance, submission)
        metrics = {'combined_score': scored['combined_score'], 'valid': 1.0, 'timeout': 0.0, 'runtime_s': 0.0, 'makespan': scored['makespan'], 'sum_of_costs': scored['sum_of_costs']}
        artifacts = {'instance_id': instance['instance_id'], 'submission': submission}
        return metrics, artifacts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('candidate')
    args = parser.parse_args()
    try:
        metrics, artifacts = evaluate(args.candidate)
    except subprocess.TimeoutExpired as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 1.0, 'runtime_s': 0.0}
        artifacts = {'error': f'timeout: {exc}'}
    except Exception as exc:
        metrics = {'combined_score': 0.0, 'valid': 0.0, 'timeout': 0.0, 'runtime_s': 0.0}
        artifacts = {'error': str(exc), 'traceback': traceback.format_exc()}
    with open(Path.cwd() / 'metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)
    with open(Path.cwd() / 'artifacts.json', 'w', encoding='utf-8') as f:
        json.dump(artifacts, f, indent=2)
    print(json.dumps(metrics))


if __name__ == '__main__':
    main()
