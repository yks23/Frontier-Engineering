# 交通信号灯控制

为单个路口选择一个相位序列。

## 输出

写出 `signal_plan.json`：

```json
{
  "phases": [0, 0, 1, 1, 0],
  "method": "..."
}
```

其中相位 `0` 服务南北向，相位 `1` 服务东西向。

## 评分方式

评测器会仿真队列演化。

对于有效计划：

- `combined_score = throughput - 0.5 * mean_waiting - 0.2 * mean_queue`

越大越好，非法输出记 0 分。

<!-- AI_GENERATED -->
