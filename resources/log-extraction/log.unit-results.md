# Unit Test Results Digest

- **Source:** `log.txt` (3,803 lines, 429 KB)
- **Build:** Jenkins FAILURE / Maven BUILD FAILURE / 06:28 min
- **Context:** PR #42, build #4, branch `scratch/STRY10000002-jest-coverage-floor`
- **Change:** STRY10000002: Count untested files in Jest coverage and add a coverage floor

## Run Summary

| Runner | Script | Passed | Failed | Skipped | Notes |
|---|---|---:|---:|---:|---|
| tsc | `sample-app:build:ts` | ok | 0 | - | type check |
| Mocha | `sample-app:cov` | 660 | 0 | 0 | 3s |
| node:test (TAP) | `sample-app:cov` | 14 | 0 | 0 | |
| Jest | `sample-app:test:jest` | 3934 | 0 | 211 | suites: 251 passed, 251 total; time: 107.417 s |

## Failures

### jest (`sample-app:test:jest`)

- Jest: "global" coverage threshold for statements (86%) not met: 85.81%

### pnpm / npm errors
```text
ELIFECYCLE  Command failed with exit code 1.
```

## Coverage (Jest)

**All files:** statements 85.81%, branches 76.34%, functions 92.21%, lines 86.61%  
(371 files measured)

### Files below 80.0% on any metric (77)

