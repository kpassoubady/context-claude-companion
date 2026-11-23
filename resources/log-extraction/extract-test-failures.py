#!/usr/bin/env python3
"""
extract-test-failures.py

Extracts test failure and error information from large Java / Jenkins build logs
(Maven Surefire/Failsafe, Gradle, JUnit) and produces a compact, LLM-ready summary.
Reduces multi-megabyte log files into a concise report containing:
  - Executive test summary (tests run, failures, errors, skipped)
  - Failure table with test classes, methods, error messages, and file locations
  - Detailed per-test failure breakdown with preceding context logs and stack traces
  - Maven Results summary and reactor / build status
"""

import argparse
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
PREFIX_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?[+-]\d{2}:?\d{2}\s+)?"
    r"(\[\d{2}:\d{2}:\d{2}(?:\.\d+)?\]\s+)?"
    r"(\[(?:ERROR|INFO|WARNING|WARN|DEBUG|TRACE)\]\s+)?"
)

METHOD_FAIL_RE = re.compile(
    r"^([a-zA-Z0-9_$]+)\(([^)]+)\)\s+Time elapsed:\s*([0-9.]+\s*s)?\s*<<<\s*(FAILURE!|ERROR!)"
)
CLASS_FAIL_RE = re.compile(
    r"^Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)"
    r"(?:,\s*Time elapsed:\s*([0-9.]+\s*s))?\s*<<<\s*(FAILURE!|ERROR!)\s*-\s*in\s+([a-zA-Z0-9_$.]+)"
)
GRADLE_FAIL_RE = re.compile(
    r"^([a-zA-Z0-9_$.]+)\s*>\s*([a-zA-Z0-9_$]+)\s*FAILED"
)
TESTS_RUN_SUMMARY_RE = re.compile(
    r"^Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+),\s*Skipped:\s*(\d+)"
)


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE_RE.sub("", text)


def clean_prefix(line: str) -> str:
    cleaned = strip_ansi(line)
    return PREFIX_RE.sub("", cleaned).strip()


