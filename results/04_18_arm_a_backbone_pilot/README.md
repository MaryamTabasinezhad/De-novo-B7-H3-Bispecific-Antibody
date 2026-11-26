# 04_18 — Arm A seeded backbone pilot

Submitted the first three seeds from the [04_17 plan](../04_17_arm_a_geometry/README.md).
Each runs one backbone with the verified RFantibody checkout
`8fe311415754e0276d1a39c87c57e69c88927a2d`, `RFdiffusion_Ab.pt`, HLT
framework, Q5ZPR3 4Ig AFDB v6 crop 29–169 and anchors T126–T129. The
existing worker now accepts optional counts, loop lengths, and start index.
Deterministic mode uses the start index as the seed for the first design.
The worker retains 50 diffusion steps, final step 1, and no trajectories.

| Seed | H3 / L1 / L3 | Slurm job | Scratch output under `04_18_arm_a_backbone_pilot/A/` |
| --- | --- | --- | --- |
| 101 | 6 / 9 / 9 | 27715194 | `27715194/ab_101.{pdb,trb}` |
| 201 | 9 / 11 / 10 | 27715195 | `27715195/ab_201.{pdb,trb}` |
| 301 | 12 / 13 / 11 | 27715196 | `27715196/ab_301.{pdb,trb}` |

Scratch root is `/scratch/ghaedi/mab`. Logs are under
`/scratch/ghaedi/mab/04_18_arm_a_backbone_pilot/logs/` as
`mab-arm-a-<seed>_<job>.{out,err}`. Each job uses one 40 GB H100 MIG slice
on `gpubase_bygpu_b1`, four CPUs, and 32 GiB RAM. Submission commands:

```bash
source config/hpc/rorqual.sh
run="$MAB_SCRATCH_ROOT/04_18_arm_a_backbone_pilot"
mkdir -p "$run/logs"
for spec in '101 6 9 9' '201 9 11 10' '301 12 13 11'; do
  read -r seed h3 l1 l3 <<< "$spec"
  sbatch --parsable --job-name="mab-arm-a-$seed" --time=00:30:00 \
    --output="$run/logs/%x_%j.out" --error="$run/logs/%x_%j.err" \
    tools/04_design_sequence/04_12_context_pilot_job.sh A 1 \
    "L1:$l1,L2:7,L3:$l3,H1:7,H2:6,H3:$h3" "$seed" 04_18_arm_a_backbone_pilot
done
```

All three jobs started and reached GPU inference. Their outputs will be
compared against A0 on intact 4Ig before deciding whether to submit the
remaining nine seeds. The QC baseline reproduced the previous A0 protein
and Fab clearance metrics. Sequence design stays at the geometry and
shared Fab format gates.
