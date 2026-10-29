#!/usr/bin/env python3
"""Give the model its own code back, describe each bug in plain English, ask for the exact lines to change.
Run from the folder that holds results/ (after run_tests.py). Saves results/fix_<name>.txt."""
import json, os, time, urllib.request
URL = "http://127.0.0.1:8081/v1/chat/completions"
BUGS = [
 ("chess", "results/chess_ai.html",
  "I played this chess game you wrote. Two bugs: (1) Black pieces show in the same light colour as White, so you cannot tell the sides apart. "
  "(2) The computer (Black) plays terrible moves, like it is trying to lose. Find the cause of both bugs and give me ONLY the exact lines to "
  "change, as 'OLD:' and 'NEW:' code blocks. Keep it short."),
 ("roguelike", "results/roguelike_3d.html",
  "I played this 3D game you wrote. My bullets fly straight through the enemies and never damage them, so wave 1 can never be cleared. "
  "Find the cause and give me ONLY the exact lines to change, as 'OLD:' and 'NEW:' code blocks. Keep it short."),
]
os.makedirs("results", exist_ok=True)
for name, path, ask in BUGS:
    code = open(path).read()
    body = {"model": "deepseek-v4.1-flash", "max_tokens": 4000, "temperature": 0.6, "stream": False,
            "messages": [{"role": "user", "content": ask + "\n\n```html\n" + code + "\n```"}]}
    t0 = time.time()
    req = urllib.request.Request(URL, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=3600) as r:
        j = json.load(r)
    dt = time.time() - t0
    msg = j["choices"][0]["message"]
    out = ("=== THINKING ===\n" + (msg.get("reasoning_content") or "") + "\n\n=== ANSWER ===\n" + (msg.get("content") or ""))
    open(f"results/fix_{name}.txt", "w").write(out)
    u = j.get("usage", {}); tm = j.get("timings", {})
    row = {"test": f"fix_{name}", "total_s": round(dt, 1), "prompt_tokens": u.get("prompt_tokens"), "gen_tokens": u.get("completion_tokens"),
           "decode_tps": round(tm.get("predicted_per_second", 0), 2), "prefill_tps": round(tm.get("prompt_per_second", 0), 1)}
    open("results/log.jsonl", "a").write(json.dumps(row) + "\n")
    print(row, flush=True)
    print((msg.get("content") or "")[:1500], "\n" + "-" * 60, flush=True)
