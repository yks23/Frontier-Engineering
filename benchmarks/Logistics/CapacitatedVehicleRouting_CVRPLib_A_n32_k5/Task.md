# CVRPLib A-n32-k5 Capacitated Vehicle Routing

This task uses the official CVRPLib instance `A-n32-k5`.

## Input

The instance contains:

- one depot
- customer coordinates
- customer demands
- one vehicle capacity value

## Output

Write `solution.json`:

```json
{
  "instance_name": "A-n32-k5",
  "routes": [[1, 5, 7, 1]],
  "method": "..."
}
```

Route nodes include the depot id `1` at both start and end.

## Validity

A solution is valid only if:

1. Every customer (all non-depot nodes) is visited exactly once.
2. Every route starts and ends at depot `1`.
3. Route demand does not exceed capacity.
4. All node ids are valid.

## Scoring

- `candidate_cost` = total Euclidean route cost
- `best_known_cost = 784`
- `combined_score = 784 / candidate_cost`
- `human_best_score = 1.0`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
