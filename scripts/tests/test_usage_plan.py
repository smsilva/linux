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


class PlanRun:
  def setUp(self):
    state = tempfile.TemporaryDirectory()
    self.addCleanup(state.cleanup)
    self.history = pathlib.Path(state.name) / "claude-status-line" / "weekly-history"
    self.environment = {**os.environ, "TZ": "America/Sao_Paulo", "XDG_STATE_HOME": state.name, "XDG_CONFIG_HOME": state.name}
    self.environment.pop("CLAUDE_USAGE_DAYS_OFF_FILE", None)

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

  def goal(self, *args, **kwargs):
    result = self.run_plan("--today-goal", *args, **kwargs)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def table_today(self, **kwargs):
    return re.search(r"\(today\)\s+\S+\s+\+\d+%\s+(\d+)%", self.run_plan(**kwargs).stdout).group(1)


class TodayGoal(PlanRun, unittest.TestCase):
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


# Only worked time counts (#2106, #2113), with the same rules as Nereus: the window of RESETS_AT runs from Mon 02/11 01:00
# to Mon 09/11 01:00; Thursday 05/11 comes before a long weekend
LONG_WEEKEND = ("--day-off", "2026-11-06=Holiday", "--weekday-off", "sat=Weekend", "--weekday-off", "sun=Weekend")


class WorkedTime(PlanRun, unittest.TestCase):
  def plan_rows(self, *args, **kwargs):
    result = self.run_plan(*args, **kwargs)
    self.assertEqual(result.returncode, 0, result.stderr)
    planned = result.stdout.split("(so far)")[1].splitlines()[1:]
    rows = [re.match(r"\s+(\S+ \d\d/\d\d)(?: \(today\))?\s+\S+\s+\+(\d+)%\s+(\d+)%(?:  (.+))?$", line) for line in planned if line.strip()]
    return [(row[1], int(row[2]), int(row[3]), row[4]) for row in rows]

  def test_a_thursday_before_a_long_weekend_lands_on_the_target_at_its_end(self):
    thursday_noon = epoch(5, 12)
    self.assertEqual(self.plan_rows(*LONG_WEEKEND, used="50", now=thursday_noon), [
      ("Thu 05/11", 50, 100, None),
      ("Fri 06/11", 0, 100, "Holiday"),
      ("Sat 07/11", 0, 100, "Weekend"),
      ("Sun 08/11", 0, 100, "Weekend"),  # Monday's hour before the reset belongs to Sunday, off with it
    ])
    self.assertEqual(self.goal(*LONG_WEEKEND, used="50", now=thursday_noon), "100")

  def test_the_worked_days_take_the_share_of_the_days_off(self):
    self.assertEqual(self.plan_rows("--weekday-off", "sat=Weekend", "--weekday-off", "sun=Weekend", used="15"), [
      ("Tue 03/11", 12, 27, None),
      ("Wed 04/11", 24, 51, None),
      ("Thu 05/11", 24, 75, None),
      ("Fri 06/11", 25, 100, None),
      ("Sat 07/11", 0, 100, "Weekend"),
      ("Sun 08/11", 0, 100, "Weekend"),
    ])

  def test_today_off_has_the_share_used_as_its_goal(self):
    saturday_noon = epoch(7, 12)
    self.assertEqual(self.goal(*LONG_WEEKEND, used="80.2", now=saturday_noon), "81")
    self.first_reading(7, 70, epoch(7, 0))
    self.assertEqual(self.goal(*LONG_WEEKEND, used="80.2", now=saturday_noon), "81")
    self.assertRegex(self.run_plan(*LONG_WEEKEND, used="80.2", now=saturday_noon).stdout, r"\(so far\) [^\n]*81%  Weekend\n")
    self.assertEqual(self.plan_rows(*LONG_WEEKEND, used="80.2", now=saturday_noon), [
      ("Sat 07/11", 0, 81, "Weekend"),
      ("Sun 08/11", 0, 81, "Weekend"),
    ])

  def test_a_date_worked_overrides_a_weekday_off(self):
    rows = self.plan_rows(*LONG_WEEKEND, "--worked", "2026-11-07", used="50", now=epoch(5, 12))
    self.assertEqual([(day, total, reason) for day, _, total, reason in rows], [
      ("Thu 05/11", 66, None),
      ("Fri 06/11", 66, "Holiday"),
      ("Sat 07/11", 100, None),
      ("Sun 08/11", 100, "Weekend"),
    ])

  def test_a_dated_day_off_wins_over_a_date_worked(self):
    rows = self.plan_rows("--day-off", "2026-11-06=Holiday", "--worked", "2026-11-06", used="50", now=epoch(5, 12))
    self.assertEqual(rows[1][3], "Holiday")

  def test_the_days_gone_and_today_show_their_reason(self):
    result = self.run_plan("--day-off", "2026-11-03=Sick", used="40", now=epoch(5, 12))
    self.assertRegex(result.stdout, r"\n  Tue 03/11 .*%  Sick\n")
    self.assertRegex(result.stdout, r"\n  Wed 04/11 [^\n]*%\n")  # a worked day has no reason

  def test_the_days_off_file_gives_the_plan_of_the_flags(self):
    days_off = pathlib.Path(self.environment["XDG_CONFIG_HOME"]) / "nereus" / "usage" / "days-off"
    days_off.parent.mkdir(parents=True)
    days_off.write_text("# the work week\nsat Weekend\nsun Weekend\n\n2026-11-06 Holiday\n")
    self.assertEqual(self.plan_rows(used="50", now=epoch(5, 12)), self.plan_rows(*LONG_WEEKEND, used="50", now=epoch(5, 12)))

  def test_a_malformed_line_fails_with_its_number_and_the_format(self):
    days_off = pathlib.Path(self.environment["XDG_CONFIG_HOME"]) / "days-off"
    days_off.write_text("sat Weekend\nworked\n")
    result = self.run_plan("--days-off-file", str(days_off))
    self.assertEqual(result.returncode, 1)
    self.assertEqual(result.stdout, "")
    self.assertIn(f"{days_off}:2: expected", result.stderr)
    self.assertIn("'worked <YYYY-MM-DD>'", result.stderr)

  def test_no_days_off_in_the_window_leaves_the_output_unchanged(self):
    expected = self.run_plan().stdout
    days_off = pathlib.Path(self.environment["XDG_CONFIG_HOME"]) / "days-off"
    days_off.write_text("# none this week\n2026-12-25 Christmas\nworked 2026-11-07\n")
    self.assertEqual(self.run_plan("--days-off-file", str(days_off)).stdout, expected)
    self.assertEqual(self.run_plan("--day-off", "2026-11-20=Trip").stdout, expected)


if __name__ == "__main__":
  unittest.main()
