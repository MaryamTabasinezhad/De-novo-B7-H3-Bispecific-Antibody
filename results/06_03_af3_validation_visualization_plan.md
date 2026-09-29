# AlphaFold 3 Arm A and Arm B validation visualization plan

This document defines how the current AF3 validation data should be presented
for scientific review. It is a visualization specification only; it does not
run analysis or create figures. The underlying data are the 69 RF2 shortlist
inputs and their 276 AF3 seed/sample complexes recorded in
`results/06_02_af3_validation_shortlist/`.

## 1. QC funnel

Create separate Arm A and Arm B funnels showing the number of models at each
stage:

`RF2 shortlist → AF3 completed → no-clash models → models with epitope contacts → models with reproducible contacts`

The funnel must distinguish model counts from candidate counts. Four AF3
samples from one RF2 input are repeated predictions, not four independent
antibody sequences. The current campaign has 40 Arm A and 29 Arm B inputs, with
four AF3 samples per input.

## 2. Confidence distributions

Use paired boxplots or violin plots for Arm A and Arm B. Plot the following
metrics separately:

- H–L ipTM: internal heavy/light antibody pairing;
- H–T ipTM: heavy-chain contact confidence with B7-H3;
- L–T ipTM: light-chain contact confidence with B7-H3;
- H–T and L–T minimum interface PAE.

The plot should make the distinction between antibody folding and target
interface confidence visually obvious. Do not combine these into one score.

## 3. Candidate ranking scatter plot

Represent each RF2 task as one point. Recommended axes are:

- x-axis: mean H–T ipTM across the four AF3 samples;
- y-axis: number of AF3 samples contacting at least one selected epitope
  residue;
- color: Arm A versus Arm B;
- point size: RF2 interface-contact count or another explicitly named RF2
  structural measure.

This plot separates candidates with stronger predicted interface confidence from
candidates that make geometric contacts without strong AF3 confidence. A point
must retain its arm and RF2 task identifier in an accompanying table.

## 4. Contact-reproducibility heatmaps

Create one heatmap for Arm A and one for Arm B:

- rows: RF2 task identifiers;
- columns: canonical selected epitope residues;
- cell value: number of AF3 samples, from 0 to 4, contacting that residue;
- row annotation: mean H–T ipTM, mean L–T ipTM, and RF2 contact count.

Arm A columns should include residues 126–129. Arm B columns should include
228, 229, 232, 234, 236, 238, 240, and 241. The heatmaps should preserve
canonical CD276 numbering and must not mix target-fragment numbering with
canonical numbering.

## 5. Representative molecular views

For selected follow-up candidates, show the AF3 complex in a molecular viewer:

- B7-H3 target in one color;
- antibody heavy and light chains in different colors;
- selected epitope residues highlighted as sticks;
- predicted contact residues shown as sticks or dashed contact lines;
- optional side-by-side comparison with the original RF2 pose.

These views are useful for checking whether a numerical contact is a coherent
binding pose or an isolated atom-level proximity. They should support the
tables and plots, not replace them.

## 6. Recommended dashboard layout

The main Arm A/Arm B dashboard should contain:

1. the two-arm QC funnel;
2. confidence-distribution panels;
3. the candidate ranking scatter plot; and
4. the two contact-reproducibility heatmaps.

Representative molecular views should be placed in a subsequent figure or
supplementary panel. Every point, row, and structure must retain the RF2 task,
arm, AF3 seed, and AF3 sample identifiers needed to trace it back to the raw
prediction.

## 7. Scientific labeling rules

All figures must label these as computational structural predictions. They must
not use terms such as “confirmed binder,” “high-affinity,” or “validated
therapeutic antibody.” H–L confidence supports internal antibody geometry;
H–T/L–T confidence and epitope contacts are evidence about a predicted
antibody–target pose. Neither establishes experimental affinity, specificity,
internalization, Fc-mediated killing, aggregation stability, or clinical
benefit.
