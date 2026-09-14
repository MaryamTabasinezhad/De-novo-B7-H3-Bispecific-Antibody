---
name: cell-surface-antigen-discovery
description: "Discover and rank tumor-selective, antibody-accessible cell-surface antigens for ADC, CAR-T, bispecific, engager, or radioligand programs. Use when expression, topology, normal-tissue safety, and modality tractability must be evaluated together."
metadata:
  short-description: "Rank tumor-selective antibody-accessible antigens"
  source: "Biomni Lab"
  source-skill-id: "skill_522578a78cb54c8fa5d7eb3fdcd7e09b"
  adaptation-stage: "portable-instruction-layer"
---

# Cell-Surface Antigen Discovery

Integrate tumor expression, extracellular topology, normal-tissue expression, and modality-specific constraints into an auditable antigen ranking.

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

- Do not substitute gene essentiality for cell-surface accessibility or tumor selectivity.
- Do not infer antibody accessibility from RNA expression alone.
- Keep known positive controls in the analysis when they are available.

## Portable workflow

1. Clarify tumor type, modality, input data, cell labels, and antigen search breadth.
2. Discover available single-cell, surfaceome, topology, and normal-tissue resources and freeze their versions.
3. Quantify malignant-compartment specificity, apply topology gates, and assess normal-tissue liabilities.
4. Score candidates transparently, run sensitivity checks, and attach source-grounded evidence to leading candidates.
5. Separate validated antigens, plausible novel candidates, and candidates limited by missing evidence.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- ranked antigen table
- normal-tissue safety table
- topology evidence
- analysis manifest

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
