#!/usr/bin/env bash
# Is the server up? Ask for one short reply.
curl -s http://127.0.0.1:8081/v1/models; echo
curl -s http://127.0.0.1:8081/v1/chat/completions -H 'Content-Type: application/json' -d \
 '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"Say hi to my YouTube viewers in one line"}],"max_tokens":40,"reasoning_effort":"none"}'
echo
