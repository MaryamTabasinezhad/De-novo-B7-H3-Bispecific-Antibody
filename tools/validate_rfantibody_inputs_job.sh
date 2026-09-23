#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-input-qc
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_input_qc_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_input_qc_%j.err
set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
INPUTS="$MAB_SCRATCH_ROOT/rfantibody_inputs_corrected2"
python "$MAB_PROJECT_ROOT/tools/validate_rfantibody_inputs.py" \
  --framework "$INPUTS/framework_HLT.pdb" \
  --target-a "$INPUTS/target_A.pdb" \
  --target-b "$INPUTS/target_B.pdb" \
  --output "$MAB_PROJECT_ROOT/reports/rfantibody_input_qc.json"
