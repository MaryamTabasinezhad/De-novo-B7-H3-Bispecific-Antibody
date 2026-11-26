"""Replay the AF3 Arm B pilot models against the prespecified geometry checks."""
import csv
from importlib import import_module
from itertools import chain as chain_lines
import json
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial.transform import Rotation

sys.path.insert(0, "tools/04_design_sequence")
core = import_module("04_19_arm_b_fab_clearance")
qc = core.qc


def predicted_atoms(path):
    # AF3 writes one atom per line in this loop, as in analyze_af3_shortlist.py.
    lines = iter(path.read_text().splitlines())
    for line in lines:
        if line == "_atom_site.group_PDB":
            break
    fields = ("auth_asym_id", "label_seq_id", "auth_seq_id", "label_atom_id",
              "type_symbol", "Cartn_x", "Cartn_y", "Cartn_z")
    columns = ["group_PDB"]
    for line in lines:
        if not line.startswith("_atom_site."):
            break
        columns.append(line.split(".", 1)[1])
    indices = [columns.index(field) for field in fields]
    for line in chain_lines((line,), lines):
        if not line.startswith(("ATOM ", "HETATM ")):
            break
        values = line.split()
        chain, seq, auth, name, element, x, y, z = (values[i] for i in indices)
        if element not in {"H", "D"}:
            yield chain, int(auth if seq == "." else seq), name, (float(x), float(y), float(z))


def angle(first, second):
    cosine = first @ second / (np.linalg.norm(first) * np.linalg.norm(second))
    return float(np.degrees(np.arccos(np.clip(cosine, -1, 1))))


def main(root):
    reference = list(qc.atoms(qc.FULL, "A"))
    lookup = {(res, name): xyz for _, res, name, xyz in reference}
    residues = sorted(qc.ARMS["B"][2])
    pivot = np.mean([lookup[r, "CA"] for r in residues], axis=0)
    cores = [xyz for _, _, _, _, xyz, clashes in core.n215_probes(lookup) if clashes == 0]
    tm = np.array([lookup[res, "CA"] for res in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    tilt = np.radians(10)
    archive = qc.SCRATCH / "rfantibody_b7h3_backbone_pilot_20260925/B"
    crop = qc.SCRATCH / "rfantibody_inputs_corrected3/target_B.pdb"
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("task", "sample", "iptm", "ht_iptm", "lt_iptm", "has_clash",
                     "target_fit_rmsd_A", "anchors_le4p5", "screened_anchors_retained",
                     "angle_to_original_deg", "angle_to_screened_deg", "protein_min_A",
                     "predicted_glycan_min_A", "n215_bond_A", "fixed_cores_min_A",
                     "tilted_clearance_A", "geometry_pass"))
    for task, euler, shift, required in (
        (248, (20, 0, 0), (2, 0, 0), {232, 234, 238, 240}),
        (152, (-10, 0, 0), (-2, 2, 2), {232, 234, 236, 240}),
    ):
        run = archive / f"task_{task}"
        binder, placed = qc.place_pilot_model("B", 0, lookup, run, crop)
        original = np.mean(np.vstack([
            np.array([p for (c, _, n, _), p in zip(binder, placed)
                      if c == chain and n == "CA"])[-8:] for chain in "HL"
        ]), axis=0) - pivot
        screened = Rotation.from_euler("xyz", euler, degrees=True).apply(original) + shift
        input_path = Path(f"results/04_23_arm_b_bound_pose/04_23_arm_b_task{task}_n215.json")
        entries = json.loads(input_path.read_text())["sequences"]
        fv_lengths = {e["protein"]["id"]: len(e["protein"]["sequence"]) - suffix
                      for e, suffix in zip(entries[:2], (105, 107))}
        models = sorted((root / f"task_{task}").glob("*/seed-*_sample-*/*_model.cif"))
        assert len(models) == 4, (task, models)
        for path in models:
            atoms = list(predicted_atoms(path))
            assert {c for c, *_ in atoms} == {"H", "L", "T", "G"}
            target_ca = {r: xyz for c, r, n, xyz in atoms if c == "T" and n == "CA"}
            assert set(target_ca) == set(range(1, 439))
            src = np.array([target_ca[r] for r in range(1, 439)])
            dest = np.array([lookup[r, "CA"] for r in range(29, 467)])
            rotation, offset = qc.fit(src, dest)
            fit_rmsd = np.sqrt(np.mean(np.sum((src @ rotation + offset - dest) ** 2, axis=1)))
            aligned = [(c, r, n, np.array(xyz) @ rotation + offset) for c, r, n, xyz in atoms]
            fab = [xyz for c, _, _, xyz in aligned if c in "HL"]
            fv = [xyz for c, r, _, xyz in aligned if c in "HL" and r <= fv_lengths[c]]
            tail = [xyz for c, r, n, xyz in aligned if c in "HL" and n == "CA"
                    and fv_lengths[c] - 8 < r <= fv_lengths[c]]
            assert len(tail) == 16
            direction = np.mean(tail, axis=0) - pivot
            target = [(r + 28, xyz) for c, r, _, xyz in aligned if c == "T"]
            contacts = {res for res in residues
                        if cdist(fv, [xyz for r, xyz in target if r == res]).min() <= 4.5}
            protein = cdist(fab, [xyz for _, xyz in target]).min()
            glycan = cdist(fab, [xyz for c, _, _, xyz in aligned if c == "G"]).min()
            atom_map = {(c, r, n): xyz for c, r, n, xyz in aligned}
            bond = np.linalg.norm(atom_map["T", 187, "ND2"] - atom_map["G", 1, "C1"])
            fixed = min(cdist(fab, xyz).min() for xyz in cores)
            relative = np.asarray(fab) - origin
            membrane = (relative[:, 2] * np.cos(tilt) -
                        np.linalg.norm(relative[:, :2], axis=1) * np.sin(tilt)).min() - top
            conf = json.loads(next(path.parent.glob("*_summary_confidences.json")).read_text())
            pair = conf["chain_pair_iptm"]
            chain_order = list(dict.fromkeys(conf["chain_ids"]))
            h, l, t = (chain_order.index(c) for c in "HLT")
            orig_angle, screen_angle = angle(direction, original), angle(direction, screened)
            passed = (required <= contacts and screen_angle < orig_angle and membrane > 0
                      and min(protein, glycan, fixed) >= 2 and 1.2 <= bond <= 1.7
                      and not conf["has_clash"])
            writer.writerow((task, path.parent.name, conf["iptm"], pair[h][t], pair[l][t],
                             int(conf["has_clash"]), f"{fit_rmsd:.3f}", qc.residue_list(contacts),
                             required <= contacts,
                             *(f"{n:.3f}" for n in (orig_angle, screen_angle, protein,
                                                   glycan, bond, fixed, membrane)), passed))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
