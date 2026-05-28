# Earth Observation Satellite Scheduling

Select a feasible subset and order of observation opportunities.

## Validity

A schedule is valid only if:

1. Every selected observation exists in the opportunity table.
2. Observations are in nondecreasing execution time order.
3. Each observation starts within its allowed time window.
4. Consecutive observations respect required slew time.
5. The planning horizon is not exceeded.

## Output

Write `plan.json`:

```json
{
  "horizon": 360,
  "method": "...",
  "selected_observations": [
    {"obs_id": "obs_01", "start": 15}
  ]
}
```

## Scoring

For a valid plan:

- `combined_score = total_reward - 0.1 * slew_cost`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
