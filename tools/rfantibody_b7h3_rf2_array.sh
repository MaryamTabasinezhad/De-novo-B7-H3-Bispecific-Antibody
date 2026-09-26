#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-rf2
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --array=0-299%20
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_rf2_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_rf2_%A_%a.err

set -euo pipefail
: "${ARM:?Submit with --export=ALL,ARM=A or ARM=B}"
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh

export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
INROOT="$MAB_SCRATCH_ROOT/rfantibody_b7h3_proteinmpnn_20260925/output"
RUN="$MAB_SCRATCH_ROOT/rfantibody_b7h3_rf2_20260926"
IN="$INROOT/$ARM/task_${SLURM_ARRAY_TASK_ID}"
OUT="$RUN/$ARM/task_${SLURM_ARRAY_TASK_ID}"
WEIGHTS="$RFA/weights/RF2_ab.pt"

mkdir -p "$OUT"
mapfile -t PDBS < <(find "$IN" -maxdepth 1 -type f -name '*.pdb' -printf '%f\n' 2>/dev/null | sort)
if (( ${#PDBS[@]} == 0 )); then
  cat > "$OUT/run_metadata.tsv" <<EOF
arm\tarray_job_id\tarray_task_id\tinput_pdbs\tstatus
$ARM\t${SLURM_ARRAY_JOB_ID}\t${SLURM_ARRAY_TASK_ID}\t0\tskipped_empty_input
EOF
  printf 'b7h3_rf2_skipped arm=%s task=%s reason=empty_input\n' "$ARM" "$SLURM_ARRAY_TASK_ID"
  exit 0
fi

# RF2 writes temporary files relative to the current directory in some code
# paths. Use the task-specific output directory to isolate concurrent tasks.
cd "$OUT"
"$RFA/.venv/bin/rf2" \
  -i "$IN" \
  -o "$OUT" \
  -r 3 \
  -w "$WEIGHTS" \
  -s "$((1000 + SLURM_ARRAY_TASK_ID))"

cat > "$OUT/run_metadata.tsv" <<EOF
arm\tarray_job_id\tarray_task_id\tinput_pdbs\trecycles\tseed\tstatus
$ARM\t${SLURM_ARRAY_JOB_ID}\t${SLURM_ARRAY_TASK_ID}\t${#PDBS[@]}\t3\t$((1000 + SLURM_ARRAY_TASK_ID))\tcompleted
EOF
printf 'b7h3_rf2_complete arm=%s task=%s inputs=%s\n' "$ARM" "$SLURM_ARRAY_TASK_ID" "${#PDBS[@]}"
