---
name: binder-antibody-design
description: "Design de novo protein binders, antibodies, nanobodies, scFv, or VHH against a structured target using RFdiffusion or RFantibody, ProteinMPNN, structure validation, interface analysis, and candidate ranking. Use for new binder generation from a defined target and epitope."
metadata:
  short-description: "Design protein binders and antibodies against structures"
  source: "Biomni Lab"
  source-skill-id: "skill_5c0f0561b5724ede838bd08b047af399"
  adaptation-stage: "portable-instruction-layer"
---

# Binder and Antibody Design

Run a staged, reproducible binder campaign that preserves target numbering, design-anchor provenance, sequence diversity, independent validation, and honest confidence interpretation.

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

- Do not begin production design until target structure, chain mapping, epitope, and design anchors are explicit.
- Predicted interface confidence is not measured binding affinity.
- Do not use upstream container paths or command flags until they are verified against the target installation.

## Portable workflow

1. Freeze the target structure, canonical numbering map, epitope, design anchors, framework, and design scope.
2. Discover the scheduler, containers, model weights, command interfaces, quotas, and supported GPU types.
3. Adapt and smoke-test a small backbone-generation job from the upstream examples.
4. Design sequences only at allowed positions, then filter liabilities while preserving diversity and provenance.
5. Repredict complexes independently, analyze interfaces, and rank candidates using staged hard gates and calibrated scores.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- design manifest
- backbone and sequence candidates
- prediction and interface metrics
- ranked candidate scorecard

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
