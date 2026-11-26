"""Compare seeded Arm A backbones with A0 on intact 4Ig."""
import csv
from importlib import import_module
from itertools import combinations
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist

fab = import_module("04_17_arm_a_fab_clearance")
qc = fab.qc
format_a = fab.format_a


def main(args):
    full = list(qc.atoms(qc.FULL, "A"))
    ecto = [row for row in full if 29 <= row[1] <= 466]
    ecto_xyz = [row[3] for row in ecto]
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    tm = np.array([lookup[res, "CA"] for res in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    tilt = np.radians(10)
    sites = {res: lookup[res, "ND2"] for res in qc.GLYCOSITES}
    _, (lo, hi), anchors = qc.ARMS["A"]
    patch = np.mean([lookup[r, "CA"] for r in sorted(anchors)], axis=0)
    scaffold = qc.SCRATCH / "rfantibody_inputs_corrected3/framework_HLT.pdb"
    reference, *_ = format_a.domain_blocks(scaffold)
    baseline = qc.SCRATCH / "04_12_context_pilot/A" / qc.ARMS["A"][0]

    # Use the resolved first sugar at N104 in each 9LME copy as a local probe.
    experimental = Path("data/raw/structures/9LME.pdb")
    n104_poses = []
    names = ("CG", "OD1", "ND2")
    for chain, nag_chain in (("A", "H"), ("B", "E")):
        asn = {name: xyz for _, res, name, xyz in qc.atoms(experimental, chain)
               if res == 104}
        nag = [xyz for _, res, _, xyz in qc.atoms(experimental, nag_chain, "HETATM")
               if res == 1]
        assert len(nag) == 14
        rotation, offset = qc.fit(np.array([asn[name] for name in names]),
                                  np.array([lookup[104, name] for name in names]))
        n104_poses.append(np.array(nag) @ rotation + offset)
    entries = [("A0", 0, baseline, None)]
    for spec in args:
        seed, job, *pose = spec.split(":")
        if pose:
            run_stage = "04_22_arm_a_conditioned"
            crop = Path("results") / run_stage / f"04_22_pose_{pose[0]}.pdb"
        else:
            run_stage = "04_18_arm_a_backbone_pilot"
            crop = None
        entries.append((seed, int(seed), qc.SCRATCH / run_stage / "A" / job, crop))

    conditioned = any(crop is not None for _, _, _, crop in entries)
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("pose", "H3_L1_L3", "VH_VL", "fixed_blocks_match",
                     "max_adjacent_CA_A", "anchors_le4p5", "fv_pairs_lt2",
                     "outside_crop_pairs_lt2", "closest_fv_pair", "closest_fv_A",
                     "max_constant_pairs_lt2", "nearest_site", "min_fab_ND2_A",
                     "min_fab_N104_NAG_A", "min_fv_z_A",
                     "worst_fab_clearance_A", "best_fab_clearance_A",
                     "worst_fab_clearance_10deg_A", "angle_from_A0_deg",
                     *(("framework_to_input_CA_rmsd_A", "loops_to_input_CA_rmsd_A")
                       if conditioned else ())))
    directions = {}
    conditioned_loops = {}
    for label, seed, run, crop in entries:
        blocks, lengths, ranges, chains = format_a.domain_blocks(run / f"ab_{seed}.pdb")
        binder, placed = qc.place_pilot_model("A", seed, lookup, run, crop)
        fv_ca = {(chain, res): xyz for (chain, res, name, _), xyz in zip(binder, placed)
                 if name == "CA"}
        realized = ("-", "-") if conditioned else ()
        if crop is not None:
            _, initial_lengths, initial_ranges, initial_chains = format_a.domain_blocks(crop)
            assert (lengths, ranges) == (initial_lengths, initial_ranges)
            assert all([r for r, _ in chains[c]] == [r for r, _ in initial_chains[c]]
                       for c in "HL")
            initial_ca = {(c, r): xyz for c, r, name, xyz in qc.atoms(crop, "HL")
                          if name == "CA"}
            loop_keys = {(loop[0], chains[loop[0]][i - 1][0])
                         for loop, positions in ranges.items() for i in positions}
            fixed = [key for key in fv_ca if key not in loop_keys]
            loops = sorted(loop_keys)
            realized = tuple(f"{rmsd([fv_ca[k] for k in group], [initial_ca[k] for k in group]):.3f}"
                             for group in (fixed, loops))
            conditioned_loops[label] = (crop, [fv_ca[k] for k in loops])
        terminal_ca = [fv_ca[chain, res] for chain in "HL" for res, _ in chains[chain][-8:]]
        direction = np.mean(terminal_ca, axis=0) - patch
        directions[label] = direction / np.linalg.norm(direction)
        max_step = max(np.linalg.norm(np.diff([fv_ca[c, r] for r, _ in chains[c]], axis=0),
                                      axis=1).max() for c in "HL")
        distances = cdist(placed, ecto_xyz)
        i, j = np.unravel_index(distances.argmin(), distances.shape)
        clashes = distances < 2
        outside = [not lo <= row[1] <= hi for row in ecto]
        contacts = {row[1] for row, hit in zip(ecto, (distances <= 4.5).any(axis=0)) if hit}
        constant_pairs, site_distances, nag_distances, clearance, tilted = [], [], [], [], []
        for _, _, _, extended in fab.place_constants(blocks, chains, fv_ca):
            complete = np.vstack((placed, extended))
            constant_pairs.append(int((cdist(extended, ecto_xyz) < 2).sum()))
            site_distances.append(cdist(complete, list(sites.values())).min(axis=0))
            nag_distances.append(min(cdist(complete, nag).min() for nag in n104_poses))
            relative = complete - origin
            clearance.append(relative[:, 2].min() - top)
            tilted.append((relative[:, 2] * np.cos(tilt) -
                           np.linalg.norm(relative[:, :2], axis=1) * np.sin(tilt)).min() - top)
        site_min = np.min(site_distances, axis=0)
        writer.writerow((label, "/".join(str(lengths[k]) for k in ("H3", "L1", "L3")),
                         "/".join(str(len(chains[c])) for c in "HL"), blocks == reference,
                         f"{max_step:.3f}", qc.residue_list(contacts & anchors),
                         int(clashes.sum()), int(clashes[:, outside].sum()),
                         f"{qc.atom_id(binder[i])}/{qc.atom_id(ecto[j])}",
                         f"{distances[i, j]:.3f}", max(constant_pairs),
                         list(sites)[site_min.argmin()], f"{site_min.min():.3f}",
                         f"{min(nag_distances):.3f}", f"{placed[:, 2].min():.3f}",
                         f"{min(clearance):.3f}", f"{max(clearance):.3f}",
                         f"{min(tilted):.3f}", f"{angle(directions[label], directions['A0']):.1f}", *realized))
    for first, second in combinations(directions, 2):
        print(first, second, f"{angle(directions[first], directions[second]):.1f}", sep="\t",
              file=sys.stderr)
    for first, second in combinations(conditioned_loops, 2):
        if conditioned_loops[first][0] == conditioned_loops[second][0]:
            print("within_pose_loop_CA_rmsd", first, second,
                  f"{rmsd(conditioned_loops[first][1], conditioned_loops[second][1]):.3f}",
                  sep="\t", file=sys.stderr)


def rmsd(first, second):
    return np.sqrt(np.mean(np.sum((np.array(first) - second) ** 2, axis=1)))


def angle(first, second):
    return np.degrees(np.arccos(np.clip(first @ second, -1, 1)))


if __name__ == "__main__":
    main(sys.argv[1:])
