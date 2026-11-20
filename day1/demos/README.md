# Day 1 Demos — Context Engineering for Claude Code

All demos run offline from the companion repo root (no API key required). Demos 2, 5, and 6 also call `git`, `pytest`, and `grep`; demo 4 runs the real hook scripts in `fixtures/hooks_repo/`. Fixture repos live in `fixtures/`. Pair these scripts with live `/context` and `/usage` (alias `/cost`) inspection in Claude Code during delivery.

| File | Topic | Goal | Run Command |
| :--- | :--- | :--- | :--- |
| `demo-noisy-vs-focused-context.py` | Topic 1 | Compare noisy vs. focused context payloads, signal ratio, trust boundaries, and invariant checks | `python3 day1/demos/demo-noisy-vs-focused-context.py` |
| `demo-agent-loop-context-growth.py` | Topic 1 | Run six real tool calls (`ls`, `grep`, `cat`, `pytest`, `git diff`) twice, unbounded vs. scoped, and measure the output each adds to context | `python3 day1/demos/demo-agent-loop-context-growth.py` |
| `demo-context-lifecycle-inspector.py` | Topic 2 | Read a fixture repo's `.claude/rules/` files from disk, parse `paths:` frontmatter, and show startup vs. on-demand rule loading | `python3 day1/demos/demo-context-lifecycle-inspector.py` |
| `demo-instructions-vs-permissions-hooks.py` | Topic 2 | Run the real `PreToolUse` and `PostToolUse` hook scripts from a fixture `settings.json` (exit code 2 blocks) and contrast them with advisory `CLAUDE.md` prose | `python3 day1/demos/demo-instructions-vs-permissions-hooks.py` |
| `demo-compaction-and-handoff-verifier.py` | Topic 3 | Audit unfocused and focused compaction summaries and `HANDOFF.md` against the output of `git status`, `pytest`, and `ast` on a fixture repo | `python3 day1/demos/demo-compaction-and-handoff-verifier.py` |
| `demo-subagent-isolation-vs-inline-search.py` | Topic 3 | Measure parent-window tokens for targeted inline search, broad inline exploration, and subagent delegation, then check local grep vs. an index built earlier | `python3 day1/demos/demo-subagent-isolation-vs-inline-search.py` |
| `demo-context-hazard-linter.py` | Topic 4 | Lint a fixture repo's `CLAUDE.md`, rules, and log files on disk for stale paths, conflicting directives, unscoped rules, and redundancy | `python3 day1/demos/demo-context-hazard-linter.py` |
| `demo-context-ab-evaluator.py` | Topic 4 | Score three context variants across correctness, adherence, safety, and cost to reject false economies | `python3 day1/demos/demo-context-ab-evaluator.py` |

