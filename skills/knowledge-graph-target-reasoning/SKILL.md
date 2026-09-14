---
name: knowledge-graph-target-reasoning
description: "Discover and rank therapeutic targets for a disease using biomedical knowledge graphs, network propagation, and interpretable evidence paths. Use for disease-target nomination or network-based prioritization; account explicitly for dataset provenance and licensing."
metadata:
  short-description: "Rank disease targets using interpretable graph paths"
  source: "Biomni Lab"
  source-skill-id: "skill_c18b5e3fe7db49728f7bfd77e3f4bdd7"
  adaptation-stage: "portable-instruction-layer"
---

# Knowledge-Graph Target Reasoning

Prioritize disease-associated genes or proteins with graph structure while preserving the provenance, license class, and biological meaning of every edge and seed source.

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

- Do not treat graph proximity as causal evidence or proof of tractability.
- Do not mix academic-only and commercial-safe graph layers without labeling the run.
- Do not claim complete graph coverage when required datasets are absent or version-mismatched.

## Portable workflow

1. Resolve the disease identity and define the intended licensing mode.
2. Discover available graph datasets, schemas, versions, and provenance fields before choosing a ranker.
3. Select disease anchors and run a transparent propagation or random-walk method with recorded parameters.
4. Apply face-validity checks, enumerate evidence paths, and validate leading candidates against independent literature or structured sources.
5. Report sensitivity to seeds, graph version, excluded sources, and edge-license filters.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- ranked target table
- interpretable evidence paths
- run manifest
- method and licensing notes

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
