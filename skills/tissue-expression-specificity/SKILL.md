---
name: tissue-expression-specificity
description: "Assess where a human target is expressed and identify expression-based on-target safety liabilities using normal-tissue RNA and protein atlases. Use for tissue specificity, vital-organ exposure, and cross-atlas concordance questions."
metadata:
  short-description: "Assess tissue expression and on-target safety"
  source: "Biomni Lab"
  source-skill-id: "skill_6555e1f8055e4a49bcc909a8fd84b635"
  adaptation-stage: "portable-instruction-layer"
---

# Tissue Expression Specificity

Resolve the target, compare available normal-tissue atlases, quantify specificity, and surface organ-level liabilities with source provenance.

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

- RNA expression alone is not proof of cell-surface protein abundance.
- Do not compare atlas values as if their measurement scales were identical.
- Flag missing tissues, version differences, and discordant RNA/protein evidence.

## Portable workflow

1. Resolve gene, Ensembl, or UniProt identifiers.
2. Discover local GTEx/HPA resources or permitted live access and record release versions.
3. Load and normalize each atlas without erasing source-specific measurement semantics.
4. Compute specificity and cross-atlas summaries and inspect vital-organ expression.
5. Ground biological interpretation in retrievable literature where needed.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- tissue expression table
- specificity metrics
- cross-atlas comparison
- on-target safety flags

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
