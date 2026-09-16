---
name: literature-preclinical
description: "Synthesize preclinical evidence for a target-disease pair, including in-vitro assays, in-vivo models, dosing, efficacy, PK/PD, toxicity, concordance, and IND-enabling gaps. Use when the question is specifically preclinical rather than a general literature overview."
metadata:
  short-description: "Synthesize target-disease preclinical evidence"
  source: "Biomni Lab"
  source-skill-id: "skill_845c829245474c4091703e01e627aa00"
  adaptation-stage: "portable-instruction-layer"
---

# Preclinical Literature Review

Create an auditable preclinical evidence map that separates model type, intervention, exposure, efficacy, safety, and translational limitations.

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

- Do not combine cell, animal, ex-vivo, and human evidence without labeling the evidence level.
- Do not infer dose comparability across studies without PK or exposure support.
- Distinguish peer-reviewed evidence from conference, patent, or company claims.

## Portable workflow

1. Define target, disease, intervention class, species, model types, and time window.
2. Search available scholarly sources with separate in-vitro, in-vivo, PK/PD, and safety queries.
3. Deduplicate and extract model, dose, route, schedule, endpoints, effect direction, and limitations.
4. Assess cross-model concordance and identify translational or IND-enabling gaps.
5. Report evidence strength and unresolved contradictions.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- preclinical evidence table
- cross-model synthesis
- PK/PD and toxicity summary
- development gaps

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
