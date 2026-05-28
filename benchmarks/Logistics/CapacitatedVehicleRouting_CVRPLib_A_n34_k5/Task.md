# CVRPLib A-n34-k5 Capacitated Vehicle Routing

This task uses the official CVRPLib instance `A-n34-k5`.

## Output

Write `solution.json` with explicit routes.

## Validity

- every customer is visited exactly once
- every route starts and ends at depot `1`
- route demand does not exceed capacity
- all node ids are valid

## Scoring

- `candidate_cost` = total Euclidean route cost
- `best_known_cost = 778`
- `combined_score = 778 / candidate_cost`
- `human_best_score = 1.0`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
