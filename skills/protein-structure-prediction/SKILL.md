---
name: protein-structure-prediction
description: "Predict protein or complex structures from sequence using locally available methods such as AlphaFold, Boltz, Chai, or ESM-based folding. Use for structure prediction and confidence analysis; select methods from discovered host capabilities rather than assumed platform services."
metadata:
  short-description: "Predict protein structures with environment-aware methods"
  source: "Biomni Lab"
  source-skill-id: "skill_a2393c9d2df847968e1f4afa92621540"
  adaptation-stage: "portable-instruction-layer"
---

# Protein Structure Prediction

Choose a method appropriate to sequence length and complex type, submit it through the discovered execution environment, and report method-specific confidence without cross-method metric conflation.

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

- Do not run the upstream orchestration script verbatim; it imports platform-specific HPC helpers.
- Do not fold a multi-chain complex through a monomer-only path.
- Do not compare pLDDT, pTM, ipTM, and PAE as interchangeable metrics.

## Portable workflow

1. Resolve sequence, chain stoichiometry, complex type, templates, ligands, and requested method constraints.
2. Discover installed predictors, scheduler interfaces, containers, databases, model weights, caches, and GPU limits.
3. Derive a host-specific command from verified local help or documentation and run a minimal smoke test.
4. Submit a suitably sized SLURM job, record its ID, and inspect completion and scientific outputs.
5. Extract structures and native confidence fields, then produce per-residue and domain-level summaries.

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

- PDB or CIF models
- native confidence outputs
- per-residue confidence table
- run and fallback manifest

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
