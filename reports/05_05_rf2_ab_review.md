# RF2_ab: scientific meaning and role in this project

Updated 2026-09-25.

## Executive answer

**RF2_ab is an antibody-finetuned RoseTTAFold2 structure-prediction model used
to repredict and filter designed antibody–antigen complexes.** In the
RFantibody workflow, RF2_ab comes after antibody-finetuned RFdiffusion backbone
generation and ProteinMPNN sequence design. It tests whether a designed amino
acid sequence can recover a plausible antibody structure and target interface
when modeled again.

RF2_ab is a computational structural-validation model. It is not an affinity
calculator, a cell assay, or evidence of therapeutic activity.

## What the name means

- **RF:** RoseTTAFold, a neural-network structure-prediction family.
- **2:** RoseTTAFold2 generation/model family.
- **ab:** antibody-finetuned training and inference intended for antibody
  structures and antibody–antigen complexes.

The `ab` suffix is scientifically important. Generic protein structure models
can struggle with antibody CDR loops, VH/VL geometry, and antibody–antigen
interfaces. RF2_ab is tuned to antibody structural patterns and is therefore
more appropriate for this pipeline than treating a generic protein predictor as
the only design filter.

## Where RF2_ab fits in the design funnel

### 1. RFantibody backbone generation

The antibody-finetuned RFdiffusion component proposes antibody backbone shapes
and docking poses against the chosen B7-H3 hotspot region. At this point the
CDR backbone geometry is designed, but the final CDR amino-acid sequences are
not yet selected.

### 2. ProteinMPNN sequence design

ProteinMPNN designs CDR sequences that fit each retained backbone. This is an
inverse-folding step: it asks which sequences are compatible with a supplied
backbone and fixed framework. A high ProteinMPNN score does not prove that the
sequence will preserve the intended antibody–B7-H3 complex when independently
predicted.

### 3. RF2_ab reprediction

RF2_ab receives the designed antibody sequence and the B7-H3 target and
generates a new predicted complex. It is not supposed to simply copy the
original RFantibody pose. The comparison between the original design and the
RF2_ab prediction can reveal whether the sequence supports the intended
structure and interface.

## What RF2_ab evaluates scientifically

For each designed sequence, we inspect:

- antibody chain labels and sequence/structure integrity;
- VH/VL and CDR structural recovery;
- CDR backbone deviation from the RFantibody design;
- target-chain movement and residue mapping;
- recovery of contacts around the intended epitope anchors;
- interface contact-map consistency;
- pLDDT or related model-confidence fields;
- predicted alignment-error/interface-confidence fields when available;
- antibody–target heavy-atom clashes and coordinate collapse;
- whether the predicted pose remains on the intended B7-H3 surface.

These measurements are used as staged computational gates. They are not
combined into a falsely precise affinity score.

## Why this project needs RF2_ab

Our workflow creates separate Arm A and Arm B antibodies against B7-H3. Each
arm can look acceptable at the backbone stage while its redesigned CDR
sequence changes the structure. RF2_ab is needed to detect that failure before
we spend compute on larger validation layers or assemble a whole 1A+1B IgG.

For this project, RF2_ab can identify:

1. **Sequence-to-backbone incompatibility:** the ProteinMPNN sequence does not
   preserve the designed CDR conformation.
2. **Loss of epitope engagement:** the predicted CDRs no longer contact the
   Arm A FG-loop or Arm B IgC1 patch-2 region.
3. **Unproductive redocking:** the antibody moves away from the intended
   B7-H3 surface or adopts a different orientation.
4. **Steric failure:** antibody and target atoms overlap or the interface
   collapses into an implausible coordinate arrangement.
5. **Candidate prioritization:** only structurally plausible sequences proceed
   to independent predictors, developability review, and later Fab-pair or
   whole-IgG modeling.

Without this step, a sequence could be accepted because it fits the original
RFantibody backbone even though an independent structure prediction does not
support that pose.

## What RF2_ab does not prove

An RF2_ab pass does not establish:

- measured affinity, kinetics, or specificity;
- internalization into B7-H3-expressing cells;
- Fc-mediated tumor-cell killing;
- simultaneous binding of both Fab arms to one native human 4Ig B7-H3 molecule;
- correct cFAE/CrossMab assembly or whole-IgG pairing;
- low aggregation, expression yield, viscosity, or formulation stability;
- human safety or clinical benefit.

Those properties require additional modeling and experimental assays.

## Current project implementation

The project uses the RFantibody installation's `RF2_ab.pt` weights after
ProteinMPNN. The official bundled RF2 H/L/T control completed successfully in
Slurm job `21747881`. Its corrected shared geometry check reported a best
pLDDT of `0.903`, a minimum heavy-atom H/L–T distance of `3.167 Å`, six
contacts below `4.5 Å`, and zero overlaps below `2.0 Å`.

The earlier four-sequence B7-H3 diagnostic RF2 run produced outputs, but all
four failed the preliminary heavy-atom geometry gate. The input backbone and
ProteinMPNN files were clean, so the result is retained as a B7-H3-specific
RF2 output/representation problem rather than treated as evidence that the
epitopes cannot bind. The current 300-backbone-per-arm pilot is generating a
broader candidate pool; RF2_ab remains the downstream validation gate after
ProteinMPNN.

## RF2_ab versus RF3

RF2_ab is the antibody-specific model currently integrated and validated in
the RFantibody pipeline. RF3 is a newer general all-atom structure-prediction
system. General RF3 may later provide an independent antibody–antigen
validation layer, but it should not replace RF2_ab without a pinned checkpoint,
validated runtime, and RF3-specific calibration.

## Sources

- [RosettaCommons RFantibody documentation](https://github.com/RosettaCommons/RFantibody) — identifies RFantibody as antibody-finetuned RFdiffusion for backbone design, ProteinMPNN for sequence design, and antibody-finetuned RoseTTAFold2 for in-silico filtering.
- [RFantibody RF2 usage documentation](https://github.com/RosettaCommons/RFantibody#rf2) — describes the RF2 stage and command-line usage in the official pipeline.
- [Atomically accurate de novo design of antibodies with RFdiffusion](https://pmc.ncbi.nlm.nih.gov/articles/PMC12727541/) — reports the antibody-design workflow and the use of fine-tuned RoseTTAFold models for structural prediction and filtering.
- [RosettaCommons Foundry RF3 documentation](https://github.com/RosettaCommons/foundry/blob/production/models/rf3/README.md) — documents general RF3 and its separate runtime/API status.
