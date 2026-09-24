#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-rf2-control
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_rf2_control_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_rf2_control_%j.err

set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh

export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
INPUT="$RFA/scripts/examples/rf2/example_inputs"
OUT="$MAB_SCRATCH_ROOT/rfantibody_rf2_official_control_20260924"
WEIGHTS="$RFA/weights/RF2_ab.pt"

mkdir -p "$OUT"
cd "$RFA"

# Use the same RF2 CLI, model weights, recycle count, and cautious mode as the
# B7-H3 wrapper. The official bundled H/L/T example is the runtime control.
.venv/bin/rf2 -i "$INPUT" -o "$OUT" -r 3 -w "$WEIGHTS" -s 101

python "$MAB_PROJECT_ROOT/tools/check_rfantibody_interface_geometry.py" "$OUT"
printf '%s\n' 'rf2_official_control_complete'
