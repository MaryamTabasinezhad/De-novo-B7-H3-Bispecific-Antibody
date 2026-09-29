#!/usr/bin/env python3
"""Screen RF2 geometry-passing models for target-interface contacts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from scipy.spatial import cKDTree


EPITOPES = {
    "A": {"target_start": 86, "selected": {126, 127, 128, 129}},
    "B": {"target_start": 188, "selected": {228, 229, 232, 234, 236, 238, 240, 241}},
}


def parse_atoms(path: Path):
    atoms = {"H": [], "L": [], "T": []}
    for line in path.read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        chain = line[21]
        if chain not in atoms:
            continue
        element = line[76:78].strip().upper() or next(
            (char for char in line[12:16] if char.isalpha()), ""
        ).upper()
        if element == "H":
            continue
        try:
            xyz = tuple(float(line[i : i + 8]) for i in (30, 38, 46))
            residue = int(line[22:26])
        except (ValueError, IndexError):
            continue
        atoms[chain].append((xyz, residue))
    return atoms


def screen(path: Path, arm: str):
    atoms = parse_atoms(path)
    antibody = [(xyz, chain, residue) for chain in ("H", "L") for xyz, residue in atoms[chain]]
    target = atoms["T"]
    if not antibody or not target:
        raise ValueError(f"{path}: missing H/L/T atoms")
    tree = cKDTree([xyz for xyz, _ in target])
    hits = tree.query_ball_point([xyz for xyz, _, _ in antibody], r=4.5)
    target_residues = set()
    selected_residues = set()
    chains = set()
    target_min = min(residue for _, residue in target)
    start = EPITOPES[arm]["target_start"]
    for (_, chain, _), indices in zip(antibody, hits):
        if indices:
            chains.add(chain)
        for index in indices:
            canonical = start + (target[index][1] - target_min)
            target_residues.add(canonical)
            if canonical in EPITOPES[arm]["selected"]:
                selected_residues.add(canonical)
    return {
        "file": str(path),
        "arm": arm,
        "target_output_range": f"{target_min}-{max(residue for _, residue in target)}",
        "target_contact_residues": len(target_residues),
        "selected_epitope_contacts": len(selected_residues),
        "selected_epitope_residues": ",".join(str(x) for x in sorted(selected_residues)) or "-",
        "antibody_chains_with_contacts": ",".join(sorted(chains)) or "-",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("arm", choices=("A", "B"))
    parser.add_argument("qc_tsv", type=Path)
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    paths = []
    with args.qc_tsv.open() as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["status"] == "PASS":
                paths.append(Path(row["file"]))
    fields = ["file", "arm", "target_output_range", "target_contact_residues", "selected_epitope_contacts", "selected_epitope_residues", "antibody_chains_with_contacts"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for path in paths:
            writer.writerow(screen(path, args.arm))
    print(f"processed={len(paths)} output={args.output}")


if __name__ == "__main__":
    raise SystemExit(main())
