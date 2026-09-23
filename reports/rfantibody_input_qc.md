# RFantibody input-pipeline QC

Updated 2026-09-23. This QC validates input formatting and geometry before any
new RFantibody design run.

## Root causes found

1. The original preparation script selected chain A from
   `human_4ig_20G5_fab_oriented.pdb`. In that structure chain A is a 20G5 Fab,
   not B7-H3. The resulting RFantibody targets were the wrong molecule.
2. The original 12 Å spatial crop retained disconnected residue fragments,
   producing large Cα gaps in the target chain. Such a crop is not a continuous
   polymer input for RFantibody.

The tracked preparer now uses the full-target AFDB structure
`data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb`, selects its
B7-H3 chain A explicitly, and retains contiguous sequence windows with 40
residues of padding around each selected epitope. The generated scratch inputs
are under `/scratch/ghaedi/mab/rfantibody_inputs_corrected3/`.

## Slurm validation

- Failed diagnostic job `21666840`: used the earlier disconnected spatial crop;
  it reported target Cα gaps and correctly returned a nonzero QC status.
- Passing validation job `21666857`: ran the tracked
  `tools/validate_rfantibody_inputs.py` through
  `tools/validate_rfantibody_inputs_job.sh` and wrote
  `reports/rfantibody_input_qc.json`.

| Arm | Target window | H/L/T CA counts | Missing hotspots | Cα gaps >4.5 Å | Minimum pre-existing H/L–T distance | Result |
|---|---:|---:|---|---|---:|---|
| A | 86–169 | 116/107/84 | none | none | 146.093 Å | PASS |
| B | 188–281 | 116/107/94 | none | none | 130.451 Å | PASS |

These checks establish input identity, chain order, hotspot presence, chain
continuity, and absence of pre-existing antibody–target overlap. They do not
establish that RFantibody will generate a valid binder. The next controlled
check is one official RFantibody runtime example, followed by one new design per
arm using these corrected inputs.
