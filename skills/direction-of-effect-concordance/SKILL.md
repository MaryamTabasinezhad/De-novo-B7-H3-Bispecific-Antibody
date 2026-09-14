---
name: direction-of-effect-concordance
description: "Assess whether a therapeutic target should be inhibited or activated by reconciling human genetics, functional screens, drug mechanisms, animal phenotypes, and literature. Use for target-directionality decisions and explicit discordance analysis."
metadata:
  short-description: "Decide whether a target should be inhibited or activated"
  source: "Biomni Lab"
  source-skill-id: "skill_b973718932a54ffb8b326f7f157e7036"
  adaptation-stage: "portable-instruction-layer"
---

# Direction-of-Effect Concordance

Build a per-evidence-axis direction matrix and derive a qualified activate, inhibit, mixed, or insufficient-evidence conclusion.

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

- A null loss-of-function phenotype does not by itself support activation.
- Do not hide conflicting evidence or collapse incompatible disease contexts.
- Do not invent directionality when an evidence axis is unavailable.

## Portable workflow

1. Resolve target and disease identifiers and define the therapeutic context.
2. Discover structured genetics, perturbation, drug-mechanism, and phenotype sources available in the environment.
3. Retrieve directional literature and preserve stable citations or record locators.
4. Construct the evidence matrix, apply explicit direction rules, and expose discordance.
5. Assign a confidence tier tied to evidence completeness rather than narrative strength.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- direction evidence matrix
- consensus call
- discordance flags
- citation-verification record

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
