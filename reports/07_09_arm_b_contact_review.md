# 07_09 — Arm B contact repeatability

Rechecked the existing 29 Arm B-only AlphaFold 3 inputs, four samples per input,
under `/scratch/ghaedi/mab/fab_category_outputs/fab_B_only/`. Used the same
4.5 Å heavy-atom distance and canonical mapping as the
[Arm A review](07_08_arm_a_contact_review.md), checking HB/LB against the eight
intended Arm B residues on chain T. No new inference or jobs.

| Antigen context | Inputs checked | 0 of 4 | 1 of 4 | 2 of 4 | 3 of 4 | 4 of 4 |
|---|---:|---:|---:|---:|---:|---:|
| Cropped antigen | 29 | 1 | 4 | 13 | 9 | 2 |
| 4Ig ectodomain | 29 | 13 | 12 | 3 | 1 | 0 |

The threshold is two or more intended epitope residues in a sample. The
cropped-antigen counts come from the tracked Step 06 per-input TSV.
The two four-of-four cropped hits, B53 and B101, each reached the threshold
in one 4Ig sample.

B282 reached the 4Ig threshold in three samples spanning both seeds with
footprints 240/241, 232/234/236, and 234/236. B131, B114 and B50 reached it
twice each, with recurring contacts at the 228–232 end of the patch.
These counts do not establish repeatable whole-arm orientation or binding.

B20 reached the threshold in one single-arm 4Ig sample. B251 reached it
in zero. Both were identified in distinct dual-contact structures in the
[Arm A review](07_08_arm_a_contact_review.md). The full-ectodomain
confidence-ranked top five from October 21 were B10, B234, B272, B226,
and B124. They reached the intended-site criterion in zero, one, one,
zero, and zero samples, respectively.
