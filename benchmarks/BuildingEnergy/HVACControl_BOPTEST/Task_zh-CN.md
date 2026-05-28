# 单区域 HVAC 控制

输出一个固定时域上的 HVAC 功率计划。

## 输出

写出 `control_schedule.json`：

```json
{
  "hvac_power_kw": [1.2, 1.2, 0.8],
  "method": "..."
}
```

## 有效性约束

- 序列长度必须等于时域长度
- 每个控制值都必须在允许功率范围内

## 评分方式

评测器会仿真室内温度：

`combined_score = -(energy_cost + comfort_penalty + peak_penalty)`

越大越好，非法输出会被赋予一个极低的哨兵分数。

<!-- AI_GENERATED -->
