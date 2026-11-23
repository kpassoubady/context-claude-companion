#!/usr/bin/env bash
# Deterministic check for Lab 3.4. Verifies the written evidence, not the live Claude session.
set -u
cd "$(dirname "$0")"
fail=0
ok()   { echo "PASS  $1"; }
bad()  { echo "FAIL  $1"; fail=1; }

[ -f LAB_LOG.md ] || { echo "FAIL  LAB_LOG.md is missing"; exit 1; }
[ -f HANDOFF.md ] || { echo "FAIL  HANDOFF.md is missing"; exit 1; }

n=$(grep -c 'TODO' LAB_LOG.md)
[ "$n" -eq 0 ] && ok "LAB_LOG.md has no TODO left" || bad "LAB_LOG.md still has $n TODO line(s)"

grep -q 'TODO' HANDOFF.md && bad "HANDOFF.md still has a TODO line" || ok "HANDOFF.md has no TODO left"

grep -qi 'REL-5521' HANDOFF.md      && ok "HANDOFF.md keeps F3 ticket"            || bad "HANDOFF.md is missing the F3 ticket (REL-5521)"
grep -q  '2026-11-20' HANDOFF.md    && ok "HANDOFF.md keeps F3 due date"          || bad "HANDOFF.md is missing the F3 due date (2026-11-20)"
grep -qi 'out of scope\|only change checkout-api\|only.*checkout-api' HANDOFF.md \
                                    && ok "HANDOFF.md keeps F1 constraint"        || bad "HANDOFF.md is missing the F1 constraint (checkout-api only, payment-gw out of scope)"
grep -qi 'reporting' HANDOFF.md && grep -q '37' HANDOFF.md \
                                    && ok "HANDOFF.md keeps F2 rejected approach and reason" || bad "HANDOFF.md is missing F2 (pool size 37 rejected, reporting job reason)"
grep -q 'ERR_POOL_EXHAUSTED_7731' HANDOFF.md && ok "HANDOFF.md names the root-cause error code" || bad "HANDOFF.md is missing ERR_POOL_EXHAUSTED_7731"

git diff --quiet -- incident 2>/dev/null || bad "files in incident/ were modified (they must stay unchanged)"

if [ "$fail" -eq 0 ]; then echo "ALL LAB 3.4 CHECKS PASSED!"; else echo "Some checks failed."; exit 1; fi
