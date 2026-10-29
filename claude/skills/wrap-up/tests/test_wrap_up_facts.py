"""Tests of wrap-up-facts (the facts of a repository at the end of a session).

Run: python3 -m unittest discover -s claude/skills/wrap-up/tests
"""
import importlib.machinery
import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # no __pycache__ next to the scripts
BIN = pathlib.Path(__file__).resolve().parents[4] / "scripts/bin"


def load(name):
  loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(BIN / name))
  module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
  loader.exec_module(module)
  return module


facts = load("wrap-up-facts")


def git(*args, cwd):
  subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class Repository(unittest.TestCase):
  """A clone of a bare origin with main pushed, a merged branch in a worktree and a branch never pushed."""

  def setUp(self):
    self.folder = pathlib.Path(tempfile.mkdtemp())
    self.addCleanup(subprocess.run, ["rm", "-rf", str(self.folder)])
    os.environ.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
                      GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    origin, self.clone = self.folder / "origin.git", self.folder / "repo"
    git("init", "--quiet", "--bare", "--initial-branch", "main", str(origin), cwd=self.folder)
    git("clone", "--quiet", str(origin), str(self.clone), cwd=self.folder)
    (self.clone / "a").write_text("a\n")
    git("add", "a", cwd=self.clone)
    git("commit", "--quiet", "--message", "feat: a", cwd=self.clone)
    git("push", "--quiet", "origin", "main", cwd=self.clone)
    # A branch whose commit was rebase-merged: the same change is on main under another SHA.
    git("worktree", "add", "--quiet", "-b", "feat/merged", str(self.folder / "repo-merged"), cwd=self.clone)
    (self.folder / "repo-merged" / "b").write_text("b\n")
    git("add", "b", cwd=self.folder / "repo-merged")
    git("commit", "--quiet", "--message", "feat: b", cwd=self.folder / "repo-merged")
    git("cherry-pick", "--quiet", "feat/merged", cwd=self.clone)
    git("push", "--quiet", "origin", "main", cwd=self.clone)
    git("fetch", "--quiet", cwd=self.clone)
    git("branch", "--quiet", "feat/local", cwd=self.clone)
    git("checkout", "--quiet", "feat/local", cwd=self.clone)
    (self.clone / "c").write_text("c\n")
    git("add", "c", cwd=self.clone)
    git("commit", "--quiet", "--message", "feat: c", cwd=self.clone)
    git("checkout", "--quiet", "main", cwd=self.clone)
    (self.clone / "dirty").write_text("x\n")

  def test_it_reports_changes_worktrees_and_branches(self):
    report = facts.facts(str(self.clone))
    self.assertEqual(report["repository"]["changes"], 1)
    self.assertEqual(report["repository"]["branch"], "main")
    [tree] = report["worktrees"]
    self.assertEqual((tree["branch"], tree["merged"], tree["changes"]), ("feat/merged", True, 0))
    states = {branch["name"]: (branch["state"], branch["merged"]) for branch in report["branches"]}
    self.assertEqual(states["feat/local"], ("not pushed", False))
    self.assertEqual(states["feat/merged"], ("not pushed", True))

  def test_a_source_that_fails_never_stops_the_others(self):
    os.environ["PATH"], path = "/usr/bin:/bin", os.environ["PATH"]  # no gh, no pontos-save from ~/.scripts
    try:
      report = facts.facts(str(self.clone))
    finally:
      os.environ["PATH"] = path
    self.assertIn("unavailable", report["board"])
    self.assertIn("unavailable", report["pull_requests"])
    self.assertIsInstance(report["branches"], list)
    self.assertIn("uncommitted change(s)", facts.text(report))

  def test_it_never_runs_the_board_script_of_a_repository_it_does_not_trust(self):
    queue = self.clone / "scripts/board/queue"
    queue.parent.mkdir(parents=True)
    queue.write_text(f"#!/bin/sh\ntouch {self.folder}/ran\necho mine\n")
    queue.chmod(0o755)
    self.assertIn("not trusted", facts.facts(str(self.clone))["board"]["unavailable"])
    self.assertFalse((self.folder / "ran").exists())

  def test_it_reads_the_owner_from_origin(self):
    for url in ("git@github.com:getnereus/nereus.git", "https://github.com/smsilva/linux"):
      git("remote", "set-url", "origin", url, cwd=self.clone)
      self.assertIn(facts.origin_owner(str(self.clone)), facts.TRUSTED_OWNERS)

  def test_it_changes_nothing(self):
    before = subprocess.run(["git", "status", "--porcelain"], cwd=self.clone, capture_output=True, text=True).stdout
    facts.facts(str(self.clone))
    after = subprocess.run(["git", "status", "--porcelain"], cwd=self.clone, capture_output=True, text=True).stdout
    self.assertEqual(before, after)


class OutsideARepository(unittest.TestCase):
  def test_it_says_so(self):
    with tempfile.TemporaryDirectory() as folder:
      self.assertTrue(facts.text(facts.facts(folder)).startswith("repository: unavailable"))


if __name__ == "__main__":
  unittest.main()
