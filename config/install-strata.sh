#!/usr/bin/env bash
# Install the Strata Terminal (Linux). Tested with Strata 0.2.7.
set -e
curl -fsSL https://github.com/Niko1221/Strata/releases/latest/download/install.sh -o install.sh
sh install.sh
export PATH="$HOME/.local/bin:$PATH"
strata --version
# The DeepSeek engine ships for CUDA 13: you need NVIDIA driver 580 or newer.
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
