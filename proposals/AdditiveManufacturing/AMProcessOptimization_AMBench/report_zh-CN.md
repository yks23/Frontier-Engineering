# Proposal Report: AMProcessOptimization_AMBench

## 1. 题源

- NIST AM-Bench: https://www.nist.gov/ambench
- Challenge list: https://www.nist.gov/ambench/challenges-and-descriptions

## 2. 建议任务名

- 目录名：`AdditiveManufacturing/AMProcessOptimization_AMBench`
- `task_name`：`am_process_optimization`

## 3. 工程场景

该题可转化为**增材制造工艺参数优化**任务。目标是在指定材料和零件几何下选择工艺参数，以改善：

- 残余应力
- 翘曲变形
- 微结构目标
- 冷却速率和缺陷风险

适用于金属 3D 打印工艺开发、工艺窗口探索和质量控制。

## 4. 建议转化方式

建议不要让 agent 直接做全物理仿真，而是基于 AM-Bench 公开测量数据，构建一个“参数搜索 + 代理评估”的任务。

初版可固定：

- 激光功率
- 扫描速度
- hatch spacing
- layer thickness

候选程序输出一组参数配置，评测器调用代理模型或简化仿真估计质量指标。

## 5. 输入 / 输出建议

### 输入

- 材料类型
- 几何/零件类型
- 参数边界
- 工艺约束

### 输出

建议输出 `process_params.json`：

```json
{
  "material": "IN625",
  "laser_power": 230.0,
  "scan_speed": 800.0,
  "hatch_spacing": 0.11,
  "layer_thickness": 0.04,
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 参数在合法边界内
2. 满足制造约束组合
3. 输出格式正确

### 主指标

- `distortion_mm`
- `residual_stress_score`

### 次指标

- `productivity_score`
- `defect_risk`

### 综合分

建议：

`penalty = a * distortion + b * stress + c * defect_risk - d * productivity_bonus`

`combined_score = 1 / (1 + penalty)`

若参数非法，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py {candidate}`
- `artifact_files.txt`：收集参数配置、代理预测结果和可视化图

## 8. 实现风险

- 直接接高保真仿真会过重
- 代理模型的可信度需要说明
- 要避免任务退化为简单黑箱数值优化

## 9. 推荐度

- 工程价值：高
- 可验证性：中高
- 实现复杂度：中
- 推荐优先级：中高

<!-- AI_GENERATED -->
