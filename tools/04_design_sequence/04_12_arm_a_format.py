"""Audit the Arm A HLT scaffold, parent cohort, and pilot pose diversity."""
import csv
from importlib import import_module
from pathlib import Path

import numpy as np

# Import the numbered QC file without changing its run-as-script entry point.

qc = import_module("04_12_expanded_context_qc")
LOOPS = ("H1", "H2", "H3", "L1", "L2", "L3")
BOUNDS = ((7, 7), (6, 6), (5, 13), (8, 13), (7, 7), (9, 11))
RESULTS = Path("results/04_12_design_inputs")


def domain_blocks(path):
    residues = qc.pdb_sequences(path, {"H", "L"})
    labels = {}
    for line in path.read_text().splitlines():
        if line.startswith("REMARK PDBinfo-LABEL:"):
            _, _, index, label = line.split()[:4]
            if label in LOOPS:
                labels[int(index)] = label
    blocks, lengths, ranges = {}, {}, {}
    for chain in ("H", "L"):
        frameworks = [""]
        previous = ""
        for position, (number, aa) in enumerate(residues[chain], 1):
            label = labels.get(number, "")
            if label:
                assert label[0] == chain, (path, number, label)
                lengths[label] = lengths.get(label, 0) + 1
                ranges.setdefault(label, []).append(position)
                if label != previous:
                    frameworks.append("")
            else:
                frameworks[-1] += aa
            previous = label
        assert len(frameworks) == 4 and all(frameworks), path
        blocks[chain] = frameworks
    assert tuple(lengths) == LOOPS, path
    ca_positions = {(chain, number) for chain, number, name, _ in qc.atoms(path, "HL")
                    if name == "CA"}
    assert ca_positions == {(chain, number) for chain in "HL"
                            for number, _ in residues[chain]}, path
    assert all(positions == list(range(positions[0], positions[-1] + 1))
               for positions in ranges.values()), path
    return blocks, lengths, ranges, residues


def main():
    scaffold = qc.SCRATCH / "rfantibody_inputs_corrected3/framework_HLT.pdb"
    reference, *_ = domain_blocks(scaffold)
    run = qc.SCRATCH / "04_12_context_pilot/A/27635726"
    with Path("results/04_09_path_launch/04_09_arm_a_parent_lengths.tsv").open() as handle:
        parents = list(csv.DictReader(handle, delimiter="\t"))
    assert len({row["parent"] for row in parents}) == len(parents) == 40
    parent_sizes = {row["parent"]: (int(row["vh_length"]), int(row["vl_length"]))
                    for row in parents}
    entries = [("scaffold", "HLT", scaffold)]
    entries += [("pilot", f"A{i}", run / f"ab_{i}.pdb") for i in range(4)]
    entries += [("parent", row["parent"], Path(row["rf2_parent"])) for row in parents]

    with (RESULTS / "04_12_arm_a_format.tsv").open("w") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("cohort", "model", "vh_length", "vl_length", *LOOPS,
                         "vh_fixed_blocks_match", "vl_fixed_blocks_match",
                         "vh_terminal_8_match", "vl_terminal_8_match",
                         "within_pilot_loop_bounds",
                         *(f"{loop}_chain_positions" for loop in LOOPS)))
        for cohort, model, path in entries:
            blocks, lengths, ranges, residues = domain_blocks(path)
            sizes = (len(residues["H"]), len(residues["L"]))
            if cohort == "parent":
                assert sizes == parent_sizes[model], path
            writer.writerow((cohort, model, *sizes,
                             *(lengths[loop] for loop in LOOPS),
                             *(blocks[c] == reference[c] for c in "HL"),
                             *(blocks[c][0][:8] == reference[c][0][:8]
                               and blocks[c][-1][-8:] == reference[c][-1][-8:] for c in "HL"),
                             all(lo <= lengths[loop] <= hi
                                 for loop, (lo, hi) in zip(LOOPS, BOUNDS)),
                             *(f"{ranges[loop][0]}-{ranges[loop][-1]}" for loop in LOOPS)))

    lookup = {(r, n): xyz for _, r, n, xyz in qc.atoms(qc.FULL, "A")}
    patch = np.mean([lookup[r, "CA"] for r in sorted(qc.ARMS["A"][2])], axis=0)
    directions = {}
    for model in range(4):
        binder, placed = qc.place_pilot_model("A", model, lookup)
        ends = []
        for chain in "HL":
            positions = [i for i, (c, _, name, _) in enumerate(binder)
                         if c == chain and name == "CA"]
            ends.extend(positions[-8:])
        vector = placed[ends].mean(axis=0) - patch
        directions[model] = vector / np.linalg.norm(vector)
    with (RESULTS / "04_12_arm_a_approach.tsv").open("w") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("model_1", "model_2", "approach_angle_deg"))
        for i in directions:
            for j in range(i + 1, len(directions)):
                cosine = np.clip(directions[i] @ directions[j], -1, 1)
                writer.writerow((f"A{i}", f"A{j}", f"{np.degrees(np.arccos(cosine)):.1f}"))


if __name__ == "__main__":
    main()
