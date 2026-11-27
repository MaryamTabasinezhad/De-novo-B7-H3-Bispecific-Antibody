#!/usr/bin/env python3
"""Compare the matched intact-4Ig AlphaFold 3 parent and variant predictions."""
import argparse
import csv
import json
import sys
from math import dist
from pathlib import Path
from statistics import median

PATCH = {126, 127, 128, 129}
ANCHORS = PATCH | {135, 140}
CHAINS = ("HA", "LA", "T")


def metrics(path):
    patch_atoms = []
    fab_atoms = []
    anchors = {}
    alpha_carbons = {}
    for line in path.open():
        if not line.startswith("ATOM "):
            continue
        fields = line.split()
        if fields[2] == "H":
            continue
        chain, index = fields[6], int(fields[8])
        xyz = tuple(map(float, fields[10:13]))
        if chain == "T":
            canonical = index + 28
            if canonical in PATCH:
                patch_atoms.append((canonical, xyz))
            if canonical in ANCHORS and fields[3] == "CA":
                anchors[canonical] = xyz
        elif chain in CHAINS[:2]:
            fab_atoms.append(xyz)
            if fields[3] == "CA":
                alpha_carbons[chain, index] = xyz
    if set(anchors) != ANCHORS or not alpha_carbons:
        raise ValueError(f"Missing antigen anchors or Fab coordinates in {path}")
    hits = sorted({n for n, xyz in patch_atoms if any(dist(xyz, atom) <= 4.5 for atom in fab_atoms)})
    signature = {key: tuple(dist(xyz, anchors[n]) for n in sorted(anchors))
                 for key, xyz in alpha_carbons.items()}
    prefix = path.name.removesuffix("_model.cif")
    summary = json.loads(path.with_name(prefix + "_summary_confidences.json").read_text())
    tokens = json.loads(path.with_name(prefix + "_confidences.json").read_text())
    order = list(dict.fromkeys(tokens["token_chain_ids"]))
    h, l, t = (order.index(chain) for chain in CHAINS)
    iptm, pae = summary["chain_pair_iptm"], summary["chain_pair_pae_min"]
    return [",".join(map(str, hits)) or ".", int(len(hits) >= 2), iptm[h][t],
            iptm[l][t], pae[h][t], pae[l][t], summary["has_clash"]], signature


def samples(directory):
    return {path.parent.name: path for path in directory.glob("seed-*_sample-*/*_model.cif")}


def placement(a, b):
    if a.keys() != b.keys():
        raise ValueError("Parent and variant Fab Cα positions differ")
    return round(median(dist(a[k], b[k]) / len(ANCHORS)**0.5 for k in a), 2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parent", type=Path, help="Directory containing parent seed/sample folders")
    parser.add_argument("variant", type=Path, help="Directory containing variant seed/sample folders")
    args = parser.parse_args()
    parent, variant = samples(args.parent), samples(args.variant)
    expected = {f"seed-{seed}_sample-{sample}" for seed in (101, 202) for sample in (0, 1)}
    if parent.keys() != expected or variant.keys() != expected:
        parser.error(f"Expected four matched samples. Found {len(parent)} parent and {len(variant)} variant.")
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    columns = ("IgV1_contacts", "pass", "H_T_ipTM", "L_T_ipTM", "H_T_PAE_min_A",
               "L_T_PAE_min_A", "clash")
    writer.writerow(["comparison", *[f"{group}_{col}" for group in ("parent", "variant")
                                     for col in columns], "placement_difference_A"])
    signatures = {"parent": {}, "variant": {}}
    for key in sorted(expected):
        p, p_sig = metrics(parent[key])
        v, v_sig = metrics(variant[key])
        signatures["parent"][key] = p_sig
        signatures["variant"][key] = v_sig
        writer.writerow([key, *p, *v, placement(p_sig, v_sig)])
    for group, poses in signatures.items():
        for a in (0, 1):
            for b in (0, 1):
                distance = placement(poses[f"seed-101_sample-{a}"], poses[f"seed-202_sample-{b}"])
                writer.writerow([f"{group}:101/{a}_vs_202/{b}", *([""] * 14), distance])


if __name__ == "__main__":
    main()
