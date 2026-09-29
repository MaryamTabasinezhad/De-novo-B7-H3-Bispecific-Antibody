#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-rf2
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_rf2_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_rf2_%j.err

set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh

export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
IN="$MAB_SCRATCH_ROOT/rfantibody_b7h3_mpnn_20260923/output"
OUT="$MAB_SCRATCH_ROOT/rfantibody_b7h3_rf2_20260924"
WEIGHTS="$RFA/weights/RF2_ab.pt"

mkdir -p "$OUT/A" "$OUT/B"
cd "$RFA"

# The two arms are kept as separate RF2 pilots. This stage evaluates the
# ProteinMPNN sequences against their accepted single-arm backbones; it does
# not claim a final 1A+1B IgG or same-antigen bispecific result.
.venv/bin/rf2 -i "$IN/A" -o "$OUT/A" -r 3 -w "$WEIGHTS" -s 101
.venv/bin/rf2 -i "$IN/B" -o "$OUT/B" -r 3 -w "$WEIGHTS" -s 202

printf '%s\n' 'b7h3_rf2_complete'
