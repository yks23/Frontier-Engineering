# Proposal Report: WindFarmLayoutOptimization

## 1. 题源

- Competition: https://www.irit.fr/wind-competition/2014/
- TOPFARM: https://topfarm.pages.windenergy.dtu.dk/TopFarm2/

## 2. 建议任务名

- 目录名：`RenewableEnergy/WindFarmLayoutOptimization`
- `task_name`：`wind_farm_layout_optimization`

## 3. 工程场景

该题可转化为**风机布局优化**任务。目标是在场址边界、最小机间距和风况分布约束下，选择风机坐标，以提升：

- 年发电量（AEP）
- 度电成本表现
- 尾流损失控制
- 土地利用效率

对应风场前期规划与重新扩容设计场景。

## 4. 建议转化方式

初版建议采用固定数量风机、固定场址边界的布局问题，避免变量数量和约束过多。agent 输出所有风机二维坐标，评测器使用简化尾流模型计算 AEP。

后续可扩展：

- 多风向玫瑰图
- 禁建区
- 电缆长度成本
- 维护通道约束

## 5. 输入 / 输出建议

### 输入

- 场地边界多边形
- 风机数量
- 风资源分布
- 最小间距约束

### 输出

建议输出 `layout.json`：

```json
{
  "site_id": "site_a",
  "turbines": [
    {"x": 120.0, "y": 330.0},
    {"x": 240.0, "y": 420.0}
  ],
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 风机数量正确
2. 全部坐标在场地内
3. 两两间距满足最小要求

### 主指标

- `aep_mwh`: 年发电量，越高越好

### 次指标

- `wake_loss_pct`: 尾流损失比例
- `cable_length_est`: 估计集电线路长度

### 综合分

建议：

`combined_score = aep_score - wake_penalty - cable_penalty`

如违反边界或间距约束，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py --candidate {candidate}`
- `artifact_files.txt`：收集布局图、功率玫瑰图和 `layout.json`

## 8. 实现风险

- 尾流模型选择会影响题目真实性与计算开销
- 若只用简化模型，可能被质疑现实性不足
- 若采用高保真模型，评测时间会过长

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：中高

<!-- AI_GENERATED -->
