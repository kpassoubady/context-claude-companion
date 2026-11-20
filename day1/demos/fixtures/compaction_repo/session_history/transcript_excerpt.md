# Debugging transcript excerpt (ground truth for rejected approaches)

Turn 8: Tried `ttl_dedupe_cache` (expire seen keys after 60s). REJECTED: breaks late retries.
Turn 14: Tried `global_post_lock` (serialize every post_refund call). REJECTED: fails the 200 refunds/s throughput SLA.
Turn 19: Root cause confirmed. post_refund appends to postings before it checks _seen.
Turn 22: Only refunds/ledger.py was edited. refunds/webhook.py is unchanged.
