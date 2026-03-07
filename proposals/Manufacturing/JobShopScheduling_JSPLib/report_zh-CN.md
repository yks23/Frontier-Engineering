# Proposal Report: JobShopScheduling_JSPLib

## 1. 题源

- JSPLib: https://scheduleopt.github.io/benchmarks/jsplib
- OR-Library Job Shop: https://people.brunel.ac.uk/~mastjjb/jeb/orlib/jobshopinfo.html

## 2. 建议任务名

- 目录名：`Manufacturing/JobShopScheduling_JSPLib`
- `task_name`：`jobshop_scheduling`

## 3. 工程场景

该题可转化为**离散制造排产**任务。给定多工件、多工序、多台机器，要求生成可行排程，降低：

- 总完工时间（makespan）
- 延迟订单数
- 机器空闲时间
- 换线或切换成本

适用于机械加工、电子装配、半导体后段制造等场景。

## 4. 建议转化方式

初版可采用经典 job shop 实例，后续再增加工程化扩展：

- due date
- machine breakdown
- sequence-dependent setup time
- energy-aware scheduling

候选程序输出每道工序的开始时间和机器分配。

## 5. 输入 / 输出建议

### 输入

- 标准 job shop 实例文件
- 可选订单优先级和交期配置

### 输出

建议输出 `schedule.json`：

```json
{
  "instance_id": "ta20",
  "operations": [
    {"job": 0, "op": 0, "machine": 2, "start": 15},
    {"job": 0, "op": 1, "machine": 1, "start": 42}
  ],
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 同一工件的工序顺序正确
2. 同一机器任意时刻只执行一个工序
3. 开始时间非负且处理时间满足

### 主指标

- `makespan`

### 次指标

- `total_tardiness`
- `machine_idle_ratio`

### 综合分

对单指标版本，建议直接：

- 可行则 `combined_score = 1 / makespan`
- 不可行则 `combined_score = 0`

对工程化版本，可使用：

`combined_score = 1 / (1 + a * makespan + b * tardiness + c * setup_cost)`

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py --instance hidden_case.json --candidate {candidate}`
- `artifact_files.txt`：收集甘特图和 `schedule.json`

## 8. 实现风险

- 纯经典 JSP 会显得偏 OR 教学题，需要加入现实约束增强工程味
- 大实例求解时间差异很大，需限制运行预算

## 9. 推荐度

- 工程价值：中高
- 可验证性：高
- 实现复杂度：低中
- 推荐优先级：中高

<!-- AI_GENERATED -->
