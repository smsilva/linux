"""Tests of pontos-extract-refs (the references of a voice note) and pontos-classification-check (the daily check).

Run: python3 -m unittest discover -s claude/pontos/tests
"""
import datetime
import importlib.machinery
import importlib.util
import json
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


refs = load("pontos-extract-refs")
check = load("pontos-classification-check")

HTML_NOTE = """<html><head><style>body { color: #111; background: #555; }</style>
<script>const accent = "#999";</script></head>
<body><p style="color:#222">Close #462 first, see <a href="https://github.com/getnereus/nereus/pull/12">the PR</a>.</p>
<svg><rect fill="#333"/></svg><p>Order 20261108-0435 follows 1010-voice-tide.md#part.</p></body></html>
"""

GOOD = """---
source: "#pontos/raw/2026-11-08/0912-voice-tide.md"
source_modified_at: 2026-11-08T12:12:00.000Z
classified_by: haiku
classified_at: 2026-11-08T13:00:00-03:00
rules_version: 3
day: 2026-11-08
time: "09:12"
topics: [tide]
topics_proposed: []
project: other
type: idea
tone: neutral
confidence: high
to_refs: []
issue_refs: ["#462"]
---

## Summary
"""
TOPICS = {"tide": "other", "nereus": "Nereus", "reef": "Nereus", "triton": "Triton"}
RAW = {"2026-11-08/0912-voice-tide.md", "2026-11-08/0000-voice-old.html", "2026-11-08/0000-voice-old-html-classification.md"}
PATH = "2026-11-08/0912-voice-tide-classification.md"


def kinds(result, field="errors"):
  return [kind for kind, _ in result[field]]


class ExtractRefs(unittest.TestCase):
  def test_css_colours_of_an_html_note_are_no_issue_refs(self):
    found = refs.extract(HTML_NOTE, is_html=True)
    self.assertEqual(found["issue_refs"], ["#462", "https://github.com/getnereus/nereus/pull/12"])

  def test_order_ids_and_note_names_without_fragment(self):
    found = refs.extract(HTML_NOTE, is_html=True)
    self.assertEqual(found["to_refs"], ["20261108-0435", "1010-voice-tide.md"])

  def test_css_in_a_markdown_note(self):
    text = "Colours: `.card { color: #111; border: 1px solid #555; }` and `color: #777`. Fixes: #42, see #43."
    self.assertEqual(refs.extract(text)["issue_refs"], ["#42", "#43"])

  def test_entities_paths_and_anchors_are_no_issue_refs(self):
    text = "&#123; a/b#45 ##7 #12abc but (#8) and #9."
    self.assertEqual(refs.extract(text)["issue_refs"], ["#8", "#9"])

  def test_urls_deduplicated_and_trailing_punctuation_stripped(self):
    text = "See https://example.com/a. And (https://example.com/a), https://example.com/w_(x) or https://example.com/b!"
    self.assertEqual(refs.extract(text)["source_urls"], ["https://example.com/a", "https://example.com/w_(x)", "https://example.com/b"])

  def test_note_names_take_the_last_part_of_a_path_and_skip_urls(self):
    text = "Read docs/agent/rules.md and 0743-voice-raw.html, not https://example.com/readme.md or notes.md.bak."
    self.assertEqual(refs.extract(text)["to_refs"], ["rules.md", "0743-voice-raw.html"])

  def test_the_command_prints_one_json_line_per_file(self):
    with tempfile.TemporaryDirectory() as directory:
      note = pathlib.Path(directory) / "note.html"
      note.write_text(HTML_NOTE)
      other = pathlib.Path(directory) / "other.md"
      other.write_text("Issue #5 at https://github.com/smsilva/linux/issues/5.")
      done = subprocess.run([sys.executable, str(BIN / "pontos-extract-refs"), str(note), str(other)], capture_output=True, text=True)
    lines = [json.loads(line) for line in done.stdout.splitlines()]
    self.assertEqual(done.returncode, 0)
    self.assertEqual(lines[0]["issue_refs"], ["#462", "https://github.com/getnereus/nereus/pull/12"])
    self.assertEqual(lines[1]["issue_refs"], ["#5", "https://github.com/smsilva/linux/issues/5"])
    self.assertEqual(set(lines[1]), {"file", "to_refs", "issue_refs", "source_urls"})


