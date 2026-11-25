# 04_09 — Three-path Slurm preflight

Run on Rorqual on 2026-11-25 UTC. Job array 27634890, tasks 0, 1, and 2,
each completed with exit code 0. Tasks 0 and 1 read the existing AF3 inputs
and lineage under `/scratch/ghaedi/mab/fab_category_inputs/fab_{A,B}_only`.
Task 2 checked the RFantibody executable, checkpoint, and existing framework
and target files in scratch and counted 300 prior backbone task records per
arm. The output lists the exact files. File presence does not establish GPU
runtime readiness.

Submission from the project root:

```bash
mkdir -p work/04_09_path_launch
sbatch --parsable --output="$PWD/work/04_09_path_launch/%A_%a.tsv" \
  --error="$PWD/work/04_09_path_launch/%A_%a.err" \
  tools/04_design_sequence/04_09_path_launch_preflight.sh
sacct -j 27634890 -X -n -o JobID,State,ExitCode
```

The committed TSVs preserve stdout with normalized line endings. All three stderr files were empty.
The parent tables contain 40 unique A and 29 unique B lineage IDs. VH
sequence lengths are 114–122 residues for both arms. VL lengths are
105–111 for A and 104–111 for B. These are AF3 input sequence lengths.
Next, compare numbered domain coverage and coordinate completeness before
classifying shortness. Map experimental references for GPT-6 redesign and
define the format criteria and early intact-4Ig comparison before submitting
a new generation pilot. This array generated no new antibody designs.
