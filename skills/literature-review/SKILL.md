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

## Before execution on a new host

Read [references/runtime-discovery.md](references/runtime-discovery.md). Complete
its read-only discovery pass before selecting commands, paths, datasets, models,
or compute resources. The skill must remain usable on a workstation, login node,
scheduled cluster, or other environment without assuming which one is present.

The original source package is retained under
`references/upstream-biomni/`. Read its `UPSTREAM_SKILL.md` and only the supporting
example files relevant to the current task. Treat source-platform tool calls,
mounts, container paths, concurrency limits, and report requirements as examples
to translate after capability discovery. Never execute them verbatim unless the
target environment independently verifies the same interface.

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

Every computational run should record the command or API request, software and
model versions, parameters, random seeds when applicable, input checksums, output
checksums, dataset releases, and important fallbacks. Preserve experimental facts,
source-derived facts, and computational predictions as separate evidence classes.

## Adaptation state

This package supplies a Codex-valid, portable instruction layer and preserved
upstream examples. Host-specific environments, scheduler adapters, dataset paths,
and scientific smoke tests remain intentionally unbound. When the target host has
been inspected, implement wrappers outside `references/upstream-biomni/`, test
them, and only then promote them into an active `scripts/` directory.
