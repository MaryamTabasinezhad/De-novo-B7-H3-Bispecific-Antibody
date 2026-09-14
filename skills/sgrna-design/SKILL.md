---
name: sgrna-design
description: "Find or design CRISPR guide RNAs for knockout, CRISPRi, or CRISPRa with supported nucleases. Prefer experimentally validated guides, then licensed precomputed resources, then transparent rule-based design."
metadata:
  short-description: "Find and rank CRISPR guide RNAs"
  source: "Biomni Lab"
  source-skill-id: "skill_8450f18da5c947caabf0a26d3f262389"
  adaptation-stage: "portable-instruction-layer"
---

# sgRNA Design

Select guides through a tiered evidence strategy with explicit genome build, transcript, nuclease, PAM, off-target method, and licensing provenance.

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

- Do not mix genome builds or transcript coordinates.
- Do not treat an in-silico score as experimental validation.
- Respect commercial-use and material-transfer restrictions of guide resources.

## Portable workflow

1. Resolve organism, genome build, gene or transcript, perturbation mode, nuclease, and delivery constraints.
2. Search bundled and literature-derived validated guides first.
3. Discover whether permitted precomputed design resources are locally available.
4. Use de novo design only when higher-evidence tiers are unavailable and a validated scorer/reference genome exists.
5. Export selected guides with sequence, PAM, coordinates, scores, evidence tier, and provenance.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- ranked guide table
- design and off-target metadata
- resource licensing notes
- selection rationale

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
