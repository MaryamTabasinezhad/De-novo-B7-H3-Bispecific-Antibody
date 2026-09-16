---
name: clinicaltrials-landscape
description: "Map a bounded, disease-centric set of ClinicalTrials.gov records by condition, purpose, intervention type, phase, status, or sponsor. Use for auditable registered-trial landscapes; not for exhaustive asset, company-pipeline, or commercial-development inventories."
metadata:
  short-description: "Map a bounded ClinicalTrials.gov landscape"
  source: "Biomni Lab"
  source-skill-id: "skill_7d39cb6745524d1d9e4493c12c265a4a"
  adaptation-stage: "portable-instruction-layer"
---

# Clinical Trials Landscape

Retrieve, classify, and summarize a reproducible set of ClinicalTrials.gov records with explicit query coverage.

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

- Registry status is not proof of current asset development or clinical efficacy.
- Do not infer commercial ownership or pipeline status beyond registry fields.
- Report query terms, filters, retrieval date, pagination, and coverage limits.

## Portable workflow

1. Clarify condition, intervention, study purpose, status, phase, sponsor, and date boundaries.
2. Discover live API access or a supplied offline export and record the mode used.
3. Retrieve all pages within the declared scope and preserve raw normalized records.
4. Classify mechanisms and study purposes with auditable rules and unresolved categories.
5. Generate summary tables and deterministic figures from the frozen record set.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- trial-level dataset
- coverage record
- classification table
- landscape summary

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
