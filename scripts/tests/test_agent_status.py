"""Tests of agent-status: each agent's claims, their journey's progress, the live state, and the page.

Run: python3 -m unittest discover -s scripts/tests
"""
import json
import os
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent.parent / "bin" / "agent-status"

FAKE_GH = """#!/usr/bin/env python3
import json, sys
issues = {
  "236": {"number": 236, "title": "the page", "html_url": "https://github.com/o/r/issues/236", "parent_issue_url": "https://api.github.com/repos/o/r/issues/200"},
  "200": {"number": 200, "title": "the room's journey", "html_url": "https://github.com/o/r/issues/200", "parent_issue_url": "https://api.github.com/repos/o/r/issues/100", "sub_issues_summary": {"completed": 3, "total": 4}},
  "100": {"number": 100, "title": "the epic", "html_url": "https://github.com/o/r/issues/100"},
}
print(json.dumps(issues[sys.argv[2].rstrip("/").split("/")[-1]]))
"""


class AgentStatus(unittest.TestCase):
  def setUp(self):
    folder = tempfile.TemporaryDirectory()
    self.addCleanup(folder.cleanup)
    self.root = pathlib.Path(folder.name)
    self.state = self.root / "state"
    self.sessions = self.root / "sessions"
    self.sessions.mkdir()
    bin_folder = self.root / "bin"
    bin_folder.mkdir()
    (bin_folder / "gh").write_text(FAKE_GH)
    (bin_folder / "gh").chmod(0o755)
    (bin_folder / "tmux").write_text("#!/bin/sh\nprintf '@1 3\\n@2 1\\n'\n")
    (bin_folder / "tmux").chmod(0o755)
    self.environment = {
      **os.environ,
      "AGENT_STATUS_STATE_DIR": str(self.state),
      "CLAUDE_SESSIONS_DIR": str(self.sessions),
      "CLAUDE_PROJECTS_DIR": str(self.root / "projects"),
      "AGENT_STATUS_HOOK_SETTLE_SECONDS": "0",
      "PATH": f"{bin_folder}:{os.environ['PATH']}",
    }
    self.environment.pop("AGENT_NAME", None)

  def register(self, name, pid=None, status="busy", cwd="/work/repo", session_id="0000aaaa-0000", pane="0:@1.%1"):
    pid = pid or os.getpid()
    (self.sessions / f"{name}.json").write_text(json.dumps({"pid": pid, "name": name, "kind": "interactive", "status": status, "cwd": cwd, "tmux": pane, "sessionId": session_id}))

  def run_script(self, *arguments, stdin=""):
    return subprocess.run([str(SCRIPT), *arguments], capture_output=True, text=True, env=self.environment, input=stdin, check=True)

  def rows(self):
    return json.loads(self.run_script("--json").stdout)

  def page(self):
    return (self.state / "index.html").read_text()

  def claim_jira(self, agent="adapa", issue="FLWP-8"):
    self.run_script(
      "claim", "--agent", agent, "--issue", issue, "--title", "the first controller",
      "--journey", "FLWP-2", "--journey-title", "the audit API Group", "--done", "8", "--total", "10",
      "--epic", "FLWP-1", "--epic-title", "an immutable audit trail",
    )

  def test_a_jira_claim_shows_its_journey_and_progress(self):
    self.register("adapa")
    self.claim_jira()
    row = self.rows()[0]
    self.assertEqual((row["agent"], row["state"], row["issue"]), ("adapa", "busy", "FLWP-8"))
    self.assertEqual((row["journey"]["done"], row["journey"]["total"], row["epic"]["key"]), (8, 10, "FLWP-1"))
    self.assertIn("8/10 · 80%", self.page())
    self.assertIn('http-equiv="refresh"', self.page())
    listing = self.run_script().stdout
    self.assertIn("FLWP-1 an immutable audit trail › FLWP-2 the audit API Group", listing)
    self.assertIn("8/10 80%", listing)

  def test_a_github_claim_finds_its_journey_and_epic(self):
    self.register("adapa")
    self.run_script("claim", "--agent", "adapa", "--issue", "236", "--repo", "o/r")
    row = self.rows()[0]
    self.assertEqual((row["issue"], row["title"]), ("#236", "the page"))
    self.assertEqual((row["journey"]["key"], row["journey"]["done"], row["journey"]["total"]), ("#200", 3, 4))
    self.assertEqual(row["epic"]["title"], "the epic")
    self.assertIn("3/4 · 75%", self.page())

  def test_a_claim_of_a_dead_session_is_orphaned(self):
    self.claim_jira()
    self.assertEqual(self.rows()[0]["state"], "orphaned")

  def test_a_namesake_does_not_inherit_a_dead_sessions_claim(self):
    self.register("adapa")
    self.claim_jira()
    record = json.loads((self.state / "adapa.json").read_text())
    record["pid"] = 1
    (self.state / "adapa.json").write_text(json.dumps(record))
    states = {row.get("issue"): row["state"] for row in self.rows()}
    self.assertEqual(states["FLWP-8"], "orphaned")

  def test_render_drops_the_record_of_a_session_that_is_gone(self):
    self.register("adapa")
    self.claim_jira()
    self.register("enmerkar")
    self.claim_jira(agent="enmerkar", issue="FLWP-9")
    dead = subprocess.Popen(["true"])
    dead.wait()
    record = json.loads((self.state / "adapa.json").read_text())
    record["pid"] = dead.pid
    (self.state / "adapa.json").write_text(json.dumps(record))
    (self.sessions / "adapa.json").unlink()
    self.run_script("render")
    self.assertFalse((self.state / "adapa.json").exists())
    self.assertEqual([row.get("issue") for row in self.rows()], ["FLWP-9"])
    self.assertNotIn("FLWP-8", self.page())

  def test_render_keeps_a_claim_with_no_known_session(self):
    self.claim_jira()
    self.run_script("render")
    self.assertEqual(self.rows()[0]["state"], "orphaned")

  def test_a_live_session_with_no_claim_is_listed(self):
    self.register("enmerkar", status="idle")
    self.assertEqual([(row["agent"], row["state"], row.get("issue")) for row in self.rows()], [("enmerkar", "idle", None)])

  def test_a_session_coordinating_several_issues_has_one_row_each(self):
    self.register("adapa")
    self.claim_jira(issue="FLWP-8")
    self.claim_jira(issue="FLWP-9")
    self.assertEqual([row["issue"] for row in self.rows()], ["FLWP-8", "FLWP-9"])

  def test_claiming_again_updates_and_keeps_the_claim_time(self):
    self.register("adapa")
    self.claim_jira()
    first = self.rows()[0]["claimed_at"]
    self.run_script("claim", "--agent", "adapa", "--issue", "FLWP-8", "--journey", "FLWP-2", "--done", "9", "--total", "10")
    rows = self.rows()
    self.assertEqual((len(rows), rows[0]["journey"]["done"], rows[0]["claimed_at"]), (1, 9, first))

  def test_release_drops_the_claim(self):
    self.register("adapa")
    self.claim_jira()
    self.run_script("release", "--agent", "adapa", "--issue", "FLWP-8")
    self.assertEqual([row.get("issue") for row in self.rows()], [None])

  def test_titles_are_escaped_on_the_page(self):
    self.register("adapa")
    self.run_script("claim", "--agent", "adapa", "--issue", "FLWP-3", "--title", "<script>alert(1)</script>", "--url", "javascript:alert(1)")
    page = self.page()
    self.assertNotIn("<script>alert", page)
    self.assertNotIn("javascript:", page)

  def test_off_records_nothing_and_the_page_says_so(self):
    self.register("adapa")
    self.run_script("off")
    self.assertIn("Agent status is off", self.page())
    self.assertIn("off, nothing recorded", self.run_script("claim", "--agent", "adapa", "--issue", "FLWP-8").stdout)
    self.assertFalse((self.state / "adapa.json").exists())
    state = subprocess.run([str(SCRIPT), "state"], capture_output=True, text=True, env=self.environment)
    self.assertEqual((state.stdout.strip(), state.returncode), ("off", 1))
    self.run_script("on")
    self.claim_jira()
    self.assertIn("8/10 · 80%", self.page())

  def test_the_folder_is_the_main_clones_name_also_from_a_worktree(self):
    main = self.root / "repos" / "linux"
    (main / ".git" / "worktrees" / "linux-columns").mkdir(parents=True)
    worktree = self.root / "repos" / "linux-columns"
    (worktree / "scripts").mkdir(parents=True)
    (worktree / ".git").write_text(f"gitdir: {main}/.git/worktrees/linux-columns\n")
    self.register("adapa", cwd=str(main))
    self.register("etana", cwd=str(worktree / "scripts"))
    self.assertEqual({row["agent"]: row["folder"] for row in self.rows()}, {"adapa": "linux", "etana": "linux"})
  def repository(self, main_branch="main", worktrees=()):
    """A main clone with linked worktrees, each (folder, branch), made of bare .git files."""
    main = self.root / "repos" / "platform-api"
    (main / ".git").mkdir(parents=True)
    (main / ".git" / "HEAD").write_text(f"ref: refs/heads/{main_branch}\n")
    for folder, branch in worktrees:
      gitdir = main / ".git" / "worktrees" / folder
      gitdir.mkdir(parents=True)
      worktree = self.root / "repos" / folder
      worktree.mkdir(parents=True)
      (worktree / ".git").write_text(f"gitdir: {gitdir}\n")
      (gitdir / "gitdir").write_text(f"{worktree}/.git\n")
      (gitdir / "HEAD").write_text(f"ref: refs/heads/{branch}\n")
    return main

  def test_a_session_with_no_claim_shows_the_issue_of_its_worktrees_branch(self):
    main = self.repository(worktrees=[("platform-api-77301", "feat/FLWP-77301-trail-store-alert")])
    self.register("nanni", cwd=str(self.root / "repos" / "platform-api-77301"))
    row = self.rows()[0]
    self.assertEqual((row["issue"], row["inferred"], row["about"]), ("FLWP-77301", True, "branch feat/FLWP-77301-trail-store-alert"))
    self.assertIn("FLWP-77301?", self.run_script().stdout)
    self.run_script("render")
    self.assertIn('FLWP-77301 <small>inferred</small>', self.page())

  def test_a_session_in_the_main_clone_shows_the_issue_of_the_worktree_it_used_last(self):
    main = self.repository(worktrees=[("linux-old", "feat/12-old"), ("linux-236", "feat/236-the-page")])
    self.register("adapa", cwd=str(main), session_id="0000aaaa-0001")
    transcript = self.root / "projects" / "-repos" / "0000aaaa-0001.jsonl"
    transcript.parent.mkdir(parents=True)
    calls = [{"command": f"git -C {self.root}/repos/linux-old status"}, {"file_path": f"{self.root}/repos/linux-236/README.md"}]
    transcript.write_text("".join(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "input": call}]}}) + "\n" for call in calls))
    self.assertEqual(self.rows()[0]["issue"], "#236")

  def test_a_session_on_main_with_no_worktree_shows_no_issue(self):
    main = self.repository()
    self.register("adapa", cwd=str(main))
    self.assertNotIn("issue", self.rows()[0])

  def test_a_claim_wins_over_the_branch(self):
    self.repository(worktrees=[("platform-api-77301", "feat/FLWP-77301-trail-store-alert")])
    self.register("adapa", cwd=str(self.root / "repos" / "platform-api-77301"))
    self.claim_jira()
    self.assertEqual([(row["issue"], row.get("inferred")) for row in self.rows()], [("FLWP-8", None)])

  def test_about_is_the_work_shown_after_the_issue(self):
    self.register("adapa")
    self.run_script("claim", "--agent", "adapa", "--issue", "FLWP-8", "--title", "the long title", "--about", "the hook")
    self.assertIn('<span title="the long title">the hook</span>', self.page())
    self.assertIn("the hook", self.run_script().stdout)

  def test_rows_sort_by_agent_or_by_tmux_window(self):
    self.register("adapa", pane="0:@1.%1")
    self.register("etana", pane="0:@2.%7")
    self.assertEqual([(row["agent"], row["window"]) for row in self.rows()], [("adapa", 3), ("etana", 1)])
    by_window = json.loads(self.run_script("list", "--sort", "window", "--json").stdout)
    self.assertEqual([row["agent"] for row in by_window], ["etana", "adapa"])
    self.run_script("render")
    self.assertIn('data-column="window" data-v="1"', self.page())
    self.assertIn('th data-sort="progress" data-numeric="yes"', self.page())

  def test_rows_sort_by_progress_with_the_empty_ones_last(self):
    self.register("adapa")
    self.register("etana")
    self.register("nami")
    self.run_script("claim", "--agent", "adapa", "--issue", "FLWP-1", "--journey", "FLWP-9", "--done", "2", "--total", "10")
    self.run_script("claim", "--agent", "etana", "--issue", "FLWP-2", "--journey", "FLWP-9", "--done", "1", "--total", "10")
    by_progress = json.loads(self.run_script("list", "--sort", "progress", "--json").stdout)
    self.assertEqual([row["agent"] for row in by_progress], ["etana", "adapa", "nami"])

  def test_the_hook_renders_and_prints_nothing(self):
    self.register("adapa")
    done = self.run_script("hook", stdin='{"hook_event_name": "Stop"}')
    self.assertEqual(done.stdout, "")
    self.assertIn("adapa", self.page())


if __name__ == "__main__":
  unittest.main()
