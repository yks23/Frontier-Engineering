# Verification Skill: 如何验证一个题目是对的

## 目标

确认一个新任务不是“看起来有结构”，而是真的：

- 能跑
- 能评
- 有效
- 能接入主框架

## 最小验证流程

### 1. 先做语法和路径检查

- 代码能 import / 解释执行
- `initial_program` 路径正确
- evaluator 依赖齐全
- 没有绝对路径和本地私有文件引用

### 2. 跑 benchmark 本地入口

优先跑：

```bash
python verification/evaluator.py scripts/init.py
```

必须确认：

- 退出码为 0
- `valid = 1`
- 输出格式正确
- 运行时间可接受

### 3. 跑主框架集成

再跑：

```bash
python -m frontier_eval task=<task_name> algorithm.iterations=0
```

必须确认：

- 任务能被框架加载
- baseline 能被评估
- `combined_score` 正常产生
- artifacts / history 正常落盘

### 4. 检查评分是否稳定

重点看：

- 重复运行是否抖动过大
- 非法输出是否会被正确判 0
- evaluator 是否容易被硬编码或漏洞刷分

### 5. 检查 benchmark 语义是否闭合

至少能回答：

- 什么样的输出算 valid
- 为什么这个 score 合理
- baseline 与 human best 分别是什么
- 是否存在明显不公平依赖

## 关键点

- 先验证合法性，再看分数高低
- 本地 evaluator 和主框架都必须跑通
- 测试产物不要提交进仓库
- 如果支持 `human_best_score`，确认其已进入 metrics/artifacts

<!-- AI_GENERATED -->
