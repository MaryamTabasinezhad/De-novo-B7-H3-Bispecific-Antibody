---
name: target-tractability-druggability
description: "Assess whether a human target is tractable and which therapeutic modality is most viable using known drugs, structural evidence, pockets, safety, essentiality, and modality-specific constraints. Use for druggability or modality-selection questions."
metadata:
  short-description: "Assess target tractability across therapeutic modalities"
  source: "Biomni Lab"
  source-skill-id: "skill_8de1ad6db2524087b4588d1c20d65422"
  adaptation-stage: "portable-instruction-layer"
---

# Target Tractability and Druggability

Combine orthogonal evidence into a transparent modality scorecard without treating any single database or pocket predictor as decisive.

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

- Do not assume a structural pocket makes an extracellular antibody target more or less viable.
- Do not silently substitute a predicted structure for an experimental structure.
- Separate target biology, modality feasibility, safety, and evidence quality.

## Portable workflow

1. Resolve the target and intended disease or modality context.
2. Discover available target, drug, safety, essentiality, and structure resources.
3. Retrieve structured tractability evidence and choose the best justified structures.
4. Run pocket analysis only when relevant and when a validated implementation is available.
5. Score modalities transparently and document missing or contradictory evidence.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- modality scorecard
- structure and pocket evidence
- safety and essentiality notes
- decision rationale

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
