# Top-five category structure export

2026-10-18. User requested five distinct antibodies/pairs in each campaign.
Export uses the existing AF3 ranking/sample layout from
`tools/06_af3_validation/analyze_af3_shortlist.py`, with the project-specific
exporter `tools/07_fab_categories/export_top_five.py`.

Command:
```bash
source config/hpc/rorqual.sh
python tools/07_fab_categories/export_top_five.py
```

Sources: `/scratch/ghaedi/mab/fab_category_outputs/{fab_A_only,fab_B_only,fab_AB_pairs}/`;
input lineage: `/scratch/ghaedi/mab/fab_category_inputs/`.
No inference, installation, or new Slurm submission was needed. Existing AF3
predictions used seeds 101/202, two diffusion samples per seed, three recycles.

Rank completed inputs by their best full-precision native ranking CSV score;
ties use index. Deduplicate antibody sequence tuples within each category,
using the ordered A/B sequence tuple for pairs. This selects different inputs,
not five stochastic samples of one antibody. Antigen T remains in each CIF.
The winning sample is copied, not converted or modified. These are variable
heavy/light-chain complexes from the existing campaign; the category label
Fab does not establish complete constant-domain or Fc assembly.

| Category | Completed inputs considered | Selected input indices, in rank order |
|---|---:|---|
| A only | 40 | 31, 26, 36, 34, 5 |
| B only | 29 | 10, 15, 13, 25, 28 |
| AB pairs | 164 | 125, 15, 101, 112, 54 |

Outputs: `07_04_top_five_20261018/` beneath each of
`results/07_01_fab_A_only/`, `results/07_02_fab_B_only/`, and
`results/07_03_fab_AB_pairs/`. Each contains five CIFs, native confidence
summaries, four-sample ranking tables, RF2 lineage records, and a selection TSV.

Validation: each selected structure has expected coordinate chain IDs
HA/LA/T, HB/LB/T, or HA/LA/HB/LB/T; all copied structures match the source
byte-for-byte; sequence tuples are distinct within each category. No new
interface/geometry pass is inferred. AF3 ranking is confidence-based and does
not establish affinity or biological activity. AB selection is provisional
because the campaign remains incomplete. Next: scientific interface, epitope,
clash, and same-antigen simultaneous-engagement assessment.
