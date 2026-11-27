#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=00:20:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"

runtime="$MAB_SCRATCH_ROOT/third_party/RFantibody"
run="$MAB_SCRATCH_ROOT/04_26_arm_a_sequence_pilot/$SLURM_JOB_ID"
export PATH="$MAB_SCRATCH_ROOT/tools:$runtime/.venv/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONUNBUFFERED=1
git -C "$runtime" rev-parse HEAD
seeds=("$@")
if (( ${#seeds[@]} == 0 )); then seeds=(412 421); fi
for seed in "${seeds[@]}"; do
  input="$run/$seed/input"
  output="$run/$seed/output"
  mkdir -p "$input" "$output"
  cp "$MAB_RESULTS_DIR/04_22_arm_a_conditioned/04_22_seed_$seed.pdb" "$input/"
  cd "$output"
  "$runtime/.venv/bin/proteinmpnn" -i "$input" -o "$output" \
    -l 'H1,H2,H3,L1,L2,L3' -n 4 -t 0.1 \
    -w "$runtime/weights/ProteinMPNN_v48_noise_0.2.pt" --deterministic
done
