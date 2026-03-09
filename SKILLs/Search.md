# Search Skill: 从公开网页中寻找可转化为 Frontier-Eng 的工程题

## 目标

当需要为仓库补充新 benchmark 时，不要只找“相似算法题”，而要优先找能够落成真实工程任务的公开来源：

- benchmark / competition / challenge
- 官方数据集或标准实例库
- 明确输入输出协议
- 可自动评测的指标

## 进入状态

以下情况进入 `Search`：

- 主流程开始
- 上一个题目在 `Verification` 连续失败 5 次后被放弃
- 上一个题目已经完成 `PullRequest`，继续寻找下一个题

## 优先级规则

进入 `Search` 后，先检查：

- `proposals/`
- `proposals/<Domain>/<Task>/report_zh-CN.md`

如果仓库里已经存在**尚未转成 benchmark 的 proposal**，则**不要继续新搜题**，而是优先消费这些已有提案，直接转到 `Transformation`。

只有当没有待处理 proposal 时，才真正执行新的网页搜索。

## 多样性规则

为了避免题库被单一 benchmark family 过度占据，`Search` 阶段必须遵守：

1. **同一 benchmark family 只按 1 类计数**
   - 例如：CVRPLib 的多个实例只算一类
   - 例如：TSPLIB 的多个实例只算一类
2. **同一类型最多 3 道**
   - 若某一类型已达到 3 道，则暂停继续扩这个类型
3. **优先补足未覆盖类型**
   - 在继续搜新题前，先看当前题库里哪些工程类型还缺失

也就是说，`Search` 的目标不是单纯增加题目数量，而是增加**题型覆盖面**。

## 搜索流程

### 1. 先判断当前仓库里的题型本质

先读仓库总 README 和对应任务文档，判断现有题到底属于哪一类：

- 设计优化
- 控制
- 仿真
- 预测
- 调度
- 系统实现优化

避免只按表面关键词搜索。

### 2. 用“题型 + benchmark / challenge / official”搜索，而不是只搜领域名

更高效的关键词模板：

- `<domain> benchmark official`
- `<domain> challenge official`
- `<domain> competition benchmark`
- `<task type> dataset evaluator`
- `<task type> open source benchmark`

示例：

- `optimal power flow benchmark official`
- `traffic signal control benchmark SUMO`
- `building HVAC control benchmark official`
- `materials discovery benchmark official`

### 3. 优先找四类来源

按优先级排序：

1. 官方 benchmark / competition 页面
2. 官方 GitHub 仓库
3. 配套论文或组织主页
4. 可公开下载的数据与评测说明

如果只有论文、没有数据或评测协议，转化成本通常偏高。

### 4. 判断是否适合转成 Frontier-Eng

一个候选题至少检查这几项：

- **现实差距**：是不是贴近真实工程，而不是纯抽象数学题
- **经济价值**：优化结果是否会影响成本、效率、质量、安全或收益
- **可验证性**：能否写出稳定 evaluator
- **预算可控**：单次评测是否能在可接受时间内完成
- **输入输出清晰**：是否能形成 submission 契约

## 搜索时的判断框架

找到链接后，不要只记“这是什么比赛”，而要继续判断：

### A. 可以转成什么任务形式

- 参数优化
- 路径/调度规划
- 控制器设计
- 稀疏观测重建
- 结构/材料选择
- 高性能实现优化

### B. 评测器怎么写

至少要能回答：

- 输入是什么
- 输出是什么
- validity 怎么判
- score 怎么算
- 是否需要 Docker / GPU / 第三方数据

### B.1 人类最优解要求

在 `Search` 阶段，必须同时找到下面至少一种“人类最佳参考”：

- 人类最优解
- best-known solution
- best-known score
- 理论最优值（若任务确有明确理论最优）

并且要记录：

- 参考值本身
- 来源链接
- 该值如何映射到本任务的 `combined_score`

### C. 风险在哪里

常见风险：

- 依赖过重
- 数据授权不清楚
- 评测时间太长
- 容易被硬编码刷分
- 任务太像普通 ML leaderboard，不像工程 benchmark

## 产出格式建议

先做成一个统一表格，再决定是否立项：

| 领域 | 来源链接 | 工程场景 | 可转化任务 | 评分方式 | 落地难度 |
|---|---|---|---|---|---|

之后再进入 proposal/report 阶段。

## 状态转移

### 成功转移

有两种成功转移方式：

#### A. 已有 proposal 待处理

若 `proposals/` 中已有尚未落地的提案，则：

- **直接** `Search -> Transformation`

#### B. 新搜索完成 proposal

当下面这些信息已经足够清楚，并写成 proposal 后，转到 `Transformation`：

- 来源链接
- 工程场景
- 输入 / 输出
- validity
- score
- human best / best-known
- 主要风险
- 当前类型未超过多样性上限

建议产出：

- `proposals/README_zh-CN.md`
- `proposals/<Domain>/<Task>/report_zh-CN.md`

### 失败转移

如果当前候选题存在以下问题，则保持在 `Search`，继续换题：

- 题源不稳定
- 无法定义 evaluator
- 依赖过重
- 输出契约不清晰
- 现实价值不足
- 找不到可核实的人类最优解 / best-known 参考
- 当前 benchmark family / 类型已经超出多样性上限

也就是说：

- **已有 proposal**：`Search -> Transformation`
- **新 proposal 完整**：`Search -> Transformation`
- **proposal 不成立**：`Search -> Search`

## 经验总结

### 1. 不要只沿着仓库现有领域搜

如果用户说“希望越多样越好”，要主动扩到：

- 电力系统
- 建筑能源
- 制造调度
- 水务
- 农业
- 港口
- 材料
- 增材制造
- 电池
- 遥感卫星
- 仓储机器人

### 2. 最容易落地的题往往不是最炫的题

优先做这些：

- 有公开 benchmark 实例
- 有简单明确的 submission 格式
- 有轻量 evaluator
- 不依赖罕见商业软件

### 3. 最终要沉淀成 proposal，而不是只给链接

真正可用的搜索结果应该进一步写成：

- 来源
- 工程背景
- 转化方案
- 输入输出
- 评分方案
- 实现风险

这样维护者才能快速 review 是否值得立项。

<!-- AI_GENERATED -->
