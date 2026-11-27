# 04_26 — De novo Arm A matched sequence pilot

The pilot compares backbone 412 (three anchors and +10.92 Å nominal Fab
clearance) with 421 (four anchors and +0.93 Å). Ile126 is tracked as a
contact. The approved provisional working format preserves cognate
heavy and light variable domains on the HLT framework. For computational
full-Fab prediction, use the same 9LY5 CH1 and CL suffixes as the
[Arm B pilot](../04_23_arm_b_bound_pose/README.md). Final constant domains,
hinge, Fc and assembly settings remain open.

The ProteinMPNN worker uses the existing checkpoint
`ProteinMPNN_v48_noise_0.2.pt`, temperature 0.1, four samples per
backbone, and deterministic mode (wrapper seed 42). Only the six
annotated loops are designable. The first submission 27788213 was
cancelled while waiting for GPU priority. CPU job 27788267 uses
the same runtime and model settings. Its inputs and threaded
PDBs are under `/scratch/ghaedi/mab/04_26_arm_a_sequence_pilot/27788267/`,
split into `{412,421}/{input,output}`. The logs are under
`/scratch/ghaedi/mab/04_26_arm_a_sequence_pilot/logs/`.

```bash
source config/hpc/rorqual.sh
stage=04_26_arm_a_sequence_pilot
mkdir -p "$MAB_SCRATCH_ROOT/$stage/logs"
sbatch --parsable --job-name=mab-arm-a-412-421-mpnn \
  --output="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.out" \
  --error="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.err" \
  tools/04_design_sequence/04_26_arm_a_mpnn_job.sh
```

## Sequence results and matched AF3 submissions

The four 412 outputs completed within job 27788267. The 421 invocation
spent over five minutes in PyTorch CPU computation without generating
outputs, so the job was cancelled after the 412 results were verified.
A 421-only retry under job 27790209 used one CPU thread, with the same
checkpoint and sampling settings, and completed in 53 seconds with exit
code 0. The 421 threaded inputs and outputs are under
`/scratch/ghaedi/mab/04_26_arm_a_sequence_pilot/27790209/421/`.
The [sequence table](04_26_sequences.tsv) records eight distinct pairs
with preserved HLT framework sequence and loop lengths. The audit
also confirms standard amino acids and complete VH/VL Cα coverage.

One sample per backbone (sample 0 for a matched comparison) was chosen
for [412](04_26_seed_412_af3.json) and [421](04_26_seed_421_af3.json)
full-Fab predictions. Both inputs contain the same 438-residue 4Ig target,
226-residue heavy and 218-residue light chains including provisional
constants, and identical seeds 101/202. No starting docking pose is
imposed. Each AF3 job requests two samples per seed and three recycles.
The N104 first-sugar geometry is checked against the predicted Fab after
target alignment. Explicit glycan conformers are outside this pilot.

| Stage | Slurm job | Output under scratch stage |
| --- | --- | --- |
| AF3 sequence 412-0 | 27789933 | `27789933/arma_412_mpnn0_fullfab/` |
| AF3 sequence 421-0 | 27790229 | `27790229/arma_421_mpnn0_fullfab/` |
| Matched geometry QC | 27790230 | `qc/27790230/` |

The scratch stage is `/scratch/ghaedi/mab/04_26_arm_a_sequence_pilot/`.
The existing AF3 category worker accepts `AF3_COMPARISON_INPUT` and
`AF3_COMPARISON_STAGE=04_26_arm_a_sequence_pilot` for both jobs. QC
depends on both AF3 jobs succeeding and will compare per-sample patch
contacts, orientation relative to each starting backbone, clashes,
N104 proximity, nominal membrane clearance, and tilt sensitivity. The
10° tilt result is a risk flag. The other six sequence pairs are
available for follow-up after reviewing these predictions.
