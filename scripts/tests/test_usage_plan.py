"""Tests of claude-usage-plan --today-goal: the percentage to reach by the end of today.

Run: python3 -m unittest discover -s scripts/tests
"""
import datetime
import json
import os
import pathlib
import re
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-usage-plan"
ZONE = datetime.timezone(datetime.timedelta(hours=-3))


def epoch(day, hour, minute=0):
  return int(datetime.datetime(2026, 11, day, hour, minute, tzinfo=ZONE).timestamp())


RESETS_AT = epoch(9, 1)


class TodayGoal(unittest.TestCase):
  def setUp(self):
    state = tempfile.TemporaryDirectory()
    self.addCleanup(state.cleanup)
    self.history = pathlib.Path(state.name) / "claude-status-line" / "weekly-history"
    self.environment = {**os.environ, "TZ": "America/Sao_Paulo", "XDG_STATE_HOME": state.name}

  def first_reading(self, day, used, saved_at, resets_at=RESETS_AT):
    self.history.mkdir(parents=True, exist_ok=True)
    (self.history / f"2026-11-{day:02d}.json").write_text(json.dumps({
      "date": f"2026-11-{day:02d}",
      "used_percentage": used,
      "resets_at": resets_at,
      "saved_at": saved_at,
    }))

  def run_plan(self, *args, used="15", now=epoch(3, 11, 50)):
    return subprocess.run(
      [SCRIPT, "--used", used, "--resets-at", str(RESETS_AT), "--now", str(now), *args],
      capture_output=True,
      text=True,
      env=self.environment,
    )

  def goal(self, **kwargs):
    result = self.run_plan("--today-goal", **kwargs)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def table_today(self, **kwargs):
    return re.search(r"\(today\)\s+\S+\s+\+\d+%\s+(\d+)%", self.run_plan(**kwargs).stdout).group(1)

  def test_without_a_first_reading_the_goal_spreads_what_is_left_up_to_midnight(self):
    self.assertEqual(self.goal(), "22")

  def test_without_a_first_reading_the_goal_never_falls_below_the_usage_shown(self):
    self.assertEqual(self.goal(used="15.4", now=epoch(3, 23, 59)), "16")

  def test_the_first_reading_fixes_the_goal_whatever_the_usage(self):
    self.first_reading(3, 8, epoch(3, 0))
    self.assertEqual(self.goal(used="15"), "23")
    self.assertEqual(self.goal(used="40"), "23")

  def test_a_first_reading_of_another_window_is_ignored(self):
    self.first_reading(3, 90, epoch(3, 0), resets_at=RESETS_AT - 3600)
    self.assertEqual(self.goal(), "22")

  def test_the_last_day_lands_on_the_target(self):
    self.assertEqual(self.goal(now=epoch(8, 12)), "100")
    self.first_reading(8, 80, epoch(8, 0))
    self.assertEqual(self.goal(used="85", now=epoch(8, 12)), "100")

  def test_the_hours_before_a_reset_past_midnight_belong_to_the_last_day(self):
    self.assertEqual(self.goal(now=epoch(8, 23)), "100")

  def test_the_goal_agrees_with_the_plan_table(self):
    self.assertEqual(self.table_today(), self.goal())
    self.first_reading(3, 8, epoch(3, 0))
    self.assertEqual(self.table_today(), self.goal())

  def test_the_table_never_plans_below_the_usage_past_the_goal(self):
    self.first_reading(3, 8, epoch(3, 0))
    self.assertEqual(self.table_today(used="40"), "40")

  def test_a_stale_window_gives_no_goal(self):
    result = self.run_plan("--today-goal", now=RESETS_AT)
    self.assertEqual(result.returncode, 1)
    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
  unittest.main()
