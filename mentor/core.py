"""判定核心。"""


class Counter:
    """记录本轮检查过的师徒对条数。"""

    def __init__(self):
        self.scanned = 0


def _qualifies(pair, boost):
    return pair["hours"] >= 10 and pair["level"] >= 30 and pair["quests"] >= 3


def _same_master(pairs, master, counter):
    mates = []
    for pair in pairs:
        counter.scanned += 1
        if pair["master"] == master:
            mates.append(pair)
    return mates


def iter_decisions(pairs, boost, cap, counter):
    for pair in pairs:
        _same_master(pairs, pair["master"], counter)
        status = "graduate" if _qualifies(pair, boost) else "waiting"
        yield {"master": pair["master"], "apprentice": pair["apprentice"], "status": status}


def settle(state, pairs, req_id, boost, cap, counter):
    out = list(iter_decisions(pairs, boost, cap, counter))
    for item in out:
        if item["status"] == "graduate":
            state["graduated"].append(item["apprentice"])
    state["seen"].append(req_id)
    return out
