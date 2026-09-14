---
name: clinicaltrials-landscape
description: "Map a bounded, disease-centric set of ClinicalTrials.gov records by condition, purpose, intervention type, phase, status, or sponsor. Use for auditable registered-trial landscapes; not for exhaustive asset, company-pipeline, or commercial-development inventories."
metadata:
  short-description: "Map a bounded ClinicalTrials.gov landscape"
  source: "Biomni Lab"
  source-skill-id: "skill_7d39cb6745524d1d9e4493c12c265a4a"
  adaptation-stage: "portable-instruction-layer"
---

# Clinical Trials Landscape

Retrieve, classify, and summarize a reproducible set of ClinicalTrials.gov records with explicit query coverage.

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

- Registry status is not proof of current asset development or clinical efficacy.
- Do not infer commercial ownership or pipeline status beyond registry fields.
- Report query terms, filters, retrieval date, pagination, and coverage limits.

## Portable workflow

1. Clarify condition, intervention, study purpose, status, phase, sponsor, and date boundaries.
2. Discover live API access or a supplied offline export and record the mode used.
3. Retrieve all pages within the declared scope and preserve raw normalized records.
4. Classify mechanisms and study purposes with auditable rules and unresolved categories.
5. Generate summary tables and deterministic figures from the frozen record set.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- trial-level dataset
- coverage record
- classification table
- landscape summary

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
