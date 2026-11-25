"""Review framework termini, experimental contacts, and historical crop placement."""
import csv
import os
import sys
from math import dist
from pathlib import Path

sys.path.insert(0, "tools/07_fab_categories")
from prepare_fab_category_input import pdb_sequences

scratch = Path(os.environ["MAB_SCRATCH_ROOT"])
inputs = scratch / "rfantibody_inputs_corrected3"


def parent_termini(arm):
    framework = pdb_sequences(inputs / "framework_HLT.pdb", {"H", "L"})
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("arm", "parent", "chain", "parent_length", "framework_length",
                     "n_terminal_8_match", "c_terminal_8_match"))
    with Path(f"results/04_09_path_launch/04_09_arm_{arm.lower()}_parent_lengths.tsv").open() as file:
        for row in csv.DictReader(file, delimiter="\t"):
            parent = pdb_sequences(row["rf2_parent"], {"H", "L"})
            for chain in ("H", "L"):
                actual = "".join(aa for _, aa in parent[chain])
                expected = "".join(aa for _, aa in framework[chain])
                output.writerow((arm, row["parent"], chain, len(actual), len(expected),
                                 actual[:8] == expected[:8], actual[-8:] == expected[-8:]))


def atoms(path):
    for line in path.read_text().splitlines():
        if line.startswith("ATOM  ") and line[76:78].strip() not in {"H", "D"}:
            yield (line[21], int(line[22:26]), line[12:16].strip(),
                   tuple(float(line[i:i + 8]) for i in (30, 38, 46)))


def references():
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("structure", "antigen_chain", "canonical_residue", "nearest_fab_A"))
    patch = (228, 229, 232, 234, 236, 238, 240, 241)
    with Path("metadata/numbering_map.csv").open() as file:
        mappings = list(csv.DictReader(file))
    for entry, antigen, antibody in (("9LY5", "C", "AB"), ("9LY6", "A", "BCDE")):
        positions = {int(row["model_residue"]): int(row["canonical_residue"])
                     for row in mappings if row["source"] == entry and row["chain"] == antigen}
        structure = list(atoms(Path(f"data/raw/structures/{entry}.pdb")))
        fab = [xyz for chain, _, _, xyz in structure if chain in antibody]
        for residue in patch:
            distances = [dist(xyz, other) for chain, index, _, xyz in structure
                         if chain == antigen and positions.get(index) == residue for other in fab]
            output.writerow((entry, antigen, residue, f"{min(distances):.3f}" if distances else "NA"))


def pilot():
    import numpy as np

    full = list(atoms(Path("data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb")))
    full_ca = {residue: xyz for chain, residue, name, xyz in full if chain == "A" and name == "CA"}
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("arm", "prior_task", "target_ca_count", "alignment_rmsd_A",
                     "outside_crop_min_distance_A", "outside_crop_pairs_below_2_A"))
    for arm in ("A", "B"):
        crop = pdb_sequences(inputs / f"target_{arm}.pdb", {"T"})["T"]
        outside = np.asarray([xyz for chain, residue, _, xyz in full
                              if chain == "A" and not crop[0][0] <= residue <= crop[-1][0]])
        for task in range(20):
            prior = scratch / "rfantibody_b7h3_backbone_pilot_20260925" / arm / f"task_{task}/ab_0.pdb"
            design = list(atoms(prior))
            target = [xyz for chain, _, name, xyz in design if chain == "T" and name == "CA"]
            assert len(target) == len(crop), prior
            target_sequence = [aa for _, aa in pdb_sequences(prior, {"T"})["T"]]
            assert target_sequence == [aa for _, aa in crop], prior
            source = np.asarray(target)
            destination = np.asarray([full_ca[residue] for residue, _ in crop])
            u, _, vt = np.linalg.svd((source - source.mean(0)).T @ (destination - destination.mean(0)))
            rotation = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
            offset = destination.mean(0) - source.mean(0) @ rotation
            rmsd = np.sqrt(np.mean(np.sum((source @ rotation + offset - destination) ** 2, axis=1)))
            binder = np.asarray([xyz for chain, _, _, xyz in design if chain in {"H", "L"}])
            distances = np.linalg.norm((binder @ rotation + offset)[:, None] - outside, axis=2)
            output.writerow((arm, task, len(crop), f"{rmsd:.3f}", f"{distances.min():.3f}",
                             int((distances < 2).sum())))


mode = sys.argv[1]
if mode in {"A", "B"}:
    parent_termini(mode)
elif mode == "references":
    references()
elif mode == "pilot":
    pilot()
else:
    raise SystemExit(f"Unknown mode: {mode}")
