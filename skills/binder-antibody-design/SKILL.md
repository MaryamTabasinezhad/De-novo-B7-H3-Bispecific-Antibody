---
name: binder-antibody-design
description: "Design de novo protein binders, antibodies, nanobodies, scFv, or VHH against a structured target using RFdiffusion or RFantibody, ProteinMPNN, structure validation, interface analysis, and candidate ranking. Use for new binder generation from a defined target and epitope."
metadata:
  short-description: "Design protein binders and antibodies against structures"
  source: "Biomni Lab"
  source-skill-id: "skill_5c0f0561b5724ede838bd08b047af399"
  adaptation-stage: "portable-instruction-layer"
---

# Binder and Antibody Design

Run a staged, reproducible binder campaign that preserves target numbering, design-anchor provenance, sequence diversity, independent validation, and honest confidence interpretation.

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

- Do not begin production design until target structure, chain mapping, epitope, and design anchors are explicit.
- Predicted interface confidence is not measured binding affinity.
- Do not use upstream container paths or command flags until they are verified against the target installation.

## Portable workflow

1. Freeze the target structure, canonical numbering map, epitope, design anchors, framework, and design scope.
2. Discover the scheduler, containers, model weights, command interfaces, quotas, and supported GPU types.
3. Adapt and smoke-test a small backbone-generation job from the upstream examples.
4. Design sequences only at allowed positions, then filter liabilities while preserving diversity and provenance.
5. Repredict complexes independently, analyze interfaces, and rank candidates using staged hard gates and calibrated scores.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- design manifest
- backbone and sequence candidates
- prediction and interface metrics
- ranked candidate scorecard

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
