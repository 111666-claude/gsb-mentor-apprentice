import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mentor import core, report


def pair(master, apprentice, hours, level, quests, days):
    return {"master": master, "apprentice": apprentice, "hours": hours,
            "level": level, "quests": quests, "days": days}


class MentorTest(unittest.TestCase):
    def test_one_pair_one_decision(self):
        out = list(core.iter_decisions([pair("m1", "a1", 20, 30, 3, 7)], False, 3, core.Counter()))
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["apprentice"], "a1")

    def test_report_has_header_and_total(self):
        out = list(core.iter_decisions([pair("m1", "a1", 20, 30, 3, 7)], False, 3, core.Counter()))
        text = report.render(out)
        self.assertTrue(text.splitlines()[0].startswith("master"))
        self.assertIn("total", text.splitlines()[-1])

    def test_master_is_kept_in_output(self):
        out = list(core.iter_decisions([pair("m7", "a1", 20, 30, 3, 7)], False, 3, core.Counter()))
        self.assertEqual(out[0]["master"], "m7")

    def test_empty_pairs(self):
        out = list(core.iter_decisions([], False, 3, core.Counter()))
        self.assertEqual(out, [])

    def test_status_is_one_of_two_values(self):
        out = list(core.iter_decisions([pair("m1", "a1", 1, 1, 0, 0)], False, 3, core.Counter()))
        self.assertIn(out[0]["status"], ("graduate", "waiting"))


if __name__ == "__main__":
    unittest.main()
