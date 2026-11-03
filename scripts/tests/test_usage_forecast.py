"""Tests of claude-usage-forecast: whether the weekly quota allows speeding up.

Run: python3 -m unittest discover -s scripts/tests
"""
import pathlib
import subprocess
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-usage-forecast"
HOUR = 3600
WEEK = 7 * 24 * HOUR
RESETS_AT = 2_000_000_000
WINDOW_START = RESETS_AT - WEEK


def forecast(used, elapsed, *options):
  return subprocess.run(
    [
      SCRIPT,
      "--used", str(used),
      "--resets-at", str(RESETS_AT),
      "--now", str(int(WINDOW_START + elapsed)),
      *options,
    ],
    capture_output=True,
    text=True,
  )


class UsageForecast(unittest.TestCase):
  def signal(self, used, elapsed):
    result = forecast(used, elapsed)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def test_todays_pace_allows_pushing(self):
    self.assertEqual(self.signal(4, 12 * HOUR), "push")

  def test_a_forecast_below_70_is_push(self):
    self.assertEqual(self.signal(34.9, WEEK // 2), "push")

  def test_a_forecast_of_exactly_70_is_steady(self):
    self.assertEqual(self.signal(35, WEEK // 2), "steady")

  def test_a_forecast_of_exactly_95_is_steady(self):
    self.assertEqual(self.signal(47.5, WEEK // 2), "steady")

  def test_a_forecast_above_95_is_slow(self):
    self.assertEqual(self.signal(47.6, WEEK // 2), "slow")

  def test_a_quota_that_runs_out_before_the_reset_is_slow(self):
    self.assertEqual(self.signal(60, WEEK // 2), "slow")

  def test_the_first_six_hours_give_no_signal(self):
    self.assertEqual(self.signal(50, 6 * HOUR - 1), "")

  def test_the_signal_starts_at_six_hours(self):
    self.assertEqual(self.signal(1, 6 * HOUR), "push")

  def test_a_reset_already_past_uses_the_percentage_as_it_is(self):
    self.assertEqual(self.signal(40, WEEK + HOUR), "push")
    self.assertEqual(self.signal(96, WEEK + HOUR), "slow")

  def test_with_percentage_prints_the_forecast_before_the_signal(self):
    result = forecast(16, 37.6 * HOUR, "--with-percentage")
    self.assertEqual(result.stdout.strip(), "71.5 steady")

  def test_with_percentage_prints_nothing_in_the_first_six_hours(self):
    result = forecast(50, 6 * HOUR - 1, "--with-percentage")
    self.assertEqual(result.stdout.strip(), "")

  def test_a_missing_or_invalid_value_fails(self):
    for args in (
      ["--used", "4"],
      ["--resets-at", str(RESETS_AT)],
      ["--used", "many", "--resets-at", str(RESETS_AT)],
      ["--used", "4", "--resets-at", "soon"],
    ):
      with self.subTest(args=args):
        result = subprocess.run([SCRIPT, *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
  unittest.main()
