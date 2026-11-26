"""Select three distinct nominally clear placements and write HLT inputs."""
import csv
from importlib import import_module
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation

screen = import_module("04_20_arm_a_pose_screen")
qc = screen.qc
output = Path("results/04_22_arm_a_conditioned")
grid = Path("results/04_20_arm_a_pose_screen/04_20_placements.tsv")
source = screen.stage / "04_18_seed_301.pdb"
full = {(r, name): xyz for _, r, name, xyz in qc.atoms(qc.FULL, "A")}
anchors = sorted(qc.ARMS["A"][2])
pivot = np.mean([full[r, "CA"] for r in anchors], axis=0)
fv, _ = screen.load_pose(301, 27715196, full)
atoms = list(qc.atoms(source, "HL"))
ends = [i for chain in "HL" for i in [j for j, row in enumerate(atoms)
        if row[0] == chain and row[2] == "CA"][-8:]]
crop = qc.SCRATCH / "04_18_arm_a_backbone_pilot/A/27715196/target.pdb"
target = list(qc.atoms(source, "T"))
target_ca = np.array([xyz for _, _, name, xyz in target if name == "CA"])
canonical_ids = [r for r, _ in qc.pdb_sequences(crop, {"T"})["T"]]
rotation, offset = qc.fit(target_ca, np.array([full[r, "CA"] for r in canonical_ids]))
target_map = dict(zip((r for _, r, name, _ in target if name == "CA"), canonical_ids))

with grid.open() as f:
    rows = [r for r in csv.DictReader(f, delimiter="\t") if r["seed"] == "301"
            and r["anchors_le4p5"] == "126,127,128,129"
            and min(float(r[k]) for k in ("protein_min_A", "N104_NAG_min_A", "nearest_ND2_A")) >= 2
            and float(r["nominal_clearance_A"]) > 0]
assert len(rows) == 60
poses = []
for row in rows:
    euler = [float(row[f"r{axis}_deg"]) for axis in "xyz"]
    shift = [float(row[f"t{axis}_A"]) for axis in "xyz"]
    rot = Rotation.from_euler("xyz", euler, degrees=True)
    vec = rot.apply(fv[ends].mean(axis=0) - pivot) + shift
    poses.append((row, rot, shift, vec / np.linalg.norm(vec)))

selected = [max(poses, key=lambda p: float(p[0]["tilted_clearance_A"]))]
for _ in range(2):
    selected.append(min(poses, key=lambda p: max(p[3] @ other[3] for other in selected)))

with (output / "04_22_placements.tsv").open("w") as f:
    table = csv.writer(f, delimiter="\t", lineterminator="\n")
    table.writerow(("placement", "minimum_angle_from_previous_deg", *rows[0]))
    for index, (row, rot, shift, direction) in enumerate(selected, 1):
        angle = "-" if index == 1 else f"{np.degrees(np.arccos(np.clip(max(direction @ other[3] for other in selected[:index-1]), -1, 1))):.2f}"
        table.writerow((index, angle, *row.values()))
        lines = []
        for line in source.read_text().splitlines():
            if line.startswith("ATOM  "):
                xyz = np.array([float(line[i:i+8]) for i in (30, 38, 46)]) @ rotation + offset
                if line[21] in "HL":
                    xyz = rot.apply(xyz - pivot) + pivot + shift
                elif line[21] == "T":
                    line = line[:22] + f"{target_map[int(line[22:26])]:4d}" + line[26:]
                line = line[:30] + "".join(f"{value:8.3f}" for value in xyz) + line[54:]
            lines.append(line)
        (output / f"04_22_pose_{index}.pdb").write_text("\n".join(lines) + "\n")
