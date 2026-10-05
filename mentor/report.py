"""把判定渲染成对齐文本表。"""


def render(decisions):
    rows = [("master", "apprentice", "status")]
    for item in decisions:
        rows.append((item["master"], item["apprentice"], item["status"]))
    widths = [max(len(row[i]) for row in rows) for i in range(3)]
    lines = ["  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) for row in rows]
    graduate = sum(1 for item in decisions if item["status"] == "graduate")
    lines.append("total graduate=%d waiting=%d" % (graduate, len(decisions) - graduate))
    return "\n".join(lines)
