"""判定核心。"""


class Counter:
    """记录本轮检查过的师徒对条数。"""

    def __init__(self):
        self.scanned = 0


def _qualifies(pair, boost):
    hours_min = 5 if boost else 10
    return (pair["hours"] >= hours_min
            and pair["level"] >= 30
            and pair["quests"] >= 3
            and pair["days"] >= 7)


def _natural_key(value):
    """徒弟号排序键：数字段按数值比，其余按文本比，避免 a10 排在 a2 前。"""
    chars = str(value)
    key = []
    digit = ""
    for ch in chars:
        if ch.isdigit():
            digit += ch
        else:
            if digit:
                key.append((1, int(digit)))
                digit = ""
            key.append((0, ch))
    if digit:
        key.append((1, int(digit)))
    return key


def iter_decisions(pairs, boost, cap, counter):
    grouped = {}
    for pair in pairs:
        counter.scanned += 1
        grouped.setdefault(pair["master"], []).append(pair)

    graduates = set()
    for master, mates in grouped.items():
        eligible = [pair for pair in mates if _qualifies(pair, boost)]
        eligible.sort(key=lambda pair: (-pair["hours"], _natural_key(pair["apprentice"])))
        for pair in eligible[:cap]:
            graduates.add(id(pair))

    for pair in pairs:
        status = "graduate" if id(pair) in graduates else "waiting"
        yield {"master": pair["master"], "apprentice": pair["apprentice"], "status": status}


def settle(state, pairs, req_id, boost, cap, counter):
    if "results" not in state:
        state["results"] = {}
    if req_id in state["results"]:
        return state["results"][req_id]
    out = list(iter_decisions(pairs, boost, cap, counter))
    for item in out:
        if item["status"] == "graduate":
            state["graduated"].append(item["apprentice"])
    state.setdefault("seen", []).append(req_id)
    state["results"][req_id] = out
    return out
