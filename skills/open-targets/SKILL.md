---
name: open-targets
description: "Query and interpret the Open Targets Platform for disease-target associations, evidence rows, drugs, studies, variants, and credible sets. Use when Open Targets is the requested or appropriate primary structured source."
metadata:
  short-description: "Query and interpret Open Targets evidence"
  source: "Biomni Lab"
  source-skill-id: "skill_53ea5bef4333422681930c9edc9f9fcd"
  adaptation-stage: "portable-instruction-layer"
---

# Open Targets

Produce bounded, schema-aware Open Targets results with pagination, release metadata, completeness labels, and provenance.

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

- Do not equate the overall association score with validated therapeutic efficacy.
- Preserve datasource and datatype semantics instead of merging unlike evidence rows.
- Report pagination or retrieval limits whenever the result is not exhaustive.

## Portable workflow

1. Resolve disease, target, drug, study, and variant identifiers as required.
2. Discover whether live API access, cached fixtures, or a local snapshot is available.
3. Record API or snapshot version metadata and apply bounded pagination.
4. Validate returned records against the expected schema and serialize source evidence before interpretation.
5. Create deterministic summaries and figures from the serialized records.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- normalized evidence records
- ranked association table
- coverage metadata
- provenance manifest

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
