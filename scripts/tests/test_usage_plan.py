"""Tests of claude-usage-plan --today-goal: the percentage to reach by the end of today.

Run: python3 -m unittest discover -s scripts/tests
"""
import datetime
import os
import pathlib
import re
import subprocess
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-usage-plan"
ENVIRONMENT = {**os.environ, "TZ": "America/Sao_Paulo"}
ZONE = datetime.timezone(datetime.timedelta(hours=-3))


def epoch(day, hour, minute=0):
  return int(datetime.datetime(2026, 11, day, hour, minute, tzinfo=ZONE).timestamp())


RESETS_AT = epoch(9, 1)


def run(*args, used="15", resets_at=RESETS_AT, now=epoch(3, 11, 50)):
  return subprocess.run(
    [SCRIPT, "--used", used, "--resets-at", str(resets_at), "--now", str(now), *args],
    capture_output=True,
    text=True,
    env=ENVIRONMENT,
  )


class TodayGoal(unittest.TestCase):
  def goal(self, **kwargs):
    result = run("--today-goal", **kwargs)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def test_the_goal_spreads_what_is_left_evenly_up_to_midnight(self):
    self.assertEqual(self.goal(), "22")

  def test_the_goal_agrees_with_the_plan_table(self):
    table = run().stdout
    row = re.search(r"\(today\)\s+\S+\s+\+\d+%\s+(\d+)%", table)
    self.assertEqual(self.goal(), row.group(1))

  def test_the_last_day_lands_on_the_target(self):
    self.assertEqual(self.goal(now=epoch(8, 12)), "100")

  def test_the_hours_before_a_reset_past_midnight_belong_to_the_last_day(self):
    self.assertEqual(self.goal(now=epoch(8, 23)), "100")

  def test_the_goal_never_falls_below_the_usage_shown(self):
    self.assertEqual(self.goal(used="15.4", now=epoch(3, 23, 59)), "16")

  def test_a_stale_window_gives_no_goal(self):
    result = run("--today-goal", now=RESETS_AT)
    self.assertEqual(result.returncode, 1)
    self.assertEqual(result.stdout, "")


if __name__ == "__main__":
  unittest.main()
