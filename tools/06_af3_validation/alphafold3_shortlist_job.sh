#!/usr/bin/env bash
# AF3 independent validation for all 69 RF2 control-equivalent shortlist models.
# Array indices 0-39 map to Arm A; 40-68 map to Arm B.
#SBATCH --job-name=mab-af3-list
#SBATCH --account=def-ghaedi_gpu
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --array=0-68%10
#SBATCH --output=/scratch/ghaedi/mab/jobs/af3_shortlist_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/af3_shortlist_%A_%a.err
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
INPUTS="$MAB_SCRATCH_ROOT/af3_validation_shortlist_inputs"
OUT="$MAB_SCRATCH_ROOT/af3_validation_shortlist"
PROJECT="$MAB_PROJECT_ROOT"
if (( SLURM_ARRAY_TASK_ID < 40 )); then
  ARM=A; ROW="$SLURM_ARRAY_TASK_ID"; TSV="$PROJECT/results/05_03_control_shortlist_20260927/arm_a.tsv"
else
  ARM=B; ROW="$((SLURM_ARRAY_TASK_ID - 40))"; TSV="$PROJECT/results/05_03_control_shortlist_20260927/arm_b.tsv"
fi
JSON="$INPUTS/arm${ARM}_row${ROW}.json"
python "$PROJECT/tools/06_af3_validation/prepare_af3_shortlist_input.py" --tsv "$TSV" --row "$ROW" --out "$JSON"
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
