# TSPLIB rd100 路由规划基准

该任务使用官方 TSPLIB 实例 `rd100`。

## 有效性约束

- 每个节点恰好出现一次
- 所有节点 id 合法

## 评分方式

- `candidate_cost` = 按 TSPLIB EUC_2D 取整规则计算的巡回总成本
- `best_known_cost = 7910`
- `combined_score = 7910 / candidate_cost`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
