"""Tests of board-queue: the work queue of a repository's GitHub Project, against a fake gh.

Run: python3 -m unittest discover -s scripts/tests
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "bin" / "board-queue"

CONFIG = """---
board: github-project
owner: someorg
number: 3
repository: someorg/somerepo
fields: [Track]
---
# Next
"""

# Stands in for gh: answers from the JSON file in FAKE_GH_BOARD, applies --jq as gh does, and logs every write
FAKE_GH = r"""#!/usr/bin/env python3
import json, os, re, subprocess, sys

args = sys.argv[1:]
board = json.load(open(os.environ["FAKE_GH_BOARD"]))


def answer(document, failed=False):
  text = json.dumps(document)
  if "--jq" in args and not failed:
    text = subprocess.run(["jq", "--raw-output", "--compact-output", args[args.index("--jq") + 1]], input=text, capture_output=True, text=True, check=True).stdout
  sys.stdout.write(text)
  sys.exit(1 if failed else 0)


def write():
  with open(os.environ["FAKE_GH_WRITES"], "a") as writes:
    writes.write(" ".join(args) + "\n")
  sys.exit(0)


def field(name):
  return next(a.split("=", 1)[1] for a in args if a.startswith(f"{name}="))


if args[:2] == ["api", "-i"]:
  print('x-oauth-scopes: project, repo\n\n{"login": "me"}')
  sys.exit(0)
if args[:2] == ["api", "user"]:
  answer({"login": "me"})
if "--method" in args or args[:2] == ["project", "item-edit"]:
  write()
if args[0] == "api" and args[1].startswith("repos/"):
  number = args[1].rsplit("/", 1)[1]
  holders = board["holders"].get(number, [])
  if os.path.exists(os.environ["FAKE_GH_WRITES"]):
    holders = holders + ["me"]
  answer({"assignees": [{"login": login} for login in holders]})

query = field("query")
owner = {"data": {"repositoryOwner": {"projectV2": None}}}
if "projectV2(number: $number) { id }" in query:
  answer({"data": {"repositoryOwner": {"projectV2": {"id": "board"}}}})
if 'field(name: "Status")' in query:
  options = [{"id": f"option-{name}", "name": name} for name in ["Backlog", "Todo", "In Progress", "Done"]]
  answer({"data": {"repositoryOwner": {"projectV2": {"id": "board", "field": {"id": "status-field", "options": options}}}}})
if "items(first" in query:
  answer({"data": {"repositoryOwner": {"projectV2": {"items": {"nodes": board["items"]}}}}})
if "issueOrPullRequest(number: $number)" in query:
  number = int(field("number"))
  answer({"data": {"repository": {"issueOrPullRequest": {"number": number, **board["issues"].get(str(number), {"body": ""})}}}})

