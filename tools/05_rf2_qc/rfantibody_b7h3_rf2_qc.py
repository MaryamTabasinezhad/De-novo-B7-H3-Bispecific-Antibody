#!/usr/bin/env python3
"""Summarize RF2 H/L-to-target heavy-atom geometry for recursive PDB outputs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from scipy.spatial import cKDTree


def atoms_for(path: Path):
    atoms = {"H": [], "L": [], "T": []}
    for line in path.read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        chain = line[21]
        if chain not in atoms:
            continue
        atom_name = line[12:16].strip()
        element = line[76:78].strip().upper()
        if not element:
            element = next((char for char in atom_name if char.isalpha()), "").upper()
        if element == "H":
            continue
        try:
            xyz = tuple(float(line[i : i + 8]) for i in (30, 38, 46))
            residue = int(line[22:26])
        except (ValueError, IndexError):
            continue
        atoms[chain].append((xyz, residue, line[17:20].strip()))
    return atoms


def measure(path: Path):
    atoms = atoms_for(path)
    antibody = [(xyz, residue, resname, chain) for chain in ("H", "L") for xyz, residue, resname in atoms[chain]]
    target = atoms["T"]
    if not antibody or not target:
        raise ValueError(f"{path}: missing H/L/T heavy atoms")
    target_xyz = [record[0] for record in target]
    antibody_xyz = [record[0] for record in antibody]
    tree = cKDTree(target_xyz)
    distances, indices = tree.query(antibody_xyz, k=1)
    contacts = sum(len(hits) for hits in tree.query_ball_point(antibody_xyz, r=4.5))
    overlaps = sum(len(hits) for hits in tree.query_ball_point(antibody_xyz, r=2.0))
    closest_idx = min(range(len(distances)), key=distances.__getitem__)
    closest_antibody = antibody[closest_idx]
    closest_target = target[indices[closest_idx]]
    return {
        "file": str(path),
        "min_hl_t_angstrom": float(distances[closest_idx]),
        "contacts_lt_4_5": contacts,
        "overlaps_lt_2_0": overlaps,
        "closest_pair": f"{closest_antibody[3]}:{closest_antibody[1]}{closest_antibody[2]}-T:{closest_target[1]}{closest_target[2]}",
        "status": "PASS" if distances[closest_idx] >= 2.0 and overlaps == 0 else "REJECT",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    paths = sorted(args.root.glob("task_*/*_best.pdb"))
    if not paths:
        parser.error(f"no RF2 best PDB files found below {args.root}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["file", "min_hl_t_angstrom", "contacts_lt_4_5", "overlaps_lt_2_0", "closest_pair", "status"]
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for path in paths:
            writer.writerow(measure(path))
    print(f"processed={len(paths)} output={args.output}")


if __name__ == "__main__":
    raise SystemExit(main())
