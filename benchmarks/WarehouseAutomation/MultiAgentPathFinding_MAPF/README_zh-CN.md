# MultiAgentPathFinding_MAPF

## 快速开始

在本 benchmark 目录下运行：

```bash
python3 verification/evaluator.py scripts/init.py
python3 -m frontier_eval task=multi_agent_path_finding algorithm.iterations=0
```

## 文件说明

- `Task_zh-CN.md`：任务定义
- `references/instance.json`：仓库地图和机器人配置
- `scripts/init.py`：自包含初始解
- `verification/evaluator.py`：评测入口
- `frontier_eval/`：unified task 接入元数据

## 注册的 task_name

`multi_agent_path_finding`

<!-- AI_GENERATED -->
