import os
import shutil
from pathlib import Path
import subprocess
import sys
import textwrap
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTests(unittest.TestCase):
    def install(self, home, *args, extra_env=None):
        env = dict(os.environ, CODEX_HOME=str(home))
        env.update(extra_env or {})
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

    def test_failed_install_restores_catalog_and_metadata(self):
        for failure in ["stage", "activate", "final"]:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as folder:
                home = Path(folder) / "codex"
                existing = home / "skills/arena/SKILL.md"
                existing.parent.mkdir(parents=True)
                existing.write_text("previous arena")
                config = home / "pstack/config.md"
                config.parent.mkdir()
                config.write_text("intentional configuration")
                manifest = config.parent / "manifest.txt"
                manifest.write_text("previous manifest")
                unrelated = home / "skills/unrelated/SKILL.md"
                unrelated.parent.mkdir()
                unrelated.write_text("unrelated")
                shims = Path(folder) / "bin"
                shims.mkdir()
                audit = shims / "python3"
                audit.write_text(textwrap.dedent(f"""\
                    #!{sys.executable}
                    import os, sys
                    if '--skills-root' in sys.argv:
                        root = sys.argv[sys.argv.index('--skills-root') + 1]
                        if os.environ['INSTALL_FAILURE'] == 'stage' or (os.environ['INSTALL_FAILURE'] == 'final' and root == os.environ['CODEX_HOME'] + '/skills'):
                            sys.exit(42)
                    os.execv({sys.executable!r}, [{sys.executable!r}] + sys.argv[1:])
                """))
                audit.chmod(0o755)
                real_mv = shutil.which("mv")
                move = shims / "mv"
                move.write_text(textwrap.dedent(f"""\
                    #!{sys.executable}
                    import os, sys
                    if os.environ['INSTALL_FAILURE'] == 'activate' and '.pstack-stage.' in sys.argv[1] and sys.argv[-1].endswith('/arena'):
                        sys.exit(42)
                    os.execv({real_mv!r}, [{real_mv!r}] + sys.argv[1:])
                """))
                move.chmod(0o755)
                result = self.install(home, extra_env=dict(PATH=str(shims) + os.pathsep + os.environ["PATH"], INSTALL_FAILURE=failure))
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(existing.read_text(), "previous arena")
                self.assertEqual(config.read_text(), "intentional configuration")
                self.assertEqual(manifest.read_text(), "previous manifest")
                self.assertEqual(unrelated.read_text(), "unrelated")
                self.assertEqual(sorted(p.name for p in (home / "skills").iterdir()), ["arena", "unrelated"])
                self.assertEqual(list(home.glob(".pstack-stage.*")), [])

    def test_fresh_install_writes_current_routes(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder) / "codex"
            result = self.install(home)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((home / "pstack/config.md").read_bytes(), (ROOT / "config.example.md").read_bytes())


if __name__ == "__main__":
    unittest.main()
