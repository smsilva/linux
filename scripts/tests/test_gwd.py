"""gwd: a worktree whose commits are on the trunk is removed, and a session that runs inside it asks for the removal
once it exits (--after-exit), which its SessionEnd hook (--hook) carries out when no program runs there any more."""

import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest

BIN = pathlib.Path(__file__).resolve().parents[1] / "bin"
SCRIPT = BIN / "gwd"


def git(*arguments, cwd):
  return subprocess.run(["git", *arguments], cwd=cwd, check=True, capture_output=True, text=True).stdout


class Gwd(unittest.TestCase):
  def setUp(self):
    folder = tempfile.TemporaryDirectory()
    self.addCleanup(folder.cleanup)
    root = pathlib.Path(folder.name)
    origin, self.clone, self.worktree = root / "origin.git", root / "repo", root / "repo-topic"
    git("init", "--quiet", "--bare", "--initial-branch", "main", str(origin), cwd=root)
    git("clone", "--quiet", str(origin), str(self.clone), cwd=root)
    for key, value in (("user.name", "Test"), ("user.email", "test@example.com"), ("commit.gpgsign", "false")):
      git("config", key, value, cwd=self.clone)
    git("commit", "--quiet", "--allow-empty", "--message", "chore(repo): start", cwd=self.clone)
    git("push", "--quiet", "origin", "main", cwd=self.clone)
    git("remote", "set-head", "origin", "main", cwd=self.clone)
    git("worktree", "add", "--quiet", str(self.worktree), "-b", "feat/topic", "origin/main", cwd=self.clone)
    # A fake tmux: its panes are the lines of a file, so a test says which pane runs what, and where.
    self.panes = root / "panes"
    self.panes.write_text("")
    self.keys = root / "keys"
    fake = root / "fake-bin"
    fake.mkdir()
    (fake / "tmux").write_text(
      f'#!/bin/sh\ncase "$1" in\n  list-panes) cat "{self.panes}" ;;\n  send-keys) echo "$@" >> "{self.keys}" ;;\nesac\n')
    (fake / "tmux").chmod(0o755)
    self.state = root / "state"
    self.environment = {**os.environ, "PATH": f"{fake}:{BIN}:{os.environ['PATH']}", "XDG_STATE_HOME": str(self.state),
                        "GWD_HOOK_FOREGROUND": "true", "GWD_WAIT_SECONDS": "5"}

  def a_program_runs_inside(self):
    """A pane whose process is not a shell (this test's own python) is a program running inside the worktree."""
    self.panes.write_text(f"%1\t{os.getpid()}\t{self.worktree}\n")

  def gwd(self, *arguments, stdin=""):
    return subprocess.run([str(SCRIPT), *arguments], cwd=self.clone, input=stdin, capture_output=True, text=True,
                          env=self.environment)

  def hook(self, reason="prompt_input_exit", cwd=None):
    payload = {"session_id": "s1", "hook_event_name": "SessionEnd", "reason": reason, "cwd": str(cwd or self.worktree)}
    return self.gwd("--hook", stdin=json.dumps(payload))

  def pending(self):
    folder = self.state / "gwd" / "pending"
    return sorted(folder.iterdir()) if folder.exists() else []

  def test_a_program_inside_still_stops_a_plain_removal(self):
    self.a_program_runs_inside()
    result = self.gwd(str(self.worktree))
    self.assertEqual(result.returncode, 1)
    self.assertIn("tmux panes run a program inside", result.stdout)
    self.assertTrue(self.worktree.exists())

  def test_after_exit_with_a_program_inside_records_the_removal_and_removes_nothing(self):
    self.a_program_runs_inside()
    result = self.gwd("--after-exit", str(self.worktree))
    self.assertEqual(result.returncode, 0, result.stdout)
    self.assertIn("removed once", result.stdout)
    self.assertTrue(self.worktree.exists())
    self.assertEqual(len(self.pending()), 1)

  def test_after_exit_with_no_name_takes_the_worktree_it_runs_in(self):
    self.a_program_runs_inside()
    result = subprocess.run([str(SCRIPT), "--after-exit"], cwd=self.worktree, capture_output=True, text=True,
                            env=self.environment)
    self.assertEqual(result.returncode, 0, result.stdout)
    self.assertEqual(self.pending()[0].read_text().splitlines(), [str(self.clone), str(self.worktree)])

  def test_after_exit_with_nothing_inside_removes_at_once(self):
    result = self.gwd("--after-exit", str(self.worktree))
    self.assertEqual(result.returncode, 0, result.stdout)
    self.assertFalse(self.worktree.exists())
    self.assertEqual(self.pending(), [])

  def test_after_exit_still_refuses_a_worktree_with_work_not_on_the_trunk(self):
    self.a_program_runs_inside()
    (self.worktree / "file").write_text("work")
    result = self.gwd("--after-exit", str(self.worktree))
    self.assertEqual(result.returncode, 1)
    self.assertIn("Uncommitted changes", result.stdout)
    self.assertEqual(self.pending(), [])

  def test_the_hook_removes_the_worktree_once_its_session_is_gone(self):
    self.a_program_runs_inside()
    self.gwd("--after-exit", str(self.worktree))
    self.panes.write_text("")
    result = self.hook()
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertFalse(self.worktree.exists())
    self.assertNotIn("feat/topic", git("branch", "--list", cwd=self.clone))
    self.assertEqual(self.pending(), [])

  def test_the_hook_returns_at_once_and_removes_the_worktree_in_the_background(self):
    """As Claude Code runs it: the session's own process still runs while its hook does."""
    self.a_program_runs_inside()
    self.gwd("--after-exit", str(self.worktree))
    del self.environment["GWD_HOOK_FOREGROUND"]
    started = time.monotonic()
    result = self.hook()
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertLess(time.monotonic() - started, 1.5)
    self.assertTrue(self.worktree.exists())
    self.panes.write_text("")
    deadline = time.monotonic() + 10
    while self.worktree.exists() and time.monotonic() < deadline:
      time.sleep(0.2)
    self.assertFalse(self.worktree.exists(), (self.state / "gwd" / "log").read_text())
    self.assertIn("removing", (self.state / "gwd" / "log").read_text())

  def test_the_hook_leaves_the_worktree_while_a_program_still_runs_there(self):
    self.a_program_runs_inside()
    self.gwd("--after-exit", str(self.worktree))
    self.hook()
    self.assertTrue(self.worktree.exists())
    self.assertEqual(len(self.pending()), 1)

  def test_a_clear_is_not_the_end_of_the_session(self):
    self.a_program_runs_inside()
    self.gwd("--after-exit", str(self.worktree))
    self.panes.write_text("")
    self.hook(reason="clear")
    self.assertTrue(self.worktree.exists())
    self.assertEqual(len(self.pending()), 1)

  def test_the_hook_of_a_session_elsewhere_leaves_the_worktree(self):
    self.a_program_runs_inside()
    self.gwd("--after-exit", str(self.worktree))
    self.panes.write_text("")
    result = self.hook(cwd=self.clone)
    self.assertEqual(result.returncode, 0)
    self.assertTrue(self.worktree.exists())

  def test_the_hook_with_nothing_pending_does_nothing(self):
    result = self.hook(cwd=self.worktree)
    self.assertEqual((result.returncode, result.stdout), (0, ""))
    self.assertTrue(self.worktree.exists())


if __name__ == "__main__":
  unittest.main()
