# QAPLIB nug14 Quadratic Assignment

Assign each facility to exactly one location.

## Output

Write `solution.json` with a permutation of 1..n.

## Validity

- permutation length must equal n
- every location appears exactly once

## Scoring

- `candidate_cost` = standard QAP objective
- `best_known_cost = 1014`
- `combined_score = 1014 / candidate_cost`
- `human_best_score = 1.0`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
