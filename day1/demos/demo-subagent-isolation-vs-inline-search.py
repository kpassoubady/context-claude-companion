"""
Demo - Subagent Isolation vs. Inline Search
Day 1 - Topic 3

Goal: Compare inline multi-module exploration in a parent session against delegating the exploration to an isolated subagent, and evaluate when local file search (`Glob`/`Grep`) vs. external RAG is appropriate.

This script runs a search across 12 simulated repository modules, measuring what enters the parent context window vs. total model token work across parent + subagent windows, while explicitly noting security boundaries.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-subagent-isolation-vs-inline-search.py
"""

REPO_MODULES = {
    f"services/mod_{i:02d}/handler.py": (
        f"# Module {i:02d}\n"
        + "\n".join([f"def helper_{i}_{j}(ctx): return ctx" for j in range(35)])
        + ("\ndef verify_idempotency_token(req): return req.headers.get('X-Idempotency-Key')\n" if i in (4, 9) else "")
    )
    for i in range(1, 13)
}

RETRIEVAL_SCENARIOS = [
    ("Find callers of `verify_idempotency_token` in current repo", "local_repo", True, "Direct `Grep` + `Read` (zero indexing lag, exact symbol match)"),
    ("Inspect uncommitted changes in `task_queue/lease.py`", "local_repo", True, "Direct `git diff` + `Read` (working tree is not in any external index)"),
    ("Search 4,000 historical postmortems across 15 teams", "external_corpus", False, "External RAG via access-controlled MCP service (semantic search + tenant ACLs)"),
]


def est_tokens(text: str) -> int:
    """Estimate tokens using a 4-chars-per-token proxy."""
    return max(1, len(text) // 4)


def run_inline_exploration(symbol: str) -> dict:
    """Read all 12 modules directly inside the parent session context."""
    parent_tokens = 0
    matched_paths = []
    for path, content in REPO_MODULES.items():
        parent_tokens += est_tokens(content)
        if symbol in content:
            matched_paths.append(path)
    return {
        "mode": "Inline Search in Parent Session",
        "parent_window_tokens": parent_tokens,
        "subagent_window_tokens": 0,
        "total_model_tokens": parent_tokens,
        "matches": matched_paths,
    }


def run_subagent_exploration(symbol: str) -> dict:
    """Run the 12-module scan in an isolated subagent and return a concise synthesis."""
    subagent_tokens = 0
    matched_paths = []
    for path, content in REPO_MODULES.items():
        subagent_tokens += est_tokens(content)
        if symbol in content:
            matched_paths.append(path)

    synthesis_report = (
        f"Subagent Finding: `{symbol}` is defined in {', '.join(matched_paths)}. "
        "Verification limit: static scan only; run pytest on those two modules to confirm runtime behavior."
    )
    returned_tokens = est_tokens(synthesis_report)
    return {
        "mode": "Isolated Subagent Delegation",
        "parent_window_tokens": returned_tokens,
        "subagent_window_tokens": subagent_tokens,
        "total_model_tokens": subagent_tokens + returned_tokens,
        "matches": matched_paths,
    }


def main() -> None:
    symbol = "verify_idempotency_token"
    inline_res = run_inline_exploration(symbol)
    sub_res = run_subagent_exploration(symbol)

    print("=== 1. Parent Context Footprint vs. Total Model Work (Illustrative Proxy) ===")
    print(f"{'Exploration Mode':<34} | {'Parent Window':>14} | {'Subagent Window':>15} | {'Total Model Work':>16}")
    print("-" * 88)
    for res in (inline_res, sub_res):
        print(
            f"{res['mode']:<34} | {res['parent_window_tokens']:>14,d} | "
            f"{res['subagent_window_tokens']:>15,d} | {res['total_model_tokens']:>16,d}"
        )

    print("\nGovernance note: Subagent context isolation keeps the parent window clean,")
    print("but subagents still consume model tokens and share the local filesystem/credentials unless sandboxed.")

    print("\n=== 2. Local File Retrieval (`Glob`/`Grep`) vs. External RAG Decision Table ===")
    for task, source_type, is_local, recommendation in RETRIEVAL_SCENARIOS:
        print(f"  * Task: {task}")
        print(f"    -> Choice: {recommendation}")

    print(
        "\nTakeaway: Use subagents to isolate heavy exploratory reads from the parent context window, "
        "and prefer direct `Glob`/`Grep` for local repository code while reserving ACL-filtered RAG "
        "for large external document corpora."
    )


if __name__ == "__main__":
    main()

