# Official RF2 control result

Updated 2026-09-24. The bundled RFantibody H/L/T example
(`scripts/examples/rf2/example_inputs/ab_proteinmpnn_output.pdb`) was run
through the tracked control wrapper
`tools/rfantibody_rf2_official_control_job.sh` as Slurm job `21747881`.

## Runtime

- Exit status: 0
- Elapsed time: 1 minute 8 seconds
- Model: `RF2_ab.pt`
- Recycles: 3 requested (RF2 log reports four refinement cycles including the
  initial pass)
- Seed: 101
- Cautious mode: enabled
- Output: `/scratch/ghaedi/mab/rfantibody_rf2_official_control_20260924/`

RF2 produced one best PDB with H, L, and T chains and best pLDDT `0.903`.

## Shared geometry check

| Output | H atoms | L atoms | T atoms | Minimum H/L–T distance | Contacts <4.5 Å | Overlaps <2.0 Å | Closest pair |
|---|---:|---:|---:|---:|---:|---:|---|
| `ab_proteinmpnn_output_best.pdb` | 1421 | 1283 | 3087 | 2.229 Å | 48 | 0 | H:59ARG–243ASN |

The same tracked checker used on the B7-H3 RF2 outputs reports no severe
sub-2 Å antibody–target overlap for the official example. The runtime,
official weights, H/L/T parser path, and geometry calculation therefore pass
this control.

## Interpretation and consequence

The RF2 failure on B7-H3 is unlikely to be explained by a universal runtime or
clash-checker failure. It is more likely related to B7-H3 input/output
representation, target-crop geometry, chain/residue handling, or the specific
RFantibody-generated complexes. This control does not rescue the four B7-H3
outputs: those remain rejected because all four had sub-2 Å overlaps.

The next diagnostic should compare a B7-H3 RFantibody backbone and its
ProteinMPNN input against the RF2 output using the same parser and coordinate
checks. No independent predictor, whole-IgG assembly, or production campaign is
authorized by this control result.
