"""Tests of pontos-save (the raw log) and claude-guard-main-clone (no change in a main clone).

Run: python3 -m unittest discover -s claude/pontos/tests
"""
import importlib.machinery
import importlib.util
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # no __pycache__ next to the scripts
BIN = pathlib.Path(__file__).resolve().parents[3] / "scripts/bin"


def load(name):
  loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(BIN / name))
  module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
  loader.exec_module(module)
  return module


def git(*args, cwd):
  subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def repository(root, remote):
  """A main clone with one commit and a linked worktree next to it."""
  main = root / "repo"
  main.mkdir()
  git("init", "--initial-branch", "main", cwd=main)
  git("remote", "add", "origin", remote, cwd=main)
  (main / ".gitignore").write_text("CLAUDE.local.md\n")
  (main / "README.md").write_text("readme\n")
  git("add", ".", cwd=main)
  git("-c", "user.email=agent@example.com", "-c", "user.name=agent", "-c", "core.hooksPath=/dev/null", "commit", "--no-verify", "--message", "chore: first", cwd=main)
  git("worktree", "add", str(root / "repo-change"), "-b", "change", cwd=main)
  return main, root / "repo-change"


class Guard(unittest.TestCase):
  def setUp(self):
    self.root = pathlib.Path(tempfile.mkdtemp())

  def guard(self, tool, tool_input, cwd):
    data = json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": str(cwd)})
    return subprocess.run([sys.executable, str(BIN / "claude-guard-main-clone")], input=data, capture_output=True, text=True)

  def test_an_edit_in_the_main_clone_is_refused_with_how_to_make_a_worktree(self):
    main, _ = repository(self.root, "git@github.com:smsilva/linux.git")
    done = self.guard("Edit", {"file_path": str(main / "README.md")}, main)
    self.assertEqual(done.returncode, 2)
    self.assertIn("is the main clone of smsilva/linux", done.stderr)
    self.assertIn("worktree add", done.stderr)

  def test_an_edit_in_a_worktree_or_of_an_ignored_file_passes(self):
    main, worktree = repository(self.root, "git@github.com:smsilva/linux.git")
    self.assertEqual(self.guard("Edit", {"file_path": str(worktree / "README.md")}, main).returncode, 0)
    self.assertEqual(self.guard("Write", {"file_path": str(main / "CLAUDE.local.md")}, main).returncode, 0)

  def test_a_commit_is_refused_in_the_main_clone_and_passes_with_git_c_a_worktree(self):
    main, worktree = repository(self.root, "git@github.com:getnereus/nereus.git")
    self.assertEqual(self.guard("Bash", {"command": "git add . && git commit --message x"}, main).returncode, 2)
    self.assertEqual(self.guard("Bash", {"command": f"git -C {worktree} commit --message x"}, main).returncode, 0)
    self.assertEqual(self.guard("Bash", {"command": f"cd {worktree} && git commit --message x"}, main).returncode, 0)
    self.assertEqual(self.guard("Bash", {"command": "git log --oneline"}, main).returncode, 0)

  def test_a_repository_of_someone_else_is_left_alone(self):
    main, _ = repository(self.root, "git@github.com:someone/else.git")
    self.assertEqual(self.guard("Edit", {"file_path": str(main / "README.md")}, main).returncode, 0)


def transcript(path, lines):
  path.write_text("".join(json.dumps(line) + "\n" for line in lines))


