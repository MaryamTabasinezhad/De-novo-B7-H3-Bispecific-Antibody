# Arm A + Arm B dual-Fab category

Inputs: 1,160 all-by-all dual-Fab AF3 combinations from the RF2 shortlist.
Large models remain in `/scratch/ghaedi/mab/fab_category_outputs/fab_AB_pairs/`.

As audited on 2026-10-18 UTC: 164 combinations have complete execution artifacts
(656 sample complexes); 996 tasks are queued across arrays 22030421, 22030424,
22030425, and 23455046. Scientific interface/geometry acceptance remains open.

- `07_03_output_audit_20261017.tsv`: artifact status for all 1,160 indices.
- `07_03_resource_accounting_20261017.tsv`: scheduler resource/completion snapshot.
- Report: `reports/07_03_dual_fab_resumption.md`.

Next: inspect completed outputs and summarize five-chain integrity, simultaneous
epitope engagement, and Fab-pair clashes before advancement to Fc assembly.

## Exported structures

`07_04_top_five_20261018/` contains five distinct confidence-ranked inputs,
one winning CIF per input, native summaries, ranking tables and source lineage.
See its README and selection TSV; scientific interface QC remains open.
