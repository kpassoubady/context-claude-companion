#!/usr/bin/env bash
# Stretch only. Generates about 400 KB of routine log noise in bulk/ so a session can reach a 100k-token auto-compact window.
# Reading this folder costs real tokens on your own plan. Run it only if you chose the stretch task.
set -eu
cd "$(dirname "$0")"
mkdir -p bulk
for f in 1 2 3 4; do
  awk -v seed="$f" 'BEGIN{srand(seed); for(i=0;i<1100;i++){printf "2026-10-14T%02d:%02d:%02dZ INFO  worker-%d job=%08x step=%s status=ok duration_ms=%d queue_depth=%d\n", 13+int(i/3600), int(i/60)%60, i%60, 1+(i%6), int(rand()*2^31), (i%3==0?"fetch":(i%3==1?"render":"store")), 20+int(rand()*400), int(rand()*80)}}' > "bulk/worker-$f.log"
done
du -sh bulk
