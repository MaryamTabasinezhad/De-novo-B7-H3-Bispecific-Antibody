#!/usr/bin/env bash
#SBATCH --account=def-ghaedi_gpu
#SBATCH --partition=gpubase_bygpu_b1
#SBATCH --gres=gpu:nvidia_h100_80gb_hbm3_3g.40gb:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=00:25:00
set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"

pose=$1
seed=$2
case "$pose" in
  412-h3)
    stage=04_24_arm_a_h3_refinement
    input="$MAB_RESULTS_DIR/$stage/04_24_seed_412_input.pdb"
    loops='[H3:]'
    partial_step=8
    ;;
  *)
    stage=04_22_arm_a_conditioned
    input="$MAB_RESULTS_DIR/$stage/04_22_pose_$pose.pdb"
    loops='[L1:,L2:,L3:,H1:,H2:,H3:]'
    partial_step=15
    ;;
esac
runtime="$MAB_SCRATCH_ROOT/third_party/RFantibody"
output="$MAB_SCRATCH_ROOT/$stage/A/$SLURM_JOB_ID"
mkdir -p "$output"
nvidia-smi -L
export PATH="$MAB_SCRATCH_ROOT/tools:$runtime/.venv/bin:$PATH"
cd "$runtime"
git rev-parse HEAD
set -x
.venv/bin/python scripts/rfdiffusion_inference.py --config-name antibody \
  "inference.input_pdb=$input" "inference.output_prefix=$output/ab" \
  "inference.ckpt_override_path=$runtime/weights/RFdiffusion_Ab.pt" \
  inference.num_designs=2 "inference.design_startnum=$seed" \
  inference.deterministic=True inference.write_trajectory=False inference.final_step=1 \
  diffuser.T=50 "diffuser.partial_T=$partial_step" antibody.T_scheme=fixed_dock \
  "antibody.design_loops=$loops" \
  'ppi.hotspot_res=[T126,T127,T128,T129]'
