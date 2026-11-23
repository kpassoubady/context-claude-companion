# Lab 1.2: Multi-Turn Agent Loop Context Growth (Solution)

Finished, runnable reference for the Lab 1.2 notebook. Run it to see the result without doing the exercise. To do the exercise yourself, start in [`../start/`](../start/README.md).

**Goal:** Measure how the output of six agent tool calls accumulates in the context window when the calls are unbounded versus scoped to source files.

**Needs:** Python 3.10+, `pytest`, `git`, and `grep` (all present in Colab). No API key. The notebook installs `pytest>=7` in its first code cell.

## Run it

**Option 1: print the results in your terminal** (needs Jupyter, for example `pip install notebook`). From this folder:

```bash
jupyter nbconvert --to markdown --execute --stdout lab1_2_agent_loop_context_growth.ipynb
```

This runs every cell and prints each cell's code with its output. To see only the verdicts, filter for the check lines:

```bash
jupyter nbconvert --to markdown --execute --stdout lab1_2_agent_loop_context_growth.ipynb 2>/dev/null | grep -E "^ +(PASS|TODO)  "
```

**Option 2: open it.** Run `jupyter notebook lab1_2_agent_loop_context_growth.ipynb` and choose **Run > Run All Cells**, or use Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/lab1_2_agent_loop_context_growth/solution/lab1_2_agent_loop_context_growth.ipynb)

**Success looks like:** every `check(...)` line prints `PASS` and the last cell prints `Lab complete.`

## What you should see

```text
Turn | Mode      | Command                                  | +Lines | Cum lines | Cum est tokens | Build/vendor lines
----------------------------------------------------------------------------------------------------------------
1    | unbounded | cat CLAUDE.md                            |      3 |         3 |             37 |   0
1    | bounded   | cat CLAUDE.md                            |      3 |         3 |             37 |   0

2    | unbounded | ls -R (everything)                       |     28 |        31 |            116 |   2
2    | bounded   | find src tests -type f                   |      3 |         6 |             53 |   0

3    | unbounded | grep -rn process_event . (whole repo)    |    665 |       696 |         16,280 | 600
3    | bounded   | grep -rn -m5 process_event src/ingest    |      5 |        11 |            120 |   0

4    | unbounded | cat dist/ingest/worker.bundled.js        |    400 |     1,096 |         22,852 | 400
4    | bounded   | cat src/ingest/worker.py                 |    100 |       111 |            506 |   0

5    | unbounded | pytest -vv (verbose dump)                |     64 |     1,160 |         24,003 |   0
5    | bounded   | pytest tests/test_ingest.py -q           |     14 |       125 |            692 |   0

6    | unbounded | re-read worker.py and dist bundle        |    500 |     1,660 |         30,962 | 400
6    | bounded   | git diff --stat src/                     |      2 |       127 |            711 |   0

After turn 6: unbounded 1,660 lines / ~30,962 tokens; bounded 127 lines / ~711 tokens (97.7% smaller).

PASS  measure() returned one row per turn for both plans
PASS  The bounded plan pulled in zero build or vendor lines
PASS  The unbounded plan pulled in hundreds of build and vendor lines
PASS  The bounded plan ends under 5% of the unbounded token count

Lab complete.
```

Your token counts may differ slightly (pytest header lines vary by version). The pattern is what matters.

## How to read the result

- **Turn 3 is the biggest single cost:** `grep -rn process_event .` returns 665 lines (600 of them from `dist/` and `node_modules/`), about 16,000 tokens in one call. The scoped grep returns 5 lines.
- **Cost is cumulative:** the unbounded plan reads the 400-line bundle in turn 4, then re-reads it in turn 6, so it carries into every later turn.
- **The scoped plan:** `find src tests -type f`, `grep -rn -m5 ... src/ingest`, `cat src/ingest/worker.py` (the one file to edit), `pytest tests/test_ingest.py -q`, `git diff --stat src/`. Zero build or vendor lines, about 97% fewer tokens.

## Takeaway

Each turn adds its tool output to the window and keeps it there. Scoping greps to `src/`, reading only the file you will edit, and using `pytest -q` keeps build and vendor files out of every later turn.
