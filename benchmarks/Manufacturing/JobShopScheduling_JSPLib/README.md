# JobShopScheduling_JSPLib

## Quick Start

Run from this benchmark directory:

```bash
python3 verification/evaluator.py scripts/init.py
python3 -m frontier_eval task=jobshop_scheduling algorithm.iterations=0
```

## Files

- `Task.md`: task definition and scoring
- `references/taillard_seeds.json`: benchmark source metadata
- `scripts/init.py`: self-contained starter solution
- `verification/evaluator.py`: evaluator entrypoint
- `frontier_eval/`: unified task metadata

## Reference score

- `human_best_score = 0.7967499751439758`
- This value is converted from public best-known makespans (`ta01=1231`, `ta02=1244`, `ta11=1357`) using this benchmark's score definition

## Registered task name

`jobshop_scheduling`

<!-- AI_GENERATED -->