class CheckClassification(unittest.TestCase):
  def test_a_good_classification_has_no_error(self):
    result = check.check_classification(PATH, GOOD, RAW, TOPICS)
    self.assertEqual(result["errors"], [])
    self.assertEqual(kinds(result, "flags"), ["project-other"])

  def test_an_unquoted_issue_ref_in_a_list_does_not_parse(self):
    result = check.check_classification(PATH, GOOD.replace('["#462"]', "[#462]"), RAW, TOPICS)
    self.assertEqual(kinds(result), ["yaml-parse"])

  def test_an_unquoted_issue_ref_alone_is_a_comment(self):
    result = check.check_classification(PATH, GOOD.replace('["#462"]', "#462"), RAW, TOPICS)
    self.assertEqual(kinds(result), ["yaml-unquoted-hash", "type"])

  def test_keys_enums_topics_day_and_time(self):
    text = (GOOD.replace("tone: neutral\n", "tone: angry\nmood: x\n").replace("confidence: high\n", "")
            .replace("[tide]", "[tide, made-up]").replace("day: 2026-11-08", "day: 2026-11-07").replace('"09:12"', "21:12"))
    result = check.check_classification(PATH, text, RAW, TOPICS)
    self.assertEqual(kinds(result), ["keys", "enum", "topic-unknown", "day", "time"])
    self.assertIn("1272", dict(result["errors"])["time"])

  def test_time_is_null_for_a_0000_note(self):
    path = "2026-11-08/0000-voice-old-html-classification.md"
    text = GOOD.replace("0912-voice-tide.md", "0000-voice-old.html").replace('"09:12"', "null")
    self.assertEqual(check.check_classification(path, text, RAW, TOPICS)["errors"], [])
    self.assertEqual(kinds(check.check_classification(path, text.replace("time: null", 'time: "00:00"'), RAW, TOPICS)), ["time"])

  def test_source_must_be_this_existing_raw_note(self):
    missing = check.check_classification(PATH, GOOD.replace("0912-voice-tide.md", "0912-voice-gone.md"), RAW, TOPICS)
    other = check.check_classification(PATH, GOOD.replace("0912-voice-tide.md", "0000-voice-old.html"), RAW, TOPICS)
    self.assertEqual(kinds(missing), ["source"])
    self.assertEqual(kinds(other), ["source"])

  def test_an_old_source_path_is_information_before_the_move(self):
    old = GOOD.replace('"#pontos/raw/2026-11-08/0912-voice-tide.md"', "dump-mental-prompts/sessions/2026-11-08/x.md")
    early = check.check_classification(PATH, old.replace("classified_at: 2026-11-08", "classified_at: 2026-11-05"), RAW, TOPICS)
    late = check.check_classification(PATH, old, RAW, TOPICS)
    self.assertEqual((early["errors"], kinds(early, "info")), ([], ["legacy-source"]))
    old_schema = check.check_classification(PATH, old.replace("classified_at: 2026-11-08", "classified_at: 2026-11-05").replace("tone: neutral\n", ""), RAW, TOPICS)
    self.assertEqual((old_schema["errors"], kinds(old_schema, "info")), ([], ["legacy-source", "legacy-schema"]))
    self.assertEqual(kinds(late), ["source"])

  def test_css_colours_taken_as_issue_refs(self):
    path = "2026-11-08/0000-voice-old-html-classification.md"
    text = (GOOD.replace("0912-voice-tide.md", "0000-voice-old.html").replace('"09:12"', "null")
            .replace('["#462"]', '["#462", "#111", "#555", "ddd", "#fff"]'))
    result = check.check_classification(path, text, RAW, TOPICS, HTML_NOTE, refs)
    self.assertEqual(kinds(result), ["issue-ref-css-colour", "issue-ref-css-colour", "issue-ref-format", "issue-ref-format"])

  def test_flags_for_review(self):
    text = GOOD.replace("project: other", "project: Triton").replace("[tide]", "[nereus, reef, triton]").replace("confidence: high", "confidence: low")
    self.assertEqual(kinds(check.check_classification(PATH, text, RAW, TOPICS), "flags"), ["confidence-low", "project-differs"])
    empty = GOOD.replace("[tide]", "[]").replace("project: other", "project: Nereus")
    self.assertEqual(kinds(check.check_classification(PATH, empty, RAW, TOPICS), "flags"), ["topics-empty"])

  def test_no_front_matter(self):
    self.assertEqual(kinds(check.check_classification(PATH, "## Summary\n", RAW, TOPICS)), ["yaml-parse"])


