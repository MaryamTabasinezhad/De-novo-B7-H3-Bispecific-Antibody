# 07_06 — Current Fab-category counts and top five

Checked 2026-10-21 UTC against the existing AF3 output artifacts. No new predictions or scheduler changes.

| Category | Completed inputs | Four-sample predictions | Planned inputs |
|---|---:|---:|---:|
| A-only | 40 | 160 | 40 |
| B-only | 29 | 116 | 29 |
| A+B dual-arm | 170 | 680 | 1,160 |
| Total | 239 | 956 | 1,229 |

There are 69 completed single-arm inputs and 170 completed dual-arm inputs. The dual campaign has 990 inputs without outputs and no incomplete artifact sets in the new audit. These are variable-heavy/light-chain complexes with antigen, not assembled full constant-domain Fab or Fc-containing antibodies. No complete IgG-Fc construct is established by these outputs.

## Selection method

Reused `tools/07_fab_categories/export_top_five.py`: require four sample rankings and sample CIFs; rank each input by its maximum full-precision native AF3 ranking score; break ties by ascending input index; deduplicate antibody sequence tuples within each category. For pairs, identity is the ordered A/B tuple. One winning sample represents each selected input, not five samples of the same antibody. Global ipTM and pTM are supplied for interpretation, not substituted for the ranking score.

The added `--snapshot YYYYMMDD` option permits a new output directory and date label; the default preserves the earlier 20261018 path. Scientific ranking, parameters, chain checks and copy checks are unchanged. Validation: current top five single-arm lists match the old snapshot; AB index133 (A149/B86) enters at rank3 and displaces index54. CIF coordinate chains and byte-for-byte copies are checked by the existing exporter.

## A only — top five

| Rank | Candidate / structure | Ranking score | Global ipTM | pTM |
|---:|---|---:|---:|---:|
| 1 | [fabA_rf2_task116](../results/07_01_fab_A_only/07_04_top_five_20261021/07_04_rank01_index31_fabA_rf2_task116_model.cif) | 0.4081 | 0.39 | 0.44 |
| 2 | [fabA_rf2_task185](../results/07_01_fab_A_only/07_04_top_five_20261021/07_04_rank02_index26_fabA_rf2_task185_model.cif) | 0.3652 | 0.34 | 0.41 |
| 3 | [fabA_rf2_task30](../results/07_01_fab_A_only/07_04_top_five_20261021/07_04_rank03_index36_fabA_rf2_task30_model.cif) | 0.3618 | 0.33 | 0.44 |
| 4 | [fabA_rf2_task160](../results/07_01_fab_A_only/07_04_top_five_20261021/07_04_rank04_index34_fabA_rf2_task160_model.cif) | 0.3535 | 0.32 | 0.43 |
| 5 | [fabA_rf2_task275](../results/07_01_fab_A_only/07_04_top_five_20261021/07_04_rank05_index5_fabA_rf2_task275_model.cif) | 0.3329 | 0.29 | 0.40 |

## B only — top five

| Rank | Candidate / structure | Ranking score | Global ipTM | pTM |
|---:|---|---:|---:|---:|
| 1 | [fabB_rf2_task10](../results/07_02_fab_B_only/07_04_top_five_20261021/07_04_rank01_index10_fabB_rf2_task10_model.cif) | 0.3806 | 0.36 | 0.42 |
| 2 | [fabB_rf2_task234](../results/07_02_fab_B_only/07_04_top_five_20261021/07_04_rank02_index15_fabB_rf2_task234_model.cif) | 0.3401 | 0.31 | 0.42 |
| 3 | [fabB_rf2_task272](../results/07_02_fab_B_only/07_04_top_five_20261021/07_04_rank03_index13_fabB_rf2_task272_model.cif) | 0.3391 | 0.31 | 0.42 |
| 4 | [fabB_rf2_task226](../results/07_02_fab_B_only/07_04_top_five_20261021/07_04_rank04_index25_fabB_rf2_task226_model.cif) | 0.3330 | 0.30 | 0.41 |
| 5 | [fabB_rf2_task124](../results/07_02_fab_B_only/07_04_top_five_20261021/07_04_rank05_index28_fabB_rf2_task124_model.cif) | 0.3246 | 0.29 | 0.41 |

## A+B pair — top five

| Rank | Candidate / structure | Ranking score | Global ipTM | pTM |
|---:|---|---:|---:|---:|
| 1 | [fabAB_A149_B20](../results/07_03_fab_AB_pairs/07_04_top_five_20261021/07_04_rank01_index125_fabAB_A149_B20_model.cif) | 0.2580 | 0.23 | 0.33 |
| 2 | [fabAB_A265_B234](../results/07_03_fab_AB_pairs/07_04_top_five_20261021/07_04_rank02_index15_fabAB_A265_B234_model.cif) | 0.2436 | 0.22 | 0.32 |
| 3 | [fabAB_A149_B86](../results/07_03_fab_AB_pairs/07_04_top_five_20261021/07_04_rank03_index133_fabAB_A149_B86_model.cif) | 0.2426 | 0.22 | 0.31 |
| 4 | [fabAB_A12_B251](../results/07_03_fab_AB_pairs/07_04_top_five_20261021/07_04_rank04_index101_fabAB_A12_B251_model.cif) | 0.2325 | 0.20 | 0.32 |
| 5 | [fabAB_A12_B226](../results/07_03_fab_AB_pairs/07_04_top_five_20261021/07_04_rank05_index112_fabAB_A12_B226_model.cif) | 0.2306 | 0.21 | 0.30 |

## Sources and execution

- Scratch outputs: `/scratch/ghaedi/mab/fab_category_outputs/{fab_A_only,fab_B_only,fab_AB_pairs}/`.
- Scratch input sequences/lineage: `/scratch/ghaedi/mab/fab_category_inputs/`.
- New durable dual audit: `results/07_03_fab_AB_pairs/07_06_output_audit_20261021.tsv`.
- Durable structures, summaries, per-sample rankings and lineage: `07_04_top_five_20261021/` under each of the three category result directories.
- Existing AF3 settings: seeds101/202, two samples per seed, three recycles.

```bash
source config/hpc/rorqual.sh
python3 tools/07_fab_categories/audit_dual_fab_outputs.py --root /scratch/ghaedi/mab/fab_category_outputs/fab_AB_pairs --out results/07_03_fab_AB_pairs/07_06_output_audit_20261021.tsv
python3 tools/07_fab_categories/export_top_five.py --snapshot 20261021
```

The source artifact inventory also checked all four nonempty model, summary-confidence and full-confidence files for each single-arm input: A40 and B29 complete, no incomplete ranking sets. Python standard library only; no installation or inference. The audit verifies execution artifacts, not interface geometry or simultaneous engagement.

Status: inventory and updated exports complete. Rankings remain confidence-based and provisional for the unfinished dual campaign. These scores do not demonstrate affinity, correct epitope binding, simultaneous cis binding or experimental activity. Next: inspect interfaces, canonical epitope contacts and same-antigen A/B engagement before advancing to Fc assembly.

## 07_07 — Downloadable structure archive

`results/07_07_top_15_structures_20261021.zip` contains the 2026-10-21 top
five CIFs per group (A-only, B-only, A+B), three source selection tables,
a combined model index and README. Original antigen-containing coordinates
are preserved without conversion. Verified ZIP integrity,15 CIFs/five per
group and exact agreement of archived bytes with tracked source files.
No new predictions or ranking changes; the historical07_05 ZIP is preserved.
