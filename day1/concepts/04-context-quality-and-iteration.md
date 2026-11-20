# Context Quality and Iteration
Reference for diagnosing context hazards and evaluating context changes using correctness, instruction adherence, safety, and cost metrics.

---

## Common Context Hazards

Context configurations degrade over time as repositories evolve and multiple contributors add rules. Five hazards account for most reliability and efficiency regressions in Claude Code workflows:

1. Verbose tool outputs flood the working window when test runners, build scripts, or broad file searches dump thousands of low-signal lines into the conversation history.
2. Stale assumptions persist when `CLAUDE.md` or handoff notes reference deleted directories, deprecated scripts, or superseded architecture patterns.
3. Redundant rules repeat identical instructions across root `CLAUDE.md`, `.claude/rules/`, and prompt templates, or pad files with generic advice that obscures project-specific invariants.
4. Context dilution occurs when rules for every microservice, frontend package, and migration script load unconditionally at startup regardless of the active task.
5. Conflicting instructions arise when a root guide mandates one pattern, such as synchronous HTTP calls or `unittest`, while a module rule or test suite requires another, such as `httpx.AsyncClient` or `pytest`.

Identifying which hazard is present prevents teams from blindly adding more rules when the real fix is removing a contradiction or scoping a rule file with `paths` frontmatter.

## Repeatable Evaluation Hierarchy

Context edits should be tested with the same discipline as application code changes. A controlled before-and-after comparison pins the starting git commit, task prompt, model, and tool configuration while varying only the context setup.

| Evaluation Tier | Metric Category | Concrete Evidence | Decision Rule |
| :--- | :--- | :--- | :--- |
| **1. Primary gate** | Task correctness | Unit, integration, and regression test exit status | Must pass 100% before considering efficiency |
| **2. Primary gate** | Instruction adherence | Checklist of non-inferable project invariants | Every required convention must hold in the diff |
| **3. Primary gate** | Safety and boundaries | Hostile-source and unauthorized-action checks | Zero security boundary violations (NIST SSDF, OWASP) |
| **4. Supporting measure** | Context and usage cost | `/context` snapshots, `/usage` session usage (alias `/cost`), turn count | Compare only among configurations that pass all primary gates |

## Telemetry and the False Economy Trap

Claude Code provides built-in diagnostic commands for observing resource usage. Running `/context` inspects what currently occupies the active context window across system instructions, memory files, MCP tools, and messages. Running `/usage` (alias `/cost`) reports session token usage and cost where supported by the account mode, and on subscription plans also shows plan usage limits. When a metric is unavailable in a given environment, record it as `N/A` rather than zero or a character-count estimate.

Fewer tokens or fewer turns alone never prove that a context change improved performance. Deleting safety rules from `CLAUDE.md` or instructing the agent to edit without reading caller files can cut token usage in half while introducing regressions and breaking security invariants. Teams accept a context optimization only after automated tests, instruction adherence checks, and code review confirm that quality gates pass.

