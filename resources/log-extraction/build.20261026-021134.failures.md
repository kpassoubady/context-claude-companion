# Java Test Failure Analysis Report

- **Source Log:** `build.20261026-021134.log`
- **Full Path:** `test/e2e/llm-context/artifacts/build-log/build.20261026-021134.log`
- **Original Log Size:** 3.90 MB (28,023 lines)
- **Build Status:** **BUILD SUCCESS** *(Note: `testFailureIgnore` was active; test failures did not halt the build)*
- **Total time:  29:53 min**
- **Finished at: 2026-10-26T02:41:29-07:00**

## Executive Test Summary

- **Total Tests Executed:** 290
- **Failures:** 16 | **Errors:** 0 | **Skipped:** 10
- **Unique Failing Tests:** 16 across 12 test classes

---

## 1. Failed Tests Overview

| # | Test Class | Method | Type | Summary Message | Code Location | Runs |
|---|------------|--------|------|-----------------|---------------|------|
| 1 | `AD_AgentSecurityDirectiveIT` | `newRelicSysAliasAndTemplate` | FAILURE | sys_alias 'New Relic MCP Server Agent' should exist | `AD_AgentSecurityDirectiveIT.java:147` | 2x |
| 2 | `AG_AppIntegrityValidationIT` | `teamAndMembersExist` | FAILURE | Team should have at least 2 members (agents), found 1 | `AG_AppIntegrityValidationIT.java:102` | 2x |
| 3 | `AG_AppIntegrityValidationIT` | `sreInvestigateChildrenExist` | FAILURE | SRE Investigate child agent 'SolarWinds analysis AI Agent' should be wired vi... | `AG_AppIntegrityValidationIT.java:383` | 2x |
| 4 | `AJ_GoldenConfigValidationIT` | `obsToolRecordsExist` | FAILURE | Tool 'Root Cause Details Agent' should be active | `AJ_GoldenConfigValidationIT.java:118` | 2x |
| 5 | `AM_AWSCloudWatchConfigIT` | `agentInstructionsContainWorkflowKeywords` | FAILURE | Agent instructions should contain all workflow structure keywords. Missing: C... | `AM_AWSCloudWatchConfigIT.java:355` | 2x |
| 6 | `AN_ThousandEyesConfigIT` | `agentInstructionsContainWorkflowKeywords` | FAILURE | Agent instructions should contain workflow keyword for 'Report confidence sec... | `AN_ThousandEyesConfigIT.java:381` | 2x |
| 7 | `AO_AWSCloudWatchAPIConfigIT` | `agentInstructionsContainWorkflowKeywords` | FAILURE | Agent instructions should contain all workflow structure keywords. Missing: C... | `AO_AWSCloudWatchAPIConfigIT.java:430` | 2x |
| 8 | `AO_SolarWindsConfigIT` | `accessRoleLimitsToOperator` | FAILURE | No access role config found for SolarWinds agent — ACL record may be missing | `AO_SolarWindsConfigIT.java:232` | 2x |
| 9 | `AP_NetworkSmeConfigIT` | `accessRoleLimitsToOperator` | FAILURE | No access role config found for Network SME agent | `AP_NetworkSmeConfigIT.java:142` | 2x |
| 10 | `AQ_LogicMonitorConfigIT` | `agentConfigRecordExists` | FAILURE | Agent config should use dedicated LM service account (svc_logicmonitor_ai_age... | `AQ_LogicMonitorConfigIT.java:247` | 2x |
| 11 | `AR_SREInvestigateConfigIT` | `runAsUserIsDedicatedOperator` | FAILURE | expected:<svc_[sre_investigate]_ai_agent> but was:<svc_[observability]_ai_agent> | `AR_SREInvestigateConfigIT.java:117` | 2x |
| 12 | `AS_NewRelicMcpConfigIT` | `accessRoleLimitsToOperator` | FAILURE | Access role config for New Relic MCP agent should exist | `AS_NewRelicMcpConfigIT.java:248` | 2x |
| 13 | `AU_AzureMonitorMCPConfigIT` | `accessRoleConfigExists` | FAILURE | Access role config for 'Azure Monitor MCP Agent' should exist | `AU_AzureMonitorMCPConfigIT.java:151` | 2x |
| 14 | `AU_AzureMonitorMCPConfigIT` | `allToolsExistAndLinked` | FAILURE | Unlinked tools: [Lookup CMDB CI] | `AU_AzureMonitorMCPConfigIT.java:305` | 2x |
| 15 | `AU_AzureMonitorMCPConfigIT` | `toolCountMatches` | FAILURE | Expected 13 tool mappings expected:<13> but was:<14> | `AU_AzureMonitorMCPConfigIT.java:323` | 2x |
| 16 | `AU_AzureMonitorMCPConfigIT` | `agentHasContextProcessingScript` | FAILURE | Context processing script should pass triggerContext | `AU_AzureMonitorMCPConfigIT.java:377` | 2x |

---

## 2. Maven Surefire / Failsafe Results Summary

### Execution Run #1
```text
Failures:
AD_AgentSecurityDirectiveIT.newRelicSysAliasAndTemplate:147 sys_alias 'New Relic MCP Server Agent' should exist
AG_AppIntegrityValidationIT.sreInvestigateChildrenExist:383 SRE Investigate child agent 'SolarWinds analysis AI Agent' should be wired via sn_aia_agent_child. If a child was renamed, update SRE_INVESTIGATE_CHILDREN. If a child was removed, remove it from SRE_INVESTIGATE_CHILDREN.
AG_AppIntegrityValidationIT.teamAndMembersExist:102 Team should have at least 2 members (agents), found 1
AJ_GoldenConfigValidationIT.obsToolRecordsExist:118 Tool 'Root Cause Details Agent' should be active
AM_AWSCloudWatchConfigIT.agentInstructionsContainWorkflowKeywords:355 Agent instructions should contain all workflow structure keywords. Missing: Confidence section
AN_ThousandEyesConfigIT.agentInstructionsContainWorkflowKeywords:381 Agent instructions should contain workflow keyword for 'Report confidence section' (expected one of: Confidence)
AO_AWSCloudWatchAPIConfigIT.agentInstructionsContainWorkflowKeywords:430 Agent instructions should contain all workflow structure keywords. Missing: Confidence section
AO_SolarWindsConfigIT.accessRoleLimitsToOperator:232 No access role config found for SolarWinds agent — ACL record may be missing
AP_NetworkSmeConfigIT.accessRoleLimitsToOperator:142 No access role config found for Network SME agent
AQ_LogicMonitorConfigIT.agentConfigRecordExists:247 Agent config should use dedicated LM service account (svc_logicmonitor_ai_agent), found: svc_observability_ai_agent
AR_SREInvestigateConfigIT.runAsUserIsDedicatedOperator:117 expected:<svc_[sre_investigate]_ai_agent> but was:<svc_[observability]_ai_agent>
AS_NewRelicMcpConfigIT.accessRoleLimitsToOperator:248 Access role config for New Relic MCP agent should exist
AU_AzureMonitorMCPConfigIT.accessRoleConfigExists:151 Access role config for 'Azure Monitor MCP Agent' should exist
AU_AzureMonitorMCPConfigIT.agentHasContextProcessingScript:377 Context processing script should pass triggerContext
AU_AzureMonitorMCPConfigIT.allToolsExistAndLinked:305 Unlinked tools: [Lookup CMDB CI]
AU_AzureMonitorMCPConfigIT.toolCountMatches:323 Expected 13 tool mappings expected:<13> but was:<14>
Tests run: 290, Failures: 16, Errors: 0, Skipped: 10
```

### Execution Run #2
```text
Failures:
AD_AgentSecurityDirectiveIT.newRelicSysAliasAndTemplate:147 sys_alias 'New Relic MCP Server Agent' should exist
AG_AppIntegrityValidationIT.sreInvestigateChildrenExist:383 SRE Investigate child agent 'SolarWinds analysis AI Agent' should be wired via sn_aia_agent_child. If a child was renamed, update SRE_INVESTIGATE_CHILDREN. If a child was removed, remove it from SRE_INVESTIGATE_CHILDREN.
AG_AppIntegrityValidationIT.teamAndMembersExist:102 Team should have at least 2 members (agents), found 1
AJ_GoldenConfigValidationIT.obsToolRecordsExist:118 Tool 'Root Cause Details Agent' should be active
AM_AWSCloudWatchConfigIT.agentInstructionsContainWorkflowKeywords:355 Agent instructions should contain all workflow structure keywords. Missing: Confidence section
AN_ThousandEyesConfigIT.agentInstructionsContainWorkflowKeywords:381 Agent instructions should contain workflow keyword for 'Report confidence section' (expected one of: Confidence)
AO_AWSCloudWatchAPIConfigIT.agentInstructionsContainWorkflowKeywords:430 Agent instructions should contain all workflow structure keywords. Missing: Confidence section
AO_SolarWindsConfigIT.accessRoleLimitsToOperator:232 No access role config found for SolarWinds agent — ACL record may be missing
AP_NetworkSmeConfigIT.accessRoleLimitsToOperator:142 No access role config found for Network SME agent
AQ_LogicMonitorConfigIT.agentConfigRecordExists:247 Agent config should use dedicated LM service account (svc_logicmonitor_ai_agent), found: svc_observability_ai_agent
AR_SREInvestigateConfigIT.runAsUserIsDedicatedOperator:117 expected:<svc_[sre_investigate]_ai_agent> but was:<svc_[observability]_ai_agent>
AS_NewRelicMcpConfigIT.accessRoleLimitsToOperator:248 Access role config for New Relic MCP agent should exist
AU_AzureMonitorMCPConfigIT.accessRoleConfigExists:151 Access role config for 'Azure Monitor MCP Agent' should exist
AU_AzureMonitorMCPConfigIT.agentHasContextProcessingScript:377 Context processing script should pass triggerContext
AU_AzureMonitorMCPConfigIT.allToolsExistAndLinked:305 Unlinked tools: [Lookup CMDB CI]
AU_AzureMonitorMCPConfigIT.toolCountMatches:323 Expected 13 tool mappings expected:<13> but was:<14>
Tests run: 290, Failures: 16, Errors: 0, Skipped: 10
```

---

## 3. Detailed Failure Breakdown

### 1. `AD_AgentSecurityDirectiveIT#newRelicSysAliasAndTemplate`
- **Full Class:** `com.example.app.com.api.AD_AgentSecurityDirectiveIT`
- **Method:** `newRelicSysAliasAndTemplate`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AD_AgentSecurityDirectiveIT.java:147`
- **Failure Detail:** sys_alias 'New Relic MCP Server Agent' should exist

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:15:26 AM com.example.app.com.api.AD_AgentSecurityDirectiveIT newRelicSysAliasAndTemplate
INFO: Step 3: Querying sys_alias for New Relic configuration
Oct 26, 2026 2:15:26 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sys_alias] with query [name=New Relic MCP Server Agent]
```

#### Stack Trace:
```java
java.lang.AssertionError: sys_alias 'New Relic MCP Server Agent' should exist
at com.example.app.com.api.AD_AgentSecurityDirectiveIT.newRelicSysAliasAndTemplate(AD_AgentSecurityDirectiveIT.java:147)
```

### 2. `AG_AppIntegrityValidationIT#teamAndMembersExist`
- **Full Class:** `com.example.app.com.api.AG_AppIntegrityValidationIT`
- **Method:** `teamAndMembersExist`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AG_AppIntegrityValidationIT.java:102`
- **Failure Detail:** Team should have at least 2 members (agents), found 1

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:15:36 AM com.example.app.com.api.AG_AppIntegrityValidationIT teamAndMembersExist
INFO: Team members: 1
```

#### Stack Trace:
```java
java.lang.AssertionError: Team should have at least 2 members (agents), found 1
at com.example.app.com.api.AG_AppIntegrityValidationIT.teamAndMembersExist(AG_AppIntegrityValidationIT.java:102)
```

### 3. `AG_AppIntegrityValidationIT#sreInvestigateChildrenExist`
- **Full Class:** `com.example.app.com.api.AG_AppIntegrityValidationIT`
- **Method:** `sreInvestigateChildrenExist`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AG_AppIntegrityValidationIT.java:383`
- **Failure Detail:** SRE Investigate child agent 'SolarWinds analysis AI Agent' should be wired via sn_aia_agent_child. If a child was renamed, update SRE_INVESTIGATE_CHILDREN. If a child was removed, remove it from SRE_INVESTIGATE_CHILDREN.

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:15:40 AM com.example.app.com.api.AG_AppIntegrityValidationIT sreInvestigateChildrenExist
INFO:   Found expected child: Dynatrace MCP Server Agent
```

#### Stack Trace:
```java
java.lang.AssertionError: SRE Investigate child agent 'SolarWinds analysis AI Agent' should be wired via sn_aia_agent_child. If a child was renamed, update SRE_INVESTIGATE_CHILDREN. If a child was removed, remove it from SRE_INVESTIGATE_CHILDREN.
at com.example.app.com.api.AG_AppIntegrityValidationIT.sreInvestigateChildrenExist(AG_AppIntegrityValidationIT.java:383)
```

### 4. `AJ_GoldenConfigValidationIT#obsToolRecordsExist`
- **Full Class:** `com.example.app.com.api.AJ_GoldenConfigValidationIT`
- **Method:** `obsToolRecordsExist`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AJ_GoldenConfigValidationIT.java:118`
- **Failure Detail:** Tool 'Root Cause Details Agent' should be active

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:16:24 AM com.example.app.com.api.AJ_GoldenConfigValidationIT obsToolRecordsExist
INFO:   Tool: Get Kentik insights report (record_type=template, type=action, active=true)
```

#### Stack Trace:
```java
java.lang.AssertionError: Tool 'Root Cause Details Agent' should be active
at com.example.app.com.api.AJ_GoldenConfigValidationIT.obsToolRecordsExist(AJ_GoldenConfigValidationIT.java:118)
```

### 5. `AM_AWSCloudWatchConfigIT#agentInstructionsContainWorkflowKeywords`
- **Full Class:** `com.example.app.com.api.AM_AWSCloudWatchConfigIT`
- **Method:** `agentInstructionsContainWorkflowKeywords`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AM_AWSCloudWatchConfigIT.java:355`
- **Failure Detail:** Agent instructions should contain all workflow structure keywords. Missing: Confidence section

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:16:42 AM com.example.app.com.api.AM_AWSCloudWatchConfigIT agentInstructionsContainWorkflowKeywords
INFO: Workflow keyword check: 24/25 matched, missing: Confidence section
```

#### Stack Trace:
```java
java.lang.AssertionError: Agent instructions should contain all workflow structure keywords. Missing: Confidence section
at com.example.app.com.api.AM_AWSCloudWatchConfigIT.agentInstructionsContainWorkflowKeywords(AM_AWSCloudWatchConfigIT.java:355)
```

### 6. `AN_ThousandEyesConfigIT#agentInstructionsContainWorkflowKeywords`
- **Full Class:** `com.example.app.com.api.AN_ThousandEyesConfigIT`
- **Method:** `agentInstructionsContainWorkflowKeywords`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AN_ThousandEyesConfigIT.java:381`
- **Failure Detail:** Agent instructions should contain workflow keyword for 'Report confidence section' (expected one of: Confidence)

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:16:52 AM com.example.app.com.api.AN_ThousandEyesConfigIT agentInstructionsContainWorkflowKeywords
INFO: Workflow keyword 'Timestamp format': matched 'UTC'
```

#### Stack Trace:
```java
java.lang.AssertionError: Agent instructions should contain workflow keyword for 'Report confidence section' (expected one of: Confidence)
at com.example.app.com.api.AN_ThousandEyesConfigIT.agentInstructionsContainWorkflowKeywords(AN_ThousandEyesConfigIT.java:381)
```

### 7. `AO_AWSCloudWatchAPIConfigIT#agentInstructionsContainWorkflowKeywords`
- **Full Class:** `com.example.app.com.api.AO_AWSCloudWatchAPIConfigIT`
- **Method:** `agentInstructionsContainWorkflowKeywords`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AO_AWSCloudWatchAPIConfigIT.java:430`
- **Failure Detail:** Agent instructions should contain all workflow structure keywords. Missing: Confidence section

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:17:01 AM com.example.app.com.api.AO_AWSCloudWatchAPIConfigIT agentInstructionsContainWorkflowKeywords
INFO: Workflow keyword check: 29/30 matched, missing: Confidence section
```

#### Stack Trace:
```java
java.lang.AssertionError: Agent instructions should contain all workflow structure keywords. Missing: Confidence section
at com.example.app.com.api.AO_AWSCloudWatchAPIConfigIT.agentInstructionsContainWorkflowKeywords(AO_AWSCloudWatchAPIConfigIT.java:430)
```

### 8. `AO_SolarWindsConfigIT#accessRoleLimitsToOperator`
- **Full Class:** `com.example.app.com.api.AO_SolarWindsConfigIT`
- **Method:** `accessRoleLimitsToOperator`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AO_SolarWindsConfigIT.java:232`
- **Failure Detail:** No access role config found for SolarWinds agent — ACL record may be missing

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:17:07 AM com.example.app.com.api.AO_SolarWindsConfigIT accessRoleLimitsToOperator
WARNING: No access role config found for 'SolarWinds' — checking by agent sys_id
Oct 26, 2026 2:17:07 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sys_agent_access_role_configuration] with query [agent=9c4e8ad2ffb3b6104f7bffffffffffcf]
```

#### Stack Trace:
```java
java.lang.AssertionError: No access role config found for SolarWinds agent — ACL record may be missing
at com.example.app.com.api.AO_SolarWindsConfigIT.accessRoleLimitsToOperator(AO_SolarWindsConfigIT.java:232)
```

### 9. `AP_NetworkSmeConfigIT#accessRoleLimitsToOperator`
- **Full Class:** `com.example.app.com.api.AP_NetworkSmeConfigIT`
- **Method:** `accessRoleLimitsToOperator`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AP_NetworkSmeConfigIT.java:142`
- **Failure Detail:** No access role config found for Network SME agent

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:17:12 AM com.example.app.com.api.AP_NetworkSmeConfigIT accessRoleLimitsToOperator
WARNING: No access role config found by name — checking by agent reference
Oct 26, 2026 2:17:12 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sys_agent_access_role_configuration] with query [agent=2ce22bb276f8435e8ad525c7a78f5530]
```

#### Stack Trace:
```java
java.lang.AssertionError: No access role config found for Network SME agent
at com.example.app.com.api.AP_NetworkSmeConfigIT.accessRoleLimitsToOperator(AP_NetworkSmeConfigIT.java:142)
```

### 10. `AQ_LogicMonitorConfigIT#agentConfigRecordExists`
- **Full Class:** `com.example.app.com.api.AQ_LogicMonitorConfigIT`
- **Method:** `agentConfigRecordExists`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AQ_LogicMonitorConfigIT.java:247`
- **Failure Detail:** Agent config should use dedicated LM service account (svc_logicmonitor_ai_agent), found: svc_observability_ai_agent

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:17:25 AM com.example.app.com.api.AQ_LogicMonitorConfigIT agentConfigRecordExists
INFO: Step 5: Checking sn_aia_agent_config for LogicMonitor agent
Oct 26, 2026 2:17:25 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sn_aia_agent_config] with query [agent.name=LogicMonitor API Agent]
```

#### Stack Trace:
```java
java.lang.AssertionError: Agent config should use dedicated LM service account (svc_logicmonitor_ai_agent), found: svc_observability_ai_agent
at com.example.app.com.api.AQ_LogicMonitorConfigIT.agentConfigRecordExists(AQ_LogicMonitorConfigIT.java:247)
```

### 11. `AR_SREInvestigateConfigIT#runAsUserIsDedicatedOperator`
- **Full Class:** `com.example.app.com.api.AR_SREInvestigateConfigIT`
- **Method:** `runAsUserIsDedicatedOperator`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `org.junit.ComparisonFailure`
- **Location:** `AR_SREInvestigateConfigIT.java:117`
- **Failure Detail:** expected:<svc_[sre_investigate]_ai_agent> but was:<svc_[observability]_ai_agent>

#### Stack Trace:
```java
org.junit.ComparisonFailure: expected:<svc_[sre_investigate]_ai_agent> but was:<svc_[observability]_ai_agent>
at com.example.app.com.api.AR_SREInvestigateConfigIT.runAsUserIsDedicatedOperator(AR_SREInvestigateConfigIT.java:117)
```

### 12. `AS_NewRelicMcpConfigIT#accessRoleLimitsToOperator`
- **Full Class:** `com.example.app.com.api.AS_NewRelicMcpConfigIT`
- **Method:** `accessRoleLimitsToOperator`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AS_NewRelicMcpConfigIT.java:248`
- **Failure Detail:** Access role config for New Relic MCP agent should exist

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:18:08 AM com.example.app.com.api.AS_NewRelicMcpConfigIT accessRoleLimitsToOperator
WARNING: No access role config found by name — checking by agent reference
Oct 26, 2026 2:18:08 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sys_agent_access_role_configuration] with query [agent=2d53a26b9998434796fad95d64d53303]
```

#### Stack Trace:
```java
java.lang.AssertionError: Access role config for New Relic MCP agent should exist
at com.example.app.com.api.AS_NewRelicMcpConfigIT.accessRoleLimitsToOperator(AS_NewRelicMcpConfigIT.java:248)
```

### 13. `AU_AzureMonitorMCPConfigIT#accessRoleConfigExists`
- **Full Class:** `com.example.app.com.api.AU_AzureMonitorMCPConfigIT`
- **Method:** `accessRoleConfigExists`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AU_AzureMonitorMCPConfigIT.java:151`
- **Failure Detail:** Access role config for 'Azure Monitor MCP Agent' should exist

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:18:42 AM com.example.app.com.api.AU_AzureMonitorMCPConfigIT accessRoleConfigExists
INFO: Step 4: Verifying access role configuration
Oct 26, 2026 2:18:42 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sn_aia_agent] with query [name=Azure Monitor MCP Agent]
Oct 26, 2026 2:18:43 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sys_agent_access_role_configuration] with query [agent=00452961698044768fce82cb3839fb27]
```

#### Stack Trace:
```java
java.lang.AssertionError: Access role config for 'Azure Monitor MCP Agent' should exist
at com.example.app.com.api.AU_AzureMonitorMCPConfigIT.accessRoleConfigExists(AU_AzureMonitorMCPConfigIT.java:151)
```

### 14. `AU_AzureMonitorMCPConfigIT#allToolsExistAndLinked`
- **Full Class:** `com.example.app.com.api.AU_AzureMonitorMCPConfigIT`
- **Method:** `allToolsExistAndLinked`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AU_AzureMonitorMCPConfigIT.java:305`
- **Failure Detail:** Unlinked tools: [Lookup CMDB CI]

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:18:51 AM com.example.app.com.api.AU_AzureMonitorMCPConfigIT allToolsExistAndLinked
INFO:   Tool 'Lookup CMDB CI': exists=true, linked=false
```

#### Stack Trace:
```java
java.lang.AssertionError: Unlinked tools: [Lookup CMDB CI]
at com.example.app.com.api.AU_AzureMonitorMCPConfigIT.allToolsExistAndLinked(AU_AzureMonitorMCPConfigIT.java:305)
```

### 15. `AU_AzureMonitorMCPConfigIT#toolCountMatches`
- **Full Class:** `com.example.app.com.api.AU_AzureMonitorMCPConfigIT`
- **Method:** `toolCountMatches`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AU_AzureMonitorMCPConfigIT.java:323`
- **Failure Detail:** Expected 13 tool mappings expected:<13> but was:<14>

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:18:51 AM com.example.app.com.api.AU_AzureMonitorMCPConfigIT toolCountMatches
INFO: Step 11: Verifying tool count
Oct 26, 2026 2:18:51 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sn_aia_agent] with query [name=Azure Monitor MCP Agent]
Oct 26, 2026 2:18:51 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sn_aia_agent_tool_m2m] with query [agent=00452961698044768fce82cb3839fb27]
```

#### Stack Trace:
```java
java.lang.AssertionError: Expected 13 tool mappings expected:<13> but was:<14>
at com.example.app.com.api.AU_AzureMonitorMCPConfigIT.toolCountMatches(AU_AzureMonitorMCPConfigIT.java:323)
```

### 16. `AU_AzureMonitorMCPConfigIT#agentHasContextProcessingScript`
- **Full Class:** `com.example.app.com.api.AU_AzureMonitorMCPConfigIT`
- **Method:** `agentHasContextProcessingScript`
- **Outcome:** `FAILURE` (Failed across 2 test executions (consistent failure))
- **Exception:** `java.lang.AssertionError`
- **Location:** `AU_AzureMonitorMCPConfigIT.java:377`
- **Failure Detail:** Context processing script should pass triggerContext

#### Preceding Execution Logs (Test Steps / DB / API Calls):
```text
Oct 26, 2026 2:18:52 AM com.example.app.com.api.AU_AzureMonitorMCPConfigIT agentHasContextProcessingScript
INFO: Step 13: Verifying agent context processing script
Oct 26, 2026 2:18:52 AM com.example.app.base.BaseTableTest queryTable
INFO: Querying table [sn_aia_agent] with query [name=Azure Monitor MCP Agent]
```

#### Stack Trace:
```java
java.lang.AssertionError: Context processing script should pass triggerContext
at com.example.app.com.api.AU_AzureMonitorMCPConfigIT.agentHasContextProcessingScript(AU_AzureMonitorMCPConfigIT.java:377)
```

---

## 4. Maven Reactor Summary

```text
Reactor Summary for AI Agents for Observability - Master Build 30.0.0.0-SNAPSHOT:

AI Agents for Observability - Parent POM ........... SUCCESS [02:23 min]
sample-agents-integration-test ................ SUCCESS [27:21 min]
AI Agents for Observability - Master Build ......... SUCCESS [  6.929 s]
Total time:  29:53 min
Finished at: 2026-10-26T02:41:29-07:00
```
