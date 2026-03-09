# SALBP instance_n=20_1.alb

在工序先后关系和节拍约束下，把任务分配到工位。

## 评分方式

- `used_stations` = 候选解使用的工位数
- `best_known_stations = 3`
- `combined_score = 3 / used_stations`
- `human_best_score = 1.0`

非法输出记为 `combined_score = 0` 且 `valid = 0`。

<!-- AI_GENERATED -->
