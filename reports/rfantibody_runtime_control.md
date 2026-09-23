# RFantibody runtime-control result

The tracked official-example control job `21666899` completed on 2026-09-23
with Slurm exit code 0. It used RFantibody's packaged RSV target and hu-4D5-8
Fv framework, one deterministic RFdiffusion design, and the official
`RFdiffusion_Ab.pt` weights.

- Output: `/scratch/ghaedi/mab/rfantibody_runtime_control/ab_0.pdb`
- Chains: H/L/T, with 116/107/251 residues
- Logged motif RMSD: `0.13 Å`
- Minimum H/L–T heavy-atom distance: `2.969 Å`
- H/L–T heavy-atom contacts under 4.5 Å: 28
- Runtime errors: none

This control establishes that the installed RFantibody runtime, model weights,
framework parsing, diffusion settings, and output writing work on the selected
GPU environment. It does not validate the B7-H3 inputs or demonstrate clinical
or experimental binding.
