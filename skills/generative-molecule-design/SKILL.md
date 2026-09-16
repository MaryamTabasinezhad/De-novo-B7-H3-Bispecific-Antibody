---
name: generative-molecule-design
description: "Generate, filter, and rank goal-directed de novo small molecules or scaffold hops using explicit activity, drug-likeness, novelty, synthesizability, and makeability objectives. Use only for small-molecule design, not antibody or protein-binder sequence design."
metadata:
  short-description: "Generate and triage goal-directed small molecules"
  source: "Biomni Lab"
  source-skill-id: "skill_2c67771543d14271bbdda3c903d773f1"
  adaptation-stage: "portable-instruction-layer"
---

# Generative Small-Molecule Design

Run a reproducible multi-objective small-molecule campaign with an explicitly qualified activity backend and honest synthesis limitations.

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

- Do not use for antibody, peptide, or protein binder generation.
- Generated structures are hypotheses and are not synthesized, active, or safe by default.
- Do not substitute an unvalidated generic oracle for target-specific activity.

## Portable workflow

1. Define target, seed chemistry, allowed transformations, objective weights, and forbidden motifs.
2. Discover installed chemistry packages, activity backends, synthesis tools, and model caches.
3. Choose and validate an activity backend before generation.
4. Generate with recorded seeds and parameters, then standardize, deduplicate, filter, and rank molecules.
5. Run retrosynthesis only when a validated local implementation and models are available; otherwise report the proxy used.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- generated molecule table
- objective and filter audit
- novelty analysis
- qualified synthesis assessment

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
