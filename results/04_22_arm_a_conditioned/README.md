# 04_22 — Arm A pose-conditioned backbone pilot

The [placement table](04_22_placements.tsv) records three choices from
the 60 seed-301 placements with four anchors, positive nominal clearance,
and no sub-2 Å hits in the protein and glycan-proxy screen. The first
maximizes clearance under the 10° sensitivity test. The others maximize
the minimum approach angle from previously chosen placements. The
minimum pairwise angle is 23.18°. Nominal clearances are +10.42, +0.99,
and +0.99 Å. Tilt clearance is recorded as a risk flag. The original
seed 201 remains the interface benchmark.

The three HLT inputs retain the seed 301 framework and its loop lengths.
The target is the original Arm A crop placed in the canonical 4Ig frame,
with T126–T129 explicitly mapped. The pilot uses the verified RFantibody
checkout and checkpoint from [04_18](../04_18_arm_a_backbone_pilot/README.md).
It tests the local fixed-dock implementation with an HLT complex,
partial diffusion at step 15 of 50, and final step 1. The fixed-dock
mask permits backbone diffusion in the six design loops. Two seeds per
placement test local loop diversity within each conditioned approach.

| Placement | Seeds | Slurm job |
| --- | --- | --- |
| 1 | 411, 412 | 27718318 |
| 2 | 421, 422 | 27718319 |
| 3 | 431, 432 | 27718320 |

Scratch outputs are in `/scratch/ghaedi/mab/04_22_arm_a_conditioned/A/<job>`
as `ab_<seed>.{pdb,trb}`. Slurm logs are in
`/scratch/ghaedi/mab/04_22_arm_a_conditioned/logs/mab-arA-dock-<pose>_<job>.{out,err}`.
Jobs were submitted from the project root with the numbered worker and
arguments shown below. Each requests one H100 40 GB MIG slice, four
CPUs, 32 GiB of RAM, and 25 minutes.

```bash
source config/hpc/rorqual.sh
mkdir -p "$MAB_SCRATCH_ROOT/04_22_arm_a_conditioned/logs"
for pose in 1 2 3; do
  sbatch --parsable --job-name="mab-arA-dock-$pose" \
    --output="$MAB_SCRATCH_ROOT/04_22_arm_a_conditioned/logs/%x_%j.out" \
    --error="$MAB_SCRATCH_ROOT/04_22_arm_a_conditioned/logs/%x_%j.err" \
    tools/04_design_sequence/04_22_arm_a_conditioned_job.sh "$pose" "$((400 + 10 * pose + 1))"
done
```

Next, QC the outputs against seed 201 on intact 4Ig and compare the
realized framework placements with the three starting poses. The nine
unused unconditional seeds and sequence design remain on hold.
