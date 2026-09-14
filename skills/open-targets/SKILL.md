---
name: open-targets
description: "Query and interpret the Open Targets Platform for disease-target associations, evidence rows, drugs, studies, variants, and credible sets. Use when Open Targets is the requested or appropriate primary structured source."
metadata:
  short-description: "Query and interpret Open Targets evidence"
  source: "Biomni Lab"
  source-skill-id: "skill_53ea5bef4333422681930c9edc9f9fcd"
  adaptation-stage: "portable-instruction-layer"
---

# Open Targets

Produce bounded, schema-aware Open Targets results with pagination, release metadata, completeness labels, and provenance.

The user's instructions and the consuming project's rules take precedence over
this skill. Preserve the requested scope and do not infer permission for external
actions, installations, large downloads, or expensive compute.

## Before execution on a new host

Read [references/runtime-discovery.md](references/runtime-discovery.md). Complete
its read-only discovery pass before selecting commands, paths, datasets, models,
or compute resources. The skill must remain usable on a workstation, login node,
scheduled cluster, or other environment without assuming which one is present.

The original source package is retained under
`references/upstream-biomni/`. Read its `UPSTREAM_SKILL.md` and only the supporting
example files relevant to the current task. Treat source-platform tool calls,
mounts, container paths, concurrency limits, and report requirements as examples
to translate after capability discovery. Never execute them verbatim unless the
target environment independently verifies the same interface.

## Scope boundaries

- Do not equate the overall association score with validated therapeutic efficacy.
- Preserve datasource and datatype semantics instead of merging unlike evidence rows.
- Report pagination or retrieval limits whenever the result is not exhaustive.

## Portable workflow

1. Resolve disease, target, drug, study, and variant identifiers as required.
2. Discover whether live API access, cached fixtures, or a local snapshot is available.
3. Record API or snapshot version metadata and apply bounded pagination.
4. Validate returned records against the expected schema and serialize source evidence before interpretation.
5. Create deterministic summaries and figures from the serialized records.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- normalized evidence records
- ranked association table
- coverage metadata
- provenance manifest

Every computational run should record the command or API request, software and
model versions, parameters, random seeds when applicable, input checksums, output
checksums, dataset releases, and important fallbacks. Preserve experimental facts,
source-derived facts, and computational predictions as separate evidence classes.

## Adaptation state

This package supplies a Codex-valid, portable instruction layer and preserved
upstream examples. Host-specific environments, scheduler adapters, dataset paths,
and scientific smoke tests remain intentionally unbound. When the target host has
been inspected, implement wrappers outside `references/upstream-biomni/`, test
them, and only then promote them into an active `scripts/` directory.
