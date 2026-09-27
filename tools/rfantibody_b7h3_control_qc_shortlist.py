#!/usr/bin/env python3
"""Build a task-deduplicated shortlist using the official RF2 control gate."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


CONTROL_MIN_DISTANCE = 3.167


def load(path: Path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def task_id(path: str) -> str:
    match = re.search(r"/task_(\d+)/", path)
    return match.group(1) if match else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("arm", choices=("A", "B"))
    parser.add_argument("qc", type=Path)
    parser.add_argument("interface", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    qc = {row["file"]: row for row in load(args.qc)}
    interface = {row["file"]: row for row in load(args.interface)}
    candidates = []
    for path, row in qc.items():
        if path not in interface:
            continue
        if float(row["min_hl_t_angstrom"]) < CONTROL_MIN_DISTANCE:
            continue
        if int(row["overlaps_lt_2_0"]) != 0:
            continue
        iface = interface[path]
        candidates.append({
            "file": path,
            "arm": args.arm,
            "rf2_task": task_id(path),
            "min_hl_t_angstrom": row["min_hl_t_angstrom"],
            "contacts_lt_4_5": row["contacts_lt_4_5"],
            "selected_epitope_contacts": iface["selected_epitope_contacts"],
            "selected_epitope_residues": iface["selected_epitope_residues"],
            "target_contact_residues": iface["target_contact_residues"],
            "antibody_chains_with_contacts": iface["antibody_chains_with_contacts"],
            "control_gate": "PASS",
        })
    # Keep the strongest interface representative for each RF2 task/backbone.
    candidates.sort(key=lambda r: (
        int(r["selected_epitope_contacts"]),
        int(r["target_contact_residues"]),
        float(r["min_hl_t_angstrom"]),
        int(r["contacts_lt_4_5"]),
    ), reverse=True)
    unique = {}
    for row in candidates:
        unique.setdefault(row["rf2_task"], row)
    selected = sorted(unique.values(), key=lambda r: (
        int(r["selected_epitope_contacts"]),
        int(r["target_contact_residues"]),
        float(r["min_hl_t_angstrom"]),
    ), reverse=True)
    fields = list(selected[0]) if selected else [
        "file", "arm", "rf2_task", "min_hl_t_angstrom", "contacts_lt_4_5",
        "selected_epitope_contacts", "selected_epitope_residues",
        "target_contact_residues", "antibody_chains_with_contacts", "control_gate"
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
    print(f"arm={args.arm} control_gate_candidates={len(candidates)} task_deduplicated={len(selected)} output={args.output}")


if __name__ == "__main__":
    raise SystemExit(main())
