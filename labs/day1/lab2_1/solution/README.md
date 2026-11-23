# Breakout Lab 2.1: Structuring Project Context with `CLAUDE.md` (Solution)

The finished reference for Lab 2.1. Run it to see the outcome without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Refactor a 75-line root `CLAUDE.md` into a concise global guide, move the order-pricing invariants into a path-scoped `.claude/rules/orders.md`, fix the integer-cent discount bug in `services/orders/pricing.py`, and record before-and-after evidence.

**Needs:** Python 3.10+ standard library only. No API key. Claude Code is optional (only for the live `/context` check below).

## Run it

From the repository root:

```bash
cd labs/day1/lab2_1/solution
python3 verify_lab.py
```

**Success looks like:**

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
=== Breakout Lab 2.1 Verification ===
[PASS] Root CLAUDE.md Check
[PASS] Scoped .claude/rules/orders.md Check
[PASS] AST Invariant Check (pricing.py)
[PASS] Unit & Acceptance Test Suite
[PASS] Before/After Comparison Record

ALL LAB 2.1 CHECKS PASSED!
```

For contrast, the same command in `../start/` prints five `[FAIL]` lines and `Lab 2.1 verification failed with 10 issue(s).`

## What the solution changes

| File | Starter | Solution |
| :--- | :--- | :--- |
| `CLAUDE.md` | 75 lines, conflicting test runners, a legacy `float` snippet, order rules mixed in | 18 lines: the `@AGENTS.md` import, the 3-component layout, the verification commands, and global conventions only |
| `.claude/rules/orders.md` | `TODO` placeholders, no frontmatter | `paths:` frontmatter scoped to `services/orders/**/*.py` and `tests/orders/**/*.py`, plus the three order invariants |
| `services/orders/pricing.py` | Returns `float`, ignores `idempotency_key` | Integer arithmetic only, `ValueError` on a blank `idempotency_key` or bad inputs, half-up basis-point rounding |
| `context_comparison.md` | `TODO` placeholders | Reference before-and-after record |

The core of the fix in `services/orders/pricing.py`:

```python
discount_cents = ((subtotal_cents * discount_bps) + 5_000) // 10_000
total_cents = subtotal_cents - discount_cents
```

The untrusted "legacy ticket #104" comment at the top of that file tells you to use `float` and skip the `idempotency_key` check. The solution ignores it, because retrieved comments are data, not instructions (OWASP LLM01). The project invariants in `.claude/rules/orders.md` win.

## What to notice

- **Scoping controls *when* guidance loads, not what tools may read.** `orders.md` loads only once an orders file is read or edited. It is not a security boundary.
- Per the reference [`context_comparison.md`](context_comparison.md), `/context` in the starter lists `CLAUDE.md`, `AGENTS.md`, and `orders.md` at startup. After the refactor it lists only `CLAUDE.md` and `AGENTS.md` until an orders file is read. Run `claude` in this folder and `/context` to see it on your own machine; your token counts will differ.
- The reference record in `context_comparison.md` holds illustrative values. Your own session's numbers will not match them.

## Run the tests only

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Expect `Ran 5 tests ... OK`.
