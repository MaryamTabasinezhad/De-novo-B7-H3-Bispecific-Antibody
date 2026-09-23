#!/usr/bin/env python3
"""Validate RFantibody framework/target input geometry and hotspot mapping."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def read_atoms(path: Path):
    atoms = []
    for line in path.read_text().splitlines():
        if not line.startswith("ATOM"):
            continue
        atom = line[12:16].strip()
        if atom == "CA" or (atom and atom[0] != "H"):
            atoms.append(
                {
                    "chain": line[21].strip() or "_",
                    "resnum": int(line[22:26]),
                    "resname": line[17:20].strip(),
                    "atom": atom,
                    "xyz": tuple(float(line[i : i + 8]) for i in (30, 38, 46)),
                }
            )
    return atoms


def min_distance(left, right):
    best = math.inf
    for a in left:
        for b in right:
            best = min(best, math.dist(a["xyz"], b["xyz"]))
    return best


def validate(framework: Path, target: Path, hotspots: list[int]):
    fa = read_atoms(framework)
    ta = read_atoms(target)
    chains = sorted({a["chain"] for a in fa + ta})
    ca_by_chain = {}
    for chain in chains:
        seen = {}
        for atom in fa + ta:
            if atom["chain"] == chain and atom["atom"] == "CA":
                seen.setdefault(atom["resnum"], atom)
        ca_by_chain[chain] = [seen[k] for k in sorted(seen)]
    target_res = {a["resnum"] for a in ta if a["chain"] == "T"}
    missing = [r for r in hotspots if r not in target_res]
    gaps = []
    target_ca = ca_by_chain.get("T", [])
    for a, b in zip(target_ca, target_ca[1:]):
        d = math.dist(a["xyz"], b["xyz"])
        if d > 4.5:
            gaps.append({"from": a["resnum"], "to": b["resnum"], "distance_A": round(d, 3)})
    antibody = [a for a in fa if a["chain"] in {"H", "L"}]
    target = [a for a in ta if a["chain"] == "T"]
    return {
        "framework": str(framework),
        "target": str(target),
        "chains": chains,
        "chain_residue_counts": {k: len(v) for k, v in ca_by_chain.items()},
        "hotspots": hotspots,
        "missing_hotspots": missing,
        "target_ca_gaps_over_4_5A": gaps,
        "min_antibody_target_heavy_atom_distance_A": round(min_distance(antibody, target), 3),
        "pass": chains == ["H", "L", "T"] and not missing and not gaps and min_distance(antibody, target) >= 1.5,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--framework", type=Path, required=True)
    ap.add_argument("--target-a", type=Path, required=True)
    ap.add_argument("--target-b", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = {
        "arm_A": validate(args.framework, args.target_a, [126, 127, 128, 129]),
        "arm_B": validate(args.framework, args.target_b, [228, 229, 232, 234, 236, 238, 240, 241]),
    }
    result["pass"] = result["arm_A"]["pass"] and result["arm_B"]["pass"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass"] else 2)


if __name__ == "__main__":
    main()
