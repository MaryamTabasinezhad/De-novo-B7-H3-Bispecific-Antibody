# B7-H3 RF2 pilot QC

Updated 2026-09-24. Slurm job `21741284` completed with exit code 0 using
three requested recycles, `RF2_ab.pt`, seed 101 for Arm A, and seed 202 for
Arm B. RF2 produced one best PDB for each of the four ProteinMPNN candidates.

## Output summary

| Arm | Candidate | Best RF2 pLDDT | Minimum H/L–T heavy-atom distance | H/L–T contacts <4.5 Å | Preliminary disposition |
|---|---|---:|---:|---:|---|
| A | `ab_0_dldesign_0` | 0.916 | 0.422 Å | 1117 | Reject geometry QC |
| A | `ab_0_dldesign_1` | 0.923 | 0.122 Å | 9990 | Reject geometry QC |
| B | `ab_0_dldesign_0` | 0.899 | 0.291 Å | 820 | Reject geometry QC |
| B | `ab_0_dldesign_1` | 0.892 | 1.016 Å | 546 | Reject geometry QC |

All four outputs retained H, L, and T chains and were written to
`/scratch/ghaedi/mab/rfantibody_b7h3_rf2_20260924/{A,B}/`. The pLDDT values are
model confidence values, not affinity measurements.

## QC interpretation

The four predicted complexes contain physically implausible heavy-atom
overlaps: every minimum H/L–T distance is below the preliminary 2.0 Å severe
overlap screen. The very large numbers of nominal contacts are consistent with
coordinate collapse or an input/output geometry problem, so these structures
cannot be used as evidence for productive binding or ranked as antibody
candidates.

This is a completed computational run with a failed geometry QC outcome. It is
not evidence that Arm A, Arm B, or the selected B7-H3 epitopes are biologically
invalid. It also does not establish or exclude internalization, Fc-mediated
killing, aggregation behavior, or clinical activity.

## Funnel consequence

The four ProteinMPNN sequences entered RF2, and **0/4 passed the RF2 geometry
screen**. No candidate advances to AlphaFold 3, RF3, whole-IgG assembly, or
production-scale design from this pilot. The next technical gate is diagnosis
of RFantibody/RF2 coordinate handling and target-crop/interface representation,
followed by a small corrected representative pilot only if the issue is
resolved.
