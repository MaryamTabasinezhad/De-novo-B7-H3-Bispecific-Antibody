# 04_21 — Arm B glycan-aware approach screen

## Inputs and method

The [archive replay](../04_12_design_inputs/04_12_arm_b_archive_screen.tsv)
identified 12 of 300 historical Arm B backbones with zero sub-2 Å
protein pairs on intact human 4Ig B7-H3. Reused those 12 and the
[full-Fab and glycan-core method](../04_19_arm_b_geometry/README.md).
The two glycan cores that cleared neighboring antigen were included as
obstacles in the subsequent local placement screen.

All 48 unmodified full-Fab placements (four per backbone) cleared intact
4Ig protein and the 10° tilted membrane proxy. All 12 backbones clashed
with both N215 cores in every Fab placement. The results for tasks 31
and 152 reproduced the earlier tables exactly.

For local placement, chose task 31 for its six original anchor contacts,
task 152 for its four contacts and relatively few core clashes, and
task 248 for the fewest core clashes among the 12. Reused the Arm A
pose-screen grid of Euler rotations from −30° to +30° in 10° increments
and translations of −2, 0 or +2 Å on each axis. Used the mean of the
eight intended anchor Cα positions as the rotation pivot. Each rigid
placement had to preserve all original anchor contacts, contact at
least four anchors at 4.5 Å, and stay at least 2 Å from antigen protein
and both N215 cores in all four Fab placements. The membrane screen
uses the least clearance over those placements at 10° tilt.

## Results and next stage

Of 9,261 placements per task, zero for task 31, four for task 152,
and 15 for task 248 cleared all screens, including the tilted membrane.
Ranked each task's surviving placements by its smallest clearance
across antigen protein and both sugar cores. Independently reproduced
the top placements' distances and anchor contacts by direct atom-pair
calculations.

| Task | Rotation xyz (°) | Translation xyz (Å) | Anchors contacted | Minimum protein distance (Å) | Minimum N215 core distance (Å) | Worst tilted membrane clearance (Å) |
| --- | --- | --- | --- | ---: | ---: | ---: |
| 248 | 20, 0, 0 | 2, 0, 0 | 232, 234, 238, 240 | 3.110 | 3.018 | +29.032 |
| 152 | −10, 0, 0 | −2, 2, 2 | 232, 234, 236, 240 | 2.226 | 2.694 | +13.598 |

Carry the task 248 placement forward as the lead geometry and task 152
as the backup. The rotations and translations move rigid models, so the
new interfaces still need bound-pose validation. The transferred cores
do not resolve native N215 occupancy, distal branching, or flexibility.
Pairing remains gated by an Arm A pose clearing its membrane screen.

## Outputs and reproduction

- [Original Fab placements](04_21_fab_clearance.tsv)
- [Original Fab–glycan-core distances and clashes](04_21_n215_core_clearance.tsv)
- [Local placement filter counts](04_21_local_counts.tsv)
- [Local placements clearing contacts, protein, and both cores](04_21_local_placements.tsv)

Read historical backbones from
`/scratch/ghaedi/mab/rfantibody_b7h3_backbone_pilot_20260925/B/task_<id>/ab_0.pdb`
and the target crop from
`/scratch/ghaedi/mab/rfantibody_inputs_corrected3/target_B.pdb`.
Ran on the login node in the existing RFantibody environment with
NumPy 1.26.4 and SciPy 1.15.3. No Slurm job was submitted.

```bash
source config/hpc/rorqual.sh
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
out=results/04_21_arm_b_core_screen
qc_python="$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python"
"$qc_python" tools/04_design_sequence/04_19_arm_b_fab_clearance.py \
  "$out/04_21_n215_core_clearance.tsv" 3 21 28 31 126 152 176 191 211 242 248 250 \
  > "$out/04_21_fab_clearance.tsv"
"$qc_python" tools/04_design_sequence/04_21_arm_b_pose_screen.py \
  > "$out/04_21_local_placements.tsv" 2> "$out/04_21_local_counts.tsv"
```
