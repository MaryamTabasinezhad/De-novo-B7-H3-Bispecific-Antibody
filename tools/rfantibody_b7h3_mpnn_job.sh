#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-mpnn
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_mpnn_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_mpnn_%j.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
OUT="$MAB_SCRATCH_ROOT/rfantibody_b7h3_mpnn_20260923"
mkdir -p "$OUT/input/A" "$OUT/input/B" "$OUT/output/A" "$OUT/output/B"
cp "$MAB_SCRATCH_ROOT/rfantibody_b7h3_arm_a_retry_20260923/ab_0.pdb" "$OUT/input/A/ab_0.pdb"
cp "$MAB_SCRATCH_ROOT/rfantibody_b7h3_arm_pilots_20260923/B/ab_0.pdb" "$OUT/input/B/ab_0.pdb"
cd "$RFA"
COMMON=(-l 'H1,H2,H3,L1,L2,L3' -n 2 -t 0.1 -w "$RFA/weights/ProteinMPNN_v48_noise_0.2.pt" --deterministic)
.venv/bin/proteinmpnn -i "$OUT/input/A" -o "$OUT/output/A" "${COMMON[@]}"
.venv/bin/proteinmpnn -i "$OUT/input/B" -o "$OUT/output/B" "${COMMON[@]}"
printf '%s\n' 'b7h3_mpnn_complete'
