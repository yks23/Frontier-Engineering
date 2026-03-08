# Proposed New Tasks

本目录收集一批适合转化为 Frontier-Eng benchmark 的候选新题，目标是方便维护者快速检查：

- 题源是否公开、稳定、可引用
- 工程场景是否真实且有价值
- 是否能定义清晰的输入/输出契约
- 是否能在可接受时间内实现自动评分

## 目录说明

每个候选题单独放在一个子目录下，并提供 `report_zh-CN.md`，统一覆盖以下内容：

1. 题源与公开链接
2. 建议的 Frontier-Eng 任务名称
3. 工程背景与现实价值
4. 可转化的任务定义
5. 输入 / 输出建议
6. 评分与有效性检查建议
7. frontier_eval 接入建议
8. 主要实现风险

## 当前候选题

当前待处理 proposal：

| 领域 | 候选任务 | 题源 | human best / best-known |
|---|---|---|---|
| Logistics | CapacitatedVehicleRouting_CVRPLibXML | CVRPLib XML set | 官方已知最优解（XML set 全部实例有最优解） |

后续新候选题需要按新的 Search 标准补齐：

- 真实工程场景
- 清晰输入 / 输出
- 稳定 evaluator 方案
- 可核实的人类最优解 / best-known 参考
- 该参考如何映射到 `combined_score`

## 说明

这些 proposal 目前只包含“如何转成任务”的设计稿，不包含实际 benchmark 实现代码。若其中某个方向被确认立项，可据此继续补齐：

- `scripts/init.py`
- `verification/evaluator.py`
- `verification/requirements.txt`
- `frontier_eval/*.txt` 元数据

<!-- AI_GENERATED -->
