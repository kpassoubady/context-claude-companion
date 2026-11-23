# Lab 4.1: Context Hazard Linter (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 4.** Notebook version of the instructor demo [`demo-context-hazard-linter.py`](../../demos/demo-context-hazard-linter.py).

**Goal:** Audit a repository's context files for stale paths, conflicting directives, unscoped rules, duplicate lines, and verbose tool output.

## What you will be able to do

1. Check every backticked path in an instruction file against the file system.
2. Detect rules that load on every session because they have no `paths:` frontmatter.
3. Detect duplicate instruction lines and oversized tool output.

## Before you start

- Python 3.10+ standard library only. No API key. Reads `day1/demos/fixtures/hazard_repo/`: run from inside your clone, or in Colab where the first cells clone the repo.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab4_1_context_hazard_linter/start/lab4_1_context_hazard_linter.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab4_1_context_hazard_linter.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the imports cell and Section 1. `hazard_repo` has a root `CLAUDE.md`, one rule file, and a captured tool log. Read both instruction files and look for problems yourself before the linter does. The conflicting-directives detector in Section 3 is provided.

## Step 1 - Stale path references (Section 2)

Implement `detect_stale_paths(files)`:

- [ ] For each `(name, text)` in `files.items()`, find backticked file paths with `re.findall(r"`([\w./-]+\.\w+)`", text)`.
- [ ] Keep a candidate only if it contains `/` and `(REPO / candidate).exists()` is `False`.
- [ ] Append `(name, candidate)` to `stale` for each candidate you keep.

**Expected output:**

```text
[('CLAUDE.md', 'docs/legacy_v1/architecture.md'), ('CLAUDE.md', 'scripts/old_deploy.sh')]
```

**These checks should print `PASS`:**

- Two stale paths found in CLAUDE.md

## Step 2 - Unscoped rules and duplicate lines (Section 4)

Implement two detectors:

- [ ] `detect_unscoped_rules(files)`: return the names that start with `.claude/rules/` **and** whose text, after `lstrip()`, does **not** start with `---`.
- [ ] `detect_duplicates(files)`: for each `(name, text)` keep a fresh set called `seen` and loop over `text.splitlines()`. Strip each line; for lines that start with a dash and a space, append `(name, line)` to `dups` when the line is already in `seen`. Add the line to `seen` after the check.

**Expected output:** No output of its own. Step 3 prints the report.

## Step 3 - Read the full report (Section 5)

No new code. Run the report cell: it runs all five checks plus a line count on the captured tool log.

**Expected output:**

```text
1. Stale path references (2 found): docs/legacy_v1/architecture.md, scripts/old_deploy.sh
2. Conflicting directives (2 found): `requests` and `unittest`
3. Rules without `paths:` frontmatter (1 found): .claude/rules/api-async.md
4. Duplicate lines (1 found): in CLAUDE.md
5. Verbose tool output: logs/last_tool_output.txt has 2,399 lines (limit 500)
```

This is a condensed view. The full report prints each finding on its own line (see `../solution/README.md`).

**These checks should print `PASS`:**

- Stale paths: 2 found
- Conflicting directives: 2 found (requests, unittest)
- Unscoped rules: .claude/rules/api-async.md
- Duplicate lines: 1 found in CLAUDE.md
- The tool log is over the 500-line limit

**Optional extension:** edit a file under `day1/demos/fixtures/hazard_repo/` (add a stale path, or give `api-async.md` a `paths:` block) and rerun the report to watch the findings change. Undo it afterwards with `git checkout -- day1/demos/fixtures/hazard_repo`, because the instructor demo uses the same fixture. Static checks do not replace human review or tests.

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
