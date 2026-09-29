# RF2 official-control-equivalent shortlist

Date: 2026-09-27  
Slurm job: `21886323`  
Control reference: `reports/05_04_rf2_official_control.md`

The official RF2 example had a minimum H/L–T heavy-atom distance of 3.167 Å,
zero antibody–target overlaps below 2.0 Å, and complete H/L/T chains. The
B7-H3 shortlist applies the available parts of that control gate:

- minimum H/L–T distance **at least 3.167 Å**;
- zero pairs below **2.0 Å**;
- existing H/L/T chain and sequence-mapping checks;
- one strongest interface-scored model retained per RF2 task to reduce
  four-sequence-per-backbone duplication.

The B7-H3 PDB files do not carry a pLDDT field matching the official control,
so no pLDDT cutoff was invented.

| Arm | Control-gate models | Task-deduplicated shortlist | Shortlist models contacting ≥1 selected residue | Shortlist models contacting ≥2 selected residues |
|---|---:|---:|---:|---:|
| A | 42 | 40 | 11 | 4 |
| B | 30 | 29 | 19 | 11 |

The task-deduplicated TSV files are in
`results/05_03_control_shortlist_20260927/`. This is a structural
control-equivalent shortlist, not proof of affinity or biological activity.
Models with weak selected-epitope coverage remain recorded for traceability but
should be deprioritized during the next independent AlphaFold 3 validation
stage. Arm A is the current bottleneck because only four strict-gate models
contact at least two selected Arm A residues.