asked = re.findall(r"i(\d+): issueOrPullRequest", query)
answer({"data": {"repository": {f"i{n}": {"state": board["states"].get(n, "CLOSED")} for n in asked}}})
"""


def item(number, status="Todo", assignees=(), track=None, open_sub_issues=0):
  values = [{"name": status, "field": {"name": "Status"}}]
  if track:
    values.append({"name": track, "field": {"name": "Track"}})
  return {
    "id": f"item{number}",
    "fieldValues": {"nodes": values},
    "content": {
      "number": number,
      "title": f"Issue {number}",
      "state": "OPEN",
      "updatedAt": "2026-11-19T00:00:00Z",
      "subIssuesSummary": {"total": open_sub_issues, "completed": 0},
      "assignees": {"nodes": [{"login": login} for login in assignees]},
    },
  }


class BoardQueue(unittest.TestCase):
  def setUp(self):
    self.directory = tempfile.TemporaryDirectory()
    self.path = pathlib.Path(self.directory.name)
    gh = self.path / "gh"
    gh.write_text(FAKE_GH.replace("/usr/bin/env python3", sys.executable + " -I"))
    gh.chmod(0o755)
    self.config = self.path / "next.md"
    self.config.write_text(CONFIG)

  def tearDown(self):
    self.directory.cleanup()

  def queue(self, *arguments, items=(), issues=None, states=None, holders=None, config=None):
    board = self.path / "board.json"
    board.write_text(json.dumps({"items": list(items), "issues": issues or {}, "states": states or {}, "holders": holders or {}}))
    env = {
      **os.environ,
      "PATH": f"{self.path}:{os.environ['PATH']}",
      "FAKE_GH_BOARD": str(board),
      "FAKE_GH_WRITES": str(self.path / "writes"),
    }
    return subprocess.run(
      [SCRIPT, "--config", str(config or self.config), *arguments],
      capture_output=True,
      text=True,
      env=env,
      cwd=self.path,
    )

  def writes(self):
    path = self.path / "writes"
    return path.read_text() if path.exists() else ""

  def test_config_prints_the_board(self):
    result = self.queue("config")
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, "owner: someorg\nnumber: 3\nrepository: someorg/somerepo\nfields: Track\n")

  def test_a_repository_without_a_board_is_refused(self):
    config = self.path / "none.md"
    config.write_text("---\nboard: none\n---\n")
    result = self.queue("next", config=config)
    self.assertEqual(result.returncode, 1)
    self.assertIn("says board: none", result.stderr)

  def test_a_number_that_is_not_a_project_number_is_refused(self):
    config = self.path / "bad.md"
    config.write_text(CONFIG.replace("number: 3", "number: 3 or 1"))
    result = self.queue("next", config=config)
    self.assertEqual(result.returncode, 1)
    self.assertIn("is not a project number", result.stderr)

  def test_next_resumes_my_in_progress_item_first(self):
    result = self.queue("next", items=[item(10), item(20, "In Progress", ["me"])])
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertRegex(result.stdout, r"In Progress\s+#20\s+Issue 20")
    self.assertNotIn("#10", result.stdout)

  def test_next_takes_the_top_free_todo(self):
    items = [item(5, "Backlog"), item(11, "Todo", ["someone"]), item(12, "Todo", open_sub_issues=2), item(13), item(14)]
    result = self.queue("next", items=items)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertRegex(result.stdout, r"^Todo\s+#13\s+Issue 13\n$")

  def test_next_skips_an_issue_with_an_open_dependency(self):
    result = self.queue("next", items=[item(13), item(14)], issues={"13": {"body": "Depends on #7"}}, states={"7": "OPEN"})
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertRegex(result.stdout, r"#14")

  def test_next_filters_by_a_configured_field_ignoring_case(self):
    result = self.queue("next", "--filter", "Track=docs", items=[item(13, track="Platform"), item(14, track="Docs")])
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertRegex(result.stdout, r"#14")

  def test_a_filter_value_no_item_has_lists_the_values_in_use(self):
    result = self.queue("next", "--filter", "Track=dcos", items=[item(13, track="Platform"), item(14, track="Docs")])
    self.assertEqual(result.returncode, 1)
    self.assertIn("no item on the board has Track 'dcos'", result.stderr)
    self.assertIn("  Docs\n  Platform", result.stderr)

  def test_claim_assigns_me_and_sets_in_progress_by_its_option_id(self):
    result = self.queue("claim", "13", items=[item(13)])
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertEqual(result.stdout, "#13 is yours (In Progress, assignee me)\n")
    self.assertIn("--method POST repos/someorg/somerepo/issues/13/assignees", self.writes())
    self.assertIn("--project-id board --field-id status-field --single-select-option-id option-In Progress", self.writes())

  def test_claim_refuses_an_issue_someone_else_holds(self):
    result = self.queue("claim", "13", items=[item(13, assignees=["someone"])], holders={"13": ["someone"]})
    self.assertEqual(result.returncode, 1)
    self.assertIn("#13 is held by someone", result.stderr)
    self.assertEqual(self.writes(), "")

  def test_claim_takes_only_an_issue_number(self):
    result = self.queue("claim", "13; rm", items=[item(13)])
    self.assertEqual(result.returncode, 1)
    self.assertIn("claim takes an issue number", result.stderr)

  def test_a_status_the_board_does_not_have_lists_the_ones_it_has(self):
    result = self.queue("status", "13", "Doing", items=[item(13)])
    self.assertEqual(result.returncode, 1)
    self.assertIn("unknown status 'Doing'", result.stderr)
    self.assertIn("  In Progress", result.stderr)

  def test_team_groups_in_progress_by_assignee_with_the_first_field(self):
    items = [item(20, "In Progress", ["me"], track="Docs"), item(21, "In Progress", ["ana"], track="Platform"), item(22, "In Progress", ["me"])]
    result = self.queue("team", items=items)
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertRegex(result.stdout, r"ana \(1\)\s+#21 \[Platform\]")
    self.assertRegex(result.stdout, r"me \(2\)\s+#20 \[Docs\], #22 \[\]")

  def test_doctor_finds_an_in_progress_item_without_assignee(self):
    result = self.queue("doctor", items=[item(30, "In Progress")])
    self.assertEqual(result.returncode, 1)
    self.assertIn("In Progress without assignee: #30 Issue 30", result.stdout)


if __name__ == "__main__":
  unittest.main()
