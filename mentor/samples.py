"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _pair(master, apprentice, hours, level, quests, days):
    return {"master": master, "apprentice": apprentice, "hours": hours,
            "level": level, "quests": quests, "days": days}


def _counts(decisions):
    graduate = sum(1 for d in decisions if d["status"] == "graduate")
    return {"graduate": graduate, "waiting": len(decisions) - graduate}


def run(name):
    counter = core.Counter()
    if name == "days":
        pairs = [_pair("m1", "a1", 20, 30, 3, 1)]
        out = list(core.iter_decisions(pairs, False, 3, counter))
        _line({"status": out[0]["status"]})
        return 0
    if name == "cap":
        pairs = [_pair("m1", "a%d" % i, 20 - i, 30, 3, 7) for i in range(4)]
        out = list(core.iter_decisions(pairs, False, 3, counter))
        _line(_counts(out))
        return 0
    if name == "boost":
        pairs = [_pair("m1", "a1", 6, 30, 3, 7)]
        out = list(core.iter_decisions(pairs, True, 3, counter))
        _line({"status": out[0]["status"]})
        return 0
    if name == "replay":
        pairs = [_pair("m1", "a1", 20, 30, 3, 7)]
        state = {"graduated": [], "seen": []}
        core.settle(state, pairs, "rep-1", False, 3, core.Counter())
        core.settle(state, pairs, "rep-1", False, 3, core.Counter())
        _line({"graduated": len(state["graduated"])})
        return 0
    if name == "work":
        pairs = [_pair("m%d" % (i % 4), "a%04d" % i, 20, 30, 3, 7) for i in range(2000)]
        list(core.iter_decisions(pairs, False, 3, counter))
        _line({"pairs": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
