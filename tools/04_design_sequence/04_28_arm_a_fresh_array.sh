#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
first_seed=$((513 + 4 * SLURM_ARRAY_TASK_ID))
bash tools/04_design_sequence/04_12_context_pilot_job.sh A 4 \
  'L1:8-13,L2:7,L3:9-11,H1:7,H2:6,H3:5-13' "$first_seed" 04_28_arm_a_breadth_expansion
