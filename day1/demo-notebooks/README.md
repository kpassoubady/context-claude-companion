# Day 1 Demo Notebooks (Colab)

Google Colab notebook versions of the instructor demos in `../demos/`. Each notebook carries the same logic as its `.py` script, split into explained cells, and ends with a `main()` call. No API key is needed.

| Notebook | Source script | Topic |
| :--- | :--- | :--- |
| `demo-noisy-vs-focused-context.ipynb` | `demo-noisy-vs-focused-context.py` | Topic 1 |
| `demo-agent-loop-context-growth.ipynb` | `demo-agent-loop-context-growth.py` | Topic 1 |
| `demo-context-lifecycle-inspector.ipynb` | `demo-context-lifecycle-inspector.py` | Topic 2 |
| `demo-instructions-vs-permissions-hooks.ipynb` | `demo-instructions-vs-permissions-hooks.py` | Topic 2 |
| `demo-compaction-and-handoff-verifier.ipynb` | `demo-compaction-and-handoff-verifier.py` | Topic 3 |
| `demo-subagent-isolation-vs-inline-search.ipynb` | `demo-subagent-isolation-vs-inline-search.py` | Topic 3 |
| `demo-context-hazard-linter.ipynb` | `demo-context-hazard-linter.py` | Topic 4 |
| `demo-context-ab-evaluator.ipynb` | `demo-context-ab-evaluator.py` | Topic 4 |

## Fixtures

The lifecycle inspector, hooks, compaction verifier, and hazard linter read repos from `../demos/fixtures/`. Run locally from a checkout, the notebooks find them automatically. In Colab, the first cell sparse-clones only `day1/demos/fixtures` from GitHub.

## Open in Colab

Use the badge in the first cell of each notebook, or open `https://colab.research.google.com/github/kpassoubady/context-claude-companion/blob/main/day1/demo-notebooks/<notebook>.ipynb`.

## Keep in sync

The `.py` scripts remain the source of truth. When a script changes, mirror the change in its notebook. The notebooks avoid nested same-quote f-strings so they run on Colab's Python 3.10 and 3.11.
