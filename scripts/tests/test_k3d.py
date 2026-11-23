"""k3d: every cluster is created without k3d's load balancer (nginx, the image k3d-proxy) and with its API on the
loopback; every other command reaches the real k3d unchanged."""

import os
import pathlib
import re
import subprocess
import tempfile
import unittest

BIN = pathlib.Path(__file__).resolve().parents[1] / "bin"
SCRIPT = BIN / "k3d"


class K3d(unittest.TestCase):
  def setUp(self):
    real = tempfile.TemporaryDirectory()
    self.addCleanup(real.cleanup)
    self.seen = pathlib.Path(real.name) / "seen"
    fake = pathlib.Path(real.name) / "k3d"
    fake.write_text(f'#!/bin/sh\nprintf "%s\\n" "$@" > "{self.seen}"\n')
    fake.chmod(0o755)
    # The wrapper's own folder first, as on the owner's PATH, then the real k3d.
    self.environment = {**os.environ, "PATH": f"{BIN}:{real.name}:{os.environ['PATH']}"}

  def run_k3d(self, *arguments):
    return subprocess.run(["k3d", *arguments], capture_output=True, text=True, env=self.environment)

  def passed(self):
    return self.seen.read_text().splitlines() if self.seen.exists() else None

  def test_a_new_cluster_gets_no_load_balancer_and_its_api_on_the_loopback(self):
    result = self.run_k3d("cluster", "create", "demo", "--wait")
    self.assertEqual(result.returncode, 0, result.stderr)
    arguments = self.passed()
    self.assertEqual(arguments[:4], ["cluster", "create", "demo", "--wait"])
    self.assertIn("--no-lb", arguments)
    self.assertEqual(arguments[arguments.index("--api-port") + 1], "127.0.0.1:random")

  def test_flags_already_given_are_kept_as_they_are(self):
    self.run_k3d("cluster", "create", "demo", "--no-lb", "--api-port", "127.0.0.1:6550")
    self.assertEqual(self.passed(), ["cluster", "create", "demo", "--no-lb", "--api-port", "127.0.0.1:6550"])

  def test_an_api_port_off_the_loopback_is_refused(self):
    for value in ("6550", "0.0.0.0:6550", "random"):
      result = self.run_k3d("cluster", "create", "demo", "--api-port", value)
      self.assertEqual(result.returncode, 1)
      self.assertIn("127.0.0.1", result.stderr)
      self.assertIsNone(self.passed())

  def test_a_port_on_the_load_balancer_is_refused_with_the_direct_form(self):
    for arguments in (["--port", "8080:80@loadbalancer"], ["--port=8080:80@loadbalancer"], ["--port", "8080:80@server:0"]):
      result = self.run_k3d("cluster", "create", "demo", *arguments)
      self.assertEqual(result.returncode, 1, arguments)
      self.assertIn("@server:0:direct", result.stderr)
      self.assertIsNone(self.passed())

  def test_a_direct_port_passes(self):
    result = self.run_k3d("cluster", "create", "demo", "--port", "127.0.0.1:8080:80@server:0:direct")
    self.assertEqual(result.returncode, 0, result.stderr)
    self.assertIn("127.0.0.1:8080:80@server:0:direct", self.passed())

  def test_other_commands_pass_unchanged(self):
    for arguments in (["cluster", "list", "--output", "json"], ["version"], ["cluster", "delete", "demo"]):
      self.run_k3d(*arguments)
      self.assertEqual(self.passed(), arguments)

  def test_with_no_real_k3d_it_says_so(self):
    environment = {**self.environment, "PATH": f"{BIN}:/usr/bin:/bin"}
    result = subprocess.run([SCRIPT, "version"], capture_output=True, text=True, env=environment)
    self.assertEqual(result.returncode, 127)
    self.assertTrue(re.search(r"no k3d on PATH", result.stderr))


if __name__ == "__main__":
  unittest.main()
