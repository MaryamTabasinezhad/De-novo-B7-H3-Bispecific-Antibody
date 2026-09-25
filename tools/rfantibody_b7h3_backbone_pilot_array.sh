#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-pilot
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --array=0-99%20
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_pilot_%A_%a.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_pilot_%A_%a.err

set -euo pipefail
: "${ARM:?Submit with --export=ALL,ARM=A or ARM=B}"
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh

export PATH="$MAB_SCRATCH_ROOT/tools:$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin:$PATH"
RFA="$MAB_SCRATCH_ROOT/third_party/RFantibody"
IN="$MAB_SCRATCH_ROOT/rfantibody_inputs_corrected3"
RUN="$MAB_SCRATCH_ROOT/rfantibody_b7h3_backbone_pilot_20260925"
OUT="$RUN/$ARM/task_${SLURM_ARRAY_TASK_ID}"
mkdir -p "$OUT"

case "$ARM" in
  A)
    TARGET="$IN/target_A.pdb"
    HOTSPOTS='T126,T127,T128,T129'
    ;;
  B)
    TARGET="$IN/target_B.pdb"
    HOTSPOTS='T228,T229,T232,T234,T236,T238,T240,T241'
    ;;
  *)
    echo "Unsupported ARM=$ARM" >&2
    exit 2
    ;;
esac

cd "$RFA"
.venv/bin/rfdiffusion \
  --target "$TARGET" \
  --framework "$IN/framework_HLT.pdb" \
  --output "$OUT/ab" \
  --num-designs 1 \
  --design-loops 'L1:8-13,L2:7,L3:9-11,H1:7,H2:6,H3:5-13' \
  --hotspots "$HOTSPOTS" \
  --final-step 1 \
  --no-trajectory \
  --weights "$RFA/weights/RFdiffusion_Ab.pt"

cat > "$OUT/run_metadata.tsv" <<EOF
arm\tarray_job_id\tarray_task_id\ttarget\thotspots\tnum_designs\n$ARM\t${SLURM_ARRAY_JOB_ID}\t${SLURM_ARRAY_TASK_ID}\t$TARGET\t$HOTSPOTS\t1
EOF
printf 'b7h3_backbone_pilot_complete arm=%s task=%s\n' "$ARM" "$SLURM_ARRAY_TASK_ID"
