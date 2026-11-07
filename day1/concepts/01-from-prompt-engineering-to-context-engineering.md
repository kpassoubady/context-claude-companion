# From Prompt Engineering to Context Engineering
Reference for extending prompt design across the full runtime information environment of an agentic coding assistant.

---

## Extending Prompt Design to Agentic Loops

Prompt engineering focuses on how a single request or system instruction is phrased before a model generates a response. Context engineering extends that discipline across every piece of information present in the model window during an iterative workflow. In Claude Code, the assistant reads repository files, executes shell commands, searches codebases, and inspects test output across multiple turns. Each step adds new tokens to the working set and shapes how subsequent decisions are made.

Treating an agentic coding session like a one-shot chat prompt leaves the working window unmanaged after turn one. Practitioners design both the initial task prompt and the rules, file selections, and tool outputs that enter the session over time.

## Prompt Engineering and Context Engineering Compared

| Dimension | Prompt Engineering | Context Engineering |
| :--- | :--- | :--- |
| **Primary scope** | Wording of a single request or static instruction | Full runtime state across a multi-turn agent loop |
| **Core inputs** | Task phrasing, examples, output format constraints | Project instructions, scoped rules, retrieved files, tool schemas, tool outputs, memory |
| **Typical failure mode** | Ambiguous task specification or missing format constraints | Noisy tool dumps, stale assumptions, competing rules, diluted focus |
| **Unit of control** | Sentences and clauses inside a prompt | What enters, remains in, or leaves the context window at each turn |

## Working Context and Recall Under Noise

As an agentic loop runs, the working context accumulates file contents, search matches, stack traces, and intermediate edits. Low-signal text competes with task-relevant instructions and architectural constraints. When thousands of lines of unfiltered test logs or lockfiles sit inside the active window, recall of earlier project conventions and focus on the active constraint can degrade, a phenomenon often described as context rot. Larger or noisier context does not guarantee a hallucination, and no fixed token count serves as a universal failure threshold, but irrelevant volume increases cost and makes subtle project invariants harder to follow.

Developers keep the working set high-signal by bounding what tools return. Running a single failing test file with concise output preserves diagnostic evidence without flooding the window with passing test traces.

```bash
# Unbounded output floods the context window with passing traces
pytest -vv --tb=long

# Bounded output keeps only the failing assertion and summary in context
pytest tests/settlement/test_rounding.py -q --tb=short
```

## Trust Boundaries in Retrieved Context

Everything read from a repository file, issue description, dependency README, or test log enters the same model context window as project guidance. Under the OWASP Top 10 for LLM Applications (LLM01 Prompt Injection and LLM02 Sensitive Information Disclosure), retrieved text is untrusted evidence rather than authority to alter the task or expose secrets. Under the NIST AI Risk Management Framework (Govern, Map, Measure, Manage), engineering teams identify acceptable data sources, map what enters context, and verify outputs against objective tests.

A search filter or `.gitignore` rule reduces noise in the working window, but it is not an access-control boundary. Teams protect sensitive data by using synthetic fixtures in development, enforcing repository and credential permissions at the platform layer, and reviewing proposed code diffs and test results before merging.

