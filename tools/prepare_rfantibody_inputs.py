#!/usr/bin/env python3
"""Prepare RFantibody HLT framework and target crops for the approved patches."""
from pathlib import Path
import argparse, shutil

AA_ATOM = {"ATOM  ", "HETATM"}

def prepare_target(src, out, core, target_chain="C", sequence_padding=40):
    lines=src.read_text().splitlines()
    atoms=[l for l in lines if l[:6] in AA_ATOM and l[21].strip()==target_chain]
    lo=max(min(core)-sequence_padding, min(int(l[22:26]) for l in atoms))
    hi=min(max(core)+sequence_padding, max(int(l[22:26]) for l in atoms))
    keep=[l[:21]+"T"+l[22:] for l in atoms if lo <= int(l[22:26]) <= hi]
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(keep)+"\nTER\nEND\n")
    residues=sorted({int(l[22:26]) for l in keep})
    return residues

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--target',type=Path,required=True); ap.add_argument('--framework',type=Path,required=True); ap.add_argument('--outdir',type=Path,required=True); ap.add_argument('--target-chain',default='C'); ap.add_argument('--sequence-padding',type=int,default=40); args=ap.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    shutil.copy2(args.framework,args.outdir/'framework_HLT.pdb')
    specs={'A':[126,127,128,129], 'B':[228,229,232,234,236,238,240,241]}
    for arm,core in specs.items():
        residues=prepare_target(args.target,args.outdir/f'target_{arm}.pdb',core,target_chain=args.target_chain,sequence_padding=args.sequence_padding)
        (args.outdir/f'target_{arm}_scope.txt').write_text(f"arm={arm}\nsource_chain={args.target_chain}\ncore={','.join(map(str,core))}\nsequence_padding={args.sequence_padding}\nretained_range={min(residues)}-{max(residues)}\nretained_residues={len(residues)}\nhotspots={';'.join('T'+str(x) for x in core)}\n")
        print(arm, 'retained',len(residues),'residues',min(residues),max(residues))
if __name__=='__main__': main()
