# Main Flow Skill: 从新题想法到可合并 PR 的四步主流程

## 目标

后续只要给出这一个主流程 skill，就能按固定顺序反复执行完整任务：

1. 搜题 / 立项
2. 转题 / 落地
3. 验证 / 跑通
4. 提 PR / 提交

## 主循环

设：

- `target_pr_count = 10`
- `current_pr_count = 已完成的新题 PR 数量`

总循环规则：

- 只要 `current_pr_count < target_pr_count`，就从 `Search` 开始下一题
- 只有当 `current_pr_count >= target_pr_count` 时，主流程才停止
- 进入 `Search` 后，**优先处理 `proposals/` 中已有待落地 proposal**
- 只有当没有待处理 proposal 时，才执行新的网页搜题

状态机可写成：

`Search -> Transformation -> Verification -> PullRequest -> Search`

其中：

- `Verification` 失败时会回退
- `PullRequest` 成功时 `current_pr_count += 1`

---

## Step 1 — Search

### 使用的子技能

- `SKILLs/Search.md`

### 要做什么

先检查 `proposals/` 中是否已有待处理提案：

- 如果有：直接挑一个进入 `Transformation`
- 如果没有：再从公开 benchmark / competition / dataset 中找候选题

### 产出路径

优先产出到：

- `proposals/README_zh-CN.md`
- `proposals/<Domain>/<Task>/report_zh-CN.md`

### 完成标志

至少明确：

- 题源链接
- 工程场景
- 输入 / 输出
- 评分方式
- 风险

如果这些不清楚，不进入 Step 2。

### 状态转移

- 已有 proposal 待处理：`Search -> Transformation`
- 新 proposal 完整：`Search -> Transformation`
- proposal 不成立：`Search -> Search`

---

## Step 2 — Transformation

### 使用的子技能

- `SKILLs/Transformation.md`

### 要做什么

把 proposal 转成仓库中的实际 benchmark 骨架。

### 目标路径

新题主目录：

- `benchmarks/<Domain>/<Task>/`

最小必需文件：

- `benchmarks/<Domain>/<Task>/README.md`
- `benchmarks/<Domain>/<Task>/README_zh-CN.md`
- `benchmarks/<Domain>/<Task>/Task.md`
- `benchmarks/<Domain>/<Task>/Task_zh-CN.md`
- `benchmarks/<Domain>/<Task>/scripts/init.py`
- `benchmarks/<Domain>/<Task>/verification/evaluator.py`
- `benchmarks/<Domain>/<Task>/verification/requirements.txt`

如果接 unified，还要补：

- `benchmarks/<Domain>/<Task>/frontier_eval/initial_program.txt`
- `benchmarks/<Domain>/<Task>/frontier_eval/eval_command.txt`
- `benchmarks/<Domain>/<Task>/frontier_eval/constraints.txt`

如果要注册 task 别名，再补：

- `frontier_eval/conf/task/<task_name>.yaml`

### 完成标志

任务目录结构完整，baseline 自包含，可被 evaluator 调用。

### 状态转移

- 最小骨架完成：`Transformation -> Verification`
- 任务契约无法落地：`Transformation -> Search`

---

## Step 3 — Verification

### 使用的子技能

- `SKILLs/Verification.md`

### 要做什么

验证任务不是“看起来有结构”，而是真的能跑、能评、有效。

### 必跑命令

在 benchmark 目录：

```bash
python verification/evaluator.py scripts/init.py
```

在仓库根目录：

```bash
python -m frontier_eval task=<task_name> algorithm.iterations=0
```

### 重点检查路径

- `benchmarks/<Domain>/<Task>/`
- `runs/.../openevolve/best/best_program_info.json`

### 完成标志

- 退出码 0
- `valid = 1`
- 有 `combined_score`
- baseline 被主框架成功加载

如果有 `human_best_score`，也要确认它进入了 metrics / artifacts。

### 状态转移

- 验证通过：`Verification -> PullRequest`
- 单次失败：`Verification -> Transformation`
- 连续 5 次失败仍无有效解：删除 proposal 与对应代码后 `Verification -> Search`

删除路径应包括：

- `proposals/<Domain>/<Task>/`
- `benchmarks/<Domain>/<Task>/`
- `frontier_eval/conf/task/<task_name>.yaml`（若存在）

---

## Step 4 — Pull Request

### 使用的子技能

- `SKILLs/PullRequest.md`

### 要做什么

把改动整理成可审查、可复现的提交。

### 重点路径

- `SKILLs/`
- `benchmarks/<Domain>/<Task>/`
- `frontier_eval/conf/task/`

### 提交前必须清理

不要把这些带进提交：

- `.env`
- API keys
- `metrics.json`
- `artifacts.json`
- 临时日志
- 绝对路径

### git 流程

至少执行：

```bash
git add ...
git commit -m "..."
git push
```

### 完成标志

- 工作区干净
- commit 已推送
- 测试证据明确可复现

### 状态转移

- PR 成功：`PullRequest -> Search`，同时 `current_pr_count += 1`
- 若 `current_pr_count >= target_pr_count`：`PullRequest -> Stop`
- PR 准备不足：`PullRequest -> Verification`

---

## 四步顺序要求

必须按顺序执行，不要跳步：

1. **Search**：没有题目定义，不做实现
2. **Transformation**：没有最小骨架，不做验证
3. **Verification**：没有测试通过，不做提交
4. **Pull Request**：没有清理产物，不做最终提交
5. **Loop**：没有完成 10 个新题 PR，就继续回到 `Search`

---

## 一句话执行模板

后续可以把任务理解成：

> 当 `current_pr_count < 10` 时，先按 `SKILLs/Search.md` 找题并写 proposal；  
> 若 `proposals/` 中已有待处理 proposal，则优先直接进入 `Transformation`；  
> 再按 `SKILLs/Transformation.md` 落成 benchmark；  
> 再按 `SKILLs/Verification.md` 跑本地与框架测试；  
> 若验证失败则回退，若连续 5 次失败则删题回到 Search；  
> 若验证成功，再按 `SKILLs/PullRequest.md` 清理、提交、推送；  
> PR 成功后 `current_pr_count += 1`，若未达 10 则继续下一轮。

<!-- AI_GENERATED -->
