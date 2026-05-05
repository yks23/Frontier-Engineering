# Frontier-Engineering Copilot Instructions

## Running Evaluations

1. Read `frontier_eval/README.md` and the relevant benchmark README first.
2. Discover env docs:
   - `python .claude/skills/scripts/discover_env_docs.py <Domain>`
   - `python .claude/skills/scripts/discover_env_docs.py <Domain>/<Task>`
   - `python .claude/skills/scripts/discover_env_docs.py --matrix frontier_eval/conf/batch/example_matrix.yaml`
3. Keep driver env and benchmark runtime env separated.
4. Run evaluations with:
   - `python -m frontier_eval task=unified task.benchmark=<Domain>/<Task> algorithm=openevolve algorithm.iterations=0`
   - `python -m frontier_eval.batch --matrix frontier_eval/conf/batch/example_matrix.yaml`

## Working with benchmark tasks

1. Read `frontier_eval/README.md` and related benchmark READMEs.
2. Prefer unified onboarding (`task=unified`) for new benchmark-style tasks.
3. Keep editable logic in `scripts/init.py` and evaluator logic in `verification/evaluator.py`.
4. Validate with:
   - `python verification/evaluator.py scripts/init.py`
   - `python -m frontier_eval task=unified task.benchmark=<Domain>/<Task> algorithm=openevolve algorithm.iterations=0`
5. Keep runtime overrides unchanged and avoid secrets or machine-local paths.
