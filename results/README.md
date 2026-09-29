# B7-H3 project result stream

Results are grouped by the workflow stage that produced them. Read directories in numeric order; directory names use `step_substep_description_date`.

| Order | Stage | Directory |
|---|---|---|
| `05_01` | RF2 structural QC | `05_01_rf2_qc_20260927/` |
| `05_02` | RF2 interface screen | `05_02_interface_screen_20260927/` |
| `05_03` | RF2 control-gate shortlist | `05_03_control_shortlist_20260927/` |
| `06_01` | AlphaFold 3 independent validation pilot | `06_01_af3_validation_pilot/` |
| `06_02` | AlphaFold 3 full RF2-shortlist validation | `06_02_af3_validation_shortlist/` |
| `06_03` | AlphaFold 3 validation visualization plan | `06_03_af3_validation_visualization_plan.md` |

Raw model weights, full databases, Slurm scratch outputs, and caches remain outside Git in documented scratch paths. Tracked result directories contain the reviewable derived artifacts and provenance needed to interpret them.

The AF3 directory contains a representative pilot, not a full-shortlist
campaign. RF2 had 42 Arm A and 30 Arm B geometry-gate models before
task-level deduplication, but AF3 evaluated only RF2 task 265 (Arm A) and task
131 (Arm B). Two seeds and two diffusion samples produced four complexes per
arm. The purpose and limitations of that sampling are documented in
`reports/06_01_alphafold3_validation_results.md`.

The `06_02` campaign is the current decision-stage validation: 40 Arm A plus
29 Arm B RF2-shortlist inputs, two seeds, and two diffusion samples per input.
It will produce up to 276 predicted complexes. Outputs are promoted into this
directory only after the Slurm run and derived contact/QC summaries have been
inspected.

| `06_04` | AlphaFold3 Validation 1 publication figures | `Alphafold3_Validation1_figures/` |

The publication figures are derived from the tracked AF3 shortlist tables and
retain RF2 task identifiers for traceability. They are computational structural
predictions; no experimental binding or biological activity is inferred.
