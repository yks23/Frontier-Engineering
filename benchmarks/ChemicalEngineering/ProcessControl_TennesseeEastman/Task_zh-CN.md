# 简化过程控制任务

输出一个控制序列，使过程变量在扰动下尽量贴近目标值。

## 输出

写出 `control.json`：

```json
{
  "control": [0.8, 0.8, 1.0],
  "method": "..."
}
```

## 有效性约束

- 控制序列长度必须等于时域长度
- 每个控制值必须落在边界内
- 过程变量必须始终处于硬安全范围内

## 评分方式

`combined_score = -(tracking_error + 0.1 * control_effort + 0.2 * recovery_time)`

越大越好，非法输出会被赋予一个极低的哨兵分数。

<!-- AI_GENERATED -->
