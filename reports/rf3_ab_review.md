# RF3-ab: what exists and how it could be used

Updated 2026-09-25.

## Executive answer

RosettaCommons publicly documents **RF3**, a general all-atom RoseTTAFold3
structure-prediction model. The current public materials do not identify a
separate antibody-finetuned checkpoint officially named `RF3-ab`, analogous to
RFantibody's `RF2_ab` checkpoint.

Therefore, “RF3-ab” should be treated as shorthand for **using general RF3 on
an antibody–antigen complex**, unless RosettaCommons later releases and names a
dedicated antibody-finetuned RF3 model. It should not be described as an
officially released model name in project reports without a specific checkpoint
and source.

## What RF3 is

RF3 is the RoseTTAFold3 all-atom biomolecular structure-prediction system in
the RosettaCommons Foundry. Its design target is broad biomolecular modeling,
including proteins and complexes, with atom-level geometric conditioning. The
public RF3 documentation describes general structure prediction and complex
modeling; it does not define an antibody-specific RF3 checkpoint.

The current RF3 documentation also states that its inference API, input formats,
and confidence outputs are still undergoing cleanup and stabilization. A
reproducible project use therefore requires recording the exact Foundry version,
checkpoint, input schema, inference settings, seeds, and confidence fields.

## What “RF3-ab” would mean in this project

If we use general RF3 to repredict a designed antibody–B7-H3 complex, the
operation would be:

1. Provide the antibody heavy chain, light chain, and B7-H3 target as an RF3
   input complex.
2. Exclude the RFantibody-designed interface as a structural template.
3. Generate multiple RF3 samples and seeds.
4. Measure antibody CDR recovery, target-chain movement, interface contacts,
   interface confidence, predicted alignment error, and severe clashes.
5. Compare whether the predicted pose supports the intended Arm A or Arm B
   epitope across samples.

This would be an **RF3 antibody–antigen validation use case**, not proof that an
antibody-specific `RF3_ab.pt` model exists.

## Difference from RF2_ab

| Property | RF2_ab | General RF3 used on an antibody complex |
|---|---|---|
| Model specialization | Antibody-finetuned RF2 model in RFantibody | General all-atom biomolecular model |
| Role in this project | Primary RFantibody self-consistency validator | Independent complementary validation layer |
| Public project checkpoint | `RF2_ab.pt` is present in the RFantibody installation | No project-verified `RF3-ab` checkpoint |
| Input/API maturity | Verified here through official and B7-H3 controls | Not installed or validated here |
| Main value | Antibody-specific filtering after ProteinMPNN | Independent pose, interface, and disagreement analysis |
| Interpretation | Computational structural evidence | Computational structural evidence |

RF2_ab remains the primary validation model for the current RFantibody
workflow. RF3 would be useful only after the RF2 stage and its QC behavior are
understood, or as a separately authorized independent comparison. RF3 outputs
must not be scored with RF2_ab thresholds without calibration.

## What RF3 could add for the B7-H3 project

For a candidate that passes the RF2 geometry gate, general RF3 could provide:

- an independently generated antibody–B7-H3 pose;
- agreement or disagreement with the RF2_ab interface;
- alternative CDR conformations and approach vectors;
- target-chain and epitope-contact consistency across samples;
- all-atom clash and interface inspection;
- confidence and predicted-alignment-error fields for a complementary scorecard.

Agreement between RF2_ab and RF3 would strengthen computational confidence in a
pose. Disagreement would trigger review and additional modeling; it would not
automatically reject a candidate because the predictors have different training,
architectures, inputs, and confidence definitions.

## What RF3 cannot establish

RF3 cannot by itself establish:

- measured affinity or kinetics;
- internalization into B7-H3-expressing cells;
- Fc-mediated tumor-cell killing;
- correct whole-IgG heavy-chain heterodimerization or light-chain pairing;
- low aggregation, expression yield, viscosity, or formulation stability;
- human safety or clinical benefit;
- simultaneous cis binding of both Fab arms to one native B7-H3 molecule.

Those claims require construct-level modeling, biophysical measurements, cellular
assays, and later experimental validation.

## Current project decision

No RF3 job is authorized or running in the current project. The active pipeline
is:

1. RFantibody antibody-finetuned RFdiffusion backbone generation.
2. ProteinMPNN CDR sequence design.
3. RF2_ab structural validation.
4. Later, if a candidate passes the RF2 gate and the runtime is verified, general
   RF3 may be added as an independent complementary predictor.

The current 300-backbone-per-arm pilot is therefore not blocked by the absence
of a model called `RF3-ab`. RF3 should be added only with a pinned checkpoint,
validated runtime, explicit input conversion, and RF3-specific QC criteria.

## Sources

- [RosettaCommons RFantibody documentation](https://github.com/RosettaCommons/RFantibody) — describes the RFantibody pipeline as antibody-finetuned RFdiffusion, ProteinMPNN, and antibody-finetuned RoseTTAFold2 filtering.
- [RosettaCommons Foundry RF3 documentation](https://github.com/RosettaCommons/foundry/blob/production/models/rf3/README.md) — describes general RF3, available checkpoints, input/inference usage, and current API stabilization caveats.
- [Foundry pull request for an RF3 antibody–antigen tutorial](https://github.com/RosettaCommons/foundry/pull/263) — evidence that antibody–antigen use is being documented, but not evidence of a separately released `RF3-ab` checkpoint.
