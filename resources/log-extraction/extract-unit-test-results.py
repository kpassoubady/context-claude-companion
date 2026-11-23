#!/usr/bin/env python3
"""
extract-unit-test-results.py

Condenses a large Jenkins / Maven unit-test build log (Mocha, node:test TAP, Jest
with coverage, Prettier, tsc) into a compact, LLM-ready Markdown digest.

Sibling of extract-test-failures.py, which targets Java/Surefire logs. This one
targets the JavaScript pipeline run by `pnpm run ci:test`:

  - Run summary: one table row per runner (passed / failed / skipped / duration)
  - Failures in full: Mocha "N failing" blocks, TAP `not ok` blocks, Jest `●` blocks,
    TypeScript errors, Prettier complaints, Jest coverage-threshold messages
  - Passing tests, compact: Mocha test names grouped by suite (de-duplicated across
    the two reporters), Jest passing files grouped by directory
  - Coverage: totals plus only the files below a threshold, with uncovered lines

Dropped on purpose: Jenkins timestamps, git/pipeline chatter, env dumps, pnpm and
vendor install output, webpack output, SDLC "Could not obtain annotations" warnings,
duplicated reporter lines, per-test timings, Jest console.log blocks.
"""

import argparse
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
TS_PREFIX_RE = re.compile(r"^\[\d{4}-\d{2}-\d{2}T[\d:.]+Z\]\s?")
LEVEL_RE = re.compile(r"^\[(INFO|ERROR|WARNING|WARN|DEBUG)\]\s?")

# "> pkg@1.0.0 script-name /abs/path"  — pnpm announces every script it runs
SCRIPT_HEADER_RE = re.compile(r"^> (\S+)@(\S+) (\S+) (/\S+)$")
SCRIPT_CMD_RE = re.compile(r"^> (.+)$")

# Matched with .search and a 2+ space anchor because Jenkins sometimes glues a pass line onto
# the tail of unrelated console output ("... {1} [    ✔ test name").
MOCHA_PASS_TIMED_RE = re.compile(r"(?:^|\s{2,})[✔✓] (.+): (\d+)ms$")      # reporter B (name: Nms)
MOCHA_PASS_SPEC_RE = re.compile(r"(?:^|\s{2,})[✔✓] (.+?)(?: \((\d+)ms\))?$")  # reporter A (spec)
MOCHA_PENDING_RE = re.compile(r"^\s+- (.+)$")
MOCHA_SUMMARY_RE = re.compile(r"^\s*(\d+) (passing|failing|pending)(?: \(([^)]+)\))?")
MOCHA_FAIL_START_RE = re.compile(r"^\s{2}(\d+)\) (.*)$")
TAP_OK_RE = re.compile(r"^(not )?ok (\d+) - (.*?)(?: # (SKIP|TODO).*)?$")
TAP_COUNT_RE = re.compile(r"^# (tests|pass|fail|skipped|todo|cancelled) (\d+)")
SUITE_DURATION_RE = re.compile(r"^\s*Suite duration:")

JEST_FILE_RE = re.compile(r"^(PASS|FAIL) (\S+)(?: \(([\d.]+) s\))?$")
JEST_BULLET_RE = re.compile(r"^\s*● (.+)$")
JEST_TOTALS_RE = re.compile(r"^(Test Suites|Tests|Snapshots|Time):\s+(.*)$")
JEST_THRESHOLD_RE = re.compile(r'^Jest: "?.*coverage threshold.*')
COV_ROW_RE = re.compile(
    r"^(\s*)(\S.*?)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(.*?)\s*$"
)
COV_HEADER_RE = re.compile(r"^\s*File\s*\|\s*% Stmts")

TS_ERROR_RE = re.compile(r"error TS\d+")
STACK_NOISE_RE = re.compile(r"node_modules|node:internal|\(<anonymous>\)|processTicksAndRejections")
MAVEN_ERROR_NOISE_RE = re.compile(r"->\s*\[Help|^\s*$|To see the full stack trace|Re-run Maven|For more information|re-run Maven|MojoFailure")


