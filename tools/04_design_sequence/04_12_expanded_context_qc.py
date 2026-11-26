"""Compare expanded and historical RFantibody poses on canonical 4Ig B7-H3."""
import csv
import os
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist

sys.path.insert(0, "tools/07_fab_categories")
from prepare_fab_category_input import pdb_sequences

SCRATCH = Path(os.environ["MAB_SCRATCH_ROOT"])
FULL = Path("data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb")
ARMS = {
    "A": ("27635726", (29, 169), {126, 127, 128, 129}),
    "B": ("27635727", (141, 281), {228, 229, 232, 234, 236, 238, 240, 241}),
}
GLYCOSITES = (104, 189, 215, 322, 407, 433)


def atoms(path, chains):
    for line in path.read_text().splitlines():
        if (line.startswith("ATOM  ") and line[21] in chains
                and line[76:78].strip() not in {"H", "D"}):
            yield (line[21], int(line[22:26]), line[12:16].strip(),
                   [float(line[i:i + 8]) for i in (30, 38, 46)])


def residue_list(residues):
    return ",".join(map(str, sorted(set(residues)))) or "-"


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
                u, _, vt = np.linalg.svd((target - target.mean(0)).T
                                        @ (destination - destination.mean(0)))
                rotation = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
                offset = destination.mean(0) - target.mean(0) @ rotation
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
    main()
