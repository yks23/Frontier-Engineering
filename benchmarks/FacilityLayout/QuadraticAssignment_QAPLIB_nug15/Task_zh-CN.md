# QAPLIB nug15 二次分配问题

为每个设施分配唯一位置。

## 有效性约束

- permutation 长度必须等于 n
- 每个位置恰好出现一次

## 评分方式

- `candidate_cost` = 标准 QAP 目标值
- `best_known_cost = 1150`
- `combined_score = 1150 / candidate_cost`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
