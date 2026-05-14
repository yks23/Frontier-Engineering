# Water Leak Detection and Localization

Given multi-zone pressure time series, detect leak events and output alarm intervals.

## Output

Write `alarms.json`:

```json
{
  "alarms": [
    {"start": 40, "end": 70, "zone_id": "zone_1", "confidence": 0.9}
  ],
  "method": "..."
}
```

## Scoring

The evaluator matches predicted alarms with hidden ground-truth leak events and computes:

- event F1
- localization accuracy
- delay score
- false alarm score

`combined_score = 0.45 * f1 + 0.25 * location_score + 0.20 * delay_score + 0.10 * false_alarm_score`

Invalid output receives score 0.

<!-- AI_GENERATED -->
