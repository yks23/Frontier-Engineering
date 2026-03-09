# Traffic Signal Control

Choose a phase sequence for a single intersection.

## Output

Write `signal_plan.json`:

```json
{
  "phases": [0, 0, 1, 1, 0],
  "method": "..."
}
```

Phase `0` serves north-south traffic, phase `1` serves east-west traffic.

## Scoring

The evaluator simulates queue evolution.

For a valid plan:

- `combined_score = throughput - 0.5 * mean_waiting - 0.2 * mean_queue`

Higher is better. Invalid output receives score 0.

<!-- AI_GENERATED -->
