---
name: cell-surface-antigen-discovery
description: "Discover and rank tumor-selective, antibody-accessible cell-surface antigens for ADC, CAR-T, bispecific, engager, or radioligand programs. Use when expression, topology, normal-tissue safety, and modality tractability must be evaluated together."
metadata:
  short-description: "Rank tumor-selective antibody-accessible antigens"
  source: "Biomni Lab"
  source-skill-id: "skill_522578a78cb54c8fa5d7eb3fdcd7e09b"
  adaptation-stage: "portable-instruction-layer"
---

# Cell-Surface Antigen Discovery

Integrate tumor expression, extracellular topology, normal-tissue expression, and modality-specific constraints into an auditable antigen ranking.

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

- Do not substitute gene essentiality for cell-surface accessibility or tumor selectivity.
- Do not infer antibody accessibility from RNA expression alone.
- Keep known positive controls in the analysis when they are available.

## Portable workflow

1. Clarify tumor type, modality, input data, cell labels, and antigen search breadth.
2. Discover available single-cell, surfaceome, topology, and normal-tissue resources and freeze their versions.
3. Quantify malignant-compartment specificity, apply topology gates, and assess normal-tissue liabilities.
4. Score candidates transparently, run sensitivity checks, and attach source-grounded evidence to leading candidates.
5. Separate validated antigens, plausible novel candidates, and candidates limited by missing evidence.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- ranked antigen table
- normal-tissue safety table
- topology evidence
- analysis manifest

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
