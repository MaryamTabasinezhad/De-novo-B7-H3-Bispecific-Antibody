# 04_16 — GPT loop hypotheses and matched AF3 predictions

GPT-6.2 Sol was run directly without Slurm on 2026-11-26. Run ID
`04_16_hypothesis`, with `--hypothesis --parent 275` for Arm A and
`--hypothesis --parent 282` for Arm B. The proposal JSONs include prompts,
parent sequences, experimental evidence, modeled contacts and thread IDs.
The worker validated that each proposed sequence changes only positions
within the RFantibody design loops and retains VH/VL lengths.

| Parent | Proposed change | AF3 job | Output root |
|---|---|---|---|
| A275 | VH S104T, H3 | 27674443 | /scratch/ghaedi/mab/04_16_loop_hypotheses/27674443 |
| B282 | VH S31T, H1 | 27674444 | /scratch/ghaedi/mab/04_16_loop_hypotheses/27674444 |

Numbering is one-based in the parent VH. Both changes are computational
hypotheses. Each generated AF3 input reuses the parent's antigen sequence,
chain identifiers, light chain and seeds 101/202. The AF3 worker retains
the parent workflow's two samples per seed, three recycles and Triton
settings. Existing parent prediction samples are the controls. MSA and
template searches are run for the variant inputs by the existing worker.

Validation submitted from the project root with:

```bash
for parent in A275 B282; do
  sbatch --parsable --job-name="mab-loop-$parent" \
    --export="ALL,AF3_COMPARISON_INPUT=$PWD/results/04_16_loop_hypotheses/04_16_${parent}_af3.json" \
    tools/07_fab_categories/alphafold3_fab_category_job.sh
done
```

Scheduler output and errors use the worker's existing
`/scratch/ghaedi/mab/jobs/fab_category_%A_%a.{out,err}` patterns.
Next compare per-sample intended-patch contacts, local interface confidence
and pose consistency against each unchanged parent.

A one-time watcher checks both jobs every 60 seconds and publishes [04_16_completion.md](04_16_completion.md) after both terminate. Its local log is work/04_16_watch_af3/watcher.log.

## A275 retry — 2026-11-27 UTC

Job 27674443 reached its four-hour limit during database searches and
produced zero model CIFs. Resubmitted A275 as **27790007** with eight hours,
the same AF3 input, and the committed worker. Slurm accepted the job and
reported it pending at submission.

```bash
source config/hpc/rorqual.sh
git show d10cc162097b59a2328744a13054c68729d21a75:tools/07_fab_categories/alphafold3_fab_category_job.sh |
  sbatch --parsable --account="$MAB_GPU_ACCOUNT" --time=08:00:00 \
    --job-name=mab-loop-A275-retry \
    --export="ALL,AF3_COMPARISON_INPUT=$MAB_PROJECT_ROOT/results/04_16_loop_hypotheses/04_16_A275_af3.json"
```

Scratch output root is `/scratch/ghaedi/mab/04_16_loop_hypotheses/27790007`.
Logs are `/scratch/ghaedi/mab/jobs/fab_category_27790007_%a.{out,err}`.

## B282 validation status — 2026-11-27 UTC

Slurm recorded B282 S31T job 27674444 as TIMEOUT at its four-hour
limit. The recorded scratch output directory had no model CIFs at
the status check. The matched comparison with the unchanged B282
parent is pending. No B282 retry was submitted in this update.
