# B7-H3 antibody design QC update

Updated 2026-09-24.

## Current corrected lineage

| Stage | Produced | Passed onward |
|---|---:|---:|
| Target/input QC | 2 arm inputs | 2 |
| RFantibody backbone pilot | 3 usable attempts | 2 accepted backbones |
| ProteinMPNN | 4 sequences, 2 per arm | 4 eligible for RF2 |
| RF2 validation | 4 sequence candidates | 4 outputs produced; 0 passed preliminary geometry QC |

## Results so far

- Arm B backbone passed on the first usable attempt.
- Arm A's first backbone was held because of a 1.758 Å close contact.
- The Arm A retry passed preliminary geometry QC.
- The combined pilot timeout produced no usable backbone.
- ProteinMPNN generated two Arm A candidates and two Arm B candidates.
- RF2 validation job `21741284` completed successfully for all four candidates.
- All four RF2 structures failed the preliminary geometry screen because their
  minimum antibody–target heavy-atom distances were below 2.0 Å.

## What these counts mean

The four current candidates are computational Fv-arm candidates, not confirmed
binders and not final whole IgG antibodies. ProteinMPNN eligibility is not a
binding or activity pass. RF2 confidence and interface metrics will remain
computational evidence and cannot establish affinity, internalization,
Fc-mediated killing, aggregation behavior, or clinical benefit.

The workflow's approximately 10,000-backbone production number is a future
planning range. No production-scale campaign has started. The final number of
whole human IgG-like 1A+1B antibodies is not fixed yet; it depends on RF2,
independent structure validation, Fab-pair geometry, and developability
filtering.

## Current next gate

Diagnose the RFantibody/RF2 coordinate-handling and target-interface problem,
then run only a small corrected representative pilot if the issue is resolved.
No candidate advances to independent validation or whole-IgG assembly, and no
final antibody selection has been made.

## GitHub record

The detailed candidate accounting is also maintained in
`reports/candidate_accounting.md`. This file was added to the tracked project
workspace and pushed with the accompanying status update.
