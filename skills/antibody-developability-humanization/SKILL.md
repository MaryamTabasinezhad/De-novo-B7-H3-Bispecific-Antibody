---
name: antibody-developability-humanization
description: "Assess or humanize existing mAb, Fv, scFv, VHH, or nanobody sequences using antibody numbering, sequence liabilities, humanness, immunogenicity, CDR grafting, and framework back-mutation analysis. Use for existing antibody sequences, not de novo binder generation."
metadata:
  short-description: "Assess and humanize antibody variable regions"
  source: "Biomni Lab"
  source-skill-id: "skill_96d2106323804eb8ad9fe07bd476ff4d"
  adaptation-stage: "portable-instruction-layer"
---

# Antibody Developability and Humanization

Produce numbered, auditable sequence assessments and conservative humanization variants while separating predicted liabilities from measured developability.

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

- Do not change CDRs or structurally important framework residues without explicit rationale.
- Do not claim reduced immunogenicity or improved developability without experimental validation.
- Licensed predictors such as NetMHCIIpan must never be downloaded automatically.

## Portable workflow

1. Ingest and validate chain identity, species, format, and antibody numbering.
2. Discover installed numbering, liability, humanness, and immunogenicity tools and their licenses.
3. Run sequence-liability and biophysical proxy analysis with recorded methods.
4. When humanization is requested, select documented human germlines, graft CDRs, and propose justified framework back-mutations.
5. Reassess every proposed construct and preserve a residue-level change ledger.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- numbered sequence table
- liability assessment
- humanization variants
- change and rationale ledger

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
