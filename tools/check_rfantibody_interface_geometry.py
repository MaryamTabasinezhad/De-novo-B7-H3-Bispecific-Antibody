#!/usr/bin/env python3
"""Measure H/L-to-T heavy-atom geometry in RFantibody PDB outputs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def atoms_for(path: Path):
    atoms = {"H": [], "L": [], "T": []}
    for line in path.read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        chain = line[21]
        if chain not in atoms:
            continue
        element = (line[76:78].strip() or line[12:16].strip()[0]).upper()
        if element == "H":
            continue
        try:
            xyz = tuple(float(line[i : i + 8]) for i in (30, 38, 46))
            residue = int(line[22:26])
        except (ValueError, IndexError):
            continue
        atoms[chain].append(
            (xyz, residue, line[17:20].strip(), line[12:16].strip())
        )
    return atoms


def measure(path: Path):
    atoms = atoms_for(path)
    pairs = []
    for chain in ("H", "L"):
        for antibody_atom in atoms[chain]:
            ax, ay, az = antibody_atom[0]
            for target_atom in atoms["T"]:
                bx, by, bz = target_atom[0]
                distance = math.sqrt(
                    (ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2
                )
                pairs.append((distance, chain, antibody_atom, target_atom))
    if not pairs:
        raise ValueError(f"{path}: missing H/L/T atoms")
    pairs.sort(key=lambda pair: pair[0])
    minimum, chain, antibody_atom, target_atom = pairs[0]
    return {
        "file": str(path),
        "h_atoms": len(atoms["H"]),
        "l_atoms": len(atoms["L"]),
        "t_atoms": len(atoms["T"]),
        "min_hl_t_angstrom": minimum,
        "contacts_lt_4_5": sum(pair[0] < 4.5 for pair in pairs),
        "overlaps_lt_2_0": sum(pair[0] < 2.0 for pair in pairs),
        "closest_pair": (
            f"{chain}:{antibody_atom[1]}{antibody_atom[2]}"
            f"-{target_atom[1]}{target_atom[2]}"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdb_dir", type=Path)
    args = parser.parse_args()
    paths = sorted(args.pdb_dir.glob("*.pdb"))
    if not paths:
        parser.error(f"no PDB files found in {args.pdb_dir}")
    print(
        "file\th_atoms\tl_atoms\tt_atoms\tmin_hl_t_angstrom\t"
        "contacts_lt_4_5\toverlaps_lt_2_0\tclosest_pair"
    )
    for path in paths:
        result = measure(path)
        print(
            "\t".join(
                [
                    result["file"],
                    str(result["h_atoms"]),
                    str(result["l_atoms"]),
                    str(result["t_atoms"]),
                    f'{result["min_hl_t_angstrom"]:.3f}',
                    str(result["contacts_lt_4_5"]),
                    str(result["overlaps_lt_2_0"]),
                    result["closest_pair"],
                ]
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
