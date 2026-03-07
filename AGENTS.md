# Agents Guide

## Cursor Cloud specific instructions

### Environment overview

Frontier-Eng is a Python-based AI agent evaluation framework (CLI tool, not a web app). It uses **conda** (`frontier-eval-2` env, Python 3.12) for environment isolation. The primary entrypoint is `python -m frontier_eval`.

Miniconda is installed at `$HOME/miniconda3`. To activate it in a shell session:

```bash
eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
conda activate frontier-eval-2
```

On first use in a new shell, you must accept conda TOS channels if not already done:

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

### Running the framework

See `frontier_eval/README.md` for full usage. Quick smoke test (no API key needed):

```bash
python -m frontier_eval task=smoke algorithm=openevolve algorithm.iterations=0
```

For evolution runs with `iterations > 0`, set `OPENAI_API_KEY` in `.env` (copy from `.env.example`).

### Linting and testing

The project has no formal linting config. `ruff` and `pytest` are installed in the conda env for ad-hoc use:

- Lint: `ruff check frontier_eval/ --select E,F,W --ignore E501,E402`
- Test: `pytest benchmarks/WirelessChannelSimulation/HighReliableSimulation/tests/ -v`

### Key gotchas

- The `algorithm=abmcts` and `algorithm=shinkaevolve` smoke tests require optional repos cloned under `third_party/` — see `frontier_eval/README.md` for setup.
- Octave + signal/control packages (installed by `init.sh` via conda-forge) are only needed for the `MannedLunarLanding` benchmark.
- Some benchmarks need specific system toolchains: `g++` for Cryptographic tasks, `make`/`gcc` for MallocLab, Docker for EngDesign, GPU/CUDA for KernelEngineering. These are pre-installed or available except Docker and GPU.
- The framework uses Hydra for config management. Run output goes to `runs/` directory.
- `conda run -n frontier-eval-2` is used internally by the unified task runner, so conda env must be properly set up even if you activate it differently.
