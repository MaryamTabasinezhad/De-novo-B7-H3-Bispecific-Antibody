# B7-H3 RF2 coordinate and chain audit

Updated 2026-09-24. This audit compares the accepted RFantibody backbone, the
ProteinMPNN input/output PDBs, and the RF2 best outputs using the tracked
`tools/audit_rfantibody_coordinate_chain.py` and corrected heavy-atom geometry
parser.

## Input-to-output comparison

| Arm/stage | Target span | Minimum H/L–T distance | Contacts <4.5 Å | Overlaps <2.0 Å | Shared target atoms | Target RMSD vs backbone |
|---|---|---:|---:|---:|---:|---:|
| A backbone | 223–306 | 2.768 Å | 54 | 0 | 336 | 0.000 Å |
| A ProteinMPNN input/output | 223–306 | 2.768 Å | 54 | 0 | 336 | 0.000 Å |
| A RF2 candidate 0 | 223–306 | 0.422 Å | 454 | 37 | 336 | 1.268 Å |
| A RF2 candidate 1 | 223–306 | 0.331 Å | 4341 | 371 | 336 | 0.326 Å |
| B backbone | 228–321 | 3.047 Å | 20 | 0 | 376 | 0.000 Å |
| B ProteinMPNN input/output | 228–321 | 3.047 Å | 20 | 0 | 376 | 0.000 Å |
| B RF2 candidate 0 | 228–321 | 0.291 Å | 337 | 23 | 376 | 0.383 Å |
| B RF2 candidate 1 | 228–321 | 1.485 Å | 170 | 2 | 376 | 5.430 Å |

The RFantibody backbone and ProteinMPNN files are exact geometry-preserving
copies for the target chain in each arm: all shared target atoms have 0.000 Å
RMSD and both inputs have zero sub-2 Å antibody–target overlaps. The severe
overlaps are introduced in the RF2 outputs, not by the target windows or
ProteinMPNN file-writing step.

## Parser correction

The first geometry pass used a fallback that could treat digit-prefixed atom
names such as `1HG2` or `2HE2` as non-hydrogen atoms when the PDB element field
was blank. The shared checker and audit now infer a missing element from the
first alphabetic character of the atom name. Reanalysis gives the official RF2
control a minimum heavy-atom distance of 3.167 Å, six contacts below 4.5 Å,
and zero overlaps below 2.0 Å. The B7-H3 RF2 outputs still fail after this
correction, with the values shown above.

## Interpretation

The official control passes while all four B7-H3 outputs fail, and the B7-H3
inputs themselves are geometrically clean. The immediate problem is therefore
specific to RF2's handling or prediction of these B7-H3 complexes (including
target movement or interface reconstruction), rather than a universal runtime
failure or a ProteinMPNN coordinate corruption. No B7-H3 candidate advances to
independent validation or whole-IgG assembly.
