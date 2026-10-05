# mentor-apprentice

师徒出师判定：把师徒对逐条判成出师或候补，再渲染成报告。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m mentor report --pairs pairs.json --req-id r1 --cap 3 [--boost]
python3 -m mentor --sample=days|cap|boost|replay|work
```

师徒对字段：`master`、`apprentice`、`hours`（共同在线小时）、`level`（徒弟等级）、
`quests`（出师任务数）、`days`（拜师天数）。

## 口径

- **出师条件**：共同在线 ≥ 10 小时、徒弟等级 ≥ 30、出师任务 ≥ 3、拜师 ≥ 7 天，四条**同时**满足。
- **活动覆盖层**：活动期（`--boost`）共同在线门槛降为 ≥ 5 小时，其余不变。
- **师父名额**：每个师父每批最多 3 个徒弟出师，按共同在线小时从多到少取，并列按徒弟号升序；其余进候补。
- **幂等**：同一个 `req_id` 只结算一次，重复请求返回首次结果且不再登记出师。

## 不变量

- 被判出师的师徒对必须四条条件全满足。
- 每个师父的出师数不超过名额。
- `scanned` 不随师徒对数放大：两千对、四个师父时不超过 9000。

## 输出契约

`report` 打印对齐文本表，列顺序为 `master`、`apprentice`、`status`（`graduate` / `waiting`），
末尾一行 `total graduate=N waiting=N`。
`--sample=work` 只打印 `{"pairs": N, "scanned": N}`。
