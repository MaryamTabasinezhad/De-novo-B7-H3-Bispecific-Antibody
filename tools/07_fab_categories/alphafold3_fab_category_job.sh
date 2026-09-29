#!/usr/bin/env bash
# AF3 generation for one of the three Fab categories.
#SBATCH --job-name=mab-fab-cat
#SBATCH --account=def-ghaedi_gpu
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/fab_category_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/fab_category_%A_%a.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
module load StdEnv/2023
module load python/3.12.4
module load hmmer-alphafold3/3.4
export LIBCIFPP_DATA_DIR="$MAB_SCRATCH_ROOT/alphafold3_deps/cifpp/rsrc"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 XLA_PYTHON_CLIENT_PREALLOCATE=false
AF3="$MAB_SCRATCH_ROOT/alphafold3_src"; UV="$MAB_SCRATCH_ROOT/uv"; DB="$MAB_SCRATCH_ROOT/alphafold3_databases"; MODEL="$MAB_SCRATCH_ROOT/alphafold3_params"
PROJECT="$MAB_PROJECT_ROOT"; CAT="${FAB_CATEGORY:?FAB_CATEGORY must be A, B, or AB}"
case "$CAT" in A) N=40; RES="fab_A_only";; B) N=29; RES="fab_B_only";; AB) N=1160; RES="fab_AB_pairs";; esac
if (( SLURM_ARRAY_TASK_ID >= N )); then exit 2; fi
JSON="$MAB_SCRATCH_ROOT/fab_category_inputs/$RES/index_${SLURM_ARRAY_TASK_ID}.json"
python "$PROJECT/tools/07_fab_categories/prepare_fab_category_input.py" --category "$CAT" --index "$SLURM_ARRAY_TASK_ID" --arm-a-tsv "$PROJECT/results/05_03_control_shortlist_20260927/arm_a.tsv" --arm-b-tsv "$PROJECT/results/05_03_control_shortlist_20260927/arm_b.tsv" --target-pdb "$PROJECT/data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb" --out "$JSON"
OUT="$MAB_SCRATCH_ROOT/fab_category_outputs/$RES"; mkdir -p "$OUT"; cd "$AF3"
"$UV" run python run_alphafold.py --json_path="$JSON" --model_dir="$MODEL" --db_dir="$DB" --pdb_database_path="$DB/mmcif_files" --output_dir="$OUT/$(basename "$JSON" .json)" --jackhmmer_binary_path="$(command -v jackhmmer)" --hmmbuild_binary_path="$(command -v hmmbuild)" --hmmsearch_binary_path="$(command -v hmmsearch)" --nhmmer_binary_path="$(command -v nhmmer)" --num_diffusion_samples=2 --num_recycles=3 --flash_attention_implementation=triton
