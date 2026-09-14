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

- Do not claim full-text support when only metadata or an abstract was inspected.
- Respect access and reuse rights for every source and figure.
- Do not fabricate quotations, page numbers, figure interpretations, or execution provenance.

## Portable workflow

1. Select an effort mode and define the review question, evidence types, and stopping rule.
2. Discover available scholarly search and document-retrieval capabilities, then freeze the corpus.
3. Acquire and parse permitted text and figures with a ledger recording source and rights state.
4. Build atomic claims and evidence anchors; separate unsupported, contradicted, and ambiguous claims.
5. Run independent verification appropriate to the available agent and scheduler capabilities.
6. Assemble machine-readable evidence and a human-readable review, then record unresolved gates.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- corpus ledger
- claim-evidence matrix
- quotation and figure anchors
- verified review artifact

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
