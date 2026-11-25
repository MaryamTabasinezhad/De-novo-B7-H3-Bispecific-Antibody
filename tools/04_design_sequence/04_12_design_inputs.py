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


def atoms(path):
    for line in path.read_text().splitlines():
        if line.startswith("ATOM  ") and line[76:78].strip() not in {"H", "D"}:
            yield (line[21], int(line[22:26]), line[12:16].strip(),
                   tuple(float(line[i:i + 8]) for i in (30, 38, 46)))


def pilot():
    import numpy as np

    full = list(atoms(Path("data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb")))
    full_ca = {residue: xyz for chain, residue, name, xyz in full if chain == "A" and name == "CA"}
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("arm", "prior_task", "target_ca_count", "alignment_rmsd_A",
                     "outside_crop_min_distance_A", "outside_crop_pairs_below_2_A",
                     "clashing_canonical_residues"))
    for arm in ("A", "B"):
        crop = pdb_sequences(inputs / f"target_{arm}.pdb", {"T"})["T"]
        outside_atoms = [(residue, xyz) for chain, residue, _, xyz in full
                         if chain == "A" and not crop[0][0] <= residue <= crop[-1][0]]
        outside_residues = np.asarray([residue for residue, _ in outside_atoms])
        outside = np.asarray([xyz for _, xyz in outside_atoms])
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
            close = distances < 2
            clash_residues = sorted(set(outside_residues[close.any(axis=0)]))
            output.writerow((arm, task, len(crop), f"{rmsd:.3f}", f"{distances.min():.3f}",
                             int(close.sum()), ",".join(map(str, clash_residues)) or "NA"))


def parent_alignment(arm):
    from difflib import SequenceMatcher

    reference = pdb_sequences(inputs / "framework_HLT.pdb", {"H", "L"})
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("arm", "parent", "chain", "framework_reference_positions",
                     "exactly_aligned_positions", "nonmatching_blocks"))
    index = Path(f"results/04_09_path_launch/04_09_arm_{arm.lower()}_parent_lengths.tsv")
    with index.open() as file:
        for row in csv.DictReader(file, delimiter="\t"):
            observed = pdb_sequences(row["rf2_parent"], {"H", "L"})
            for chain in ("H", "L"):
                ref = "".join(aa for _, aa in reference[chain])
                seq = "".join(aa for _, aa in observed[chain])
                alignment = SequenceMatcher(None, ref, seq, autojunk=False)
                changes = [
                    f"{tag}:reference[{r0 + 1}:{r1 + 1})={ref[r0:r1]}"
                    f":parent[{s0 + 1}:{s1 + 1})={seq[s0:s1]}"
                    for tag, r0, r1, s0, s1 in alignment.get_opcodes() if tag != "equal"
                ]
                writer.writerow((arm, row["parent"], chain, len(ref),
                                 sum(match.size for match in alignment.get_matching_blocks()),
                                 ";".join(changes)))


def references():
    raw = Path("data/raw/structures/9LY5.cif").read_text().splitlines()
    scheme_start = raw.index("_pdbx_poly_seq_scheme.hetero ") + 1
    patch = {228: "GLN", 229: "GLN", 232: "HIS", 234: "SER",
             236: "THR", 238: "THR", 240: "GLN", 241: "ARG"}
    structure = list(atoms(Path("data/raw/structures/9LY5.pdb")))
    fab = [xyz for chain, _, _, xyz in structure if chain in "AB"]
    output = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    output.writerow(("canonical_residue", "reference_residue", "pdb_author_number",
                     "minimum_20G5_heavy_atom_distance_A"))
    for line in raw[scheme_start:]:
        if line.startswith("#"):
            break
        columns = line.split()
        if not columns or columns[0] != "C":
            continue
        label, monomer, author_number = int(columns[2]), columns[3], columns[6]
        canonical = label + 28  # 9LY5 _struct_ref_seq C aligns label 1–433 to Q5ZPR3 29–461.
        if canonical not in patch:
            continue
        assert monomer == patch[canonical], (canonical, monomer)
        if author_number == "?":
            output.writerow((canonical, monomer, "unresolved", "NA"))
            continue
        distances = [dist(xyz, other) for chain, residue, _, xyz in structure
                     if chain == "C" and residue == int(author_number) for other in fab]
        output.writerow((canonical, monomer, author_number, f"{min(distances):.3f}" if distances else "NA"))


mode = sys.argv[1]
if mode in {"A", "B"}:
    parent_alignment(mode)
elif mode == "references":
    references()
elif mode == "pilot":
    pilot()
else:
    raise SystemExit(f"Unknown mode: {mode}")
