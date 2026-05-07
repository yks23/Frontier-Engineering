# Frontier-Eng

English | [简体中文](README_zh-CN.md)

This repository is a benchmark for **generative optimization**: agents iteratively edit runnable engineering code, read feedback from frozen verifiers, and improve under a fixed interaction budget. The benchmark emphasizes:

- continuous reward signals instead of binary grading
- real verifiers and simulators instead of judge models
- improvement trajectories instead of single-shot answers

The released problem set currently covers **47 tasks** across computing, quantum information, operations research, robotics and control, optics and communications, and physical sciences. Most tasks start from a feasible baseline and reward iterative improvement rather than one-shot correctness.

## 0. Host Requirements

The repository-owned Python environments are automated, but a full `v1` baseline sweep still assumes a Linux host with the following capabilities already in place:

| Requirement | Needed for | Notes |
|---|---|---|
| Standard build tools and outbound network access | all setup paths | required for `uv`, Python wheels, and benchmark-local downloads |
| NVIDIA GPU + working CUDA stack | `KernelEngineering/*`, `Aerodynamics/CarAerodynamicsSensing`, selected robotics tasks | not needed for CPU-only tasks |
| Docker | `EngDesign` | needed only for that task family |
| Octave | `Astrodynamics/MannedLunarLanding` | host-level tool, not installed by `uv` |
| Extra datasets / checkpoints / third-party repos | selected tasks such as `SustainableDataCenterControl`, `CarAerodynamicsSensing`, `MolecularMechanics` | see task README files for exact paths |

Third-party benchmark sources, data/checkpoint providers, and task-defining
open-source package licenses are tracked in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
Repository-level attribution guidance is in [`NOTICE`](NOTICE), with standard
third-party license texts under [`LICENSES/third_party/`](LICENSES/third_party/).
Original Frontier-Engineering contributions are licensed under
[Apache-2.0](LICENSE); third-party materials remain under their upstream
licenses as recorded in the notice files.

If you want the task-by-task preparation details, including host-tool installation notes, read [`run.md`](run.md) before launching the full `v1` problem set.

## Quickstart

### 1. Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

### 2. Create the driver environment

From the repository root:

```bash
bash init.sh
source .venvs/frontier-eval-driver/bin/activate
```

This creates the **driver** environment used to run `python -m frontier_eval`.

### 3. Run a smoke test

```bash
python -m frontier_eval task=smoke algorithm=openevolve algorithm.iterations=0
```

This does not need an API key and is the fastest way to confirm the framework itself is wired correctly.

## Running Real Benchmarks

There are two layers of environments in this repository:

- `frontier-eval-driver`: the driver environment
- `.venvs/<runtime-name>`: task runtime environments such as `frontier-v1-main`, `frontier-v1-kernel`, and `frontier-v1-summit`

To create the v1 task runtime environments used by the released `v1` problem set:

```bash
bash scripts/env/setup_v1_task_envs.sh
```

The runtime selector now uses:

- `task.runtime.env_name=<name>` to prepend `.venvs/<name>/bin` to `PATH`
- `task.runtime.python_path=uv-env:<name>` when a task must call a runtime interpreter directly

### Single-task baseline run

No LLM key is needed for baseline-only validation:

```bash
python -m frontier_eval \
  task=unified \
  task.benchmark=WirelessChannelSimulation/HighReliableSimulation \
  algorithm=openevolve \
  algorithm.iterations=0
```

### Full `v1` baseline sweep

To validate the released `v1` problem set without any model API calls:

```bash
bash scripts/batch/validate_v1_task_envs.sh
```

That command runs the batch config for the `v1` problem set with `algorithm.iterations=0`, which evaluates each task's shipped baseline instead of asking an LLM to improve it.

If you want the full `v1` problem set with normal optimization runs later, see [`run.md`](run.md).

## Where To Go Next

- Framework commands and task onboarding: [`frontier_eval/README.md`](frontier_eval/README.md)
- Batch-running the released `v1` problem set: [`run.md`](run.md)
- Full task list: [`TASK_DETAILS.md`](TASK_DETAILS.md)
- Archived best solutions from recorded runs: [`baseline_archive/README.md`](baseline_archive/README.md)
