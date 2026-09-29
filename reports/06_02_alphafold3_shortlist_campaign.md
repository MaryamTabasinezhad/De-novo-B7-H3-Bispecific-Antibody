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

## Completed run and results

Slurm array `21999799` completed on 2026-09-29 with exit code `0:0` for all 69
array tasks. Every input produced four seed/sample predictions, so the run
produced 276 sample complexes. AF3 also writes one aggregate model per input;
there are therefore 345 model CIF files in scratch (276 sample models plus 69
aggregate models). No task failed and no AF3 summary reported a clash flag.

The tracked derived tables are:

- `results/06_02_af3_validation_shortlist/per_input.tsv`: one row per RF2
  shortlist input, with four-sample averages and contact-recovery counts;
- `results/06_02_af3_validation_shortlist/per_sample.tsv`: one row per AF3
  seed/sample model, with confidence, PAE, and canonical epitope contacts;
- `results/06_02_af3_validation_shortlist/run_manifest.json`: job, input,
  output, and counting record.

### Aggregate structural results

| Arm | Inputs | AF3 sample complexes | Inputs with ≥1 selected-epitope contact in at least one sample | Inputs with ≥2 selected-epitope contacts in at least one sample | Inputs with ≥2 contacts in all four samples | Mean H–L ipTM | Mean H–T ipTM | Mean L–T ipTM | Inputs with any clash flag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 40 | 160 | 27 | 21 | 0 | 0.864 | 0.152 | 0.146 | 0 |
| B | 29 | 116 | 29 | 28 | 2 | 0.868 | 0.138 | 0.132 | 0 |

The heavy/light results are consistent with the pilot: both arms generally
form internally coherent antibody units. The mean antibody–target interface
confidence is much lower than the mean H–L confidence. Mean minimum interface
PAE was 12.1 Å (H–T) and 12.4 Å (L–T) for Arm A, and 13.3 Å (H–T) and 13.5 Å
(L–T) for Arm B. These values describe model uncertainty; they are not
affinity measurements and are not being used as an invented universal cutoff.

### Contact-recovery interpretation

The contact counts are geometric observations from AF3 coordinates. “At least
one sample” means that one or more of the four predictions for that input placed
an antibody heavy/light atom within 4.5 Å of at least one selected canonical
epitope residue. It does not mean that the contact is stable, energetically
favorable, or experimentally observed. “All four samples” is a stricter
repeatability description.

Arm A had 43 of 160 samples with at least one selected-residue contact and 29
with at least two; 17 had at least three. Arm B had 79 of 116 samples with at
least one selected-residue contact, 65 with at least two, and 34 with at least
three. Arm A therefore has a weaker and less reproducible contact-recovery
pattern than Arm B under this AF3 setup.

Examples of contact-supported structures for follow-up—not final selections—
include Arm A RF2 task 283 (at least two selected residues in 3/4 samples) and
Arm B RF2 tasks 275 and 101 (at least two selected residues in 3/4 and 4/4
samples, respectively). These examples must still be checked for pose
consistency, target context, sequence liabilities, and Fab-pair compatibility.

### Scientific conclusion and promotion gate

The 69-model campaign successfully validated the AF3 runtime and generated a
complete, inspectable prediction set. It supports robust antibody H–L folding
for the RF2 shortlist and shows that some models repeatedly contact the intended
canonical target regions. It does **not** establish that the arms bind B7-H3,
that the contacts are specific or high-affinity, or that either arm will
internalize or recruit Fc-mediated killing.

The next gate is a pose/contact audit of the contact-supported subset, followed
by Fab-pair geometry and same-antigen cis-reachability analysis. Whole-IgG
assembly should use only candidates that survive those checks. The current
results do not justify treating all 69 models as equivalent survivors or
advancing directly to a final Fc-containing construct.
