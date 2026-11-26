# 02_04 — GPT-6 compute-node access preflight

Submitted two independent CPU diagnostics on Rorqual using
`-A def-ghaedi_cpu -p cpubase_bycore_b1`. Job stdout/stderr was captured in
`work/02_04_gpt6_preflight/<job-id>.log`. No parent sequence data was used.

| Slurm job | Task | Result |
|---|---|---|
| 27671411 | Check Codex login status and HTTPS reachability of the model API | ChatGPT login recognized. curl returned HTTP 000 and timed out, exit 28. |
| 27671419 | Try headless Codex with a harmless prompt and explicit GPT-6 selection | Model metadata refresh timed out. No model response was verified. The outer timeout ended the process with exit 124. |

Commands inside the allocations, after sourcing `config/hpc/rorqual.sh`:

```bash
codex login status
curl -sS -o /dev/null -w "HTTP %{http_code}\n" --connect-timeout 8 --max-time 12 https://api.openai.com/v1/models
```

```bash
cd /tmp
timeout 45 codex exec --skip-git-repo-check --sandbox read-only -m gpt-6 \
  "Reply with READY only. Do not access files or call tools."
```

The two probes did not establish a working compute-node route to GPT-6.
The redesign arrays were not submitted. Reference-chain reconciliation and
numbered parent coverage also remain release gates.
