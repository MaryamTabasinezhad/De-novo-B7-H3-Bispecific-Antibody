#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
cd "$MAB_PROJECT_ROOT"

stage="$MAB_RESULTS_DIR/04_22_arm_a_conditioned"
scratch="$MAB_SCRATCH_ROOT/04_22_arm_a_conditioned"
pose2_job=${1:-27718319}
qc_dir="$scratch/qc/$SLURM_JOB_ID"
mkdir -p "$qc_dir"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
"$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_18_arm_a_backbone_qc.py \
  201:27715195 411:27718318:1 412:27718318:1 "421:$pose2_job:2" "422:$pose2_job:2" \
  431:27718320:3 432:27718320:3 \
  > "$qc_dir/04_22_geometry.tsv" 2> "$qc_dir/04_22_geometry_detail.tsv"
test "$(wc -l < "$qc_dir/04_22_geometry.tsv")" -eq 9
for spec in '411 27718318' '412 27718318' "421 $pose2_job" "422 $pose2_job" '431 27718320' '432 27718320'; do
  read -r seed job <<< "$spec"
  test -s "$scratch/A/$job/ab_$seed.trb"
  cp "$scratch/A/$job/ab_$seed.pdb" "$stage/04_22_seed_$seed.pdb"
done
cp "$qc_dir/04_22_geometry.tsv" "$qc_dir/04_22_geometry_detail.tsv" "$stage/"
