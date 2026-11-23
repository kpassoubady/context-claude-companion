# Context Engineering for Claude Code — Companion

Student companion repository for the **Context Engineering for Claude Code** course. Contains concept references, hands-on breakout labs, offline demo scripts, and reference resources for learning context engineering in Claude Code.

## Tech Stack

- **Language / Runtime:** Python 3.10+ (standard library only, no install step), Markdown, Shell
- **Primary tool:** Anthropic Claude Code CLI
- **Package manager:** None required (`pytest` optional)
- **Content type:** Concept references, breakout labs (`start/` and `solution/` pairs), Colab notebooks

## Project Structure

| Path | Purpose |
| :--- | :--- |
| `day1/concepts/` | Concept reference guides, Sessions 1–4 (`01` to `04`) |
| `day1/demos/` | Eight offline demo scripts (`demo-*.py`), `fixtures/` demo repos, `README.md` |
| `day1/demo-notebooks/` | Colab notebook versions of each demo, with `README.md` |
| `day1/lab1_1_*`, `lab1_2_*`, `lab2_2_*`, `lab2_3_*`, `lab3_2_*`, `lab3_3_*`, `lab4_1_*`, `lab4_2_*` | Breakout labs: `README.md`, `start/`, `solution/` notebooks |
| `day1/lab2_1`, `day1/lab3_1` (and `*_structuring_project_context`, `*_context_compaction_and_handoffs`) | Symlinks to `labs/day1/` |
| `labs/day1/lab2_1/` | Breakout Lab 2.1: structuring project context with `CLAUDE.md` (`README.md`, `start/`, `solution/`) |
| `labs/day1/lab3_1/` | Breakout Lab 3.1: context compaction and state handoffs (`README.md`, `start/`, `solution/`) |
| `labs/day1/lab3_4_claude_context_commands/` | Lab 3.4: live Claude Code context commands, no Python; checked with `./check_lab.sh` |
| `resources/` | Cheatsheet PDFs (Claude CLI, context-claude) |
| `scripts/` | Mermaid, Marp, and Excalidraw build/export helpers (see `scripts/README.md`) |
| `llm-context/` | Working folders for LLM agents: `issues/`, `done/`, `todos/`, `roadmap/`, `brainstorm/`, `info/`, `prompts/`, `learnings/`, `artifacts/` (all empty apart from `.gitkeep`) |
| `.vscode/` | Editor settings and Markdown-to-PDF stylesheet |
| `.claude/`, `.devin/` | Assistant config. Only `settings.local.json` and `config.local.json` are tracked; `docs/`, `skills/`, and `scripts/` are local symlinks, not in git |
| `.agents/`, `.github/copilot/` | Local-only (git-excluded) copies of courseware docs, skills, and scripts, symlinked to an external repo |
| `AGENTS.md`, `.github/copilot-instructions.md` | One-line pointers to this file |

## Key Commands

```bash
# Verify the Lab 2.1 solution
python3 labs/day1/lab2_1/solution/verify_lab.py

# Verify the Lab 3.1 solution
python3 labs/day1/lab3_1/solution/verify_lab.py

# Run a demo (offline, no API key; run from repo root)
python3 day1/demos/demo-noisy-vs-focused-context.py
```

## Conventions

- Each breakout lab ships as a `start/` (student) and `solution/` (reference) pair with a `README.md`.
- Demos run offline from the repo root. Only `git`, `pytest`, and `grep` are needed, and only by some demos (`day1/demos/README.md`).
- Markdown lint rules live in `.markdownlint.json` and `.markdownlintignore`.
- `scripts/README.md` describes an instructor-repo layout (`slides/…`, `book/…`) that does not exist in this repo. Verify paths before running a script.

## Related Repositories

| Repository | Purpose |
| :--- | :--- |
| [context-claude-setup](https://github.com/kpassoubady/context-claude-setup) | Pre-class setup guides and environment verification |
