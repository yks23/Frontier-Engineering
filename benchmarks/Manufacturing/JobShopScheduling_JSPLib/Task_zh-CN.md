# 基于 Taillard / OR-Library 风格实例的作业车间调度

## 背景

该任务刻画一个典型的制造排产问题：每个工件都需要按固定顺序经过若干机器加工，目标是在满足工序先后关系和机器容量约束的前提下，生成总完工时间尽可能短的调度方案。

本 benchmark 的实例使用 OR-Library 发布的 Taillard 生成规则按固定种子生成，因此既保持了题源的公开标准性，也避免了把大量原始实例文件直接塞进仓库。

## 问题定义

给定：

- `num_jobs` 个工件
- `num_machines` 台机器
- 每个工件的一系列有序工序
- 每道工序包含：
  - 必须使用的机器
  - 加工时长

你需要为每道工序输出开始时间。

## 可行性约束

只有同时满足以下条件时，调度才有效：

1. 每道工序恰好出现一次。
2. 每道工序使用正确的机器。
3. 同一工件的工序顺序必须满足先后约束。
4. 同一机器上的任意两道工序不能重叠。
5. 所有开始时间必须是非负整数。

## 输出格式

候选程序需要写出如下 JSON：

```json
{
  "instance_id": "ta01",
  "algorithm": "my_dispatch_rule",
  "operations": [
    {"job": 0, "op": 0, "machine": 4, "start": 0},
    {"job": 0, "op": 1, "machine": 1, "start": 13}
  ]
}
```

## 评测实例

当前 starter benchmark 在 `references/taillard_seeds.json` 中列出的固定 Taillard 风格实例上评测。

## 评分方式

对每个实例：

- 计算调度的 makespan（总完工时间）
- 计算一个简单下界：
  - 任一工件总加工时间的最大值
  - 任一机器总负载的最大值
- 单实例分数 = `lower_bound / makespan`

最终分数为所有评测实例单实例分数的平均值。

若输出非法，则：

- `valid = 0`
- `combined_score = 0`

## 为什么适合 Frontier-Eng

- 对应真实制造排产场景
- evaluator 确定性强
- 约束明确，易于自动验证
- 可以从简单派工规则逐步演化到更复杂的搜索或局部优化方法

<!-- AI_GENERATED -->
