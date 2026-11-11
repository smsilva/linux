"""Tests of claude-peers: each live Claude Code session with its role (peer, self, helper).

Run: python3 -m unittest discover -s scripts/tests
"""
import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest

PEERS = pathlib.Path(__file__).resolve().parent.parent / "bin" / "claude-peers"


def wait_for(path):
  for _ in range(100):
    if path.exists() and path.read_text().strip():
      return int(path.read_text())
    time.sleep(0.05)
  raise AssertionError(f"{path} was never written")


def register(sessions, pid, name, cwd="/work/repo-1-x", pane="0:@0.%0"):
  (sessions / f"{pid}.json").write_text(json.dumps({"pid": pid, "name": name, "cwd": cwd, "tmux": pane, "kind": "interactive"}))


def rows(sessions):
  done = subprocess.run([str(PEERS), "--sessions", str(sessions)], capture_output=True, text=True, check=True)
  lines = done.stdout.splitlines()
  assert lines[0].split()[:3] == ["NAME", "ROLE", "ORIGIN"]
  return {line.split()[0]: line.split()[1:3] for line in lines[1:]}


class ClaudePeersTest(unittest.TestCase):
  def setUp(self):
    self.scratch = tempfile.TemporaryDirectory()
    self.tmp = pathlib.Path(self.scratch.name)
    self.sessions = self.tmp / "sessions"
    self.sessions.mkdir()

  def tearDown(self):
    self.scratch.cleanup()

  def start_hook(self, hook):
    hook.write_text(f"#!/usr/bin/env bash\nsleep 30 &\necho $! > {self.tmp / 'helper.pid'}\nwait\n")
    hook.chmod(0o755)
    parent = subprocess.Popen(["bash", "-c", f"{hook} & wait"], start_new_session=True)
    self.addCleanup(os.killpg, parent.pid, 9)
    return parent, wait_for(self.tmp / "helper.pid")

  def test_a_session_a_plugin_hook_started_is_a_helper_named_after_its_parent_and_the_plugin(self):
    # A parent session that runs a plugin's hook, which starts a headless session: parent -> hook -> helper.
    hook = self.tmp / "plugins" / "cache" / "official" / "security-guidance" / "2.0.19" / "hooks" / "review"
    hook.parent.mkdir(parents=True)
    parent, helper = self.start_hook(hook)
    peer = subprocess.Popen(["sleep", "30"])
    self.addCleanup(peer.kill)
    register(self.sessions, parent.pid, "eudora", cwd="/work/repo")
    register(self.sessions, helper, "repo-1-x-70")
    register(self.sessions, peer.pid, "galene", pane="0:@2.%2")
    register(self.sessions, 999999, "gone")  # a dead process: not listed

    found = rows(self.sessions)

    self.assertEqual(found["repo-1-x-70"], ["helper", "eudora/security-guidance"])
    self.assertEqual(found["eudora"], ["peer", "-"])
    self.assertEqual(found["galene"], ["peer", "-"])
    self.assertNotIn("gone", found)

  def test_a_hook_outside_a_plugin_is_named_after_its_script(self):
    parent, helper = self.start_hook(self.tmp / "summarize.py")
    register(self.sessions, parent.pid, "doto")
    register(self.sessions, helper, "repo-1-x-12")

    self.assertEqual(rows(self.sessions)["repo-1-x-12"], ["helper", "doto/summarize"])

  def test_the_session_that_runs_it_is_self(self):
    register(self.sessions, os.getpid(), "menippe")

    self.assertEqual(rows(self.sessions)["menippe"], ["self", "-"])


if __name__ == "__main__":
  unittest.main()
