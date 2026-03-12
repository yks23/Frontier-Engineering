# SALBP_instance_n20_6

## Overview

This benchmark is a strict transformation of the official SALBP instance `instance_n=20_6`.

It models a real assembly-line balancing problem: tasks with precedence constraints and processing times must be assigned to stations under a fixed cycle time, while minimizing the number of stations.

## Quick Start

```bash
python3 verification/evaluator.py scripts/init.py
FRONTIER_EVAL_UNIFIED_PYTHON=python3 python3 -m frontier_eval task=salbp_n20_6 algorithm.iterations=0
```

## Registered task name

`salbp_n20_6`

## Reference

- Benchmark family: SALBP
- Instance: `instance_n=20_6`
- Official best-known / optimal number of stations: `3`
- Score mapping: `combined_score = 3 / used_stations`
- `human_best_score = 1.0`

<!-- AI_GENERATED -->
