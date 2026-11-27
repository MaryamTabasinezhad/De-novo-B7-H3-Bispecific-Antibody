# 04_25 — Path A benchmark and cohort baseline

Audited all 40 unique Arm A parents against canonical human 4Ig CD276 residues
29–466. Used the existing `04_15_parent_interface.py` worker with the
04_09 lineage table and all four AF3 samples per parent. The worker checks
VH/VL identity and RFantibody design-loop mapping. The
[baseline table](04_25_parent_baselines.tsv) records the canonical residues
touched in each sample at 4.5 Å. At least two of residues 126–129 were
contacted in zero samples for 32 parents, one sample for six parents, and
two samples for A232 and A275. No parent passed in three or four samples.
A232 passed in one sample per seed. A275 passed in both seed-202 samples.

## Reference and diagnostic cases

Verified the ch8H9 IgG epitope experiment and human 4Ig residue mapping
against Ahmed et al., Fig. 7 and Table 10. The recombinant 2Ig-Fc experiment
supports R127 and D128 involvement. The corresponding 4Ig motif occurs in
both IgV domains. The isolated Fab structure and docking model provide
context for the paratope. Exact tested humanized chain-pair qualification
and IgV1 preference on intact 4Ig remain open.
[Reference review](../../reports/02_04_b7h3_full_length_humanized_reference_screen.md)

The [crop comparison](04_25_crop_to_4ig.tsv) combines Step 06 per-sample
crop metrics with Step 07 coordinates and confidence for A217 and A283.
Both parents passed in three of four crops and zero of four intact 4Ig
complexes. Their 4Ig samples show widely distributed alternative contacts.
A217 contacted IgV1 F129 and IgV2 F347 in separate samples. A283 contacted
neither IRDF motif in its four 4Ig samples. Interface confidence remains low
and the minimum chain-pair PAE is above 20 Å in every intact 4Ig sample.
These observations support pose ambiguity. The data leave the physical cause
of crop-to-4Ig contact loss unresolved. Keep both parents in diagnostic
review until there is a credible intact 4Ig starting pose.

## Matched prediction pilot

- **A232** — GPT-6.2 Sol was run directly with
  `python3 tools/04_design_sequence/04_13_gpt6_redesign.py A --run-id 04_25_path_a_benchmark --parent 232 --hypothesis`.
  It proposed VL T26S in RFantibody L1. Checked the sequence difference against
  the parent input. The [proposal](04_25_A232_proposal.json) preserves the
  prompt, rationale and thread ID. AF3 job **27785535** uses the same VH,
  antigen, chain IDs, seeds 101/202, two samples per seed and three recycles
  as the parent workflow. The eight-hour allocation allows for the
  database-search phase observed in the A275 pilot.
- **A275** — AF3 job **27674443** was running in the data pipeline at the
  last check. Its output directory had no model files at that point.
  [Original submission](../04_16_loop_hypotheses/README.md)

After sourcing `config/hpc/rorqual.sh`, submitted A232 with:

```bash
sbatch --parsable --account="$MAB_GPU_ACCOUNT" --time=08:00:00 \
  --job-name=mab-loop-A232 \
  --export="ALL,AF3_COMPARISON_INPUT=$PWD/results/04_25_path_a_benchmark/04_25_A232_af3.json" \
  tools/07_fab_categories/alphafold3_fab_category_job.sh
```

A232 scratch output root is `/scratch/ghaedi/mab/04_16_loop_hypotheses/27785535`.
Slurm logs use `/scratch/ghaedi/mab/jobs/fab_category_27785535_%a.{out,err}`.
After predictions finish, inspect all four samples per variant against the
parent on intended-patch contacts, pose repeatability and interface
confidence before scaling the redesign review. The 40-parent baseline
audit is complete. The 40-parent redesign review is open.
