#!/usr/bin/env bash
# Show where every part of the model will go (VRAM / RAM / SSD) before downloading anything.
strata launch --family deepseek41 --model ist-das-2.00bpw --context 64k --plan