class Listing(unittest.TestCase):
  ENTRIES = [
    {"Path": "2026-11-08", "IsDir": True},
    {"Path": "2026-11-08", "IsDir": True},
    {"Path": "2026-11-08/.prev", "IsDir": True},
    {"Path": "2026-11-08/.prev/0912-voice-tide.md", "IsDir": False, "ModTime": "2026-11-08T10:00:00Z"},
    {"Path": "2026-11-08/0912-voice-tide.md", "IsDir": False, "ModTime": "2026-11-08T10:00:00Z"},
    {"Path": "2026-11-08/0912-voice-tide-classification.md", "IsDir": False},
    {"Path": "2026-11-08/0913-voice-page.html", "IsDir": False, "ModTime": "2026-11-08T10:00:00Z"},
    {"Path": "2026-11-08/0914-voice-late.md", "IsDir": False, "ModTime": "2026-11-08T20:00:00Z"},
    {"Path": "2026-11-08/0915-voice-gone-classification.md", "IsDir": False},
    {"Path": "2026-11-08/0916-voice-x-classification.prev.md", "IsDir": False},
    {"Path": "2026-11-08/0917-voice-y.prev.md", "IsDir": False, "ModTime": "2026-11-08T10:00:00Z"},
    {"Path": "2026-11-08/0918-m15-ploto.md", "IsDir": False, "ModTime": "2026-11-08T10:00:00Z"},
  ]

  def test_siblings(self):
    self.assertEqual(check.sibling("d/0912-voice-a.md"), "d/0912-voice-a-classification.md")
    self.assertEqual(check.sibling("d/0912-voice-a.html"), "d/0912-voice-a-html-classification.md")
    self.assertEqual(check.notes_of("d/0912-voice-a-html-classification.md"), ["d/0912-voice-a-html.md", "d/0912-voice-a.html"])

  def test_notes_coverage_orphans_and_duplicates(self):
    notes, classifications = check.split_raw(self.ENTRIES)
    self.assertEqual(sorted(notes), ["2026-11-08/0912-voice-tide.md", "2026-11-08/0913-voice-page.html", "2026-11-08/0914-voice-late.md"])
    watermark = datetime.datetime(2026, 11, 8, 12, tzinfo=datetime.timezone.utc)
    missing, pending, orphans, legacy = check.coverage(notes, classifications, watermark)
    self.assertEqual(missing, ["2026-11-08/0913-voice-page.html"])
    self.assertEqual(pending, ["2026-11-08/0914-voice-late.md"])
    self.assertEqual(orphans, ["2026-11-08/0915-voice-gone-classification.md"])
    self.assertEqual(legacy, [])
    old_name = self.ENTRIES + [{"Path": "2026-11-08/0913-voice-page-classification.md", "IsDir": False}]
    notes, classifications = check.split_raw(old_name)
    missing, _, orphans, legacy = check.coverage(notes, classifications, watermark)
    self.assertEqual((missing, legacy), ([], ["2026-11-08/0913-voice-page-classification.md"]))
    self.assertNotIn("2026-11-08/0913-voice-page-classification.md", orphans)
    self.assertEqual(check.duplicates(self.ENTRIES, "raw"), [("duplicate-folder", "#pontos/raw/2026-11-08", "2 copies")])

  def test_next_run_number_and_watermark(self):
    silver = [{"Path": "classification/2026-11-08/03-classification-worklist.md"},
              {"Path": "classification/2026-11-08/04-classification-report.md"},
              {"Path": "classification/2026-11-07/09-classification-report.md"},
              {"Path": "classification/classification-watermark-20261108-0435.md"},
              {"Path": "classification/classification-watermark-20261108-1050.md"},
              {"Path": "classification/classification-watermark.md"}]
    self.assertEqual(check.next_number(silver, "2026-11-08"), "05")
    self.assertEqual(check.next_number(silver, "2026-11-09"), "01")
    self.assertEqual(check.latest_watermark(silver), "classification-watermark-20261108-1050.md")
    self.assertEqual(check.watermark_time("- last_classified_at: 2026-11-08T10:50:03-03:00\n").hour, 10)

  def test_the_report_ends_with_the_flagged_list(self):
    results = {PATH: check.check_classification(PATH, GOOD.replace('["#462"]', "[#462]"), RAW, TOPICS)}
    counts = {"notes": 2, "classifications": 1, "watermark": "none"}
    report, errors, flagged = check.render(results, [], ["2026-11-08/0913-voice-page.html"], [], [], counts, datetime.datetime(2026, 11, 8, 5, 30))
    self.assertEqual((errors, flagged), (2, 2))
    self.assertIn("### yaml-parse (1)", report)
    self.assertTrue(report.rstrip().endswith('  - "#pontos/raw/2026-11-08/0913-voice-page.html"\n```'))


