"""Evaluate historical Arm B Fabs and transferred 9LME glycan cores."""
import csv
from importlib import import_module
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist

fab = import_module("04_17_arm_a_fab_clearance")
qc = fab.qc


def n215_probes(lookup):
    experiment = Path("data/raw/structures/9LME.pdb")
    observed = {(res, name): xyz for _, res, name, xyz in qc.atoms(experiment, "A")}
    with Path("metadata/numbering_map.csv").open() as handle:
        mapping = {int(row["canonical_residue"]): int(row["model_residue"])
                   for row in csv.DictReader(handle) if row["source"] == "9LME"
                   and row["chain"] == "A" and row["canonical_residue"].isdigit()}
    window = [(res, "CA") for res in range(210, 221)]
    assert all(mapping[res] == res for res, _ in window)
    rotation, offset = qc.fit(np.array([observed[key] for key in window]),
                              np.array([lookup[key] for key in window]))
    aligned = {key: np.array(xyz) @ rotation + offset for key, xyz in observed.items()}
    names = ("CG", "OD1", "ND2")
    for label, target in (("AFDB_v6", lookup), ("9LME_local_210_220", aligned)):
        destination = np.array([target[215, name] for name in names])
        nearby = [xyz for (res, _), xyz in target.items() if 29 <= res <= 466 and res != 215]
        for chain, res, glycan_chain in (("A", 104, "H"), ("A", 189, "D"),
                                         ("B", 104, "E"), ("B", 189, "G")):
            source = {name: xyz for _, number, name, xyz in qc.atoms(experiment, chain)
                      if number == res}
            glycan = list(qc.atoms(experiment, glycan_chain, "HETATM"))
            residues = np.array([row[1] for row in glycan])
            sugar_count = len(set(residues))
            assert sugar_count in (3, 4)
            rotation, offset = qc.fit(np.array([source[name] for name in names]), destination)
            xyz = np.array([row[3] for row in glycan]) @ rotation + offset
            target_pairs = int((cdist(xyz, nearby) < 2).sum())
            yield label, f"9LME_{chain}{res}_{glycan_chain}", sugar_count, residues, xyz, target_pairs


def main(glycan_output):
    full = list(qc.atoms(qc.FULL, "A"))
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    ecto = [row for row in full if 29 <= row[1] <= 466]
    ecto_xyz = [row[3] for row in ecto]
    tm = np.array([lookup[res, "CA"] for res in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    tilt = np.radians(10)
    probes = list(n215_probes(lookup))
    archive = qc.SCRATCH / "rfantibody_b7h3_backbone_pilot_20260925/B"
    crop = qc.SCRATCH / "rfantibody_inputs_corrected3/target_B.pdb"
    geometry = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    glycans = csv.writer(glycan_output, delimiter="\t", lineterminator="\n")
    geometry.writerow(("task", "fab_template", "terminal_ca_per_chain", "fit_rmsd_A",
                       "anchor_contacts_le4p5", "fv_target_pairs_lt2", "constant_target_pairs_lt2",
                       "constant_target_min_A", "nearest_target_atom", "membrane_clearance_A",
                       "membrane_clearance_10deg_A"))
    glycans.writerow(("task", "fab_template", "terminal_ca_per_chain", "n215_conformer",
                      "glycan_template", "sugars", "core_target_pairs_lt2",
                      "first_sugar_fab_min_A", "core_fab_min_A", "core_fab_pairs_lt2",
                      "clashing_sugar_residues", "clashing_fv_residues"))
    for task in (31, 152):
        run = archive / f"task_{task}"
        binder, placed = qc.place_pilot_model("B", 0, lookup, run, crop)
        blocks, _, _, chains = fab.format_a.domain_blocks(run / "ab_0.pdb")
        fv_ca = {(chain, res): xyz for (chain, res, name, _), xyz in zip(binder, placed)
                 if name == "CA"}
        protein = cdist(placed, ecto_xyz)
        contacts = {row[1] for row, hit in zip(ecto, (protein <= 4.5).any(axis=0)) if hit}
        anchors = qc.residue_list(contacts & qc.ARMS["B"][2])
        for template, n, rmsd, extended in fab.place_constants(blocks, chains, fv_ca):
            complete = np.vstack((placed, extended))
            constants = cdist(extended, ecto_xyz)
            _, nearest = np.unravel_index(constants.argmin(), constants.shape)
            relative = complete - origin
            tilted_z = relative[:, 2] * np.cos(tilt) - np.linalg.norm(
                relative[:, :2], axis=1) * np.sin(tilt)
            geometry.writerow((task, template, n, f"{rmsd:.3f}", anchors,
                               int((protein < 2).sum()), int((constants < 2).sum()),
                               f"{constants.min():.3f}", qc.atom_id(ecto[nearest]),
                               f"{relative[:, 2].min() - top:.3f}", f"{tilted_z.min() - top:.3f}"))
            for conformer, source, sugars, residues, core, target_pairs in probes:
                distances = cdist(complete, core)
                clashes = distances < 2
                fv_hits = {f"{atom[0]}:{atom[1]}" for atom, hit in
                           zip(binder, clashes.any(axis=1)) if hit}
                glycans.writerow((task, template, n, conformer, source, sugars, target_pairs,
                                  f"{distances[:, residues == 1].min():.3f}",
                                  f"{distances.min():.3f}", int(clashes.sum()),
                                  qc.residue_list(residues[clashes.any(axis=0)]),
                                  ",".join(sorted(fv_hits)) or "-"))


if __name__ == "__main__":
    with Path(sys.argv[1]).open("w") as glycan_output:
        main(glycan_output)
