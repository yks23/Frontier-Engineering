# Wind Farm Layout Optimization

Choose turbine coordinates inside a rectangular site.

## Validity

A layout is valid only if:

1. It contains exactly the required number of turbines.
2. Every turbine lies inside the site bounds.
3. Every pair of turbines respects the minimum spacing.

## Output

Write `layout.json`:

```json
{
  "site_id": "windfarm_small_v1",
  "method": "...",
  "turbines": [{"x": 10.0, "y": 20.0}]
}
```

## Scoring

The evaluator computes a simplified annual energy production proxy with pairwise wake penalties.

For a valid solution:

- higher `aep_score` is better
- `combined_score = aep_score`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
