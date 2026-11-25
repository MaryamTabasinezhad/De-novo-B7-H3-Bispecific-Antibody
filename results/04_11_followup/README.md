# 04_11 — Separate Slurm follow-up jobs

Run on Rorqual on 2026-11-25 UTC. All four jobs completed with exit code 0
and empty stderr. Run from the project root with:

```bash
mkdir -p work/04_11_followup
for job in A B references pilot; do
  sbatch --parsable --job-name="mab-next-$job" \
    --output="$PWD/work/04_11_followup/${job}_%j.out" \
    --error="$PWD/work/04_11_followup/${job}_%j.err" \
    tools/04_design_sequence/04_11_followup_job.sh "$job"
done
```

| Job | Task | Result |
|---|---|---|
| 27635634 | Arm A parent termini | 80/80 VH or VL chains match the first and last eight residues of the prior framework chain. |
| 27635635 | Arm B parent termini | 58/58 chains match at both termini. |
| 27635636 | Experimental contact check | 9LY6 reproduces a minimum of 5.169 Å for Q228 with all eight sites beyond 4.5 Å. The tracked 9LY5 map has no entries for the eight sites and has large canonical-number jumps past author residue 218. Verify the raw mmCIF mapping before interpreting 9LY5 overlap. |
| 27635637 | Path C intact-4Ig replay | Of the first 20 historical backbones per arm, 20 A and 17 B had at least one heavy-atom pair below 2 Å outside the design crop. Maximum crop Cα fit RMSD was 0.297 Å for A and 0.390 Å for B. |

The parent checks used the AF3 input/RF2 lineage from 04_09 and the prior
`/scratch/ghaedi/mab/rfantibody_inputs_corrected3/framework_HLT.pdb`.
Terminal identities support retention of the framework ends. Internal CDR
and framework coverage still require a numbering or alignment review.

The Path C replay used historical `ab_0.pdb` files from tasks 0–19 per arm
under `/scratch/ghaedi/mab/rfantibody_b7h3_backbone_pilot_20260925`, the
corrected3 crop inputs, and the tracked oriented 4Ig AlphaFold model. It
matched crop sequences, fitted corresponding target Cα atoms, and screened
distances from transformed H/L backbone atoms to antigen heavy atoms
outside the crop. The 2 Å flag is a geometric screening threshold. The
40-task subset is a baseline diagnostic. Glycans, membrane, and AF3
reprediction were outside this replay. Next, review which omitted target
segments cause the clashes and test a defined context-aware alternative
against the existing baseline.

The four older Fab arrays (22030421, 22030424, 22030425, 23455046) remained
pending with `ReqNodeNotAvail`. Slurm reported node rg13301 as DOWN+DRAIN
with a pump warning. No duplicate arrays or new redesign jobs were submitted.
