# Pull Request Skill: 提交一个可审查的 PR

## 目标

让维护者快速看懂：

- 你改了什么
- 为什么这样改
- 是否真的跑通过

## 流程

### 1. 提交前先清理

不要带进 PR：

- `.env`
- API key
- 临时日志
- 本地测试产物
- 绝对路径

### 2. commit 要按逻辑拆分

优先做到：

- 一个 commit 做一类事
- 消除测试产物后再提交
- commit message 直接描述改动

### 3. PR 描述最少包含什么

建议固定写：

- 任务 / 改动概述
- 背景与来源
- 关键设计选择
- 如何运行
- 测试证据

### 4. 测试证据必须真实

至少贴：

```bash
python verification/evaluator.py scripts/init.py
python -m frontier_eval task=<task_name> algorithm.iterations=0
```

并说明：

- 是否通过
- 关键输出是什么

### 5. reviewer 最关心什么

优先回答：

- 是否可复现
- 是否满足仓库结构规范
- 是否真的 valid
- 是否引入了不必要依赖
- 是否和现有框架兼容

## 关键点

- PR 不是写“我做了很多”，而是写“维护者怎么快速验证”
- 证据比描述更重要
- 对 benchmark 类改动，要说明 baseline、score、validity 和运行方式

<!-- AI_GENERATED -->
