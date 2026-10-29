# Summary — DeepSeek V4.1 Flash 763B · RTX 5070 12 GB · 62 GB RAM · Strata 0.2.7

TTFT = time to the first word. Decode = writing speed. Prefill = reading speed.

| Test | TTFT s | Decode tok/s | Prefill tok/s | Prompt tok | Gen tok | Total s | Result |
|---|---|---|---|---|---|---|---|
| speed_1 | 1.75 | 10.45 | 12.0 | 21 | 163 | 17.3 |  |
| speed_2 | 0.16 | 11.63 | 134.3 | 21 | 200 | 17.4 |  |
| speed_3 | 0.19 | 11.34 | 112.7 | 21 | 165 | 14.7 |  |
| full_quality_speed_1 | 2.08 | 8.71 | 10.1 | 21 | 184 | 23.2 |  |
| full_quality_speed_2 | 0.21 | 9.11 | 101.0 | 21 | 166 | 18.4 |  |
| full_quality_speed_3 | 0.21 | 9.19 | 99.4 | 21 | 218 | 23.9 |  |
| context_8k | 15.75 | 7.8 | 363.5 | 5723 | 6 | 16.5 | recall ✓ |
| context_32k | 41.36 | 11.37 | 551.4 | 22804 | 6 | 41.9 | recall ✓ |
| hard_aime | 4.85 | 7.82 | 13.0 | 63 | 383 | 53.8 | 70 ✓ |
| hard_zeros | 2.68 | 7.65 | 11.6 | 31 | 310 | 43.2 | 105 ✓ |
| hard_letters | 2.64 | 7.96 | 11.4 | 30 | 135 | 19.6 | 6 ✓ |
| hard_code | 6.03 | 7.69 | 10.6 | 64 | 370 | 54.1 | 5/5 hidden ✓ |
| aime24_I_1 | 4.77 | 8.03 | 32.5 | 155 | 686 | 90.3 | 204 ✓ |
| aime24_I_2 | 6.21 | 10.29 | 12.1 | 75 | 1078 | 110.9 | 25 ✓ |
| aime24_II_1 | 4.48 | 9.7 | 30.6 | 137 | 1345 | 143.1 | 73 ✓ |
| code_sudoku | 7.65 | 8.26 | 11.0 | 84 | 899 | 116.5 | ✗ unfinished grid |
| code_calc | 3.96 | 8.68 | 27.2 | 108 | 553 | 67.7 | ✗ -2^2 → 4 |
| svg_poster | 0.24 | 10.02 | 277.1 | 67 | 3729 | 372.5 | ✓ |
| canvas_scene | 0.2 | 9.32 | 326.8 | 65 | 3575 | 383.7 | ✓ |
| threejs_scene | 3.87 | 9.23 | 26.6 | 103 | 2508 | 275.5 | ✓ |
| chess_ai | 0.18 | 9.11 | 619.2 | 110 | 8401 | 922.6 | 1 bug (colours + move choice) |
| roguelike_3d | 5.18 | 9.04 | 29.2 | 151 | 6271 | 698.5 | 1 bug (hit check) |
| vision_chart | 16.1 | 7.7 | 17.5 | 282 | 140 | 34.3 | March ✓ |
| vision_ui | 5.6 | 8.85 | 52.3 | 293 | 1311 | 153.8 | near-perfect |
| multilingual | 5.42 | 7.81 | 10.3 | 56 | 542 | 74.8 | 1 Czech slip |
| fix_chess | — | 7.3 | 274.6 | 8513 | 3318 | 485.5 | both bugs fixed |
| fix_roguelike | — | 7.3 | 261.9 | 6359 | 1860 | 280.2 | hit check fixed |

`full_quality_speed_*` ran after relaunching with `--full-quality` (all 6 experts). Everything else ran in the default Faster mode.
context_8k / context_32k were really 5,723 and 22,804 tokens.
