# DeepSeek V4.1 Flash (763B) on a 12GB GPU: Strata, real numbers

![GPU](https://img.shields.io/badge/Tested%20on-RTX%205070%2012GB-76b900?style=for-the-badge&logo=nvidia&logoColor=white)
![Model](https://img.shields.io/badge/Model-DeepSeek%20V4.1%20Flash%20763B-4f46e5?style=for-the-badge)
![Quant](https://img.shields.io/badge/Quant-2--bit%20GSQ%20%2B%20RCO%20(138%20GB)-0ea5e9?style=for-the-badge)
![Engine](https://img.shields.io/badge/Engine-Strata%200.2.7-000000?style=for-the-badge)
![RAM](https://img.shields.io/badge/RAM-62%20GB-f59e0b?style=for-the-badge)
![Cloud](https://img.shields.io/badge/Cloud-Not%20Required-red?style=for-the-badge)
![API](https://img.shields.io/badge/API-OpenAI%20Compatible-black?style=for-the-badge)

Run **DeepSeek V4.1 Flash**, a 763B mixture-of-experts model, on one **12 GB gaming graphics card** with **Strata**. The graphics card, system RAM and the SSD work together: the experts used most stay in memory, and the rest are read from the SSD when a word needs them.

This repo has the exact **commands**, the **test script** with its graders, the **bug-fix script**, every **model output** (the games, the SVG, the vision rebuild), the **fixed files**, and the **raw logs** from the video, including a per-second log of VRAM, RAM and SSD reads.

[![Subscribe](https://img.shields.io/badge/Subscribe-NetworkCoder-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@NetworkCoder?sub_confirmation=1)

⭐ If this helped, **star the repo** so more people can find it.

## Results

| Level | Test | Result |
|:---:|---|---|
| 1 | Speed, short answers (same prompt 3×) | **10.45 → 11.63 → 11.34 tok/s** · first word 1.75 s cold, 0.16 s warm |
| 1 | Speed, long answers (2.5K–8.4K tokens of code) | **~9–10 tok/s** |
| 1 | Faster mode (default, 5 of 6 experts) vs Full quality (6 of 6) | **10.5–11.6** vs **8.7–9.2 tok/s** (about 20% quicker) |
| 2 | Long memory: secret code in a 5,723-token and a 22,804-token document | **2 / 2 found** · first word after **15.8 s** and **41.4 s** |
| 3 | AIME 2025 + three AIME 2024 problems (thinking on) | **4 / 4** (70, 204, 25, 73) |
| 3 | Small traps: n! with 25 zeros · letter count · LRU cache (hidden tests) | **105 ✓ · 6 ✓ · 5/5 ✓** |
| 3 | Hard code: “hardest sudoku” solver · expression parser (hidden tests) | **✗ · ✗** (returned an unfinished grid with empty cells · `-2^2` gave `+4`, `"3 4"` gave `34`) |
| 4 | Builds from one prompt: SVG poster · canvas lighthouse · 3D solar system · chess engine · 3D action game | **5 / 5 ran** · chess and the 3D game had **one fatal bug each** (chess also showed both armies in one colour) |
| 4 | Fix round: own code back + one plain sentence per bug | **both fixed in one try** (chess 8.1 min, game 4.7 min) |
| 5 | Vision: read a bar chart + trick question · rebuild a dashboard screenshot | **chart perfect (March ✓)** · dashboard nearly perfect (two headings run together) |
| 5 | One paragraph in Hindi, Marathi, Czech, French | all readable · **one Czech grammar slip** |

> Small sample, one machine. Treat these as a real-world check, not a benchmark.

## Hardware

| Spec | |
|---|---|
| GPU | RTX 5070 · 12 GB · driver 615 (CUDA 13) |
| CPU | Intel Core i5-11600KF · 6 cores |
| System RAM | 62 GB |
| Drive | NVMe SSD · 300 GB free |
| Model | DeepSeek V4.1 Flash · IST-DAS 2.00 bpw set (GSQ + RCO) |
| Download | 257 GB = 138 GB model + 111 GB n-gram table + 8 GB drafter |
| Context | 64K |

### Where the model lives (Strata's own plan)

| Part | Experts | Size |
|---|---|---|
| Graphics card | 828 of 15,360 | ~7 GB |
| CPU, from system RAM | 14,532 | ~125 GB |
| SSD | the experts RAM can't hold | read on demand |

Measured while the model was writing (`logs/monitor.csv`, one row per second): **GPU 11.4 GB at 100%**, **RAM ~46 GB**, **SSD reads ~1–1.5 GB/s**.

### What you need

| | Minimum | Comfortable |
|---|---|---|
| GPU | NVIDIA, 12 GB | — |
| Driver | **580 or newer** (the DeepSeek engine is CUDA 13 only) | — |
| System RAM | 46 GB | 64 GB |
| Disk | **300 GB free on NVMe** | faster NVMe = faster words |

A slow disk makes every word slower: part of the model is read from it for every token.

### The quality cost

2-bit is a compromise. Strata reports about **15.5% worse perplexity** overall and **5–9%** on code and agent work, compared with the original model.

## How 2-bit stays usable

- **RCO** sets a total size budget, measures which parts of the model hurt the output most when squeezed, and gives those parts more bits (and the others fewer).
- **GSQ** decides how each weight is rounded: instead of snapping to the nearest value, it keeps the options open and tunes toward the one that fits the model best.

## Setup

**1. Check the card and driver**
```bash
nvidia-smi        # 12 GB card, driver 580+
free -g && df -h  # RAM and 300 GB free disk
```

**2. Install Strata** ([`config/install-strata.sh`](config/install-strata.sh))
```bash
curl -fsSL https://github.com/Niko1221/Strata/releases/latest/download/install.sh -o install.sh && sh install.sh
export PATH="$HOME/.local/bin:$PATH"
strata --version
```

**3. See the plan first** ([`config/plan.sh`](config/plan.sh)). Nothing downloads yet.
```bash
strata launch --family deepseek41 --model ist-das-2.00bpw --context 64k --plan
```

**4. Download, check and serve** ([`config/launch.sh`](config/launch.sh))
```bash
strata launch --family deepseek41 --model ist-das-2.00bpw \
  --context 64k --vision on --access local --port 8081 --yes --no-tui
```
The first run downloads 257 GB and checks every file. Wait for `Ready: http://127.0.0.1:8081`. The server speaks the OpenAI API at `http://127.0.0.1:8081/v1`, so any app or agent can plug in.

**5. Quick check** ([`config/quick-check.sh`](config/quick-check.sh))
```bash
curl -s http://127.0.0.1:8081/v1/models
```

**6. (Optional) Full quality mode** ([`config/launch-full-quality.sh`](config/launch-full-quality.sh))
```bash
strata launch --stop
strata launch --family deepseek41 --model ist-das-2.00bpw --context 64k --vision on --access local --port 8081 --full-quality --yes --no-tui
```

## Run the same tests

Standard library only, no installs. Safe to re-run: finished tests are skipped.
```bash
python3 scripts/monitor.py monitor.csv &            # VRAM / RAM / SSD log, 1 row per second
python3 scripts/run_tests.py --phase main           # speed, long memory, reasoning, builds, vision, languages
python3 scripts/run_tests.py --phase hard2          # 3 AIME 2024 problems + sudoku + parser, hidden tests
# relaunch with --full-quality, then:
python3 scripts/run_tests.py --phase full           # same speed prompt with all 6 experts
python3 scripts/fix_bugs.py                         # give the model its own chess + game code back with the bug reports
```
Results land in `results/` with a `summary.md` table.

## The fix round

The bug reports were one plain sentence each. These are the lines the model changed:

**Chess** — both armies were the same light colour, and the computer picked the best move for *White*:
```diff
+ span.style.color = isWhite(p) ? '#fff' : '#111';
- let bestVal = -Infinity;   …   if (val > bestVal)
+ let bestVal = Infinity;    …   if (val < bestVal)
```
**3D game** — the hit check measured height too, and bullets fly above the enemies:
```diff
- const dist = b.position.distanceTo(e.group.position);
+ const dist = Math.hypot(b.position.x - e.group.position.x, b.position.z - e.group.position.z);
```

## Tips

- **Driver 580+.** On an older driver the DeepSeek engine refuses to install.
- **300 GB on NVMe.** The n-gram table stays on the SSD and is read for every word.
- **Long prompts wait.** It reads prompts at about 350–550 tok/s, so a 23K-token document means ~40 s before the first word. Fine for a document question, slow for a long agent session.
- **Faster mode is the default** on 12 GB cards. Full quality is about 20% slower.
- **Check long, precise code.** It reasons well, but slips on small details in long code.
- **The 3D files** load Three.js from unpkg, so open them with an internet connection.

## Files

| File | What's in it |
|---|---|
| [`config/install-strata.sh`](config/install-strata.sh) | Install the Strata Terminal and check the driver |
| [`config/plan.sh`](config/plan.sh) | Where every part of the model goes, before downloading |
| [`config/launch.sh`](config/launch.sh) | The exact launch used in the video (Faster mode, 64K, vision on) |
| [`config/launch-full-quality.sh`](config/launch-full-quality.sh) | Same, all 6 experts per word |
| [`config/quick-check.sh`](config/quick-check.sh) | Is the server up? One short reply |
| [`scripts/run_tests.py`](scripts/run_tests.py) | All tests with their graders and hidden tests |
| [`scripts/fix_bugs.py`](scripts/fix_bugs.py) | The fix round: own code back + plain-English bug reports |
| [`scripts/monitor.py`](scripts/monitor.py) | Per-second VRAM / RAM / SSD-read logger |
| [`test-images/`](test-images) | The bar chart and the dashboard screenshot used for vision |
| [`results/outputs/`](results/outputs) | Everything the model wrote: SVG, lighthouse, solar system, chess, 3D game, dashboard, code, languages |
| [`results/fixed/`](results/fixed) | The chess game and 3D game after the fix round |
| [`results/summary.md`](results/summary.md) | Every test with first-word time, speed and token counts |
| [`logs/`](logs) | Raw run logs, Strata output, and `monitor.csv` |

## Related

| Video | Repo |
|---|---|
| Flint 40B on an 8GB GPU (llama.cpp + DeepSeek Harness) | [link](https://github.com/network-tocoder/Flint-40B-on-an-8GB-GPU-llama.cpp-DeepSeek-Harness) |
| Run a 125B model on one GPU (Strata + Qwen 3.8 Flash-Next) | [link](https://github.com/network-tocoder/Run-a-125B-AI-Model-on-One-GPU-Strata-Qwen3.8-Flash-Next) |
| Free local AI coding agent — 125B on 16GB (Strata + opencode) | [link](https://github.com/network-tocoder/free-local-ai-coding-agent-125b-on-16gb-gpu-strata-opencode) |
| 125B local AI on a 12GB GPU (Strata + Pi 1.0) | [link](https://github.com/network-tocoder/125B-Local-AI-on-a-12GB-GPU-Strata-Pi-1.0-Coding-Agent) |

## Credits

DeepSeek V4.1 Flash by [DeepSeek](https://www.deepseek.com) · 2-bit GSQ + RCO set by ISTA-DASLab · [Strata](https://github.com/Niko1221/Strata) by Niko1221
