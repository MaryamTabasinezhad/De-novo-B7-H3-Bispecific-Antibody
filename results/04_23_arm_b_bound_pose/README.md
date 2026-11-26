# 04_23 — Arm B bound-pose prediction pilot

## Prior predictions

The archived task 152 run under
`/scratch/ghaedi/mab/fab_category_outputs/fab_B_only/index_6/fabB_rf2_task152`
contains a 438-residue target in both its processed input and its models.
The staging JSON for the same index currently describes a 94-residue crop.
Use the processed input and coordinates to identify the archived run.

In the [four archived 4Ig Fv models](04_23_task152_archived_af3.tsv),
none retains the intended four anchor contacts of the screened approach.
One sample contacts anchor 228 and three contact none. Heavy–target and
light–target pair ipTM values are 0.09–0.12, indexed by the chain order
in the confidence JSON. The archived models contain the Fv and lack an
explicit N215 glycan. Task 248 has a historical RF2 crop prediction.
The inspected archive yielded no intact-4Ig AF3 output for that lineage.

## Pilot inputs and execution

Predict two full Fab–B7-H3 complexes independently with AF3 checkout
`a66cc52`, the existing Rorqual databases and parameter directory.
Each input uses a previously designed RF2 `ab_0_dldesign_0_best.pdb`
VH/VL sequence from
`/scratch/ghaedi/mab/rfantibody_b7h3_rf2_20260926/B/task_{248,152}/`.
Append the 9LY5 heavy and light SEQRES suffixes after VH 118 and VL 106,
the same provisional constants used for the rigid Fab screen. Use human
Q5ZPR3 residues 29–466, so canonical N215 is sequence index 187. Model
the core chemistry resolved at 9LME A:N189 (NAG–NAG–MAN with
core fucose) as an explicitly linked ligand chain at N215. The two
[pilot inputs](04_23_arm_b_task248_n215.json) use the same target and
glycan chemistry. The [task 152 input](04_23_arm_b_task152_n215.json)
uses the corresponding historical Fab sequence.

The screened rotations and translations serve as comparison geometries.
AF3 gets no imposed interchain pose. The pilot tests whether it recovers
the screened approach independently. Use seeds 101 and 202, two diffusion
samples per seed and three recycles. Neither modeled glycan conformers nor
predicted binding establish native N215 occupancy or binding affinity.

Submitted array **27718731**, index 0 for task 248 and index 1 for task 152,
against the GPU account. Outputs are under
`/scratch/ghaedi/mab/04_23_arm_b_bound_pose/27718731/task_{248,152}/`.
Logs are `/scratch/ghaedi/mab/jobs/04_23_arm_b_27718731_{0,1}.{out,err}`.

```bash
source config/hpc/rorqual.sh
sbatch --parsable \
  --output="$MAB_SCRATCH_ROOT/jobs/04_23_arm_b_%A_%a.out" \
  --error="$MAB_SCRATCH_ROOT/jobs/04_23_arm_b_%A_%a.err" \
  tools/06_af3_validation/04_23_arm_b_bound_pose_job.sh
```

## Evaluation and current status

The array is queued for priority as of November 26 UTC, with a tentative
November 27 start shown by Slurm. Both JSONs passed the installed AF3
fold-input parser and structure construction with its chemical component
dictionary. CPU job **27718920** depends on successful completion of the
entire array (`afterok:27718731`). The QC aligns 438 target Cα atoms to the oriented
reference, measures all intended Fv contacts, and compares the Fab
approach direction to the original and screened references. It checks
Fab clearance from predicted protein and glycan and from both fixed
glycan cores in the reference frame. It also checks the N215 glycan
attachment distance and the 10° membrane tilt proxy. Report chain-pair
ipTM alongside geometry. Treat retention across seeds as a separate
criterion for advancement.

```bash
source config/hpc/rorqual.sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/06_af3_validation/04_23_arm_b_bound_pose_qc.py \
  "$MAB_SCRATCH_ROOT/04_23_arm_b_bound_pose/27718731" \
  > results/04_23_arm_b_bound_pose/04_23_per_sample.tsv
```

The QC job runs the same command using one CPU, 2 GB of memory and a
10-minute limit. It first writes
`/scratch/ghaedi/mab/04_23_arm_b_bound_pose/27718731/per_sample_qc.tsv`
and copies the table to the project result directory upon success.
Scheduler logs are `/scratch/ghaedi/mab/jobs/04_23_arm_b_qc_27718920.{out,err}`.

Compare the completed predictions before deciding whether either lineage
advances. Pairing also depends on the Arm A membrane screen.
