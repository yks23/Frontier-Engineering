# Small Optimal Power Flow

Choose generator dispatch and bus phase angles.

## Output

Write `solution.json`:

```json
{
  "benchmark_id": "opf_small_v1",
  "generator_p": [1.2, 0.6],
  "theta": [0.0, -0.1, -0.2],
  "method": "..."
}
```

## Validity

A solution is valid only if:

1. generator dispatch is within limits
2. line flows are within thermal limits
3. bus power balance residual is below tolerance
4. slack bus angle is fixed at 0

## Scoring

`combined_score = 1 / (1 + generation_cost)` for valid solutions.
Invalid output receives score 0.

<!-- AI_GENERATED -->
