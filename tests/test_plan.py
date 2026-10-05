from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULE = "Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked."


def plan(lanes=3):
    program = "\n".join(f"### {name}\n\n- [ ] Complete the task and save its output.\n" for name in ["Arm the program", "Spawn owners", "PR mechanics", "Verdict and merge", "Boot recipe"])
    live = "\n".join(f"- [ ] Lane {n}. Run the real CLI scenario. Save `lane-{n}.txt`. Pass when the persisted output matches the expected result." for n in range(1, lanes + 1))
    return f"""# CLI update plan

Update the CLI output for its users in PR1.

## How to read this

One box is one unit of work. Every box names the evidence.
Check a box only when its evidence exists.
Run `playbooks/autopilot-stack.md`.
{RULE}

## Program checklist

{program}
Read installed playbooks before starting.
Save an hourly Codex heartbeat automation that sends a status message only for a change.

## Update the CLI (PR1)

**Depends on.** None.

**Files.**

- [ ] Edit `cli.ts`.

**Build.**

- [ ] Update the output formatter.

**You see.**

- [ ] CLI output contains the requested value.

**Verify, unit.** {RULE}

- [ ] Run `bun test cli.test.ts` and save the output.

**Verify, live.** {RULE} {lanes} lanes on `gpt-6-luna@high` at the PR head.

{live}

**Verify, perf.** {RULE}

- [ ] Metric. CLI wall time in ms.
- [ ] Probe. Alternate trunk and head five times.
- [ ] Baseline. Save the trunk values first.
- [ ] Rule. Head must stay below 100 ms.

**Review gate.** None. PR1 is not review-gated.

**Merge.**

- [ ] Keep the verified PR at merge-ready for the operator.

## Close the program

- [ ] Save the evidence and report the outcome.

## Appendix A. Prototype evidence

The existing CLI fixture proves the format.

## Appendix B. Alternatives rejected

No extra formatter layer.

## Appendix C. Risks

CLI consumers may parse the old output.

## Appendix D. Links and reading list

Read `cli.ts` and `cli.test.ts`.
"""


class PlanTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "plan.md"
            file.write_text(text)
            return subprocess.run([shutil.which("node") or shutil.which("bun"), str(ROOT / "skills/poteto-mode/scripts/check-plan.mjs"), str(file)], capture_output=True, text=True)

    def test_bounded_panel_with_terminal_receipts_passes(self):
        result = self.check(plan(3))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_one_lane_can_be_enough_for_a_narrow_change(self):
        result = self.check(plan(1))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_required_lane_fails(self):
        result = self.check(plan(3).replace("- [ ] Lane 2.", "- [ ] Missing lane 2."))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected 1 to 3", result.stderr)

    def test_missing_receipt_fails(self):
        result = self.check(plan().replace("Save `lane-1.txt`.", ""))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("names no evidence receipt", result.stderr)

    def test_missing_verification_rule_fails(self):
        result = self.check(plan().replace(f"**Verify, unit.** {RULE}", "**Verify, unit.** Run the tests."))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not open with the rule", result.stderr)

    def test_an_unarmed_audit_tick_fails(self):
        result = self.check(plan().replace("hourly Codex heartbeat automation", "later audit"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("hourly Codex heartbeat automation", result.stderr)


if __name__ == "__main__":
    unittest.main()
