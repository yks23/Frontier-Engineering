# Pull Request Skill: 提交一个可审查的 PR

## 目标

让维护者快速看懂：

- 你改了什么
- 为什么这样改
- 是否真的跑通过

## 进入状态

从 `Verification` 进入。进入前应当已经满足：

- 本地 evaluator 通过
- `frontier_eval` 集成通过
- 测试证据可复现
- 当前题已在独立分支中开发完成

## 前置凭证要求

如果这一阶段不仅要 push 分支，还要**真正创建 GitHub PR 对象**，则必须具备以下至少一种能力：

1. **可写 GitHub token**
   - 例如带 Pull Request 写权限的 token
2. **等价的可写 PR API / 工具**
   - 例如内部 MCP 工具或平台提供的 CreatePullRequest 能力

如果没有这些能力，就只能做到：

- push 分支
- 生成 PR 标题与描述
- 给出 PR 创建链接

但**不能真正创建 PR 对象**。

## 流程

### 1. 提交前先清理

不要带进 PR：

- `.env`
- API key
- 临时日志
- 本地测试产物
- 绝对路径

### 1.5 创建 PR 前先检查凭证

若当前任务要求“真的创建 GitHub PR 对象”，则先检查是否已提供：

- GitHub token
- 或等价的 PR 创建 API/tool

若**未提供**，则在此步骤停止，并明确要求用户提供：

- 可写 GitHub token
- 或可写 PR 工具

不要假设只靠只读 `gh` 或普通 git push 就能创建 PR。

### 2. commit 要按逻辑拆分

优先做到：

- 一个 commit 做一类事
- 消除测试产物后再提交
- commit message 直接描述改动

### 2.5 分支要求

每个题只对应一个分支，例如：

```bash
git checkout -b feat/<Domain>/<Task>
```

提交 PR 时：

- 当前分支只包含这一个题的改动
- 一个题只提一个 PR

### 3. PR 描述最少包含什么

建议固定写：

- 任务 / 改动概述
- 背景与来源
- 关键设计选择
- 如何运行
- 测试证据

### 4. 测试证据必须真实

至少贴：

```bash
python verification/evaluator.py scripts/init.py
python -m frontier_eval task=<task_name> algorithm.iterations=0
python -m frontier_eval task=<task_name> algorithm.iterations=10
```

并说明：

- 是否通过
- 关键输出是什么
- baseline score 是多少
- Qwen3-Coder 10 轮后的 best score 是多少
- 提升是否 **> 0**

### 5. reviewer 最关心什么

优先回答：

- 是否可复现
- 是否满足仓库结构规范
- 是否真的 valid
- 是否引入了不必要依赖
- 是否和现有框架兼容

## 状态转移

### 成功转移

当以下条件满足时，认为当前题的 PR 任务完成：

- 改动已提交并推送
- PR 所需说明已准备好
- 工作区干净
- 已为当前题分支单独发起 PR

此时：

1. `current_pr_count += 1`
2. 若 `current_pr_count < 10`，回到 `Search`
3. 若 `current_pr_count >= 10`，主循环停止

### 失败转移

如果在准备提交时发现：

- 测试证据不完整
- 有未清理的测试产物
- commit 内容混乱
- reviewer 关键信息缺失
- 需要创建 PR，但没有提供可写 token / PR API / PR 工具

则回到 `Verification` 或补充修正后再提交。

也就是说：

- **提交准备完成**：`PullRequest -> Search` 或 `Stop`
- **提交准备不充分**：`PullRequest -> Verification`

## 关键点

- PR 不是写“我做了很多”，而是写“维护者怎么快速验证”
- 证据比描述更重要
- 对 benchmark 类改动，要说明 baseline、score、validity 和运行方式
- 还要说明 human best / best-known，以及 Qwen3-Coder 10 轮提升证据
- 每个题一个分支、一个 PR
- 每完成一个可提交 PR，计数 +1，然后继续下一个题
- 如果任务要求“创建 GitHub PR 对象”，没有 token 或可写 PR 工具时必须向用户索取

<!-- AI_GENERATED -->
