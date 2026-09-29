#!/usr/bin/env python3
"""Prepare AF3 JSON for Arm A-only, Arm B-only, or dual-Fab category."""
import argparse, csv, json
from pathlib import Path

AA={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}

def pdb_sequences(path, wanted=None):
    out={}; seen=set()
    for line in Path(path).read_text().splitlines():
        if not line.startswith(('ATOM  ','HETATM')) or len(line)<27: continue
        if line[0:6].strip()=='HETATM' and line[17:20].strip()!='MSE': continue
        c=line[21].strip(); r=line[22:26].strip(); aa=AA.get(line[17:20].strip())
        if wanted and c not in wanted: continue
        if c and r and aa and (c,r) not in seen:
            out.setdefault(c,[]).append((int(r),aa)); seen.add((c,r))
    return out

def fasta_chain(path, chain, start=None, end=None):
    vals=pdb_sequences(path,{chain}).get(chain,[])
    if start is not None: vals=[x for x in vals if x[0]>=start and x[0]<=end]
    if not vals: raise SystemExit(f'no residues for chain {chain} in {path}')
    return ''.join(a for _,a in vals)

def rows(path):
    with Path(path).open(newline='') as f: return list(csv.DictReader(f,delimiter='\t'))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--category',choices=['A','B','AB'],required=True); ap.add_argument('--index',type=int,required=True); ap.add_argument('--arm-a-tsv',type=Path,required=True); ap.add_argument('--arm-b-tsv',type=Path,required=True); ap.add_argument('--target-pdb',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--seeds',type=int,nargs='+',default=[101,202]); a=ap.parse_args()
    aa=rows(a.arm_a_tsv); bb=rows(a.arm_b_tsv)
    if a.category=='A':
        if a.index>=len(aa): raise SystemExit('Arm A index outside shortlist')
        ra=aa[a.index]; seqs=[('HA',fasta_chain(ra['file'],'H')),('LA',fasta_chain(ra['file'],'L'))]; name=f'fabA_rf2_task{ra["rf2_task"]}'
        lineage={'arm_a_task':ra['rf2_task'],'arm_b_task':None,'arm_a_pdb':ra['file'],'arm_b_pdb':None}
    elif a.category=='B':
        if a.index>=len(bb): raise SystemExit('Arm B index outside shortlist')
        rb=bb[a.index]; seqs=[('HB',fasta_chain(rb['file'],'H')),('LB',fasta_chain(rb['file'],'L'))]; name=f'fabB_rf2_task{rb["rf2_task"]}'
        lineage={'arm_a_task':None,'arm_b_task':rb['rf2_task'],'arm_a_pdb':None,'arm_b_pdb':rb['file']}
    else:
        if a.index>=len(aa)*len(bb): raise SystemExit('dual index outside 40x29 pair space')
        ia,ib=divmod(a.index,len(bb)); ra,rb=aa[ia],bb[ib]
        seqs=[('HA',fasta_chain(ra['file'],'H')),('LA',fasta_chain(ra['file'],'L')),('HB',fasta_chain(rb['file'],'H')),('LB',fasta_chain(rb['file'],'L'))]; name=f'fabAB_A{ra["rf2_task"]}_B{rb["rf2_task"]}'
        lineage={'arm_a_task':ra['rf2_task'],'arm_b_task':rb['rf2_task'],'arm_a_pdb':ra['file'],'arm_b_pdb':rb['file']}
    seqs.append(('T',fasta_chain(a.target_pdb,'A',29,466)))
    obj={'name':name,'sequences':[{'protein':{'id':c,'sequence':s,'description':f'{a.category} category {c}'}} for c,s in seqs],'modelSeeds':a.seeds,'dialect':'alphafold3','version':4}
    a.out.parent.mkdir(parents=True,exist_ok=True); a.out.write_text(json.dumps(obj,indent=2)+'\n'); a.out.with_suffix('.lineage.json').write_text(json.dumps(lineage,indent=2)+'\n'); print(json.dumps({'category':a.category,'index':a.index,'name':name,'lineage':lineage,'lengths':{c:len(s) for c,s in seqs}}))
if __name__=='__main__': main()
