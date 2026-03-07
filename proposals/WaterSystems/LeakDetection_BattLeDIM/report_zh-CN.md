# Proposal Report: LeakDetection_BattLeDIM

## 1. 题源

- BattLeDIM: https://battledim.ucy.ac.cy/
- GitHub: https://github.com/KIOS-Research/BattLeDIM
- Dataset: https://zenodo.org/records/4017659

## 2. 建议任务名

- 目录名：`WaterSystems/LeakDetection_BattLeDIM`
- `task_name`：`water_leak_detection`

## 3. 工程场景

该题可转化为**供水管网漏损检测与定位**任务。给定压力、流量和计量表时间序列，识别：

- 是否发生漏损
- 漏损开始时间
- 漏损大致位置
- 漏损规模

对应城市供水系统降损、运维巡检和告警响应。

## 4. 建议转化方式

可先采用 L-Town 固定数据集，划分公开训练期和隐藏测试期。agent 需输出一份告警文件，列出若干事件的：

- 起始时间
- 结束时间
- 位置候选
- 置信度

初版可以只做“检测 + 粗定位”，不强求精确管段识别。

## 5. 输入 / 输出建议

### 输入

- 多传感器时间序列
- 管网拓扑
- 传感器映射表

### 输出

建议输出 `alarms.csv`：

```text
start_ts,end_ts,zone_id,confidence
2019-03-01T12:00,2019-03-03T18:00,zone_12,0.87
```

## 6. 评分建议

### 有效性检查

1. 输出格式合法
2. 时间范围有效
3. 位置标签属于允许区域集合

### 主指标

- 事件检测 F1
- 平均检测延迟

### 次指标

- 定位准确率
- 误报率

### 综合分

建议：

`combined_score = 0.45 * F1 + 0.25 * location_score + 0.20 * delay_score + 0.10 * false_alarm_score`

其中：

- `delay_score = 1 / (1 + normalized_delay)`
- `false_alarm_score = max(0, 1 - false_alarm_rate)`

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py {candidate}`
- `artifact_files.txt`：收集检测事件表、误差报告和告警曲线图

## 8. 实现风险

- 数据质量和缺失值处理会显著影响公平性
- 若定位粒度太细，任务难度会陡增
- 需注意时间序列泄漏问题

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：高

<!-- AI_GENERATED -->
