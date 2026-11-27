"""Audit ProteinMPNN sequence coverage and write matched full-Fab AF3 inputs."""
import csv
from importlib import import_module
import json
from pathlib import Path
import sys

format_a = import_module("04_12_arm_a_format")
qc = format_a.qc
three_to_one = import_module("prepare_fab_category_input").AA
stage = Path("results/04_26_arm_a_sequence_pilot")
backbones = Path("results/04_22_arm_a_conditioned")
scratch = qc.SCRATCH / stage.name
pdb = Path("data/raw/structures/9LY5.pdb")
constants = {}
for chain, end in (("A", 118), ("B", 106)):
    codes = [aa for line in pdb.read_text().splitlines()
             if line.startswith("SEQRES") and line[11] == chain
             for aa in line[19:70].split()]
    constants[chain] = "".join(three_to_one[aa] for aa in codes[end:])
assert len(constants["A"]) == 105 and len(constants["B"]) == 107
target = "".join(aa for number, aa in qc.pdb_sequences(qc.FULL, {"A"})["A"]
                 if 29 <= number <= 466)
assert len(target) == 438

table = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
table.writerow(("backbone", "sample", "VH", "VL", "H1", "H2", "H3", "L1", "L2", "L3",
                "fixed_framework", "first_occurrence"))
for spec in sys.argv[1:]:
    seed_text, job = spec.split(":")
    seed = int(seed_text)
    run = scratch / job
    reference, loop_lengths, _, _ = format_a.domain_blocks(backbones / f"04_22_seed_{seed}.pdb")
    paths = sorted((run / str(seed) / "output").glob("*_dldesign_*.pdb"))
    assert len(paths) == 4, paths
    seen = set()
    for index, path in enumerate(paths):
        blocks, lengths, ranges, chains = format_a.domain_blocks(path)
        assert blocks == reference and lengths == loop_lengths, path
        seq = {c: "".join(aa for _, aa in chains[c]) for c in ("H", "L")}
        assert all(set(s) <= set("ACDEFGHIKLMNPQRSTVWY") for s in seq.values()), path
        pair = (seq["H"], seq["L"])
        loops = ["".join(seq[loop[0]][i - 1] for i in ranges[loop]) for loop in format_a.LOOPS]
        table.writerow((seed, index, *pair, *loops, True, pair not in seen))
        seen.add(pair)
        if index == 0:
            af3 = {"name": f"arma_{seed}_mpnn0_fullfab", "modelSeeds": [101, 202],
                   "sequences": [
                       {"protein": {"id": "H", "sequence": seq["H"] + constants["A"]}},
                       {"protein": {"id": "L", "sequence": seq["L"] + constants["B"]}},
                       {"protein": {"id": "T", "sequence": target}}],
                   "dialect": "alphafold3", "version": 1}
            (stage / f"04_26_seed_{seed}_af3.json").write_text(json.dumps(af3, indent=2) + "\n")
