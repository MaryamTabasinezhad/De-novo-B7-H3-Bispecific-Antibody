---
name: targeted-degrader-design
description: "Design and computationally triage heterobifunctional PROTACs or targeted degraders using target warheads, E3 ligands, linkers, physicochemical filters, docking, and optional ternary modeling. Use for small-molecule degrader programs, not antibody-mediated degradation."
metadata:
  short-description: "Design and triage small-molecule targeted degraders"
  source: "Biomni Lab"
  source-skill-id: "skill_c8d77a80500548a5ad07d8756469814d"
  adaptation-stage: "portable-instruction-layer"
---

# Targeted Degrader Design

Build a transparent degrader design space and rank candidates without overstating degradation, permeability, or ternary-complex predictions.

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

- Do not use for antibody, lysosome-targeting chimera, or protein-binder design unless explicitly adapted.
- A binary warhead binder is not automatically a functional degrader.
- Do not use non-commercial software in a commercial workflow without an appropriate license or substitution.

## Portable workflow

1. Define target, degradation mechanism, cellular context, warhead evidence, and allowed E3 ligases.
2. Discover licensed structure-preparation, chemistry, docking, property, and modeling tools.
3. Validate warhead pose and exit vector before enumerating E3 ligands and linkers.
4. Assemble candidates reproducibly and score physicochemical, permeability, synthesis, and structural criteria.
5. Use ternary-complex modeling only as a qualified optional tier and preserve uncertainty.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- candidate degrader table
- component and linker provenance
- property and docking scorecard
- assumption log

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
