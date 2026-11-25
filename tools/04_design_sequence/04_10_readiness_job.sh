#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --partition=cpubase_bycore_b1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:15:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
export PYTHONDONTWRITEBYTECODE=1
python3 tools/04_design_sequence/04_10_readiness.py "$@"
