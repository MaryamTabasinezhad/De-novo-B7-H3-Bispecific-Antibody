---
name: protein-structure-prediction
description: "Predict protein or complex structures from sequence using locally available methods such as AlphaFold, Boltz, Chai, or ESM-based folding. Use for structure prediction and confidence analysis; select methods from discovered host capabilities rather than assumed platform services."
metadata:
  short-description: "Predict protein structures with environment-aware methods"
  source: "Biomni Lab"
  source-skill-id: "skill_a2393c9d2df847968e1f4afa92621540"
  adaptation-stage: "portable-instruction-layer"
---

# Protein Structure Prediction

Choose a method appropriate to sequence length and complex type, submit it through the discovered execution environment, and report method-specific confidence without cross-method metric conflation.

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

- Do not run the upstream orchestration script verbatim; it imports platform-specific HPC helpers.
- Do not fold a multi-chain complex through a monomer-only path.
- Do not compare pLDDT, pTM, ipTM, and PAE as interchangeable metrics.

## Portable workflow

1. Resolve sequence, chain stoichiometry, complex type, templates, ligands, and requested method constraints.
2. Discover installed predictors, scheduler interfaces, containers, databases, model weights, caches, and GPU limits.
3. Derive a host-specific command from verified local help or documentation and run a minimal smoke test.
4. Submit bounded jobs with durable manifests, polling or scheduler inspection, timeouts, and cancellation behavior.
5. Extract structures and native confidence fields, then produce per-residue and domain-level summaries.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- PDB or CIF models
- native confidence outputs
- per-residue confidence table
- run and fallback manifest

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
