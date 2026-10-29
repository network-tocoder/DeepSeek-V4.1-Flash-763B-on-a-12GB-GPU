#!/usr/bin/env bash
# Same model, all 6 experts per word (about 20% slower in my test).
strata launch --stop
strata launch --family deepseek41 --model ist-das-2.00bpw \
  --context 64k --vision on --access local --port 8081 \
  --full-quality --yes --no-tui 2>&1 | tee strata_full.log
