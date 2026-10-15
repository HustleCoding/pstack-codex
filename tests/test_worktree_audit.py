from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/poteto-mode/scripts/worktree-audit.sh"


@unittest.skipUnless(shutil.which("git") and shutil.which("jq"), "git and jq required")
class WorktreeAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="audit-test-", dir=ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.source = self.root / "source"
        self.run_command("git", "init", "-b", "integration", str(self.source))
        self.git(self.source, "config", "user.email", "test@example.invalid")
        self.git(self.source, "config", "user.name", "Test")
        self.git(self.source, "commit", "--allow-empty", "-m", "initial")
        self.git(self.source, "branch", "main")
        self.git(self.source, "commit", "--allow-empty", "-m", "integration only")
        self.checkout = self.root / "checkout"
        self.run_command("git", "clone", "--single-branch", str(self.source), str(self.checkout))
        self.candidate = self.root / "candidate"
        self.git(self.checkout, "worktree", "add", "-b", "candidate", str(self.candidate))
        self.bin = self.root / "bin"
        self.bin.mkdir()
        gh = self.bin / "gh"
        gh.write_text('#!/bin/sh\n[ "${FAKE_GH_FAILURE:-}" != yes ] || exit 1\nprintf "%s\\n" "${FAKE_GH_PRS:-[]}"\n')
        gh.chmod(0o755)
        self.env["PATH"] = str(self.bin) + os.pathsep + self.env["PATH"]

    def run_command(self, *args):
        result = subprocess.run(args, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def git(self, repo, *args):
        return self.run_command("git", "-C", str(repo), *args)

    def audit(self, *args):
        return subprocess.run(["bash", str(SCRIPT), *args, str(self.checkout)], env=self.env, capture_output=True, text=True)

    def row(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = [line for line in result.stdout.splitlines() if not line.startswith("#")]
        self.assertEqual(len(lines), 2, result.stdout)
        return dict(zip(lines[0].split("\t"), lines[1].split("\t")))

    def test_uses_remote_default_instead_of_main(self):
        result = self.audit()
        self.assertIn("# base: origin/integration", result.stdout)
        row = self.row(result)
        self.assertEqual(row["MERGED"], "YES")
        self.assertEqual(row["BUCKET"], "verify-task-usage")

    def test_explicit_base_is_fetched_in_single_branch_clone(self):
        self.assertNotEqual(subprocess.run(["git", "-C", str(self.checkout), "rev-parse", "--verify", "origin/main"], capture_output=True).returncode, 0)
        result = self.audit("--base", "origin/main")
        self.assertIn("# base: origin/main", result.stdout)
        self.assertEqual(self.row(result)["MERGED"], "no")
        self.git(self.checkout, "rev-parse", "--verify", "origin/main")

    def test_refreshes_existing_remote_ref_before_audit(self):
        self.git(self.source, "branch", "-f", "main", "integration")
        self.assertEqual(self.row(self.audit("-b", "origin/main"))["MERGED"], "YES")
        self.git(self.source, "branch", "-f", "main", "integration~1")
        self.assertEqual(self.row(self.audit("-b", "origin/main"))["MERGED"], "no")

    def test_local_base_works_without_remote(self):
        self.git(self.checkout, "remote", "remove", "origin")
        self.assertEqual(self.row(self.audit("-b", "integration"))["MERGED"], "YES")

    def test_missing_base_fails_with_actionable_error(self):
        result = self.audit("-b", "absent")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("base ref not found: absent", result.stderr)
        self.git(self.checkout, "remote", "remove", "origin")
        result = self.audit()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("pass -b <ref>", result.stderr)

    def test_falls_back_to_main_then_master_without_origin_head(self):
        self.git(self.checkout, "fetch", "origin", "refs/heads/main:refs/remotes/origin/main")
        self.git(self.checkout, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
        self.assertIn("# base: origin/main", self.audit().stdout)
        self.git(self.source, "branch", "master", "main")
        self.git(self.checkout, "fetch", "origin", "refs/heads/master:refs/remotes/origin/master")
        self.git(self.checkout, "update-ref", "-d", "refs/remotes/origin/main")
        self.assertIn("# base: origin/master", self.audit().stdout)

    def test_keeps_open_pr_and_unknown_pr_holds(self):
        self.env["FAKE_GH_PRS"] = json.dumps([{"number": 12, "state": "OPEN", "headRefName": "candidate"}])
        self.assertEqual(self.row(self.audit())["BUCKET"], "hold-open-pr")
        self.env["FAKE_GH_FAILURE"] = "yes"
        row = self.row(self.audit())
        self.assertEqual(row["PR"], "?")
        self.assertEqual(row["BUCKET"], "review")

    def test_rejects_bad_arguments(self):
        for args in [("--unknown",), ("-b",), ("one", "two")]:
            with self.subTest(args=args):
                result = subprocess.run(["bash", str(SCRIPT), *args], env=self.env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)


if __name__ == "__main__":
    unittest.main()
