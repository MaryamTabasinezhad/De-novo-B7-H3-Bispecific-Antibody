#!/usr/bin/env python3
"""Build a mapped, membrane-oriented Step 1 B7-H3 target ensemble.

This is a small project-specific preparation worker. It uses only standard
library code plus numpy/scipy from the verified Rorqual scipy-stack module;
raw UniProt/RCSB/AlphaFold inputs remain immutable.
"""
from __future__ import annotations
import csv, json, math, re, shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
import numpy as np
from scipy.spatial.transform import Rotation

ROOT = Path("/project/def-ghaedi/ghaedi/mab")
RAW_U = ROOT / "data/raw/uniprot"
RAW_S = ROOT / "data/raw/structures"
OUT = ROOT / "data/processed/target_ensemble"
META = ROOT / "metadata"
WORK = ROOT / "work/01_target_preparation"
OUT.mkdir(parents=True, exist_ok=True); META.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
NOW = datetime.now(timezone.utc).isoformat()

AA3 = {"ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLN":"Q","GLU":"E","GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V","MSE":"M"}

def fasta(path):
    lines = path.read_text().splitlines()
    return "".join(x.strip() for x in lines if x and not x.startswith(">"))

def get_json(url):
    with urlopen(url, timeout=60) as h: return json.loads(h.read().decode())

def global_map(ref, query):
    """Return query-index -> 1-based ref-index map using a deterministic NW alignment."""
    n,m=len(ref),len(query); gap=-2; match=2; mismatch=-1
    score=[[0]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1): score[i][0]=i*gap
    for j in range(1,m+1): score[0][j]=j*gap
    for i in range(1,n+1):
        for j in range(1,m+1):
            score[i][j]=max(score[i-1][j-1]+(match if ref[i-1]==query[j-1] else mismatch), score[i-1][j]+gap, score[i][j-1]+gap)
    i,j=n,m; pairs=[]
    while i or j:
        if i and j and score[i][j]==score[i-1][j-1]+(match if ref[i-1]==query[j-1] else mismatch):
            pairs.append((j,i)); i-=1; j-=1
        elif i and score[i][j]==score[i-1][j]+gap: i-=1
        else: j-=1
    pairs.reverse(); return {q:r for q,r in pairs}

def parse_pdb(path, chain=None):
    residues={}; atoms=[]; het=[]
    for line in path.read_text(errors="replace").splitlines():
        if len(line)<54 or line[:6].strip() not in ("ATOM","HETATM"): continue
        ch=line[21].strip();
        if chain is not None and ch!=chain: continue
        try: rn=int(line[22:26]); icode=line[26].strip(); xyz=np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])],float)
        except ValueError: continue
        resn=line[17:20].strip(); key=(rn,icode)
        if line[:6].strip()=="ATOM" and resn in AA3:
            residues.setdefault(key,{"resn":resn,"atoms":[]})["atoms"].append((line,xyz))
            atoms.append((line,xyz,key))
        elif line[:6].strip()=="HETATM": het.append((line,xyz,key,resn))
    ordered=sorted(residues.items(), key=lambda kv:(kv[0][0],kv[0][1]))
    return ordered, atoms, het

def ca_coords(ordered):
    out=[]
    for (rn,ic),r in ordered:
        for line,xyz in r["atoms"]:
            if line[12:16].strip()=="CA": out.append(((rn,ic),xyz)); break
    return out

def transform_pdb(src, dst, transforms, keep_het=True):
    out=[]
    for line in src.read_text(errors="replace").splitlines(True):
        if len(line)>=54 and line[:6].strip() in ("ATOM","HETATM"):
            ch=line[21].strip()
            if ch in transforms:
                R,t=transforms[ch]; xyz=np.array([float(line[30:38]),float(line[38:46]),float(line[46:54])]); q=R@xyz+t
                line=f"{line[:30]}{q[0]:8.3f}{q[1]:8.3f}{q[2]:8.3f}{line[54:]}"
            if line[:6].strip()=="HETATM" and not keep_het: continue
        out.append(line)
    dst.write_text("".join(out))

def orient_reference(af_path, tm_lo, tm_hi):
    ordered,_,_=parse_pdb(af_path, "A"); cas=dict(ca_coords(ordered));
    pts=np.array([cas[i] for i in sorted(cas) if tm_lo<=i[0]<=tm_hi]); center=pts.mean(0)
    cov=np.cov((pts-center).T); vals,vecs=np.linalg.eigh(cov); axis=vecs[:,np.argmax(vals)]
    if axis[2]<0: axis=-axis
    rot,_=Rotation.align_vectors(np.array([[0.,0.,1.]]), np.array([axis]))
    R=rot.as_matrix();
    # Translate TM midpoint to z=0, then choose extracellular side as +z.
    c2=R@center; ext=np.array([R@cas[i] for i in sorted(cas) if 29<=i[0]<=461]).mean(0)-c2
    if ext[2]<0:
        flip=np.diag([1.,-1.,-1.]); R=flip@R; c2=R@center
    return R, -R@center

