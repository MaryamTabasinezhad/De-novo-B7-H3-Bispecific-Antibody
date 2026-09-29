#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_%j.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
IN="$MAB_SCRATCH_ROOT/rfantibody_inputs_corrected3"
OUT="$MAB_SCRATCH_ROOT/rfantibody_b7h3_pilot_20260923"
mkdir -p "$OUT/A" "$OUT/B"
cd "$RFA"
COMMON=(--framework "$IN/framework_HLT.pdb" --num-designs 1 --design-loops 'L1:8-13,L2:7,L3:9-11,H1:7,H2:6,H3:5-13' --final-step 1 --deterministic --no-trajectory --weights "$RFA/weights/RFdiffusion_Ab.pt")
.venv/bin/rfdiffusion --target "$IN/target_A.pdb" --output "$OUT/A/ab" --hotspots 'T126,T127,T128,T129' "${COMMON[@]}"
.venv/bin/rfdiffusion --target "$IN/target_B.pdb" --output "$OUT/B/ab" --hotspots 'T228,T229,T232,T234,T236,T238,T240,T241' "${COMMON[@]}"
printf '%s\n' 'b7h3_rf_diffusion_pilot_complete'
