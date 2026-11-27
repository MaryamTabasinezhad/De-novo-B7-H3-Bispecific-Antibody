# 04_27 — De novo Arm A parallel expansion

Two independent Slurm submissions run alongside the earlier full-Fab
predictions. This batch requests 24 ProteinMPNN samples per lead backbone
and 12 fresh RFantibody backbones. No wall time was explicitly requested.
Slurm assigned both jobs its one-hour default.

| Track | Slurm job | Inputs and sampling |
| --- | --- | --- |
| Lead sequence expansion | 27798098 | Archived 412 and 421 HLT backbone PDBs. ProteinMPNN v48 noise 0.2 checkpoint, temperature 0.1, four original samples per backbone as comparisons, and 24 samples requested per backbone in this run. |
| Fresh backbone generation | 27798099 | Original HLT scaffold, canonical 4Ig crop 29–169, anchors T126–T129, previous loop bounds and RFdiffusion checkpoint. Twelve new indices and deterministic seeds 501–512, with no starting antibody–target docking pose. |

ProteinMPNN preserves the fixed framework and cognate VH/VL pairing
and samples the six annotated loops. The wrapper reuses seed 42,
so compare the sampled pairs against the eight original sequences and
deduplicate before counting expansion. The fresh run uses 50 diffusion
steps and final step 1. It does not start from the 412 or 421 backbones.
The [earlier sequence pilot](../04_26_arm_a_sequence_pilot/README.md)
and [backbone pilot](../04_18_arm_a_backbone_pilot/README.md) record
the reused runtime and settings.

Scratch root for this stage is
`/scratch/ghaedi/mab/04_27_arm_a_parallel_expansion/`. Sequence
outputs go to `27798098/{412,421}/output/`, and fresh backbones and
TRBs go to `A/27798099/`. Logs use
`logs/mab-arma-<track>_<job>.{out,err}`.

```bash
source config/hpc/rorqual.sh
stage=04_27_arm_a_parallel_expansion
mkdir -p "$MAB_SCRATCH_ROOT/$stage/logs"
for track in scale fresh; do
  sbatch --parsable --job-name="mab-arma-$track" \
    --output="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.out" \
    --error="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.err" \
    "tools/04_design_sequence/04_27_arm_a_${track}_job.sh"
done
```

The submissions were accepted. Once outputs are available, audit framework
and loop integrity and sequence uniqueness for both leads. Replay the
fresh backbones on intact 4Ig and compare anchor coverage, protein and glycan
distance checks, approach diversity, and full-Fab membrane clearance.
Record tilt sensitivity as a risk flag. Full-Fab validation remains a
separate advancement step.
