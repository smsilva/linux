"""Worktree removal never strands a shell: gwd checks tmux panes, the hook sends agents to gwd, cwd-fallback picks the way out."""

import json
import os
import pathlib
import subprocess
import tempfile
import unittest

BIN = pathlib.Path(__file__).resolve().parents[1] / "bin"
GWD = BIN / "gwd"
GUARD = BIN / "claude-guard-worktree-remove"
FALLBACK = BIN / "cwd-fallback"

FAKE_TMUX = """#!/bin/bash
case "${1}" in
  list-panes ) cat "${FAKE_TMUX_PANES}" ;;
  send-keys ) shift; printf '%s\\n' "${*}" >> "${FAKE_TMUX_LOG}" ;;
esac
"""


def git(*arguments, cwd):
  subprocess.run(["git", *arguments], cwd=cwd, check=True, capture_output=True)


class Gwd(unittest.TestCase):
  def setUp(self):
    temporary = tempfile.TemporaryDirectory()
    self.addCleanup(temporary.cleanup)
    self.root = pathlib.Path(temporary.name).resolve()
    origin = self.root / "origin.git"
    self.clone = self.root / "repo"
    git("init", "--quiet", "--bare", "--initial-branch=main", str(origin), cwd=self.root)
    git("clone", "--quiet", str(origin), str(self.clone), cwd=self.root)
    for setting in (("user.email", "test@example.com"), ("user.name", "Test")):
      git("config", *setting, cwd=self.clone)
    git("commit", "--quiet", "--allow-empty", "--message", "chore(test): start", cwd=self.clone)
    git("push", "--quiet", "origin", "main", cwd=self.clone)
    git("remote", "set-head", "origin", "main", cwd=self.clone)
    self.worktree = self.root / "repo-slug"
    git("worktree", "add", "--quiet", "-b", "feat/slug", str(self.worktree), "origin/main", cwd=self.clone)
    bin_directory = self.root / "bin"
    bin_directory.mkdir()
    (bin_directory / "tmux").write_text(FAKE_TMUX)
    (bin_directory / "tmux").chmod(0o755)
    self.panes = self.root / "panes"
    self.panes.write_text("")
    self.log = self.root / "send-keys"
    self.environment = {
      **os.environ,
      "PATH": f"{bin_directory}:{os.environ['PATH']}",
      "FAKE_TMUX_PANES": str(self.panes),
      "FAKE_TMUX_LOG": str(self.log),
      "GIT_CONFIG_GLOBAL": "/dev/null",
    }

  def shell(self, busy):
    """A real bash process: idle (no child) or busy (running sleep)."""
    script = "sleep 30; :" if busy else "read line"
    process = subprocess.Popen(["bash", "-c", script], stdin=subprocess.PIPE)
    self.addCleanup(process.wait)
    self.addCleanup(process.kill)
    self.addCleanup(process.stdin.close)
    if busy:
      for _ in range(50):
        if subprocess.run(["ps", "-o", "pid=", "--ppid", str(process.pid)], capture_output=True, text=True).stdout.strip():
          break
        subprocess.run(["sleep", "0.05"])
    return process.pid

  def pane(self, pane_id, pid, path):
    with self.panes.open("a") as panes:
      panes.write(f"{pane_id}\t{pid}\t{path}\n")

  def gwd(self, *arguments):
    return subprocess.run([GWD, *arguments, "repo-slug"], cwd=self.clone, env=self.environment, capture_output=True, text=True)

  def test_without_a_name_and_a_terminal_it_asks_for_the_name_and_removes_nothing(self):
    result = subprocess.run([GWD], cwd=self.clone, env=self.environment, capture_output=True, text=True, stdin=subprocess.DEVNULL, start_new_session=True)
    self.assertEqual(result.returncode, 1)
    self.assertIn("No terminal to pick a worktree with fzf: pass its name, e.g. gwd repo-slug", result.stdout)
    self.assertTrue(self.worktree.exists())

  def test_an_idle_shell_inside_moves_to_the_main_clone_before_the_removal(self):
    self.pane("%1", self.shell(busy=False), self.worktree / "docs")
    result = self.gwd()
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertIn(f"Panes:    %1 move to {self.clone}", result.stdout)
    self.assertEqual(self.log.read_text().splitlines(), [f"-t %1 -l cd '{self.clone}'", "-t %1 Enter"])
    self.assertFalse(self.worktree.exists())

  def test_a_program_running_inside_stops_the_removal(self):
    self.pane("%2", self.shell(busy=True), self.worktree)
    result = self.gwd()
    self.assertEqual(result.returncode, 1)
    self.assertIn("tmux panes run a program inside", result.stdout)
    self.assertIn("%2 (bash,sleep)", result.stdout)
    self.assertTrue(self.worktree.exists())
    self.assertFalse(self.log.exists())

  def test_force_removes_and_names_the_stranded_pane(self):
    self.pane("%2", self.shell(busy=True), self.worktree)
    result = self.gwd("--force")
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertIn("left in a removed folder (--force)", result.stdout)
    self.assertFalse(self.worktree.exists())

  def test_dry_run_shows_the_panes_and_changes_nothing(self):
    self.pane("%1", self.shell(busy=False), self.worktree)
    result = self.gwd("--dry-run")
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertIn("%1 move to", result.stdout)
    self.assertIn("Dry run: nothing removed", result.stdout)
    self.assertTrue(self.worktree.exists())
    self.assertFalse(self.log.exists())

  def test_a_pane_in_a_sibling_folder_with_the_same_prefix_is_left_alone(self):
    self.pane("%3", self.shell(busy=True), f"{self.worktree}-other")
    result = self.gwd()
    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
    self.assertNotIn("Panes:", result.stdout)
    self.assertFalse(self.worktree.exists())


