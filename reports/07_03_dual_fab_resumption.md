# Dual-Fab output audit and campaign resumption

Recorded 2026-10-18 03:33 UTC (scheduler timestamps report 2026-10-17).

Inputs: existing AF3 dual-Fab outputs, Slurm accounting for arrays 22030421,
22030424, and 22030425, and the existing category worker. No predictor,
sequence, seed, recycle, diffusion-sample, or resource settings were changed.

## Audit

The audit follows the AF3 file layout used by
`tools/06_af3_validation/analyze_af3_shortlist.py`. For each of 1,160 indices,
it checks four ranking rows, four nonempty sample CIFs and native confidence
files, five-chain confidence matrices, and top-ranked model/summary presence.
164 inputs passed these artifact checks (656 sample complexes); zero existing
inputs were incomplete and 996 indices had no outputs. This is an execution
artifact audit, not structural chain validation, interface QC, or binding evidence.
Large CIFs and full confidence arrays were not parsed in this lightweight audit.

Scratch output root: `/scratch/ghaedi/mab/fab_category_outputs/fab_AB_pairs/`.
Scratch inputs: `/scratch/ghaedi/mab/fab_category_inputs/fab_AB_pairs/`.
Durable audit: `results/07_03_fab_AB_pairs/07_03_output_audit_20261017.tsv`.
Durable accounting: `results/07_03_fab_AB_pairs/07_03_resource_accounting_20261017.tsv`.
The filenames label the scheduler date of this snapshot.

```bash
source config/hpc/rorqual.sh
python tools/07_fab_categories/audit_dual_fab_outputs.py --root /scratch/ghaedi/mab/fab_category_outputs/fab_AB_pairs --out results/07_03_fab_AB_pairs/07_03_output_audit_20261017.tsv
sacct -n -P -j 22030421,22030424,22030425 --format=JobID,State,ExitCode,ElapsedRaw,MaxRSS,TotalCPU,ReqMem
```

## Resource and scheduler findings

All 164 completed array tasks report exit 0:0. Elapsed time min/median/max:
43.5/51.18/195.38 minutes. Batch-step peak host RSS min/median/max:
7.46/8.87/11.05 GiB. These measurements do not establish GPU-memory needs
or performance with fewer CPUs. Keep the verified request of one H100,
16 CPUs, 64 GiB host memory, and four hours; the longest task makes a
shorter two-hour limit unsuitable without further investigation.

736 existing tasks were pending with ReqNodeNotAvail. Node rg12903 was drained
for GPU assert and rg13403 for Pump 3; jobs have no explicit node pinning.
Their partitions remain gpubase_bygpu_b2 and gpubackfill. The reported start
estimate was October 19 01:15 scheduler time, which is not a guarantee.
The GPU association MaxSubmitJobs is 1,000; only 736 user tasks were active.

## Submission and verification

```bash
source config/hpc/rorqual.sh
sbatch --export=ALL,FAB_CATEGORY=AB --array=900-1159%10 tools/07_fab_categories/alphafold3_fab_category_job.sh
scontrol show job 23455046
squeue -u ghaedi -r -h -o '%T'
```

Slurm accepted job **23455046**, indices 900–1159 with concurrency 10.
Verified account def-ghaedi_gpu, existing partitions, requested resources,
worker path, and no dependency or explicit node restriction. Initial state:
PENDING (Priority). Existing arrays were neither cancelled nor resubmitted.
The expanded queue contains 996 pending tasks: 736 existing plus 260 new.
All 1,160 intended combinations are now accounted for: 164 artifact-complete
and 996 queued. No new model completion is inferred from submission.

Logs: `/scratch/ghaedi/mab/jobs/fab_category_23455046_<index>.out` and `.err`.
Runtime and model/database locations remain those in the unchanged tracked
worker; the existing AF3 settings remain seeds 101/202, two samples per seed,
and three recycles. No software was installed or changed.

Next: inspect scheduler completion and logs; rerun the artifact audit, then
perform five-chain structural and simultaneous-epitope geometry/interface QC
before ranking or Fc assembly. Cluster support can clarify prolonged scheduling
unavailability; no external message was sent.
