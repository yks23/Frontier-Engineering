# Simplified Process Control

Output a control schedule that keeps a process variable close to target under disturbance.

## Output

Write `control.json`:

```json
{
  "control": [0.8, 0.8, 1.0],
  "method": "..."
}
```

## Validity

- control length must equal horizon
- every control value must stay inside bounds
- process variable must remain within hard safety range

## Scoring

`combined_score = -(tracking_error + 0.1 * control_effort + 0.2 * recovery_time)`

Higher is better. Invalid output receives score 0.

<!-- AI_GENERATED -->
