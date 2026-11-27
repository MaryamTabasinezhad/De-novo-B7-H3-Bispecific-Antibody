#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
cd "$MAB_PROJECT_ROOT"

stage=04_26_arm_a_sequence_pilot
scratch="$MAB_SCRATCH_ROOT/$stage/qc/$SLURM_JOB_ID"
mkdir -p "$scratch"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
"$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/06_af3_validation/04_26_arm_a_fullfab_qc.py "$1" "$2" \
  > "$scratch/04_26_fullfab_geometry.tsv"
test "$(wc -l < "$scratch/04_26_fullfab_geometry.tsv")" -eq 9
cp "$scratch/04_26_fullfab_geometry.tsv" "$MAB_RESULTS_DIR/$stage/"
