---
name: target-tractability-druggability
description: "Assess whether a human target is tractable and which therapeutic modality is most viable using known drugs, structural evidence, pockets, safety, essentiality, and modality-specific constraints. Use for druggability or modality-selection questions."
metadata:
  short-description: "Assess target tractability across therapeutic modalities"
  source: "Biomni Lab"
  source-skill-id: "skill_8de1ad6db2524087b4588d1c20d65422"
  adaptation-stage: "portable-instruction-layer"
---

# Target Tractability and Druggability

Combine orthogonal evidence into a transparent modality scorecard without treating any single database or pocket predictor as decisive.

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

- Do not assume a structural pocket makes an extracellular antibody target more or less viable.
- Do not silently substitute a predicted structure for an experimental structure.
- Separate target biology, modality feasibility, safety, and evidence quality.

## Portable workflow

1. Resolve the target and intended disease or modality context.
2. Discover available target, drug, safety, essentiality, and structure resources.
3. Retrieve structured tractability evidence and choose the best justified structures.
4. Run pocket analysis only when relevant and when a validated implementation is available.
5. Score modalities transparently and document missing or contradictory evidence.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- modality scorecard
- structure and pocket evidence
- safety and essentiality notes
- decision rationale

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
