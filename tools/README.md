# Project execution stream

The numbered subdirectories mirror the scientific workflow. Read them in order.
Shell workers are submitted through Slurm; Python files are analysis or preparation utilities.

| Stage | Directory | Purpose |
|---|---|---|
| `01` | `01_target_input_qc/` | Prepare and validate target/antibody input structures |
| `04` | `04_design_sequence/` | RFantibody backbone generation and ProteinMPNN sequence design |
| `05` | `05_rf2_qc/` | RF2 prediction, geometry QC, interface analysis, and shortlist construction |
| `06` | `06_af3_validation/` | AlphaFold 3 input preparation and independent validation |
| `99` | `99_runtime_support/` | Runtime checks, installation workers, and support utilities |

The executable names inside each directory remain descriptive. A task is only complete when its numbered report, matching result directory, status entry, and Slurm record agree.
