# 遥感卫星任务调度

在给定观测机会表中选择一个可执行的子集和执行顺序。

## 有效性约束

只有满足以下条件时，调度才有效：

1. 选中的观测机会必须存在于机会表中。
2. 观测按执行时间非递减排序。
3. 每个观测的开始时间必须在允许时间窗内。
4. 相邻观测之间必须满足姿态切换时间要求。
5. 不能超过规划时域上限。

## 输出

写出 `plan.json`：

```json
{
  "horizon": 360,
  "method": "...",
  "selected_observations": [
    {"obs_id": "obs_01", "start": 15}
  ]
}
```

## 评分方式

对于有效计划：

- `combined_score = total_reward - 0.1 * slew_cost`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
