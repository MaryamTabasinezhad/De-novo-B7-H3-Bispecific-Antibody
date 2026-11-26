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
