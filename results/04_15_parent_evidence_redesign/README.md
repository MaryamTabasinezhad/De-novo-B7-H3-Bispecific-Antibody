# 04_15 — Parent-specific GPT-6.2 Sol redesign pilot

Run without Slurm on the connected project shell. After sourcing
`config/hpc/rorqual.sh`, ran
`python3 tools/04_design_sequence/04_13_gpt6_redesign.py <arm> --run-id 04_15_evidence --limit 1`
for A265 and B131. Used `--parent 275` and `--parent 282` for the two
additional, more repeatable candidates.

The worker reads the exact RF2 parent from the 04_09 lineage. It checks
VH/VL identity against the AF3 input, maps RFantibody design-loop labels
to one-based chain positions, and verifies the 4Ig target against Q5ZPR3
positions 29–466. In four AF3 samples per parent it records heavy-atom
contacts to the intended patch at 4.5 Å. Loop labels are design labels
rather than standardized IMGT numbering. All input paths, thresholds,
parent sequences, prompts and model thread IDs are in the individual records.

| Parent | Samples with at least two intended-site residue contacts | GPT-6.2 Sol outcome |
|---|---:|---|
| A265 | 0/4 | Review required. No intended-site contacts observed. |
| A275 | 2/4 | Review required. Sequence unchanged. |
| B131 | 2/4 | Review required. Sequence unchanged. |
| B282 | 3/4 | Review required. Sequence unchanged. |

All four outputs matched the original VH/VL. The requests allowed one or two
loop substitutions while preserving framework and chain length. The model
did not identify a warranted change under that instruction. This is a
prompt and evidence outcome. It does not establish that the parents cannot
be redesigned. No further parents were submitted. A future design comparison
should assess candidate substitutions through structural reprediction against
the corresponding unchanged parent.
