"""Tests of session-prompt's hook: the prompt after /clear, its archive at a session's end, and its return on resume.

Run: python3 -m unittest discover -s scripts/tests -p test_session_prompt.py
"""
import json
import os
import pathlib
import subprocess
import tempfile
import time
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "session-prompt"


class SessionPrompt(unittest.TestCase):
  def setUp(self):
    directory = tempfile.TemporaryDirectory()
    self.addCleanup(directory.cleanup)
    self.root = pathlib.Path(directory.name)
    self.repository = self.root / "repository"
    self.repository.mkdir()
    subprocess.run(["git", "init", "--quiet", str(self.repository)], check=True)
    self.archive = self.root / "archive"
    self.prompt = self.repository / ".git" / "session-prompts" / "kilo.md"

  def run_script(self, *args, stdin=None, agent="kilo"):
    environment = {key: value for key, value in os.environ.items() if not key.startswith(("AGENT_NAME", "PROMPT_", "CLAUDE_CODE_SESSION_ID"))}
    environment.update({"AGENT_NAME": agent, "PROMPT_ARCHIVE": str(self.archive), "PATH": "/usr/bin:/bin"})
    result = subprocess.run([str(SCRIPT), *args], input=stdin, env=environment, cwd=self.repository, capture_output=True, text=True)
    self.assertEqual(result.returncode, 0, result.stderr)
    return result.stdout

  def hook(self, event, session_id, agent="kilo", **extra):
    payload = json.dumps({"hook_event_name": event, "session_id": session_id, **extra})
    return self.run_script("hook", stdin=payload, agent=agent)

  def save(self, text="# Session prompt: kilo\n"):
    draft = self.root / "draft.md"
    draft.write_text(text)
    self.run_script("save", "--file", str(draft))

  def test_an_exit_archives_the_prompt(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save()
    self.hook("SessionEnd", "s1", reason="prompt_input_exit")
    self.assertFalse(self.prompt.exists())
    self.assertEqual(len(list(self.archive.glob("kilo-*.md"))), 1)

  def test_a_resume_of_the_same_session_takes_the_prompt_back(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save("# Session prompt: kilo\n\nthe start\n")
    self.hook("SessionEnd", "s1", reason="prompt_input_exit")
    output = self.hook("SessionStart", "s1", source="resume")
    self.assertIn("Session prompt of kilo restored from", output)
    self.assertEqual(self.prompt.read_text(), "# Session prompt: kilo\n\nthe start\n")
    self.assertEqual(list(self.archive.glob("kilo-*.md")), [])

  def test_a_restored_prompt_is_not_stale_at_the_next_clear(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save()
    self.hook("SessionEnd", "s1", reason="prompt_input_exit")
    time.sleep(1.1)  # a resume a second later: the start must come back, not be taken from the clock
    self.hook("SessionStart", "s1", source="resume")
    self.hook("SessionEnd", "s1", reason="clear")
    output = self.hook("SessionStart", "s2", source="clear")
    self.assertIn("follow it.", output)
    self.assertNotIn("STALE", output)

  def test_a_resume_of_another_session_does_not_take_it(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save()
    self.hook("SessionEnd", "s1", reason="prompt_input_exit")
    output = self.hook("SessionStart", "s2", source="resume")
    self.assertEqual(output, "")
    self.assertFalse(self.prompt.exists())
    self.assertEqual(len(list(self.archive.glob("kilo-*.md"))), 1)

  def test_a_new_session_does_not_take_it(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save()
    self.hook("SessionEnd", "s1", reason="prompt_input_exit")
    self.hook("SessionStart", "s1", source="startup")
    self.assertFalse(self.prompt.exists())

  def test_clear_keeps_the_prompt_and_prints_it(self):
    self.hook("SessionStart", "s1", source="startup")
    self.save("# Session prompt: kilo\n\nnext step\n")
    self.hook("SessionEnd", "s1", reason="clear")
    output = self.hook("SessionStart", "s2", source="clear")
    self.assertIn("next step", output)
    self.assertTrue(self.prompt.exists())

  def test_a_marker_pointing_outside_the_archive_is_ignored(self):
    self.hook("SessionStart", "s1", source="startup")
    outside = self.root / "outside.md"
    outside.write_text("planted\n")
    marker = self.prompt.with_suffix(".ended")
    marker.write_text(f"session_id=s1\narchive={outside}\nstarted=1\n")
    self.hook("SessionStart", "s1", source="resume")
    self.assertFalse(self.prompt.exists())
    self.assertTrue(outside.exists())

  def test_a_repository_with_its_own_script_refuses_save_and_names_it(self):
    own = self.repository / "scripts" / "session" / "prompt"
    own.parent.mkdir(parents=True)
    own.write_text("#!/usr/bin/env bash\necho 'the repository script ran' > ran\n")
    own.chmod(0o755)
    draft = self.root / "draft.md"
    draft.write_text("# Session prompt: kilo\n")
    environment = {key: value for key, value in os.environ.items() if not key.startswith(("AGENT_NAME", "PROMPT_", "CLAUDE_CODE_SESSION_ID"))}
    environment.update({"AGENT_NAME": "kilo", "PROMPT_ARCHIVE": str(self.archive), "PATH": "/usr/bin:/bin"})
    for args in (["save", "--file", str(draft)], ["show"], ["path"], ["clear", "--topic", "x"]):
      result = subprocess.run([str(SCRIPT), *args], env=environment, cwd=self.repository, capture_output=True, text=True)
      self.assertEqual(result.returncode, 1, args)
      self.assertIn(f"run scripts/session/prompt {args[0]}", result.stderr)
    self.assertFalse(self.prompt.exists())
    self.assertFalse((self.repository / "ran").exists())


if __name__ == "__main__":
  unittest.main()
