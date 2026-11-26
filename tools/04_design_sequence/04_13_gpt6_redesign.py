"""Run one traceable GPT-6 redesign campaign for a single arm."""
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

arm = sys.argv[1]
expected = {"A": 40, "B": 29}[arm]
root = Path(os.environ["SLURM_SUBMIT_DIR"])
job_id = os.environ["SLURM_JOB_ID"]
output = root / "work/04_13_gpt6_redesign" / f"{arm}_{job_id}"
output.mkdir(parents=True, exist_ok=True)
screen = root / "reports/02_04_b7h3_full_length_humanized_reference_screen.md"
reference = screen.read_text().split(f"## Arm {arm} ", 1)[1].split("\n## ", 1)[0]
with (root / f"results/04_09_path_launch/04_09_arm_{arm.lower()}_parent_lengths.tsv").open() as file:
    parents = list(csv.DictReader(file, delimiter="\t"))
if len(parents) != expected or len({row["parent"] for row in parents}) != expected:
    raise SystemExit(f"Expected {expected} unique Arm {arm} parents")
print(f"Slurm job {job_id}: Arm {arm}, {expected} parents, model gpt-6", flush=True)
failures = []
for row in parents:
    parent = row["parent"]
    source = Path(row["af3_input"])
    sequences = json.loads(source.read_text())["sequences"]
    chains = {item["protein"]["id"]: item["protein"]["sequence"] for item in sequences}
    prompt = f"""Propose one experimentally testable VH/VL redesign for B7-H3 Arm {arm}
parent {parent}, for a Y-shaped humanized IgG with separate HC and LC.
Use only the reference evidence below at its stated strength. Preserve the arm's
intended epitope and complete variable-domain framework. Treat reference-chain
and internal-coverage uncertainties explicitly. If evidence is insufficient for
a warranted sequence change, return a review_required result with the reason.
Return JSON with parent_id, arm, status, vh, vl, changes, rationale and uncertainties.
Do not use tools or read other files. The final Fc and pairing architecture are
outside this proposal. Do not represent predicted binding as measured.
Reference record:
{reference}
Parent VH: {chains[f'H{arm}']}
Parent VL: {chains[f'L{arm}']}
"""
    base = output / f"parent_{parent}"
    with base.with_suffix(".events.jsonl").open("w") as events, base.with_suffix(".err").open("w") as errors:
        try:
            result = subprocess.run(
                ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
                 "-m", "gpt-6", "--json", "-o", str(base.with_suffix(".proposal.txt")), "-"],
                input=prompt, text=True, stdout=events, stderr=errors, cwd=output, timeout=90,
            )
            valid = result.returncode == 0 and base.with_suffix(".proposal.txt").is_file()
        except subprocess.TimeoutExpired:
            print(f"Parent {parent}: GPT-6 request timed out", flush=True)
            valid = False
    if valid:
        print(f"Parent {parent}: model response saved", flush=True)
    else:
        failures.append(parent)
        print(f"Parent {parent}: no verified model response", flush=True)
        if len(failures) == 1 and parent == parents[0]["parent"]:
            raise SystemExit("First parent request failed; remaining parents were not attempted.")
if failures:
    raise SystemExit(f"Parents without verified responses: {', '.join(failures)}")
