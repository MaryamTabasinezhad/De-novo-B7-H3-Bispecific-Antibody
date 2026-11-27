"""Compare independent Arm A Fab predictions with their designed poses."""
import csv
from importlib import import_module
import json
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist

bound = import_module("04_23_arm_b_bound_pose_qc")
qc = bound.qc
stage = Path("results/04_26_arm_a_sequence_pilot")
run = qc.SCRATCH / stage.name
parent_stage = Path("results/04_22_arm_a_conditioned")
lookup = {(r, n): x for _, r, n, x in qc.atoms(qc.FULL, "A")}
anchors = sorted(qc.ARMS["A"][2])
pivot = np.mean([lookup[r, "CA"] for r in anchors], axis=0)
tm = np.array([lookup[r, "CA"] for r in range(467, 488)])
origin = tm.mean(axis=0)
top = tm[:, 2].max() - origin[2]
tilt = np.radians(10)
sites = [lookup[r, "ND2"] for r in qc.GLYCOSITES]
glycan = []
for chain, sugar in (("A", "H"), ("B", "E")):
    experiment = Path("data/raw/structures/9LME.pdb")
    asn = {n: x for _, r, n, x in qc.atoms(experiment, chain) if r == 104}
    names = ("CG", "OD1", "ND2")
    rot, shift = qc.fit(np.array([asn[n] for n in names]),
                        np.array([lookup[104, n] for n in names]))
    nag = [x for _, r, _, x in qc.atoms(experiment, sugar, "HETATM") if r == 1]
    assert len(nag) == 14
    glycan.extend(np.array(nag) @ rot + shift)

writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
writer.writerow(("backbone", "sample", "ht_iptm", "lt_iptm", "af3_clash",
                 "crop_fit_rmsd_A", "anchors_le4p5", "angle_to_backbone_deg", "protein_min_A",
                 "nearest_glycosite_ND2_A", "N104_first_NAG_min_A", "nominal_clearance_A",
                 "tilted_clearance_A"))
for seed, origin_job, pose, af3_job in [(412, "27718318", 1, sys.argv[1]),
                                       (421, "27722542", 2, sys.argv[2])]:
    parent = qc.SCRATCH / "04_22_arm_a_conditioned/A" / origin_job
    binder, placed = qc.place_pilot_model("A", seed, lookup, parent,
                                         parent_stage / f"04_22_pose_{pose}.pdb")
    original = np.mean([p for chain in "HL" for p in
                        [x for (c, _, n, _), x in zip(binder, placed)
                         if c == chain and n == "CA"][-8:]], axis=0) - pivot
    config = json.loads((stage / f"04_26_seed_{seed}_af3.json").read_text())
    lengths = {c: len(e["protein"]["sequence"]) - constant for c, e, constant in
               zip("HL", config["sequences"], (105, 107))}
    paths = sorted((run / af3_job).glob("**/seed-*_sample-*/*_model.cif"))
    assert len(paths) == 4, (seed, paths)
    for path in paths:
        atoms = list(bound.predicted_atoms(path))
        assert {c for c, *_ in atoms} == set("HLT"), path
        target = {r + 28: x for c, r, n, x in atoms if c == "T" and n == "CA"}
        assert len(target) == 438, path
        crop = range(29, 170)
        source = np.array([target[r] for r in crop])
        dest = np.array([lookup[r, "CA"] for r in crop])
        rot, shift = qc.fit(source, dest)
        fit = np.sqrt(np.mean(np.sum((source @ rot + shift - dest) ** 2, axis=1)))
        aligned = [(c, r, n, np.array(x) @ rot + shift) for c, r, n, x in atoms]
        fab = np.array([x for c, _, _, x in aligned if c in "HL"])
        fv = [x for c, r, _, x in aligned if c in "HL" and r <= lengths[c]]
        terminal = [x for c, r, n, x in aligned if c in "HL" and n == "CA"
                    and lengths[c] - 8 < r <= lengths[c]]
        assert len(terminal) == 16, path
        direction = np.mean(terminal, axis=0) - pivot
        antigen = [(r + 28, x) for c, r, _, x in aligned if c == "T"]
        contacts = [r for r in anchors
                    if cdist(fv, [x for a, x in antigen if a == r]).min() <= 4.5]
        relative = fab - origin
        tilted = (relative[:, 2] * np.cos(tilt) -
                  np.linalg.norm(relative[:, :2], axis=1) * np.sin(tilt)).min() - top
        summary = json.loads(next(path.parent.glob("*_summary_confidences.json")).read_text())
        pairs = summary["chain_pair_iptm"]
        order = list(dict.fromkeys(summary.get("chain_ids", ["H", "L", "T"])))
        h, l, t = (order.index(c) for c in "HLT")
        writer.writerow((seed, path.parent.name, pairs[h][t], pairs[l][t], summary["has_clash"],
                         f"{fit:.3f}", qc.residue_list(contacts),
                         *(f"{v:.3f}" for v in (
                             bound.angle(direction, original),
                             cdist(fab, [x for _, x in antigen]).min(),
                             cdist(fab, sites).min(), cdist(fab, glycan).min(),
                             relative[:, 2].min() - top, tilted))))
