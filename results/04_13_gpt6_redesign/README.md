# 04_13 — GPT-6 redesign submission

The user directed immediate submission of separate full-cohort jobs and
cancellation of existing project jobs. Ran
`scancel 22030421 22030424 22030425 23455046` and verified those four
Fab modeling arrays left the active queue. Scheduler rejected the first
submission attempt with a partition/fit error. Removed the explicit CPU
partition and resubmitted. Slurm accepted both jobs.

| Arm | Slurm job | Parents | Worker output |
|---|---|---:|---|
| A | 27672795 | 40 | work/04_13_gpt6_redesign/A_27672795/ |
| B | 27672796 | 29 | work/04_13_gpt6_redesign/B_27672796/ |

Submission from the project root:

```bash
mkdir -p work/04_13_gpt6_redesign
for arm in A B; do
  sbatch --parsable --job-name="mab-gpt6-$arm" \
    --output="$PWD/work/04_13_gpt6_redesign/${arm}_%j.log" \
    tools/04_design_sequence/04_13_gpt6_redesign_job.sh "$arm"
done
```

Tracked inputs are the 04_09 parent lineage tables and 02_04 reference screen.
Actual VH/VL are read from each recorded AF3 input path. The worker logs model
events and stores each last message separately. Each call allows 90 seconds.
A failed first request stops that arm. A model reply requires additional
scientific and sequence validation before being treated as a design.
Prior connectivity tests timed out. Exact reference-chain reconciliation
and standardized internal parent numbering remain open.

## Completion status

Both jobs failed with exit code 1 after 90 seconds. The initial GPT-6
request timed out for A265 and B131. Both logs reported a model metadata
refresh timeout. Neither response was verified. The remaining 39 Arm A
and 28 Arm B parents were never attempted. The queue was empty when checked.
