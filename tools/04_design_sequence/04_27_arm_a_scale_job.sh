#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export MAB_MPNN_STAGE=04_27_arm_a_parallel_expansion MAB_MPNN_SAMPLES=24
bash tools/04_design_sequence/04_26_arm_a_mpnn_job.sh 412 421
