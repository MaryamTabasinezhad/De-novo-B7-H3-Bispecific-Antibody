#!/usr/bin/env python3
"""Convert selected RF2 PDB complexes into minimal AlphaFold 3 JSON inputs."""
import argparse, json, pathlib
AA = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def seqs(pdb):
    chains={}
    seen=set()
    for line in pathlib.Path(pdb).read_text().splitlines():
        if not line.startswith(('ATOM  ','HETATM')) or len(line)<27: continue
        if line[0:6].strip()=='HETATM' and line[17:20].strip()!='MSE': continue
        c=line[21].strip(); n=line[22:26].strip(); aa=AA.get(line[17:20].strip())
        if c and n and aa and (c,n) not in seen:
            chains.setdefault(c,[]).append(aa); seen.add((c,n))
    return chains
ap=argparse.ArgumentParser(); ap.add_argument('--pdb',required=True); ap.add_argument('--out',required=True); ap.add_argument('--name',required=True); ap.add_argument('--seeds',type=int,nargs='+',default=[101,202])
a=ap.parse_args(); s=seqs(a.pdb)
missing=[c for c in ('H','L','T') if c not in s]
if missing: raise SystemExit(f'missing chains {missing} in {a.pdb}')
obj={'name':a.name,'sequences':[{'protein':{'id':c,'sequence':''.join(s[c]),'description':f'RF2 complex chain {c}'}} for c in ('H','L','T')],'modelSeeds':a.seeds,'dialect':'alphafold3','version':4}
pathlib.Path(a.out).write_text(json.dumps(obj,indent=2)+'\n')
print(a.out, {c:len(s[c]) for c in ('H','L','T')})
