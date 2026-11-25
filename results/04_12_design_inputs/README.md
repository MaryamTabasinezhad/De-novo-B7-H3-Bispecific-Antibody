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
