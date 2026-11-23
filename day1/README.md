# Day 1: Context Engineering for Claude Code

Day 1 has four topics. Each topic has a concept reference, instructor demos, and one or more hands-on labs. This page lists every demo and lab, what each one is for, and how to run it.

| Topic | Theme | Concept reference |
| :--- | :--- | :--- |
| 1 | From prompt engineering to context engineering | [`concepts/01-from-prompt-engineering-to-context-engineering.md`](concepts/01-from-prompt-engineering-to-context-engineering.md) |
| 2 | How Claude Code manages context | [`concepts/02-how-claude-code-manages-context.md`](concepts/02-how-claude-code-manages-context.md) |
| 3 | Maintaining coherence across long tasks | [`concepts/03-maintaining-coherence-across-long-tasks.md`](concepts/03-maintaining-coherence-across-long-tasks.md) |
| 4 | Context quality and iteration | [`concepts/04-context-quality-and-iteration.md`](concepts/04-context-quality-and-iteration.md) |

## Before you start

- **Python 3.10+.** Standard library only; there is no install step. No API key is needed for any demo or notebook lab.
- **`git`, `grep`, and `pytest`** are used by a few items (marked below). Colab has all three.
- **Jupyter or Google Colab** for the notebook labs. Every notebook has an Open in Colab badge in its README.
- **Claude Code** for Labs 2.1, 3.1, and 3.4. These ask you to observe `/context`, `/compact`, and `/clear` in a live session. Labs 2.1 and 3.1 have offline fallbacks; Lab 3.4 needs Claude Code.
- Run the commands below **from the repository root** unless a step says otherwise.

## Two ways to use a lab

Every lab has two folders:

- **`start/`** holds the exercise: a `README.md` with step-by-step instructions, the `TODO` tasks, and the expected output at each step.
- **`solution/`** holds the finished work: a `README.md` that tells you the one command to run and exactly what you should see. Use it when you want the result without writing the code, or to check your own work afterwards.

## Demos

The eight demos are offline Python scripts you run from the repository root. Details and fixtures are in [`demos/README.md`](demos/README.md). Colab versions of each are in [`demo-notebooks/`](demo-notebooks/README.md).

| # | Demo | Topic | Goal | Run |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `demo-noisy-vs-focused-context.py` | 1 | Compare noisy and focused context payloads: signal ratio, trust boundaries, and invariant checks. | `python3 day1/demos/demo-noisy-vs-focused-context.py` |
| 2 | `demo-agent-loop-context-growth.py` | 1 | Run six real tool calls twice, unbounded and scoped, and measure the output each adds to context. *(uses `git`, `pytest`, `grep`)* | `python3 day1/demos/demo-agent-loop-context-growth.py` |
| 3 | `demo-context-lifecycle-inspector.py` | 2 | Show which `.claude/rules/` files load at startup and which load only when a matching file is read. | `python3 day1/demos/demo-context-lifecycle-inspector.py` |
| 4 | `demo-instructions-vs-permissions-hooks.py` | 2 | Run the real `PreToolUse` and `PostToolUse` hook scripts and contrast them with advisory `CLAUDE.md` prose. | `python3 day1/demos/demo-instructions-vs-permissions-hooks.py` |
| 5 | `demo-compaction-and-handoff-verifier.py` | 3 | Audit compaction summaries and a `HANDOFF.md` against `git status`, `pytest`, and `ast`. *(uses `git`, `pytest`)* | `python3 day1/demos/demo-compaction-and-handoff-verifier.py` |
| 6 | `demo-subagent-isolation-vs-inline-search.py` | 3 | Measure parent-window tokens for targeted inline search, broad inline search, and subagent delegation. *(uses `git`, `grep`)* | `python3 day1/demos/demo-subagent-isolation-vs-inline-search.py` |
| 7 | `demo-context-hazard-linter.py` | 4 | Lint a fixture repo's `CLAUDE.md` and rules for stale paths, conflicts, unscoped rules, and redundancy. | `python3 day1/demos/demo-context-hazard-linter.py` |
| 8 | `demo-context-ab-evaluator.py` | 4 | Score three context variants on correctness, adherence, safety, and cost to reject false economies. | `python3 day1/demos/demo-context-ab-evaluator.py` |

