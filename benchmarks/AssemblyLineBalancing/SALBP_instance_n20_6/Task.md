# SALBP `instance_n=20_6`

## Background

Simple Assembly Line Balancing Problem (SALBP) is an engineering optimization problem from production system design. The practical objective is to minimize the number of stations needed to achieve a required cycle time while respecting task precedence constraints.

## Instance Setting

This task uses the official benchmark instance `instance_n=20_6`.

- number of tasks: 20
- cycle time: 1000
- official best-known / optimal number of stations: 3

## Candidate Output

The candidate must write:

```json
{
  "instance_name": "instance_n=20_6",
  "priority_order": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
  "method": "..."
}
```

The evaluator uses this priority order in a deterministic serial assignment procedure.

## Validity

A solution is valid only if:

1. `priority_order` is a permutation of all tasks.
2. The evaluator can construct a complete feasible assignment.
3. All precedence constraints are satisfied.
4. Every station stays within the cycle time.

## Scoring

- `used_stations` = number of stations produced by the evaluator
- `best_known_stations = 3`
- `combined_score = 3 / used_stations`
- `human_best_score = 1.0`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
