---
name: generative-molecule-design
description: "Generate, filter, and rank goal-directed de novo small molecules or scaffold hops using explicit activity, drug-likeness, novelty, synthesizability, and makeability objectives. Use only for small-molecule design, not antibody or protein-binder sequence design."
metadata:
  short-description: "Generate and triage goal-directed small molecules"
  source: "Biomni Lab"
  source-skill-id: "skill_2c67771543d14271bbdda3c903d773f1"
  adaptation-stage: "portable-instruction-layer"
---

# Generative Small-Molecule Design

Run a reproducible multi-objective small-molecule campaign with an explicitly qualified activity backend and honest synthesis limitations.

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

- Do not use for antibody, peptide, or protein binder generation.
- Generated structures are hypotheses and are not synthesized, active, or safe by default.
- Do not substitute an unvalidated generic oracle for target-specific activity.

## Portable workflow

1. Define target, seed chemistry, allowed transformations, objective weights, and forbidden motifs.
2. Discover installed chemistry packages, activity backends, synthesis tools, and model caches.
3. Choose and validate an activity backend before generation.
4. Generate with recorded seeds and parameters, then standardize, deduplicate, filter, and rank molecules.
5. Run retrosynthesis only when a validated local implementation and models are available; otherwise report the proxy used.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- generated molecule table
- objective and filter audit
- novelty analysis
- qualified synthesis assessment

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
