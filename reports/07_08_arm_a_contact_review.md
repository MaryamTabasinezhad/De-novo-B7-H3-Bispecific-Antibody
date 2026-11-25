# 07_08 — Arm A contact repeatability

Reviewed 2026-11-25 UTC. Inputs were the tracked Step 06 shortlist summaries
and existing Step 07 AlphaFold 3 mmCIFs under
`/scratch/ghaedi/mab/fab_category_outputs/{fab_A_only,fab_AB_pairs}/`.
No inference or scheduler changes were needed.

| Antigen context | Inputs checked | 0 of 4 | 1 of 4 | 2 of 4 | 3 of 4 | 4 of 4 |
|---|---:|---:|---:|---:|---:|---:|
| Arm A with cropped antigen | 40 | 19 | 15 | 4 | 2 | 0 |
| Arm A with 4Ig ectodomain | 40 | 32 | 6 | 2 | 0 | 0 |
| Arm A in dual-arm 4Ig complexes | 280 | 255 | 23 | 2 | 0 | 0 |

Counts refer to models that contact at least two of the four intended Arm A
residues. The dual-arm audit covered four sample CIFs per included input.

## Candidate observations

- **A217** hit the threshold in three cropped-antigen samples. The fourth
  contacted R127 alone. With the 4Ig ectodomain, it contacted F129 alone in
  one of four single-arm samples. In nine dual-arm pairs (36 samples), four
  samples contacted F129 alone and none reached two.
- **A283** hit the threshold in three cropped samples and had zero intended
  contacts in the remaining sample. All four single-arm 4Ig samples had zero
  intended contacts. No four-sample dual-arm pair was available for this arm.
- **A232** met the 4Ig single-arm threshold in two samples from different
  seeds. Their respective footprints were 127–129 and 126–129. The other
  two samples had zero intended contacts. No four-sample dual-arm pair was
  available for A232.
- **A275** contacted R127 and F129 in two 4Ig single-arm samples from seed
  202. The other two samples had zero intended contacts. Across 29 dual-arm
  pairs, eight samples met the Arm A criterion and one met both arms' criteria.

The two positive 4Ig single-arm samples for A275 had more similar
antigen-relative distance patterns than those for A232 (3.7 Å and 6.4 Å,
respectively, using the metric below). Similar footprints leave uncertainty
about overall arm orientation.

Two of 1,120 dual-arm samples contacted at least two intended residues per
arm in the same model. AlphaFold 3 did not flag a clash in either sample.

| Pair | Seed/sample | Arm A contacts | Arm B contacts | Global ipTM |
|---|---|---|---|---:|
| A275/B20 | 202/0 | 127, 128, 129 | 236, 238 | 0.19 |
| A205/B251 | 101/0 | 127, 128, 129 | 240, 241 | 0.18 |

Each hit occurred in one of four samples for its pair. Their low global ipTM
and limited repeatability leave simultaneous binding unverified. A275 is a
candidate for closer interface inspection because it has contact support in
both 4Ig contexts. These are variable-region predictions with the antigen
ectodomain. The analysis leaves native membrane access and full-IgG geometry
open.

## Method and follow-up

Ran a read-only Python standard-library coordinate check after sourcing
`config/hpc/rorqual.sh`. Used the 4.5 Å heavy-atom contact definition from
`tools/06_af3_validation/analyze_af3_shortlist.py`. Parsed the mmCIF atom
columns and assigned HA/LA to Arm A, HB/LB to Arm B, and T to antigen.
Mapped T residue numbers to canonical CD276 by adding 28 for the Step 07
antigen, and verified the IRDF residue identities at 126–129 in each model.
The Arm B contact set was 228, 229, 232, 234, 236, 238, 240, and 241.
For each matched antibody Cα in the two positive single-arm samples, computed
the RMS difference across its distances to six antigen Cα anchors
(126–129, 135, and 140) and took the median across the antibody. This is an
antigen-relative placement check. The reported distance difference is neither
a superposed coordinate RMSD nor a binding score.

Next, inspect the two dual-contact interfaces for paratope placement and
local confidence before advancing a pair to full-IgG geometry assessment.
