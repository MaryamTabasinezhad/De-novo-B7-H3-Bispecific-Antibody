---
name: sgrna-design
description: "Find or design CRISPR guide RNAs for knockout, CRISPRi, or CRISPRa with supported nucleases. Prefer experimentally validated guides, then licensed precomputed resources, then transparent rule-based design."
metadata:
  short-description: "Find and rank CRISPR guide RNAs"
  source: "Biomni Lab"
  source-skill-id: "skill_8450f18da5c947caabf0a26d3f262389"
  adaptation-stage: "portable-instruction-layer"
---

# sgRNA Design

Select guides through a tiered evidence strategy with explicit genome build, transcript, nuclease, PAM, off-target method, and licensing provenance.

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

- Do not mix genome builds or transcript coordinates.
- Do not treat an in-silico score as experimental validation.
- Respect commercial-use and material-transfer restrictions of guide resources.

## Portable workflow

1. Resolve organism, genome build, gene or transcript, perturbation mode, nuclease, and delivery constraints.
2. Search bundled and literature-derived validated guides first.
3. Discover whether permitted precomputed design resources are locally available.
4. Use de novo design only when higher-evidence tiers are unavailable and a validated scorer/reference genome exists.
5. Export selected guides with sequence, PAM, coordinates, scores, evidence tier, and provenance.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- ranked guide table
- design and off-target metadata
- resource licensing notes
- selection rationale

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
