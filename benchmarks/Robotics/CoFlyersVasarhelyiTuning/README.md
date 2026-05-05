# CoFlyersVasarhelyiTuning

This benchmark is built from the released `Vasarhelyi_module/params_for_parallel` parameter sets in the `Prototype_Simulator` of the original `CoFlyers` repository.

Instead of invoking the original MATLAB/Simulink runtime directly, this task provides a **Python reimplementation** of the core flocking control law and the `evaluation_0` metric structure so that it can be evaluated uniformly inside `Frontier-Engineering`.

## Sources

- Original repository:
- Original global configuration:
- Original swarm control entry:
- Original evaluation entry:
- Original case parameter files: `Vasarhelyi_module/params_for_parallel/Vasarhelyi_module_parameters_{1..8}.m`

## Layout

```text
CoFlyersVasarhelyiTuning/
├── README.md
├── README_zh-CN.md
├── Task.md
├── Task_zh-CN.md
├── references/
│   └── coflyers_cases.json
├── scripts/
│   └── init.py
├── verification/
│   ├── evaluator.py
│   └── requirements.txt
├── baseline/
│   ├── solution.py
│   └── result_log.txt
└── frontier_eval/
    ├── initial_program.txt
    ├── candidate_destination.txt
    ├── eval_command.txt
    ├── eval_cwd.txt
    ├── agent_files.txt
    ├── artifact_files.txt
    ├── constraints.txt
    └── readonly_files.txt
```

## Quick Start

Run the evaluator inside the benchmark directory:

```bash
python verification/evaluator.py scripts/init.py
```

Run the benchmark through the unified `frontier_eval` interface from the repo root:

```bash
python -m frontier_eval \
  task=unified \
  task.benchmark=Robotics/CoFlyersVasarhelyiTuning \
  task.runtime.use_conda_run=false \
  algorithm=openevolve \
  algorithm.iterations=0
```

## Submission Interface

The candidate entrypoint is `scripts/init.py`, which must implement:

```python
def solve(problem: dict[str, Any]) -> dict[str, Any]:
    ...
```

The recommended return format is:

```python
{"params": {...}}
```

Returning a direct parameter-update dictionary is also accepted. The evaluator merges the update with the original case `baseline_params` and clips the values to valid ranges.

## Benchmark Identifier

- Unified benchmark name: `Robotics/CoFlyersVasarhelyiTuning`
- Evolvable program: `scripts/init.py`

