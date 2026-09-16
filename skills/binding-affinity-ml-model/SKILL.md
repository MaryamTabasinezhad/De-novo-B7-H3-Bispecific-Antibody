---
name: binding-affinity-ml-model
description: "Train and benchmark target-specific small-molecule affinity or potency models from IC50, Ki, or Kd data, then screen compounds with scaffold-split and applicability-domain checks. Use only for small-molecule QSAR or affinity modeling, not antibody or protein-protein binding prediction."
metadata:
  short-description: "Train honest target-specific small-molecule affinity models"
  source: "Biomni Lab"
  source-skill-id: "skill_0c841f13357d45b0ac471169e58a535d"
  adaptation-stage: "portable-instruction-layer"
---

# Small-Molecule Binding Affinity ML

Curate endpoint-consistent compound data, evaluate models with leakage-resistant splits, and restrict screening claims to the validated applicability domain.

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

- Do not use this skill to estimate antibody affinity or protein-protein binding.
- Do not mix IC50, Ki, and Kd values without an explicit justified model.
- Do not silently replace a requested framework or report random-split performance as scaffold generalization.

## Portable workflow

1. Resolve the target and define endpoint, units, assay scope, and modeling objective.
2. Discover accessible ChEMBL or supplied datasets and freeze source versions.
3. Standardize structures, censoring, duplicates, and assay context; pass a data-reality gate.
4. Benchmark suitable models with scaffold and random splits, uncertainty, and applicability-domain checks.
5. Screen external compounds only with the selected validated model and report novelty and domain limitations.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- curated assay dataset
- benchmark results
- model bundle or specification
- screened candidate table

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
