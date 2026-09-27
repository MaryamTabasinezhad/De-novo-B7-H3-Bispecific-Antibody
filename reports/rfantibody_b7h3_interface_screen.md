# RF2 interface screen

Date: 2026-09-27 04:19 UTC  
Slurm job: `21885408`  
Inputs: geometry-passing RF2 models from `results/rfantibody_b7h3_rf2_qc_20260927/`

The screen counted heavy-atom antibody–target contacts within 4.5 Å for each
geometry-passing model. RF2 renumbers the target chain, so target residues were
mapped back to the canonical crop by sequence-verified offset: Arm A crop
86–169 and Arm B crop 188–281. The sequence of the RF2 target chain matched
the corresponding corrected input crop for representative outputs.

| Arm | Geometry-passing models | Any target contact | Any selected-epitope contact | At least 2 selected residues | Both H and L contact target |
|---|---:|---:|---:|---:|---:|
| A | 167 | 162 | 70 | 37 | 98 |
| B | 155 | 148 | 129 | 98 | 107 |

Selected residues were Arm A 126–129 (8H9-like IgV1 FG-loop) and Arm B 228,
229, 232, 234, 236, 238, 240 and 241 (coordinate-derived IgC1 patch 2).
The screen is a contact-coverage filter, not an affinity or biological assay.
No numerical interface cutoff has been approved, so these counts are retained
for review rather than treated as final candidate acceptance. The per-model
records, including contacted selected residues and antibody-chain coverage,
are in `results/rfantibody_b7h3_interface_20260927/`.
