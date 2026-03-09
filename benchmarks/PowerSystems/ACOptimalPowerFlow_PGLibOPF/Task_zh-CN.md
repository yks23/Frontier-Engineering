# 小型最优潮流任务

选择发电机出力和母线相角。

## 输出

写出 `solution.json`：

```json
{
  "benchmark_id": "opf_small_v1",
  "generator_p": [1.2, 0.6],
  "theta": [0.0, -0.1, -0.2],
  "method": "..."
}
```

## 有效性约束

只有满足以下条件时解才有效：

1. 发电机出力在上下限内
2. 线路潮流不超过热限额
3. 节点功率平衡残差低于容差
4. 平衡母线相角固定为 0

## 评分方式

有效解：`combined_score = 1 / (1 + generation_cost)`。
非法输出记 0 分。

<!-- AI_GENERATED -->
