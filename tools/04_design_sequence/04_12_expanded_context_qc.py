"""Compare expanded and historical RFantibody poses on canonical 4Ig B7-H3."""
import csv
import os
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial.transform import Rotation

sys.path.insert(0, "tools/07_fab_categories")
from prepare_fab_category_input import pdb_sequences

SCRATCH = Path(os.environ["MAB_SCRATCH_ROOT"])
FULL = Path("data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb")
ARMS = {
    "A": ("27635726", (29, 169), {126, 127, 128, 129}),
    "B": ("27635727", (141, 281), {228, 229, 232, 234, 236, 238, 240, 241}),
}
GLYCOSITES = (104, 189, 215, 322, 407, 433)


def atoms(path, chains, record="ATOM  "):
    for line in path.read_text().splitlines():
        if (line.startswith(record) and line[21] in chains
                and line[76:78].strip() not in {"H", "D"}):
            yield (line[21], int(line[22:26]), line[12:16].strip(),
                   [float(line[i:i + 8]) for i in (30, 38, 46)])


def residue_list(residues):
    return ",".join(map(str, sorted(set(residues)))) or "-"


def fit(source, destination):
    u, _, vt = np.linalg.svd((source - source.mean(0)).T
                            @ (destination - destination.mean(0)))
    rotation = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
    return rotation, destination.mean(0) - source.mean(0) @ rotation


def place_pilot_model(arm, model, lookup):
    job, _, _ = ARMS[arm]
    run = SCRATCH / "04_12_context_pilot" / arm / job
    crop = pdb_sequences(run / "target.pdb", {"T"})["T"]
    path = run / f"ab_{model}.pdb"
    assert [aa for _, aa in pdb_sequences(path, {"T"})["T"]] == [aa for _, aa in crop]
    source = np.array([xyz for _, _, name, xyz in atoms(path, "T") if name == "CA"])
    rotation, offset = fit(source, np.array([lookup[res, "CA"] for res, _ in crop]))
    binder = list(atoms(path, "HL"))
    return binder, np.array([xyz for _, _, _, xyz in binder]) @ rotation + offset


def ser125_scan():
    full = [row for row in atoms(FULL, "A") if 29 <= row[1] <= 466]
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    assert dict(pdb_sequences(FULL, {"A"})["A"])[125] == "S"
    _, placed = place_pilot_model("A", 0, lookup)

    site = {(res, name): np.array(xyz) for (res, name), xyz in lookup.items() if res == 125}
    n, ca, cb, og = (site[125, name] for name in ("N", "CA", "CB", "OG"))
    axis = (cb - ca) / np.linalg.norm(cb - ca)
    n_plane = n - ca - np.dot(n - ca, axis) * axis
    og_plane = og - cb - np.dot(og - cb, axis) * axis
    chi1 = np.degrees(np.arctan2(np.dot(np.cross(axis, n_plane), og_plane),
                                  np.dot(n_plane, og_plane)))

    fixed = [row for row in full if row[1:3] != (125, "OG")]
    distances = cdist(placed, [xyz for _, _, _, xyz in fixed])
    fixed_clashes = int((distances < 2).sum())
    assert fixed_clashes == 0
    contacts = {row[1] for row, hit in zip(fixed, (distances <= 4.5).any(axis=0)) if hit}
    anchors = contacts & ARMS["A"][2]
    assert anchors == ARMS["A"][2]
    # Exclude directly bonded and angle-linked atoms CB and CA.
    target = [xyz for _, res, name, xyz in fixed if res != 125 or name not in {"CA", "CB"}]

    table = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    table.writerow(("pose", "chi1_deg", "rotation_deg", "og_min_to_fv_A",
                    "og_min_to_target_A", "fv_protein_pairs_lt2",
                    "og_target_pairs_lt2", "anchor_contacts_le4p5"))
    for pose, angle in [("original", chi1), *(("scan", angle) for angle in range(-180, 180, 5))]:
        delta = (angle - chi1 + 180) % 360 - 180
        moved = cb + Rotation.from_rotvec(axis * np.radians(delta)).apply(og - cb)
        to_fv = cdist([moved], placed)
        to_target = cdist([moved], target)
        table.writerow((pose, f"{angle:.2f}", f"{delta:.2f}", f"{to_fv.min():.3f}",
                        f"{to_target.min():.3f}", fixed_clashes + int((to_fv < 2).sum()),
                        int((to_target < 2).sum()), residue_list(anchors)))


