#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-arm-a-retry
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_arm_a_retry_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_arm_a_retry_%j.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
IN="$MAB_SCRATCH_ROOT/rfantibody_inputs_corrected3"
OUT="$MAB_SCRATCH_ROOT/rfantibody_b7h3_arm_a_retry_20260923"
mkdir -p "$OUT"
cd "$RFA"
.venv/bin/rfdiffusion \
  --target "$IN/target_A.pdb" \
  --framework "$IN/framework_HLT.pdb" \
  --output "$OUT/ab" \
  --num-designs 1 \
  --design-loops 'L1:8-13,L2:7,L3:9-11,H1:7,H2:6,H3:5-13' \
  --hotspots 'T126,T127,T128,T129' \
  --final-step 1 \
  --no-trajectory \
  --weights "$RFA/weights/RFdiffusion_Ab.pt"
printf '%s\n' 'b7h3_arm_a_retry_complete'
