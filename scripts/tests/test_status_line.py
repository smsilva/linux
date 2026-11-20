"""Tests of claude-status-line's usage segments: each window's verdict and projection at its reset.

Run: python3 -m unittest discover -s scripts/tests
"""
import json
import pathlib
import re
import subprocess
import tempfile
import time
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-status-line"
HOUR = 3600
DAY = 24 * HOUR
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def status_line(five_hour_used, five_hour_left, seven_day_used, seven_day_left):
  now = int(time.time())
  reading = {
    "workspace": {"current_dir": "/tmp"},
    "model": {"display_name": "Opus 5.5"},
    "context_window": {"total_input_tokens": 1000},
    "rate_limits": {
      "five_hour": {"used_percentage": five_hour_used, "resets_at": now + five_hour_left},
      "seven_day": {"used_percentage": seven_day_used, "resets_at": now + seven_day_left},
    },
  }
  with tempfile.TemporaryDirectory() as home:
    # Without the nereus CLI on the PATH: no cache read, no report started; the state and config stay in the temp home
    result = subprocess.run(
      [SCRIPT],
      input=json.dumps(reading),
      capture_output=True,
      text=True,
      env={"PATH": "/usr/bin:/bin", "HOME": home, "XDG_STATE_HOME": home, "XDG_CONFIG_HOME": home},
    )
  return result.returncode, ANSI.sub("", result.stdout)


class StatusLineVerdicts(unittest.TestCase):
  def line(self, *reading):
    returncode, line = status_line(*reading)
    self.assertEqual(returncode, 0)
    return line

  def test_both_windows_on_pace_are_ok(self):
    # 5h: 27% after 2h45m of 5h ends at 49%; week: 59% after 4d12h of 7d ends near 92%
    line = self.line(27, 2 * HOUR + 15 * 60, 59, 2 * DAY + 12 * HOUR)
    self.assertIn("27% ↻", line)
    self.assertRegex(line, r"↻ \d\d:\d\d • 49%")
    self.assertRegex(line, r"↻ \w{3} \d\d:\d\d • 9[12]%")

  def test_a_week_left_over_says_push(self):
    self.assertRegex(self.line(27, 2 * HOUR + 15 * 60, 30, 2 * DAY + 12 * HOUR), r"▲ 4[67]%")

  def test_a_week_past_99_says_slow(self):
    self.assertRegex(self.line(27, 2 * HOUR + 15 * 60, 65, 2 * DAY + 12 * HOUR), r"▼ 10[01]%")

  def test_a_5_hour_window_below_70_is_ok_not_push(self):
    self.assertRegex(self.line(10, 2 * HOUR + 15 * 60, 59, 2 * DAY + 12 * HOUR), r"↻ \d\d:\d\d • 18%")

  def test_a_5_hour_window_past_95_says_slow(self):
    self.assertRegex(self.line(62, 2 * HOUR + 15 * 60, 59, 2 * DAY + 12 * HOUR), r"↻ \d\d:\d\d ▼ 113%")

  def test_no_5_hour_projection_in_its_first_30_minutes(self):
    line = self.line(3, 4 * HOUR + 40 * 60, 59, 2 * DAY + 12 * HOUR)
    self.assertRegex(line, r"3% ↻ \d\d:\d\d +\S")
    self.assertNotRegex(line, r"3% ↻ \d\d:\d\d [•▲▼]")

  def test_the_old_today_and_forecast_segments_are_gone(self):
    line = self.line(27, 2 * HOUR + 15 * 60, 59, 2 * DAY + 12 * HOUR)
    self.assertNotIn("today", line)
    self.assertNotIn("forecast", line)


if __name__ == "__main__":
  unittest.main()
