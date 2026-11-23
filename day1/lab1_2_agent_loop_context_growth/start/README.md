# Lab 1.2: Multi-Turn Agent Loop Context Growth (Start)

> **Short on time, or want to see the finished result first?** Run the reference notebook in [`../solution/`](../solution/README.md) instead. It needs no editing.

**Day 1, Topic 1.** Notebook version of the instructor demo [`demo-agent-loop-context-growth.py`](../../demos/demo-agent-loop-context-growth.py).

**Goal:** Measure how the output of six agent tool calls accumulates in the context window when the calls are unbounded versus scoped to source files.

## What you will be able to do

1. Measure the real lines and estimated tokens each tool call adds to the window.
2. Scope `ls`, `grep`, `cat`, `pytest`, and `git diff` commands so build output and vendored code stay out of context.
3. Explain why every turn's output stays in the window for all later turns.

## Before you start

- Python 3.10+, `pytest`, `git`, and `grep` (all present in Colab). No API key. The notebook installs `pytest>=7` in its first code cell.
- Local Jupyter: activate your Python environment first (`source venv/bin/activate` on macOS and Linux, `venv\Scripts\activate` on Windows). See the [setup guide](../../../README.md) for installation.
- Google Colab needs nothing installed.

## Open the notebook

- **Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_2_agent_loop_context_growth/start/lab1_2_agent_loop_context_growth.ipynb)
- **Local Jupyter:** from this folder run `jupyter notebook lab1_2_agent_loop_context_growth.ipynb`

## How the notebook is organized

Work top to bottom and run every cell in order. Every `# TODO` comment marks code you write. Below each TODO block, `check(...)` lines print `PASS` when your result is correct and `TODO` while a step is unfinished. Compare your output with the `# Expected:` comment in the cell.

## Step 0 - Run the setup cells

Run the install cell, the imports cell, and Section 1. The helper builds a small telemetry-ingest project in a temporary folder (`src/`, `tests/`, a compiled `dist/` bundle, and a vendored `node_modules/`), commits it with git, and makes one real edit so `git diff` has content. `run()` executes a shell command and returns everything it prints, like an agent tool call.

## Step 1 - Write the scoped command plan (Section 2)

`UNBOUNDED` is what an agent does when nothing scopes it. Replace the `BOUNDED = list(UNBOUNDED)` placeholder with six scoped `(label, command)` pairs that keep `dist/` and `node_modules/` out of the output:

- [ ] Turn 1: keep reading `CLAUDE.md` (small, and it holds the rules).
- [ ] Turn 2: list only `src` and `tests`, files only (hint: `find DIR DIR -type f`).
- [ ] Turn 3: grep only `src/ingest`, at most 5 matches per file (hint: `grep -rn -m5 PATTERN DIR`).
- [ ] Turn 4: read only the one file you will edit, `src/ingest/worker.py`.
- [ ] Turn 5: run only `tests/test_ingest.py`, quiet output (hint: `f"{PYTEST} FILE -q"`).
- [ ] Turn 6: summarize the change in `src/` only (hint: `git diff --stat PATH`).

**Expected output:** No output yet. This cell only defines the plan.

## Step 2 - Measure each turn (Section 3)

Implement `measure(root, steps)` so the totals are cumulative across turns:

- [ ] Count this turn's lines with `len(out.splitlines())` and its characters with `len(out)`.
- [ ] Add them to `total_lines` and `total_chars`.
- [ ] Append a dict to `rows` with keys `label`, `lines`, `cum_lines`, `cum_tokens` (`total_chars // 4`), and `polluted` (`polluted_lines(out)`).

**Expected output:** No output yet. Until `measure()` returns rows, the next cell prints: `measure() has not returned six rows per plan yet. Finish the TODOs above.`

## Step 3 - Compare the two plans (Section 4)

No new code. Run the comparison cell and read the table: the unbounded plan drags the 400-line `dist/` bundle into the window twice, and every later turn carries it.

**Expected output:**

```text
After turn 6: unbounded ~1,660 lines / ~31,000 tokens; bounded ~127 lines / ~700-900 tokens (about 97% smaller).
```

Exact token counts shift a little between runs because `pytest -vv` prints version-dependent header lines. The shape does not change: the unbounded plan is roughly 35x larger.

**These checks should print `PASS`:**

- measure() returned one row per turn for both plans
- The bounded plan pulled in zero build or vendor lines
- The unbounded plan pulled in hundreds of build and vendor lines
- The bounded plan ends under 5% of the unbounded token count

## Done when

Every `check(...)` line prints `PASS`, and the last cell prints `Lab complete.` and a one-line takeaway.

## Getting stuck?

Try each TODO on your own first. Then compare with the finished notebook in [`../solution/`](../solution/README.md), which also lists the complete expected output.
