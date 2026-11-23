# Lab 2.2: Context Lifecycle Inspector (Solution)

Finished, runnable reference for the Lab 2.2 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Show which instruction files load at session startup and which load on demand when a file matching a rule's `paths:` globs is accessed.

**Needs:** Python 3.10+ standard library only. No API key. Reads `day1/demos/fixtures/rules_repo/`: run the notebook from inside your clone, or in Colab where the first cells clone the repo for you.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab2_2_context_lifecycle_inspector.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab2_2_context_lifecycle_inspector.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab2_2_context_lifecycle_inspector.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab2_2_context_lifecycle_inspector/solution/lab2_2_context_lifecycle_inspector.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
Using fixtures in .../day1/demos/fixtures

['services/orders/**/*.py', 'tests/orders/**/*.py']
PASS  parse_rule finds both paths: globs in orders-service.md
PASS  parse_rule returns the body without the frontmatter
PASS  A rule with no frontmatter has no globs

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
  + CLAUDE.md (root)                       | startup                                              |  4 lines
  + .claude/rules/global-security.md       | startup (no paths: frontmatter)                      |  3 lines
  Guidance lines in the active window: 7 of 18

PASS  Startup loads only the root CLAUDE.md and the unscoped rule (7 lines)
PASS  Reading services/orders/pricing.py adds the orders rule on demand (13 lines)
PASS  The control file loads nothing extra (7 lines)

Lab complete.
```

## How to read the result

- **Startup:** 7 guidance lines, the root `CLAUDE.md` (4) plus `global-security.md` (3), which has no `paths:` frontmatter and so always loads.
- **On demand:** reading `services/orders/pricing.py` matches `orders-service.md`'s globs and adds its 6 lines (13 total).
- **Control:** reading `scripts/legacy_migration/run.py` matches nothing, so the window stays at 7 lines. Inlining everything into one `CLAUDE.md` would cost 18 lines every session.

## Takeaway

The root `CLAUDE.md` and rules without `paths:` load at startup. Rules with `paths:` load only when a matching file is accessed.
