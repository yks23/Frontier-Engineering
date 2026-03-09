# Proposal Report: CapacitatedVehicleRouting_CVRPLibXML

## 1. 题源

- CVRPLib: https://galgos.inf.puc-rio.br/cvrplib/
- All Instances: https://galgos.inf.puc-rio.br/cvrplib/
- BKS / Overview: https://galgos.inf.puc-rio.br/cvrplib/index.php/en/bks_challenge/overview
- DIMACS CVRP Track: http://dimacs.rutgers.edu/programs/challenge/vrp/cvrp/

## 2. 建议任务名

- 目录名：`Logistics/CapacitatedVehicleRouting_CVRPLibXML`
- `task_name`：`capacitated_vehicle_routing`

## 3. 工程场景

该题可转化为**物流配送路径规划**任务。给定：

- 仓库/配送中心位置
- 客户需求
- 车辆容量
- 距离或坐标信息

目标是在满足容量约束的前提下最小化总路程或总成本。

这直接对应：

- 城市末端配送
- 仓配一体调度
- 生鲜/快递车队路径规划

## 4. 选择这个题的原因

它满足新的 Search 标准：

1. **真实工程问题**：CVRP 是经典物流工程问题，不是纯数学玩具题。
2. **官方 benchmark 稳定**：CVRPLib 是公开且长期维护的标准基准库。
3. **有明确 human best / best-known**：
   - CVRPLib 官方维护 best-known solutions
   - **XML set 的 10,000 个 100 客户实例全部有已知最优解**
4. **后续可做 1:1 复刻**：
   - 输入可以保持标准 VRP 格式
   - 输出可以保持真实 route 列表
   - score 可以直接相对最优成本计算

## 5. human best / best-known

### 可核实参考

根据 CVRPLib 官方说明：

- **XML set**：10,000 个 100 客户实例
- **All XML instances have known optimal solutions**

因此，这个题可以天然满足：

- `human_best_score` 来自官方最优解
- 可精确映射，而不是模糊参考

### 建议的 score 映射

若原始目标是最小化 route cost，设：

- `best_known_cost` = 官方最优解成本
- `candidate_cost` = 候选解成本

建议：

- `combined_score = best_known_cost / candidate_cost`

这样：

- 最优解分数 = `1.0`
- 次优解分数 < `1.0`
- 非法解分数 = `0`

这非常适合后续统一 `human_best_score = 1.0`

## 6. 1:1 复刻建议

为了满足新的 Transformation 约束，建议尽量 1:1 保留真实问题结构：

### 输入

- depot
- customer coordinates / distance matrix
- customer demand
- vehicle capacity

### 输出

- 显式 route 列表
- 每条 route 从 depot 出发并回到 depot

### 约束

- 每个客户恰好访问一次
- 每条车路径总需求不超过容量
- route 合法闭合

### 目标

- 最小化总里程 / 总成本

不要把它简化成：

- 只输出客户排序
- 不显式检查 route feasibility
- 不按真实 route cost 评分

## 7. evaluator 建议

### validity 检查

1. 所有客户被访问且仅访问一次
2. 路径起终点是 depot
3. 每条 route 的需求和不超过容量
4. 输出格式正确

### 主指标

- `candidate_cost`

### 综合分

- `combined_score = best_known_cost / candidate_cost`

### human best

- `human_best_score = 1.0`

## 8. 推荐的首批实例

建议首批不要直接接 10,000 个实例，而是从 XML set 中挑一个小批次：

- 若干 100-customer 实例
- 都带官方最优解

这样：

- evaluator 稳定
- human best 明确
- 后续更容易做 Qwen3-Coder 10 轮对比

## 9. 风险

- 如果 baseline 太弱，Qwen 10 轮很容易提升，但区分度可能不足
- 如果 baseline 太强，可能又会出现“10 轮不提升”的验证失败
- 需要谨慎挑实例，既要真实，又要便于演化

## 10. 推荐度

- 工程价值：高
- 可验证性：高
- human best 清晰度：高
- 1:1 复刻可行性：高
- 推荐优先级：高

<!-- AI_GENERATED -->