def clean(line: str) -> str:
    line = ANSI_RE.sub("", line.rstrip("\r\n"))
    return TS_PREFIX_RE.sub("", line)


def split_level(line: str):
    m = LEVEL_RE.match(line)
    if m:
        return m.group(1), line[m.end():]
    return "", line


def classify_command(cmd: str) -> str:
    # `pnpm run a && pnpm run b` wrappers only delegate; the leaf script gets its own section.
    if re.match(r"^(pnpm|npm|yarn)\s", cmd):
        return "other"
    if "mocha" in cmd:
        return "mocha"
    if "jest" in cmd:
        return "jest"
    if "prettier" in cmd:
        return "prettier"
    if re.search(r"\btsc\b", cmd):
        return "tsc"
    return "other"


# --------------------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------------------

class Section:
    def __init__(self, script, pkg, command):
        self.script = script
        self.pkg = pkg
        self.command = command
        self.kind = classify_command(command)
        self.lines = []  # (level, text)

    @property
    def label(self):
        return f"{self.pkg}:{self.script}"


def split_sections(entries):
    """Group log lines into per-script sections. entries = [(level, text)]."""
    sections = []
    current = None
    meta = {}
    pending_header = None
    for level, text in entries:
        h = SCRIPT_HEADER_RE.match(text)
        if h:
            pending_header = (h.group(1), h.group(3))
            continue
        if pending_header:
            c = SCRIPT_CMD_RE.match(text)
            if c:
                current = Section(pending_header[1], pending_header[0], c.group(1))
                sections.append(current)
                pending_header = None
                continue
            if text.strip():
                pending_header = None  # header with no command line; ignore
        if current is not None:
            current.lines.append((level, text))
    return sections


def parse_mocha(section):
    """Return dict describing a Mocha run (spec + TAP output, both reporters)."""
    res = {
        "suites": OrderedDict(),  # suite -> [test names]
        "pending": [],
        "failures": [],
        "tap": {"ok": [], "not_ok": [], "skipped": [], "counts": {}},
        "passing": None, "failing": None, "pending_n": None, "duration": None,
    }
    suite = "(no suite)"
    seen_timed = False
    lines = [t for _, t in section.lines]

    # Pass 1: find the point where mocha's "N failing" block begins so we can stop treating
    # lines as spec output there.
    fail_idx = None
    for i, t in enumerate(lines):
        m = MOCHA_SUMMARY_RE.match(t)
        if m and m.group(2) == "failing":
            fail_idx = i
            break

    i = 0
    n = len(lines)
    while i < n:
        t = lines[i]

        # ---- TAP (node:test) ----
        tap = TAP_OK_RE.match(t)
        if tap:
            name = tap.group(3)
            if tap.group(1):
                block = []
                j = i + 1
                if j < n and lines[j].strip() == "---":
                    while j < n and lines[j].strip() != "...":
                        block.append(lines[j].rstrip())
                        j += 1
                res["tap"]["not_ok"].append((name, block[:40]))
            elif tap.group(4):
                res["tap"]["skipped"].append(name)
            else:
                res["tap"]["ok"].append(name)
            i += 1
            continue
        tc = TAP_COUNT_RE.match(t)
        if tc:
            res["tap"]["counts"][tc.group(1)] = int(tc.group(2))
            i += 1
            continue

        # ---- mocha summary lines ----
        ms = MOCHA_SUMMARY_RE.match(t)
        if ms:
            count, word, dur = int(ms.group(1)), ms.group(2), ms.group(3)
            if word == "passing":
                res["passing"] = count
                res["duration"] = dur
            elif word == "failing":
                res["failing"] = count
            else:
                res["pending_n"] = count
            if word == "failing":
                # Consume the failure block up to the end of the section.
                res["failures"] = parse_mocha_failures(lines[i + 1:])
                break
            i += 1
            continue

        # Stop spec parsing once the failing block starts (handled above).
        if SUITE_DURATION_RE.match(t) or not t.strip():
            i += 1
            continue

        # ---- spec lines ----
        timed = MOCHA_PASS_TIMED_RE.search(t)
        if timed:
            seen_timed = True
            res["suites"].setdefault(suite, []).append(timed.group(1))
            i += 1
            continue
        spec = MOCHA_PASS_SPEC_RE.search(t)
        if spec:
            # Spec-reporter duplicate of a timed line; only use it if the section never
            # emits the timed variant (single-reporter runs, e.g. local-agent-runner).
            if not seen_timed and not has_timed_variant(lines):
                res["suites"].setdefault(suite, []).append(spec.group(1))
            i += 1
            continue
        pend = MOCHA_PENDING_RE.match(t)
        if pend and (fail_idx is None or i < fail_idx):
            res["pending"].append((suite, pend.group(1)))
            i += 1
            continue

        # A non-indented-by-4+ title line sets the suite name. With mocha-multi-reporters the
        # *last* 2-space title before a block of tests is the full (joined) suite title.
        indent = len(t) - len(t.lstrip())
        if indent == 2 and not t.strip().startswith(("#", "ok ", "not ok", "---", "...")):
            suite = t.strip()
        i += 1

    return res


