#!/usr/bin/env python3
"""Prepare RFantibody HLT framework and target crops for the approved patches."""
from pathlib import Path
import argparse, math, shutil

AA_ATOM = {"ATOM  ", "HETATM"}

def xyz(line):
    return tuple(float(line[30+i:38+i]) for i in (0,8,16))

def prepare_target(src, out, core, target_chain="C", margin=12.0):
    lines=src.read_text().splitlines()
    atoms=[l for l in lines if l[:6] in AA_ATOM and l[21].strip()==target_chain]
    core_atoms=[xyz(l) for l in atoms if int(l[22:26]) in core]
    keep=[]
    for l in atoms:
        p=xyz(l)
        if min(math.dist(p,q) for q in core_atoms) <= margin:
            keep.append(l[:21]+"T"+l[22:])
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(keep)+"\nTER\nEND\n")
    residues=sorted({int(l[22:26]) for l in keep})
    return residues

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--target',type=Path,required=True); ap.add_argument('--framework',type=Path,required=True); ap.add_argument('--outdir',type=Path,required=True); ap.add_argument('--target-chain',default='C'); args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.framework,args.outdir/'framework_HLT.pdb')
    specs={'A':[126,127,128,129], 'B':[228,229,232,234,236,238,240,241]}
    for arm,core in specs.items():
        residues=prepare_target(args.target,args.outdir/f'target_{arm}.pdb',core,target_chain=args.target_chain)
        (args.outdir/f'target_{arm}_scope.txt').write_text(f"arm={arm}\nsource_chain={args.target_chain}\ncore={','.join(map(str,core))}\nmargin_A=12.0\nretained_range={min(residues)}-{max(residues)}\nretained_residues={len(residues)}\nhotspots={';'.join('T'+str(x) for x in core)}\n")
        print(arm, 'retained',len(residues),'residues',min(residues),max(residues))
if __name__=='__main__': main()
