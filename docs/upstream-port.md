# Upstream port record

## October 15, 2026: upstream 0.15.25

Reviewed all 29 pstack commits after `ccb5507cec1546dc88135c1139c811e6c59115ba` through [`e5136d82418d2db3165ea1050d17577cd618cc05`](https://github.com/cursor/plugins/commit/e5136d82418d2db3165ea1050d17577cd618cc05). This is a Codex-native port of the corresponding pstack 0.15.25 changes, not a package of the upstream runtime integrations.

The catalog adds **ketchup**, **in-your-own-words**, and **sharpen**, for **53 skills** including 24 principles. Existing persisted model configuration is preserved. Per-task effort selection uses only supported Codex pairs and does not rewrite the user's budget or model routes.

| Upstream commit | Disposition |
|---|---|
| [00b14f1](https://github.com/cursor/plugins/commit/00b14f1df36b32a8dd1529324a3a459f6563b127) | Port shorter skills, principle leaves, reviewer prompts, and source references while preserving Codex routes and authorization. |
| [978ca6e](https://github.com/cursor/plugins/commit/978ca6e9c0e012047cd5058b8e829240336e704e) | Add ketchup as a read-only catch-up skill. Remove unsupported invocation frontmatter. |
| [ea32d95](https://github.com/cursor/plugins/commit/ea32d9562a1c9f077d7cdd3be53d07383eb18866) | Port factual before/after visuals and unresolved user decisions in ketchup. |
| [08bd59b](https://github.com/cursor/plugins/commit/08bd59b37834550f5e8fa0bb5e8852204a7534cf) | Port useful reductions. Retain Codex configuration, review, history, and scope rules. |
| [de2dba6](https://github.com/cursor/plugins/commit/de2dba6ffa001bc3c97acf1f58bc7ab29d5fdc7a) | Exclude the Grok agent-id rename. Codex uses a normal collaboration reviewer and the existing Comment Sicko prompt. |
| [87c8103](https://github.com/cursor/plugins/commit/87c810326a9a1dc727651b7d9bbfc5a116d68582) | Port matching CommonMark fence semantics and tests while preserving the stricter Codex unclosed-fence check and configurable lanes. |
| [ff8f83d](https://github.com/cursor/plugins/commit/ff8f83da30af53de945acd0e1dc10a7b21a3187f) | Port review-thread pagination and owner-approval ACTION_REQUIRED classification with typed page fixtures and tests. Reject malformed or repeated continuation cursors. |
| [bc697d0](https://github.com/cursor/plugins/commit/bc697d0a5a163cec979e362b601e36f5616083fd) | Port the narrower unslop description. Its use remains explicit in the pstack workflow. |
| [cf9a111](https://github.com/cursor/plugins/commit/cf9a111eaf1eda5724abb607ef4c446ced843d65) | Adapt worktree audit to resolve the remote default branch or explicit base, fetch the exact remote ref, and preserve Codex task-use checks. |
| [2bd5dd4](https://github.com/cursor/plugins/commit/2bd5dd4f22ef958435082c417c027079f8f4ddb7) | Port the receiving-chat runner rule. Ordinary Codex agents execute bounded steps rather than taking over the playbook. |
| [e5a02f8](https://github.com/cursor/plugins/commit/e5a02f8fb0409c2db7eb06eae9078b235a2b5009) | Exclude the upstream Agent Plugins manifest. The Codex package uses its audited skill manifest and installer. |
| [c49b37a](https://github.com/cursor/plugins/commit/c49b37a2c0e7bede60a71ad7322e3f12c337a3da) | Port usable readiness from empty data, migrations and seed data, failed journey preconditions, and stand-in environment limitations. |
| [1b6d44f](https://github.com/cursor/plugins/commit/1b6d44ff26d4e242f4e8f68c391e6d2f7ca16def) | Record upstream version history only. No Cursor plugin metadata is packaged. |
| [364a77e](https://github.com/cursor/plugins/commit/364a77eb358f16292410a7295fd8d103fb7dd40e) | Adapt bundled leaf discovery to the actual poteto-mode path supplied in child prompts. |
| [997ffc7](https://github.com/cursor/plugins/commit/997ffc7fe26bdaa6478a14e7f5b8d5f9ed747102) | Record upstream version history only. No Cursor plugin metadata is packaged. |
| [b93e811](https://github.com/cursor/plugins/commit/b93e8117880f695bc49ef7b1ef72c09bfcc7c1de) | Retain name/description-only frontmatter and Codex skill discovery. Adapt leaf paths and help; exclude Cursor slash-menu and agent-model metadata. |
| [7d8d909](https://github.com/cursor/plugins/commit/7d8d9091e59a1fe9600bb317a1b7f69a31daa349) | Add in-your-own-words to restate the user goal and problem without introducing an approval gate. |
| [d00ba6e](https://github.com/cursor/plugins/commit/d00ba6ee9b26ff3bb084b8a5051ff6436860cbdf) | Port short ketchup replies built on existing visual evidence, with explicit missing evidence. |
| [36cecbf](https://github.com/cursor/plugins/commit/36cecbf2b5089b275254d59cb4612d6f96f00fbd) | Port the proposal for a cheap always-on diagnostic signal after a difficult diagnosis. This does not enable monitoring or authorize changes. |
| [3177dab](https://github.com/cursor/plugins/commit/3177dab5d4057724e6a02a198596664707795444) | Record upstream version history only. No Cursor plugin metadata is packaged. |
| [dbf4981](https://github.com/cursor/plugins/commit/dbf49813a39c1a5389c5e28cb8e4c1c2379e2454) | Port the goal-and-problem wording for in-your-own-words. |
| [c86f349](https://github.com/cursor/plugins/commit/c86f349b102feb91f1966f8a6a60882a4e601b50) | Port ketchup plain speech and its under-150-word text target. |
| [ce649c0](https://github.com/cursor/plugins/commit/ce649c03ac3b75b6ae80cbd15b7e2c536caedb5a) | Adapt per-task effort selection, fresh children, reduced full-swarm repeats, merge-result checks, gate countersigns, and single-writer stack rules. Retain Codex model families, configured budgets, heartbeat tools, bottom-only shipping, and bounded Orchestrate. Exclude speed suffixes, cloud assumptions, and the upstream orch CLI/store. |
| [8043881](https://github.com/cursor/plugins/commit/8043881e5cbb962f8948d1a1f8f8e28089d67c9a) | Route changed autopilot audit ticks through ketchup. Preserve quiet unchanged ticks and requested Codex heartbeat scheduling. |
| [79afd75](https://github.com/cursor/plugins/commit/79afd75d5bd51383fbb526b72f36db03180b8301) | Add sharpen for internal task framing followed by execution, preserving user choices and scope. |
| [1e5c90a](https://github.com/cursor/plugins/commit/1e5c90a4b6f249917bd21fe361b3a2a7deb741b8) | Record upstream version history only. No Cursor plugin metadata is packaged. |
| [afd51cf](https://github.com/cursor/plugins/commit/afd51cf66a3100a95f878d6c4b93a01f6508e3b0) | Port ketchup screenshots, videos, and small factual diagrams. Missing media does not authorize starting jobs or changing code. |
| [6ce45c5](https://github.com/cursor/plugins/commit/6ce45c59b9301a638c1fe1a7b8dc2a82b650898f) | Record upstream 0.15.25. The Codex manifest now contains 53 skills, including 24 principles. |
| [e5136d8](https://github.com/cursor/plugins/commit/e5136d82418d2db3165ea1050d17577cd618cc05) | Port reasoning-based tests, legitimate-state guards, explicit-premise testing, and retry convergence. Update correct and principle summaries together. |

The Codex shipping protocol retains bottom-only preparation, current-head checks, stable patch IDs, forge-confirmed merge state, and squash-commit reachability. Stack owners do not mutate topology. Only the root rebases or retargets the chain, and the operator owns landing unless they explicitly grant it. Upstream reductions do not broaden publication, messaging, scheduling, cleanup, or production authority.

Validation passed the 53-skill source and installed audits, 37 Python audit/installer/plan/worktree tests, 49 Bun PR watcher tests, strict typecheck, shell syntax, YAML frontmatter, Markdown links, and an installation content comparison. A read-only live GraphQL request also exercised the production review-thread reader against the previous update PR. Installation checks verify that persisted configuration and unrelated skills remain unchanged. These checks establish packaging and executable helper behavior; they do not evaluate every LLM workflow end to end.

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

The bundled watcher has focused tests and a strict TypeScript check. GitHub Actions runs these checks on pull requests and pushes to main. Structural validation and these deterministic tests prove packaging and checker behavior. They do not prove every workflow's future LLM behavior or a production application's runtime.
