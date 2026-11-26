"""Estimate Arm A Fab clearance using rigid 20G5 constant-domain placements."""
import csv
from importlib import import_module
from pathlib import Path
import sys

import numpy as np
from scipy.spatial.distance import cdist

qc = import_module("04_12_expanded_context_qc")
format_a = import_module("04_12_arm_a_format")

# Heavy/light chain IDs and final variable residue numbers in each 20G5 copy.
TEMPLATES = (
    ("9LY5", "A", "B", 118, 106),
    ("9LY6", "B", "C", 118, 106),
)


def place_constants(blocks, chains, fv_ca):
    for entry, heavy, light, vh_end, vl_end in TEMPLATES:
        template = Path(f"data/raw/structures/{entry}.pdb")
        ends = {heavy: vh_end, light: vl_end}
        template_atoms = list(qc.atoms(template, ends))
        template_ca = {(chain, res): xyz for chain, res, name, xyz in template_atoms
                       if name == "CA"}
        constant = np.array([xyz for chain, res, _, xyz in template_atoms
                             if res > ends[chain]])
        for n in (8, 10):
            ref, dest = [], []
            for chain, source in (("H", heavy), ("L", light)):
                assert len(blocks[chain][-1]) >= n
                for delta, (res, _) in enumerate(reversed(chains[chain][-n:])):
                    ref.append(template_ca[source, ends[source] - delta])
                    dest.append(fv_ca[chain, res])
            ref, dest = np.array(ref), np.array(dest)
            rotation, offset = qc.fit(ref, dest)
            rmsd = np.sqrt(np.mean(np.sum((ref @ rotation + offset - dest)**2, axis=1)))
            extended = constant @ rotation + offset
            yield f"{entry}:{heavy}{light}", n, rmsd, extended


def main():
    full = list(qc.atoms(qc.FULL, "A"))
    ecto = [row for row in full if 29 <= row[1] <= 466]
    ecto_xyz = [row[3] for row in ecto]
    lookup = {(res, name): xyz for _, res, name, xyz in full}
    tm = np.array([lookup[res, "CA"] for res in range(467, 488)])
    origin = tm.mean(axis=0)
    top = tm[:, 2].max() - origin[2]
    sites = {res: lookup[res, "ND2"] for res in qc.GLYCOSITES}
    job = qc.ARMS["A"][0]
    run = qc.SCRATCH / "04_12_context_pilot/A" / job
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("pose", "template", "terminal_ca_per_chain", "fit_rmsd_A",
                     "fv_clashes", "closest_fv_atom", "closest_target_atom",
                     "closest_fv_target_A", "constant_clashes", "constant_target_min_A",
                     "closest_glycosite", "fab_nd2_min_A", "fv_min_z_A", "fab_min_z_A",
                     "fab_clearance_A", "fab_clearance_10deg_A"))
    for model in (0, 1):
        binder, placed = qc.place_pilot_model("A", model, lookup)
        blocks, _, _, chains = format_a.domain_blocks(run / f"ab_{model}.pdb")
        fv_ca = {(chain, res): xyz for (chain, res, name, _), xyz in zip(binder, placed)
                 if name == "CA"}
        distances = cdist(placed, ecto_xyz)
        i, j = np.unravel_index(distances.argmin(), distances.shape)
        for template, n, rmsd, extended in place_constants(blocks, chains, fv_ca):
            fab = np.vstack((placed, extended))
            const_dist = cdist(extended, ecto_xyz)
            glycan = cdist(fab, list(sites.values())).min(axis=0)
            relative = fab - origin
            tilt = np.radians(10)
            tilted_z = relative[:, 2] * np.cos(tilt) - np.linalg.norm(
                relative[:, :2], axis=1) * np.sin(tilt)
            writer.writerow((f"A{model}", template, n, f"{rmsd:.3f}",
                             int((distances < 2).sum()), qc.atom_id(binder[i]),
                             qc.atom_id(ecto[j]), f"{distances[i, j]:.3f}",
                             int((const_dist < 2).sum()), f"{const_dist.min():.3f}",
                             list(sites)[glycan.argmin()], f"{glycan.min():.3f}",
                             f"{placed[:, 2].min():.3f}", f"{fab[:, 2].min():.3f}",
                             f"{relative[:, 2].min() - top:.3f}",
                             f"{tilted_z.min() - top:.3f}"))


if __name__ == "__main__":
    main()
