# Context Engineering for Claude Code — Companion

Student companion repository for the **Context Engineering for Claude Code** course. Contains concept reference guides, hands-on breakout exercises (`start/` and `solution/` pairs), and executable verification scripts.

## Prerequisites & Environment Setup

Before class, complete the environment check in [context-claude-setup](https://github.com/kpassoubady/context-claude-setup) and confirm:

1. **Python 3.10+**:
   ```bash
   python3 --version
   ```
   All lab verification scripts (`verify_lab.py`) and unit suites run with the Python 3 standard library (`unittest`, `ast`, `re`, `pathlib`) with zero external package installation required (`pytest` is also supported if installed).
2. **Claude Code CLI** and **Git**:
   ```bash
   git --version
   ```

## Repository Structure

| Path | Contents |
| :--- | :--- |
| `day1/README.md` | **Start here:** every demo and lab, what it is for, and how to run it |
| `day1/concepts/` | Student concept reference guides for Sessions 1–4 |
| `day1/demos/`, `day1/demo-notebooks/` | Eight offline demos as Python scripts and as Colab notebooks |
| `day1/lab1_1_*` … `day1/lab4_2_*` | Notebook labs (1.1, 1.2, 2.2, 2.3, 3.2, 3.3, 4.1, 4.2), each with `start/` and `solution/` |
| `labs/day1/lab2_1/` | **Breakout Lab 2.1:** Structuring Project Context with `CLAUDE.md` (`start/` and `solution/`, each with its own `README.md`) |
| `labs/day1/lab3_1/` | **Breakout Lab 3.1:** Context Compaction and State Handoffs (`start/` and `solution/`, each with its own `README.md`) |
| `labs/day1/lab3_4_claude_context_commands/` | **Lab 3.4:** Claude Code Context Commands (`/context`, `/compact`, `/clear`, `/autocompact`), checked with `check_lab.sh` instead of Python (`start/` and `solution/`, each with its own `README.md`) |
| `day1/lab2_1`, `day1/lab3_1` & `day1/lab3_4` | Convenience symlinks into `labs/day1/` |

## Running Breakout Lab Checks

Each breakout exercise includes a deterministic acceptance check. Run it from the lab's `start/` folder as you work:

```bash
# Breakout Lab 2.1
cd labs/day1/lab2_1/start
python3 verify_lab.py

# Breakout Lab 3.1 (setup_repo.sh creates the local git repository the check reads)
cd labs/day1/lab3_1/start
./setup_repo.sh
python3 verify_lab.py

# Lab 3.4 (checks your written evidence)
cd labs/day1/lab3_4_claude_context_commands/start
./check_lab.sh
```

To see a finished lab pass, run the same check from `solution/`. Lab 3.1 needs a throwaway copy; see [`day1/README.md`](day1/README.md#just-want-to-see-the-results).

## Related Repositories

- [context-claude-setup](https://github.com/kpassoubady/context-claude-setup) — Pre-class setup guides and environment verification.
