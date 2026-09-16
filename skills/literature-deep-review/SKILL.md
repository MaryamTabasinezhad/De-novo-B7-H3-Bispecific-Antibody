---
name: literature-deep-review
description: "Produce an audit-ready biomedical review with exact quotations or stable locators, claim-evidence tables, contradiction checks, and optional figure evidence. Use when ordinary narrative review is insufficient and every delivered claim needs traceable support."
metadata:
  short-description: "Build audit-ready claim-level evidence reviews"
  source: "Biomni Lab"
  source-skill-id: "skill_18ead39ed464498b83ebe9fbcbfb7666"
  adaptation-stage: "portable-instruction-layer"
---

# Literature Deep Review

Freeze a review corpus, acquire permissible source text, construct claim-level evidence, independently verify anchors, and deliver reproducible review artifacts.

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

- Do not claim full-text support when only metadata or an abstract was inspected.
- Respect access and reuse rights for every source and figure.
- Do not fabricate quotations, page numbers, figure interpretations, or execution provenance.

## Portable workflow

1. Select an effort mode and define the review question, evidence types, and stopping rule.
2. Discover available scholarly search and document-retrieval capabilities, then freeze the corpus.
3. Acquire and parse permitted text and figures with a ledger recording source and rights state.
4. Build atomic claims and evidence anchors; separate unsupported, contradicted, and ambiguous claims.
5. Cross-check consequential claims against the inspected sources; additional agents are not required.
6. Write the requested review with a concise evidence table and unresolved questions.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- corpus ledger
- claim-evidence matrix
- quotation and figure anchors
- verified review artifact

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
