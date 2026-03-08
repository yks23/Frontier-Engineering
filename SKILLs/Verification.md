# Verification Skill: 如何验证一个题目是对的

## 目标

确认一个新任务不是“看起来有结构”，而是真的：

- 能跑
- 能评
- 有效
- 能接入主框架

## 进入状态

从 `Transformation` 进入。进入前应当已经存在：

- `proposals/<Domain>/<Task>/report_zh-CN.md`
- `benchmarks/<Domain>/<Task>/...`

## 最小验证流程

### 1. 先做语法和路径检查

- 代码能 import / 解释执行
- `initial_program` 路径正确
- evaluator 依赖齐全
- 没有绝对路径和本地私有文件引用

### 2. 跑 benchmark 本地入口

优先跑：

```bash
python verification/evaluator.py scripts/init.py
```

必须确认：

- 退出码为 0
- `valid = 1`
- 输出格式正确
- 运行时间可接受

### 3. 跑主框架集成

再跑：

```bash
python -m frontier_eval task=<task_name> algorithm.iterations=0
```

必须确认：

- 任务能被框架加载
- baseline 能被评估
- `combined_score` 正常产生
- artifacts / history 正常落盘

### 3.5 跑 Qwen3-Coder 10 轮演化

除了 baseline 集成通过，还必须额外验证：

```bash
python -m frontier_eval task=<task_name> algorithm.iterations=10
```

并要求使用：

- Qwen3-Coder（如 `qwen/qwen3-coder-next`）

验证目标不是只看“能不能跑”，而是要看：

- 10 轮后的 best score 是否 **严格大于** baseline score

### 4. 检查评分是否稳定

重点看：

- 重复运行是否抖动过大
- 非法输出是否会被正确判 0
- evaluator 是否容易被硬编码或漏洞刷分

### 5. 检查 benchmark 语义是否闭合

至少能回答：

- 什么样的输出算 valid
- 为什么这个 score 合理
- baseline 与 human best 分别是什么
- 是否存在明显不公平依赖

## 状态转移

### 成功转移

满足以下条件时，转到 `PullRequest`：

- 本地 evaluator 通过
- `frontier_eval` 集成通过
- `valid = 1`
- `combined_score` 正常产生
- 在 Qwen3-Coder 10 轮下，best score 相比 baseline 有 **> 0** 的提升

### 失败转移

若一次验证失败，不直接放弃，而是：

1. 记录失败原因
2. 回到 `Transformation`
3. 修正实现后再次回到 `Verification`

这里的“失败”包括：

- baseline 本身不合法
- `frontier_eval` 跑不通
- Qwen3-Coder 10 轮后**没有取得 >0 提升**

### 最大尝试次数

若连续尝试 **5 次** 仍无法得到有效解，则认为当前题目不适合继续投入，执行：

1. 删除 proposal：
   - `proposals/<Domain>/<Task>/`
2. 删除对应 benchmark 代码：
   - `benchmarks/<Domain>/<Task>/`
3. 若存在 task 别名配置，也删除：
   - `frontier_eval/conf/task/<task_name>.yaml`
4. 回到 `Search`

也就是说：

- **短期失败**：`Verification -> Transformation`
- **5 次失败仍无有效解**：`Verification -> Search`

## 关键点

- 先验证合法性，再看分数高低
- 本地 evaluator 和主框架都必须跑通
- 测试产物不要提交进仓库
- 如果支持 `human_best_score`，确认其已进入 metrics/artifacts
- Verification 不止检查“能跑”，还检查 Qwen3-Coder 10 轮下能否真正改进
- 5 次失败后不要继续堆补丁，直接删题回到 Search

<!-- AI_GENERATED -->
