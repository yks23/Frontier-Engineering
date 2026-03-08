# 增材制造工艺参数优化

为一次金属增材制造工艺选择参数。

## 输出

写出 `process_params.json`：

```json
{
  "material": "IN625",
  "laser_power": 230.0,
  "scan_speed": 800.0,
  "hatch_spacing": 0.11,
  "layer_thickness": 0.04,
  "method": "..."
}
```

## 有效性约束

所有参数必须落在声明的边界范围内。

## 评分方式

评测器使用确定性代理模型估计：

- 形变
- 残余应力
- 生产率
- 缺陷风险

`combined_score = productivity_bonus - distortion_penalty - stress_penalty - defect_penalty`

越大越好，非法输出记 0 分。

<!-- AI_GENERATED -->
