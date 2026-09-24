#!/usr/bin/env python3
"""Audit RFantibody H/L/T chains, target coordinates, and interface geometry."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def read_atoms(path: Path):
    atoms = []
    seen = set()
    for line in path.read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        try:
            chain = line[21]
            residue = int(line[22:26])
            atom_name = line[12:16].strip()
            xyz = tuple(float(line[i : i + 8]) for i in (30, 38, 46))
        except (ValueError, IndexError):
            continue
        element = line[76:78].strip().upper()
        if not element:
            element = next((char for char in atom_name if char.isalpha()), "").upper()
        key = (chain, residue, atom_name)
        if key in seen:
            continue
        seen.add(key)
        atoms.append((key, xyz, element))
    return atoms


def interface_measure(atoms):
    antibody = [a for a in atoms if a[0][0] in ("H", "L") and a[2] != "H"]
    target = [a for a in atoms if a[0][0] == "T" and a[2] != "H"]
    if not antibody or not target:
        return None
    minimum = (float("inf"), None, None)
    contacts = overlaps = 0
    for a in antibody:
        ax, ay, az = a[1]
        for t in target:
            tx, ty, tz = t[1]
            distance = math.sqrt(
                (ax - tx) ** 2 + (ay - ty) ** 2 + (az - tz) ** 2
            )
            if distance < 4.5:
                contacts += 1
            if distance < 2.0:
                overlaps += 1
            if distance < minimum[0]:
                minimum = (distance, a[0], t[0])
    return minimum[0], contacts, overlaps, minimum[1], minimum[2]


def target_rmsd(reference, current):
    ref = {key: xyz for key, xyz, _ in reference if key[0] == "T"}
    cur = {key: xyz for key, xyz, _ in current if key[0] == "T"}
    shared = sorted(set(ref) & set(cur))
    if not shared:
        return 0, None, None
    sq = []
    max_shift = (0.0, None)
    for key in shared:
        d = math.dist(ref[key], cur[key])
        sq.append(d * d)
        if d > max_shift[0]:
            max_shift = (d, key)
    return len(shared), math.sqrt(sum(sq) / len(sq)), max_shift


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, help="label=path")
    parser.add_argument("pdb", nargs="+", help="label=path entries")
    args = parser.parse_args()

    entries = [args.reference] + args.pdb
    parsed = {}
    for entry in entries:
        label, raw_path = entry.split("=", 1)
        path = Path(raw_path)
        parsed[label] = (path, read_atoms(path))

    ref_label = args.reference.split("=", 1)[0]
    ref_atoms = parsed[ref_label][1]
    print(
        "label\tpath\tH_atoms\tL_atoms\tT_atoms\tT_residue_span\t"
        "min_HL_T_A\tcontacts_lt_4.5\toverlaps_lt_2.0\tshared_T_atoms\t"
        "T_RMSD_vs_ref_A\tT_max_shift_A"
    )
    for label, (path, atoms) in parsed.items():
        counts = {chain: sum(a[0][0] == chain for a in atoms) for chain in "HLT"}
        target_residues = sorted({a[0][1] for a in atoms if a[0][0] == "T"})
        span = f"{target_residues[0]}-{target_residues[-1]}" if target_residues else "NA"
        geometry = interface_measure(atoms)
        if geometry is None:
            minimum = contacts = overlaps = closest_a = closest_t = "NA"
        else:
            minimum, contacts, overlaps, closest_a, closest_t = geometry
            minimum = f"{minimum:.3f}"
        shared, rmsd, max_shift = target_rmsd(ref_atoms, atoms)
        rmsd_text = "NA" if rmsd is None else f"{rmsd:.3f}"
        max_text = "NA" if max_shift[1] is None else f"{max_shift[0]:.3f}"
        print(
            "\t".join(
                [
                    label,
                    str(path),
                    str(counts["H"]),
                    str(counts["L"]),
                    str(counts["T"]),
                    span,
                    str(minimum),
                    str(contacts),
                    str(overlaps),
                    str(shared),
                    rmsd_text,
                    max_text,
                ]
            )
        )
        if geometry is not None:
            print(f"# {label} closest_pair={closest_a}-{closest_t}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