def followup(b_models=(2,), include_a0=True):
    experiment = Path("data/raw/structures/9LME.pdb")
    full = [row for row in atoms(FULL, "A") if 29 <= row[1] <= 466]
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    table = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    table.writerow(("check", "target_conformer", "template", "fv_atom", "target_atom",
                    "distance_A", "fv_pairs_lt2", "other_target_pairs_lt2"))
    if include_a0:
        binder, placed = place_pilot_model("A", 0, lookup)
        distances = cdist(placed, [xyz for _, _, _, xyz in full])
        for i, j in zip(*np.where(distances < 2)):
            table.writerow(("A0_protein", "AFDB_v6", "-", atom_id(binder[i]),
                            atom_id(full[j]), f"{distances[i, j]:.3f}", 1, "-"))
    b_poses = {model: place_pilot_model("B", model, lookup) for model in b_models}

    observed = list(atoms(experiment, "A"))
    experimental_map = {(res, name): xyz for _, res, name, xyz in observed}
    with Path("metadata/numbering_map.csv").open() as handle:
        mapped = {int(r["canonical_residue"]): int(r["model_residue"])
                  for r in csv.DictReader(handle) if r["source"] == "9LME"
                  and r["chain"] == "A" and r["canonical_residue"].isdigit()}
    assert all(mapped[res] == res for res in range(210, 221))
    window = [(res, "CA") for res in range(210, 221)]
    rotation, offset = fit(np.array([experimental_map[key] for key in window]),
                           np.array([lookup[key] for key in window]))
    observed_aligned = {(res, name): np.array(xyz) @ rotation + offset
                        for (res, name), xyz in experimental_map.items()}
    side_names = ("CG", "OD1", "ND2")
    for label, target in (("AFDB_v6", lookup), ("9LME_local_210_220", observed_aligned)):
        site = np.array([target[215, name] for name in side_names])
        other = [xyz for (res, _), xyz in target.items() if res != 215 and 29 <= res <= 466]
        glycan_poses = []
        for chain, res, nag_chain in (("A", 104, "H"), ("A", 189, "D"),
                                      ("B", 104, "E"), ("B", 189, "G")):
            template_asn = {name: xyz for _, n, name, xyz in atoms(experiment, chain)
                            if n == res}
            nag = [row for row in atoms(experiment, nag_chain, "HETATM") if row[1] == 1]
            assert len(nag) == 14, (nag_chain, nag)
            rotation, offset = fit(np.array([template_asn[name] for name in side_names]), site)
            glycan = np.array([xyz for _, _, _, xyz in nag]) @ rotation + offset
            glycan_poses.append((f"9LME_{chain}{res}_{nag_chain}1", nag, glycan,
                                 int((cdist(glycan, other) < 2).sum())))

        for model, (binder, placed) in b_poses.items():
            nd2 = cdist(placed, site[2:3])[:, 0]
            table.writerow((f"B{model}_N215", label, "-", atom_id(binder[nd2.argmin()]),
                            "A:215:ND2", f"{nd2.min():.3f}", int((nd2 < 2).sum()), "-"))
            for template, nag, glycan, target_clashes in glycan_poses:
                distances = cdist(placed, glycan)
                i, j = np.unravel_index(distances.argmin(), distances.shape)
                table.writerow((f"B{model}_N215_first_NAG", label, template,
                                atom_id(binder[i]), f"NAG:{nag[j][2]}",
                                f"{distances[i, j]:.3f}", int((distances < 2).sum()),
                                target_clashes))


def atom_id(atom):
    return ":".join(map(str, atom[:3]))


