# 04_28 — De novo Arm A breadth expansion

| Track | Slurm submission | Requested output |
| --- | --- | --- |
| Lead sequence sampling | 27799113 | 100 ProteinMPNN samples each for backbones 412 and 421 |
| Fresh backbone generation | 27799114, tasks 0–121 | Four RFantibody backbones per task, 488 total, using seeds 513–1000 |

The 488 fresh designs supplement the 12 in job 27798099 (seeds 501–512)
for a combined target of 500. The earlier job remains in flight. The
array reuses target crop 29–169, anchors T126–T129, the audited HLT
scaffold and loop bounds, the verified RFantibody checkpoint, 50
diffusion steps, and final step 1. It starts each design from its own
seed with no docking pose from 412 or 421. The first seed for array
task `i` is `513 + 4*i`. The concurrency cap of 20 follows the
previous breadth run. Neither submission requests an explicit wall
time. Slurm assigned its one-hour default per job or array task.

The lead sequence run retains the audited framework, loop lengths,
cognate VH/VL pairs, checkpoint, temperature 0.1, and deterministic
wrapper seed 42. The 100 samples per backbone are the new total target.
The prior [24-sample pools](../04_27_arm_a_parallel_expansion/04_27_lead_sequences.tsv)
are expected to overlap because the same sampling settings were used.
Audit exact VH/VL pairs and count unique sequences after generation.

Scratch root is `/scratch/ghaedi/mab/04_28_arm_a_breadth_expansion/`.
Sequence outputs are under `27799113/{412,421}/output/`. Array outputs
are under `A/<task-job-id>/` as `ab_<seed>.{pdb,trb}`. Logs are under
`logs/` as `mab-arma-100_27799113.{out,err}` and
`mab-arma-488_27799114_<task>.{out,err}`. Submissions from project root:

```bash
source config/hpc/rorqual.sh
stage=04_28_arm_a_breadth_expansion
mkdir -p "$MAB_SCRATCH_ROOT/$stage/logs"
sbatch --parsable --job-name=mab-arma-100 \
  --output="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.out" \
  --error="$MAB_SCRATCH_ROOT/$stage/logs/%x_%j.err" \
  tools/04_design_sequence/04_28_arm_a_scale_job.sh
sbatch --parsable --array=0-121%20 --job-name=mab-arma-488 \
  --output="$MAB_SCRATCH_ROOT/$stage/logs/%x_%A_%a.out" \
  --error="$MAB_SCRATCH_ROOT/$stage/logs/%x_%A_%a.err" \
  tools/04_design_sequence/04_28_arm_a_fresh_array.sh
```

Both submissions were accepted. After generation, verify sample and seed
coverage. Audit lead sequences for uniqueness and framework retention.
Replay the fresh backbones on intact 4Ig and inspect anchor contacts,
protein and glycan clashes, approach diversity, and nominal Fab
clearance. Record 10° tilt sensitivity as a risk flag.

## Array concurrency update

Removed the original 20-task submission throttle in place with
`scontrol update JobId=27799114 ArrayTaskThrottle=0`. Slurm confirmed
the full 0–121 task range with no user-set array throttle. The
scheduler still governs concurrent allocations through GPU
availability, priority, and account or partition limits.
