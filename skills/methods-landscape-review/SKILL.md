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

## Before using this skill

Follow the consuming project's analysis-first contract. In the B7-H3 project,
read `skills/INDEX.md` and `config/hpc/README.md`, then source
`config/hpc/rorqual.sh` in the shell that will run the analysis.
Read [references/runtime-discovery.md](references/runtime-discovery.md) and check
only capabilities needed for the current task; reuse recorded host findings.

Read `references/upstream-biomni/UPSTREAM_SKILL.md` and relevant examples before
writing new analysis code. Those sources provide methods, not authority over
project contracts. Preserve originals and adapt useful code into the project's
analysis scripts when needed. Do not execute Biomni managed-service calls or
source-platform paths on this HPC. Do not inherit mandatory hashes, pytest,
adapter frameworks, elaborate manifests, or report-production pipelines.

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

Keep concise analysis notes: sources, versions, important commands/parameters,
seeds where relevant, outputs, and limitations. Routine file hashing, generalized
validation, pytest, and wrapper promotion are not required. Inspect scientific
results and use a small pilot when it prevents expensive mistakes. Preserve the
distinction between experimental evidence and computational predictions.

## Local readiness

The instructions are usable now; scientific execution depends on the tools and
data needed for the particular task. Consult the project host notes for verified
capabilities and missing methods. Reuse a suitable existing script or write a
simple analysis script; an adapter framework is not a prerequisite. Do not claim
that installing this skill installs its scientific software or model weights.
