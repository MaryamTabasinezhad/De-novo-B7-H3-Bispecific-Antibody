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

## Input verification and queued QC

The installed RFantibody HLT parser read all three inputs as 232 binder
residues plus 141 target residues, with 56 design-loop residues and all
four requested hotspot indices. Slurm accepted job IDs 27718318–27718320.
Their pending time limits were reduced to 10 minutes to allow shorter
backfill windows, based on observed 50-step pilot timings and the
15-step conditioned workload.

CPU job 27718507 uses dependency `afterok:27718318:27718319:27718320`.
It compares all six output backbones with A0 and seed 201, checks the
target and variable-domain mapping, and records framework and loop Cα
RMSDs to each input, within-placement loop RMSDs, approach angles,
anchor contacts, protein pairs, and glycan and full-Fab clearance
proxies. The legacy 04_18 comparison reproduces the archived geometry
table with the updated script. The QC job writes temporary tables under
`/scratch/ghaedi/mab/04_22_arm_a_conditioned/qc/27718507/` and records
the six PDBs and two tables here after the checks execute. Its logs
are in the same scratch log directory as the GPU jobs.

## Partial results and retry

Jobs 27718318 and 27718320 completed with seeds 411/412 and 431/432.
Job 27718319 timed out before writing either output. Its dependent QC
job 27718507 was cancelled. The [partial geometry table](04_22_partial_geometry.tsv)
and [approach and loop metrics](04_22_partial_geometry_detail.tsv) cover the
four finished backbones. All four clear the sub-2 Å protein and glycan
distance checks. Three clear the nominal membrane. None retains all four
anchors. Seed 412 contacts 127–129 with +10.92 Å nominal clearance, and
seed 431 contacts 126, 127 and 129 with +0.52 Å nominal clearance.
Framework Cα coordinates moved 2.32–3.75 Å relative to the input after
antigen alignment despite the fixed-dock mask. Evaluate realized poses
when ranking candidates.

Placement 2 was resubmitted as 27722542 with the same input, seeds and
scientific settings and the original 25-minute limit. Its outputs go
under `/scratch/ghaedi/mab/04_22_arm_a_conditioned/A/27722542`.
Dependent job 27722544 runs the six-backbone QC with 27722542 as the
placement 2 output directory. The QC inputs are passed as a positional
job ID to the existing worker. Sequence design remains on hold.
