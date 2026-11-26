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


def status_line(five_hour_used, five_hour_left, seven_day_used, seven_day_left, pace=None, cache_shift=0):
  """The line for a reading; with pace, a fake nereus CLI on the PATH and its cache holding that word for the week
  (resetsAt shifted by cache_shift seconds, as a cache of another window)."""
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
    path = "/usr/bin:/bin"
    if pace is not None:
      bin_dir = pathlib.Path(home) / "bin"
      bin_dir.mkdir()
      (bin_dir / "nereus").write_text("#!/bin/sh\nexit 0\n")
      (bin_dir / "nereus").chmod(0o755)
      path = f"{bin_dir}:{path}"
      cache = pathlib.Path(home) / "nereus" / "usage" / "weekly.json"
      cache.parent.mkdir(parents=True)
      figures = {} if pace == "" else {"pace": pace}
      cache.write_text(json.dumps({"resetsAt": now + seven_day_left + cache_shift, "figures": figures}))
    result = subprocess.run(
      [SCRIPT],
      input=json.dumps(reading),
      capture_output=True,
      text=True,
      env={"PATH": path, "HOME": home, "XDG_STATE_HOME": home, "XDG_CONFIG_HOME": home},
    )
  return result.returncode, result.stdout


class StatusLineVerdicts(unittest.TestCase):
  def line(self, *reading, **cache):
    returncode, line = status_line(*reading, **cache)
    self.assertEqual(returncode, 0)
    return ANSI.sub("", line)

  # The week's word from Nereus (spec 0015 of getnereus/nereus, #2326): the cache wins, the local rule is the fallback
  WEEK_OK = (27, 2 * HOUR + 15 * 60, 59, 2 * DAY + 12 * HOUR)  # the local rule says ok (about 92%)

  def test_the_week_takes_the_word_of_the_nereus_cache(self):
    self.assertRegex(self.line(*self.WEEK_OK, pace="slow"), r"↻ \w{3} \d\d:\d\d ▼ 9[12]%")
    self.assertRegex(self.line(*self.WEEK_OK, pace="push"), r"↻ \w{3} \d\d:\d\d ▲ 9[12]%")

  def test_final_is_neutral_gray(self):
    returncode, line = status_line(*self.WEEK_OK, pace="final")
    self.assertRegex(line, r"\x1b\[38;5;247m• 9[12]%")

  def test_a_cache_of_another_window_falls_back_to_the_local_rule(self):
    self.assertRegex(self.line(*self.WEEK_OK, pace="slow", cache_shift=DAY), r"↻ \w{3} \d\d:\d\d • 9[12]%")

  def test_no_word_in_the_cache_falls_back_to_the_local_rule(self):
    self.assertRegex(self.line(*self.WEEK_OK, pace=""), r"↻ \w{3} \d\d:\d\d • 9[12]%")

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
