# Single-Zone HVAC Control

Output an HVAC power schedule over a fixed horizon.

## Output

Write `control_schedule.json`:

```json
{
  "hvac_power_kw": [1.2, 1.2, 0.8],
  "method": "..."
}
```

## Validity

- schedule length must equal horizon
- every control value must remain within allowed power bounds

## Scoring

The evaluator simulates indoor temperature.

`combined_score = -(energy_cost + comfort_penalty + peak_penalty)`

Higher is better. Invalid output receives score 0.

<!-- AI_GENERATED -->
