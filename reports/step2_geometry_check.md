# Step 2 — preliminary same-antigen geometry check

Prepared 2026-09-21 after the user confirmed the preliminary pair in
`reports/step2_epitope_evidence.md`.

## Pair carried forward

| Arm | Preliminary target | Canonical residues used for the geometry screen |
|---|---|---|
| A | 8H9-like exposed IgV1 FG-loop | 126–129 (`IRDF`); R127 and F129 were the independent exposure-screen hits |
| B | Coordinate-derived exposed IgC1 patch 2 | Q228, Q229, H232, S234, T236, T238, Q240 and R241 |

## Coordinate result

The screen used the oriented unbound AlphaFold model and the oriented 9LY6
human B7-H3 chain. In the unbound model, the A/B patch centroid separation was
approximately **61.6 Å** and the minimum heavy-atom separation was approximately
**33.5 Å**. In 9LY6, the corresponding values were approximately **62.0 Å**
and **34.2 Å**. These measurements support distinct surface locations, but they
are not a Fab-reach or simultaneous-binding result.

The selected IgV1 patch is membrane-distal. The selected IgC1 patch is a
separate exposed surface and is adjacent to, with partial overlap at the edge
of, the broader 20G5 region; it is not assumed to be the 20G5 footprint.

## Interpretation and remaining gate

The pair is suitable for a preliminary 1A + 1B geometry test. The calculation
did not generate antibody poses and did not test Fab approach vectors, hinge
flexibility, glycan shielding, membrane clearance, or simultaneous binding to
one native cell-surface 4Ig molecule. Those checks must precede sequence design.
The outputs are `metadata/candidate_regions.csv`,
`metadata/binder_epitope_evidence.csv`, `metadata/epitope_pair_geometry.csv`,
`config/epitopes.yaml`, and the local geometry record under
`work/02_epitope_selection/`.