def parse_build_log(filepath: str, context_lines: int = 15, max_stack: int = 25):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw_lines = [strip_ansi(line.rstrip("\r\n")) for line in f]

    total_lines = len(raw_lines)
    file_size_bytes = os.path.getsize(filepath)

    failures = []
    class_summaries = []
    results_sections = []
    compilation_errors = []
    reactor_summary_lines = []
    build_status = "UNKNOWN"
    total_time = None
    finished_at = None

    current_goal = None
    goal_changes = []

    in_results_section = False
    current_results_block = []

    in_reactor = False
    in_compilation = False

    for idx, line in enumerate(raw_lines):
        clean = clean_prefix(line)

        # Detect maven goals/phases
        goal_match = re.search(r"--- ([^:]+:[^:]+:[^ ]+)(?:\s+\(([^)]+)\))?\s+@\s+([^\s]+)", line)
        if goal_match:
            plugin = goal_match.group(1)
            exec_id = goal_match.group(2) or "default"
            artifact = goal_match.group(3)
            current_goal = f"{plugin} ({exec_id}) @ {artifact}"
            goal_changes.append((idx, current_goal))

        # Detect compilation errors
        if "COMPILATION ERROR :" in clean:
            in_compilation = True
            compilation_errors.append(clean)
            continue
        if in_compilation:
            if clean.startswith("-------------------------------------------------------------") or clean.startswith("BUILD "):
                in_compilation = False
            elif clean:
                compilation_errors.append(clean)

        # Detect Results section
        if clean == "Results:":
            in_results_section = True
            current_results_block = []
            continue
        if in_results_section:
            if clean.startswith("--- ") or clean.startswith("BUILD ") or clean.startswith("Reactor Summary"):
                in_results_section = False
                if current_results_block:
                    results_sections.append(current_results_block)
                    current_results_block = []
            elif clean.startswith("Tests run:") and ("Failures:" in clean or "Errors:" in clean):
                current_results_block.append(clean)
                results_sections.append(current_results_block)
                current_results_block = []
                in_results_section = False
                continue
            else:
                if clean:
                    current_results_block.append(clean)
                continue

        # Detect Reactor Summary
        if clean.startswith("Reactor Summary for "):
            in_reactor = True
            reactor_summary_lines.append(clean)
            continue
        if in_reactor:
            if clean.startswith("------------------------------------------------------------------------") or clean.startswith("BUILD "):
                in_reactor = False
            else:
                reactor_summary_lines.append(clean)

        # Detect BUILD SUCCESS / FAILURE
        if "BUILD SUCCESS" in clean:
            build_status = "BUILD SUCCESS"
        elif "BUILD FAILURE" in clean:
            build_status = "BUILD FAILURE"

        # Detect Total time and finished at
        if clean.startswith("Total time:"):
            total_time = clean
        elif clean.startswith("Finished at:"):
            finished_at = clean

        # Detect class-level failure header
        m_class = CLASS_FAIL_RE.match(clean)
        if m_class:
            class_summaries.append({
                "line": idx + 1,
                "class": m_class.group(7),
                "runs": int(m_class.group(1)),
                "failures": int(m_class.group(2)),
                "errors": int(m_class.group(3)),
                "skipped": int(m_class.group(4)),
                "elapsed": m_class.group(5) or "",
                "type": m_class.group(6),
                "goal": current_goal
            })
            continue

        # Detect method-level failure
        m_method = METHOD_FAIL_RE.match(clean)
        m_gradle = GRADLE_FAIL_RE.match(clean) if not m_method else None

        if m_method or m_gradle:
            if m_method:
                method_name = m_method.group(1)
                class_name = m_method.group(2)
                elapsed = m_method.group(3) or ""
                fail_type = m_method.group(4)
            else:
                class_name = m_gradle.group(1)
                method_name = m_gradle.group(2)
                elapsed = ""
                fail_type = "FAILURE!"

            simple_class = class_name.split(".")[-1]

            # Collect stack trace lines
            stack_lines = []
            exception_type = "Unknown"
            error_message = ""
            file_location = None

            j = idx + 1
            while j < total_lines:
                raw_next = raw_lines[j]
                clean_next = clean_prefix(raw_next)

                if not clean_next:
                    if stack_lines:
                        break
                elif clean_next.startswith("at ") or clean_next.startswith("Caused by:") or clean_next.startswith("... ") or clean_next.startswith("\tat "):
                    stack_lines.append(clean_next)
                    if not file_location:
                        loc_match = re.search(r"\(([A-Za-z0-9_$.]+\.java:\d+)\)", clean_next)
                        if loc_match:
                            file_location = loc_match.group(1)
                elif any(clean_next.startswith(prefix) for prefix in ["Oct ", "Jan ", "Feb ", "Mar ", "Apr ", "May ", "Jun ", "Jul ", "Aug ", "Sep ", "Nov ", "Dec "]) or \
                     clean_next.startswith("INFO:") or clean_next.startswith("WARNING:") or clean_next.startswith("ERROR:") or \
                     "Running " in clean_next or "<<<" in clean_next or clean_next.startswith("Tests run:"):
                    break
                else:
                    if not stack_lines:
                        stack_lines.append(clean_next)
                        if ":" in clean_next:
                            parts = clean_next.split(":", 1)
                            if "." in parts[0] or "Error" in parts[0] or "Exception" in parts[0]:
                                exception_type = parts[0].strip()
                                error_message = parts[1].strip()
                        else:
                            exception_type = clean_next.strip()
                    else:
                        stack_lines.append(clean_next)

                j += 1
                if len(stack_lines) >= max_stack + 10:
                    break

            if not error_message and stack_lines:
                first_line = stack_lines[0]
                if ":" in first_line:
                    exception_type, error_message = [p.strip() for p in first_line.split(":", 1)]
                else:
                    error_message = first_line

            # Extract preceding context lines for this test method
            context_log = []
            search_start = max(0, idx - 300)
            found_method_log_idx = -1

            for search_idx in range(idx - 1, search_start - 1, -1):
                prev_line = raw_lines[search_idx]
                if "<<<" in prev_line:
                    continue
                if method_name in prev_line:
                    found_method_log_idx = search_idx
                    break

            if found_method_log_idx != -1:
                for k in range(found_method_log_idx, min(total_lines, found_method_log_idx + context_lines)):
                    if "<<<" in raw_lines[k] or k >= idx:
                        break
                    if k > found_method_log_idx and (f"{simple_class} " in raw_lines[k] and method_name not in raw_lines[k]):
                        break
                    context_log.append(raw_lines[k])
            else:
                for k in range(idx - 1, max(0, idx - 7), -1):
                    if "<<<" in raw_lines[k]:
                        break
                    c_line = raw_lines[k].strip()
                    if c_line:
                        context_log.insert(0, raw_lines[k])

            failures.append({
                "line": idx + 1,
                "class": class_name,
                "simple_class": simple_class,
                "method": method_name,
                "elapsed": elapsed,
                "type": fail_type.replace("!", ""),
                "exception_type": exception_type,
                "message": error_message,
                "location": file_location,
                "context": context_log,
                "stack": stack_lines[:max_stack],
                "goal": current_goal
            })

    # Group failures by unique test method
    unique_failures = OrderedDict()
    for f in failures:
        key = f"{f['class']}#{f['method']}"
        if key not in unique_failures:
            unique_failures[key] = {
                "class": f["class"],
                "simple_class": f["simple_class"],
                "method": f["method"],
                "type": f["type"],
                "exception_type": f["exception_type"],
                "message": f["message"],
                "location": f["location"],
                "stack": f["stack"],
                "context": f["context"],
                "runs": [f]
            }
        else:
            unique_failures[key]["runs"].append(f)
            if not unique_failures[key]["location"] and f["location"]:
                unique_failures[key]["location"] = f["location"]
            if not unique_failures[key]["message"] and f["message"]:
                unique_failures[key]["message"] = f["message"]
            if not unique_failures[key]["context"] and f["context"]:
                unique_failures[key]["context"] = f["context"]

    # Try to extract the highest test summary count from results_sections
    overall_stats = {"runs": 0, "failures": 0, "errors": 0, "skipped": 0}
    for sec in results_sections:
        for l in sec:
            m_stat = TESTS_RUN_SUMMARY_RE.search(l)
            if m_stat:
                r = int(m_stat.group(1))
                f_count = int(m_stat.group(2))
                e_count = int(m_stat.group(3))
                s_count = int(m_stat.group(4))
                if r >= overall_stats["runs"]:
                    overall_stats = {
                        "runs": r,
                        "failures": f_count,
                        "errors": e_count,
                        "skipped": s_count
                    }

    return {
        "file_path": filepath,
        "file_name": os.path.basename(filepath),
        "total_lines": total_lines,
        "size_bytes": file_size_bytes,
        "build_status": build_status,
        "total_time": total_time,
        "finished_at": finished_at,
        "overall_stats": overall_stats,
        "results_sections": results_sections,
        "failures": failures,
        "unique_failures": unique_failures,
        "class_summaries": class_summaries,
        "compilation_errors": compilation_errors,
        "reactor_summary": reactor_summary_lines,
    }


