# 04_12 — Design inputs and expanded-context pilot

Rorqual, 2026-11-25 UTC. See the scheduler snapshot and result tables in this
directory. Commands from the project root:

```bash
mkdir -p work/04_12_design_inputs
for job in A B references pilot; do
  sbatch --parsable --job-name="mab-inputs-$job" \
    --output="$PWD/work/04_12_design_inputs/${job}_%j.out" \
    --error="$PWD/work/04_12_design_inputs/${job}_%j.err" \
    tools/04_design_sequence/04_12_design_inputs_job.sh "$job"
done
for arm in A B; do
  sbatch --parsable --job-name="mab-context-$arm" \
    --output="$PWD/work/04_12_design_inputs/context_${arm}_%j.out" \
    --error="$PWD/work/04_12_design_inputs/context_${arm}_%j.err" \
    tools/04_design_sequence/04_12_context_pilot_job.sh "$arm"
done
```

- **27635695 and 27635696:** Compared all 69 RF2 parent VH/VL chains to the
  RFantibody HLT template. The tables report internal sequence difference
  blocks in one-based, half-open sequence coordinates. Exact-block alignment
  does not assign standardized antibody positions or distinguish a CDR-length
  change from an internal framework deletion. Use this as an input to the
  numbered framework coverage review, along with the prior termini checks.
- **27635697:** Used 9LY5 mmCIF chain C alignment to Q5ZPR3 and its polymer
  sequence scheme to verify the eight Arm B positions. Q228 contacts 20G5
  at 3.001 Å. Five other resolved sites are beyond 4.5 Å. Q240 and R241 have
  no resolved coordinates in the entry. Raw 9LY6 puts Q228 at 5.169 Å.
  The evidence supports partial, structure-dependent overlap of 20G5 with
  the intended Arm B patch. The new table supersedes the earlier 9LY5 result
  for these eight sites. Recheck the wider tracked 9LY5 map before using it.
- **27635698:** Localized the replay clashes in the first 20 historical
  backbones per arm. Omitted clashing residues span 24–85 for A and 141–169
  for B. NA indicates no clashing residues. The pilot uses the project's native ectodomain boundary at 29,
  omitting residues 24–28 from the expanded A input.
- **27635726 and 27635727:** Separate Path C GPU diagnostics for Arm A and
  Arm B. Expanded crops are 29–169 and 141–281 respectively. Each requests
  four RFantibody backbones with the previous framework, CDR length ranges,
  anchor sets, checkpoint and diffusion settings, plus deterministic mode
  for this pilot. The historical backbones are the comparison baseline.
  The pilot changes crop context and does not establish a final Fab format.
  Scratch output paths are
  `/scratch/ghaedi/mab/04_12_context_pilot/A/27635726` and
  `/scratch/ghaedi/mab/04_12_context_pilot/B/27635727`. Logs record the
  checkout, visible GPU, command, input paths and crop bounds at execution.

Next, inspect GPU pilot outputs and compare intact-4Ig clash and epitope contact
metrics with the historical runs before scaling. GPT-6 redesign awaits
verified internal format criteria and experimental reference inputs. No GPT-6
redesign or AF3 inference was submitted in this milestone.

## GPU completion

Both jobs completed in 15 minutes 33 seconds with exit code 0. Each produced
four nonempty backbone PDBs and four associated TRB files. The completion
record lists paths and file sizes. Scientific geometry and contact QC remain
pending.

## Intact 4Ig geometry review — 2026-11-26 UTC

[Per-model results](04_12_expanded_context_qc.tsv) cover four expanded backbones
per arm and the first four historical tasks per arm. The analysis read the
scratch outputs listed above and the historical inputs under
`/scratch/ghaedi/mab/rfantibody_b7h3_backbone_pilot_20260925/{A,B}/task_{0..3}`
and `/scratch/ghaedi/mab/rfantibody_inputs_corrected3/target_{A,B}.pdb`.
No Slurm job was submitted.

