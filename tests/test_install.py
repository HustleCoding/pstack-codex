import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def install(self, home, *args):
        env = dict(os.environ, CODEX_HOME=str(home))
        return subprocess.run([str(ROOT / "scripts/install.sh"), *args], env=env, capture_output=True, text=True)

    def test_dry_run_does_not_create_codex_home(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "codex"
            result = self.install(home, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(home.exists())

    def test_install_and_reinstall_preserve_user_state(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "codex"
            existing = home / "skills/correct/SKILL.md"
            existing.parent.mkdir(parents=True)
            existing.write_text("the user's previous skill")
            unrelated = home / "skills/unrelated/SKILL.md"
            unrelated.parent.mkdir(parents=True)
            unrelated.write_text("unrelated skill")
            config = home / "pstack/config.md"
            config.parent.mkdir()
            config.write_text("the user's intentional config")
            result = self.install(home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            names = (ROOT / "manifest.txt").read_text().splitlines()
            for name in names:
                self.assertEqual((home / "skills" / name / "SKILL.md").read_bytes(), (ROOT / "skills" / name / "SKILL.md").read_bytes())
            self.assertFalse((home / "skills/poteto-mode/scripts/node_modules").exists())
            self.assertEqual(config.read_text(), "the user's intentional config")
            self.assertEqual(unrelated.read_text(), "unrelated skill")
            backups = list((home / "backups").glob("*/correct/SKILL.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "the user's previous skill")
            result = self.install(home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(len(list((home / "backups").iterdir())), 2)
            self.assertEqual(config.read_text(), "the user's intentional config")

    def test_fresh_install_writes_current_routes(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "codex"
            result = self.install(home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((home / "pstack/config.md").read_bytes(), (ROOT / "config.example.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
