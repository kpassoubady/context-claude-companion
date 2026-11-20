#!/usr/bin/env bash
# Create the local git repository the Lab 3.1 audit runs against.
# One baseline commit, then the in-progress edit left behind at the end of the session.
# HANDOFF.md stays untracked so the commit hash does not depend on your notes.
set -euo pipefail
cd "$(dirname "$0")"

if [ -e .git ]; then
  echo ".git already exists here. Run 'rm -rf .git' first to recreate it."
  exit 1
fi

git init -q
git symbolic-ref HEAD refs/heads/main
printf '__pycache__/\n.pytest_cache/\n*.pyc\n' > .git/info/exclude
git add -A -- . ':!HANDOFF.md'

export GIT_AUTHOR_DATE="2026-11-06T09:00:00+00:00" GIT_COMMITTER_DATE="2026-11-06T09:00:00+00:00"
git -c user.name="Lab Setup" -c user.email="lab-setup@example.invalid" -c commit.gpgsign=false \
  commit -q -m "Baseline before the lease renewal fix"

# The unfinished edit from the investigation: a marker comment in lease.py (no-op if already fixed).
python3 - <<'PY'
from pathlib import Path

path = Path("task_queue/lease.py")
text = path.read_text(encoding="utf-8")
marker = '        record["expires_at"] = now_ts + self.default_ttl_seconds\n        return dict(record)\n\n    def get_lease_status'
if "TODO: Verify that" in text and marker in text:
    note = "        # WIP: seq comparison and increment not written yet\n"
    path.write_text(text.replace(marker, note + marker, 1), encoding="utf-8")
PY

echo "Repository ready. Try: git log --oneline && git status --short"
