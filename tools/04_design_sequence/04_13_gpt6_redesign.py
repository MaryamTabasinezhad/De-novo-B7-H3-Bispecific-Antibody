"""Run one traceable GPT-6 redesign campaign for a single arm."""
import csv
import json
import subprocess
import re
from pathlib import Path

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("arm", choices=["A", "B"])
parser.add_argument("--limit", type=int, choices=[1])
parser.add_argument("--run-id", required=True)
args = parser.parse_args()
arm = args.arm
model = "gpt-6.2-sol"
expected = {"A": 40, "B": 29}[arm]
root = Path(__file__).resolve().parents[2]
job_id = args.run_id
if not re.fullmatch(r"[A-Za-z0-9_-]+", job_id):
    parser.error("Invalid run ID")
output = root / "work/04_13_gpt6_redesign" / f"{arm}_{job_id}"
output.mkdir(parents=True, exist_ok=True)
screen = root / "reports/02_04_b7h3_full_length_humanized_reference_screen.md"
reference = screen.read_text().split(f"## Arm {arm} ", 1)[1].split("\n## ", 1)[0]
with (root / f"results/04_09_path_launch/04_09_arm_{arm.lower()}_parent_lengths.tsv").open() as file:
    parents = list(csv.DictReader(file, delimiter="\t"))
if len(parents) != expected or len({row["parent"] for row in parents}) != expected:
    raise SystemExit(f"Expected {expected} unique Arm {arm} parents")
parents = parents[:args.limit]
print(f"Run {job_id}: Arm {arm}, {len(parents)} parents, model {model}", flush=True)
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
    verified = base.with_suffix(".result.json")
    if verified.exists():
        continue
    base.with_suffix(".input.json").write_text(json.dumps({
        "arm": arm, "parent_id": parent, "model": model, "af3_input": str(source),
        "reference": str(screen.relative_to(root)), "prompt": prompt,
    }, indent=2) + "\n")
    with base.with_suffix(".events.jsonl").open("w") as events, base.with_suffix(".err").open("w") as errors:
        try:
            result = subprocess.run(
                ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
                 "-m", model, "--json", "-o", str(base.with_suffix(".proposal.txt")), "-"],
                input=prompt, text=True, stdout=events, stderr=errors, cwd=output, timeout=180,
            )
            valid = result.returncode == 0 and base.with_suffix(".proposal.txt").exists() and base.with_suffix(".proposal.txt").stat().st_size > 0
        except subprocess.TimeoutExpired:
            print(f"Parent {parent}: GPT-6 request timed out", flush=True)
            valid = False
    if valid:
        try:
            response = base.with_suffix(".proposal.txt").read_text().strip()
            response = re.sub(r"^```(?:json)?\s*|\s*```$", "", response)
            proposal = json.loads(response)
            valid = (
                str(proposal["parent_id"]).upper() in {parent, arm + parent}
                and proposal["arm"] == arm
                and bool(proposal["rationale"])
                and (proposal["status"] == "review_required" or (
                    all(re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", proposal[key]) for key in ("vh", "vl"))
                    and (proposal["vh"], proposal["vl"]) != (chains[f"H{arm}"], chains[f"L{arm}"])
                    and bool(proposal["changes"])
                ))
            )
        except (ValueError, TypeError, KeyError):
            valid = False
    if valid:
        thread_ids = [event.get("thread_id") for event in map(json.loads, base.with_suffix(".events.jsonl").read_text().splitlines())
                      if event.get("type") == "thread.started"]
        verified.write_text(json.dumps({"run_id": job_id, "model": model,
                                       "codex_thread_ids": thread_ids, "input": json.loads(base.with_suffix(".input.json").read_text()),
                                       "proposal": proposal}, indent=2) + "\n")
        print(f"Parent {parent}: {proposal['status']}", flush=True)
    else:
        failures.append(parent)
        print(f"Parent {parent}: no verified model response", flush=True)
        if len(failures) == 1 and parent == parents[0]["parent"]:
            raise SystemExit("First parent request failed; remaining parents were not attempted.")
if failures:
    raise SystemExit(f"Parents without verified responses: {', '.join(failures)}")
