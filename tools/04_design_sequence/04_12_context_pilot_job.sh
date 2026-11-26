#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"

arm=$1
case "$arm" in
  A) lower=29; upper=169; anchors='T126,T127,T128,T129' ;;
  B) lower=141; upper=281; anchors='T228,T229,T232,T234,T236,T238,T240,T241' ;;
  *) printf 'Unknown arm %s\n' "$arm" >&2; exit 2 ;;
esac

designs=${2:-4}
loops=${3:-L1:8-13,L2:7,L3:9-11,H1:7,H2:6,H3:5-13}
start=${4:-0}
stage=${5:-04_12_context_pilot}

runtime="$MAB_SCRATCH_ROOT/third_party/RFantibody"
output="$MAB_SCRATCH_ROOT/$stage/$arm/$SLURM_JOB_ID"
input="$MAB_DATA_DIR/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb"
framework="$MAB_SCRATCH_ROOT/rfantibody_inputs_corrected3/framework_HLT.pdb"
weights="$runtime/weights/RFdiffusion_Ab.pt"
mkdir -p "$output"
awk -v lo="$lower" -v hi="$upper" '
  /^ATOM  / && substr($0, 22, 1) == "A" && substr($0, 23, 4)+0 >= lo &&
      substr($0, 23, 4)+0 <= hi { print substr($0, 1, 21) "T" substr($0, 23) }
  END { print "TER"; print "END" }
' "$input" > "$output/target.pdb"
nvidia-smi -L
export PATH="$MAB_SCRATCH_ROOT/tools:$runtime/.venv/bin:$PATH"
cd "$runtime"
git rev-parse HEAD
printf 'arm=%s job=%s crop=%s-%s anchors=%s input=%s output=%s framework=%s weights=%s\n' \
  "$arm" "$SLURM_JOB_ID" "$lower" "$upper" "$anchors" "$input" "$output" "$framework" "$weights"
set -x
.venv/bin/rfdiffusion --target "$output/target.pdb" --framework "$framework" \
  --output "$output/ab" --num-designs "$designs" \
  --design-loops "$loops" \
  --hotspots "$anchors" --final-step 1 --no-trajectory --weights "$weights" --deterministic \
  --extra "inference.design_startnum=$start"