_timed_cache = {}


def has_timed_variant(lines):
    key = id(lines)
    if key not in _timed_cache:
        _timed_cache[key] = any(MOCHA_PASS_TIMED_RE.search(t) for t in lines)
    return _timed_cache[key]


def parse_mocha_failures(lines, max_lines=30):
    """Parse the body of a mocha `N failing` block into [(title, [lines])], de-duplicated."""
    blocks = []
    cur = None
    for t in lines:
        m = MOCHA_FAIL_START_RE.match(t)
        if m:
            cur = [m.group(2).strip()]
            blocks.append(cur)
            continue
        if cur is None:
            continue
        if STACK_NOISE_RE.search(t) and t.strip().startswith("at "):
            continue
        if t.strip():
            cur.append(t.rstrip())
    out, seen = [], set()
    for b in blocks:
        key = "\n".join(b)
        if key in seen:
            continue
        seen.add(key)
        out.append((b[0], b[1:max_lines + 1]))
    return out


def parse_jest(section):
    res = {
        "passed": [], "failed": [], "totals": OrderedDict(), "thresholds": [],
        "failures": OrderedDict(), "coverage": [], "coverage_all": None,
    }
    lines = [t for _, t in section.lines]
    n = len(lines)
    cov_dir = ""
    i = 0
    while i < n:
        t = lines[i]

        fm = JEST_FILE_RE.match(t)
        if fm:
            (res["passed"] if fm.group(1) == "PASS" else res["failed"]).append(fm.group(2))
            i += 1
            continue

        tm = JEST_TOTALS_RE.match(t)
        if tm:
            res["totals"][tm.group(1)] = tm.group(2).strip()
            i += 1
            continue

        if JEST_THRESHOLD_RE.match(t):
            res["thresholds"].append(t.strip())
            i += 1
            continue

        cm = COV_ROW_RE.match(t)
        if cm and not COV_HEADER_RE.match(t):
            indent, name, st, br, fn, ln, unc = cm.groups()
            vals = tuple(float(x) for x in (st, br, fn, ln))
            if name == "All files":
                res["coverage_all"] = vals
            elif len(indent) <= 1:  # directory row
                cov_dir = name
            else:
                res["coverage"].append({
                    "path": f"{cov_dir}/{name}" if cov_dir else name,
                    "stmts": vals[0], "branch": vals[1], "funcs": vals[2], "lines": vals[3],
                    "uncovered": unc,
                })
            i += 1
            continue

        bm = JEST_BULLET_RE.match(t)
        if bm:
            title = bm.group(1).strip()
            body = []
            j = i + 1
            while j < n:
                u = lines[j]
                if (JEST_BULLET_RE.match(u) or JEST_FILE_RE.match(u) or JEST_TOTALS_RE.match(u)
                        or COV_ROW_RE.match(u) or u.startswith("Summary of all failing")
                        or u.startswith("-----")):
                    break
                body.append(u.rstrip())
                j += 1
            if not title.startswith("Console") and not title.startswith("Test Suites"):
                prev = res["failures"].get(title)
                # Jest prints each failure twice (inline and in the summary); keep the longer.
                if prev is None or len(body) > len(prev):
                    res["failures"][title] = body
            i = j
            continue
        i += 1

    # Trim failure bodies: drop leading/trailing blanks, node_modules frames, cap length.
    for title, body in list(res["failures"].items()):
        body = [b for b in body if not (STACK_NOISE_RE.search(b) and b.strip().startswith("at "))]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        res["failures"][title] = body[:40]
    return res


