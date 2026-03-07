# Proposal Report: MultiAgentPathFinding_MAPF

## 1. 题源

- MAPF Benchmarks: https://movingai.com/benchmarks/mapf.html
- MAPF community: https://mapf.info/

## 2. 建议任务名

- 目录名：`WarehouseAutomation/MultiAgentPathFinding_MAPF`
- `task_name`：`multi_agent_path_finding`

## 3. 工程场景

该题可转化为**仓储多机器人协同路径规划**任务。给定仓库地图、多个机器人起终点和时间同步约束，生成无碰撞路径，使：

- 总完工时间最短
- 总步长尽量小
- 拥堵和局部死锁少

适用于自动化仓储、分拣中心和搬运机器人系统。

## 4. 建议转化方式

建议选用官方 warehouse map，并将任务表述为：

- 输入：一个固定批次的订单搬运请求
- 输出：所有机器人离散时间路径

初版只要求静态环境；进阶版可加入动态任务插入和临时封路。

## 5. 输入 / 输出建议

### 输入

- 栅格地图
- 机器人起点和目标点
- 时间步上限

### 输出

建议输出 `paths.json`：

```json
{
  "map_id": "warehouse-10-20-10-2-1",
  "paths": {
    "agent_0": [[1, 1], [1, 2], [1, 3]],
    "agent_1": [[2, 1], [2, 1], [2, 2]]
  },
  "method": "..."
}
```

## 6. 评分建议

### 有效性检查

1. 路径起终点正确
2. 不允许顶点冲突和边冲突
3. 路径长度不超过时间上限

### 主指标

- `makespan`

### 次指标

- `sum_of_costs`
- `throughput`

### 综合分

建议：

`combined_score = 0.6 / makespan + 0.4 / sum_of_costs`

若任一冲突存在，则 `valid = 0`。

## 7. frontier_eval 接入建议

- `initial_program.txt`：`scripts/init.py`
- `eval_command.txt`：`{python} verification/evaluator.py {candidate}`
- `artifact_files.txt`：收集路径动画、冲突分析和 `paths.json`

## 8. 实现风险

- 纯 MAPF 容易被认为偏算法题，需要在叙述中强化仓储场景
- 若地图过小，区分度不足；过大则求解时间会暴涨

## 9. 推荐度

- 工程价值：中高
- 可验证性：高
- 实现复杂度：低中
- 推荐优先级：中高

<!-- AI_GENERATED -->
