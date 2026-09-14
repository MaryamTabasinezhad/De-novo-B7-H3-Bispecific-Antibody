---
name: binding-affinity-ml-model
description: "Train and benchmark target-specific small-molecule affinity or potency models from IC50, Ki, or Kd data, then screen compounds with scaffold-split and applicability-domain checks. Use only for small-molecule QSAR or affinity modeling, not antibody or protein-protein binding prediction."
metadata:
  short-description: "Train honest target-specific small-molecule affinity models"
  source: "Biomni Lab"
  source-skill-id: "skill_0c841f13357d45b0ac471169e58a535d"
  adaptation-stage: "portable-instruction-layer"
---

# Small-Molecule Binding Affinity ML

Curate endpoint-consistent compound data, evaluate models with leakage-resistant splits, and restrict screening claims to the validated applicability domain.

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

- Do not use this skill to estimate antibody affinity or protein-protein binding.
- Do not mix IC50, Ki, and Kd values without an explicit justified model.
- Do not silently replace a requested framework or report random-split performance as scaffold generalization.

## Portable workflow

1. Resolve the target and define endpoint, units, assay scope, and modeling objective.
2. Discover accessible ChEMBL or supplied datasets and freeze source versions.
3. Standardize structures, censoring, duplicates, and assay context; pass a data-reality gate.
4. Benchmark suitable models with scaffold and random splits, uncertainty, and applicability-domain checks.
5. Screen external compounds only with the selected validated model and report novelty and domain limitations.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- curated assay dataset
- benchmark results
- model bundle or specification
- screened candidate table

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