def parse_log(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        raw = [clean(line) for line in fh]

    entries = [split_level(l) for l in raw]
    info = {
        "lines": len(raw),
        "build_status": None, "jenkins_result": None, "total_time": None,
        "pr": None, "branch": None, "title": None, "build_number": None, "build_url": None,
        "maven_errors": [], "pipeline_errors": [],
    }

    for level, text in entries:
        if text.startswith("BUILD SUCCESS") or text.startswith("BUILD FAILURE"):
            info["build_status"] = text.strip()
        elif text.startswith("Finished: "):
            info["jenkins_result"] = text.split(":", 1)[1].strip()
        elif text.startswith("Total time:"):
            info["total_time"] = text.split(":", 1)[1].strip()
        elif text.startswith("CHANGE_BRANCH="):
            info["branch"] = text.split("=", 1)[1]
        elif text.startswith("CHANGE_TITLE="):
            info["title"] = text.split("=", 1)[1]
        elif text.startswith("BUILD_NUMBER="):
            info["build_number"] = text.split("=", 1)[1]
        elif text.startswith("CHANGE_ID="):
            info["pr"] = text.split("=", 1)[1]
        elif level == "ERROR" and not MAVEN_ERROR_NOISE_RE.search(text):
            if text not in info["maven_errors"]:
                info["maven_errors"].append(text.strip())

    sections = split_sections(entries)
    runs = []
    seen_tsc = set()
    other_problems = []  # tsc / prettier
    for sec in sections:
        if sec.kind == "mocha":
            runs.append(("mocha", sec, parse_mocha(sec)))
        elif sec.kind == "jest":
            runs.append(("jest", sec, parse_jest(sec)))
        elif sec.kind == "prettier":
            warns = [t for _, t in sec.lines if t.startswith("[warn]") or "Code style issues" in t]
            ok = any("All matched files use Prettier" in t for _, t in sec.lines)
            runs.append(("prettier", sec, {"ok": ok, "warnings": warns}))
        elif sec.kind == "tsc":
            errs = [t for _, t in sec.lines if TS_ERROR_RE.search(t)]
            key = (sec.label, tuple(errs))
            if key not in seen_tsc:  # build:ts runs twice in CI; report it once
                seen_tsc.add(key)
                runs.append(("tsc", sec, {"errors": errs}))
        # Any section: pick up pnpm/npm failures
        for _, t in sec.lines:
            if re.search(r"ELIFECYCLE|ERR_PNPM|Command failed with exit code", t) and t.strip() not in other_problems:
                other_problems.append(t.strip())
    info["pipeline_errors"] = other_problems
    return info, runs


# --------------------------------------------------------------------------------------
# Formatting
# --------------------------------------------------------------------------------------

def one_line(s, limit=110):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 3] + "..."


