#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=04:00:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
python3 "$SLURM_SUBMIT_DIR/tools/04_design_sequence/04_13_gpt6_redesign.py" "$1"
