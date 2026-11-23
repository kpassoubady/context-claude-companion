# #inc-checkout Slack Export (trimmed)

13:31 oncall-1: Paging Payments. Error rate 18 percent on confirm.
13:33 payments-1: Gateway dashboards are green on our side. Are you timing out before we respond?
13:36 oncall-1: p95 is 4s+. Checking our pool.
13:44 oncall-1: payment-gw logs full of ERR_POOL_EXHAUSTED_7731. in_use is pinned at 40.
13:47 sre-lead: Is this the 4.18 deploy? That added retries.
13:52 oncall-1: Yes. Timeouts now retry 3x and hold the connection for the full window.
13:55 sre-lead: Roll back. Do not touch the pool size while we are burning, db limit is 150 and we run four replicas.
14:05 oncall-1: Rolling back to 4.17.2.
14:12 oncall-1: Error rate 0.4 percent. Recovered.
14:15 sre-lead: Open the review. I want a retry budget proposal, not just "remove retries".
14:30 oncall-1: Closing the incident.