```bash
source config/hpc/rorqual.sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_12_expanded_context_qc.py \
  > results/04_12_design_inputs/04_12_expanded_context_qc.tsv
```

NumPy 1.26.4 and SciPy 1.15.3. Crop sequences matched the canonical Q5ZPR3
model and RFantibody output target chains. The replay used crop Cα alignment
and counted atom pairs below 2 Å on ectodomain residues 29–466. Intended
anchor contacts use a 4.5 Å cutoff. The eight historical outside-crop counts
reproduced the earlier replay exactly. Expanded crop fits were 0.123–0.175 Å
RMSD. Every model had both variable chains and adjacent Cα distances at or
below 3.89 Å. These are preliminary fold continuity checks on Fv backbones.

- **Arm A.** Outside-crop clashes fell from 4/4 historical poses to 0/4
  expanded poses. All four expanded poses contact at least two of four
  anchors and each has 1–4 sub-2 Å pairs against the ectodomain. Models 0
  and 1 contact all four anchors. Their lowest Fv atoms are at z=24.11 and
  11.19 Å, respectively. Model 3 also reaches z=12.95 Å. The transmembrane
  Cα span is z=−15.18 to +15.35 Å. Models 1 and 3 warrant membrane review. The nearest
  annotated glycosite is N104, at 20.36–21.91 Å from the Fv to Asn ND2.
- **Arm B.** Outside-crop clashes fell from 3/4 historical poses to 0/4
  expanded poses. Expanded models contact 4–7 of eight anchors. Model 2
  contacts seven anchors and has zero sub-2 Å ectodomain pairs. Its nearest
  Fv atom is 2.90 Å from N215 ND2, which flags possible glycan interference.
  Model 3 is similarly close to N215. The lowest Fv atoms for all four B
  models are above z=61 Å.

The z coordinate is an orientation proxy on one predicted 4Ig model.
Asn ND2 distances flag proximity to glycan attachment points. Native glycan
occupancy and motion, membrane tilt, and complete Fab constant-domain
clearance remain unverified. Inspect the close protein contacts for A0 and
the N215 glycan for B2 before advancing. The comparison uses a small sample
and supports continued pilot review before scaling.

### Close-contact and N215 follow-up

Run the same QC command with the argument `followup` and redirect to
[04_12_contact_followup.tsv](04_12_contact_followup.tsv). The original geometry
table was reproduced byte for byte after sharing the alignment routine.

- **Arm A model 0.** The only protein pair below 2 Å is the heavy-chain
  residue 101 backbone carbonyl oxygen against canonical B7-H3 Ser125 OG
  (1.680 Å). This is a local steric overlap in the starting pose. It remains
  open whether a Ser125 rotamer change can remove it while retaining the
  intended contacts.
- **Arm B model 2.** The first N215 sugar was unresolved in the available
  experimental structures. To test geometric sensitivity, the first NAG
  linked to Asn104 or Asn189 on each of chains A and B in local
  `data/raw/structures/9LME.pdb` was transferred by CG/OD1/ND2 alignment
  to N215. The target site was evaluated in AFDB v6 and in 9LME chain A
  after fitting canonical Cα positions 210–220 to AFDB v6 using the project
  numbering map. B2 was held fixed. For the AFDB side chain, both transfers
  from N189 had zero sub-2 Å pairs with other target residues and each
  overlapped B2 (8–10 pairs below 2 Å). All four placements clashed with B2
  in both conformers. The 9LME-based transfers also clashed with the
  surrounding antigen, reducing their value as physical glycan poses.
  This fixed-pose sensitivity test flags a credible interference risk.
  Native N215 occupancy, alternate rotamers, and full glycan flexibility
  remain unresolved. Hold B2 at the geometry gate pending that evidence.

The analysis reused jobs 27635726 and 27635727 from the scratch paths
recorded above. No Slurm job was submitted and no structure was relaxed.