def main():
    full = list(atoms(FULL, "A"))
    full_seq = dict(pdb_sequences(FULL, {"A"})["A"])
    full_ca = {res: xyz for _, res, name, xyz in full if name == "CA"}
    ecto = [(res, xyz) for _, res, _, xyz in full if 29 <= res <= 466]
    residues = np.array([res for res, _ in ecto])
    glycan_sites = {res: xyz for _, res, name, xyz in full
                    if res in GLYCOSITES and name == "ND2"}
    assert set(glycan_sites) == set(GLYCOSITES)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("arm", "cohort", "model", "crop", "fit_rmsd_A", "antigen_pairs_lt2",
                     "outside_crop_pairs_lt2", "outside_crop_clash_residues",
                     "contact_residues_le4p5", "anchor_contacts_le4p5",
                     "nearest_glycosite", "glycosite_ND2_min_A", "fv_min_z_A",
                     "vh_length", "vl_length", "max_adjacent_ca_A"))

    for arm, (job, expanded_bounds, anchors) in ARMS.items():
        expanded = SCRATCH / "04_12_context_pilot" / arm / job
        historical = SCRATCH / "rfantibody_b7h3_backbone_pilot_20260925" / arm
        historical_crop = SCRATCH / "rfantibody_inputs_corrected3" / f"target_{arm}.pdb"
        for cohort, crop_path, paths in (
            ("expanded", expanded / "target.pdb", sorted(expanded.glob("ab_*.pdb"))),
            ("historical", historical_crop, [historical / f"task_{i}/ab_0.pdb" for i in range(4)]),
        ):
            assert len(paths) == 4, paths
            crop = pdb_sequences(crop_path, {"T"})["T"]
            assert all(full_seq[res] == aa for res, aa in crop), crop_path
            start, end = crop[0][0], crop[-1][0]
            if cohort == "expanded":
                assert (start, end) == expanded_bounds
            outside = ~np.isin(residues, [res for res, _ in crop])
            destination = np.array([full_ca[res] for res, _ in crop])

            for index, path in enumerate(paths):
                design = list(atoms(path, "THL"))
                target = np.array([xyz for chain, _, name, xyz in design
                                   if chain == "T" and name == "CA"])
                target_seq = pdb_sequences(path, {"T"})["T"]
                assert [aa for _, aa in target_seq] == [aa for _, aa in crop], path
                assert len(target) == len(crop), path
                rotation, offset = fit(target, destination)
                rmsd = np.sqrt(np.mean(np.sum((target @ rotation + offset - destination)**2,
                                              axis=1)))
                binder = np.array([xyz for chain, _, _, xyz in design if chain in {"H", "L"}])
                placed = binder @ rotation + offset
                distances = cdist(placed, [xyz for _, xyz in ecto])
                clashes = distances < 2
                contacts = set(residues[(distances <= 4.5).any(axis=0)])
                sites = cdist(placed, list(glycan_sites.values())).min(axis=0)
                chains = [np.array([xyz for c, _, name, xyz in design if c == chain and name == "CA"])
                          for chain in ("H", "L")]
                max_ca = max(np.linalg.norm(np.diff(chain, axis=0), axis=1).max()
                             for chain in chains)
                writer.writerow((arm, cohort, index, f"{start}-{end}", f"{rmsd:.3f}",
                                 clashes.sum(), clashes[:, outside].sum(),
                                 residue_list(residues[outside & clashes.any(axis=0)]),
                                 residue_list(contacts), residue_list(contacts & anchors),
                                 list(glycan_sites)[sites.argmin()], f"{sites.min():.2f}",
                                 f"{placed[:, 2].min():.2f}", *map(len, chains), f"{max_ca:.2f}"))


if __name__ == "__main__":
    if sys.argv[1:] == ["followup"]:
        followup()
    elif sys.argv[1:] == ["b-alternates"]:
        followup((0, 1), include_a0=False)
    elif sys.argv[1:] == ["ser125"]:
        ser125_scan()
    else:
        main()
