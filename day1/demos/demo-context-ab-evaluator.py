"""
Demo - Context A/B/C Scorecard Evaluator
Day 1 - Session 4

Goal: Evaluate three context configurations against the same coding task using mandatory correctness, instruction adherence, and safety gates before comparing supporting token and turn efficiency metrics.

This script runs a deterministic evaluation rubric over three labeled synthetic benchmark variants (Variant A: Bloated & Conflicting Baseline, Variant B: Over-Trimmed "Token Miser", Variant C: Engineered Scoped Context) to demonstrate why token or turn reductions never excuse a failed quality or safety gate.

No API key needed. Pure Python.

Run: python3 day1/demos/demo-context-ab-evaluator.py
"""

SYNTHETIC_BENCHMARK_VARIANTS = [
    {
        "id": "Variant A (Bloated & Conflicting)",
        "evidence_type": "synthetic",
        "commit": "a91f02b",
        "tests_passed": 4,
        "tests_total": 5,
        "invariants": {
            "uses_httpx_async_client": False,
            "preserves_timeout_config": True,
            "structured_audit_log": True,
        },
        "safety_gate_passed": True,
        "context_checkpoint_tokens": 24_800,
        "turns": 6,
        "session_cost_usd": None,  # Recorded as N/A when account mode does not expose dollar billing
    },
    {
        "id": "Variant B (Over-Trimmed 'Token Miser')",
        "evidence_type": "synthetic",
        "commit": "a91f02b",
        "tests_passed": 3,
        "tests_total": 5,
        "invariants": {
            "uses_httpx_async_client": True,
            "preserves_timeout_config": False,
            "structured_audit_log": False,
        },
        "safety_gate_passed": False,  # Omitted tenant-isolation check
        "context_checkpoint_tokens": 6_200,
        "turns": 2,
        "session_cost_usd": None,
    },
    {
        "id": "Variant C (Engineered Scoped Context)",
        "evidence_type": "synthetic",
        "commit": "a91f02b",
        "tests_passed": 5,
        "tests_total": 5,
        "invariants": {
            "uses_httpx_async_client": True,
            "preserves_timeout_config": True,
            "structured_audit_log": True,
        },
        "safety_gate_passed": True,
        "context_checkpoint_tokens": 11_400,
        "turns": 3,
        "session_cost_usd": None,
    },
]


def evaluate_variant(v: dict) -> dict:
    """Apply the strict quality-first decision rule to a context evaluation record."""
    tests_ok = v["tests_passed"] == v["tests_total"]
    adherence_ok = all(v["invariants"].values())
    safety_ok = bool(v["safety_gate_passed"])
    all_primary_gates_pass = tests_ok and adherence_ok and safety_ok

    if not tests_ok:
        reason = "REJECTED (failed acceptance tests)"
    elif not safety_ok:
        reason = "REJECTED (failed mandatory safety/tenant boundary gate)"
    elif not adherence_ok:
        reason = "REJECTED (failed project instruction adherence)"
    else:
        reason = "ELIGIBLE (passes all primary gates; compare efficiency)"

    cost_display = f"${v['session_cost_usd']:.2f}" if v["session_cost_usd"] is not None else "N/A"
    adherence_ratio = f"{sum(1 for ok in v['invariants'].values() if ok)}/{len(v['invariants'])}"

    return {
        "id": v["id"],
        "evidence": v["evidence_type"],
        "tests": f"{v['tests_passed']}/{v['tests_total']}",
        "adherence": adherence_ratio,
        "safety": "PASS" if safety_ok else "FAIL",
        "context_tokens": v["context_checkpoint_tokens"],
        "turns": v["turns"],
        "cost": cost_display,
        "eligible": all_primary_gates_pass,
        "verdict": reason,
    }


def main() -> None:
    print("=== Controlled Context Evaluation Scorecard (Evidence Type: synthetic) ===")
    print(
        f"{'Variant':<36} | {'Tests':<5} | {'Rules':<5} | {'Safety':<6} | "
        f"{'/context':>9} | {'Turns':>5} | {'/cost':>5} | {'Verdict'}"
    )
    print("-" * 118)

    evaluated = [evaluate_variant(v) for v in SYNTHETIC_BENCHMARK_VARIANTS]
    for row in evaluated:
        print(
            f"{row['id']:<36} | {row['tests']:<5} | {row['adherence']:<5} | {row['safety']:<6} | "
            f"{row['context_tokens']:>9,d} | {row['turns']:>5d} | {row['cost']:>5} | {row['verdict']}"
        )

    eligible = [r for r in evaluated if r["eligible"]]
    winner = min(eligible, key=lambda r: r["context_tokens"]) if eligible else None
    print(f"\nSelected Configuration: {winner['id'] if winner else 'None'}")
    print(
        "Notice: Variant B used the fewest tokens (6,200) and turns (2) but was automatically rejected "
        "because it failed acceptance tests and safety gates."
    )
    print(
        "\nTakeaway: Always gate context changes on task correctness, instruction adherence, and safety "
        "first; compare `/context`, `/cost`, and turn counts only among passing configurations."
    )


if __name__ == "__main__":
    main()

