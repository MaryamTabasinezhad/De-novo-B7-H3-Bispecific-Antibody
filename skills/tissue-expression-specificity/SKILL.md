---
name: tissue-expression-specificity
description: "Assess where a human target is expressed and identify expression-based on-target safety liabilities using normal-tissue RNA and protein atlases. Use for tissue specificity, vital-organ exposure, and cross-atlas concordance questions."
metadata:
  short-description: "Assess tissue expression and on-target safety"
  source: "Biomni Lab"
  source-skill-id: "skill_6555e1f8055e4a49bcc909a8fd84b635"
  adaptation-stage: "portable-instruction-layer"
---

# Tissue Expression Specificity

Resolve the target, compare available normal-tissue atlases, quantify specificity, and surface organ-level liabilities with source provenance.

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

- RNA expression alone is not proof of cell-surface protein abundance.
- Do not compare atlas values as if their measurement scales were identical.
- Flag missing tissues, version differences, and discordant RNA/protein evidence.

## Portable workflow

1. Resolve gene, Ensembl, or UniProt identifiers.
2. Discover local GTEx/HPA resources or permitted live access and record release versions.
3. Load and normalize each atlas without erasing source-specific measurement semantics.
4. Compute specificity and cross-atlas summaries and inspect vital-organ expression.
5. Ground biological interpretation in retrievable literature where needed.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- tissue expression table
- specificity metrics
- cross-atlas comparison
- on-target safety flags

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
