"""Extract verified design-loop labels and modeled 4Ig patch contacts."""
import json
from math import dist
from pathlib import Path

PATCH = {"A": (126, 127, 128, 129), "B": (228, 229, 232, 234, 236, 238, 240, 241)}
AA = dict(zip("ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
              "ARNDCQEGHILKMFPSTWYV"))


def interface(root, arm, row, chains):
    pdb = Path(row["rf2_parent"])
    residues = {}
    labels = {}
    for line in pdb.read_text().splitlines():
        if line.startswith("ATOM  ") and line[21] in "HL":
            residues[int(line[22:26])] = (line[21], AA[line[17:20]])
        elif line.startswith("REMARK PDBinfo-LABEL:"):
            _, _, number, label = line.split()[:4]
            labels[int(number)] = label
    loops = {}
    for chain in "HL":
        positions = [(number, aa) for number, (ch, aa) in residues.items() if ch == chain]
        if "".join(aa for _, aa in positions) != chains[chain + arm]:
            raise ValueError(f"{pdb}: chain {chain} does not match AF3 input")
        for index, (number, _) in enumerate(positions, 1):
            if labels.get(number) in {chain + "1", chain + "2", chain + "3"}:
                loops.setdefault(labels[number], []).append(index)
    if set(loops) != {"H1", "H2", "H3", "L1", "L2", "L3"}:
        raise ValueError(f"{pdb}: incomplete loop mapping")
    canonical = "".join((root / "data/raw/uniprot/Q5ZPR3.fasta").read_text().splitlines()[1:])
    if chains["T"] != canonical[28:466]:
        raise ValueError("AF3 antigen differs from canonical residues 29–466")
    af3 = Path(row["af3_input"])
    models = af3.parent.parent.parent / "fab_category_outputs" / af3.parent.name / af3.stem
    samples = []
    for cif in sorted(models.glob("*/*sample*/*_model.cif")):
        antigen = []
        fab = []
        for line in cif.open():
            if not line.startswith("ATOM "):
                continue
            fields = line.split()
            if fields[2] == "H":
                continue
            chain, index = fields[6], int(fields[8])
            xyz = tuple(map(float, fields[10:13]))
            if chain == "T" and index + 28 in PATCH[arm]:
                antigen.append((index + 28, xyz))
            elif chain in {"H" + arm, "L" + arm}:
                fab.append((chain, index, AA[fields[5]], xyz))
        if set(n for n, _ in antigen) != set(PATCH[arm]) or not fab:
            raise ValueError(f"{cif}: missing expected chains or patch residues")
        contacts = {}
        for target, xyz in antigen:
            for chain, index, aa, other in fab:
                distance = dist(xyz, other)
                if distance <= 4.5:
                    key = (target, chain, index, aa)
                    contacts[key] = min(distance, contacts.get(key, 4.5))
        samples.append({"source": str(cif), "contacts": [
            {"target_canonical": target, "chain": chain, "position": index,
             "residue": aa, "min_distance_A": round(distance, 2)}
            for (target, chain, index, aa), distance in sorted(contacts.items())
        ]})
    if len(samples) != 4:
        raise ValueError(f"Expected four 4Ig models for {arm}{row['parent']}, found {len(samples)}")
    return json.dumps({"loop_source": str(pdb), "rfantibody_design_loop_positions": loops,
                       "numbering": "One-based parent chain positions. RFantibody labels, not IMGT.",
                       "contact_cutoff_A": 4.5, "modeled_4ig_samples": samples}, indent=2)
