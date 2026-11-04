"""claude-usage-plan-hook: one line for the owner, who may be reading it on a phone."""

import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "claude-usage-plan-hook"


class UsagePlanHook(unittest.TestCase):
  def setUp(self):
    state = tempfile.TemporaryDirectory()
    self.addCleanup(state.cleanup)
    self.directory = pathlib.Path(state.name) / "claude-status-line"
    self.directory.mkdir()
    self.environment = {**os.environ, "TZ": "America/Sao_Paulo", "XDG_STATE_HOME": state.name}

  def save_usage(self):
    (self.directory / "weekly.json").write_text(json.dumps({
      "used_percentage": 33,
      "resets_at": int(time.time()) + 3 * 86400,
      "saved_at": int(time.time()),
    }))

  def run_hook(self):
    return subprocess.run([SCRIPT], capture_output=True, text=True, env=self.environment, stdin=subprocess.DEVNULL, check=True)

  def test_the_message_is_one_line_with_the_used_share_and_todays_goal(self):
    self.save_usage()
    message = json.loads(self.run_hook().stdout)["systemMessage"]
    self.assertEqual(len(message.splitlines()), 1, message)
    self.assertRegex(message, r"^Weekly quota: 33% used, resets .+, target 100%; today's goal \d+%\. Full plan: claude-usage-plan$")

  def test_it_shows_once_within_the_interval(self):
    self.save_usage()
    self.assertTrue(self.run_hook().stdout)
    self.assertEqual(self.run_hook().stdout, "")

  def test_no_saved_usage_prints_nothing_and_records_nothing(self):
    self.assertEqual(self.run_hook().stdout, "")
    self.assertFalse((self.directory / "plan-last-shown").exists())


if __name__ == "__main__":
  unittest.main()
