---
name: targeted-degrader-design
description: "Design and computationally triage heterobifunctional PROTACs or targeted degraders using target warheads, E3 ligands, linkers, physicochemical filters, docking, and optional ternary modeling. Use for small-molecule degrader programs, not antibody-mediated degradation."
metadata:
  short-description: "Design and triage small-molecule targeted degraders"
  source: "Biomni Lab"
  source-skill-id: "skill_c8d77a80500548a5ad07d8756469814d"
  adaptation-stage: "portable-instruction-layer"
---

# Targeted Degrader Design

Build a transparent degrader design space and rank candidates without overstating degradation, permeability, or ternary-complex predictions.

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

- Do not use for antibody, lysosome-targeting chimera, or protein-binder design unless explicitly adapted.
- A binary warhead binder is not automatically a functional degrader.
- Do not use non-commercial software in a commercial workflow without an appropriate license or substitution.

## Portable workflow

1. Define target, degradation mechanism, cellular context, warhead evidence, and allowed E3 ligases.
2. Discover licensed structure-preparation, chemistry, docking, property, and modeling tools.
3. Validate warhead pose and exit vector before enumerating E3 ligands and linkers.
4. Assemble candidates reproducibly and score physicochemical, permeability, synthesis, and structural criteria.
5. Use ternary-complex modeling only as a qualified optional tier and preserve uncertainty.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- candidate degrader table
- component and linker provenance
- property and docking scorecard
- assumption log

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
