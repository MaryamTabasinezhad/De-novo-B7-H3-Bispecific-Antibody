# B7-H3 ProteinMPNN pilot

ProteinMPNN job `21719319` completed on 2026-09-24 with exit code 0. It used
the accepted Arm A retry and Arm B backbone, designed the six CDR loops, used
temperature 0.1, generated two deterministic sequences per backbone, and ran
on the GPU without errors.

| Arm | Candidate | ProteinMPNN score |
|---|---|---:|
| A | `ab_0_dldesign_0` | 1.0752 |
| A | `ab_0_dldesign_1` | 1.1878 |
| B | `ab_0_dldesign_0` | 1.3557 |
| B | `ab_0_dldesign_1` | 1.4213 |

Outputs are retained in
`/scratch/ghaedi/mab/rfantibody_b7h3_mpnn_20260923/output/{A,B}/`.
The two sequence candidates per arm are distinct at designed CDR positions;
the framework and target chains are retained in each output PDB. The scores are
ProteinMPNN model scores, not affinity or activity measurements.

The four candidates are eligible for the bounded RF2 structure-prediction
check. RF2 will be used to assess structural plausibility and interfaces, not
to claim experimental binding.