class Pontos(unittest.TestCase):
  def setUp(self):
    self.root = pathlib.Path(tempfile.mkdtemp())
    os.environ["PONTOS_STATE"] = str(self.root / "state")
    os.environ["PONTOS_CONFIG"] = str(self.root / "config")
    os.environ.pop("TMUX_PANE", None)
    self.pontos = load("pontos-save")
    self.main, _ = repository(self.root, "git@github.com:smsilva/linux.git")
    self.session = "ed1a5c33-1b20-4e67-adde-68dc7ab46509"
    self.path = self.root / f"{self.session}.jsonl"
    transcript(self.path, [
      {"type": "user", "timestamp": "2026-10-29T13:00:00Z", "version": "2.1.312", "cwd": str(self.main),
       "message": {"role": "user", "content": "abre o deck, né?"}},
      {"type": "user", "isMeta": True, "timestamp": "2026-10-29T13:00:01Z", "message": {"content": "<local-command-caveat>x"}},
      {"type": "assistant", "timestamp": "2026-10-29T13:00:02Z",
       "message": {"model": "claude-opus-5-5", "content": [{"type": "thinking", "thinking": "private"}]}},
      {"type": "assistant", "timestamp": "2026-10-29T13:00:03Z",
       "message": {"model": "claude-opus-5-5", "content": [{"type": "text", "text": "Abrindo o deck."}]}},
      {"type": "assistant", "timestamp": "2026-10-29T13:00:04Z", "message": {"model": "claude-opus-5-5", "content": [
        {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "gh issue view 479", "description": "Read the issue"}}]}},
      {"type": "user", "timestamp": "2026-10-29T13:00:05Z", "toolUseResult": {},
       "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "secret output"}]}},
      {"type": "assistant", "timestamp": "2026-10-29T13:00:06Z", "message": {"model": "claude-opus-5-5", "content": [
        {"type": "tool_use", "id": "t2", "name": "Write", "input": {"file_path": str(self.main / "a.md"), "content": "x" * 1000}}]}},
    ])
    self.me = self.pontos.identity({"session_id": self.session, "cwd": str(self.main), "transcript_path": str(self.path)})

  def built(self):
    return self.pontos.build_session(self.me)

  def test_the_file_is_named_by_start_time_and_agent_in_its_day_folder(self):
    day, name, _ = self.built()[0]
    started = self.pontos.local_time("2026-10-29T13:00:00Z")
    self.assertEqual(day, started.strftime("%Y-%m-%d"))
    self.assertEqual(name, f"{started.strftime('%H%M')}-{self.me['agent']}.md")
    self.assertTrue(self.me["agent"].endswith("-repo-ed1a5c33"))

  def test_the_header_carries_the_identity(self):
    text = self.built()[0][2]
    self.assertTrue(text.startswith("---\npontos: 1\n"))
    for line in ('repository: "smsilva/linux"', "main_checkout: true", 'model: "claude-opus-5-5"', "issues: [479]",
                 "traceparent: \"00-ed1a5c331b204e67adde68dc7ab46509-0000000000000001-01\""):
      self.assertIn(line, text)

  def test_the_log_keeps_words_and_calls_but_no_outputs_or_thinking(self):
    text = self.built()[0][2]
    self.assertIn("abre o deck, né?", text)
    self.assertIn("Abrindo o deck.", text)
    self.assertIn("gh issue view 479", text)
    self.assertIn("→ ok, 13 chars of output", text)
    self.assertIn('"content": "<1000 chars>"', text)
    for hidden in ("secret output", "private", "local-command-caveat"):
      self.assertNotIn(hidden, text)

  def test_the_check_finds_secrets_and_personal_data(self):
    for text in ("ghp_" + "a" * 36, "token: abcdefghijklmnop", "CPF 123.456.789-09", "write to someone@company.io",
                 "-----BEGIN RSA PRIVATE KEY-----"):
      self.assertTrue(self.pontos.check(text), text)
    self.assertEqual(self.pontos.check("mail agent@example.com, fine"), [])
    self.assertEqual(self.pontos.check("git@github.com:getnereus/nereus.git"), [])
    self.assertEqual(self.pontos.check("me@home.io", {"me@home.io"}), [])

  def test_secrets_inside_json_headers_urls_and_jwts_are_found(self):
    for text in ('{\\"api_key\\": \\"abcdefghijklmnop\\"}', "Authorization: Bearer abcdefghijklmnopqrstuvwxyz",
                 "https://user:pass@example.com/x", "curl -u admin:hunter22 https://x", "Me@Company.IO",
                 "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijklmnopqrstuv"):
      self.assertTrue(self.pontos.check(text), text)

  def test_an_owner_s_name_on_another_host_is_not_opted_in(self):
    self.assertEqual(self.pontos.repository_of("git@github.com:getnereus/nereus.git"), "getnereus/nereus")
    self.assertEqual(self.pontos.repository_of("https://github.com/smsilva/linux"), "smsilva/linux")
    self.assertFalse(self.pontos.opted_in(self.pontos.repository_of("git@gitlab.example.com:smsilva/app.git")))

  def test_the_upload_checks_the_bytes_again(self):
    self.pontos.write_spool(self.session, [("2026-10-29", "x.md", "clean")], set())
    (self.root / f"state/sessions/{self.session}/out/2026-10-29/x.md").write_text("ghp_" + "a" * 36)
    self.pontos.REMOTE = str(self.root / "nowhere")
    self.assertTrue(self.pontos.upload(self.session))
    self.assertIn("2026-10-29/x.md", self.pontos.load(self.root / f"state/sessions/{self.session}/state.json")["blocked"])

  def test_the_deny_list_and_live_tokens_block(self):
    (self.root / "config").mkdir()
    (self.root / "config/deny-list").write_text("# names\nAcme Corp\nC&A.\n")
    self.assertTrue(self.pontos.check("we met at acme corp today"))
    self.assertTrue(self.pontos.check("bought at C&A. yesterday"))
    os.environ["SOME_TOKEN"] = "live-value-1234567890"
    self.addCleanup(os.environ.pop, "SOME_TOKEN")
    self.assertTrue(self.pontos.check("it was live-value-1234567890"))

  def test_a_blocked_file_stays_in_the_spool_and_raises_the_alert(self):
    blocked = self.pontos.write_spool(self.session, [("2026-10-29", "x.md", "ghp_" + "a" * 36)], set())
    self.assertIn("2026-10-29/x.md", blocked)
    self.assertEqual(self.pontos.pending(self.session), [])
    self.assertTrue(self.pontos.alert())
    self.assertTrue((self.root / "state/alert").exists())

  def test_a_blocked_file_holds_back_only_itself_the_clean_ones_go_up(self):
    calls = []
    self.pontos.in_background = lambda *args: calls.append(args)
    self.pontos.build_session = lambda me, end=None: [
      ("2026-10-29", "x.md", "ghp_" + "a" * 36), ("2026-10-29", "x-agent.md", "clean")]
    stdin = sys.stdin
    self.addCleanup(setattr, sys, "stdin", stdin)
    sys.stdin = io.StringIO(json.dumps({"session_id": self.session, "hook_event_name": "SubagentStop",
                                        "cwd": str(self.main), "transcript_path": str(self.path)}))
    self.pontos.hook(None)
    self.assertIn(("upload", "--session", self.session), calls)
    self.assertEqual([key for key, _, _ in self.pontos.pending(self.session)], ["2026-10-29/x-agent.md"])

  def test_redact_keeps_the_words_around_the_value_and_passes_the_check(self):
    (self.root / "config").mkdir(exist_ok=True)
    (self.root / "config/deny-list").write_text("Acme Corp\n")
    text = ("WWW-Authenticate: Bearer resource_metadata_location=\"https://x\"\n  token = os.environ.get(\"X\")\n"
            "write to someone@company.io or agent@example.com at Acme Corp")
    redacted, count = self.pontos.redact(text)
    self.assertEqual(count, 4)
    self.assertIn("Bearer [REDACTED]", redacted)
    self.assertIn("token = [REDACTED]\n", redacted)
    self.assertIn("write to [REDACTED] or agent@example.com at [REDACTED]", redacted)
    self.assertEqual(self.pontos.check(redacted), [])

  def test_redact_leaves_nothing_of_the_secret_behind(self):
    os.environ["SOME_TOKEN"] = "live(value)1234567890"
    self.addCleanup(os.environ.pop, "SOME_TOKEN")
    for text, kept in (("password=abcdefghijklmnop$qrs(tuv) end", "password=[REDACTED] end"),
                       ("aws_secret_access_key = wJal(rXUtnFEMI/K7MDENG end", "aws_secret_access_key = [REDACTED] end"),
                       ("-----BEGIN RSA PRIVATE KEY-----\nMIIEow\nbody\n-----END RSA PRIVATE KEY-----\nend", "[REDACTED]\nend"),
                       ("token: live(value)1234567890 end", "token: [REDACTED] end")):
      redacted, _ = self.pontos.redact(text)
      self.assertEqual(redacted, kept)
      self.assertEqual(self.pontos.check(redacted), [], text)
    # a label with no value, or a redacted one, is no secret
    self.assertEqual(self.pontos.check("the aws_secret_access_key = [REDACTED] label"), [])
    self.assertEqual(self.pontos.check(r"grep 'aws_secret_access_key = \\[REDACTED\\]' in a log"), [])
    self.assertTrue(self.pontos.check(r"aws_secret_access_key = \"wJal(rXUtnFEMI\""))

  def test_redact_never_clears_a_log_that_shrank(self):
    self.pontos.write_spool(self.session, [("2026-10-29", "x.md", "### a\n### b\nghp_" + "a" * 36)], set())
    state = self.pontos.load(self.root / f"state/sessions/{self.session}/state.json")
    state["files"] = {"2026-10-29/x.md": {"turns": 5}}
    self.pontos.save(self.root / f"state/sessions/{self.session}/state.json", state)
    self.pontos.REMOTE = str(self.root / "drive")
    self.pontos.command_redact(type("Args", (), {"session": self.session[:8], "dry_run": False}))
    blocked = self.pontos.load(self.root / f"state/sessions/{self.session}/state.json")["blocked"]
    self.assertIn("the log shrank", blocked["2026-10-29/x.md"][0])

  def test_redact_needs_exactly_one_session(self):
    self.assertEqual(self.pontos.command_redact(type("Args", (), {"session": "nope", "dry_run": True})), 1)

  def test_the_redact_command_unblocks_the_file_and_uploads_it(self):
    self.pontos.write_spool(self.session, [("2026-10-29", "x.md", "Authorization: Bearer abcdefghijklmnopqrstuvwxyz")], set())
    self.pontos.REMOTE = str(self.root / "drive")
    args = type("Args", (), {"session": self.session[:8], "dry_run": False})
    self.assertEqual(self.pontos.command_redact(args), 0)
    state = self.pontos.load(self.root / f"state/sessions/{self.session}/state.json")
    self.assertEqual(state["blocked"], {})
    self.assertEqual((self.root / "drive/raw/2026-10-29/x.md").read_text(), "Authorization: Bearer [REDACTED]")
    self.assertFalse((self.root / "state/alert").exists())
    # an open session rebuilds its log each turn: the next build is redacted too, not blocked again
    self.assertEqual(self.pontos.write_spool(self.session, [("2026-10-29", "x.md", "Bearer abcdefghijklmnopqrstuvwxyz, then more")], set()), {})

  def test_another_owner_s_repository_is_not_opted_in_unless_listed(self):
    self.assertTrue(self.pontos.opted_in("getnereus/nereus"))
    self.assertFalse(self.pontos.opted_in("client/app"))
    (self.root / "config").mkdir(exist_ok=True)
    (self.root / "config/allow-list").write_text("client/app  # mine too\n")
    self.assertTrue(self.pontos.opted_in("client/app"))


if __name__ == "__main__":
  unittest.main()
