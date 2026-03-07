# Transformation Skill: 从已有题目汇报转成可合并到主框架的 benchmark

## 目标

把一个“题目汇报 / proposal / report”转成能进入主仓库的实际任务骨架，而不是停留在概念层。

## 流程

### 1. 先确认题目是否值得落地

至少检查四件事：

- 题源公开且可引用
- 工程场景真实，有现实价值
- 输入 / 输出能定义清楚
- 能写出稳定 evaluator

如果这四点不清楚，先不要进实现。

### 2. 先把 report 压缩成任务契约

从 proposal 中提炼出：

- 任务名称
- 输入格式
- 输出格式
- validity 规则
- score 定义
- 依赖与运行预算

目标是把“描述”变成“可执行接口”。

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

要让维护者能快速看懂：

- 这题做什么
- 怎么跑
- 怎么评分

## 关键点

- 先做可运行，再做高级版本
- score 空间要统一，最好“越大越好”
- validity 必须比 score 更硬
- 尽量优先接入 unified，减少专门 task 代码
- proposal 里的“人类最佳 / best-known”最好同步补成元数据

<!-- AI_GENERATED -->
