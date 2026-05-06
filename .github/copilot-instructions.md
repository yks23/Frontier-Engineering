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
