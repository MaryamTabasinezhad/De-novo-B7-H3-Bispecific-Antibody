# Three-category Fab generation and comparison campaign

**Authorization:** user-directed on 2026-09-29. This campaign generates three
categories for direct comparison before complete Fc-containing antibody
assembly.

## Categories and counts

| Category | Inputs | AF3 chains | Purpose |
|---|---:|---|---|
| Arm A-only Fab | 40 | H-A, L-A, shared target T | Independent evaluation of each Arm A Fab |
| Arm B-only Fab | 29 | H-B, L-B, shared target T | Independent evaluation of each Arm B Fab |
| Arm A + Arm B dual-Fab | 1,160 | H-A, L-A, H-B, L-B, shared target T | Test two Fab arms on one human 4Ig B7-H3 molecule |

The dual-Fab count is 40 × 29 = 1,160. Each input uses AF3 seeds 101 and 202,
two diffusion samples per seed, and three recycles, yielding four predicted
complexes per input. The maximum planned sample count is therefore 160 for
Category A, 116 for Category B, and 4,640 for Category AB.

## Shared target and lineage

All three categories use the same extracellular portion of the tracked human
4Ig B7-H3 model, `human_4ig_afdb_v6_oriented.pdb`, canonical residues 29–466.
This shared target includes both selected epitopes and prevents the dual-Fab
category from combining two incompatible cropped target fragments. Each input
retains the Arm A and/or Arm B RF2 task IDs and source PDB paths in a sidecar
lineage record.

## Measurements

For each category, record AF3 runtime completion, chain integrity, clash flag,
disorder fraction, pTM, ranking score, H–L ipTM, target-interface ipTM and PAE,
and contacts with the canonical selected residues. For Category AB additionally
record Fab–Fab clashes, simultaneous A/B epitope contacts on the same T chain,
epitope accessibility, relative Fab orientation, and membrane/glycan-aware
geometry where available.

The three categories must be compared using common fields, while retaining the
same-antigen cis-binding requirement as a distinct Category AB gate. These
predictions are computational structural hypotheses and do not establish
experimental affinity, internalization, Fc-mediated killing, aggregation
stability, or clinical benefit.

## Tracked execution

Worker: `tools/07_fab_categories/alphafold3_fab_category_job.sh`.
Input generator: `tools/07_fab_categories/prepare_fab_category_input.py`.
Scratch inputs are written under
`/scratch/ghaedi/mab/fab_category_inputs/`; AF3 outputs are written under
`/scratch/ghaedi/mab/fab_category_outputs/`. Reviewable summaries and
rejection reasons will be copied to the numbered result directories after the
Slurm jobs complete.