def mocha_totals(res):
    tap = res["tap"]["counts"]
    tap_pass = tap.get("pass", len(res["tap"]["ok"]))
    tap_fail = tap.get("fail", len(res["tap"]["not_ok"]))
    tap_skip = tap.get("skipped", len(res["tap"]["skipped"]))
    spec_pass = res["passing"] if res["passing"] is not None else sum(len(v) for v in res["suites"].values())
    spec_fail = res["failing"] or 0
    spec_skip = res["pending_n"] or len(res["pending"])
    return (spec_pass, spec_fail, spec_skip), (tap_pass, tap_fail, tap_skip)


def has_failures(kind, res, sec=None):
    if kind == "mocha":
        return bool(res["failures"] or res["failing"] or res["tap"]["not_ok"])
    if kind == "jest":
        return bool(res["failed"] or res["failures"] or res["thresholds"])
    if kind == "prettier":
        return bool(res["warnings"]) and not res["ok"]
    if kind == "tsc":
        return bool(res["errors"])
    return False


def group_files_by_dir(paths):
    groups = defaultdict(list)
    for p in paths:
        d, _, f = p.rpartition("/")
        groups[d].append(re.sub(r"\.test\.[jt]sx?$", "", f))
    return groups


def render(info, runs, args, src_path, src_bytes):
    out = []
    A = out.append

    A("# Unit Test Results Digest")
    A("")
    A(f"- **Source:** `{os.path.basename(src_path)}` ({info['lines']:,} lines, {src_bytes / 1024:.0f} KB)")
    verdict = info["jenkins_result"] or "UNKNOWN"
    maven = info["build_status"] or "UNKNOWN"
    A(f"- **Build:** Jenkins {verdict} / Maven {maven}" + (f" / {info['total_time']}" if info["total_time"] else ""))
    ctx = []
    if info["pr"]:
        ctx.append(f"PR #{info['pr']}")
    if info["build_number"]:
        ctx.append(f"build #{info['build_number']}")
    if info["branch"]:
        ctx.append(f"branch `{info['branch']}`")
    if ctx:
        A("- **Context:** " + ", ".join(ctx))
    if info["title"]:
        A(f"- **Change:** {info['title']}")
    A("")

    # ---------- summary table ----------
    A("## Run Summary")
    A("")
    A("| Runner | Script | Passed | Failed | Skipped | Notes |")
    A("|---|---|---:|---:|---:|---|")
    total_failed = 0
    for kind, sec, res in runs:
        if kind == "mocha":
            (sp, sf, ss), (tp, tf, ts) = mocha_totals(res)
            note = f"{res['duration']}" if res["duration"] else ""
            if sp or sf or ss:
                A(f"| Mocha | `{sec.label}` | {sp} | {sf} | {ss} | {note} |")
                total_failed += sf
            if tp or tf or ts:
                A(f"| node:test (TAP) | `{sec.label}` | {tp} | {tf} | {ts} | |")
                total_failed += tf
        elif kind == "jest":
            t = res["totals"]
            tests = t.get("Tests", "")
            m = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|skipped|total)", tests)}
            f = m.get("failed", 0)
            total_failed += f
            A(f"| Jest | `{sec.label}` | {m.get('passed', len(res['passed']))} | {f} | {m.get('skipped', 0)} | "
              f"suites: {t.get('Test Suites', '?')}; time: {t.get('Time', '?')} |")
        elif kind == "prettier":
            nfiles = len([w for w in res["warnings"] if "Code style issues" not in w])
            A(f"| Prettier | `{sec.label}` | {'ok' if res['ok'] else '-'} | {nfiles} | - | format check |")
        elif kind == "tsc":
            A(f"| tsc | `{sec.label}` | {'ok' if not res['errors'] else '-'} | {len(res['errors'])} | - | type check |")
    A("")

    # ---------- failures ----------
    any_fail = any(has_failures(k, r) for k, _, r in runs) or info["maven_errors"] or info["pipeline_errors"]
    A("## Failures")
    A("")
    if not any_fail:
        A("None. Every test passed and no threshold, format or type errors were reported.")
        A("")
    for kind, sec, res in runs:
        if not has_failures(kind, res):
            continue
        A(f"### {kind} (`{sec.label}`)")
        A("")
        if kind == "mocha":
            for title, body in res["failures"]:
                A(f"**{title}**")
                A("```text")
                A("\n".join(body) if body else "(no detail captured)")
                A("```")
            for name, block in res["tap"]["not_ok"]:
                A(f"**TAP not ok: {name}**")
                A("```text")
                A("\n".join(block) if block else "(no detail captured)")
                A("```")
        elif kind == "jest":
            for f in OrderedDict.fromkeys(res["failed"]):  # Jest prints FAIL twice (inline + summary)
                A(f"- FAIL `{f}`")
            for t in res["thresholds"]:
                A(f"- {t}")
            for title, body in res["failures"].items():
                A("")
                A(f"**● {title}**")
                A("```text")
                A("\n".join(body) if body else "(no detail captured)")
                A("```")
        elif kind == "prettier":
            for w in res["warnings"]:
                A(f"- {w}")
        elif kind == "tsc":
            for e in res["errors"][:60]:
                A(f"- {e}")
        A("")
    if info["maven_errors"]:
        A("### Maven / pipeline errors")
        A("```text")
        A("\n".join(one_line(e, 300) for e in info["maven_errors"][:20]))
        A("```")
        A("")
    if info["pipeline_errors"]:
        A("### pnpm / npm errors")
        A("```text")
        A("\n".join(info["pipeline_errors"][:10]))
        A("```")
        A("")

    # ---------- coverage ----------
    for kind, sec, res in runs:
        if kind != "jest" or not res["coverage"]:
            continue
        A("## Coverage (Jest)")
        A("")
        if res["coverage_all"]:
            s, b, f, l = res["coverage_all"]
            A(f"**All files:** statements {s}%, branches {b}%, functions {f}%, lines {l}%  ")
            A(f"({len(res['coverage'])} files measured)")
        A("")
        thr = args.cov_below
        cov = res["coverage"]
        zero = [c for c in cov if c["stmts"] == 0 and c["branch"] == 0 and c["funcs"] == 0 and c["lines"] == 0]
        low = [c for c in cov if c not in zero and min(c["stmts"], c["branch"], c["funcs"], c["lines"]) < thr]
        low.sort(key=lambda c: (c["stmts"], c["branch"], c["path"]))
        A(f"### Files below {thr}% on any metric ({len(low)})")
        A("")
        if low:
            A("| File | Stmts | Branch | Funcs | Lines | Uncovered lines |")
            A("|---|---:|---:|---:|---:|---|")
            for c in low:
                unc = one_line(c["uncovered"], args.max_uncovered) if c["uncovered"] else ""
                A(f"| `{c['path']}` | {c['stmts']} | {c['branch']} | {c['funcs']} | {c['lines']} | {unc} |")
        else:
            A("None.")
        A("")
        if zero:
            A(f"### Files with zero coverage ({len(zero)})")
            A("")
            for c in zero:
                A(f"- `{c['path']}`")
            A("")

    # ---------- passing tests ----------
    if args.passed != "none":
        A("## Passing Tests")
        A("")
        for kind, sec, res in runs:
            if kind == "mocha":
                total = sum(len(v) for v in res["suites"].values())
                if total:
                    A(f"### Mocha (`{sec.label}`): {total} passing across {len(res['suites'])} suites")
                    A("")
                    for suite, names in res["suites"].items():
                        A(f"- **{suite}** ({len(names)})")
                        if args.passed == "names":
                            for nm in names:
                                A(f"  - {one_line(nm, 160)}")
                    A("")
                if res["pending"]:
                    A(f"Skipped / pending ({len(res['pending'])}):")
                    for suite, nm in res["pending"]:
                        A(f"- {suite}: {one_line(nm, 160)}")
                    A("")
                if res["tap"]["ok"]:
                    A(f"### node:test (TAP): {len(res['tap']['ok'])} passing")
                    A("")
                    if args.passed == "names":
                        for nm in res["tap"]["ok"]:
                            A(f"- {one_line(nm, 160)}")
                        A("")
            elif kind == "jest" and res["passed"]:
                groups = group_files_by_dir(res["passed"])
                A(f"### Jest (`{sec.label}`): {len(res['passed'])} passing test files "
                  f"(Jest prints per-file results only; run with `--verbose` for test names)")
                A("")
                for d in sorted(groups):
                    files = sorted(groups[d])
                    if args.passed == "names":
                        A(f"- `{d}/`: {', '.join(files)}")
                    else:
                        A(f"- `{d}/` ({len(files)})")
                A("")

    # ---------- footer ----------
    A("---")
    A("*Omitted as noise: Jenkins timestamps, git/pipeline output, env dump, pnpm/vendor install, webpack, "
      "SDLC annotation warnings, duplicate reporter lines, per-test timings, console output.*")
    return "\n".join(out) + "\n"


