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

| 领域 | 候选任务 | 题源 |
|---|---|---|
| PowerSystems | ACOptimalPowerFlow_PGLibOPF | PGLib-OPF |
| BuildingEnergy | HVACControl_BOPTEST | BOPTEST |
| Manufacturing | JobShopScheduling_JSPLib | JSPLib / OR-Library |
| Transportation | TrafficSignalControl_RESCO | RESCO |
| WaterSystems | LeakDetection_BattLeDIM | BattLeDIM |
| RenewableEnergy | WindFarmLayoutOptimization | Wind Farm Layout Optimization Competition |
| ChemicalEngineering | ProcessControl_TennesseeEastman | Tennessee Eastman Challenge |
| MaterialsEngineering | MaterialsDiscovery_MatBench | MatBench |
| AdditiveManufacturing | AMProcessOptimization_AMBench | NIST AM-Bench |
| SatelliteOperations | EarthObservationScheduling_GECCO2025 | GECCO 2025 EOSS Competition |
| WarehouseAutomation | MultiAgentPathFinding_MAPF | Moving AI MAPF Benchmarks |

## 说明

这些 proposal 目前只包含“如何转成任务”的设计稿，不包含实际 benchmark 实现代码。若其中某个方向被确认立项，可据此继续补齐：

- `scripts/init.py`
- `verification/evaluator.py`
- `verification/requirements.txt`
- `frontier_eval/*.txt` 元数据

<!-- AI_GENERATED -->
