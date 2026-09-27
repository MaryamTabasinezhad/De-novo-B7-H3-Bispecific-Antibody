#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-iface
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_iface_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_iface_%j.err

set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
module load scipy-stack/2025a

QC="$MAB_RESULTS_DIR/rfantibody_b7h3_rf2_qc_20260927"
RUN="$MAB_SCRATCH_ROOT/rfantibody_b7h3_rf2_20260926"
OUT="$MAB_RESULTS_DIR/rfantibody_b7h3_interface_20260927"
mkdir -p "$OUT"
python "$MAB_PROJECT_ROOT/tools/rfantibody_b7h3_interface_screen.py" A "$QC/arm_a.tsv" "$RUN/A" "$OUT/arm_a.tsv"
python "$MAB_PROJECT_ROOT/tools/rfantibody_b7h3_interface_screen.py" B "$QC/arm_b.tsv" "$RUN/B" "$OUT/arm_b.tsv"
printf 'interface_screen_complete arm_a=%s arm_b=%s\n' "$OUT/arm_a.tsv" "$OUT/arm_b.tsv"