def to_json(info, runs):
    def ser(kind, sec, res):
        d = {"kind": kind, "script": sec.label}
        if kind == "mocha":
            d.update({
                "passing": res["passing"], "failing": res["failing"], "pending": res["pending_n"],
                "suites": res["suites"], "failures": [{"title": t, "detail": b} for t, b in res["failures"]],
                "tap": res["tap"],
            })
        else:
            d.update(res)
        return d
    return json.dumps({"info": info, "runs": [ser(*r) for r in runs]}, indent=2, default=str)


def main():
    ap = argparse.ArgumentParser(description="Condense a Jenkins unit-test log (Mocha/Jest/TAP) for an LLM.")
    ap.add_argument("log_file", nargs="?",
                    default="test/e2e/llm-context/artifacts/unit-test-jenkins-logs/log.txt",
                    help="Path to the Jenkins console log (default: the unit-test-jenkins-logs artifact)")
    ap.add_argument("-o", "--output", help="Output path (default: <log>.unit-results.md next to the log)")
    ap.add_argument("-f", "--format", choices=["md", "json"], default="md")
    ap.add_argument("--passed", choices=["names", "suites", "none"], default="names",
                    help="Detail for passing tests: names (default), suites (counts only), none")
    ap.add_argument("--cov-below", type=float, default=80.0,
                    help="List files with any coverage metric below this percent (default: 80)")
    ap.add_argument("--max-uncovered", type=int, default=90,
                    help="Max characters of the uncovered-lines column (default: 90)")
    ap.add_argument("--stdout", action="store_true", help="Also print the digest to stdout")
    args = ap.parse_args()

    if not os.path.isfile(args.log_file):
        print(f"[ERROR] File not found: {args.log_file}", file=sys.stderr)
        sys.exit(1)

    info, runs = parse_log(args.log_file)
    src_bytes = os.path.getsize(args.log_file)
    content = to_json(info, runs) if args.format == "json" else render(info, runs, args, args.log_file, src_bytes)

    if args.output:
        out_path = args.output
    else:
        p = Path(args.log_file)
        out_path = str(p.parent / f"{p.stem}.unit-results.{args.format}")
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    Path(out_path).write_text(content, encoding="utf-8")

    out_bytes = os.path.getsize(out_path)
    print("Extracted unit test results.", file=sys.stderr)
    print(f"  Input:  {args.log_file} ({info['lines']:,} lines, {src_bytes / 1024:.0f} KB)", file=sys.stderr)
    print(f"  Output: {out_path} ({len(content.splitlines()):,} lines, {out_bytes / 1024:.0f} KB)", file=sys.stderr)
    print(f"  Reduced: {(1 - out_bytes / src_bytes) * 100:.1f}% (~{out_bytes // 4:,} tokens est.)", file=sys.stderr)
    if args.stdout:
        print(content)


if __name__ == "__main__":
    main()
