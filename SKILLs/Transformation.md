# Transformation Skill: 从已有题目汇报转成可合并到主框架的 benchmark

## 目标

把一个“题目汇报 / proposal / report”转成能进入主仓库的实际任务骨架，而不是停留在概念层。

## 进入状态

从 `Search` 进入。进入前应当已经存在：

- `proposals/<Domain>/<Task>/report_zh-CN.md`

同时应当先切到当前题独立分支：

- `feat/<Domain>/<Task>`

## 流程

### 1. 先确认题目是否值得落地

至少检查四件事：

- 题源公开且可引用
- 工程场景真实，有现实价值
- 输入 / 输出能定义清楚
- 能写出稳定 evaluator
- 已经有可核实的人类最优解 / best-known 参考

如果这四点不清楚，先不要进实现。

### 2. 先把 report 压缩成任务契约

从 proposal 中提炼出：

- 任务名称
- 输入格式
- 输出格式
- validity 规则
- score 定义
- 依赖与运行预算
- human best / best-known 如何映射到 `combined_score`

目标是把“描述”变成“可执行接口”。

### 2.5 1:1 复刻要求

Transformation 阶段要尽量做到：

- **1:1 复刻真实问题的核心结构**
- 不要把真实工程问题过度降维成无关的抽象玩具题

可以做轻量化，但必须保留真实问题的关键组成：

- 真实输入结构
- 真实约束类型
- 真实目标函数方向
- 真实输出契约

### 3. 先做最小可运行版本

优先补齐：

- `scripts/init.py`
- `verification/evaluator.py`
- `verification/requirements.txt`
- `frontier_eval/*.txt`

如果是 unified task，再补：

- `frontier_eval/initial_program.txt`
- `eval_command.txt`
- `constraints.txt`

### 4. baseline 要求

baseline 不必强，但必须：

- 自包含
- 合法可运行
- 产生非零有效分
- 方便后续演化

不要一开始就把 baseline 做成很重的大系统。

### 5. 文档最少要补什么

即使只做 starter，也建议补：

- `README.md / README_zh-CN.md`
- `Task.md / Task_zh-CN.md`

并明确记录：

- human best / best-known
- 来源链接
- 是否已写入统一元数据（如 `human_best_score.txt`）

要让维护者能快速看懂：

- 这题做什么
- 怎么跑
- 怎么评分

### 6. 分支边界

一个题只在一个分支里完成：

- 当前题的 benchmark 文件
- 当前题的 `frontier_eval/conf/task/<task_name>.yaml`
- 当前题自己的文档和元数据

不要把别的题顺手混进同一个分支。

## 状态转移

### 成功转移

当最小任务骨架已经形成时，转到 `Verification`：

- baseline 自包含
- evaluator 可调用
- unified 元数据已补齐（若适用）
- README / Task 文档可供检查
- 已记录 human best / best-known
- 已尽量 1:1 保留真实问题核心结构

目标路径通常是：

- `benchmarks/<Domain>/<Task>/`
- `frontier_eval/conf/task/<task_name>.yaml`（若需要）

### 失败转移

若在转化过程中发现 proposal 本身无法闭合，例如：

- 输入输出无法定义
- evaluator 难以稳定实现
- baseline 无法做成最小可运行版本
- 为了省事把问题改得与真实场景脱节
- 无法在任务中明确记录 human best / best-known

则删除半成品代码并回到 `Search`：

- 删除 `benchmarks/<Domain>/<Task>/`
- 删除 `frontier_eval/conf/task/<task_name>.yaml`（若已创建）

也就是说：

- **最小骨架完成**：`Transformation -> Verification`
- **任务契约无法落地**：`Transformation -> Search`

## 关键点

- 先做可运行，再做高级版本
- score 空间要统一，最好“越大越好”
- validity 必须比 score 更硬
- 尽量优先接入 unified，减少专门 task 代码
- proposal 里的“人类最佳 / best-known”最好同步补成元数据
- Transformation 的目标不是“做个像的”，而是尽量 1:1 复刻真实问题
- 做不出最小闭环时，不要硬撑，直接回 Search

<!-- AI_GENERATED -->
