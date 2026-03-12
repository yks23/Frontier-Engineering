# SALBP_instance_n20_6

## 任务概述

该 benchmark 严格基于官方 SALBP 实例 `instance_n=20_6` 转化而来。

问题对应真实装配线平衡：任务带有 precedence 关系和处理时间，需要在节拍约束下分配到工位，并尽量减少工位数量。

## 快速开始

```bash
python3 verification/evaluator.py scripts/init.py
FRONTIER_EVAL_UNIFIED_PYTHON=python3 python3 -m frontier_eval task=salbp_n20_6 algorithm.iterations=0
```

## 注册的 task_name

`salbp_n20_6`

## 参考信息

- Benchmark family：SALBP
- 实例：`instance_n=20_6`
- 官方最优工位数：`3`
- 分数映射：`combined_score = 3 / used_stations`
- `human_best_score = 1.0`

<!-- AI_GENERATED -->
