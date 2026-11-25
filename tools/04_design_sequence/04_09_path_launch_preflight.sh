#!/usr/bin/env bash
#SBATCH --job-name=mab-path-preflight
#SBATCH --account=def-ghaedi_cpu
#SBATCH --partition=cpubase_bycore_b1
#SBATCH --array=0-2
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00

set -euo pipefail
source "$SLURM_SUBMIT_DIR/config/hpc/rorqual.sh"
python3 - "$SLURM_ARRAY_TASK_ID" "$MAB_SCRATCH_ROOT" <<'PY'
import csv
import json
import sys
from pathlib import Path

task, scratch_path = sys.argv[1:]
scratch = Path(scratch_path)

if task == "2":
    for relative in (
        "third_party/RFantibody/.venv/bin/rfdiffusion",
        "third_party/RFantibody/weights/RFdiffusion_Ab.pt",
        "rfantibody_inputs_corrected3/framework_HLT.pdb",
        "rfantibody_inputs_corrected3/target_A.pdb",
        "rfantibody_inputs_corrected3/target_B.pdb",
    ):
        path = scratch / relative
        print(f"{path}\t{'available' if path.is_file() else 'missing'}")
        if not path.is_file():
            raise SystemExit(f"Missing required Path C input: {path}")
    for arm in ("A", "B"):
        baseline = scratch / "rfantibody_b7h3_backbone_pilot_20260925" / arm
        print(f"{baseline}\t{len(list(baseline.glob('task_*/run_metadata.tsv')))} recorded tasks")
    raise SystemExit(0)

arm, expected = {"0": ("A", 40), "1": ("B", 29)}[task]
inputs = scratch / "fab_category_inputs" / f"fab_{arm}_only"
lineages = sorted(inputs.glob("index_*.lineage.json"))
if len(lineages) != expected:
    raise SystemExit(f"Expected {expected} Arm {arm} parents, found {len(lineages)}")
output = csv.writer(sys.stdout, delimiter="\t")
output.writerow(("arm", "parent", "vh_length", "vl_length", "af3_input", "rf2_parent"))
parents = set()
for lineage_file in lineages:
    lineage = json.loads(lineage_file.read_text())
    parent = lineage[f"arm_{arm.lower()}_task"]
    if parent in parents:
        raise SystemExit(f"Duplicate Arm {arm} parent {parent}")
    parents.add(parent)
    input_file = lineage_file.with_name(lineage_file.name.replace(".lineage.json", ".json"))
    af3_input = json.loads(input_file.read_text())
    chains = {entry["protein"]["id"]: entry["protein"]["sequence"] for entry in af3_input["sequences"]}
    output.writerow((arm, parent, len(chains[f"H{arm}"]), len(chains[f"L{arm}"]),
                     input_file, lineage[f"arm_{arm.lower()}_pdb"]))
PY
