---
name: methods-landscape-review
description: "Compare computational methods, tools, algorithms, or analytical approaches using published benchmarks. Use to produce a method matrix, benchmark catalog, performance scorecard, and regime-specific recommendation."
metadata:
  short-description: "Compare computational methods using published benchmarks"
  source: "Biomni Lab"
  source-skill-id: "skill_5c16bd4ae5fc49b199405080a847165e"
  adaptation-stage: "portable-instruction-layer"
---

# Methods Landscape Review

Build an evidence-grounded comparison that distinguishes task regime, dataset, metric, compute cost, licensing, and implementation maturity.

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

- Do not compare headline metrics measured on incompatible datasets or splits.
- Do not treat popularity as benchmark superiority.
- Separate published performance from local runtime availability.

## Portable workflow

1. Define the computational task, regimes, candidate families, metrics, and constraints.
2. Search benchmark papers and authoritative method documentation with recency and citation-bias controls.
3. Extract comparable evidence into a normalized benchmark catalog.
4. Score methods by regime and expose missing, incompatible, or weak comparisons.
5. Inventory locally available implementations only after the literature comparison is stable.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- method comparison matrix
- benchmark catalog
- performance scorecard
- regime-specific recommendation

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
