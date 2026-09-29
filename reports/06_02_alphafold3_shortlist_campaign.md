# AlphaFold 3 validation campaign for the 69-model RF2 shortlist

**Status:** campaign authorized by the user on 2026-09-28; Slurm array
`21999799` submitted on 2026-09-28. This report is the
campaign specification and will be extended with the job result table after
completion.

## Purpose

The earlier eight-model AF3 run was a technical and structural pilot. The user
has now instructed the project to skip that pilot as the decision gate and run
the same independent-validation sequence across the complete RF2
control-equivalent shortlist. The campaign asks whether RF2-derived antibody
arms retain coherent antibody folding and the intended B7-H3 interface when
AlphaFold3 independently rebuilds the complex from sequence.

This is still a computational validation. It cannot by itself establish
experimental affinity, cell binding, internalization, Fc-mediated killing,
aggregation stability, or clinical benefit.

## Inputs and exact count

The inputs are the task-deduplicated RF2 shortlist tables:

| Arm | RF2 geometry-gate pool before deduplication | AF3 inputs in this campaign |
|---|---:|---:|
| A | 42 | 40 |
| B | 30 | 29 |
| **Total** | **72** | **69** |

Each input is one RF2 PDB containing antibody heavy chain H, light chain L,
and cropped B7-H3 target chain T. The target is a local cropped fragment, not a
full-length glycosylated membrane receptor. The input-preparation script
extracts H/L/T amino-acid sequences, preserves the RF2 task lineage, and writes
AF3 dialect-version-4 JSON.

## AF3 sampling design

Each of the 69 inputs is evaluated with random seeds 101 and 202 and two
diffusion samples per seed. This produces:

- 4 predicted complexes per RF2 input;
- 160 AF3 complexes for Arm A;
- 116 AF3 complexes for Arm B;
- 276 predicted complexes in total.

The four outputs from one input are repeated structural predictions of the same
antibody sequence; they are not four newly designed antibodies.

## Validation questions and measurements

For every generated complex, the analysis records runtime completion, chain
presence, model and confidence-file availability, clash flag, disorder
fraction, pTM, ranking score, H–L ipTM, H–T ipTM, L–T ipTM, and interface PAE.
The downstream contact audit compares predicted antibody–T contacts with the
selected canonical Arm A or Arm B residues and records contact recovery,
contact-map consistency, and whether the antibody pose is reproducible across
seeds and samples.

The H–L measurements answer whether the antibody arm folds as a coherent Fv.
The H–T and L–T measurements answer whether the intended antibody–B7-H3 pose
is supported. These are separate questions: strong H–L confidence does not
prove antigen binding. No universal AF3 cutoff will be invented after looking
at the results; numerical gates remain documented as provisional and their
rejection reasons will be preserved.

## Promotion sequence after AF3

The 69 inputs will not automatically become final antibodies. The campaign
results will be filtered for reproducible target-interface evidence and
intended-epitope contact recovery. Survivors then proceed to Fab-pair geometry
and same-antigen cis-reachability analysis, followed by compatible 1A+1B
whole-IgG modeling. Only after those gates will Fc/developability triage and
experimental prioritization be considered.

## Traceability

Tracked worker: `tools/06_af3_validation/alphafold3_shortlist_job.sh`.
Tracked input preparation: `tools/06_af3_validation/prepare_af3_shortlist_input.py`.
Scratch inputs and AF3 outputs are under
`/scratch/ghaedi/mab/af3_validation_shortlist_inputs/` and
`/scratch/ghaedi/mab/af3_validation_shortlist/`; the exact paths, Slurm job
ID, command, exit state, and derived summaries will be recorded in the status
report and in `results/06_02_af3_validation_shortlist/`.
