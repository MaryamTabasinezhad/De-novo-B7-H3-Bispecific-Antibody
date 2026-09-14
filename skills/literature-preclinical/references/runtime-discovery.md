# Portable Runtime Discovery

Read this file before attempting to execute an upstream workflow on a new host.
The purpose is to bind the scientific method to the environment that actually
exists. Never assume the scheduler, filesystem, network, package manager,
container runtime, accelerator, database layout, or model-weight location.

## 1. Establish safe working paths

Resolve the skill directory from the loaded `SKILL.md`. Resolve the project root
with repository context when available; otherwise use the user's supplied working
directory. Choose and record project-local or user-configured locations for:

- work and temporary files;
- final results;
- input datasets;
- shared caches;
- model weights and large databases.

Pass those locations as command-line arguments or environment variables supported
by the adapted implementation. Do not create or depend on `/mnt/results`,
`/mnt/datalake`, `/mnt/fsx`, `/workspace`, or another source-platform mount.
Do not search an entire shared filesystem when a configured project, module, data
catalog, or administrator-provided path can answer the question.

## 2. Inventory execution capabilities

Use read-only checks first. Determine whether execution is local or scheduled.
Check for scheduler commands such as `sbatch`, `squeue`, `sacct`, `scancel`,
`srun`, `bsub`, or `qsub`; module tooling; and container runtimes such as
Apptainer, Singularity, Docker, or Podman. Inspect accelerators and quotas rather
than inferring them from the hostname. Record the commands and versions found.

If a scientific engine is needed, inspect local modules, containers, executable
help, project configuration, and administrator documentation. Treat commands in
`references/upstream-biomni/` as examples of method inputs and important flags,
not as evidence that a matching executable or path exists.

## 3. Inventory software and dependencies

Inspect the imported scripts and their imports before selecting an environment.
Prefer an existing tested environment or container. If dependencies are missing,
prepare a reproducible environment specification for review; do not improvise an
unversioned installation inside a scientific run. Record software versions,
container digests, model versions, and dependency gaps.

## 4. Inventory data and network access

Determine whether required sources are local datasets, supplied files, cached
artifacts, or live APIs. Record dataset release, schema, license, checksums, and
retrieval date. Test network reachability with a small read-only request before a
large retrieval. If compute nodes lack egress, stage data through the site's
approved transfer mechanism and keep raw inputs immutable.

## 5. Map source-platform concepts

Use the following semantic mapping when reading upstream examples:

| Upstream concept | Portable Codex interpretation |
|---|---|
| managed literature search | available scholarly APIs, web search, or supplied corpus, with an explicit search ledger |
| managed image generation | available image-generation capability or a deterministic data figure; make conceptual art optional |
| managed machines | discovered scheduler jobs, job arrays, or local processes |
| managed HPC tool ID | locally verified executable, module, or container invocation |
| execution-trace reference log | project-owned provenance JSONL or manifest built from real tool results |
| platform results mount | configured results directory inside the current project or approved storage |
| platform datalake | configured local dataset path or a documented live-source retrieval |
| platform report skill | an available Codex document or PDF capability, or a direct Markdown report |

Never fabricate a trace event, tool identifier, job ID, source record, or successful
capability check merely to satisfy an upstream gate.

## 6. Create a host binding outside the upstream examples

When implementation is required, create a project-local adapter or wrapper that:

1. accepts explicit input, output, data, cache, and model paths;
2. invokes only locally verified commands;
3. supports dry-run or command-preview mode;
4. records scheduler job IDs and complete commands;
5. uses bounded waits and reports cancellation or timeout outcomes;
6. writes a run manifest with parameters, versions, seeds, checksums, and outputs.

Keep `references/upstream-biomni/` unchanged so it remains a trustworthy example
and provenance source. Do not promote an adapted wrapper into the skill's active
`scripts/` directory until it has been tested on the target host.

## 7. Scientific fallback rules

If an unavailable method would change the scientific meaning, stop that stage and
record the missing capability. A cheaper or different method may be offered as an
explicit alternative, but never substituted silently. Work that can proceed
without the missing capability may continue, provided outputs state which stages
were not executed. Predictions remain hypotheses until experimentally validated.
