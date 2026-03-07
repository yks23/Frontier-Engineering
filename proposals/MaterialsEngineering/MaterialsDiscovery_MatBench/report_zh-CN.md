# Proposal Report: MaterialsDiscovery_MatBench

## 1. 题源

- MatBench: https://matbench.materialsproject.org/
- Docs: https://next-gen.materialsproject.org/ml/matbench

## 2. 建议任务名

- 目录名：`MaterialsEngineering/MaterialsDiscovery_MatBench`
- `task_name`：`materials_discovery`

## 3. 工程场景

该题可转化为**材料候选筛选与逆向发现**任务。目标是在有限实验/计算预算下，从大量候选材料中找到满足目标性能的配方或晶体结构，例如：

- 高带隙
- 低形成能
- 高弹性模量
- 可剥离性或热稳定性

适合材料发现、器件选材和实验资源分配场景。

## 4. 建议转化方式

不建议只做普通回归 leaderboard，而应转成**预算受限的发现任务**：

- 给定候选池
- 限制最多查询/评估 N 次
- 目标是在预算内找到性能最优的若干材料

这样更符合 Frontier-Eng 强调的探索与峰值表现。

## 5. 输入 / 输出建议

### 输入

- 材料候选集特征
- 允许查询预算
- 目标性质定义

### 输出

建议输出 `submission.json`：

```json
{
  "task_id": "matbench_dielectric",
  "selected_candidates": ["mat_0123", "mat_4388", "mat_2011"],
  "query_order": ["mat_1001", "mat_2011", "mat_0123"],
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 查询次数不超过预算
2. 候选 ID 合法
3. 输出格式完整

### 主指标

- `best_property_found`
- `topk_mean_property`

### 次指标

- `sample_efficiency`

### 综合分

建议：

`combined_score = 0.6 * normalized_best + 0.3 * normalized_topk + 0.1 * efficiency_score`

超预算直接 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py --candidate {candidate}`
- `constraints.txt`：说明预算约束和禁止访问隐藏标签
- `artifact_files.txt`：收集查询轨迹和发现结果表

## 8. 实现风险

- 若仅做监督学习，任务会太像普通 ML benchmark
- 需要明确“查询一次”的成本模型
- 不同 MatBench 子任务之间分数尺度差异较大

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：高

<!-- AI_GENERATED -->
