---
name: direction-of-effect-concordance
description: "Assess whether a therapeutic target should be inhibited or activated by reconciling human genetics, functional screens, drug mechanisms, animal phenotypes, and literature. Use for target-directionality decisions and explicit discordance analysis."
metadata:
  short-description: "Decide whether a target should be inhibited or activated"
  source: "Biomni Lab"
  source-skill-id: "skill_b973718932a54ffb8b326f7f157e7036"
  adaptation-stage: "portable-instruction-layer"
---

# Direction-of-Effect Concordance

Build a per-evidence-axis direction matrix and derive a qualified activate, inhibit, mixed, or insufficient-evidence conclusion.

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

- A null loss-of-function phenotype does not by itself support activation.
- Do not hide conflicting evidence or collapse incompatible disease contexts.
- Do not invent directionality when an evidence axis is unavailable.

## Portable workflow

1. Resolve target and disease identifiers and define the therapeutic context.
2. Discover structured genetics, perturbation, drug-mechanism, and phenotype sources available in the environment.
3. Retrieve directional literature and preserve stable citations or record locators.
4. Construct the evidence matrix, apply explicit direction rules, and expose discordance.
5. Assign a confidence tier tied to evidence completeness rather than narrative strength.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- direction evidence matrix
- consensus call
- discordance flags
- citation-verification record

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
