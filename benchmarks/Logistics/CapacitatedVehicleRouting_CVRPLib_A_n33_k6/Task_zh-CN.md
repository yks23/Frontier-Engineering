# CVRPLib A-n33-k6 容量约束车辆路径规划

该任务使用官方 CVRPLib 实例 `A-n33-k6`。

## 有效性约束

- 每个客户恰好访问一次
- 每条路径都从 depot `1` 出发并回到 depot `1`
- 每条路径总需求不超过容量上限
- 所有节点 id 合法

## 评分方式

- `candidate_cost` = 总欧式路径成本
- `best_known_cost = 742`
- `combined_score = 742 / candidate_cost`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