class Grades(unittest.TestCase):
  LOW = GOOD.replace("confidence: high", "confidence: low")

  def grade(self, grade, classified_at="2026-11-08T13:00:00-03:00", grader="sonnet"):
    return json.dumps({"file": RAW_PREFIX + PATH, "grade": grade, "grader": grader, "classified_at": classified_at})

  def flagged(self, grades_text):
    results = {PATH: check.check_classification(PATH, self.LOW, RAW, TOPICS)}
    counts = {"notes": 1, "classifications": 1, "watermark": "none"}
    return check.render(results, [], [], [], [], counts, datetime.datetime(2026, 11, 8, 5, 30), check.graded(grades_text))

  def test_a_graded_classification_leaves_the_flagged_list(self):
    report, _, flagged = self.flagged(self.grade("acceptable") + "\n")
    self.assertEqual(flagged, 0)
    self.assertIn("already graded, left out: 1", report)

  def test_a_changed_classification_is_flagged_again(self):
    self.assertEqual(self.flagged(self.grade("good", "2026-11-07T04:00:00-03:00"))[2], 1)

  def test_the_latest_wrong_grade_keeps_it_flagged_and_silvio_wins(self):
    self.assertEqual(self.flagged(self.grade("good") + "\n" + self.grade("wrong"))[2], 1)
    self.assertEqual(self.flagged(self.grade("good", grader="silvio") + "\n" + self.grade("wrong"))[2], 0)

  def test_errors_stay_flagged_and_bad_lines_are_ignored(self):
    results = {PATH: check.check_classification(PATH, GOOD.replace('["#462"]', "[#462]"), RAW, TOPICS)}
    counts = {"notes": 1, "classifications": 1, "watermark": "none"}
    grades = check.graded("not json\n" + self.grade("good") + "\n")
    self.assertEqual(check.render(results, [], [], [], [], counts, datetime.datetime(2026, 11, 8, 5, 30), grades)[2], 1)


class Accuracy(unittest.TestCase):
  def line(self, name, grade, grader="sonnet", classified_at="2026-11-08T13:00:00-03:00"):
    return json.dumps({"file": RAW_PREFIX + name, "grade": grade, "grader": grader, "classified_at": classified_at})

  def test_the_latest_grade_counts_and_silvio_counts_double(self):
    text = "\n".join([self.line("a", "wrong"), self.line("a", "good"), self.line("b", "wrong", "silvio"),
                       self.line("c", "acceptable")])
    scores = check.accuracy(text)
    self.assertEqual((scores["good"], scores["total"], scores["classifications"]), (2, 4, 3))
    self.assertEqual(scores["sample_rate"], 20)

  def test_the_window_leaves_older_classifications_out(self):
    text = "\n".join([self.line("old", "wrong", classified_at="2026-11-01T10:00:00-03:00"), self.line("new", "good")])
    scores = check.accuracy(text, check.parse_time("2026-11-05T00:00:00-03:00"))
    self.assertEqual((scores["good"], scores["total"]), (1, 1))

  def test_the_sample_rate_follows_the_accuracy(self):
    good = [self.line(str(index), "good") for index in range(19)]
    self.assertEqual(check.accuracy("\n".join(good + [self.line("x", "wrong")]))["sample_rate"], 5)
    self.assertEqual(check.accuracy("\n".join(good[:9] + [self.line("x", "wrong")]))["sample_rate"], 10)
    self.assertEqual(check.accuracy("\n".join(good[:5]))["sample_rate"], 20)

  def test_the_grade_files_are_the_main_file_and_one_per_run(self):
    entries = [{"Path": "classification/grades/run-b.jsonl"}, {"Path": "classification/classification-grades.jsonl"},
               {"Path": "classification/grades/run-a.jsonl"}, {"Path": "classification/grades/notes.md"}]
    self.assertEqual(check.grade_files(entries), ["classification/classification-grades.jsonl",
                                                  "classification/grades/run-a.jsonl", "classification/grades/run-b.jsonl"])


RAW_PREFIX = "#pontos/raw/"


if __name__ == "__main__":
  unittest.main()
