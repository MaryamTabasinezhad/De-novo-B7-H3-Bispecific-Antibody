#!/usr/bin/env bash
#SBATCH --job-name=mab-rfa-b7h3-shortlist
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:15:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_shortlist_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/rfantibody_b7h3_shortlist_%j.err

set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
OUT="$MAB_RESULTS_DIR/rfantibody_b7h3_control_shortlist_20260927"
QC="$MAB_RESULTS_DIR/rfantibody_b7h3_rf2_qc_20260927"
IFACE="$MAB_RESULTS_DIR/rfantibody_b7h3_interface_20260927"
mkdir -p "$OUT"
python "$MAB_PROJECT_ROOT/tools/05_rf2_qc/rfantibody_b7h3_control_qc_shortlist.py" A "$QC/arm_a.tsv" "$IFACE/arm_a.tsv" "$OUT/arm_a.tsv"
python "$MAB_PROJECT_ROOT/tools/05_rf2_qc/rfantibody_b7h3_control_qc_shortlist.py" B "$QC/arm_b.tsv" "$IFACE/arm_b.tsv" "$OUT/arm_b.tsv"
printf 'shortlist_complete output=%s\n' "$OUT"
