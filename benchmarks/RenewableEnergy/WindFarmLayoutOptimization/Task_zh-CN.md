# 风场布局优化

在给定矩形场地内选择风机坐标。

## 有效性约束

只有满足以下条件时布局才有效：

1. 风机数量必须正确。
2. 每台风机都必须在场地范围内。
3. 任意两台风机都必须满足最小间距约束。

## 输出

写出 `layout.json`：

```json
{
  "site_id": "windfarm_small_v1",
  "method": "...",
  "turbines": [{"x": 10.0, "y": 20.0}]
}
```

## 评分方式

评测器使用简化的年发电量代理模型，并加入两两尾流惩罚。

对于有效解：

- `aep_score` 越高越好
- `combined_score = aep_score`

非法输出记为 `combined_score = 0`、`valid = 0`。

<!-- AI_GENERATED -->
