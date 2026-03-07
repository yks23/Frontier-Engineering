# Warehouse Multi-Agent Path Finding

## Background

This task models a warehouse robot coordination problem. Several robots must move inventory between locations on a discrete warehouse grid without colliding.

## Problem

Given a grid map with obstacles and a fixed set of agents, output one path per agent. Every path is a sequence of grid cells over time.

## Validity constraints

A solution is valid only if:

1. Every path starts at the required start cell.
2. Every path ends at the required goal cell.
3. Each move is either wait or move by one Manhattan step.
4. Agents never enter obstacle cells or leave the grid.
5. No two agents share the same cell at the same time.
6. No two agents swap positions on the same timestep.

## Output format

Write `paths.json` with:

```json
{
  "instance_id": "warehouse_small_v1",
  "method": "...",
  "paths": {
    "agent_0": [[0, 0], [0, 1]],
    "agent_1": [[6, 0], [6, 1]]
  }
}
```

## Scoring

For a valid solution:

- `makespan` = maximum path length minus one
- `sum_of_costs` = total number of moves over all agents
- `combined_score = 0.6 / (1 + makespan) + 0.4 / (1 + sum_of_costs)`

Invalid output receives `valid = 0` and `combined_score = 0`.

<!-- AI_GENERATED -->
