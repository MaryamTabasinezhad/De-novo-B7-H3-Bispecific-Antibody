#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-control
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_control_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_control_%j.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
OUT="$MAB_SCRATCH_ROOT/rfantibody_runtime_control"
mkdir -p "$OUT"
cd "$RFA"
.venv/bin/rfdiffusion \
  --target "$RFA/scripts/examples/example_inputs/rsv_site3.pdb" \
  --framework "$RFA/scripts/examples/example_inputs/hu-4D5-8_Fv.pdb" \
  --output "$OUT/ab" \
  --num-designs 1 \
  --hotspots 'T305,T456' \
  --deterministic \
  --weights "$RFA/weights/RFdiffusion_Ab.pt"
printf '%s\n' 'rfantibody_runtime_control_complete'
