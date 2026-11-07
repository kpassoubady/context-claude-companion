# Maintaining Coherence Across Long Tasks
Reference for managing extended Claude Code workflows using compaction, durable state handoffs, isolated subagents, and external retrieval.

---

## Compaction and Its Limits

Long debugging and refactoring sessions accumulate failed hypotheses, verbose command outputs, and intermediate file diffs. Claude Code manages window capacity through automatic compaction when context limits approach and through manual compaction via `/compact`. Passing focus instructions to `/compact` guides the summarizer toward preserving specific task details.

Compaction summarizes conversation history, which makes it an inherently lossy operation. While root `CLAUDE.md` and Auto Memory reload after compaction, specific line numbers, exact error strings, or rejected fix attempts from earlier turns can drop out of the summary. Practitioners treat a compacted summary as an aid rather than a complete record, re-reading critical files and re-running tests to confirm the current state.

## Durable Handoffs and Fresh Sessions

When a task spans multiple stages or a session becomes cluttered with dead ends, writing a durable handoff file on disk and starting a fresh session with `/clear` provides explicit state control. Under the NIST AI Risk Management Framework, a handoff document functions as an auditable set of assertions with provenance rather than an unverified narrative.

```markdown
# Task Handoff: Lease Renewal Bug
- Revision: git commit a1b2c3d (dirty: task_queue/lease.py)
- Goal: Fix duplicate job execution when worker leases expire under load.
- Current State: Reproduced in tests/test_lease.py; root cause isolated to non-atomic sequence check.
- Constraints: Preserve public LeaseManager signature; no external broker dependencies.
- Failed Approaches: Global mutex lock (failed test_concurrent_lease_renewal latency check).
- Next Verification: Apply sequence token check and run pytest tests/test_lease.py -q.
```

A fresh session reads `CLAUDE.md` and the handoff artifact without inheriting thirty turns of obsolete logs. Before editing code, the resumed session verifies the handoff claims against `git status`, `git diff`, and the test suite, and ensures no credentials or untrusted prompt instructions were copied into the handoff file.

## State Continuation Strategies Compared

| Strategy | Mechanism | Best Use Case | Primary Risk to Mitigate |
| :--- | :--- | :--- | :--- |
| **Automatic compaction** | CLI summarizes history near capacity | Uninterrupted flow on moderate tasks | Unfocused summary may omit rejected approaches or exact error details |
| **Focused `/compact`** | User supplies focus directives to summarizer | Mid-session cleanup when one milestone finishes | Lossy natural-language summary still requires file and test verification |
| **Durable handoff + `/clear`** | Structured markdown file on disk plus fresh session | Multi-phase debugging or noisy investigation logs | Handoff notes can drift from uncommitted working-tree changes |
| **Isolated subagent** | Separate worker context returns a synthesis | Broad codebase search or log exploration | Context isolation is not filesystem or credential isolation; adds model usage |

## Subagents and External Retrieval

Subagents run exploratory work in a separate context window so that dozens or hundreds of intermediate `Grep` and `Read` results do not bloat the parent conversation. The subagent returns a concise synthesis of file paths and findings to the parent session. Separating context windows keeps the parent focused, though it does not reduce total model token consumption across both windows and does not sandbox the subagent from the local filesystem or credentials.

For locating information, Claude Code relies on direct file retrieval (`Glob`, `Grep`, `Read`) for code inside the repository because local search has zero indexing lag and reflects uncommitted edits immediately. Retrieval-augmented generation (RAG) over an external index is appropriate when relevant knowledge lives in a large external corpus such as architecture decision records, incident archives, or vendor specifications accessed through an MCP connector. External retrieval services must enforce tenant and document access controls before content enters model context (OWASP LLM08).
