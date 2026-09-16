---
name: literature-review
description: "Find and synthesize evidence across multiple scientific or biomedical papers. Use for general literature reviews, key-paper searches, state-of-the-art summaries, or evidence synthesis that does not require the audit depth of a claim-by-claim deep review."
metadata:
  short-description: "Find and synthesize scientific literature"
  source: "Biomni Lab"
  source-skill-id: "skill_36c19691710c4e16a088fb810be15460"
  adaptation-stage: "portable-instruction-layer"
---

# Scientific Literature Review

Answer a bounded scientific question using retrieved peer-reviewed records and open full text when available.

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

- Do not cite papers that were not actually retrieved and inspected.
- Distinguish abstract-level support from full-text support.
- Use the deep-review skill when exact quotations, stable locators, or figure-level evidence are required.

## Portable workflow

1. Define the question, date range, study types, and inclusion boundaries from existing context.
2. Use available scholarly databases or web search with several complementary queries.
3. Deduplicate records and retain stable identifiers, retrieval dates, and source URLs.
4. Extract claims, methods, limitations, and contradictions only from inspected records.
5. Synthesize the evidence and state important coverage gaps.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- cited narrative
- structured evidence table
- search and inclusion summary
- limitations

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
