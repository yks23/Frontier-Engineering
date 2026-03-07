# Job Shop Scheduling from Taillard / OR-Library Style Instances

## Background

This task models a manufacturing scheduling problem where each job must visit a fixed sequence of machines. The goal is to generate a feasible production schedule with low makespan.

The benchmark instances are generated from the Taillard procedure distributed through OR-Library. This keeps the benchmark lightweight while still anchored in a standard public source.

## Problem

Given:

- `num_jobs` jobs
- `num_machines` machines
- for each job, an ordered list of operations
- each operation has:
  - a required machine
  - a processing duration

You must output a start time for every operation.

## Feasibility constraints

Your schedule is valid only if:

1. Every operation appears exactly once.
2. Each operation is assigned to the correct machine.
3. Operations of the same job respect precedence order.
4. Operations on the same machine do not overlap.
5. All start times are non-negative integers.

## Output format

The candidate program must write a JSON file with the following structure:

```json
{
  "instance_id": "ta01",
  "algorithm": "my_dispatch_rule",
  "operations": [
    {"job": 0, "op": 0, "machine": 4, "start": 0},
    {"job": 0, "op": 1, "machine": 1, "start": 13}
  ]
}
```

## Evaluation instances

The current starter benchmark evaluates on a fixed set of Taillard-style instances listed in `references/taillard_seeds.json`.

## Scoring

For each instance:

- compute the schedule makespan
- compute a simple lower bound:
  - max total processing time of any job
  - max total machine workload
- instance score = `lower_bound / makespan`

The final score is the mean instance score across all evaluation instances.

Invalid output receives:

- `valid = 0`
- `combined_score = 0`

## Why it fits Frontier-Eng

- realistic production planning setting
- deterministic evaluator
- clear feasibility rules
- easy to evolve from a simple dispatch rule to more advanced search

<!-- AI_GENERATED -->
