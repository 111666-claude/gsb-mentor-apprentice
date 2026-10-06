"""判定核心。"""


class Counter:
    """记录本轮检查过的师徒对条数。"""

    def __init__(self):
        self.scanned = 0


def _qualifies(pair, boost):
    hours_needed = 5 if boost else 10
    return (pair["hours"] >= hours_needed and pair["level"] >= 30
            and pair["quests"] >= 3 and pair["days"] >= 7)


def _group_by_master(pairs, counter):
    by_master = {}
    for pair in pairs:
        counter.scanned += 1
        by_master.setdefault(pair["master"], []).append(pair)
    return by_master


def iter_decisions(pairs, boost, cap, counter):
    pairs = list(pairs)
    by_master = _group_by_master(pairs, counter)
    allowed = set()
    for master, mates in by_master.items():
        qualified = [p for p in mates if _qualifies(p, boost)]
        qualified.sort(key=lambda p: (-p["hours"], p["apprentice"]))
        for pair in qualified[:cap]:
            allowed.add(id(pair))
    for pair in pairs:
        status = "graduate" if id(pair) in allowed else "waiting"
        yield {"master": pair["master"], "apprentice": pair["apprentice"], "status": status}


def settle(state, pairs, req_id, boost, cap, counter):
    results = state.setdefault("results", {})
    if req_id in state["seen"]:
        return results[req_id]
    out = list(iter_decisions(pairs, boost, cap, counter))
    for item in out:
        if item["status"] == "graduate":
            state["graduated"].append(item["apprentice"])
    state["seen"].append(req_id)
    results[req_id] = out
    return out
