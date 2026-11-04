"""Tests of agent-name: unique names for the agent sessions of this machine.

Run: python3 -m unittest discover -s scripts/tests
"""
import concurrent.futures
import json
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "agent-name"
ROOT = pathlib.Path(__file__).resolve().parents[2] / "claude" / "agent-names"


def names_in(path):
  return [line for line in path.read_text().splitlines() if line and not line.startswith("#")]


NEREIDS = names_in(ROOT / "lists" / "nereids")
NAMES = "alfa bravo charlie delta echo foxtrot golf hotel india juliett kilo lima mike november oscar papa quebec romeo sierra tango uniform victor whiskey x-ray yankee zulu".split()


class AgentName(unittest.TestCase):
  def setUp(self):
    self.state = tempfile.TemporaryDirectory()
    self.addCleanup(self.state.cleanup)
    self.home = tempfile.TemporaryDirectory()
    self.addCleanup(self.home.cleanup)
    self.config = pathlib.Path(self.home.name) / "config"
    self.configure("nato", "list", "listed")
    self.sleepers = []
    self.addCleanup(self.stop_sleepers)

  def configure(self, lists, scope, order):
    self.config.write_text(f"lists={lists}\nscope={scope}\norder={order}\n")

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
    environment = {key: value for key, value in os.environ.items() if not key.startswith("AGENT_NAME")}
    environment.update({"AGENT_NAME_STATE_DIR": self.state.name, "AGENT_NAME_CONFIG": str(self.config), **(env or {})})
    result = subprocess.run([str(SCRIPT), *args], input=stdin, env=environment, capture_output=True, text=True)
    if check:
      self.assertEqual(result.returncode, 0, result.stderr)
    return result

  def acquire(self, session_id, pid=None, name=None):
    args = ["acquire", "--session-id", session_id, "--pid", str(pid or self.live_pid())]
    if name:
      args += ["--name", name]
    return self.run_script(*args).stdout.strip()

  def test_acquire_gives_the_names_in_order(self):
    self.assertEqual(self.acquire("s1"), "alfa")
    self.assertEqual(self.acquire("s2"), "bravo")
    self.assertEqual(self.acquire("s3"), "charlie")

  def test_a_closed_session_does_not_give_its_name_to_the_next_one(self):
    self.assertEqual(self.acquire("s1"), "alfa")
    self.run_script("release", "--session-id", "s1")
    self.assertEqual(self.acquire("s2"), "bravo")
    self.run_script("release", "--session-id", "s2")
    self.assertEqual(self.acquire("s3"), "charlie")

  def test_the_list_starts_over_after_zulu(self):
    for index, _ in enumerate(NAMES):
      session_id = f"s{index}"
      self.acquire(session_id)
      self.run_script("release", "--session-id", session_id)
    self.assertEqual(self.acquire("next"), "alfa")

  def test_starting_over_skips_the_names_still_in_use(self):
    self.assertEqual(self.acquire("long-lived"), "alfa")
    for index, _ in enumerate(NAMES[1:]):
      session_id = f"s{index}"
      self.acquire(session_id)
      self.run_script("release", "--session-id", session_id)
    self.assertEqual(self.acquire("next"), "bravo")

  def test_a_dead_holder_gets_its_turn_when_the_list_comes_back(self):
    self.assertEqual(self.acquire("crashed", self.dead_pid()), "alfa")
    self.assertEqual(self.acquire("s1"), "bravo")
    (pathlib.Path(self.state.name) / ".queue").write_text("")
    self.assertEqual(self.acquire("s2"), "alfa")

  def test_keeping_a_name_does_not_move_the_list(self):
    pid = self.live_pid()
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s1-after-clear", pid), "alfa")
    self.assertEqual(self.acquire("s2"), "bravo")

  def test_the_launcher_reservation_moves_the_list_once(self):
    launcher = os.getpid()
    self.assertEqual(self.acquire(f"launcher-{launcher}", launcher), "alfa")
    self.assertEqual(self.acquire("session", self.live_pid()), "alfa")
    self.assertEqual(self.acquire("other", name="alfa"), "bravo")

  def test_a_preferred_name_does_not_move_the_list(self):
    self.assertEqual(self.acquire("s1", name="kilo"), "kilo")
    self.assertEqual(self.acquire("s2"), "alfa")

  def test_the_queue_files_are_not_listed_as_names(self):
    self.acquire("s1")
    self.assertNotIn(".queue", self.run_script("list").stdout)

  def round_of(self, size, env=None):
    names = []
    for index in range(size):
      session_id = f"round-{index}"
      pid = self.live_pid()
      names.append(self.run_script("acquire", "--session-id", session_id, "--pid", str(pid), env=env).stdout.strip())
      self.run_script("release", "--session-id", session_id, env=env)
    return names

  def test_the_versioned_configuration_is_the_nereids_at_random(self):
    self.config.unlink()
    self.assertEqual(self.run_script("config").stdout.split(), ["lists=nereids", "scope=list", "order=random", "names=26"])
    self.assertIn(self.acquire("s1"), NEREIDS)

  def test_listed_follows_the_file_of_each_list(self):
    self.configure("nereids,nato", "list", "listed")
    self.assertEqual(self.round_of(52), NEREIDS + NAMES)

  def test_alphabetical_per_list_sorts_inside_each_list(self):
    self.configure("nereids,nato", "list", "alphabetical")
    self.assertEqual(self.round_of(52), sorted(NEREIDS) + sorted(NAMES))

  def test_alphabetical_over_all_sorts_the_pool(self):
    self.configure("nereids,nato", "all", "alphabetical")
    self.assertEqual(self.round_of(52), sorted(NEREIDS + NAMES))

  def test_random_per_list_finishes_one_list_before_the_next(self):
    self.configure("nereids,nato", "list", "random")
    names = self.round_of(52)
    self.assertEqual(sorted(names[:26]), sorted(NEREIDS))
    self.assertEqual(sorted(names[26:]), sorted(NAMES))

  def test_random_over_all_mixes_the_lists(self):
    self.configure("nereids,nato", "all", "random")
    names = self.round_of(52, env={"AGENT_NAME_SEED": "7"})
    self.assertEqual(sorted(names), sorted(NEREIDS + NAMES))
    self.assertTrue(set(names[:26]) & set(NAMES) and set(names[:26]) & set(NEREIDS))

  def test_random_repeats_no_name_inside_a_round(self):
    self.configure("nereids", "list", "random")
    self.assertEqual(sorted(self.round_of(26)), sorted(NEREIDS))

  def test_the_same_seed_gives_the_same_round(self):
    self.configure("nereids", "list", "random")
    first = self.round_of(26, env={"AGENT_NAME_SEED": "7"})
    second = self.round_of(26, env={"AGENT_NAME_SEED": "7"})
    self.assertEqual(first, second)
    self.assertNotEqual(first, NEREIDS)

  def test_a_changed_configuration_ends_the_round(self):
    self.assertEqual(self.acquire("s1"), "alfa")
    self.configure("nereids", "list", "listed")
    self.assertEqual(self.acquire("s2"), NEREIDS[0])

  def test_a_name_in_use_stays_valid_when_its_list_is_turned_off(self):
    pid = self.live_pid()
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.configure("nereids", "list", "listed")
    self.assertEqual(self.acquire("s1", pid), "alfa")

  def test_an_invalid_configuration_is_refused(self):
    for lists, scope, order in (("nato", "list", "shuffled"), ("nato", "everything", "listed"), ("no-such-list", "list", "listed")):
      self.configure(lists, scope, order)
      result = self.run_script("acquire", "--session-id", "s1", "--pid", str(self.live_pid()), check=False)
      self.assertNotEqual(result.returncode, 0)
      self.assertEqual(result.stdout.strip(), "")

  def test_no_list_holds_a_reserved_name(self):
    reserved = set(names_in(ROOT / "reserved"))
    for path in (ROOT / "lists").iterdir():
      self.assertFalse(set(names_in(path)) & reserved, path.name)

  def test_the_names_are_valid_and_appear_once(self):
    for path in (ROOT / "lists").iterdir():
      names = names_in(path)
      self.assertEqual(len(names), len(set(names)), path.name)
      for name in names:
        self.assertRegex(name, r"^[a-z]+(-[a-z]+)?$")

  def test_the_old_state_folder_moves_once_and_keeps_the_names(self):
    home = pathlib.Path(self.home.name)
    old = home / "nato-names"
    old.mkdir()
    (old / "alfa").write_text(f"session_id=old-session\npid={os.getpid()}\n")
    (old / ".last").write_text("alfa\n")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("AGENT_NAME")}
    environment.update({"XDG_STATE_HOME": str(home), "AGENT_NAME_CONFIG": str(self.config)})
    result = subprocess.run([str(SCRIPT), "whoami", "--session-id", "old-session"], env=environment, capture_output=True, text=True)
    self.assertEqual(result.stdout.strip(), "alfa")
    self.assertFalse(old.exists())
    self.assertFalse((home / "agent-names" / ".last").exists())

  def test_the_old_command_still_works(self):
    self.acquire("s1")
    result = subprocess.run(
      [str(SCRIPT.parent / "nato-name"), "whoami", "--session-id", "s1"],
      env={**os.environ, "AGENT_NAME_STATE_DIR": self.state.name, "AGENT_NAME_CONFIG": str(self.config)},
      capture_output=True,
      text=True,
    )
    self.assertEqual(result.stdout.strip(), "alfa")

  def test_acquire_again_keeps_the_session_name(self):
    pid = self.live_pid()
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s1", pid), "alfa")
    self.assertEqual(self.acquire("s2"), "bravo")

  def test_release_frees_the_name(self):
    self.acquire("s1")
    self.acquire("s2")
    self.run_script("release", "--session-id", "s1")
    self.assertEqual(self.acquire("s3", name="alfa"), "alfa")

  def test_whoami_prints_the_session_name(self):
    self.acquire("s1")
    self.acquire("s2")
    self.assertEqual(self.run_script("whoami", "--session-id", "s2").stdout.strip(), "bravo")
    self.assertNotEqual(self.run_script("whoami", "--session-id", "unknown", check=False).returncode, 0)

  def test_a_dead_holder_is_reclaimed(self):
    self.acquire("crashed", self.dead_pid())
    self.assertEqual(self.acquire("s2", name="alfa"), "alfa")
    self.assertEqual(self.run_script("whoami", "--session-id", "crashed", check=False).stdout.strip(), "")

  def test_a_reused_pid_does_not_keep_the_name(self):
    pid = self.live_pid()
    self.acquire("old", pid)
    holder = pathlib.Path(self.state.name) / "alfa"
    holder.write_text(holder.read_text().replace("started=", "started=1"))
    self.assertEqual(self.acquire("new", name="alfa"), "alfa")

  def test_overflow_continues_with_a_suffix(self):
    for index, _ in enumerate(NAMES):
      self.acquire(f"s{index}")
    self.assertEqual(self.acquire("s26"), "alfa-2")
    self.assertEqual(self.acquire("s27"), "bravo-2")
    self.run_script("release", "--session-id", "s0")
    self.assertEqual(self.acquire("s28"), "alfa")

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
    return self.run_script("hook", stdin=payload, env={"AGENT_NAME_PID": str(pid)}).stdout

  def test_the_session_start_hook_tells_the_agent_its_name(self):
    output = json.loads(self.hook("SessionStart", "s1", self.live_pid(), source="startup"))
    self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "SessionStart")
    self.assertIn("Your name is alfa", output["hookSpecificOutput"]["additionalContext"])

  def test_the_session_end_hook_releases_the_name(self):
    pid = self.live_pid()
    self.hook("SessionStart", "s1", pid, source="startup")
    self.hook("SessionEnd", "s1", pid, reason="logout")
    self.assertEqual(self.acquire("s2", name="alfa"), "alfa")

  def test_clear_keeps_the_name_for_the_same_process(self):
    pid = self.live_pid()
    self.acquire("other")
    self.hook("SessionStart", "s1", pid, source="startup")
    self.hook("SessionEnd", "s1", pid, reason="clear")
    output = json.loads(self.hook("SessionStart", "s2", pid, source="clear"))
    self.assertIn("Your name is bravo", output["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
  unittest.main()
