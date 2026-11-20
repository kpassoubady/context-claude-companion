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
| `day1/concepts/` | Student concept reference guides for Sessions 1–4 |
| `labs/day1/lab2_1/` | **Breakout Lab 2.1:** Structuring Project Context with `CLAUDE.md` (`README.md`, `start/`, `solution/`) |
| `labs/day1/lab3_1/` | **Breakout Lab 3.1:** Context Compaction and State Handoffs (`README.md`, `start/`, `solution/`) |
| `day1/lab2_1` & `day1/lab3_1` | Convenience symlinks to `labs/day1/lab2_1` and `labs/day1/lab3_1` |

## Running Breakout Lab Checks

Each breakout exercise includes a deterministic acceptance check (`verify_lab.py`):

```bash
# Breakout Lab 2.1
cd labs/day1/lab2_1/start
python3 verify_lab.py

# Breakout Lab 3.1
cd labs/day1/lab3_1/start
python3 verify_lab.py
```

## Related Repositories

- [context-claude-setup](https://github.com/kpassoubady/context-claude-setup) — Pre-class setup guides and environment verification.
