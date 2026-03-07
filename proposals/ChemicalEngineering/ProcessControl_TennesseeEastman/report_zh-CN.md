# Proposal Report: ProcessControl_TennesseeEastman

## 1. 题源

- Archive: https://depts.washington.edu/control/LARRY/TE/download.html
- GitHub mirror: https://github.com/camaramm/tennessee-eastman-challenge

## 2. 建议任务名

- 目录名：`ChemicalEngineering/ProcessControl_TennesseeEastman`
- `task_name`：`process_control_tennessee_eastman`

## 3. 工程场景

该题可转化为**化工过程控制与异常应对**任务。目标是在复杂耦合化工流程中，使系统在扰动或故障下：

- 保持产品质量
- 降低波动
- 避免设备约束触发
- 维持稳定运行

适合真实工业控制和过程安全场景。

## 4. 建议转化方式

推荐分两期：

1. 初版：故障检测与诊断
2. 进阶版：给定可控变量接口，输出控制策略

如果优先追求可验证性，建议先做“控制器调参/监督控制”而不是低层连续控制，降低实现难度。

## 5. 输入 / 输出建议

### 输入

- 多变量过程时间序列
- 初始稳态条件
- 扰动/故障脚本

### 输出

可选两种任务形式：

1. `fault_report.csv`：输出故障类型和发生时间
2. `controller.py`：输出每个控制周期的设定值修正

建议优先做第 2 种，更符合工程控制题。

## 6. 评分建议

### 有效性检查

1. 仿真全程不崩溃
2. 控制量在允许范围内
3. 安全约束不被严重违反

### 主指标

- `quality_loss`
- `constraint_violation_integral`

### 次指标

- `control_effort`
- `recovery_time`

### 综合分

建议：

`combined_score = max(0, 1 - a * quality_loss - b * violation - c * control_effort - d * recovery_time)`

若触发硬安全约束，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `candidate_destination.txt`：`controller.py`
- `eval_command.txt`：`{python} verification/evaluator.py {candidate}`
- `artifact_files.txt`：收集关键变量趋势图和告警日志

## 8. 实现风险

- 模型和仿真依赖老旧，需要适配现代环境
- 连续控制任务需要谨慎设计动作空间
- 安全约束定义不清会导致刷分漏洞

## 9. 推荐度

- 工程价值：高
- 可验证性：中高
- 实现复杂度：中高
- 推荐优先级：中高

<!-- AI_GENERATED -->
