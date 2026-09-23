# Corrected B7-H3 RFantibody backbone QC

Jobs `21676743` (Arm A) and `21676744` (Arm B) completed successfully on
2026-09-23. Each generated one H/L/T Fv-target backbone using the corrected
AFDB-target crops, default diffusion horizon, and the approved hotspots.

| Arm | Output | Logged motif RMSD range | Hotspot sequence | Minimum H/L–T heavy-atom distance | H/L–T contacts <4.5 Å | Initial disposition |
|---|---|---:|---|---:|---:|---|
| A | `/scratch/ghaedi/mab/rfantibody_b7h3_arm_pilots_20260923/A/ab_0.pdb` | 0.24–0.34 Å | IRDF | 1.758 Å | 44 | Hold: one severe close contact |
| B | `/scratch/ghaedi/mab/rfantibody_b7h3_arm_pilots_20260923/B/ab_0.pdb` | 0.27–0.35 Å | QQHSTTQR | 3.047 Å | 20 | Provisional pass |

Both outputs retained H/L/T chains and the expected target crop. The Arm A
closest pair is an antibody-chain L212 oxygen and target-chain T228 nitrogen at
1.758 Å; this is below the preliminary 2.0 Å severe-overlap screen. Arm B had
no H/L–T atom pair below 3.0 Å. Motif RMSD and hotspot sequences show that the
corrected inputs are being handled by RFantibody, but they do not establish
affinity or biological activity.

Arm B may proceed to a bounded ProteinMPNN/RF2 check after the Arm A retry is
recorded. Arm A is held for a fresh backbone draw; no final arm or whole-IgG
claim is made.
