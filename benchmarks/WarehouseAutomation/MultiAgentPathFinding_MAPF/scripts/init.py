from __future__ import annotations

import argparse
import heapq
import json
from pathlib import Path


def load_instance(path: str | Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def neighbors(grid: list[str], cell: tuple[int, int]):
    r, c = cell
    candidates = [(r, c), (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    h = len(grid)
    w = len(grid[0])
    for nr, nc in candidates:
        if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] != '#':
            yield nr, nc


def shortest_path(grid: list[str], start: tuple[int, int], goal: tuple[int, int], reserved_v: set[tuple[int, int, int]], reserved_e: set[tuple[int, int, int, int, int]], max_t: int = 80) -> list[list[int]]:
    start_state = (0, start[0], start[1])
    pq = [(abs(start[0]-goal[0]) + abs(start[1]-goal[1]), 0, start_state)]
    parent = {start_state: None}
    best_g = {start_state: 0}
    while pq:
        _, g, (t, r, c) = heapq.heappop(pq)
        if (r, c) == goal:
            state = (t, r, c)
            out = []
            while state is not None:
                _, rr, cc = state
                out.append([rr, cc])
                state = parent[state]
            return list(reversed(out))
        if t >= max_t:
            continue
        for nr, nc in neighbors(grid, (r, c)):
            nt = t + 1
            if (nt, nr, nc) in reserved_v:
                continue
            if (r, c, nr, nc, nt) in reserved_e:
                continue
            st = (nt, nr, nc)
            ng = g + 1
            if ng >= best_g.get(st, 10**9):
                continue
            best_g[st] = ng
            parent[st] = (t, r, c)
            h = abs(nr - goal[0]) + abs(nc - goal[1])
            heapq.heappush(pq, (ng + h, ng, st))
    raise RuntimeError('No feasible prioritized path found')


def reserve(path: list[list[int]], reserved_v: set[tuple[int, int, int]], reserved_e: set[tuple[int, int, int, int, int]], horizon: int = 80) -> None:
    for t, cell in enumerate(path):
        r, c = cell
        reserved_v.add((t, r, c))
        if t > 0:
            pr, pc = path[t - 1]
            reserved_e.add((r, c, pr, pc, t))
    end_r, end_c = path[-1]
    for t in range(len(path), horizon + 1):
        reserved_v.add((t, end_r, end_c))


def solve_instance(instance: dict) -> dict:
    grid = instance['grid']
    reserved_v: set[tuple[int, int, int]] = set()
    reserved_e: set[tuple[int, int, int, int, int]] = set()
    paths: dict[str, list[list[int]]] = {}
    for agent in instance['agents']:
        name = agent['name']
        start = tuple(agent['start'])
        goal = tuple(agent['goal'])
        path = shortest_path(grid, start, goal, reserved_v, reserved_e)
        paths[name] = path
        reserve(path, reserved_v, reserved_e)
    return {
        'instance_id': instance['instance_id'],
        'method': 'prioritized_a_star',
        'paths': paths,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = solve_instance(load_instance(args.instance))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
