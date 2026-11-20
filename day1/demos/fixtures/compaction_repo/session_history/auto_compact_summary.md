Session summary: Investigated duplicate refund postings in the webhook handler.
Looked at refunds/webhook.py and refunds/ledger.py. Tried a cache for seen keys
and some locking. Next step: finish the fix in refunds/webhook.py and refunds/ledger.py.
