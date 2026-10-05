import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pstack_audit", ROOT / "scripts/audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def routes(self, transform=lambda text: text):
        with tempfile.TemporaryDirectory() as folder:
            config = Path(folder) / "config.md"
            config.write_text(transform((ROOT / "config.example.md").read_text()))
            return audit.model_routes(config, audit.DEFAULT_MODEL_SLUGS)

    def test_recommended_routes_are_valid(self):
        routes, errors = self.routes()
        self.assertEqual(errors, [])
        self.assertEqual({model for entries in routes.values() for model, _ in entries}, audit.DEFAULT_MODEL_SLUGS)

    def test_luna_ultra_is_rejected(self):
        _, errors = self.routes(lambda text: text.replace("gpt-6-luna@medium", "gpt-6-luna@ultra"))
        self.assertTrue(any("unsupported reasoning effort" in error for error in errors))

    def test_unavailable_provider_is_rejected(self):
        _, errors = self.routes(lambda text: text.replace("gpt-6.1-sol@medium", "claude-opus-5-5@high"))
        self.assertTrue(any("unavailable model" in error for error in errors))

    def test_inherited_panel_seats_keep_the_count(self):
        _, errors = self.routes(lambda text: text.replace("gpt-6-luna@high, gpt-6.1-sol@high, gpt-6-astra@high", "inherit-parent, auto, inherit-parent"))
        self.assertEqual(errors, [])

    def test_parent_model_effort_is_checked(self):
        _, errors = self.routes(lambda text: text.replace("gpt-6.1-sol@high for", "gpt-6-luna@ultra for"))
        self.assertTrue(any("unsupported parent-task effort" in error for error in errors))

    def test_panel_count_mismatch_is_rejected(self):
        _, errors = self.routes(lambda text: text.replace("- default review panel: 3", "- default review panel: 2"))
        self.assertTrue(any("interrogate reviewers needs 2 entries" in error for error in errors))

    def test_duplicate_route_is_rejected(self):
        _, errors = self.routes(lambda text: text.replace("## Model routes\n", "## Model routes\n\n- default child: inherit-parent\n"))
        self.assertTrue(any("duplicate model route" in error for error in errors))

    def test_single_role_cannot_be_a_panel(self):
        _, errors = self.routes(lambda text: text.replace("- default child: gpt-6-luna@medium", "- default child: inherit-parent, auto"))
        self.assertTrue(any("default child needs exactly one" in error for error in errors))

    def test_duplicate_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate frontmatter"):
            audit.frontmatter("---\nname: first\nname: second\ndescription: test\n---\n")

    def test_broken_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            skills = Path(folder)
            for name in (ROOT / "manifest.txt").read_text().splitlines():
                (skills / name).mkdir()
                (skills / name / "SKILL.md").write_text(f"---\nname: {name}\ndescription: test\n---\n")
            with (skills / "correct/SKILL.md").open("a") as file:
                file.write("Read [missing](references/missing.md).\n")
            result = subprocess.run([str(ROOT / "scripts/audit.py"), "--skills-root", str(skills)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing Markdown target references/missing.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
