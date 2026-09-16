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
