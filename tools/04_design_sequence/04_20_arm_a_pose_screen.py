"""Screen rigid seed-301 placements around the Arm A epitope."""
import csv
from importlib import import_module
from itertools import product
from pathlib import Path
import sys

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from scipy.spatial.transform import Rotation

fab = import_module("04_17_arm_a_fab_clearance")
qc = fab.qc
stage = Path("results/04_18_arm_a_backbone_pilot")


def load_pose(seed, job, lookup):
    run = qc.SCRATCH / "04_18_arm_a_backbone_pilot/A" / str(job)
    path = stage / f"04_18_seed_{seed}.pdb"
    crop = qc.pdb_sequences(run / "target.pdb", {"T"})["T"]
    full_sequence = dict(qc.pdb_sequences(qc.FULL, {"A"})["A"])
    assert all(full_sequence[r] == aa for r, aa in crop)
    assert [aa for _, aa in qc.pdb_sequences(path, {"T"})["T"]] == [aa for _, aa in crop]
    target_ca = np.array([xyz for _, _, name, xyz in qc.atoms(path, "T") if name == "CA"])
    rotation, offset = qc.fit(target_ca, np.array([lookup[r, "CA"] for r, _ in crop]))
    binder = list(qc.atoms(path, "HL"))
    placed = np.array([row[3] for row in binder]) @ rotation + offset
    blocks, _, _, chains = fab.format_a.domain_blocks(path)
    ca = {(chain, res): xyz for (chain, res, name, _), xyz in zip(binder, placed) if name == "CA"}
    return placed, np.vstack([xyz for _, _, _, xyz in fab.place_constants(blocks, chains, ca)])


def main():
    full = list(qc.atoms(qc.FULL, "A"))
    lookup = {(r, name): xyz for _, r, name, xyz in full}
    residues = sorted(qc.ARMS["A"][2])
    anchors = [np.array([xyz for _, res, _, xyz in full if res == r]) for r in residues]
    pivot = np.mean([lookup[r, "CA"] for r in residues], axis=0)
    protein = cKDTree([xyz for _, r, _, xyz in full if 29 <= r <= 466])
    sites = np.array([lookup[r, "ND2"] for r in qc.GLYCOSITES])
    tm = np.array([lookup[r, "CA"] for r in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    tilt = np.radians(10)
    names = ("CG", "OD1", "ND2")
    experiment = Path("data/raw/structures/9LME.pdb")
    glycans = []
    for chain, sugar in (("A", "H"), ("B", "E")):
        asn = {n: x for _, r, n, x in qc.atoms(experiment, chain) if r == 104}
        nag = [xyz for _, r, _, xyz in qc.atoms(experiment, sugar, "HETATM") if r == 1]
        assert len(nag) == 14
        rot, shift = qc.fit(np.array([asn[n] for n in names]),
                            np.array([lookup[104, n] for n in names]))
        glycans.extend(np.array(nag) @ rot + shift)
    glycans = cKDTree(glycans)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("seed", "rx_deg", "ry_deg", "rz_deg", "tx_A", "ty_A", "tz_A",
                     "anchors_le4p5", "protein_min_A", "N104_NAG_min_A",
                     "nearest_ND2_A", "nominal_clearance_A", "tilted_clearance_A", "pass"))
    for seed, job in ((201, 27715195), (301, 27715196)):
        fv, constants = load_pose(seed, job, lookup)
        complete = np.vstack((fv, constants))
        angles = [(0, 0, 0)] if seed == 201 else product(range(-30, 31, 10), repeat=3)
        shifts = [(0, 0, 0)] if seed == 201 else list(product((-2, 0, 2), repeat=3))
        for euler in angles:
            rotated = Rotation.from_euler("xyz", euler, degrees=True).apply(complete - pivot) + pivot
            for shift in shifts:
                pose = rotated + shift
                contacts = [r for r, anchor in zip(residues, anchors)
                            if cdist(pose[:len(fv)], anchor).min() <= 4.5]
                protein_min = protein.query(pose)[0].min()
                sugar_min = glycans.query(pose)[0].min()
                nd2_min = cdist(pose, sites).min()
                relative = pose - origin
                nominal = relative[:, 2].min() - top
                tilted = (relative[:, 2] * np.cos(tilt) -
                          np.linalg.norm(relative[:, :2], axis=1) * np.sin(tilt)).min() - top
                passes = (contacts == residues and min(protein_min, sugar_min, nd2_min) >= 2
                          and min(nominal, tilted) > 0)
                writer.writerow((seed, *euler, *shift, qc.residue_list(contacts),
                                 *(f"{x:.4f}" for x in (protein_min, sugar_min, nd2_min,
                                                        nominal, tilted)), passes))


if __name__ == "__main__":
    main()
