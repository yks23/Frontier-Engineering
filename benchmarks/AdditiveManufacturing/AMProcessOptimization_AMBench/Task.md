# Additive Manufacturing Process Optimization

Choose process parameters for a metal additive manufacturing run.

## Output

Write `process_params.json`:

```json
{
  "material": "IN625",
  "laser_power": 230.0,
  "scan_speed": 800.0,
  "hatch_spacing": 0.11,
  "layer_thickness": 0.04,
  "method": "..."
}
```

## Validity

Parameters must stay inside the declared bounds.

## Scoring

The evaluator uses a deterministic surrogate for:

- distortion
- residual stress
- productivity
- defect risk

`combined_score = productivity_bonus - distortion_penalty - stress_penalty - defect_penalty`

Higher is better. Invalid output receives score 0.

<!-- AI_GENERATED -->
