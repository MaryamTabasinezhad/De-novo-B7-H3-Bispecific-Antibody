# 04_20 — Arm A solvent-facing placement screen

Screened 9,261 rigid placements of seed 301 on the intact human canonical
4Ig B7-H3 AFDB v6 model. Seed 201 was replayed at its original placement
as the interface benchmark. Inputs are the [tracked seed PDBs](../04_18_arm_a_backbone_pilot/)
and their original target crops in
`/scratch/ghaedi/mab/04_18_arm_a_backbone_pilot/A/{27715195,27715196}/target.pdb`.
The crop placement uses the existing Cα fit. Anchor positions are
canonical 126–129.

The grid used extrinsic x/y/z rotations from −30° through +30° in 10°
increments about the anchor Cα centroid, followed by translations of
−2, 0, or +2 Å along each oriented target axis. The Fv and all four
CH1/CL placements moved together. The clearance metric takes the lowest
atom across the four full-Fab estimates at both the nominal plane and
the worst azimuth of a 10° tilt around the transmembrane Cα centroid.
The clash screen requires at least 2 Å to ectodomain heavy atoms, all
annotated glycosite ND2 atoms, and both N104 first-NAG transfers from
9LME. Each of the four anchors must be within 4.5 Å of the Fv.

| Screen | Seed 301 placements retained |
| --- | ---: |
| Rigid grid | 9,261 |
| All four anchors | 2,790 |
| Also clear the protein and glycan-proxy distance screen | 174 |
| Also clear the nominal membrane plane | 60 |
| Also clear the 10° tilt screen | 0 |

The best tilted clearance among the 174 placements was −10.99 Å,
with +10.42 Å nominal clearance and a 2.30 Å minimum protein distance.
Its rotation was (−10°, +30°, +20°) and translation (−2, +2, 0) Å.
The original seed 301 and 201 clearances reproduce the earlier
worst-of-four results to the precision of the original table. Some grid
placements cleared the tilted plane, but none also preserved the anchor
and clash criteria. The finite grid, rigid poses, same-lineage Fab elbow
templates, first-sugar probes, and planar tilt model limit the inference.

The [per-placement table](04_20_placements.tsv) records the seed 201
control and each grid point. Verified 9,261 unique transforms and
recounted the advancement gates directly from the table.

```bash
source config/hpc/rorqual.sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_20_arm_a_pose_screen.py \
  > results/04_20_arm_a_pose_screen/04_20_placements.tsv
```

Hold the pose-conditioned pilot, nine unused seeds, and sequence design.
Before another GPU batch, assess broader approach geometry against a
better-supported membrane and Fab-elbow ensemble. The nominally clear
placements can serve as controls for checking sensitivity to that
ensemble. No Slurm job was submitted for this CPU screen.
