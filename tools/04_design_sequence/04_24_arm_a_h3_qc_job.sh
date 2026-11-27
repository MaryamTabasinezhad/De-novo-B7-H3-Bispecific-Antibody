#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
cd "$MAB_PROJECT_ROOT"
job=$1
stage=04_24_arm_a_h3_refinement
run="$MAB_SCRATCH_ROOT/$stage/A/$job"
qc_dir="$MAB_SCRATCH_ROOT/$stage/qc/$SLURM_JOB_ID"
mkdir -p "$qc_dir"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
"$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_18_arm_a_backbone_qc.py \
  421:27722542:2 412:27718318:1 \
  "441:$job:$stage:04_24_seed_412_input.pdb" "442:$job:$stage:04_24_seed_412_input.pdb" \
  > "$qc_dir/04_24_geometry.tsv" 2> "$qc_dir/04_24_geometry_detail.tsv"
test "$(wc -l < "$qc_dir/04_24_geometry.tsv")" -eq 6
for seed in 441 442; do
  test -s "$run/ab_$seed.trb"
  cp "$run/ab_$seed.pdb" "$MAB_RESULTS_DIR/$stage/04_24_seed_$seed.pdb"
done
cp "$qc_dir/04_24_geometry.tsv" "$qc_dir/04_24_geometry_detail.tsv" "$MAB_RESULTS_DIR/$stage/"