## Labs

Eight labs are Python notebooks that mirror a demo. Three are 25-minute breakout labs that work in a small project and are verified by a script.

| Lab | Topic | Format | Goal | Mirrors demo |
| :--- | :--- | :--- | :--- | :--- |
| **1.1** Noisy vs. Focused Context Payloads | 1 | Notebook | Measure signal percentage and constraint distance, flag untrusted issue text, and verify two candidate patches against project invariants. | 1 |
| **1.2** Multi-Turn Agent Loop Context Growth | 1 | Notebook | Measure the lines and tokens each tool call adds, and scope `ls`, `grep`, `cat`, `pytest`, and `git diff` so build and vendor output stays out. | 2 |
| **2.1** Structuring Project Context with `CLAUDE.md` | 2 | Breakout, script-verified | Refactor a 75-line `CLAUDE.md` to under 60 lines, scope the order rules with `paths:` frontmatter, fix an integer-cent pricing bug, and record `/context` before and after. | n/a |
| **2.2** Context Lifecycle Inspector | 2 | Notebook | Parse `paths:` frontmatter and decide which rules load at startup and which load on demand. | 3 |
| **2.3** Instructions vs. Permissions and Hooks | 2 | Notebook | Select hooks by matcher, run a hook with the JSON-on-stdin protocol, and explain why `PostToolUse` cannot undo a write. | 4 |
| **3.1** Context Compaction and State Handoffs | 3 | Breakout, script-verified | Audit a lossy compaction summary, write a verified `HANDOFF.md`, resume in a fresh session, and fix `LeaseManager.renew_lease`. | n/a |
| **3.2** Compaction and Handoff Verifier | 3 | Notebook | Collect ground truth from `git`, `pytest`, and `ast`, then audit three summaries against it. | 5 |
| **3.3** Subagent Isolation vs. Inline Search | 3 | Notebook | Measure parent-window cost of inline search versus a modeled subagent, and decide when local `grep` beats an index. | 6 |
| **3.4** Claude Code Context Commands | 3 | Breakout, live session | Use `/context`, `/compact`, `/clear`, and `/autocompact` in a real session and show that a short `HANDOFF.md` keeps what a summary loses. | n/a |
| **4.1** Context Hazard Linter | 4 | Notebook | Detect stale paths, unscoped rules, duplicate lines, and oversized tool output in instruction files. | 7 |
| **4.2** Context A/B/C Scorecard Evaluator | 4 | Notebook | Apply quality-first gates, then choose the cheapest variant only among those that pass every gate. | 8 |

### Lab folders

