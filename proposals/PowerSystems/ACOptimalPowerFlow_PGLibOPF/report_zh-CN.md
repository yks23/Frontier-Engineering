# Proposal Report: ACOptimalPowerFlow_PGLibOPF

## 1. 题源

- PGLib-OPF: https://github.com/power-grid-lib/pglib-opf
- 论文说明页: https://www.coffrin.com/publication/pglib-opf/

## 2. 建议任务名

- 目录名：`PowerSystems/ACOptimalPowerFlow_PGLibOPF`
- `task_name`：`ac_optimal_power_flow`

## 3. 工程场景

该题可转化为**电网运行优化**任务。给定一个交流输电网络、负荷、发电机和线路约束，求一组可行运行点，使发电成本最低，同时保证：

- 节点功率平衡
- 电压幅值在允许范围内
- 发电机出力上下限满足
- 线路热稳定约束满足

这类问题直接对应调度中心和市场出清前后的运行分析，工程价值明确。

## 4. 建议转化方式

不要求 agent 从零写 AC-OPF 求解器，而是允许其在 `scripts/init.py` 中调用成熟优化库或实现启发式修正策略。

建议固定一个实例集，例如：

- 训练/公开实例：`pglib_opf_case14_ieee.m`、`case57`、`case118`、`case300`
- 测试实例：隐藏若干中大型实例

候选程序需要输出每台发电机有功/无功出力、各节点电压幅值/相角。

## 5. 输入 / 输出建议

### 输入

- 单个 MATPOWER 风格网络文件
- 可选附加约束配置（如负荷扰动、线路退化、备用要求）

### 输出

建议输出 `solution.json`：

```json
{
  "benchmark_id": "pglib_opf_case118_ieee",
  "generator_p": [ ... ],
  "generator_q": [ ... ],
  "voltage_vm": [ ... ],
  "voltage_va": [ ... ],
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 输出长度与系统维度一致
2. 潮流方程残差低于容差
3. 电压、出力、线路约束满足
4. 求解时间不超过阈值

### 主指标

- `objective_cost`: 总发电成本，越低越好

### 次指标

- `constraint_violation`: 总约束违反量，必须接近 0
- `runtime_s`: 运行时间，越短越好

### 综合分

建议采用：

- 若不可行：`valid = 0`, `combined_score = 0`
- 若可行：`combined_score = feasibility_bonus + normalized_cost_score - runtime_penalty`

更简单的版本也可以直接使用：

- `combined_score = 1 / (1 + objective_cost_scaled)`

前提是只有可行解才计分。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py --case <case> --candidate {candidate}`
- `artifact_files.txt`：收集 `solution.json`、`stdout.log`
- `constraints.txt`：说明必须输出可行 AC 潮流解，不能只给 DC 近似

## 8. 实现风险

- 依赖成熟非线性优化器时，环境可能偏重
- 需要避免把任务做成“直接调用现成最优求解器”的薄包装
- 需控制实例规模，保证评测时间稳定

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：高

<!-- AI_GENERATED -->
