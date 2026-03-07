# Budgeted Materials Discovery

Select candidates under a fixed query budget.

## Input

The benchmark provides a candidate table with numeric descriptors and hidden target properties.

## Output

Write `submission.json`:

```json
{
  "task_id": "matbench_small_v1",
  "query_order": ["mat_001", "mat_002"],
  "selected_candidates": ["mat_010", "mat_014"],
  "method": "..."
}
```

## Validity

A submission is valid only if:

1. `query_order` length does not exceed the query budget.
2. All candidate ids exist.
3. `selected_candidates` is non-empty and only contains valid ids.
4. Duplicate ids are not allowed.

## Scoring

For a valid submission:

- `best_property_found` = best hidden property among selected candidates
- `topk_mean_property` = mean hidden property of selected candidates
- `query_efficiency = 1 - len(query_order)/budget`
- `combined_score = 0.6 * best_property_found + 0.3 * topk_mean_property + 0.1 * query_efficiency`

Invalid output receives `combined_score = 0` and `valid = 0`.

<!-- AI_GENERATED -->