| Lab | Start (exercise) | Solution (finished) |
| :--- | :--- | :--- |
| 1.1 | [`lab1_1_noisy_vs_focused_context/start/`](lab1_1_noisy_vs_focused_context/start/README.md) | [`lab1_1_noisy_vs_focused_context/solution/`](lab1_1_noisy_vs_focused_context/solution/README.md) |
| 1.2 | [`lab1_2_agent_loop_context_growth/start/`](lab1_2_agent_loop_context_growth/start/README.md) | [`lab1_2_agent_loop_context_growth/solution/`](lab1_2_agent_loop_context_growth/solution/README.md) |
| 2.1 | [`../labs/day1/lab2_1/start/`](../labs/day1/lab2_1/start/README.md) | [`../labs/day1/lab2_1/solution/`](../labs/day1/lab2_1/solution/README.md) |
| 2.2 | [`lab2_2_context_lifecycle_inspector/start/`](lab2_2_context_lifecycle_inspector/start/README.md) | [`lab2_2_context_lifecycle_inspector/solution/`](lab2_2_context_lifecycle_inspector/solution/README.md) |
| 2.3 | [`lab2_3_instructions_vs_permissions_hooks/start/`](lab2_3_instructions_vs_permissions_hooks/start/README.md) | [`lab2_3_instructions_vs_permissions_hooks/solution/`](lab2_3_instructions_vs_permissions_hooks/solution/README.md) |
| 3.1 | [`../labs/day1/lab3_1/start/`](../labs/day1/lab3_1/start/README.md) | [`../labs/day1/lab3_1/solution/`](../labs/day1/lab3_1/solution/README.md) |
| 3.2 | [`lab3_2_compaction_and_handoff_verifier/start/`](lab3_2_compaction_and_handoff_verifier/start/README.md) | [`lab3_2_compaction_and_handoff_verifier/solution/`](lab3_2_compaction_and_handoff_verifier/solution/README.md) |
| 3.3 | [`lab3_3_subagent_isolation_vs_inline_search/start/`](lab3_3_subagent_isolation_vs_inline_search/start/README.md) | [`lab3_3_subagent_isolation_vs_inline_search/solution/`](lab3_3_subagent_isolation_vs_inline_search/solution/README.md) |
| 3.4 | [`../labs/day1/lab3_4_claude_context_commands/start/`](../labs/day1/lab3_4_claude_context_commands/start/README.md) | [`../labs/day1/lab3_4_claude_context_commands/solution/`](../labs/day1/lab3_4_claude_context_commands/solution/README.md) |
| 4.1 | [`lab4_1_context_hazard_linter/start/`](lab4_1_context_hazard_linter/start/README.md) | [`lab4_1_context_hazard_linter/solution/`](lab4_1_context_hazard_linter/solution/README.md) |
| 4.2 | [`lab4_2_context_ab_evaluator/start/`](lab4_2_context_ab_evaluator/start/README.md) | [`lab4_2_context_ab_evaluator/solution/`](lab4_2_context_ab_evaluator/solution/README.md) |

Labs 2.1, 3.1, and 3.4 physically live under `../labs/day1/`; `day1/lab2_1`, `day1/lab3_1`, and `day1/lab3_4` are symlinks to them.

## Just want to see the results?

Skip the exercise and run each finished solution. The expected output for every command is in that lab's `solution/README.md`.

**Notebook labs.** Needs Jupyter (`pip install notebook`). Each command runs every cell and prints the outputs, ending with `PASS` lines:

```bash
# Lab 1.1 (swap in any notebook lab's folder and file name)
cd day1/lab1_1_noisy_vs_focused_context/solution
jupyter nbconvert --to markdown --execute --stdout lab1_1_noisy_vs_focused_context.ipynb
```

Add `2>/dev/null | grep -E "^ +(PASS|TODO)  "` to print only the verdicts. Prefer a browser? Use the Open in Colab badge in the solution's README.

**Breakout labs.** From the repository root:

```bash
# Lab 2.1: expect "ALL LAB 2.1 CHECKS PASSED!"
(cd labs/day1/lab2_1/solution && python3 verify_lab.py)

# Lab 3.1: runs in a throwaway copy because setup creates a .git folder
cp -R labs/day1/lab3_1/solution /tmp/lab3_1_solution
(cd /tmp/lab3_1_solution && ./setup_repo.sh && python3 verify_lab.py)   # expect "ALL LAB 3.1 CHECKS PASSED!"

# Lab 3.4: checks the written evidence, expect "ALL LAB 3.4 CHECKS PASSED!"
(cd labs/day1/lab3_4_claude_context_commands/solution && ./check_lab.sh)
```

> **Local Jupyter and Lab 3.2:** if the ground-truth step shows `pytest failing: (none)` and two checks print `TODO`, pytest is emitting colour codes inside your Jupyter kernel. Run with `NO_COLOR=1` in front of the `jupyter` command.

## Want to do the exercise?

1. Open the lab's `start/README.md` from the table above and follow it top to bottom.
2. Complete each `TODO`, then run the check (`PASS` lines in a notebook, or `python3 verify_lab.py` / `./check_lab.sh` for a breakout lab).
3. If you are stuck, compare with `solution/` after reading the exact failure output.
