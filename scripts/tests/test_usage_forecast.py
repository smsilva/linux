"""Tests of claude-usage-forecast: whether the weekly quota allows speeding up.

Run: python3 -m unittest discover -s scripts/tests
"""
import datetime
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-usage-forecast"
HOUR = 3600
WEEK = 7 * 24 * HOUR
RESETS_AT = 2_000_000_000
WINDOW_START = RESETS_AT - WEEK
# No days-off file of the machine's own: only a test's flags and files count
ENVIRONMENT = {**{key: value for key, value in os.environ.items() if key != "CLAUDE_USAGE_DAYS_OFF_FILE"}, "XDG_CONFIG_HOME": "/nonexistent"}


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
    env=ENVIRONMENT,
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

  def test_a_forecast_of_97_is_steady(self):
    self.assertEqual(self.signal(48.5, WEEK // 2), "steady")

  def test_a_forecast_of_exactly_99_is_steady(self):
    self.assertEqual(self.signal(49.5, WEEK // 2), "steady")

  def test_a_forecast_above_99_is_slow(self):
    self.assertEqual(self.signal(49.6, WEEK // 2), "slow")

  def test_a_quota_that_runs_out_before_the_reset_is_slow(self):
    self.assertEqual(self.signal(60, WEEK // 2), "slow")

  def test_the_first_six_hours_give_no_signal(self):
    self.assertEqual(self.signal(50, 6 * HOUR - 1), "")

  def test_the_signal_starts_at_six_hours(self):
    self.assertEqual(self.signal(1, 6 * HOUR), "push")

  def test_a_reset_already_past_uses_the_percentage_as_it_is(self):
    self.assertEqual(self.signal(40, WEEK + HOUR), "push")
    self.assertEqual(self.signal(100, WEEK + HOUR), "slow")

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
        result = subprocess.run([SCRIPT, *args], capture_output=True, text=True, env=ENVIRONMENT)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")


# Only worked time counts (#2106, #2113), with the same rules as Nereus: the window of WORKED_RESETS_AT runs from
# Mon 09/11 01:00 to Mon 16/11 01:00 in Sao Paulo
ZONE = datetime.timezone(datetime.timedelta(hours=-3))


def at(day, hour, minute=0):
  return int(datetime.datetime(2026, 11, day, hour, minute, tzinfo=ZONE).timestamp())


WORKED_RESETS_AT = at(16, 1)
WEEKEND = ("--weekday-off", "sat=Weekend", "--weekday-off", "sun=Weekend")


class WorkedTime(unittest.TestCase):
  def setUp(self):
    config = tempfile.TemporaryDirectory()
    self.addCleanup(config.cleanup)
    self.config = pathlib.Path(config.name)
    self.environment = {**ENVIRONMENT, "TZ": "America/Sao_Paulo", "XDG_CONFIG_HOME": config.name}

  def run_forecast(self, used, now, *options, environment=None):
    return subprocess.run(
      [SCRIPT, "--used", str(used), "--resets-at", str(WORKED_RESETS_AT), "--now", str(now), "--with-percentage", *options],
      capture_output=True,
      text=True,
      env=environment or self.environment,
    )

  def figures(self, used, now, *options, **kwargs):
    result = self.run_forecast(used, now, *options, **kwargs)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout.strip()

  def test_a_tuesday_marked_off_after_it_passed_changes_the_forecast(self):
    friday_noon = at(13, 12)
    self.assertEqual(self.figures(40, friday_noon), "62.8 push")  # 40 x 168h / 107h
    self.assertEqual(self.figures(40, friday_noon, "--day-off", "2026-11-10=Sick"), "69.4 push")  # 40 x 144h / 83h

  def test_a_saturday_with_no_worked_time_left_is_final_at_the_share_used(self):
    # Monday's hour before the reset belongs to Sunday, off with it
    self.assertEqual(self.figures(80, at(14, 12), *WEEKEND), "80.0 final")

  def test_a_date_worked_overrides_a_weekday_off(self):
    self.assertEqual(self.figures(80, at(14, 12), *WEEKEND, "--worked", "2026-11-14"), "87.3 steady")  # 80 x 143h / 131h

  def test_the_forecast_is_hidden_until_six_worked_hours_have_passed(self):
    monday_off = ("--day-off", "2026-11-09=Holiday")
    self.assertEqual(self.figures(5, at(10, 5, 59), *monday_off), "")
    self.assertEqual(self.figures(5, at(10, 6), *monday_off), "120.8 slow")  # 5 x 145h / 6h

  def test_the_days_off_file_gives_the_figures_of_the_flags(self):
    days_off = self.config / "days-off"
    days_off.write_text("# the work week\nsat Weekend\n\nsun Weekend\n2026-11-10 Sick\n")
    expected = self.figures(40, at(13, 12), *WEEKEND, "--day-off", "2026-11-10=Sick")
    self.assertEqual(self.figures(40, at(13, 12), "--days-off-file", str(days_off)), expected)
    environment = {**self.environment, "CLAUDE_USAGE_DAYS_OFF_FILE": str(days_off)}
    self.assertEqual(self.figures(40, at(13, 12), environment=environment), expected)

  def test_the_default_days_off_file_is_read_when_it_exists(self):
    default = self.config / "nereus" / "usage" / "days-off"
    default.parent.mkdir(parents=True)
    default.write_text("sat Weekend\nsun Weekend\n")
    self.assertEqual(self.figures(80, at(14, 12)), "80.0 final")

  def test_a_malformed_line_fails_with_its_number_and_the_format(self):
    days_off = self.config / "days-off"
    days_off.write_text("# the work week\nsat Weekend\nsaturday Weekend\n")
    result = self.run_forecast(40, at(13, 12), "--days-off-file", str(days_off))
    self.assertEqual(result.returncode, 1)
    self.assertEqual(result.stdout, "")
    self.assertIn(f"{days_off}:3: expected '<YYYY-MM-DD> [reason]'", result.stderr)

  def test_an_invalid_flag_value_fails(self):
    for options in (["--day-off", "2026-11-31"], ["--weekday-off", "someday"], ["--worked", "tomorrow"], ["--day-off", "2026-11-10=" + "x" * 41]):
      with self.subTest(options=options):
        result = self.run_forecast(40, at(13, 12), *options)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")

  def test_no_days_off_in_the_window_leaves_the_figures_unchanged(self):
    days_off = self.config / "days-off"
    days_off.write_text("# nothing yet\n\nworked 2026-11-14\n2026-12-25 Christmas\n")
    expected = self.figures(40, at(13, 12))
    self.assertEqual(self.figures(40, at(13, 12), "--days-off-file", str(days_off)), expected)
    self.assertEqual(self.figures(40, at(13, 12), "--day-off", "2026-11-20"), expected)


if __name__ == "__main__":
  unittest.main()