def metadata_rcsb(pdb):
    d=get_json(f"https://data.rcsb.org/rest/v1/core/entry/{pdb}")
    return {"pdb":pdb,"title":d.get("struct",{}).get("title"),"method":d.get("rcsb_entry_info",{}).get("experimental_method"),"resolution":d.get("rcsb_entry_info",{}).get("resolution_combined"),"release_date":d.get("rcsb_accession_info",{}).get("initial_release_date"),"url":f"https://data.rcsb.org/rest/v1/core/entry/{pdb}","retrieved_utc":NOW}

def main():
    iso1=fasta(RAW_U/"Q5ZPR3-1.fasta"); iso2=fasta(RAW_U/"Q5ZPR3-2.fasta")
    # Canonical feature boundaries from the reviewed UniProt flatfile.
    features={"accession":"Q5ZPR3","entry_version":176,"sequence_version":1,"retrieved_utc":NOW,"signal_peptide":[1,28],"transmembrane":[467,487],"extracellular":[29,466],"cytoplasmic":[488,534],"domains":[[29,139],[145,238],[243,357],[363,456]],"n_linked_glycosylation_sites":[104,189,215,322,407,433],"isoforms":{"Q5ZPR3-1":{"length":len(iso1),"role":"canonical human 4Ig; membrane baseline"},"Q5ZPR3-2":{"length":len(iso2),"role":"shorter human 2Ig; optional characterization; membrane/soluble presentation not conflated"}},"sources":["https://rest.uniprot.org/uniprotkb/Q5ZPR3.txt","https://rest.uniprot.org/uniprotkb/Q5ZPR3-1.fasta","https://rest.uniprot.org/uniprotkb/Q5ZPR3-2.fasta"]}
    (META/"target_features.json").write_text(json.dumps(features,indent=2)+"\n")
    af=RAW_S/"AF-Q5ZPR3-F1-model_v6.pdb"; Rref,tref=orient_reference(af,467,487)
    # Orient full-length AlphaFold baseline and produce a glycan-free control (no glycans in AF).
    transform_pdb(af,OUT/"human_4ig_afdb_v6_oriented.pdb",{"A":(Rref,tref)},keep_het=False)
    af2=RAW_S/"AF-Q5ZPR3-2-F1-model_v6.pdb"; seq2map=global_map(iso1,iso2); tm2=[q for q,r in seq2map.items() if 467<=r<=487];
    o2,_,_=parse_pdb(af2,"A"); cas2=dict(ca_coords(o2)); pts2=np.array([cas2[i] for i in sorted(cas2) if tm2 and min(tm2)<=i[0]<=max(tm2)]); c2=pts2.mean(0); vals,vecs=np.linalg.eigh(np.cov((pts2-c2).T)); axis=vecs[:,np.argmax(vals)];
    if axis[2]<0: axis=-axis
    rot,_=Rotation.align_vectors(np.array([[0.,0.,1.]]),np.array([axis])); R2=rot.as_matrix(); ext2=np.array([R2@cas2[i] for i in sorted(cas2) if i[0] < min(tm2)]).mean(0)-R2@c2
    if ext2[2]<0: R2=np.diag([1.,-1.,-1.])@R2
    t2=-R2@c2; transform_pdb(af2,OUT/"human_2ig_afdb_v6_oriented.pdb",{"A":(R2,t2)},keep_het=False)
    # Experimental ectodomain structures: map target chain to canonical 4Ig and orient into AF frame.
    exp=[("9LY5","C","human_4ig_20G5_fab"),("9LY6","A","human_4ig_20G5_fab2"),("9LME","A","human_4ig_T3CL11_nanobody_partial")]
    maps=[]; manifest=[]; qc=[]
    for pdb,ch,label in exp:
        src=RAW_S/(pdb+".pdb"); ordered,atoms,hets=parse_pdb(src,ch); qseq="".join(AA3[r["resn"]] for _,r in ordered); ca=dict(ca_coords(ordered));
        # 9LME contains an N-terminal ENLYFQG affinity tag. Its construct
        # residue numbering then resumes at canonical B7-H3 residue 29;
        # avoid a repeat-domain global alignment that can map the tag and
        # repeated Ig domains to the wrong canonical copy.
        if pdb == "9LME":
            qm={i:key[0]-28 for i,(key,_) in enumerate(ca_coords(ordered),start=1) if key[0] >= 29}
        else:
            qm=global_map(iso1[28:466],qseq)
        common=[(k,29+qm[i]-1) for i,(k,_) in enumerate([(x[0],x[1]) for x in ca.items()]) if i in qm and (29+qm[i]-1) in dict(ca)];
        # Build alignment using explicit order from residues; map target residues to AF CA coordinates.
        exp_pts=[]; af_pts=[]; rows=[]; can_for_q={i:28+qm[i] for i in qm}
        aford,_,_=parse_pdb(af,"A"); afca=dict(ca_coords(aford))
        for qi,(key,xyz) in enumerate(ca_coords(ordered),start=1):
            if qi in can_for_q and (can_for_q[qi],"") in afca:
                exp_pts.append(xyz); af_pts.append(afca[(can_for_q[qi],"")]); rows.append((key,can_for_q[qi],qseq[qi-1]))
        if len(exp_pts)<20: raise RuntimeError(f"too few mapped residues for {pdb}: {len(exp_pts)}")
        rc,_=Rotation.align_vectors(np.array(af_pts),np.array(exp_pts)); Re=Rref@rc.as_matrix(); te=tref + Rref@(np.array(af_pts).mean(0)-rc.as_matrix()@np.array(exp_pts).mean(0))
        base=OUT/(label+"_oriented.pdb"); transform_pdb(src,base,{ch:(Re,te)},keep_het=True); transform_pdb(src,OUT/(label+"_unglycosylated_oriented.pdb"),{ch:(Re,te)},keep_het=False)
        meta=metadata_rcsb(pdb); meta.update({"label":label,"chain":ch,"canonical_range":[min(r[1] for r in rows),max(r[1] for r in rows)],"mapped_residues":len(rows),"glycan_state":"resolved HETATM retained"}); manifest.append(meta)
        for key,can,aa in rows: maps.append({"source":pdb,"chain":ch,"model_residue":key[0],"canonical_residue":can,"aa":aa})
        qc.append({"model":label,"type":"experimental","mapped_residues":len(rows),"canonical_start":min(r[1] for r in rows),"canonical_end":max(r[1] for r in rows),"membrane_orientation":"oriented to AFDB transmembrane axis; ectodomain is +z","glycan_control":"resolved and unglycosylated copies"})
    manifest += [{"label":"human_4ig_afdb_v6_oriented","type":"predicted","source":"AlphaFold DB AF-Q5ZPR3-F1-model_v6","chain":"A","canonical_range":"1-534","mapped_residues":534,"glycan_state":"none; glycan-free model","membrane_orientation":"TM 467-487 centered at z=0; extracellular +z","url":"https://alphafold.ebi.ac.uk/entry/AF-Q5ZPR3-F1"},{"label":"human_2ig_afdb_v6_oriented","type":"predicted","source":"AlphaFold DB AF-Q5ZPR3-2-F1-model_v6","chain":"A","canonical_range":"isoform 2 coordinates","mapped_residues":len(iso2),"glycan_state":"none; glycan-free model","membrane_orientation":"isoform-2 TM mapped from canonical 467-487; extracellular +z","url":"https://alphafold.ebi.ac.uk/entry/AF-Q5ZPR3-2-F1"}]
    qc += [{"model":"human_4ig_afdb_v6_oriented","type":"predicted","mapped_residues":534,"canonical_start":1,"canonical_end":534,"membrane_orientation":"TM 467-487 centered at z=0; extracellular +z","glycan_control":"not modeled; experimental glycan controls retained separately"},{"model":"human_2ig_afdb_v6_oriented","type":"predicted","mapped_residues":len(iso2),"canonical_start":"isoform 2","canonical_end":"isoform 2","membrane_orientation":"TM mapped from canonical coordinates; extracellular +z","glycan_control":"not modeled"}]
    with (META/"structure_manifest.csv").open("w",newline="") as f:
        fields=sorted({k for x in manifest for k in x}); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(manifest)
    with (META/"numbering_map.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["source","chain","model_residue","canonical_residue","aa"]); w.writeheader(); w.writerows(maps)
    with (WORK/"ensemble_qc.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=sorted({k for x in qc for k in x})); w.writeheader(); w.writerows(qc)
    (WORK/"run_notes.md").write_text(f"# Step 1 target preparation\n\nRetrieved UTC: {NOW}\n\nInputs: UniProt Q5ZPR3 entry version 176 / sequence version 1; AlphaFold DB model v6; RCSB 9LY5, 9LY6, 9LME.\n\nOrientation: AFDB transmembrane axis mapped to z with the ectodomain on +z and TM midpoint at z=0. Experimental ectodomains were rigidly mapped to the AFDB frame by target-chain Cα alignment; resolved-glycan and unglycosylated controls were emitted.\n\nLimitations: representative modeled glycoforms, loop repair/relaxation, and 4Ig oligomer hypotheses were not fabricated. They require a glycan/structure modeling runtime not currently verified.\n")
    print('Step1 outputs written:', len(manifest),'manifest rows,',len(maps),'mapping rows')

if __name__=='__main__': main()
