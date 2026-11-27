"""Map Arm A loop contacts and prepare a canonical-numbered HLT refinement input."""
import csv
from importlib import import_module
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist

format_a = import_module("04_12_arm_a_format")
qc = format_a.qc
source = Path("results/04_22_arm_a_conditioned")
output = Path("results/04_24_arm_a_h3_refinement")


def main():
    full = list(qc.atoms(qc.FULL, "A"))
    lookup = {(r, n): xyz for _, r, n, xyz in full}
    table = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    table.writerow(("seed", "anchor", "loop", "fv_atom", "target_atom", "distance_A"))
    for seed, placement in ((421, 2), (412, 1)):
        p = source / f"04_22_seed_{seed}.pdb"
        crop = qc.pdb_sequences(source / f"04_22_pose_{placement}.pdb", {"T"})["T"]
        target = qc.pdb_sequences(p, {"T"})["T"]
        assert [a for _, a in target] == [a for _, a in crop]
        rotation, offset = qc.fit(
            np.array([xyz for _, _, name, xyz in qc.atoms(p, "T") if name == "CA"]),
            np.array([lookup[r, "CA"] for r, _ in crop]))
        binder = list(qc.atoms(p, "HL"))
        placed = np.array([row[3] for row in binder]) @ rotation + offset
        _, _, ranges, chains = format_a.domain_blocks(p)
        loops = {(loop[0], chains[loop[0]][i - 1][0]): loop
                 for loop, positions in ranges.items() for i in positions}
        for anchor in sorted(qc.ARMS["A"][2]):
            antigen = [row for row in full if row[1] == anchor]
            distances = cdist(placed, [row[3] for row in antigen])
            for loop in (*format_a.LOOPS, "framework"):
                indices = [i for i, row in enumerate(binder)
                           if loops.get(row[:2], "framework") == loop]
                i, j = np.unravel_index(distances[indices].argmin(),
                                        (len(indices), len(antigen)))
                table.writerow((seed, anchor, loop, qc.atom_id(binder[indices[i]]),
                                qc.atom_id(antigen[j]), f"{distances[indices[i], j]:.3f}"))
        if seed == 412:
            mapping = {old: new for (old, _), (new, _) in zip(target, crop)}
            lines = []
            for line in p.read_text().splitlines():
                if line.startswith("ATOM  "):
                    xyz = np.array([float(line[i:i + 8]) for i in (30, 38, 46)])
                    if line[21] == "T":
                        line = line[:22] + f"{mapping[int(line[22:26])]:4d}" + line[26:]
                    line = line[:30] + "".join(f"{x:8.3f}" for x in xyz @ rotation + offset) + line[54:]
                lines.append(line)
            (output / "04_24_seed_412_input.pdb").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
