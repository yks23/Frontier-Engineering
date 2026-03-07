# 预算受限的材料发现任务

在固定查询预算下选择候选材料。

## 输入

benchmark 提供一个候选表，包含数值描述符和隐藏目标性质。

## 输出

写出 `submission.json`：

```json
{
  "task_id": "matbench_small_v1",
  "query_order": ["mat_001", "mat_002"],
  "selected_candidates": ["mat_010", "mat_014"],
  "method": "..."
}
```

## 有效性约束

只有满足以下条件时提交才有效：

1. `query_order` 长度不能超过查询预算。
2. 所有候选 id 都必须存在。
3. `selected_candidates` 不能为空，且只能包含合法 id。
4. 不允许重复 id。

## 评分方式

对于有效提交：

- `best_property_found` = 选中候选中的最佳隐藏性质
- `topk_mean_property` = 选中候选的平均隐藏性质
- `query_efficiency = 1 - len(query_order)/budget`
- `combined_score = 0.6 * best_property_found + 0.3 * topk_mean_property + 0.1 * query_efficiency`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
