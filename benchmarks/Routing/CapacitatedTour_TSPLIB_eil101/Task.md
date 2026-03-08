# TSPLIB eil101 Routing Benchmark

This task uses the official TSPLIB instance `eil101`.

## Output

Write `solution.json` with a Hamiltonian cycle order.

## Validity

- every node appears exactly once
- all node ids are valid

## Scoring

- `candidate_cost` = total tour cost using TSPLIB EUC_2D rounding
- `best_known_cost = 629`
- `combined_score = 629 / candidate_cost`
- `human_best_score = 1.0`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
