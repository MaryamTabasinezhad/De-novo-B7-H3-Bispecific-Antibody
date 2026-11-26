"""Screen local Arm B placements with both antigen-compatible N215 cores."""
import csv
from importlib import import_module
from itertools import product
import sys

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from scipy.spatial.transform import Rotation

core = import_module("04_19_arm_b_fab_clearance")
qc = core.qc


def main():
    full = list(qc.atoms(qc.FULL, "A"))
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    anchors = sorted(qc.ARMS["B"][2])
    anchor_xyz = {res: [xyz for _, number, _, xyz in full if number == res] for res in anchors}
    pivot = np.mean([lookup[res, "CA"] for res in anchors], axis=0)
    protein = cKDTree([xyz for _, res, _, xyz in full if 29 <= res <= 466])
    sugars = [cKDTree(xyz) for _, _, _, _, xyz, clashes in core.n215_probes(lookup) if clashes == 0]
    assert len(sugars) == 2
    tm = np.array([lookup[res, "CA"] for res in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    tilt = np.radians(10)
    archive = qc.SCRATCH / "rfantibody_b7h3_backbone_pilot_20260925/B"
    crop = qc.SCRATCH / "rfantibody_inputs_corrected3/target_B.pdb"
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("task", "rx_deg", "ry_deg", "rz_deg", "tx_A", "ty_A", "tz_A",
                     "anchors_le4p5", "protein_min_A", "core1_min_A", "core2_min_A",
                     "tilted_clearance_A"))
    print("task", "contact_pass", "protein_pass", "core_pass", sep="\t", file=sys.stderr)
    shifts = np.array(list(product((-2, 0, 2), repeat=3)))
    for task in (31, 152, 248):
        run = archive / f"task_{task}"
        binder, fv = qc.place_pilot_model("B", 0, lookup, run, crop)
        blocks, _, _, chains = core.fab.format_a.domain_blocks(run / "ab_0.pdb")
        ca = {(chain, res): xyz for (chain, res, name, _), xyz in zip(binder, fv) if name == "CA"}
        constants = [xyz for _, _, _, xyz in core.fab.place_constants(blocks, chains, ca)]
        complete = np.vstack([fv, *constants])
        original_contacts = {res for res in anchors if cdist(fv, anchor_xyz[res]).min() <= 4.5}
        # Keep atoms that could reach the contact cutoff anywhere on this grid.
        max_rotation = np.radians(90)
        max_shift = np.linalg.norm(shifts, axis=1).max()
        reach = 2 * np.linalg.norm(fv - pivot, axis=1) * np.sin(max_rotation / 2) + max_shift
        near = {res: cdist(fv, anchor_xyz[res]).min(axis=1) <= 4.5 + reach for res in anchors}
        contact_pass = protein_pass = core_pass = 0
        for euler in product(range(-30, 31, 10), repeat=3):
            rotated = Rotation.from_euler("xyz", euler, degrees=True).apply(complete - pivot) + pivot
            for shift in shifts:
                pose = rotated + shift
                contacts = {res for res in anchors
                            if cdist(pose[:len(fv)][near[res]], anchor_xyz[res]).min(initial=np.inf) <= 4.5}
                if len(contacts) < 4 or not original_contacts <= contacts:
                    continue
                contact_pass += 1
                protein_min = protein.query(pose)[0].min()
                if protein_min < 2:
                    continue
                protein_pass += 1
                sugar_min = [tree.query(pose)[0].min() for tree in sugars]
                if min(sugar_min) < 2:
                    continue
                core_pass += 1
                relative = pose - origin
                tilted = (relative[:, 2] * np.cos(tilt) -
                          np.linalg.norm(relative[:, :2], axis=1) * np.sin(tilt)).min() - top
                writer.writerow((task, *euler, *shift, qc.residue_list(contacts),
                                 *(f"{x:.4f}" for x in (protein_min, *sugar_min, tilted))))
        print(task, contact_pass, protein_pass, core_pass, sep="\t", file=sys.stderr)


if __name__ == "__main__":
    main()
