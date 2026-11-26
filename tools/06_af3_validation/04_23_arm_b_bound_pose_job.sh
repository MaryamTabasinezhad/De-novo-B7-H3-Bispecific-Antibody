#!/usr/bin/env bash
#SBATCH --job-name=mab-armB-bound
#SBATCH --account=def-ghaedi_gpu
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --array=0-1
set -euo pipefail
source config/hpc/rorqual.sh
module load StdEnv/2023
module load python/3.12.4
module load hmmer-alphafold3/3.4
export LIBCIFPP_DATA_DIR="$MAB_SCRATCH_ROOT/alphafold3_deps/cifpp/rsrc"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 XLA_PYTHON_CLIENT_PREALLOCATE=false
tasks=(248 152)
task="${tasks[$SLURM_ARRAY_TASK_ID]}"
input="$MAB_PROJECT_ROOT/results/04_23_arm_b_bound_pose/04_23_arm_b_task${task}_n215.json"
out="$MAB_SCRATCH_ROOT/04_23_arm_b_bound_pose/$SLURM_ARRAY_JOB_ID/task_$task"
db="$MAB_SCRATCH_ROOT/alphafold3_databases"
mkdir -p "$out"
nvidia-smi -L
cd "$MAB_SCRATCH_ROOT/alphafold3_src"
"$MAB_SCRATCH_ROOT/uv" run --no-sync python run_alphafold.py \
  --json_path="$input" --output_dir="$out" \
  --model_dir="$MAB_SCRATCH_ROOT/alphafold3_params" --db_dir="$db" \
  --pdb_database_path="$db/mmcif_files" \
  --jackhmmer_binary_path="$(command -v jackhmmer)" \
  --hmmbuild_binary_path="$(command -v hmmbuild)" \
  --hmmsearch_binary_path="$(command -v hmmsearch)" \
  --nhmmer_binary_path="$(command -v nhmmer)" \
  --num_diffusion_samples=2 --num_recycles=3 --flash_attention_implementation=triton
