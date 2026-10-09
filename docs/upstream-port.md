# Upstream port record

## October 9, 2026: upstream 0.15.15

Reviewed all five pstack commits from `4e5b1cf2ccb0ea3716f08c8ee0a5856b5ab93536` through [`ccb5507cec1546dc88135c1139c811e6c59115ba`](https://github.com/cursor/plugins/commit/ccb5507cec1546dc88135c1139c811e6c59115ba). The latter is the reviewed repository head; the latest pstack-specific commit is `df58112`.

| Upstream commit | Disposition |
|---|---|
| [00b52d9](https://github.com/cursor/plugins/commit/00b52d9) | Keep the help/work boundary. Do not import Cursor's typed-only frontmatter; this port preserves Codex's existing discovery policy and name/description frontmatter. |
| [807c031](https://github.com/cursor/plugins/commit/807c031) | Port prompting and recipe references. Adapt recurring work to requested Codex heartbeat automations, constrain worker fan-out, and preserve authorization boundaries while away. |
| [2cbf585](https://github.com/cursor/plugins/commit/2cbf585) | Adapt the guide additions into `docs/usage.md` and the help references: evidence, prototypes, verifiable plans, repeatable harnesses, benchmarks, repeated mistakes, and longer-run handoffs. Exclude Cursor cloud projects, Bot UI, and the upstream Slack automation pack. |
| [1e56b29](https://github.com/cursor/plugins/commit/1e56b29) | Offer setup now or later once per chat when configuration is missing and relevant, and review seeded defaults during onboarding; answer the original question either way and preserve existing choices. |
| [df58112](https://github.com/cursor/plugins/commit/df58112) | Port explicit budget targets: unlimited now means max, with supported-effort fallback. Preserve balanced Codex-only model routes and three-seat panels. Exclude the switch to non-Codex providers, related wording churn, Cursor plugin metadata, and the excluded orchestration test fixture rename. |

The Codex-only routes still match the active collaboration schema. Balanced keeps the existing efforts. Updating skills does not migrate a user's persisted configuration or silently raise their budget. The help references and usage guide explain actual Codex behavior rather than claiming Cursor invocation controls or cloud isolation.

Validation for this update includes the repository audit, existing unit tests, skill validation for the changed skills, and link checks for the new documentation. Global installation is verified against repository content and preserves existing model configuration. These are packaging checks, not claims of end-to-end workflow evaluation.

## October 5, 2026: upstream 0.15.10

This update ports the pstack changes between `9490cc1cf95d5de2e4941196cdac00dd861812a4` and [`4e5b1cf2ccb0ea3716f08c8ee0a5856b5ab93536`](https://github.com/cursor/plugins/commit/4e5b1cf2ccb0ea3716f08c8ee0a5856b5ab93536). The reviewed upstream version is 0.15.10, checked on October 5, 2026. All 25 pstack commits in that range were reviewed.

The original MIT license and attribution remain. Codex runtime instructions take precedence over upstream Cursor integration.

## Changes reviewed

| Upstream commit | Disposition |
|---|---|
| [63d938c](https://github.com/cursor/plugins/commit/63d938c) | Exclude the Grok default. Codex routes replace provider defaults. |
| [4612556](https://github.com/cursor/plugins/commit/4612556) | Port workflow and schema-first boundary guidance. Adapt runtime tools. |
| [bdf7aa3](https://github.com/cursor/plugins/commit/bdf7aa3) | Adapt the verified multi-PR checklist and executable plan checker. |
| [799151d](https://github.com/cursor/plugins/commit/799151d) | Exclude make-bot-ui and its Grok Bot and Tailscale prerequisites. |
| [6fecddb](https://github.com/cursor/plugins/commit/6fecddb) | Exclude registration of the excluded Bot UI skill. |
| [73f8be4](https://github.com/cursor/plugins/commit/73f8be4) | Exclude Cursor invocation frontmatter. Preserve name and description discovery. |
| [23a56e2](https://github.com/cursor/plugins/commit/23a56e2) | Adapt forge-neutral PR mechanics, stack verification, and schemas. Exclude Fable defaults. |
| [efa2a53](https://github.com/cursor/plugins/commit/efa2a53) | Exclude Cursor plugin logo metadata. |
| [7314f72](https://github.com/cursor/plugins/commit/7314f72) | Exclude the Cursor plugin image size change. |
| [e8d856f](https://github.com/cursor/plugins/commit/e8d856f) | Port prose improvements, attack-the-premise, and test-behavior-not-implementation. |
| [d7cde2b](https://github.com/cursor/plugins/commit/d7cde2b) | Port the prose punctuation pass while retaining Codex runtime wording. |
| [71ed0d1](https://github.com/cursor/plugins/commit/71ed0d1) | Adapt version and skill counts to this port's manifest. |
| [f8abedd](https://github.com/cursor/plugins/commit/f8abedd) | Port evidence-or-label claims. |
| [f5bdd68](https://github.com/cursor/plugins/commit/f5bdd68) | Port operator-neutral wording and report only previously unreported status changes. |
| [889ec4b](https://github.com/cursor/plugins/commit/889ec4b) | Replace provider defaults with Codex bug-fix, perf-issue, and hillclimb routes. |
| [5bf2b15](https://github.com/cursor/plugins/commit/5bf2b15) | Adapt reasoning budgets to verified Codex model and effort pairs. |
| [70b2dc8](https://github.com/cursor/plugins/commit/70b2dc8) | Port benchmark-checklist and workflow updates. Replace Opus and Grok defaults. |
| [b42effe](https://github.com/cursor/plugins/commit/b42effe) | Adapt upgrade help to verified Codex models. |
| [b0b9c7a](https://github.com/cursor/plugins/commit/b0b9c7a) | Port instruction reductions where they preserve Codex runtime and authorization rules. |
| [12d587d](https://github.com/cursor/plugins/commit/12d587d) | Adapt consistent model-config reads, inherited routes, and the simplified How workflow. Retire How's critic panel. |
| [23e4138](https://github.com/cursor/plugins/commit/23e4138) | Port explain-the-number, fresh-owner handoff, schema-first casts, and PR headings. Adapt hourly audits to Codex heartbeat automations. |
| [9511e60](https://github.com/cursor/plugins/commit/9511e60) | Port correct, with architecture and types before lints, tests, or docs. |
| [a586282](https://github.com/cursor/plugins/commit/a586282) | Port architecture screening for split ownership, duplicate APIs, exposed internals, and hand-synced lists. |
| [e43c7ee](https://github.com/cursor/plugins/commit/e43c7ee) | Port the ordered performance mantras. |
| [4e5b1cf](https://github.com/cursor/plugins/commit/4e5b1cf) | Adapt poteto-help to Codex installation, routes, collaboration, and scheduling. |

## Codex adaptations

Model routes use separate `model@reasoning_effort` values, with `inherit-parent` and `auto` for inheritance. The balanced example uses GPT-6.1 Sol, GPT-6 Luna, and GPT-6 Astra. These model slugs and effort ranges were verified against the active Codex schemas and [official model documentation](https://learn.chatgpt.com/docs/models). Model availability must be rechecked in each setup session. The parent model remains a user-selected Codex setting.

Full-history child forks inherit their parent's model and effort. A route override therefore needs a fresh child with minimal task-local context. All fan-out respects the runtime's live capacity. An instruction to keep a task read-only replaces upstream spawn fields that Codex does not expose.

The plan checker preserves the ordered PR blocks, verification rules, performance probe, and review gate. A stated positive number of lanes replaces the fixed ten-lane assumption. CLI and library lanes save terminal receipts; UI lanes save screenshots. Missing or duplicate lanes and missing receipts fail the checker.

PR operations resolve one forge for the run. GitHub CLI remains the default. Origin is optional and only used when detected and able to resolve the repository. Graphite is not required. PR monitoring retains this port's tested GitHub watcher. Merge authority still needs the user's explicit landing scope. Verification receipts are tied to the patch and current head.

Requested hourly follow-up uses a saved Codex heartbeat automation when available. The prompt reports meaningful changes only. No active scheduler is created by installing these skills. Installed playbooks are resolved from the actual pstack source path rather than assumed to live inside the application repository.

Memory and transcript review use scoped Codex history, the active conversation, or supplied artifacts. Unavailable transcripts are an evidence gap. This port keeps its safe worktree cleanup and bounded Orchestrate implementation rather than importing upstream's cloud-agent, orch CLI, or fixed platform assumptions. Upstream guides are represented by the Codex README and poteto-help rather than copied with incompatible installation instructions.

Comment Sicko is supplied as a prompt for a normal Codex collaboration reviewer. It is not a fabricated Codex agent type. The parent reviews its patch, preserves proven constraints without missing approval, and owns application-code fixes. Reflection does not authorize ticket writes or global memory changes.

## Validation

Run `./scripts/audit.py` and `python3 -m unittest discover -s tests -v`. The tests check actual rejection of invalid routes and incomplete plans, then install and reinstall in isolated temporary Codex homes. They verify skill contents, backups, existing configuration, unrelated skills, cache exclusion, and a dry run with no writes.

The bundled watcher retains its 38 tests and strict TypeScript check. GitHub Actions runs these checks on pull requests and pushes to main. Structural validation and these deterministic tests prove packaging and checker behavior. They do not prove every workflow's future LLM behavior or a production application's runtime.
