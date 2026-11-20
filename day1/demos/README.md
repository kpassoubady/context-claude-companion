# Day 1 Demos — Context Engineering for Claude Code

All demos run deterministically offline with standard Python 3 (no API key required). Pair these scripts with live `/context` and `/usage` (alias `/cost`) inspection in Claude Code during delivery.

| File | Topic | Goal | Run Command |
| :--- | :--- | :--- | :--- |
| `demo-noisy-vs-focused-context.py` | Topic 1 | Compare noisy vs. focused context payloads, signal ratio, trust boundaries, and invariant checks | `python3 day1/demos/demo-noisy-vs-focused-context.py` |
| `demo-agent-loop-context-growth.py` | Topic 1 | Simulate 6 turns of an agentic loop and compare unbounded vs. path-filtered context accumulation | `python3 day1/demos/demo-agent-loop-context-growth.py` |
| `demo-context-lifecycle-inspector.py` | Topic 2 | Parse `.claude/rules/` YAML frontmatter globs and show startup vs. on-demand rule loading | `python3 day1/demos/demo-context-lifecycle-inspector.py` |
| `demo-instructions-vs-permissions-hooks.py` | Topic 2 | Contrast advisory `CLAUDE.md` prose with blocking `PreToolUse` gates and post-action `PostToolUse` checks | `python3 day1/demos/demo-instructions-vs-permissions-hooks.py` |
| `demo-compaction-and-handoff-verifier.py` | Topic 3 | Audit unfocused and focused compaction summaries and `HANDOFF.md` against actual repo and test state | `python3 day1/demos/demo-compaction-and-handoff-verifier.py` |
| `demo-subagent-isolation-vs-inline-search.py` | Topic 3 | Compare inline multi-module search with isolated subagent delegation and local search vs. external RAG | `python3 day1/demos/demo-subagent-isolation-vs-inline-search.py` |
| `demo-context-hazard-linter.py` | Topic 4 | Detect stale paths, conflicting directives, unscoped rules, and redundancy in a sample context setup | `python3 day1/demos/demo-context-hazard-linter.py` |
| `demo-context-ab-evaluator.py` | Topic 4 | Score three context variants across correctness, adherence, safety, and cost to reject false economies | `python3 day1/demos/demo-context-ab-evaluator.py` |

