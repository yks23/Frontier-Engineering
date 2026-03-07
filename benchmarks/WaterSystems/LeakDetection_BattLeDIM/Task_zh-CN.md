# 供水漏损检测与定位

给定多区域压力时间序列，检测漏损事件并输出告警区间。

## 输出

写出 `alarms.json`：

```json
{
  "alarms": [
    {"start": 40, "end": 70, "zone_id": "zone_1", "confidence": 0.9}
  ],
  "method": "..."
}
```

## 评分方式

评测器将预测告警与隐藏真值漏损事件匹配，并计算：

- event F1
- 定位准确率
- 延迟得分
- 误报得分

`combined_score = 0.45 * f1 + 0.25 * location_score + 0.20 * delay_score + 0.10 * false_alarm_score`

非法输出记 0 分。

<!-- AI_GENERATED -->
