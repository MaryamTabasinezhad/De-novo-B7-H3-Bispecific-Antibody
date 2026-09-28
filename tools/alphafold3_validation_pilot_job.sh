#!/usr/bin/env bash
#SBATCH --job-name=mab-af3-val
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_interac
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/af3_validation_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/af3_validation_%A_%a.err
#SBATCH --array=0-1
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
module load StdEnv/2023
module load python/3.12.4
module load hmmer-alphafold3/3.4
export LIBCIFPP_DATA_DIR="$MAB_SCRATCH_ROOT/alphafold3_deps/cifpp/rsrc"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 XLA_PYTHON_CLIENT_PREALLOCATE=false
AF3="$MAB_SCRATCH_ROOT/alphafold3_src"
UV="$MAB_SCRATCH_ROOT/uv"
DB="$MAB_SCRATCH_ROOT/alphafold3_databases"
MODEL="$MAB_SCRATCH_ROOT/alphafold3_params"
INPUTS="$MAB_SCRATCH_ROOT/af3_validation_inputs"
OUT="$MAB_SCRATCH_ROOT/af3_validation_pilot"
case "$SLURM_ARRAY_TASK_ID" in
  0) JSON="$INPUTS/armA_task265.json" ;;
  1) JSON="$INPUTS/armB_task131.json" ;;
  *) exit 2 ;;
esac
mkdir -p "$OUT"
cd "$AF3"
"$UV" run python run_alphafold.py \
  --json_path="$JSON" \
  --model_dir="$MODEL" \
  --db_dir="$DB" \
  --pdb_database_path="$DB/mmcif_files" \
  --output_dir="$OUT/$(basename "$JSON" .json)" \
  --jackhmmer_binary_path="$(command -v jackhmmer)" \
  --hmmbuild_binary_path="$(command -v hmmbuild)" \
  --hmmsearch_binary_path="$(command -v hmmsearch)" \
  --nhmmer_binary_path="$(command -v nhmmer)" \
  --num_diffusion_samples=2 \
  --num_recycles=3 \
  --flash_attention_implementation=triton
