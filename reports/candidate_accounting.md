# B7-H3 candidate accounting and QC funnel

Updated 2026-09-24. This report counts the corrected, traceable pilot lineage
and separates attempts, usable outputs, QC passes, and future planned capacity.
No count below is an experimental antibody count or a claim of binding.

## Current corrected lineage

| Stage | Attempts or inputs | Outputs | Passed to next stage | Current disposition |
|---|---:|---:|---:|---|
| Target/input QC | 2 arm windows | 2 corrected continuous target inputs | 2/2 | Passed chain, hotspot-presence, continuity, and pre-existing-clash checks in job `21666857` |
| RFantibody backbone pilot | 3 arm-level attempts with usable output | 3 H/L/T backbones | 2/3 | Arm B from `21676744` passed; Arm A from `21676743` held for a 1.758 Å close contact; Arm A retry `21681492` passed |
| ProteinMPNN pilot | 2 accepted backbones | 4 sequences (2 per arm) | 4/4 eligible for RF2 | Job `21719319` completed; scores are sequence-model scores, not affinity |
| RF2 validation | 4 sequence candidates | Pending | 0 confirmed until QC completes | Job `21741284` is pending Slurm priority |

The accepted backbone set entering ProteinMPNN is therefore **two arm-specific
Fv designs**: one Arm A retry and one Arm B design. The four current sequence
IDs are:

| Arm | Candidate | ProteinMPNN score | RF2 status |
|---|---|---:|---|
| A | `ab_0_dldesign_0` | 1.0752 | Pending in job `21741284` |
| A | `ab_0_dldesign_1` | 1.1878 | Pending in job `21741284` |
| B | `ab_0_dldesign_0` | 1.3557 | Pending in job `21741284` |
| B | `ab_0_dldesign_1` | 1.4213 | Pending in job `21741284` |

The broad RFantibody target windows are QC/context windows, not complete
epitope definitions: Arm A is canonical 86–169 and Arm B is 188–281. The
smaller design anchors are Arm A 126–129 and Arm B 228, 229, 232, 234, 236,
238, 240, and 241.

## Attempts excluded from the corrected lineage

- Combined corrected pilot `21670962` reached the time limit before producing
  either arm PDB. It produced **zero usable backbones** and was an execution
  failure, not a scientific rejection.
- The earlier RFantibody pilots and their RF2 outputs are historical diagnostic
  runs. Their severe coordinate overlaps and B-arm hotspot warning caused them
  to be rejected for ranking; they are not counted as current candidates.

## Planned capacity versus work actually done

The workflow describes a production campaign of approximately **10,000 total
RFantibody backbones** across anchor sets, CDR lengths, poses, and seeds, and
typically **5–20 ProteinMPNN sequences per retained backbone**. Those are
planning ranges, not completed work or an authorization to launch a production
campaign. The current work is deliberately a small pilot: one accepted
backbone per arm and two sequences per backbone.

After RF2, candidates must pass structural/interface QC before any survivor is
sent to independent AlphaFold 3 or RF3 validation. Only after those filters
would the workflow begin parent selection, Fab-pair geometry, simultaneous
same-antigen modeling, complete 1A+1B IgG-Fc assembly, and developability
ranking. At present, the number of RF2 survivors is **zero confirmed** because
the job has not completed.

## Interpretation

The pipeline has produced computational Fv-arm prototypes, not a final
therapeutic antibody. A ProteinMPNN candidate is not counted as a passed binder;
it is only eligible for structural validation. RF2 confidence and interface
metrics will remain computational evidence and cannot establish affinity,
internalization, Fc-mediated killing, aggregation behavior, or clinical benefit.