| File | Stmts | Branch | Funcs | Lines | Uncovered lines |
|---|---:|---:|---:|---:|---|
| `server/agents/aws-cloudwatch-mcp/agent-scripts/aws-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/aws-cloudwatch-mcp/agent-scripts/aws-mcp-context-processing.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 23-29 |
| `server/agents/azure-monitor-mcp/agent-scripts/azure-monitor-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/azure-monitor-mcp/agent-scripts/azure-monitor-mcp-context-processing.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 23-29 |
| `server/agents/dynatrace-mcp/agent-scripts/dynatrace-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/gca-a2a/agent-scripts/gca-a2a-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 7-8 |
| `server/agents/kentik/agent-scripts/kentik-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/logicmonitor-api/agent-scripts/logicmonitor-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-4 |
| `server/agents/logicmonitor-api/agent-scripts/logicmonitor-context-processing.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 11-17 |
| `server/agents/new-relic-mcp/agent-scripts/new-relic-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-6 |
| `server/agents/prometheus/agent-scripts/prometheus-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-4 |
| `server/agents/prometheus/agent-scripts/prometheus-context-processing.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 23-29 |
| `server/agents/splunk-mcp/agent-scripts/splunk-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/thousandeyes-mcp/agent-scripts/te-mcp-applicability.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 3-5 |
| `server/agents/thousandeyes-mcp/agent-scripts/te-mcp-context-processing.ts` | 0.0 | 100.0 | 0.0 | 0.0 | 23-29 |
| `server/infra/vendors/logicmonitor/cmdb/get-recent-changes-for-ci.ts` | 4.25 | 0.0 | 0.0 | 4.44 | 42-111 |
| `server/infra/vendors/logicmonitor/cmdb/get-cmdb-service-association.ts` | 4.61 | 0.0 | 0.0 | 4.76 | 78-188 |
| `server/agents/sre-investigate/tool-scripts/find-vendors-referencing-entity.ts` | 25.44 | 20.95 | 25.97 | 25.77 | 121-139,202-204,219-357,423-460,509-515,541-784,799-819,868-1008,1074-1117,1138-1262,12... |
| `server/agents/sre-investigate/tool-scripts/utils.ts` | 38.96 | 20.22 | 47.82 | 40.19 | 94,99-104,113-124,131,140-147,159-246,266-287,389,399,451,461,471,484-487,518,529,547-5... |
| `server/infra/metadata/payload.ts` | 71.42 | 35.0 | 100.0 | 70.96 | 26,30,41-47 |
| `server/infra/vendors/azure/azure-optional-plan.ts` | 71.42 | 63.15 | 64.28 | 74.62 | 56,65,138-199 |
| `server/agents/_shared/availability.ts` | 71.42 | 64.7 | 75.0 | 72.72 | 64-66,114-137 |
| `server/infra/metadata/validate.ts` | 75.0 | 59.25 | 100.0 | 82.85 | 16,19,33,36,50,53 |
| `server/infra/charging/compile-policy.ts` | 77.77 | 66.66 | 66.66 | 77.77 | 25-30 |
| `server/infra/vendors/meraki/meraki-core-plan.ts` | 79.31 | 69.82 | 88.46 | 79.28 | 48,51,126-127,186,193-194,205-206,223-224,230-233,267-270,286,292-294,415,547-548,601-6... |
| `server/infra/vendors/meraki/meraki-wan-plan.ts` | 80.46 | 68.75 | 96.72 | 83.67 | 207-208,268-270,293-295,305-307,310-312,347-349,405-408,533-548 |
| `server/agents/sre-investigate-basic/tool-scripts/sanitize-content.ts` | 80.64 | 61.53 | 100.0 | 83.67 | 83-93 |
| `server/agents/gca-a2a/agent-scripts/gca-a2a-context-processing.ts` | 80.7 | 69.04 | 100.0 | 83.33 | 82-83,88-94 |
| `server/infra/vendors/newrelic/newrelic-nrql.ts` | 82.35 | 40.0 | 100.0 | 80.0 | 10,25,28 |
| `server/agents/_shared/vendor-availability.ts` | 82.75 | 66.66 | 100.0 | 84.61 | 167-168,202-205 |
| `server/infra/vendors/aws/aws-retry.ts` | 83.33 | 100.0 | 76.19 | 82.14 | 42-43,52-54 |
| `server/agents/sre-investigate-basic/tool-scripts/overview-summary.ts` | 83.47 | 64.58 | 92.3 | 86.73 | 97-100,104-105,166-175 |
| `server/infra/vendors/gcp/gcp-optional-plan.ts` | 84.44 | 74.07 | 95.0 | 84.09 | 60-61,76-90 |
| `server/infra/vendors/meraki/meraki-tool.ts` | 85.0 | 73.01 | 91.3 | 90.14 | 167,183,193,196,199,202,208,214,221,235-236,239-240,279 |
| `server/infra/vendors/meraki/meraki-window.ts` | 86.76 | 79.38 | 100.0 | 87.43 | 69,74,114,121-122,158-161,199,263,274,279,309,332,337,371,374-379,394 |
| `server/agents/sre-investigate-basic/tool-scripts/report-gen.ts` | 86.79 | 68.75 | 93.33 | 89.36 | 132,174-180 |
| `server/infra/metadata/store.ts` | 87.26 | 74.19 | 100.0 | 90.24 | 158,202,228,233,248,250,252,287,295,299,307,310,321,352,362,364,380-382,397,411,420,423... |
| `server/agents/sre-investigate-basic/tool-scripts/route-investigation.ts` | 88.63 | 69.56 | 60.0 | 89.47 | 95-102,126-129 |
| `server/infra/vendors/meraki/meraki-reply.ts` | 88.69 | 76.92 | 100.0 | 89.52 | 19,34,40,43,48,55,59,72,76,179-186 |
| `server/infra/vendors/newrelic/newrelic-entity.ts` | 88.88 | 73.68 | 100.0 | 100.0 | 18-24,38,43-45 |
| `server/infra/vendors/gcp/gcp-core-plan.ts` | 89.51 | 78.57 | 95.23 | 90.83 | 76-77,120,143,186-195,212-215,246-247,352 |
| `server/infra/vendors/gcp/gcp-log-trace-evidence.ts` | 90.47 | 68.29 | 83.33 | 90.47 | 139,150-154 |
| `server/infra/vendors/prometheus/prometheus-range-plan.ts` | 90.58 | 79.06 | 100.0 | 96.1 | 67-70,253 |
| `server/infra/vendors/azure/tools.ts` | 90.62 | 74.13 | 100.0 | 93.33 | 96,118,211,214 |
| `server/infra/vendors/prometheus/prometheus-plan.ts` | 90.62 | 78.57 | 100.0 | 92.43 | 104-108,174,273-274,277,321,344 |
| `server/infra/vendors/meraki/meraki-privacy.ts` | 90.68 | 77.98 | 100.0 | 94.61 | 63,79,97,556,579,581,599 |
| `server/infra/vendors/splunk/splunk-enrichment.ts` | 91.07 | 61.11 | 100.0 | 95.83 | 50-53 |
| `server/infra/vendors/gcp/gcp-core-logs.ts` | 91.66 | 76.92 | 100.0 | 91.17 | 14-16 |
| `server/agents/sre-investigate-basic/tool-scripts/routing.ts` | 91.75 | 69.76 | 92.3 | 92.94 | 177-179,231-236 |
| `server/infra/vendors/newrelic/tools.ts` | 91.78 | 63.33 | 100.0 | 91.66 | 33,41,49,56,277,390 |
| `server/infra/vendors/gcp/gcp-metric-evidence.ts` | 91.8 | 72.58 | 88.88 | 94.73 | 103,195-196 |
| `server/agents/_shared/tool-scripts/metadata-gcp-extractor.ts` | 92.3 | 60.0 | 100.0 | 100.0 | 10 |
| `server/infra/metadata/source-rows.ts` | 92.42 | 72.72 | 100.0 | 93.22 | 55,115,122,127 |
| `server/infra/vendors/api-transport.ts` | 92.68 | 62.5 | 100.0 | 94.59 | 42,54 |
| `server/infra/vendors/meraki/meraki-projectors.ts` | 93.04 | 63.38 | 96.15 | 94.34 | 164-165,313,422-460,665-668 |
| `server/infra/vendors/connections.ts` | 93.33 | 69.56 | 100.0 | 96.29 | 74-77 |
| `server/agents/sre-investigate-basic/tool-scripts/report-model.ts` | 93.47 | 67.24 | 100.0 | 100.0 | 26-32,42-45,51-54,90-91,99-103,111 |
| `server/infra/vendors/gcp/tools.ts` | 93.9 | 70.58 | 96.66 | 94.8 | 55,144-145,345 |
| `server/infra/vendors/azure/azure-cmdb.ts` | 93.9 | 74.13 | 100.0 | 97.22 | 71,139 |
| `server/infra/vendors/credential.ts` | 94.44 | 75.0 | 100.0 | 100.0 | 8 |
| `server/agents/_shared/tool-scripts/find-alert-ref.ts` | 95.0 | 62.5 | 100.0 | 100.0 | 8,26-27 |
| `server/infra/vendors/logicmonitor/probes/interface.probe.ts` | 96.0 | 66.66 | 100.0 | 100.0 | 12,44,55-59 |
| `server/infra/vendors/dynatrace/probes/entity-detail.probe.ts` | 96.0 | 79.16 | 94.73 | 97.14 | 63,136 |
| `server/infra/vendors/newrelic/newrelic-tool.ts` | 96.22 | 78.26 | 90.9 | 97.82 | 124 |
| `server/infra/vendors/azure/azure-kql.ts` | 96.42 | 79.16 | 100.0 | 100.0 | 24-25,89-92,122 |
| `server/infra/vendors/logicmonitor/probes/reachability.probe.ts` | 96.87 | 72.72 | 100.0 | 100.0 | 20,59,69-75 |
| `server/agents/sre-investigate-basic/tool-scripts/sre-status.ts` | 97.56 | 66.66 | 100.0 | 97.56 | 125 |
| `server/infra/vendors/aws/example-context.ts` | 98.18 | 75.67 | 100.0 | 98.0 | 116 |
| `server/infra/vendors/dynatrace/vulnerability-task.ts` | 100.0 | 50.0 | 100.0 | 100.0 | 11-18,45 |
| `server/infra/vendors/thousandeyes/thousandeyes-vendor.ts` | 100.0 | 57.14 | 100.0 | 100.0 | 29-32 |
| `server/infra/baseMode/mcp.ts` | 100.0 | 66.66 | 100.0 | 100.0 | 33 |
| `server/infra/baseMode/scheduler/transport.ts` | 100.0 | 66.66 | 100.0 | 100.0 | 45 |
| `server/infra/vendors/dynatrace/probes/davis-events.probe.ts` | 100.0 | 69.23 | 100.0 | 100.0 | 49-55 |
| `server/infra/vendors/resolve.ts` | 100.0 | 71.42 | 100.0 | 100.0 | 32,50-70 |
| `server/infra/metadata/result.ts` | 100.0 | 75.0 | 100.0 | 100.0 | 5 |
| `server/infra/vendors/newrelic/newrelic-connection.ts` | 100.0 | 76.92 | 100.0 | 100.0 | 32,37-38 |
| `server/infra/vendors/datadog/signals/trace-signal.ts` | 100.0 | 77.77 | 100.0 | 100.0 | 38 |

### Files with zero coverage (31)

- `server/global.d.ts`
- `server/agents/_shared/alert-timestamp.ts`
- `server/agents/dynatrace-mcp/agent-scripts/dynatrace-mcp-context-processing.ts`
- `server/agents/dynatrace-mcp/tool-scripts/execute-dql.ts`
- `server/agents/dynatrace-mcp/tool-scripts/get-entity-detail.ts`
- `server/agents/dynatrace-mcp/tool-scripts/get-problems.ts`
- `server/agents/logicmonitor-api/tool-scripts/connection-lookup.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-alert-details.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-collector-health.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-device-details.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-metric.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-process-detail.ts`
- `server/agents/logicmonitor-api/tool-scripts/get-related-entities.ts`
- `server/agents/logicmonitor-api/tool-scripts/list-alerts.ts`
- `server/agents/logicmonitor-api/tool-scripts/list-datasource-instances.ts`
- `server/agents/logicmonitor-api/tool-scripts/list-device-datasources.ts`
- `server/agents/logicmonitor-api/tool-scripts/list-devices.ts`
- `server/agents/logicmonitor-api/tool-scripts/list-sdts.ts`
- `server/agents/logicmonitor-api/tool-scripts/utils.ts`
- `server/agents/new-relic-mcp/agent-scripts/new-relic-mcp-context-processing.ts`
- `server/agents/prometheus/tool-scripts/collect-alert-metadata.ts`
- `server/agents/prometheus/tool-scripts/connection-lookup.ts`
- `server/agents/prometheus/tool-scripts/get-alerts.ts`
- `server/agents/prometheus/tool-scripts/get-rules.ts`
- `server/agents/prometheus/tool-scripts/get-targets.ts`
- `server/agents/prometheus/tool-scripts/list-metrics-for-entity.ts`
- `server/agents/prometheus/tool-scripts/query-instant.ts`
- `server/agents/prometheus/tool-scripts/query-range.ts`
- `server/agents/prometheus/tool-scripts/utils.ts`
- `server/agents/splunk-mcp/agent-scripts/splunk-mcp-context-processing.ts`
- `server/agents/sre-investigate/tool-scripts/vendor-affinity.ts`

## Passing Tests

### Mocha (`sample-app:cov`): 660 passing across 105 suites

- **create-connections plan** (10)
  - creates and links a LogicMonitor Bearer API-key connection
  - skips an attached connection and its credential with --skip-existing
  - updates and activates an inactive linked connection with --skip-existing
  - repairs a linked connection with no connection_alias and activates it
  - updates the connection and credential already linked to the alias
  - reuses the credential linked from the existing HTTP connection
  - skips linked connections for other vendors with --skip-existing
  - reuses an unlinked same-name connection when --skip-existing is set
  - ignores the noncanonical http_connection alias field
  - does not reuse a same-name connection owned by another alias
- **trigger-analyze-alert-impact background script** (9)
  - invokes the Analyze alert impact usecase once per alert
  - logs the execution plan id, state and links for each trigger
  - isolates per-alert failures and keeps processing the batch
  - serializes the full response when the runtime returns an unexpected shape
  - aborts without triggering when the batch exceeds MAX_BATCH_SIZE (KB0560516)
  - aborts in preflight when the usecase record is missing
  - no-ops when ALERT_SYS_IDS is empty
  - ships a deployment plan that inlines the script and requires credentials
  - fails fast when SN_USERNAME or SN_PASSWORD is unset
- **Fluent records — sn_aia_tool + sn_aia_agent_tool_m2m guardrails** (5)
  - every sn_aia_tool $id matches its filename sys_id
  - every sn_aia_agent_tool_m2m $id matches its filename sys_id
  - no two records share a $id across tool + m2m folders
  - every sn_aia_agent_tool_m2m record has non-empty agent and tool fields
  - discovers a non-zero number of records (smoke check)
- **DEF0933484 — Get Alarm Details script** (5)
  - flags truncation when history reaches the 50-row cap
  - does not flag truncation when the 50 rows reach back past 24 hours
  - reports an exact count when history is below the cap
  - returns alarm description, datapoints_to_alarm, treat_missing_data and unit
  - omits description fields cleanly when the alarm has none
- **DEF0933484 — AWS CloudWatch API agent instructions** (4)
  - declares the new tool fields in Step 1
  - has a metric-direction rule for balance and credit metrics
  - says "at least N" when history is truncated
  - keeps declared validation intent and forbids threshold-change advice from a zero threshold alone
- **Azure Monitor MCP Agent — scaffold guardrails** (15)
  - agent definition files exist
  - agent config runs as the shared observability agent user
  - agent record has record_type template and agent_type internal
  - version record references the agent and is published
  - connection alias has correct id
  - MCP server record references the connection alias
  - SRE Investigate child record exists and uses agent memory_scope
  - child visibility script exists
  - has 13 tool definition files
  - has 13 tool mapping files
  - every tool has a corresponding mapping
  - every mapping references a tool export
  - all MCP tool mappings use json_object type for parameters
  - context processing script delegates to compiled TypeScript
  - alert metadata tool script extracts Azure fields
- **Basic vendor flag build output** (1)
  - installs the full per-vendor boolean map
- **Datadog APM MCP Agent — instructions guardrails (DEF0933485)** (14)
  - A2 extracts the full monitor query, operator, threshold and window
  - explains permissive monitor conditions such as 100 - idle > 0
  - adds exactly one host-scoped metric call and no host guessing
  - requires load claims to quote returned values, else "not verified"
  - queries the bare metric (no arithmetic) and retries only on a syntax error
  - judges permissive monitors by a rule, not just the one example
  - accepts a host named in the request when the context has none
  - omits the scope line when no host is known
  - labels the alert-supplied service as unverified on the host
  - says higher idle values mean less load
  - KB mode only uses the alert window for steps that work from the alert time
  - uses the precomputed absolute window instead of now-30m
  - no longer claims Get Datadog Metric takes relative syntax only
  - SRE Investigate passes the host to the Datadog agent
- **Dynatrace MCP — tool mapping input schemas** (2)
  - get-events-for-kubernetes-cluster input types match the MCP input schema
  - get-dynatrace-vulnerabilities input types match the MCP input schema
- **keys.ts drift** (1)
  - is in sync with the Fluent source (no uncommitted drift)
- **New Relic MCP Agent — instructions guardrails** (3)
  - List Change Events step exists
  - history_period_hours formula rounds the elapsed hours up with ceil()
  - tells the agent the tool rejects fractional history_period_hours
- **New Relic MCP — tool schemas match the MCP server** (14)
  - list-recent-logs tool input_schema matches the MCP server
  - list-recent-logs mapping inputs match the MCP server
  - list-recent-issues tool input_schema matches the MCP server
  - list-recent-issues mapping inputs match the MCP server
  - list-gc-metrics tool input_schema matches the MCP server
  - list-gc-metrics mapping inputs match the MCP server
  - search-incidents tool input_schema matches the MCP server
  - search-incidents mapping inputs match the MCP server
  - analyze-kafka-metrics tool input_schema matches the MCP server
  - analyze-kafka-metrics mapping inputs match the MCP server
  - analyze-transactions tool input_schema matches the MCP server
  - analyze-transactions mapping inputs match the MCP server
  - list-recent-logs level filter documents lowercase values
  - list-recent-issues priorities documents uppercase values
- **New Relic MCP — instructions use the current tool parameters** (3)
  - do not reference the removed List Recent Logs params
  - tell the agent to call List Recent Logs with limit and start/end time
  - document the List Recent Issues time window and priorities
- **AIOps SRE hand-off manual charge rule** (4)
  - runs async on completed plans owned by the AIOps specialist
  - leaves channel and run type to the charge policy, not the filter
  - queues one delayed charge event for the current plan
  - does not charge in the rule
- **Observability AI Agent manual charge rule** (1)
  - queues one delayed charge event for the current plan
- **Datadog APM MCP context processing flattened.monitor_id (DEF0885201)** (7)
  - reads monitor_id from a literal "flattened.monitor_id" key
  - reads service and env from their flattened literal keys
  - reads monitor_name from flattened "monitor_name" and "monitor_title" keys
  - prefers bare keys over flattened keys when both are present
  - still resolves bare keys with no flattened form present
  - returns is_alert_flow false when no monitor_id, monitor_name, or service can be resolved
  - resolves flattened keys nested inside additional_info JSON
- **Datadog APM MCP context processing host and absolute window (DEF0933485)** (3)
  - extracts host and computes an ISO window from an ISO alert timestamp
  - treats "YYYY-MM-DD HH:mm:ss" as UTC and accepts epoch seconds
  - leaves host and window null when absent or unparseable
- **Datadog APM MCP context processing timestamp edge cases (DEF0933485)** (3)
  - returns a null window for epoch microseconds and implausible values
  - does not throw on an out-of-range numeric timestamp
  - reads a zone-less date-time as UTC whether written with T or a space
- **Datadog APM MCP context processing end to end: permissive CPU monitor alert (DEF0933485)** (3)
  - hands the agent the service, host and an absolute window around the alert
  - leaves host null when the alert has none, so the agent cannot invent one
  - the instructions use every field the script emits for this flow
- **GcaA2aUtils — buildStartInvestigationRequest** (27)
  - reports a 404 precheck error when the alert is not found
  - reports a 422 precheck error when additional_info is not valid JSON
  - reports a 422 precheck error when sn_source is not googlemonitor
  - matches sn_source case-insensitively
  - reports a 422 precheck error when sn_source is missing entirely
  - formats investigationId as "sn-" + the alert sys_id
  - uses messageId, role, and the A2A v1alpha extension metadata
  - includes the alert summary, condition, and resource in the text part
  - builds a timeRange from started_at/ended_at epoch seconds
  - falls back to "now" for endTime when ended_at is absent
  - maps a "gce_instance" resource to its GCP resource URI
  - maps a "cloud_run_revision" resource to its GCP resource URI
  - maps a "cloud_run_service" resource to its GCP resource URI
  - maps a "k8s_container" resource to its GCP resource URI
  - maps a "k8s_pod" resource to its GCP resource URI
  - maps a "k8s_node" resource to its GCP resource URI
  - maps a "cloudsql_database" resource to its GCP resource URI
  - maps a "gcs_bucket" resource to its GCP resource URI
  - maps a "gae_app" resource to its GCP resource URI
  - leaves relevantResources empty for an unrecognized resource type
  - also returns time_ranges as a top-level field alongside message_json
  - extracts ownership-relevant keys from incident.metadata.user_labels into resource_ownership_labels_json
  - extracts ownership-relevant keys from incident.policy_user_labels into policy_ownership_labels_json, kept separate from resource labels
  - ignores label keys that do not look ownership-related
  - excludes GCP/k8s structural "service_*" labels (service_namespace, service_account) as false positives
  - still matches "service" as a bare key or a trailing segment (owning_service, payments-service)
  - returns empty ownership label objects when the incident has no metadata or policy labels
- **GcaA2aUtils — buildStartInvestigationRequest (Entity Mode)** (10)
  - builds a request from entityName alone, with no precheck error
  - never queries em_alert when only entityName is given
  - includes the entity name in the text prompt and title, without alert framing
  - builds a fixed last-1-hour timeRange since there is no alert to derive one from
  - leaves relevantResources empty — a bare entity name cannot be mapped to a GCP resource URI
  - returns empty ownership labels — there is no alert to derive them from
  - builds a sanitized, unique investigationId prefixed "sn-entity-"
  - prefers alertSysId over entityName when both are somehow present
  - reports a 400 precheck error when neither alertSysId nor entityName is given
  - reports a 400 precheck error for a whitespace-only entityName instead of running Entity Mode
- **GcaA2aUtils — parseSendMessageResponse** (11)
  - passes through a precheck error using the precheck status
  - defaults the precheck status to 400 when unparseable
  - surfaces the API error message for a 4xx/5xx response
  - omits the colon-suffixed message when the error body has none
  - reports a non-JSON body error on an otherwise successful status
  - reports a non-JSON body error for a valid-JSON-but-non-object body (null)
  - reports a missing task id error, including state when present
  - extracts taskId, contextId (camelCase), and state on success
  - parses and passes through resourceOwnershipLabels/policyOwnershipLabels on success
  - carries ownership labels through even on a precheck error, since ownership is a property of the alert, not of API success
  - defaults ownership labels to empty objects when the JSON args are unparseable
- **GcaA2aUtils — buildTaskName** (3)
  - prefixes a bare task id with "tasks/"
  - leaves an already-prefixed task id unchanged
  - handles an empty/undefined task id
- **GcaA2aUtils — parseGetTaskResponse** (10)
  - surfaces the API error message for a 4xx/5xx response
  - reports a non-JSON body error
  - reports a non-JSON body error for a valid-JSON-but-non-object body (null)
  - reports TASK_STATE_WORKING as not done
  - reports TASK_STATE_SUBMITTED (the initial state on task creation) as not done
  - reports TASK_STATE_FAILED as done+failed with an error message
  - treats any other terminal state (e.g. TASK_STATE_CANCELLED) as done+failed too, not just TASK_STATE_FAILED
  - extracts investigationName, revision, and summaryText from a completed task's artifacts (wrapped {task:{...}} shape)
  - also handles an unwrapped (bare Task object) response shape
  - reports an error when completed but no investigation reference is found
- **GcaA2aUtils — buildInvestigationResourceName** (3)
  - prefers revision over investigationName and strips leading slashes
  - falls back to investigationName when revision is absent
  - reports a precheck error when neither is provided
- **GcaA2aUtils — parseInvestigationResult** (11)
  - passes through a precheck error with status 400
  - surfaces the API error message for a 4xx/5xx response
  - reports a non-JSON body error
  - reports a non-JSON body error for a valid-JSON-but-non-object body (null)
  - discards the result when the investigation carries a non-success error code
  - discards the result when the error object has a message but omits code entirely
  - does not treat an error field with code 0 as an error
  - strips observerStatuses from the returned investigation
  - trims observations to keys starting with conclusion.hypothesis or early_hypotheses_observer
  - leaves observations untouched when it is an array rather than a plain object
  - prefers executionState over state, falling back to an empty string
- **KbConversionOneExtendResourceAttributeUtil — getKbArticlesText** (10)
  - resolves a KB article by number, strips HTML tags, and collapses newlines and tabs
  - falls back to a template child table when kb_knowledge has no text
  - keys the result by KB number even when given a sys_id
  - omits an article from the result when no source table has any text for it
  - collapses embedded newlines to a single space when cleaning for prompt consumption
  - returns an empty object for an empty kb_articles input
  - picks the longest value among multiple attribute rows for the same source table
  - ignores ais_datasource_field_attribute rows for a different datasource or value
  - returns tool_disabled with empty articles without querying sources when the feature flag is disabled
  - returns tool_disabled without querying sources when the feature flag read throws
- **KbConversionOneExtendResourceAttributeUtil — getAlertFields** (5)
  - returns every non-empty field on the alert resolved by number
  - resolves the alert by sys_id when given one directly
  - returns an empty object when the alert cannot be found
  - returns tool_disabled with an empty alert without querying the alert when the feature flag is disabled
  - returns tool_disabled without querying the alert when the feature flag read throws
- **Kentik get-device-labels script parser happy path (Kentik v5 /api/v5/devices response)** (4)
  - maps every known label key into the ownership object
  - preserves every label as a "key:value" string in labels[]
  - matches device_name case-insensitively
  - does NOT leak labels from a different device in the response
- **Kentik get-device-labels script parser label-shape variants** (4)
  - accepts labels as an array of raw "key:value" strings
  - accepts labels as objects with separate key/value fields
  - falls back to device.tags when device.labels is missing
  - keeps unrecognized label keys in labels[] but not in ownership
- **Kentik get-device-labels script parser error and edge cases** (5)
  - returns found:false and API_ERROR when the REST call was non-200
  - returns found:false and PARSE_ERROR on malformed JSON
  - returns found:false when the device is not in a multi-device response
  - falls back to the sole device when a single-device response name does not match
  - returns found:true with empty ownership when the device has no labels
- **Kentik get-device-labels Fluent-source configuration** (2)
  - points the REST step at grpc.api.kentik.com
  - calls GET /api/v5/devices
- **ObservabilityResultsWriterUtils — _htmlToPlainText** (10)
  - returns empty string for null or undefined input
  - converts <br>, <br/>, <br /> (any case) to single newlines
  - converts </p> closing tags to double newlines (opening <p> is stripped by the generic tag pass)
  - converts <li> tags to "\n- " bullets and strips </li>
  - rewrites anchor tags to "text (url)" form
  - decodes &nbsp;, &amp;, &lt;, &gt;, &quot; entities
  - collapses runs of 3+ newlines to exactly two
  - trims leading and trailing whitespace
  - handles a realistic Dynatrace-style snippet end-to-end
  - flattens the full SRE investigation report skeleton (step 8 format)
- **ObservabilityResultsWriterUtils — _formatReportWithUrl** (6)
  - uses "investigation" wording when platform is Gemini Cloud Assist
  - uses "observability report" wording for non-Gemini platforms
  - uses "observability report" for all common non-Gemini platform names
  - embeds the problemURL inside an anchor with target="_blank"
  - appends the report body verbatim after the opening line
  - handles an empty report body without producing a trailing artifact
- **ObservabilityResultsWriterUtils — _writeToWorkNotes** (3)
  - wraps the response in [code]...[/code] markup
  - skips silently when em_alert.get returns false
  - passes the GlideRecord and the wrapped message to updateWorkNotesOnAlert, then calls update
- **ObservabilityResultsWriterUtils — _writeToInsightsTable** (9)
  - stores status and plain-text summary as JSON under OBSERVABILITY_FIELD on the happy path
  - _insightJson is the exact text the write stores
  - DEF0911253: a failed write falls through to the non-destructive upsert, never to bootstrap
  - DEF0911253: does not bootstrap when the write succeeds, even if a row lookup would come back empty
  - treats an unexpected return shape as a failure and still never bootstraps
  - falls back to direct setValue + update when cross-scope writer throws and an insight record exists
  - falls back to direct initialize + insert when cross-scope writer throws and no insight record exists
  - DEF0911253: sets gai_alert on the fallback insert so the new row keeps its link to em_gai
  - omits gai_alert but still inserts when no em_gai row can be resolved
- **ObservabilityResultsWriterUtils — writeToInsightsTable (public wrapper)** (1)
  - delegates to _writeToInsightsTable with the same arguments
- **ObservabilityResultsWriterUtils — _markSreCompleteIfCardExists** (10)
  - marks the SRE step complete and returns true when the em_gai card already has html_insight
  - marks the SRE step complete and returns true when only ai_insight (not html_insight) has content
  - still marks the SRE step complete (without a write) but returns false when the em_gai card has neither html_insight nor ai_insight
  - propagates status-update exceptions instead of treating existing analysis as absent
  - propagates failed status results instead of claiming completion
  - propagates lookup failures rather than allowing a replacement report
  - treats whitespace-only content as empty (still finalizes, reports no existing content)
  - treats a missing em_gai record as a soft no-op: warns, creates nothing, does not finalize
  - allows the platform to skip worker status for an existing non-worker record
  - returns success (no record created, no render event) when em_gai is missing in the no-evidence case
- **ObservabilityResultsWriterUtils — _getAlertAutonomousUtils** (2)
  - lazily constructs EmAiaAlertAutonomousUtils on first call
  - reuses the same instance on subsequent calls
- **ObservabilitySkillsExecutorUtils — _executeSkillRequest** (2)
  - returns a placeholder message when OneExtend execution throws
  - returns a placeholder message when the LLM response status is not completed
- **ObservabilitySkillsUtils — getObservabilityReport** (4)
  - returns a status object when a known alert source is handled
  - returns a no_data status object for an unsupported alert source
  - returns no_data and writes to insights when a known source is missing required fields
  - never pre-creates the insight row on the way into a supported source
- **RequestAuthCustomHeaderKentik — generateAuth** (6)
  - adds both api_key and user_name headers when both are set
  - omits the email header when user_name is nil
  - omits the token header when api_key is nil
  - adds no headers when both credential attributes are nil
  - always sets the directive to HEADER and status to SUCCESS
  - returns the request data object that was constructed
- **SizeGuard — guard()** (6)
  - returns the response unchanged when under the limit
  - returns a "too large" wrapper with a row preview when resultPath resolves to an array over the limit
  - falls back to a character preview when resultPath is missing
  - falls back to a character preview when resultPath does not resolve to an array
  - falls back to a character preview when the response is not valid JSON
  - truncates the preview to maxChars when the row preview is itself still too large
- **SizeGuard — guard() maxChars resolution priority** (6)
  - prefers the explicit maxChars option over any property
  - honors an explicit maxChars of 0 rather than falling back to a property or default
  - uses the vendor-specific property when no explicit maxChars is given
  - falls back to the global property when no vendor property is set
  - honors a global property of "0" rather than falling back to the hardcoded default
  - falls back to the hardcoded 10000 default when nothing is configured
- **SreInvestigateAlertAssistKbSearchUtil — search** (9)
  - trims each article down to number and short_description on success
  - parses a JSON string payload before trimming articles
  - returns no_data when the wrapper returns null
  - returns no_data when the wrapper returns an empty array
  - returns error when the wrapper result carries an error field
  - returns error when the JSON string payload cannot be parsed
  - returns error when EmGaiWrapper throws
  - returns tool_disabled without calling EmGaiWrapper when the feature flag is disabled
  - returns tool_disabled without calling EmGaiWrapper when the feature flag read throws
- **SRE Investigate direct manual charge rule** (3)
  - runs only on completed direct SRE execution plans
  - uses the compiled direct policy and charges the current plan once
  - leaks no agent sys_id, feature name, or feature mapping into the rule
- **SREPreEngagementEval — evaluate()** (4)
  - AC2: returns object with overall in {PASS,WARN,FAIL} and a checks array
  - AC3: checks array has at least one entry
  - AC2: generated_at reflects the value returned by GlideDateTime().getValue()
  - AC2: evaluate() applies a default lookbackDays of 30 when not supplied
- **SREPreEngagementEval — parseRequestParams()** (12)
  - lookback_days unset → defaults to 30
  - AC1: lookback_days=0 clamps to 1, does not fall back to default 30
  - lookback_days=400 clamps to 365 (upper bound)
  - lookback_days=abc (non-numeric) → NaN handling defaults to 30
  - lookback_days=7 (normal value) passes through unchanged
  - vendors unset → vendorFilter is undefined
  - AC2: vendors as a plain string "Dynatrace" → single-element filter, no throw
  - vendors="Dynatrace,Splunk" as a plain string (not the platform-observed shape) → splits into 2 elements
  - FIXED (DEF0867872): vendors=["Dynatrace,Splunk"] (platform-observed shape for a comma-embedded single param) → splits into 2 elements
  - vendors as a genuine array ["Dynatrace","Splunk"] → filter passes through unchanged
  - DEF0867872: vendors array with a comma-containing element ["Vendor, Inc.","Splunk"] → the element is split on comma
  - AC4: vendors with more than 20 entries is capped at 20
- **SREPreEngagementEval — toJson()** (2)
  - AC4: output parses cleanly via JSON.parse and preserves overall + checks
  - AC4: toJson round-trips all check fields (name, status, detail)
- **SREPreEngagementEval — toHtml()** (3)
  - AC5: output contains a <table> element
  - AC5: output contains one <tr> per check plus one header row
  - AC5: each check name and status appears in the HTML output
- **SREPreEngagementEval — _escHtml()** (3)
  - escapes &, <, >, ", and ' characters
  - returns empty string for null or undefined
  - toHtml escapes special characters in check fields
- **SREPreEngagementEval — _countByQuery()** (4)
  - returns the COUNT value when rows exist
  - returns 0 when next() is false (no rows match)
  - calls addEncodedQuery when a query string is provided
  - does not call addEncodedQuery when query is null
- **SREPreEngagementEval — _checkEmSources()** (8)
  - AC1: plugin inactive → single FAIL result for em_plugin_active, no source discovery
  - AC4: result always contains em_plugin_active check
  - AC4: em_source_discovery present only when plugin is active
  - AC2: plugin active + events exist → em_source_discovery PASS with source count and names
  - AC3: plugin active + zero sources → em_source_discovery WARN
  - AC6: lookbackDays defaults to 30 when config.lookbackDays is undefined
  - AC6: lookbackDays appears in detail string when sources found
  - AC5: source names in detail reflect what GlideAggregate returns
- **SREPreEngagementEval — _checkAlertVolume()** (10)
  - AC2: each active em_event source produces exactly one alert_volume.<source> entry
  - AC3: eligible count >= threshold → PASS with total and eligible in detail
  - AC3: 0 < eligible < threshold → WARN with both counts and threshold in detail
  - AC6: total > 0 but eligible = 0 → WARN noting filters exclude all
  - AC5: source in em_event but zero alerts in em_alert → FAIL
  - AC3: total count = 0 → FAIL (not WARN)
  - AC7: detail always includes both total and eligible counts when total > 0
  - AC4: lookbackDays defaults to 30 when not provided
  - AC1: reads threshold from sn_obs_aia.pre_eval.alert_volume_threshold property
  - malformed property value falls back to default threshold of 100
- **SREPreEngagementEval — _checkAliasStatus()** (8)
  - AC2: missing alias → FAIL with alias name in detail
  - AC4: connection alias with populated http_connection → PASS
  - AC3: connection alias present but no populated http_connection → WARN with state in detail
  - AC4: AWS-API credential alias with linked credential → PASS
  - AC6: each vendor produces exactly one alias check entry
  - the 3 newly-added vendors (Azure Monitor, LogicMonitor, Gemini Cloud Assist A2A) resolve to their exact alias names
  - AC5: vendorFilter limits which aliases are checked (case-insensitive substring)
  - AC1: check name format is alias_status.<alias_display_name>
- **SREPreEngagementEval — _checkPlatformStats()** (11)
  - AC1: result contains check entries for all four plugin IDs plus platform_version
  - AC6: pre-Yokohama release → platform_version status = FAIL
  - AC7: Zurich below patch 9 → platform_version FAIL with patch in detail
  - AC8: Zurich patch 9+ → platform_version PASS
  - AC7: Australia below patch 3 → platform_version FAIL
  - AC8: Australia patch 3+ → platform_version PASS
  - Yokohama any patch → platform_version PASS (no minimum patch)
  - AC5: platform_version detail contains the full buildtag string
  - AC2: com.example.sn_aia inactive → plugin check status = FAIL
  - AC3: com.example.sample.snac inactive → plugin check status = FAIL
  - AC4: com.example.service_mapping or com.example.discovery inactive → WARN (not FAIL)
- **SREPreEngagementEval — _deriveOverall()** (4)
  - AC6: any FAIL in checks produces FAIL (worst-status wins)
  - AC6: WARN without FAIL produces WARN
  - AC6: all PASS produces PASS
  - AC6: empty checks array produces PASS
- **SREVendorCapabilityEval — _discoverSubAgents() discovery is dynamic (AC1)** (1)
  - returnsEveryLeafInTheFixtureHierarchyNotAFixedTen
- **SREVendorCapabilityEval — result contract (AC2)** (2)
  - everyResultHasNameSysIdAndBooleanEnabled
  - enabledReflectsAgentConfigActiveAndDefaultsFalseWhenNoConfig
- **SREVendorCapabilityEval — evaluate() (AC3)** (2)
  - zeroVendorsProducesOverallFailAndDelegationDetail
  - nonZeroVendorsProducesPassWithPopulatedVendorRows
- **SREVendorCapabilityEval — intermediate exclusion is structural (AC4)** (1)
  - intermediateAgentsAreExcludedByStructureNotByName
- **SREVendorCapabilityEval — deterministic order (AC5)** (1)
  - resultIsSortedByNameAscendingAndIsStableAcrossRuns
- **SREVendorCapabilityEval — robustness** (3)
  - cyclicHierarchyTerminatesAndDoesNotDuplicate
  - hierarchyDeeperThanTheCapIsTruncatedWithAWarning
  - alwaysReturnsAnArrayNeverNull
- **SREVendorCapabilityEval — toJson()** (1)
  - toJsonRoundTripsTheMatrix
- **_mapSourcesToAgents** (13)
  - AC1: each distinct source produces exactly one mapping result, no fan-out
  - AC2: all 9 keyword rows match case-insensitively, PASS with the correct sub_agent name
  - AC2 (aws cardinality, OQ-1): "aws" keyword maps to BOTH CloudWatch agents as an array, not a joined string
  - AC3: an unmatched source returns WARN, sub_agent null, and a non-empty explanatory detail
  - AC4: Dynatrace/New Relic/AWS/Datadog/Prometheus/ThousandEyes all map to PASS on one fixture
  - all 9 keyword rows (10 target agent names, aws counted once) map correctly together in one fixture
  - AC5: unmatched sources (Azure Monitor, GCP, Grafana) appear as WARN, not omitted, alongside matched ones
  - Robustness: zero-source fixture returns [] — never null or undefined
  - Robustness: blank/null source group values are filtered out, not turned into a row
  - OQ-2 (agents[] cross-check): a keyword match downgrades to WARN when the sub-agent was not discovered
  - OQ-2 (agents[] cross-check): a keyword match downgrades to WARN when the sub-agent is discovered but disabled
  - OQ-2 (agents[] cross-check): the aws row downgrades to WARN if only one of the two CloudWatch agents is available
  - OQ-3 (plugin guard): Event Management plugin inactive returns a single sentinel row, not per-source results
- **_checkAliasPerVendor** (7)
  - zero-agents input returns [] — never null or undefined
  - an unmapped vendor (no ALIASES entry) produces a FAIL with the "no expected alias defined" detail, aliasId null
  - AWS CloudWatch API Agent (credential-type) with no linked credential produces FAIL, not WARN (mirrors Story 5)
  - mapped connection-type vendor with a populated http_connection produces PASS, carrying the aliasId forward
  - mapped connection-type vendor with no populated http_connection produces WARN, detail includes the alias state
  - alias not found in sys_alias produces FAIL, aliasId null
  - the 3 newly-mapped vendors (Azure Monitor, LogicMonitor, Gemini Cloud Assist A2A) resolve to their exact alias names
- **_buildAuthHeaders (per-vendor auth header schemes)** (20)
  - New Relic MCP Server Agent uses a single API-Key header
  - Datadog APM MCP Server Agent uses dual DD-API-KEY + DD-APPLICATION-KEY headers
  - Dynatrace MCP Server Agent sends the raw api_key value as-is under Authorization (not re-wrapped)
  - Prometheus API Agent uses a Basic-encoded Authorization header built from user_name/password
  - SolarWinds analysis AI Agent uses a Basic-encoded Authorization header built from user_name/password
  - Splunk MCP Server Agent uses the custom header name from credential.header when set
  - Splunk MCP Server Agent defaults the header name to Authorization when credential.header is unset
  - ThousandEyes MCP Server Agent uses the custom header name from credential.header, api_key sent as-is
  - Kentik analysis AI agent uses a custom header plus conditional X-CH-Auth-Email when user_name is present
  - Kentik analysis AI agent omits X-CH-Auth-Email when user_name is absent
  - an unknown vendor produces an empty header map (default switch branch)
  - no credential resolvable for the given credId produces an empty header map
  - New Relic MCP Server Agent with a missing api_key attribute produces an empty header map
  - Datadog APM MCP Server Agent with either attribute missing produces an empty header map, not a partial one
  - Dynatrace MCP Server Agent with a missing api_key attribute produces an empty header map
  - Prometheus API Agent with either user_name or password missing produces an empty header map, not a "null:..." Basic token
  - SolarWinds analysis AI Agent with either user_name or password missing produces an empty header map, not a "null:..." Basic token
  - Splunk MCP Server Agent with a missing api_key attribute produces an empty header map
  - ThousandEyes MCP Server Agent with a missing api_key attribute produces an empty header map
  - Kentik analysis AI agent with a missing api_key attribute produces an empty header map
- **_classifyConnectivity (outcome classification)** (7)
  - 2xx/3xx with no error classifies as PASS, with the status code in detail
  - 2xx/3xx with haveError=true classifies as WARN, not PASS or FAIL
  - HTTP 401 classifies as FAIL with the error message text in detail
  - HTTP 403 classifies as FAIL with the error message text in detail
  - HTTP 500+ classifies as WARN, not FAIL
  - a missing/falsy status code classifies as WARN
  - another 4xx code (404) classifies as FAIL (documented accepted gap, not WARN)
- **_testConnectivity** (17)
  - empty/undefined aliasChecks returns [] without crashing
  - AWS CloudWatch API Agent always SKIPs with credential_only, regardless of check.status
  - AWS CloudWatch MCP Server Agent always SKIPs with unsupported_auth_scheme, regardless of check.status
  - a vendor whose upstream alias check is WARN SKIPs with alias_not_ready
  - a vendor whose upstream alias check is FAIL SKIPs with alias_not_ready
  - a PASSed alias with no populated http_connection SKIPs with connection_not_populated
  - use_mid=true with no mid_server configured produces WARN
  - use_mid=true, mid_server set, but no validated/running ecc_agent produces WARN
  - use_mid=true with a valid ecc_agent proceeds to the REST call with setMIDServer invoked
  - a successful REST call (2xx, no error) classifies as PASS with the status code in detail
  - HTTP 401 classifies as FAIL with the error message in detail
  - HTTP 403 classifies as FAIL with the error message in detail
  - HTTP 500+ classifies as WARN
  - a missing status code classifies as WARN
  - another 4xx (404) classifies as FAIL (documented accepted gap)
  - execute() throwing (timeout/transport failure) classifies as WARN, never FAIL
  - AC6: a mixed multi-vendor input yields exactly one output per input, in order, none omitted
- **_buildMatrix** (10)
  - AC1: producesExactlyOneRowPerDiscoveredVendor
  - AC2: everyRowHasAllFiveDocumentedColumnsAsBooleans
  - AC3: readyIsTrueOnlyWhenAllApplicableChecksPass
  - AC3 (credential-only exception): awsApiCredentialOnlySkipDoesNotBlockReadyWhenAliasPasses
  - AC3 (absence-SKIP blocks): absenceSkipOnAConnectionVendorBlocksReady
  - Flagged decision #2: unsupportedAuthSchemeSkipBlocksReadyByDefault
  - AC6: anyNonPassNonByDesignCheckForcesReadyFalse
  - sourceConfiguredTrueOnlyWhenAMatchingSourceRowIsPass
  - vendorWithNoMatchingSourcesRowIsSourceConfiguredFalse
  - alwaysReturnsAnArrayNeverNullOrUndefinedOnEmptyInputs
- **toJson (VendorRow[])** (1)
  - AC4: toJsonProducesValidJsonWithAllVendorEntries
- **toHtml (VendorRow[])** (5)
  - AC5: toHtmlContainsATableWithTheSixDocumentedHeaders
  - AC5: toHtmlEmitsExactlyOneRowPerVendor
  - toHtmlRendersNaForCredentialOnlySkipAndDashForAbsenceSkip
  - toHtmlEscapesVendorNamesContainingHtmlSpecialCharacters
  - toHtmlOnEmptyMatrixStillRendersAWellFormedEmptyTable
- **evaluate (wired)** (3)
  - evaluateReturnsEmptyVendorsAndFailCheckWhenNoAgentsDiscovered
  - evaluateCallsFullChainAndReturnsBuildMatrixOutput
  - evaluateDefaultsLookbackDaysTo30WhenOmitted
- **Shared alert-timestamp parser (DEF0892251)** (9)
  - parses ISO-8601 with Z
  - applies numeric UTC offsets in +HH:MM, +HHMM and +HH forms
  - rolls the date correctly when an offset crosses midnight
  - parses example "yyyy-MM-dd HH:mm:ss" as UTC
  - handles fractional seconds of 1, 3 and 9 digits
  - rejects out-of-range and rolled-over components
  - rejects out-of-range offsets
  - returns null for empty, whitespace and non-timestamp input
  - trims surrounding whitespace
- **Basic mode finding output without importance levels** (2)
  - omits the level and evidence citation from report findings
  - omits the level and evidence citation from the overview summary
- **Basic to V1 child visibility script** (3)
  - is visible only when the compiled flag reader returns true
  - hides V1 when the compiled flag reader cannot be loaded
  - hides V1 when the flag read throws
- **Basic to V1 delegation boundary** (2)
  - reads the flag only in the flag reader and its property record
  - links the only Basic child to the agent named by Route
- **Datadog APM MCP Agent — context-processing monitor_id extraction (DEF0889090)** (4)
  - extracts monitor_id from additional_info.alert_id, matching real Datadog em_alert payloads
  - extracts monitor_id from the Event Management flattened.alert_id key
  - prefers monitor_id over alert_id when both are present
  - leaves monitor_id null and is_alert_flow false when no identifying context is present
- **Dynatrace MCP Agent — context-processing alert_timestamp extraction (DEF0892251)** (13)
  - extracts alert_timestamp from triggerContext.sys_created_on
  - extracts alert_timestamp from additional_info JSON opened_at
  - passes through example-format sys_created_on without rewriting
  - extracts alert_timestamp from nested em_alert.sys_created_on
  - extracts alert_timestamp from flattened.timestamp
  - extracts alert_timestamp from a literal "flattened.timestamp" key
  - leaves alert_timestamp null when context is empty
  - does not throw when context is null
  - emits an absolute [alert-24h, alert+15m] entity window in UTC
  - normalizes a UTC-offset alert timestamp when building the entity window
  - leaves the entity window null when the timestamp is unparseable or absent
  - prefers alert-specific sys_created_on over an unrelated top-level timestamp
  - does not take the alert timestamp from pageContext
- **executeDql — execute-dql orchestration** (6)
  - calls execute-dql with the query and passes the raw tool_response through SizeGuard
  - coerces a truthy includeTypes into a boolean before calling the executor
  - returns a serializable error payload when dqlQueryString is empty
  - returns a serializable error payload when the executor reports is_error
  - returns a serializable error payload when the parsed MCP response reports isError
  - passes a non-JSON tool_response through to SizeGuard instead of throwing a parse error
- **getEntityDetail — describe+fetch orchestration** (31)
  - returns the fetched record when describe + fetch both succeed
  - caps fields at 100 and emits gs.warn when describe returns more than 100
  - returns a serializable error payload when describe returns an empty records array
  - returns a serializable error payload when fetch returns an empty records array
  - returns a serializable error payload when the executor returns is_error: true
  - returns a serializable error payload when the tool_response envelope has isError: true
  - returns a serializable error payload when inputs.entityId is missing or blank
  - returns a serializable error payload when the entityId contains no dash
  - projects by default, skipping only expansion relationships and bulk fields
  - adds arraySize blast-radius counts only for expansion relationships present on the type
  - projects fields whose data_types are absent, preserving pre-classification behavior
  - omits fields over the 1 KB ceiling and reports them on _omittedLargeFields
  - enforces a total record budget when many fields individually fit
  - stays within budget when no field is left to drop to pay for the omission list
  - stays within budget when droppable fields are smaller than their own omission note
  - leaves a record untouched when every field is under the ceiling
  - parses PROCESS_GROUP_INSTANCE-XXX to dt.entity.process_group_instance
  - defaults the fetch lookback to 24h when history is not provided
  - uses the caller-provided history for the fetch lookback
  - falls back to the 24h default and warns when history is not a valid Grail duration
  - anchors the fetch window to an ISO-8601 alertTimestamp instead of now()
  - parses example-format alertTimestamp as UTC and subtracts history
  - accepts ISO-8601 alertTimestamp with more than 3 fractional-second digits
  - accepts ISO-8601 alertTimestamp with fewer than 3 fractional-second digits
  - normalizes UTC offset +00:00 alertTimestamp to UTC
  - normalizes UTC offset +02:00 alertTimestamp to UTC
  - normalizes UTC offset -05:30 alertTimestamp to UTC
  - normalizes UTC offset +0200 (no colon) alertTimestamp to UTC
  - rejects an out-of-range UTC offset and a rolled-over date, surfacing window_note
  - falls back to from:now()-history and warns when alertTimestamp is invalid
  - preserves from:now()-history when alertTimestamp is omitted
- **getProblems** (6)
  - sanitizes inputs and routes problem IDs to get-problem-by-id
  - routes missing problem IDs to query-problems with the default status
  - resolves and sanitizes wrapped JSON inputs
  - treats a non-JSON wrapped string as a problem ID
  - preserves top-level history with wrapped object inputs
  - returns a serializable error payload when the MCP executor returns an error
- **findVendorsReferencingEntity — mock scenario override** (7)
  - uses a valid active scenario instead of MOCKED_SUMMARIES
  - ignores invalid summaries within an otherwise valid scenario
  - falls back to the hardcoded fixtures when no active scenario property
  - falls back to the hardcoded fixtures when active slug without a scenario property
  - falls back to the hardcoded fixtures when scenario property is invalid JSON
  - falls back to the hardcoded fixtures when scenario has zero valid summaries
  - never queries sys_properties for a non-mock entity
- **Find Vendors source unavailable reason** (3)
  - returns the reason when the source vendor is unavailable
  - omits the reason when the source vendor is configured
  - omits the reason when the entity name is empty
- **getAlertImpactSummary (compiled tool script)** (1)
  - reports not_found instead of throwing when the alert has no AI insight row
- **Get Alert Metadata source unavailable reason** (8)
  - keeps source and reason when additional_info is ""
  - keeps source and reason when additional_info is "{bad"
  - adds the unavailable reason for a named source vendor
  - does not add a reason to Group Alert without an effective source
  - omits a reason when its lookup returns null
  - leaves a successful Prometheus report unchanged
  - attributes grouped-alert reasons to the matching vendor
  - returns an unavailable-source reason through the tool entry point
- **SourceTenantCheckUtil** (3)
  - requires the compiled module from the expected dist path and delegates to it
  - returns an empty string and warns when require() throws (e.g. unsupported in this execution context)
  - returns an empty string and warns when the underlying module throws
- **LogicMonitor event evidence — DEF0933486** (27)
  - binds the 02:17Z occurrence (314, one minute) from the LM Start text, not the later 428
  - accepts a requested time inside the occurrence as Unix seconds
  - does not bind a nearby re-fire for a Unix time inside an earlier occurrence
  - returns occurrence_unresolved without event data for no matching occurrence
  - returns occurrence_unresolved without event data for two occurrences equally close to the time
  - returns occurrence_unresolved without event data for a capped candidate page
  - picks the closest start when escalations start 60 s apart (Alert0011354 rerun)
  - does not establish uniqueness when the candidate total is unknown
  - falls back to the latest occurrence for times it cannot parse, such as non-US zones
  - binds each requested firing of a fast-flapping pod alert (Alert0011354, Alert0011349)
  - keeps the legacy latest lookup, labelled latest_unbound, when no time is given
  - reports a re-fire as flapping without replacing the selected occurrence or its device
  - names open replicaSQLRunning, replicaIORunning and ping alerts on the device
  - keeps a later re-fire on another datapoint out of the event but blocks an all-clear
  - rejects event mode without the selected portal id so the alert cannot count itself
  - establishes scoped absence only from complete event and current queries
  - reports not_established for unknown total
  - reports not_established for truncated result
  - reports not_established for missing items
  - reports not_established for a full page even with a matching total
  - lists at most 20 alerts each but reports full totals
  - keeps positive findings when one query fails and is unavailable when both fail
  - covers a three-hour event in full and marks longer events partial
  - leaves generic filter mode unchanged
  - finds historical peer LMD16942400 in the namespace group of a now-healthy pod
  - reports a deleted device as 404 and flags it in Get Alert Details
  - keeps trigger 99.6133 separate from the sampled peak and its window
- **new-relic-mcp-context-processing — extractNewRelicAlertContext (DEF0885199)** (3)
  - resolves a UUID issue_id from pageContext.additional_info flattened.issue_id, ahead of the non-UUID flattened.incident_id
  - resolves alert flow from a UUID-shaped flattened.incident_id when no issue_id is present
  - prefers a later, UUID-shaped incident_id over an earlier non-UUID flattened.issue_id
- **newRelicVendor.identifiers — issue_id resolution (DEF0885199)** (2)
  - prefers flattened.issue_id (UUID) over the non-UUID flattened.incident_id
  - prefers a later, UUID-shaped incident_id over an earlier non-UUID flattened.issue_id
- **sanitizeInputs** (1)
  - strips one pair of surrounding quotes from top-level string inputs
- **SRE Investigate failure-handling instructions** (9)
  - preserves the failure gate, reason tables, and save rules
  - keeps partial findings and independent vendor calls after a failure
  - keeps hidden-source and optional-tool reasons in the report
  - keeps no-evidence reports short and limited to attempted checks
  - sets noEvidence only for the non-gate No-Evidence report
  - allows needs_input questions only in interactive conversations
  - records needs_input gaps without questions in background runs
  - preserves invocation, source mapping, and Unknown wording rules
  - matches approved routing, synthesis, persistence, and delivery sections
- **SRE Investigate — save tool input contracts** (4)
  - tools/sre-investigate-save-analysis.now.ts exposes valid JSON with the expected required and optional inputs
  - tool-mappings/sre-investigate-save-analysis-mapping.now.ts exposes valid JSON with the expected required and optional inputs
  - tools/sre-investigate-save-gai-insight.now.ts exposes valid JSON with the expected required and optional inputs
  - tool-mappings/sre-investigate-save-gai-insight-mapping.now.ts exposes valid JSON with the expected required and optional inputs
- **SRE Investigate — Save Analysis tool** (6)
  - returns an error object when writing work notes fails
  - returns success when insights write fails but work notes succeed
  - writes only work notes when noEvidence is true
  - does not claim insights were saved when no-evidence work notes fail
  - writes both destinations when noEvidence is undefined
  - writes both destinations when noEvidence is false
- **SRE Investigate — Save GAI Insight tool: no-evidence leaves the Overview card untouched** (4)
  - preserves the existing card and skips rendering when the card already has content
  - leaves the card untouched and does not backfill or render when the existing card is empty
  - ignores an unusable summarization payload when noEvidence is true, since the card is never written
  - renders normally (unaffected by the no-evidence path) when noEvidence is not set
- **SRE Investigate — Save GAI Insight failure boundaries** (8)
  - returns an error without writing if the preservation check fails
  - warns and skips the render event but still succeeds when persistence returns no record id
  - rejects unusable summarization on the normal render path: not json
  - rejects unusable summarization on the normal render path: null
  - rejects unusable summarization on the normal render path: []
  - rejects unusable summarization on the normal render path: {}
  - rejects unusable summarization on the normal render path: {"alert_overview":"No vendor or SO dashboard data was available for this alert.","what_is_affected"...
  - uses the original render path when other tools found evidence despite a mismatch
- **SRE Investigate — Save GAI Insight ai_insight length limit** (6)
  - accepts a summary whose projected stored size is exactly at the limit
  - rejects a summary one character over the projected limit without writing or rendering
  - rejects a summary the first write alone would accept but the render would push over the limit
  - tells the agent how much text is allowed and lists each field length
  - keeps the full text of a long summary under the limit without truncating it
  - keeps the value the render step writes under the limit for a summary at the projected limit
- **SRE Investigate — Save GAI Insight minimum summary length** (6)
  - accepts a summary whose text is exactly at the minimum
  - rejects a summary one character under the minimum without writing or rendering
  - tells the agent how to opt out when the report really is short
  - accepts a short summary when shortReport is "true"
  - only honors shortReport when it is exactly "true"
  - does not apply to the no-evidence case, which never writes the card
- **agent availability reasons** (5)
  - returns agent_inactive before checking a connection
  - returns no_connection when an active agent has no usable HTTP connection
  - returns null when an active agent has a usable HTTP connection
  - returns null when an active agent has a populated credential alias
  - logs a warning and returns null when an availability lookup throws
- **source vendor availability reasons** (5)
  - reports supported Prometheus failure reasons
  - returns null when either AWS transport is available
  - reports NOT_INSTALLED only when every AWS transport is inactive
  - reports NO_CONNECTION when an AWS transport lacks a connection
  - returns null for unknown vendors and lookup errors
- **vendor availability registry** (2)
  - routes every vendor to the expected availability check
  - fails closed and warns for an unknown vendor
- **source vendor availability gate** (10)
  - normalizes custom Meraki sources and default connection names consistently
  - uses the Meraki registry check when configured=true
  - uses the Meraki registry check when configured=false
  - uses the shared vendor registry and reports an unavailable source
  - treats AWS as configured when either MCP or API availability succeeds
  - falls back to connection check when vendor has no availability entry
  - falls back to connection check and returns false when no connection exists
  - routes azure to isVendorAvailable("azure-monitor-mcp"), not the connection-name fallback
  - reports azure as unconfigured when its availability check fails
  - fails open when the source vendor cannot be classified
- **Google Cloud Monitor adapter (googlemonitor)** (8)
  - matches when a result's last path segment equals the entity exactly
  - does NOT match a substring hit whose last path segment differs from the entity
  - matches on a non-empty timeSeries (Cloud Monitoring pod-network probe shape)
  - does not match an empty body
  - throws on an {error:{...}} body and marks the vendor uncheckable instead of a false miss
  - queues 3 ApiJobs for one googlemonitor connection, each carrying the resolved oauth2ProfileId
  - marks the vendor uncheckable, without queuing a job, when getGcaProjectId throws
  - marks the vendor uncheckable, without queuing a job, when getOauthEntityProfile throws
- **toRfc3339** (1)
  - converts a GlideDateTime value to an RFC3339 timestamp
- **vendorKeyFromName** (3)
  - classifies Azure connection/source names as "azure"
  - still classifies every other named vendor correctly
  - falls back to a plain slug for an unclassified vendor name

### node:test (TAP): 14 passing

- loadArtifact writes timestamped cache metadata and falls back to newest cache
- buildTaskModel emits one ordered post-install script task
- app merging deduplicates scopes and selects newest versions
- buildTaskModel merges Brazil apps before base setup scripts
- default merged script appends preview, enablement, Brazil settings, and diagnostics
- plan and JSON plan render the same ordered tasks
- parseArgs rejects conflicting output modes
- remote plan evaluation does not expose require or dynamic code generation
- generate writes script and plan by default with injected sources
- generate writes only the combined script with --script
- generate uses Brazil apps when the upstream base plan is unavailable
- generate still reports when a required preview artifact is unavailable
- Brazil plan apps are unique and AI Insights property is enabled
- asciiBox lists every generated path

### Jest (`sample-app:test:jest`): 251 passing test files (Jest prints per-file results only; run with `--verbose` for test names)

- `src/unit-tests/agents/_shared/`: aws-region, meraki-context
- `src/unit-tests/agents/_shared/tool-scripts/`: find-alert-ref, get-alert-impact-summary, get-alert-metadata, metadata-refactor, metadata-vendor-identity
- `src/unit-tests/agents/datadog-apm-mcp/`: datadog-apm-mcp-alias-templates
- `src/unit-tests/agents/gca-a2a/agent-scripts/`: gca-a2a-context-processing
- `src/unit-tests/agents/sre-incident-investigate/tool-scripts/`: extract-incident-candidates, resolve-incident
- `src/unit-tests/agents/sre-investigate/`: charge-policy-specs
- `src/unit-tests/agents/sre-investigate-basic/`: agent-evidence, agent-execute-acl, analysis-schema, billing-records, charge-contract, charge-event-wiring, charge-policy-specs, citation-contract, collect-evidence, collect-evidence-entry, collect-records, delegation-flag, derive, downstream-contract, gather-source-evidence, gcp-alias-templates, gcp-wiring, hook-filter-conditions, instructions-contract, meraki-connection-records, overview-summary, renderers, repair, report-gen, report-persist, result-contract, route-investigation, routing, routing-aws, routing-named-vendor, sanitize-content, save-basic-sre-report, sre-status, start-investigation
- `src/unit-tests/agents/sre-investigate/tool-scripts/`: find-vendors-thousandeyes, source-tenant-check, utils
- `src/unit-tests/fluent/`: agent-tool-schema-json
- `src/unit-tests/fluent/hooks/`: basic-metadata-plan-link
- `src/unit-tests/golden-dataset-test/`: golden, safety
- `src/unit-tests/golden-dataset-test/harness/`: cassette, clock, compare, masking, scenario
- `src/unit-tests/golden-dataset-test/harness/transports/`: transports
- `src/unit-tests/infra/`: cut-text, infra-independence, redact-secrets
- `src/unit-tests/infra/baseMode/`: api-transport, context-cap, mcp, module-boundary, orchestrator, orchestrator-source-selection, source-builder, vendor-gate
- `src/unit-tests/infra/baseMode/scheduler/`: budget, limits, loop, outcome, records, transport
- `src/unit-tests/infra/charging/`: charge-engine, charge-gates, charge-logging, charge-properties, charge-schedule, compile-policy, execution-tasks, feature-mapping, link-strategy, manual-usage-log, policy-spec
- `src/unit-tests/infra/featureFlag/`: feature-flag
- `src/unit-tests/infra/logging/`: logger, safe-log
- `src/unit-tests/infra/metadata/`: claim, contract, delegated-parent, store
- `src/unit-tests/infra/vendors/`: api-tool-json, basic-sre-usage, compare, connections, connections-credential, credential-guard, cut-marks, dynatrace-enrichment, dynatrace-gaps, dynatrace-gather, dynatrace-plan, explicit-time, ladder, latency-basic-sre-fast, mcp-reply, mcp-server-ids, named-queries, platform-alert, registry, resolve, support, support-evidence-clean, support-parse-json, support-text, values, vendor-module-value-by-key, vendor-modules, vendor-plan, wave-queue
- `src/unit-tests/infra/vendors/aws/`: alarm-config-check, aws-alarm, aws-anomalies, aws-correlation, aws-discovery-plan, aws-evidence, aws-gather, aws-insights, aws-log-groups, aws-plan, aws-reply, aws-retry, aws-saved-query, aws-signer, aws-tags, aws-tool, aws-tools, aws-vendor, aws-windows, example-context, signals-history-metric, signals-logs-correlation
- `src/unit-tests/infra/vendors/azure/`: azure-contracts, azure-evidence-cmdb, azure-plan
- `src/unit-tests/infra/vendors/datadog/`: data-block, datadog-evidence, datadog-extras, datadog-gather, datadog-plan, datadog-query, datadog-reply, datadog-tools, datadog-vendor, max-tokens-schema
- `src/unit-tests/infra/vendors/datadog/signals/`: dependencies-signal, deployments-signal, incidents-signal, logs-signal, metric-signal, monitor-signal, services-signal, slos-signal, spans-signal, trace-signal
- `src/unit-tests/infra/vendors/dynatrace/`: dynatrace-entity-detail, dynatrace-host-metric-periods, dynatrace-log-sources, dynatrace-log-t2, dynatrace-log-t3, dynatrace-parity-plan, dynatrace-spans, dynatrace-time, dynatrace-vulnerabilities
- `src/unit-tests/infra/vendors/gcp/`: gcp-acceptance, gcp-budget, gcp-cmdb, gcp-core-plan, gcp-evidence, gcp-identifiers, gcp-optional-plan, gcp-refusal, gcp-tool, gcp-tools, gcp-window
- `src/unit-tests/infra/vendors/logicmonitor/`: alert-timeline, cmdb, datasource-hints, domain-basics, group-blast-radius, ipv4, lm-alert, lm-device, lm-waves, logicmonitor-plan, logicmonitor-vendor, metric-assessment, metric-summary, occurrence, parent-groups, parity-wiring, probes-w2a, probes-w2b, probes-w3, reboot, siblings, target, threshold, tools, upstream
- `src/unit-tests/infra/vendors/meraki/`: meraki-catalog-tools, meraki-core-plan, meraki-followup-plan, meraki-privacy-vendor, meraki-reply, meraki-window-evidence
- `src/unit-tests/infra/vendors/newrelic/`: newrelic-connection, newrelic-contracts, newrelic-discovery, newrelic-oauth, newrelic-plan
- `src/unit-tests/infra/vendors/prometheus/`: prometheus-evidence, prometheus-plan, prometheus-tools-match, promql-window
- `src/unit-tests/infra/vendors/solarwinds/`: solarwinds-api-response, solarwinds-api-tool, solarwinds-gather, solarwinds-node-extra, solarwinds-node-extra-plan, solarwinds-plan, solarwinds-resolve-entity, solarwinds-window
- `src/unit-tests/infra/vendors/splunk/`: spl, spl-queries, splunk-entity, splunk-evidence, splunk-plan, splunk-tool, splunk-tool-factory, splunk-vendor
- `src/unit-tests/infra/vendors/thousandeyes/`: thousandeyes-evidence, thousandeyes-plan, thousandeyes-reply-shapes, thousandeyes-reply-tools, thousandeyes-types-rule, thousandeyes-vendor, thousandeyes-window

---
*Omitted as noise: Jenkins timestamps, git/pipeline output, env dump, pnpm/vendor install, webpack, SDLC annotation warnings, duplicate reporter lines, per-test timings, console output.*
