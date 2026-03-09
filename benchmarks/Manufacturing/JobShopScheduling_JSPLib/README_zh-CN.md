# JobShopScheduling_JSPLib

## 快速开始

在本 benchmark 目录下运行：

```bash
python3 verification/evaluator.py scripts/init.py
python3 -m frontier_eval task=jobshop_scheduling algorithm.iterations=0
```

## 文件说明

- `Task_zh-CN.md`：任务定义与评分方式
- `references/taillard_seeds.json`：题源与实例元数据
- `scripts/init.py`：自包含初始解
- `verification/evaluator.py`：评测入口
- `frontier_eval/`：unified task 接入元数据

## 参考分数

- `human_best_score = 0.7967499751439758`
- 该值由公开 best-known makespan（`ta01=1231`, `ta02=1244`, `ta11=1357`）按本任务评分公式换算得到

## 注册的 task_name

`jobshop_scheduling`

<!-- AI_GENERATED -->
