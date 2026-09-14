---
name: ligand-binding-mode-analysis
description: "Analyze how a small-molecule ligand binds in an experimental or supplied protein-ligand structure, including pocket residues and geometric interactions. Use for observed ligand poses; not protein-protein interfaces, de novo docking, or binding-affinity prediction."
metadata:
  short-description: "Map small-molecule contacts in protein structures"
  source: "Biomni Lab"
  source-skill-id: "skill_ebf89d293f8c49058111727a00675dce"
  adaptation-stage: "portable-instruction-layer"
---

# Ligand Binding-Mode Analysis

Produce a reproducible contact map from a specified structure while separating observed geometry from energetic or affinity claims.

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

- Do not use for antibody-antigen or other protein-protein interfaces.
- Do not present geometric contacts as binding energies.
- Do not invent a pose when no bound ligand structure is available.

## Portable workflow

1. Resolve the structure, ligand identifier, chain scope, interaction depth, and comparison set.
2. Discover installed parsing, protonation, interaction, and rendering tools.
3. Fetch or validate the structure and identify the intended ligand unambiguously.
4. Run a validated interaction engine or documented geometry fallback and label confidence and source.
5. Compare structures only after establishing residue and ligand mappings.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- pocket contact table
- interaction classifications
- cross-structure comparison
- visualization inputs

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
