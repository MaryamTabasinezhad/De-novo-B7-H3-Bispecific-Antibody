# Task-scoped runtime use

Follow the project's analysis-first contract. Use its existing host notes and
environment file first. For B7-H3 these are `config/hpc/README.md` and
`config/hpc/rorqual.sh` at the repository root. Source the latter in each execution
shell or SLURM script; exports do not persist between unrelated tool calls.

Check only what the current analysis needs:

- Resolve input/output paths and confirm the required executable or Python imports.
- Use recorded module/container choices where applicable. Do not assume that an
  available module, an empty model directory, or a skill installation proves that
  a scientific method can run.
- Use SLURM for substantial compute; choose the CPU/GPU account and resources for
  this job. Query availability when submitting. Never run GPU inference on a login node.
- Record source accession/release or retrieval date, important settings, versions,
  outputs, and job IDs in concise notes. Hashes and formal manifests are optional
  only when they answer a concrete question.
- Reuse relevant upstream examples after checking their imports and command-line
  interface. Preserve the examples; put adaptations in project analysis scripts.
- Keep scientific checks (numbering, chains, units, meaningful controls) relevant
  to the result. No mandatory pytest, generalized adapters, or fixture suites.
- Use real literature/search tools and ordinary Markdown/tables/plots. Biomni
  managed tool IDs, datalake mounts, report services, and execution-trace gates do
  not exist here and must not be fabricated or mechanically emulated.
- Confirm access to a source when it is needed. A login-node network check does
  not establish compute-node egress. Do not download large datasets/model weights
  or install packages merely to complete an inventory.
- If a requested method is missing, report that specific gap. Continue independent
  work and discuss any scientifically different alternative explicitly.

Original sources remain in `references/upstream-biomni/`. Their operational and
reporting contracts do not override these active instructions or project rules.
