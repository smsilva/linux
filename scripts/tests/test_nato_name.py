"""Tests of nato-name: unique NATO phonetic names for the agent sessions of this machine.

Run: python3 -m unittest discover -s scripts/tests
"""
import concurrent.futures
import json
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "nato-name"
NAMES = "alfa bravo charlie delta echo foxtrot golf hotel india juliett kilo lima mike november oscar papa quebec romeo sierra tango uniform victor whiskey x-ray yankee zulu".split()


class NatoName(unittest.TestCase):
  def setUp(self):
    self.state = tempfile.TemporaryDirectory()
    self.addCleanup(self.state.cleanup)
    self.sleepers = []
    self.addCleanup(self.stop_sleepers)

  def stop_sleepers(self):
    for process in self.sleepers:
      process.kill()
      process.wait()

  def live_pid(self) -> int:
    """A live process that is not an ancestor of another sleeper, so each one stands for its own session."""
    process = subprocess.Popen(["sleep", "60"])
    self.sleepers.append(process)
    return process.pid

  def dead_pid(self) -> int:
    process = subprocess.Popen(["true"])
    process.wait()
    return process.pid

  def run_script(self, *args, stdin=None, env=None, check=True):
    environment = {key: value for key, value in os.environ.items() if not key.startswith("NATO_NAME")}
    environment.update({"NATO_NAME_STATE_DIR": self.state.name, **(env or {})})
    result = subprocess.run([str(SCRIPT), *args], input=stdin, env=environment, capture_output=True, text=True)
    if check:
      self.assertEqual(result.returncode, 0, result.stderr)
    return result

  def acquire(self, session_id, pid=None, name=None):
    args = ["acquire", "--session-id", session_id, "--pid", str(pid or self.live_pid())]
    if name:
      args += ["--name", name]
    return self.run_script(*args).stdout.strip()

  def test_acquire_gives_the_first_free_name_in_order(self):
    self.assertEqual(self.acquire("s1"), "alfa")
    self.assertEqual(self.acquire("s2"), "bravo")
    self.assertEqual(self.acquire("s3"), "charlie")

  def test_acquire_again_keeps_the_session_name(self):
    pid = self.live_pid()
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s2"), "bravo")

  def test_release_frees_the_name(self):
    self.acquire("s1")
    self.acquire("s2")
    self.run_script("release", "--session-id", "s1")
    self.assertEqual(self.acquire("s3"), "alfa")

  def test_whoami_prints_the_session_name(self):
    self.acquire("s1")
    self.acquire("s2")
    self.assertEqual(self.run_script("whoami", "--session-id", "s2").stdout.strip(), "bravo")
    self.assertNotEqual(self.run_script("whoami", "--session-id", "unknown", check=False).returncode, 0)

  def test_a_dead_holder_is_reclaimed(self):
    self.acquire("crashed", self.dead_pid())
    self.assertEqual(self.acquire("s2"), "alfa")
    self.assertEqual(self.run_script("whoami", "--session-id", "crashed", check=False).stdout.strip(), "")

  def test_a_reused_pid_does_not_keep_the_name(self):
    pid = self.live_pid()
    self.acquire("old", pid)
    holder = pathlib.Path(self.state.name) / "alfa"
    holder.write_text(holder.read_text().replace("started=", "started=1"))
    self.assertEqual(self.acquire("new"), "alfa")

  def test_overflow_continues_with_a_suffix(self):
    for index, _ in enumerate(NAMES):
      self.acquire(f"s{index}")
    self.assertEqual(self.acquire("s26"), "alfa-2")
    self.assertEqual(self.acquire("s27"), "bravo-2")

  def test_the_launcher_name_passes_to_its_child(self):
    launcher = os.getpid()
    self.assertEqual(self.acquire(f"launcher-{launcher}", launcher), "alfa")
    self.assertEqual(self.acquire("session", self.live_pid()), "alfa")
    self.assertEqual(self.run_script("whoami", "--session-id", "session").stdout.strip(), "alfa")

  def test_a_session_started_inside_another_gets_its_own_name(self):
    parent = os.getpid()
    self.assertEqual(self.acquire("parent", parent), "alfa")
    self.assertEqual(self.acquire("child", self.live_pid()), "bravo")
    self.assertEqual(self.run_script("whoami", "--session-id", "parent").stdout.strip(), "alfa")

  def test_a_free_preferred_name_is_taken(self):
    self.assertEqual(self.acquire("s1", name="kilo"), "kilo")
    self.assertEqual(self.acquire("s2", name="kilo"), "alfa")

  def test_parallel_acquires_get_different_names(self):
    pids = [self.live_pid() for _ in range(12)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
      names = list(pool.map(lambda pair: self.acquire(f"s{pair[0]}", pair[1]), enumerate(pids)))
    self.assertEqual(sorted(names), sorted(NAMES[:12]))

  def test_list_shows_each_name(self):
    self.acquire("s1")
    self.acquire("crashed", self.dead_pid())
    output = self.run_script("list").stdout
    self.assertIn("alfa", output)
    self.assertIn("stale", output)

  def hook(self, event, session_id, pid, **extra):
    payload = json.dumps({"hook_event_name": event, "session_id": session_id, **extra})
    return self.run_script("hook", stdin=payload, env={"NATO_NAME_PID": str(pid)}).stdout

  def test_the_session_start_hook_tells_the_agent_its_name(self):
    output = json.loads(self.hook("SessionStart", "s1", self.live_pid(), source="startup"))
    self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
    self.assertIn("Your name is alfa", output["hookSpecificOutput"]["additionalContext"])

  def test_the_session_end_hook_releases_the_name(self):
    pid = self.live_pid()
    self.hook("SessionStart", "s1", pid, source="startup")
    self.hook("SessionEnd", "s1", pid, reason="logout")
    self.assertEqual(self.acquire("s2"), "alfa")

  def test_clear_keeps_the_name_for_the_same_process(self):
    pid = self.live_pid()
    self.acquire("other")
    self.hook("SessionStart", "s1", pid, source="startup")
    self.hook("SessionEnd", "s1", pid, reason="clear")
    output = json.loads(self.hook("SessionStart", "s2", pid, source="clear"))
    self.assertIn("Your name is bravo", output["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
  unittest.main()
