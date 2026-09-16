---
name: ligand-binding-mode-analysis
description: "Analyze how a small-molecule ligand binds in an experimental or supplied protein-ligand structure, including pocket residues and geometric interactions. Use for observed ligand poses; not protein-protein interfaces, de novo docking, or binding-affinity prediction."
metadata:
  short-description: "Map small-molecule contacts in protein structures"
  source: "Biomni Lab"
  source-skill-id: "skill_ebf89d293f8c49058111727a00675dce"
  adaptation-stage: "portable-instruction-layer"
---

# Ligand Binding-Mode Analysis

Produce a reproducible contact map from a specified structure while separating observed geometry from energetic or affinity claims.

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

- Do not use for antibody-antigen or other protein-protein interfaces.
- Do not present geometric contacts as binding energies.
- Do not invent a pose when no bound ligand structure is available.

## Portable workflow

1. Resolve the structure, ligand identifier, chain scope, interaction depth, and comparison set.
2. Discover installed parsing, protonation, interaction, and rendering tools.
3. Fetch or validate the structure and identify the intended ligand unambiguously.
4. Run a validated interaction engine or documented geometry fallback and label confidence and source.
5. Compare structures only after establishing residue and ligand mappings.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- pocket contact table
- interaction classifications
- cross-structure comparison
- visualization inputs

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
