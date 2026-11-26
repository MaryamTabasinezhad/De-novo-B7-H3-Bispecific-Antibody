# 04_19 — Arm B full-Fab and N215 glycan-core clearance

## Inputs and method

Placed the existing RFantibody Arm B backbones from tasks 31 and 152
on oriented AFDB v6 canonical human 4Ig B7-H3 (Q5ZPR3), using the
historical crop Cα fit. Used the same rigid 20G5 CH1/CL extensions and
membrane proxy as the [Arm A screen](../04_17_arm_a_geometry/README.md).
Each pose has four placements from 9LY5 A/B and 9LY6 B/C, each fit with
eight or ten terminal variable-domain Cα atoms per chain. The membrane
tilt sensitivity calculation uses the least clearance at any azimuth
for a 10° tilt. The modeled Fv and its anchor contacts stay fixed.

No N215 glycan is resolved in the local experimental structures.
Transferred all resolved sugars (three or four monosaccharides) from
the four linked 9LME chains H, D, E and G to N215. Reused the CG/OD1/ND2
fit on AFDB v6 and 9LME chain A after the canonical 210–220 Cα fit.
Counted heavy-atom pairs below 2 Å against both the Fab and the
non-N215 antigen atoms in each reference conformer.

## Results and decision

| Historical pose | Intended anchors within 4.5 Å | Fv and constant-domain clashes with 4Ig | Minimum membrane clearance at 10° tilt | Fab clash pairs in the two antigen-compatible glycan cores |
| --- | ---: | ---: | ---: | ---: |
| Task 31 | 6/8 | 0 | +18.302 Å | 37 and 35 |
| Task 152 | 4/8 | 0 | +19.844 Å | 10 and 5 |

Both poses clear the protein and membrane screens in all four rigid Fab
placements. The AFDB-based N189 transfers from 9LME chains A and B are
the two cores that clear the antigen. Both overlap the Fab light chain
in both poses. The first NAG stays at least 3.047 Å away, but the second
NAG clashes in both cores and both poses. Additional sugars clash in
task 31. Task 152's overlaps are confined to the second NAG and light-chain
residues 171–172 in input PDB numbering.

Hold both poses and defer Arm A pairing and sequence optimization.
The light-chain clashes support trying a different approach to the
same epitope with the N215 core present during screening. The fixed
transfers sample resolved cores from other sites. Native N215 occupancy,
distal branches, glycan flexibility, and alternate side-chain and
backbone conformations remain unresolved. This screen establishes clashes
for the tested geometries and leaves native compatibility open.

## Outputs and reproduction

- [Fab clearance by template and fit window](04_19_fab_clearance.tsv)
- [Glycan-core clearance by placement](04_19_n215_core_clearance.tsv)

Inputs include
`/scratch/ghaedi/mab/rfantibody_b7h3_backbone_pilot_20260925/B/task_{31,152}/ab_0.pdb`,
`/scratch/ghaedi/mab/rfantibody_inputs_corrected3/target_B.pdb`,
the oriented Q5ZPR3 PDB, the canonical numbering map, and local 9LME,
9LY5 and 9LY6 PDBs. Ran on the login node with the existing RFantibody
environment (NumPy 1.26.4 and SciPy 1.15.3). No Slurm job was submitted.

```bash
source config/hpc/rorqual.sh
out=results/04_19_arm_b_geometry
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_19_arm_b_fab_clearance.py \
  "$out/04_19_n215_core_clearance.tsv" > "$out/04_19_fab_clearance.tsv"
```