class Guard(unittest.TestCase):
  def run_hook(self, tool, command):
    payload = json.dumps({"tool_name": tool, "tool_input": {"command": command}, "cwd": "/tmp"})
    return subprocess.run([GUARD], input=payload, capture_output=True, text=True)

  def test_a_direct_worktree_remove_is_refused_with_gwd_in_the_message(self):
    for command in (
      "git worktree remove /home/user/flow/repo-123",
      "git -C /home/user/flow/repo worktree remove ../repo-123 && git branch -D feat/x",
      "cd /home/user/flow/repo && git worktree  remove --force ../repo-123",
    ):
      result = self.run_hook("Bash", command)
      self.assertEqual(result.returncode, 2, command)
      self.assertIn("gwd --dry-run", result.stderr)

  def test_other_commands_pass(self):
    for tool, command in (
      ("Bash", "git worktree list"),
      ("Bash", "git worktree add ../repo-1 -b feat/x origin/main"),
      ("Bash", "gwd repo-123"),
      ("Bash", "git worktree prune"),
      ("Read", "git worktree remove x"),
    ):
      self.assertEqual(self.run_hook(tool, command).returncode, 0, command)


class CwdFallback(unittest.TestCase):
  def setUp(self):
    temporary = tempfile.TemporaryDirectory()
    self.addCleanup(temporary.cleanup)
    self.root = pathlib.Path(temporary.name).resolve()

  def fallback(self, removed):
    return subprocess.run([FALLBACK, str(removed)], capture_output=True, text=True, check=True).stdout.strip()

  def test_a_removed_worktree_leads_to_the_main_clone_next_to_it(self):
    (self.root / "platform-api" / ".git").mkdir(parents=True)
    self.assertEqual(self.fallback(self.root / "platform-api-77301"), str(self.root / "platform-api"))
    self.assertEqual(self.fallback(self.root / "platform-api-77301" / "docs" / "adr"), str(self.root / "platform-api"))

  def test_a_linked_worktree_with_a_git_file_counts_as_a_checkout(self):
    (self.root / "linux").mkdir()
    (self.root / "linux" / ".git").write_text("gitdir: elsewhere\n")
    self.assertEqual(self.fallback(self.root / "linux-gwd-guard"), str(self.root / "linux"))

  def test_without_a_checkout_it_leads_to_the_first_parent_left(self):
    (self.root / "flow").mkdir()
    self.assertEqual(self.fallback(self.root / "flow" / "gone-1" / "deep"), str(self.root / "flow"))


if __name__ == "__main__":
  unittest.main()