def format_markdown_report(data: dict) -> str:
    lines = []
    file_name = data["file_name"]
    file_path = data["file_path"]
    total_lines = data["total_lines"]
    size_mb = data["size_bytes"] / (1024 * 1024)
    stats = data["overall_stats"]
    unique_failures = data["unique_failures"]
    build_status = data["build_status"]

    total_failures_count = stats["failures"] if stats["failures"] else len(unique_failures)
    total_errors_count = stats["errors"]

    lines.append("# Java Test Failure Analysis Report")
    lines.append("")
    lines.append(f"- **Source Log:** `{file_name}`")
    lines.append(f"- **Full Path:** `{file_path}`")
    lines.append(f"- **Original Log Size:** {size_mb:.2f} MB ({total_lines:,} lines)")
    
    status_note = ""
    if build_status == "BUILD SUCCESS" and (len(unique_failures) > 0 or stats["failures"] > 0):
        status_note = " *(Note: `testFailureIgnore` was active; test failures did not halt the build)*"
    lines.append(f"- **Build Status:** **{build_status}**{status_note}")

    if data["total_time"]:
        lines.append(f"- **{data['total_time']}**")
    if data["finished_at"]:
        lines.append(f"- **{data['finished_at']}**")

    lines.append("")
    lines.append("## Executive Test Summary")
    lines.append("")
    lines.append(
        f"- **Total Tests Executed:** {stats['runs']:,}\n"
        f"- **Failures:** {total_failures_count} | **Errors:** {total_errors_count} | **Skipped:** {stats['skipped']}\n"
        f"- **Unique Failing Tests:** {len(unique_failures)} across {len({f['class'] for f in unique_failures.values()})} test classes"
    )
    lines.append("")

    # 1. Quick Summary Table
    lines.append("---")
    lines.append("")
    lines.append("## 1. Failed Tests Overview")
    lines.append("")

    if not unique_failures:
        lines.append("*No individual test failures were detected in this log.*")
        lines.append("")
    else:
        lines.append("| # | Test Class | Method | Type | Summary Message | Code Location | Runs |")
        lines.append("|---|------------|--------|------|-----------------|---------------|------|")

        for idx, (key, item) in enumerate(unique_failures.items(), 1):
            s_class = item["simple_class"]
            method = item["method"]
            f_type = item["type"]
            msg = item["message"] or item["exception_type"]
            msg_clean = re.sub(r"\s+", " ", msg)
            if len(msg_clean) > 80:
                msg_clean = msg_clean[:77] + "..."
            msg_clean = msg_clean.replace("|", "\\|")
            loc = item["location"] or "-"
            run_count = len(item["runs"])
            run_str = f"{run_count}x" if run_count > 1 else "1x"
            lines.append(f"| {idx} | `{s_class}` | `{method}` | {f_type} | {msg_clean} | `{loc}` | {run_str} |")

        lines.append("")

    # 2. Maven Test Results Block (if available)
    if data["results_sections"]:
        lines.append("---")
        lines.append("")
        lines.append("## 2. Maven Surefire / Failsafe Results Summary")
        lines.append("")
        for s_idx, sec in enumerate(data["results_sections"], 1):
            if len(data["results_sections"]) > 1:
                lines.append(f"### Execution Run #{s_idx}")
            lines.append("```text")
            for sec_line in sec:
                lines.append(sec_line)
            lines.append("```")
            lines.append("")

    # 3. Compilation Errors (if any)
    if data["compilation_errors"]:
        lines.append("---")
        lines.append("")
        lines.append("## Compilation / Build Errors")
        lines.append("")
        lines.append("```text")
        for err_line in data["compilation_errors"]:
            lines.append(err_line)
        lines.append("```")
        lines.append("")

    # 4. Detailed Failure Breakdown
    lines.append("---")
    lines.append("")
    lines.append("## 3. Detailed Failure Breakdown")
    lines.append("")

    for idx, (key, item) in enumerate(unique_failures.items(), 1):
        s_class = item["simple_class"]
        full_class = item["class"]
        method = item["method"]
        f_type = item["type"]
        loc = item["location"] or "Unknown"
        run_count = len(item["runs"])

        run_desc = "Single run" if run_count == 1 else f"Failed across {run_count} test executions (consistent failure)"

        lines.append(f"### {idx}. `{s_class}#{method}`")
        lines.append(f"- **Full Class:** `{full_class}`")
        lines.append(f"- **Method:** `{method}`")
        lines.append(f"- **Outcome:** `{f_type}` ({run_desc})")
        if item["exception_type"]:
            lines.append(f"- **Exception:** `{item['exception_type']}`")
        if item["location"]:
            lines.append(f"- **Location:** `{item['location']}`")
        if item["message"]:
            lines.append(f"- **Failure Detail:** {item['message']}")

        # Context lines
        if item["context"]:
            lines.append("")
            lines.append("#### Preceding Execution Logs (Test Steps / DB / API Calls):")
            lines.append("```text")
            for c_line in item["context"]:
                lines.append(c_line)
            lines.append("```")

        # Stack trace
        if item["stack"]:
            lines.append("")
            lines.append("#### Stack Trace:")
            lines.append("```java")
            for s_line in item["stack"]:
                lines.append(s_line)
            lines.append("```")

        lines.append("")

    # 5. Reactor Summary
    if data["reactor_summary"]:
        lines.append("---")
        lines.append("")
        lines.append("## 4. Maven Reactor Summary")
        lines.append("")
        lines.append("```text")
        for r_line in data["reactor_summary"]:
            lines.append(r_line)
        if data["total_time"]:
            lines.append(data["total_time"])
        if data["finished_at"]:
            lines.append(data["finished_at"])
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def format_text_report(data: dict) -> str:
    md_content = format_markdown_report(data)
    text = re.sub(r"^#+\s*", "", md_content, flags=re.MULTILINE)
    text = text.replace("`", "")
    text = re.sub(r"^\*\*(.*?)\*\*", r"\1", text, flags=re.MULTILINE)
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Extract test failure and error details from Java / Jenkins build logs."
    )
    parser.add_argument(
        "log_file",
        nargs="?",
        help="Path to the build log file (e.g. build.20261026-021134.log). If omitted, finds the newest log in default folders."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path for output file. Defaults to <input_stem>.failures.md"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["md", "txt", "json"],
        default="md",
        help="Output format (default: md)"
    )
    parser.add_argument(
        "-c", "--context-lines",
        type=int,
        default=15,
        help="Number of preceding context log lines to capture before each failure (default: 15)"
    )
    parser.add_argument(
        "-s", "--max-stack",
        type=int,
        default=25,
        help="Maximum stack trace lines per failure (default: 25)"
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the report to stdout in addition to saving to disk"
    )

    args = parser.parse_args()

    # Determine input log file
    target_log = args.log_file
    if not target_log:
        candidates = []
        # Priority search directories (shallow scan first)
        priority_dirs = [
            "test/e2e/llm-context/artifacts/build-log",
            os.path.expanduser("~/llm-context/artifacts/build-log"),
        ]
        for p_dir in priority_dirs:
            if os.path.isdir(p_dir):
                for f in os.listdir(p_dir):
                    if f.endswith(".log") and not f.startswith("."):
                        full_p = os.path.join(p_dir, f)
                        candidates.append((os.path.getmtime(full_p), full_p))
                if candidates:
                    break

        if not candidates:
            fallback_dirs = [
                "test/e2e/llm-context/artifacts",
                os.path.expanduser("~/llm-context/artifacts"),
                "."
            ]
            for s_dir in fallback_dirs:
                if os.path.isdir(s_dir):
                    for root, _, files in os.walk(s_dir):
                        for f in files:
                            if f.endswith(".log") and not f.startswith("."):
                                full_p = os.path.join(root, f)
                                candidates.append((os.path.getmtime(full_p), full_p))

        if candidates:
            candidates.sort(reverse=True)
            target_log = candidates[0][1]
            print(f"[INFO] No log file specified. Auto-detected newest log: {target_log}", file=sys.stderr)
        else:
            print("[ERROR] No build log file specified and none found.", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

    if not os.path.isfile(target_log):
        print(f"[ERROR] File not found: {target_log}", file=sys.stderr)
        sys.exit(1)

    # Parse build log
    data = parse_build_log(target_log, context_lines=args.context_lines, max_stack=args.max_stack)

    # Determine output file path
    out_format = args.format
    if args.output:
        out_path = args.output
    else:
        p = Path(target_log)
        ext = f".failures.{out_format}"
        out_path = str(p.parent / f"{p.stem}{ext}")

    # Generate output
    if out_format == "json":
        import json
        output_content = json.dumps(data, indent=2, default=str)
    elif out_format == "txt":
        output_content = format_text_report(data)
    else:
        output_content = format_markdown_report(data)

    # Write output file
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out_f:
        out_f.write(output_content)

    out_size_bytes = os.path.getsize(out_path)
    in_size_bytes = data["size_bytes"]
    reduction = (1 - (out_size_bytes / in_size_bytes)) * 100 if in_size_bytes > 0 else 0

    print(f"Extracted test failures successfully!", file=sys.stderr)
    print(f"  Input Log:     {target_log} ({data['total_lines']:,} lines, {in_size_bytes / 1024 / 1024:.2f} MB)", file=sys.stderr)
    print(f"  Output File:   {out_path} ({len(output_content.splitlines()):,} lines, {out_size_bytes / 1024:.1f} KB)", file=sys.stderr)
    print(f"  Size Reduced:  {reduction:.1f}%", file=sys.stderr)
    print(f"  Unique Failed: {len(data['unique_failures'])} test(s)", file=sys.stderr)

    if args.stdout:
        print(output_content)


if __name__ == "__main__":
    main()
