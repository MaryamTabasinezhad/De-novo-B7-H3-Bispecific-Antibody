# B7-H3 project report stream

Read the reports in numeric order. The two-digit prefix is the workflow step; the second number is the document within that step.

| Order | Stage | Read these files |
|---|---|---|
| `00` | Scope, evidence policy, decisions, live status | `00_01_scope.md`, `00_02_screening_policy.md`, `00_03_isoform_review.md`, `00_04_fc_pairing_review.md`, `00_05_decision_log.md`, `00_06_status.md` |
| `01` | Target preparation | `01_01_target_preparation.md` |
| `02` | Epitope evidence and geometry | `02_01_epitope_evidence.md`, `02_02_geometry_check.md` |
| `03` | Design anchors | `03_01_design_anchor_candidates.md` |
| `04` | RFantibody, ProteinMPNN, and input/backbone QC | `04_01_backbone_sequence_pilot.md` through `04_08_rfantibody_pilot_qc.md` |
| `05` | RF2 QC, interface analysis, and candidate shortlist | `05_01_rf2_qc.md` through `05_06_qc_update.md` |
| `06` | Independent structure validation | `06_01_alphafold3_validation_results.md`, `06_02_rf3_ab_review.md` |
| `07` | Candidate accounting and advancement decision | `07_01_candidate_accounting.md` |

Read `00_06_status.md` for the current active job and next authorized stage. A report is not a completed result unless its corresponding durable artifact appears under the matching numbered `results/` directory.
