# SALBP `instance_n=20_6`

## 背景

简单装配线平衡问题（SALBP）是生产系统设计中的真实工程优化问题。实际目标是在满足节拍和 precedence 约束的前提下，尽量减少工位数量，从而降低人工和产线成本。

## 实例设定

本任务使用官方 benchmark 实例 `instance_n=20_6`。

- 任务数：20
- 节拍：1000
- 官方最优工位数：3

## 候选输出

候选程序需要输出：

```json
{
  "instance_name": "instance_n=20_6",
  "priority_order": [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
  "method": "..."
}
```

评测器会把该优先级顺序放入一个确定性的串行工位分配过程。

## 有效性约束

只有满足以下条件，候选解才有效：

1. `priority_order` 是所有任务的一个排列。
2. 评测器能够构造出完整可行的工位分配。
3. 所有 precedence 约束满足。
4. 任意工位总时长不超过节拍。

## 评分方式

- `used_stations` = 评测器最终使用的工位数
- `best_known_stations = 3`
- `combined_score = 3 / used_stations`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
