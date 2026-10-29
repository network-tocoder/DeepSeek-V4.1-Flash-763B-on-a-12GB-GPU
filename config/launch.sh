#!/usr/bin/env bash
# Download (first run, ~257 GB), check every file, and serve an OpenAI-compatible API on port 8081.
# Default speed on a 12 GB card is "Faster" (5 of 6 experts per word).
strata launch --family deepseek41 --model ist-das-2.00bpw \
  --context 64k --vision on --access local --port 8081 \
  --yes --no-tui 2>&1 | tee strata.log
