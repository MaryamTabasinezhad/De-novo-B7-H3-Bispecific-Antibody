---
name: antibody-developability-humanization
description: "Assess or humanize existing mAb, Fv, scFv, VHH, or nanobody sequences using antibody numbering, sequence liabilities, humanness, immunogenicity, CDR grafting, and framework back-mutation analysis. Use for existing antibody sequences, not de novo binder generation."
metadata:
  short-description: "Assess and humanize antibody variable regions"
  source: "Biomni Lab"
  source-skill-id: "skill_96d2106323804eb8ad9fe07bd476ff4d"
  adaptation-stage: "portable-instruction-layer"
---

# Antibody Developability and Humanization

Produce numbered, auditable sequence assessments and conservative humanization variants while separating predicted liabilities from measured developability.

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

- Do not change CDRs or structurally important framework residues without explicit rationale.
- Do not claim reduced immunogenicity or improved developability without experimental validation.
- Licensed predictors such as NetMHCIIpan must never be downloaded automatically.

## Portable workflow

1. Ingest and validate chain identity, species, format, and antibody numbering.
2. Discover installed numbering, liability, humanness, and immunogenicity tools and their licenses.
3. Run sequence-liability and biophysical proxy analysis with recorded methods.
4. When humanization is requested, select documented human germlines, graft CDRs, and propose justified framework back-mutations.
5. Reassess every proposed construct and preserve a residue-level change ledger.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- numbered sequence table
- liability assessment
- humanization variants
- change and rationale ledger

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
