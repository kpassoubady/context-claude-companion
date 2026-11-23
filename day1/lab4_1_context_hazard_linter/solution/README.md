# Lab 4.1: Context Hazard Linter (Solution)

Finished, runnable reference for the Lab 4.1 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Audit a repository's context files for stale paths, conflicting directives, unscoped rules, duplicate lines, and verbose tool output.

**Needs:** Python 3.10+ standard library only. No API key. Reads `day1/demos/fixtures/hazard_repo/`: run from inside your clone, or in Colab where the first cells clone the repo.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab4_1_context_hazard_linter.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab4_1_context_hazard_linter.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab4_1_context_hazard_linter.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab4_1_context_hazard_linter/solution/lab4_1_context_hazard_linter.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
=== Context Hazard Audit of fixtures/hazard_repo (2 instruction files) ===

1. Stale path references (2 found):
   - CLAUDE.md: `docs/legacy_v1/architecture.md` does not exist on disk
   - CLAUDE.md: `scripts/old_deploy.sh` does not exist on disk

2. Conflicting directives (2 found):
   - `requests` is forbidden in .claude/rules/api-async.md but CLAUDE.md says: Outbound HTTP: Use synchronous `requests.Session()` for service-to-service calls.
   - `unittest` is forbidden in .claude/rules/api-async.md but CLAUDE.md says: Standard testing: Run all tests using `python -m unittest discover`.

3. Rules without `paths:` frontmatter (1 found):
   - .claude/rules/api-async.md loads on every session start

4. Duplicate lines (1 found):
   - CLAUDE.md: - Always write clean code, follow best practices, and be careful with errors.

5. Verbose tool output:
   - logs/last_tool_output.txt has 2,399 lines (over the limit; bound with `-q --tb=short` or path filters, limit 500)

PASS  Stale paths: 2 found
PASS  Conflicting directives: 2 found (requests, unittest)
PASS  Unscoped rules: .claude/rules/api-async.md
PASS  Duplicate lines: 1 found in CLAUDE.md
PASS  The tool log is over the 500-line limit

Lab complete.
```

## How to read the result

- **Stale paths:** `CLAUDE.md` points at `docs/legacy_v1/architecture.md` and `scripts/old_deploy.sh`, neither of which exists.
- **Conflicts:** `CLAUDE.md` says use `requests` and `unittest`; the rule file says both are forbidden.
- **Unscoped rule:** `api-async.md` has no `paths:` frontmatter, so it loads on every session.
- **Waste:** one bullet is repeated in `CLAUDE.md`, and the captured tool log is 2,399 lines against a 500-line limit.

## Takeaway

Static checks catch broken paths, unscoped rules, and explicit contradictions, so human review and tests can focus on whether Claude actually follows the guidance.
