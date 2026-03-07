# Proposal Report: EarthObservationScheduling_GECCO2025

## 1. 题源

- GECCO 2025 Competition: https://gecco-2025.sigevo.org/Competition?itemId=2389
- ESA Kelvins: https://kelvins.esa.int/

## 2. 建议任务名

- 目录名：`SatelliteOperations/EarthObservationScheduling_GECCO2025`
- `task_name`：`earth_observation_scheduling`

## 3. 工程场景

该题可转化为**遥感卫星任务调度**任务。给定卫星轨道窗口、姿态机动约束、云层预测和客户成像请求，生成成像计划，使：

- 服务收益最大
- 超时/漏单最少
- 机动代价受控
- 可执行性满足

非常贴近商业遥感卫星运营与任务规划。

## 4. 建议转化方式

建议固定一个 12 小时或 24 小时规划窗口，使用离散成像机会集。候选程序输出被接受的任务集合及执行顺序。

初版只做单星或双星，后续再扩展到多星协同和应急插单。

## 5. 输入 / 输出建议

### 输入

- 卫星和姿态机动约束
- 成像机会列表
- 任务收益、时窗和云量信息

### 输出

建议输出 `plan.json`：

```json
{
  "horizon": "12h",
  "selected_observations": [
    {"obs_id": "req_001", "start": 5120},
    {"obs_id": "req_104", "start": 8775}
  ],
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 所选任务均在合法时间窗内
2. 相邻任务满足机动和姿态可达性
3. 同一资源无冲突

### 主指标

- `total_reward`

### 次指标

- `completion_rate`
- `slew_cost`
- `cloud_penalty`

### 综合分

建议：

`combined_score = normalized_reward + 0.2 * completion_rate - 0.1 * slew_penalty - 0.1 * cloud_penalty`

若计划不可执行，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py --candidate {candidate}`
- `artifact_files.txt`：收集甘特图、任务完成清单和收益分解

## 8. 实现风险

- 若实例规模过大，评测时间和搜索空间都会爆炸
- 需谨慎定义隐藏测试集，避免过拟合固定机会集
- 云量和收益模型应保持公开透明

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：高

<!-- AI_GENERATED -->
