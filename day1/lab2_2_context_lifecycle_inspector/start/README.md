# Lab 2.2: Context Lifecycle Inspector (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 2.** Notebook version of the instructor demo [`demo-context-lifecycle-inspector.py`](../../demos/demo-context-lifecycle-inspector.py).

**Goal:** Show which instruction files load at session startup and which load on demand when a file matching a rule's `paths:` globs is accessed.

## What you will be able to do

1. Parse `paths:` frontmatter from a `.claude/rules/` file.
2. Decide which rules load at startup and which load only when a matching file is accessed.
3. Compare the active guidance against one monolithic `CLAUDE.md`.

## Before you start

- Python 3.10+ standard library only. No API key. Reads `day1/demos/fixtures/rules_repo/`: run the notebook from inside your clone, or in Colab where the first cells clone the repo for you.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_2_context_lifecycle_inspector/start/lab2_2_context_lifecycle_inspector.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab2_2_context_lifecycle_inspector.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the imports cell (it finds the fixture repo, or clones it in Colab), then Section 1, which prints the three rule files in `rules_repo` and one rule in full. Two rules declare `paths:` globs; one does not. The glob-matching helpers in Section 3 are provided; run them as they are.

## Step 1 - Parse a rule file (Section 2)

Implement `parse_rule(text)` so it returns `(globs, body)`:

- [ ] If there are no lines, or the first line (stripped) is not `---`, the rule has no frontmatter: `return ([], text.strip())`.
- [ ] Find `end`, the index of the next line after index 0 whose stripped text is `---` (hint: `next(i for i in range(1, len(lines)) if ...)`).
- [ ] For each line between the two `---` lines that starts with `-`, strip the dash, spaces, and quotes to get one glob, and collect it in `globs`.
- [ ] Return `(globs, body)` where `body` is the lines after the closing `---`, joined with `"\n"` and stripped.

**Expected output:**

```text
['services/orders/**/*.py', 'tests/orders/**/*.py']
```

**These checks should print `PASS`:**

- parse_rule finds both paths: globs in orders-service.md
- parse_rule returns the body without the frontmatter
- A rule with no frontmatter has no globs

## Step 2 - Resolve what loads (Section 4)

Implement `resolve(accessed, rules, root_lines)`. The root `CLAUDE.md` is already in `loaded`; for each rule:

- [ ] If the rule has no globs, append `(name, "startup (no paths: frontmatter)", n)` to `loaded` and `continue`.
- [ ] Otherwise find the first accessed file `f` where `matches(f, globs)` is true (hint: `hit = next((f for f in accessed if ...), None)`).
- [ ] If there is a `hit`, append `(name, f"on-demand (matched {hit})", n)`.

**Expected output:**

```text
Baseline: inlining every rule into one CLAUDE.md loads 18 lines at startup on every session.

=== 1. Session startup (before file reads) ===
  + CLAUDE.md (root)                       | startup                                              |  4 lines
  + .claude/rules/global-security.md       | startup (no paths: frontmatter)                      |  3 lines
  Guidance lines in the active window: 7 of 18

=== 2. Reading services/orders/pricing.py ===
  + CLAUDE.md (root)                       | startup                                              |  4 lines
  + .claude/rules/global-security.md       | startup (no paths: frontmatter)                      |  3 lines
  + .claude/rules/orders-service.md        | on-demand (matched services/orders/pricing.py)       |  6 lines
  Guidance lines in the active window: 13 of 18

=== 3. Control: reading scripts/legacy_migration/run.py ===
  (same two startup lines, nothing added)
  Guidance lines in the active window: 7 of 18
```

**These checks should print `PASS`:**

- Startup loads only the root CLAUDE.md and the unscoped rule (7 lines)
- Reading services/orders/pricing.py adds the orders rule on demand (13 lines)
- The control file loads nothing extra (7 lines)

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
