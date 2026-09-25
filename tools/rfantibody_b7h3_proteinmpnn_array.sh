#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-mpnn
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --array=0-299%20
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_mpnn_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_mpnn_%A_%a.err

set -euo pipefail
: "${ARM:?Submit with --export=ALL,ARM=A or ARM=B}"
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh

export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
BACKBONES="$MAB_SCRATCH_ROOT/rfantibody_b7h3_backbone_pilot_20260925"
RUN="$MAB_SCRATCH_ROOT/rfantibody_b7h3_proteinmpnn_20260925"
TASK="$SLURM_ARRAY_TASK_ID"
IN="$RUN/input/$ARM/task_${TASK}"
OUT="$RUN/output/$ARM/task_${TASK}"
SOURCE="$BACKBONES/$ARM/task_${TASK}/ab_0.pdb"

if [[ ! -s "$SOURCE" ]]; then
  echo "Missing backbone: $SOURCE" >&2
  exit 2
fi
mkdir -p "$IN" "$OUT"
cp "$SOURCE" "$IN/ab_0.pdb"

cd "$RFA"
.venv/bin/proteinmpnn \
  -i "$IN" \
  -o "$OUT" \
  -l 'H1,H2,H3,L1,L2,L3' \
  -n 4 \
  -t 0.1 \
  -w "$RFA/weights/ProteinMPNN_v48_noise_0.2.pt" \
  --deterministic

cat > "$OUT/run_metadata.tsv" <<EOF
arm\tarray_job_id\tarray_task_id\tparent_backbone\tseqs_per_struct\ttemperature\tloops
$ARM\t${SLURM_ARRAY_JOB_ID}\t${TASK}\t$SOURCE\t4\t0.1\tH1,H2,H3,L1,L2,L3
EOF
printf 'b7h3_proteinmpnn_complete arm=%s task=%s\n' "$ARM" "$TASK"
