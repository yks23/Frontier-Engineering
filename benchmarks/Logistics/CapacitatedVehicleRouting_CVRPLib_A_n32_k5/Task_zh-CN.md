# CVRPLib A-n32-k5 容量约束车辆路径规划

该任务使用官方 CVRPLib 实例 `A-n32-k5`。

## 输入

实例包含：

- 1 个 depot
- 客户坐标
- 客户需求
- 车辆容量上限

## 输出

写出 `solution.json`：

```json
{
  "instance_name": "A-n32-k5",
  "routes": [[1, 5, 7, 1]],
  "method": "..."
}
```

每条路径都必须以 depot `1` 开始并以 depot `1` 结束。

## 有效性约束

只有满足以下条件时解才有效：

1. 每个客户（除 depot 外的节点）恰好访问一次。
2. 每条路径都从 depot `1` 出发并回到 depot `1`。
3. 每条路径总需求不超过容量上限。
4. 所有节点 id 合法。

## 评分方式

- `candidate_cost` = 总欧式路径成本
- `best_known_cost = 784`
- `combined_score = 784 / candidate_cost`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
