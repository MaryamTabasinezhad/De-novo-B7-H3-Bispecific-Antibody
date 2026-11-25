"""Prepare independent evidence, sequence coverage, and pilot input records."""
import csv
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

scratch = Path(os.environ["MAB_SCRATCH_ROOT"])
sys.path.insert(0, "tools/07_fab_categories")
from prepare_fab_category_input import pdb_sequences


def references():
    sources = {
        "clinicaltrials": "https://clinicaltrials.gov/api/v2/studies?" + urlencode({
            "query.term": '(B7-H3 OR CD276 OR omburtamab OR enoblituzumab) AND (antibody OR ADC)',
            "pageSize": 100,
            "fields": "NCTId,BriefTitle,OverallStatus,Phase,InterventionName,InterventionType",
        }),
        "europe_pmc": "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode({
            "query": '(TITLE_ABS:"B7-H3" OR TITLE_ABS:CD276) AND '
                     '(TITLE_ABS:antibody OR TITLE_ABS:omburtamab) AND '
                     '(TITLE_ABS:epitope OR TITLE_ABS:structure OR TITLE_ABS:binding)',
            "format": "json", "pageSize": 100,
        }),
        "fda": "https://api.fda.gov/drug/drugsfda.json?" + urlencode({
            "search": 'openfda.generic_name:(omburtamab OR enoblituzumab OR ifinatamab '
                      'OR vobramitamab OR risvutatug OR b7-h3 OR cd276)',
            "limit": 100,
        }),
    }
    for name, url in sources.items():
        print(f"Fetching {name}: {url}", flush=True)
        try:
            with urlopen(url, timeout=20) as response:
                payload = json.load(response)
        except (OSError, ValueError) as exc:
            print(f"{name}: {exc}", file=sys.stderr)
            continue
        Path(f"work/04_10_parallel_readiness/{name}.json").write_text(
            json.dumps(payload, indent=2) + "\n")


def coverage():
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("arm", "parent", "input", "chain", "input_length",
                     "rf2_length", "exact_sequence_match", "rf2_first", "rf2_last"))
    for arm, expected in (("A", 40), ("B", 29)):
        with Path(f"results/04_09_path_launch/04_09_arm_{arm.lower()}_parent_lengths.tsv").open() as file:
            parents = list(csv.DictReader(file, delimiter="\t"))
        assert len(parents) == expected
        for parent in parents:
            af3 = json.loads(Path(parent["af3_input"]).read_text())
            input_chains = {item["protein"]["id"]: item["protein"]["sequence"]
                            for item in af3["sequences"]}
            coordinates = pdb_sequences(parent["rf2_parent"], {"H", "L"})
            for chain in ("H", "L"):
                sequence = input_chains[chain + arm]
                residues = coordinates[chain]
                observed = "".join(aa for _, aa in residues)
                output.writerow((arm, parent["parent"], parent["af3_input"], chain,
                                 len(sequence), len(observed), sequence == observed,
                                 residues[0][0], residues[-1][0]))


def pilot():
    target = Path("data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb")
    full = dict(pdb_sequences(target, {"A"})["A"])
    print("RFantibody checkout:", subprocess.check_output(
        ["git", "-C", str(scratch / "third_party/RFantibody"), "rev-parse", "HEAD"],
        text=True).strip())
    print("Full target:", target)
    print("Arm\tCrop\tFirst\tLast\tResidues\tCanonical sequence discrepancies")
    for arm in ("A", "B"):
        crop = scratch / "rfantibody_inputs_corrected3" / f"target_{arm}.pdb"
        residues = pdb_sequences(crop, {"T"})["T"]
        mismatches = [str(number) for number, aa in residues if full.get(number) != aa]
        print(arm, crop, residues[0][0], residues[-1][0], len(residues),
              ",".join(mismatches) or "none", sep="\t")
    print("Baseline script: tools/04_design_sequence/rfantibody_b7h3_backbone_pilot_array.sh")
    print("Baseline records: results/04_09_path_launch/04_09_path_c_baseline.tsv")


{"references": references, "coverage": coverage, "pilot": pilot}[sys.argv[1]]()
