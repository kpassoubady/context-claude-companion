# How Claude Code Manages Context
Reference for the Claude Code context lifecycle, project instruction files, path-scoped rules, on-demand retrieval, and execution controls.

---

## Startup Context and On-Demand Retrieval

Claude Code combines baseline context loaded at session start with task-specific context retrieved as work proceeds. At startup, the session loads system instructions, the project root `CLAUDE.md`, unconditional rule files, the entrypoint of Auto Memory (`MEMORY.md`), and concise metadata for available Skills and Model Context Protocol (MCP) tools. Every item loaded at startup occupies space in the context window from the first turn onward, even when prompt caching reduces billing cost.

During the session, additional information enters the window on demand. Claude Code uses `Glob` to locate file paths, `Grep` to search for symbols or patterns, and `Read` to inspect targeted file ranges. Full Skill instructions and deferred MCP tool schemas also load when a task invokes them. Inspecting `/context` during a session reveals how much capacity is used by startup instructions, tools, and conversation turns.

## Structuring Project Guidance and Scoped Rules

Root `CLAUDE.md` is the primary entry point for project-wide guidance in Claude Code. If a repository maintains shared cross-tool instructions in `AGENTS.md`, reference that file explicitly with `@AGENTS.md` inside `CLAUDE.md` and verify loading with `/context` rather than assuming bare `AGENTS.md` support. Keep root `CLAUDE.md` focused on repository structure, exact build and test commands, and global coding standards that apply to every component.

Component-specific conventions belong in `.claude/rules/*.md` files with a YAML frontmatter `paths` field. Rules without `paths` load at startup, whereas rules with `paths` load only when Claude accesses a file matching those globs.

```markdown
---
paths:
  - "services/orders/**/*.py"
  - "tests/orders/**/*.py"
---
# Orders Service Rules

- Represent monetary amounts as integer cents; do not use float.
- Require an idempotency_key on all state-changing order operations.
- Verify changes with: pytest tests/orders -q
```

Moving specialized rules into path-scoped files prevents unrelated tasks from paying the context cost of every subsystem.

## Lifecycle Mechanisms Compared

| Mechanism | When It Enters Context | Primary Role |
| :--- | :--- | :--- |
| **Root `CLAUDE.md`** | Session startup | Global build commands, architecture summary, repo-wide invariants |
| **Scoped `.claude/rules/*.md`** | On demand when matching `paths` are accessed | Subsystem conventions and component-specific verification |
| **Targeted search (`Glob`, `Grep`, `Read`)** | On demand during task execution | Just-in-time inspection of relevant source files and tests |
| **Auto Memory (`MEMORY.md`)** | Entrypoint at startup; details on demand | Persistent notes Claude records across sessions from corrections |
| **Skills and MCP tool discovery** | Descriptions at startup; full body or schema on demand | Reusable workflows and external tool integrations |

## Guidance Versus Deterministic Enforcement

Project instructions in `CLAUDE.md` and `.claude/rules/` guide model reasoning, but they do not enforce security policy or authorization. Under NIST Zero Trust and Secure Software Development Framework (SSDF) principles, model-facing prose cannot replace access control, least-privilege credentials, or protected branches.

Deterministic enforcement requires permissions and hooks configured in Claude Code settings. Permission rules (`allow`, `ask`, `deny`) and blocking `PreToolUse` hooks evaluate before a tool runs and can stop an unapproved command on covered tool paths. `PostToolUse` hooks run after a tool completes, making them suitable for automated linting or verification feedback, but they cannot prevent an action that already occurred. Practitioners pair concise `CLAUDE.md` guidance with permission rules, pre-action hooks, and CI checks to keep agent behavior both well-informed and bounded.

