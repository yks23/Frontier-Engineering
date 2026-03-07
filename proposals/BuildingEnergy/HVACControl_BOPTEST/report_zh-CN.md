# Proposal Report: HVACControl_BOPTEST

## 1. 题源

- BOPTEST: https://ibpsa.github.io/project1-boptest/
- User Guide: https://ibpsa.github.io/project1-boptest/docs-userguide/introduction.html

## 2. 建议任务名

- 目录名：`BuildingEnergy/HVACControl_BOPTEST`
- `task_name`：`hvac_control_boptest`

## 3. 工程场景

该题可转化为**楼宇暖通空调控制**任务。目标是在真实动态建筑模型上设计控制策略，在满足舒适度约束的前提下，降低：

- 总能耗
- 峰值功率
- 电费成本
- 舒适度违约时间

对应智能楼宇、园区节能和需求响应等真实工程场景。

## 4. 建议转化方式

使用 BOPTEST 的一个固定 test case，例如中型办公楼或多分区建筑。agent 在给定天气和电价信息下，输出逐时段控制信号：

- 送风温度设定值
- 冷冻水温度设定值
- 设备启停/功率命令

为降低复杂度，建议先只开放监督控制层，不让 agent 修改底层设备模型。

## 5. 输入 / 输出建议

### 输入

- 固定建筑 test case
- 天气预测
- 电价序列
- KPI 约束配置

### 输出

建议输出 `control_schedule.csv`：

```text
time,ahu_supply_temp,chiller_setpoint,zone_temp_sp
0, ...
900, ...
```

也可允许提交 Python 控制器，由 evaluator 与仿真环境交互。

## 6. 评分建议

### 有效性检查

1. 控制信号格式正确
2. 所有控制量在安全范围内
3. 仿真全程无崩溃

### 主指标

- `energy_kwh`
- `cost_total`

### 次指标

- `comfort_violation_degree_hours`
- `peak_power_kw`

### 综合分

建议采用加权最小化后映射为越高越好的分数：

`penalty = w1 * normalized_energy + w2 * normalized_cost + w3 * normalized_comfort + w4 * normalized_peak`

`combined_score = max(0, 1 - penalty)`

若舒适度严重违约，则直接 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py {candidate}`
- `copy_files.txt`：复制固定 building case 和天气文件
- `artifact_files.txt`：收集 KPI 报告、控制轨迹图

## 8. 实现风险

- BOPTEST 依赖较重，Docker 化更合适
- 单次评测时间可能偏长，需要限制仿真周期
- 需避免控制器通过利用仿真漏洞获得不合理高分

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中高
- 推荐优先级：高

<!-- AI_GENERATED -->
