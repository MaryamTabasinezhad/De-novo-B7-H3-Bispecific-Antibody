#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --partition=cpubase_bycore_b1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:20:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1
python=python3
if [[ "$1" == pilot ]]; then
  python="$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python"
fi
"$python" tools/04_design_sequence/04_11_followup.py "$1"
