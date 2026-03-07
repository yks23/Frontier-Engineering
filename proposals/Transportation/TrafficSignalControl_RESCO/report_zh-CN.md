# Proposal Report: TrafficSignalControl_RESCO

## 1. 题源

- RESCO: https://github.com/Pi-Star-Lab/RESCO
- SUMO-RL: https://github.com/LucasAlegre/sumo-rl

## 2. 建议任务名

- 目录名：`Transportation/TrafficSignalControl_RESCO`
- `task_name`：`traffic_signal_control`

## 3. 工程场景

该题可转化为**城市交通信号控制**任务。目标是在多路口或单路网场景下，动态调整相位与绿灯时长，减少：

- 平均等待时间
- 排队长度
- 通行时间
- 停车次数

适用于智慧交通、园区交通控制和事件扰动下的自适应控制。

## 4. 建议转化方式

使用 RESCO/SUMO 提供的固定路网与流量需求。为了适配 Frontier-Eng，建议采用“给定一次仿真 episode，输出控制器”而不是只输出静态参数。

初版可以限定为：

- 单个或 4x4 路口网格
- 每 5 秒做一次控制决策
- 固定相位集合，仅允许切换和延长

## 5. 输入 / 输出建议

### 输入

- SUMO 路网文件
- 交通流 demand 文件
- 观测字段定义（车流、队长、相位）

### 输出

两种可选形式：

1. 提交 `controller.py`
2. 提交固定时序表 `signal_plan.csv`

推荐优先采用 `controller.py`，这样更贴近在线控制。

## 6. 评分建议

### 有效性检查

1. 控制器输出合法相位
2. 满足黄灯和安全切换逻辑
3. 仿真无死锁、无崩溃

### 主指标

- `mean_waiting_time_s`
- `mean_travel_time_s`

### 次指标

- `queue_length_mean`
- `throughput`

### 综合分

建议构造越高越好的分数：

`combined_score = throughput_score - waiting_penalty - queue_penalty`

或：

`combined_score = 0.5 / (1 + normalized_waiting) + 0.5 * normalized_throughput`

若出现非法信号切换，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `candidate_destination.txt`：`controller.py`
- `eval_command.txt`：`{python} verification/evaluator.py --candidate {candidate}`
- `artifact_files.txt`：收集 `metrics.json`、路口轨迹图、队列曲线

## 8. 实现风险

- SUMO 环境依赖需要单独处理
- 评测需保证随机种子固定，降低波动
- 多路口场景可能导致运行时间增加

## 9. 推荐度

- 工程价值：高
- 可验证性：高
- 实现复杂度：中
- 推荐优先级：高

<!-- AI_GENERATED -->
