---
name: literature-preclinical
description: "Synthesize preclinical evidence for a target-disease pair, including in-vitro assays, in-vivo models, dosing, efficacy, PK/PD, toxicity, concordance, and IND-enabling gaps. Use when the question is specifically preclinical rather than a general literature overview."
metadata:
  short-description: "Synthesize target-disease preclinical evidence"
  source: "Biomni Lab"
  source-skill-id: "skill_845c829245474c4091703e01e627aa00"
  adaptation-stage: "portable-instruction-layer"
---

# Preclinical Literature Review

Create an auditable preclinical evidence map that separates model type, intervention, exposure, efficacy, safety, and translational limitations.

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

- Do not combine cell, animal, ex-vivo, and human evidence without labeling the evidence level.
- Do not infer dose comparability across studies without PK or exposure support.
- Distinguish peer-reviewed evidence from conference, patent, or company claims.

## Portable workflow

1. Define target, disease, intervention class, species, model types, and time window.
2. Search available scholarly sources with separate in-vitro, in-vivo, PK/PD, and safety queries.
3. Deduplicate and extract model, dose, route, schedule, endpoints, effect direction, and limitations.
4. Assess cross-model concordance and identify translational or IND-enabling gaps.
5. Report evidence strength and unresolved contradictions.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- preclinical evidence table
- cross-model synthesis
- PK/PD and toxicity summary
- development gaps

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
