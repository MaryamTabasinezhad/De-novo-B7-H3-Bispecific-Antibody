# AlphaFold3 Validation 1 publication figures

These figures summarize the completed AF3 validation campaign (Slurm job
21999799) using 40 Arm A and 29 Arm B RF2-shortlist inputs, four AF3
seed/sample predictions per input, and 276 sample complexes total. They are
computational structural predictions and do not establish experimental affinity
or biological activity.

## Figure files

- `Figure1_validation_funnel`: RF2 shortlist to AF3 completion, clash-free
  outputs, epitope-contact recovery, and four-sample reproducibility.
- `Figure2_interface_confidence`: Arm A/Arm B distributions for H–L ipTM,
  H–T ipTM, L–T ipTM, and H–T interface PAE.
- `Figure3_contact_heatmaps`: canonical selected-residue contact counts from 0
  to 4 AF3 samples for each RF2 task.
- `Figure4_candidate_structures`: candidate comparison scatter plot plus
  representative structures for Arm A RF2 task 283 and Arm B RF2 task 101.

PNG files are provided for review and PDF files for figure editing or
submission. The `figure_manifest.json` records representative structure
lineage and source tables. Full per-input and per-sample tables remain in
`results/06_02_af3_validation_shortlist/`.

## Caption requirements

Captions must identify these as computational structural predictions. Do not
call a candidate an experimentally confirmed binder, high-affinity antibody, or
validated therapeutic antibody without experimental measurements.
