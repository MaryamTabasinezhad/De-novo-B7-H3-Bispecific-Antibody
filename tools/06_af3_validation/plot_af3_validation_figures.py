#!/usr/bin/env python3
"""Create publication-oriented AF3 validation figures from tracked summaries."""
from __future__ import annotations
import argparse, csv, json, re
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

EP = {'A': [126,127,128,129], 'B': [228,229,232,234,236,238,240,241]}
COL = {'A':'#1769aa','B':'#c44e52'}

def read_tsv(path):
    with Path(path).open() as f: return list(csv.DictReader(f, delimiter='\t'))

def f(rows, key): return np.array([float(r[key]) for r in rows], dtype=float)

def atom_coordinates(path):
    lines=Path(path).read_text().splitlines(); i=lines.index('_atom_site.group_PDB'); heads=[]
    while i<len(lines) and lines[i].startswith('_atom_site.'):
        heads.append(lines[i].split('.',1)[1]); i+=1
    ix={h:j for j,h in enumerate(heads)}; out={c:[] for c in ('H','L','T')}
    for line in lines[i:]:
        if line.startswith('#'): break
        if not line.strip() or line.startswith('_') or line.startswith('loop_'): continue
        v=line.split();
        if len(v)<len(heads): continue
        c=v[ix['auth_asym_id']]
        if c not in out or v[ix['type_symbol']].upper()=='H': continue
        try:
            out[c].append((float(v[ix['Cartn_x']]), float(v[ix['Cartn_y']]),
                           float(v[ix['Cartn_z']]), int(v[ix['auth_seq_id']])))
        except (ValueError,IndexError): pass
    return out

def contact_residues(coords, arm):
    # Grid-based atom contact audit, matching the tracked 4.5-A convention.
    target=coords['T']; antibody=[(x,c) for c in ('H','L') for x in coords[c]]
    if not target: return set()
    radius=4.5; r2=radius*radius; grid={}
    cell=lambda x: tuple(int(v//radius) for v in x[:3])
    for j,x in enumerate(target): grid.setdefault(cell(x),[]).append(j)
    start=86 if arm=='A' else 188; min_t=min(x[3] for x in target); hits=set()
    for x,c in antibody:
        q=cell(x)
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for j in grid.get((q[0]+dx,q[1]+dy,q[2]+dz),[]):
                        y=target[j]
                        if sum((x[k]-y[k])**2 for k in range(3))<=r2:
                            can=start+y[3]-min_t
                            if can in EP[arm]: hits.add(can)
    return hits

def structure_path(root, arm, task, seed, sample):
    pat=f'arm{arm}_rf2_task{task}_seed-{seed}_sample-{sample}_model.cif'
    return next(Path(root).glob(f'arm{arm}_row*/arm{arm}_rf2_task{task}/seed-{seed}_sample-{sample}/{pat}'))

def save(fig, out, name):
    try: fig.tight_layout()
    except RuntimeError: pass
    fig.savefig(out/f'{name}.png',dpi=300,bbox_inches='tight'); fig.savefig(out/f'{name}.pdf',bbox_inches='tight'); plt.close(fig)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--summary',type=Path,required=True); ap.add_argument('--scratch',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    per=read_tsv(args.summary/'per_input.tsv'); samp=read_tsv(args.summary/'per_sample.tsv')
    plt.rcParams.update({'font.size':9,'axes.titlesize':11,'axes.labelsize':9,'font.family':'DejaVu Sans'})
    # Figure 1: funnel, with explicit repeated-prediction distinction.
    fig,ax=plt.subplots(figsize=(8.2,4.8)); stages=['RF2\ninputs','AF3\ncompleted','No clash\nflag','≥1 epitope\ncontact','≥2 contacts\nin all 4 samples']
    vals={'A':[40,40,40,27,0],'B':[29,29,29,29,2]}; x=np.arange(len(stages)); w=.34
    for off,a in [(-w/2,'A'),(w/2,'B')]:
        bars=ax.bar(x+off,vals[a],w,label=f'Arm {a}',color=COL[a]); ax.bar_label(bars,fontsize=8,padding=2)
    ax.set_xticks(x,stages); ax.set_ylabel('Number of RF2 input models'); ax.set_title('Figure 1. AF3 validation funnel (computational predictions)'); ax.legend(frameon=False); ax.text(.01,-.20,'Each input produced 4 AF3 seed/sample predictions: 69 inputs = 276 repeated AF3 complexes.',transform=ax.transAxes,fontsize=8)
    save(fig,args.out,'Figure1_validation_funnel')
    # Figure 2: paired confidence distributions.
    fig,axs=plt.subplots(2,2,figsize=(8,7)); specs=[('HL_iptm','H–L ipTM',None),('HT_iptm','H–T ipTM',None),('LT_iptm','L–T ipTM',None),('HT_pae_min','H–T interface PAE (Å)',None)]
    for ax,(key,label,_) in zip(axs.flat,specs):
        data=[f([r for r in samp if r['arm']==a],key) for a in 'AB']; bp=ax.boxplot(data,patch_artist=True,labels=['Arm A','Arm B'],showfliers=False)
        for patch,c in zip(bp['boxes'],[COL['A'],COL['B']]): patch.set_facecolor(c); patch.set_alpha(.65)
        ax.set_ylabel(label); ax.grid(axis='y',alpha=.25)
    fig.suptitle('Figure 2. AF3 confidence distributions (computational structural predictions)'); save(fig,args.out,'Figure2_interface_confidence')
    # Figure 3: contact reproducibility heatmaps.
    fig,axs=plt.subplots(2,1,figsize=(9,10),constrained_layout=True); cmap=LinearSegmentedColormap.from_list('contact',['#f7fbff','#6baed6','#08306b'])
    for ax,a in zip(axs,'AB'):
        rows=sorted([r for r in per if r['arm']==a],key=lambda r:int(r['rf2_task'])); mat=[]
        for r in rows:
            ss=[s for s in samp if s['input']==r['input']]; mat.append([sum(int(str(s['selected_epitope_residues'])!='-' and str(res) in str(s['selected_epitope_residues']).split(',')) for s in ss) for res in EP[a]])
        im=ax.imshow(np.array(mat),aspect='auto',vmin=0,vmax=4,cmap=cmap); ax.set_yticks(range(len(rows)),[r['rf2_task'] for r in rows],fontsize=6); ax.set_xticks(range(len(EP[a])),EP[a]); ax.set_ylabel(f'Arm {a} RF2 task'); ax.set_title(f'Arm {a} selected-residue contact recovery (0–4 AF3 samples)'); fig.colorbar(im,ax=ax,label='AF3 samples contacting residue',shrink=.8)
    fig.suptitle('Figure 3. Epitope-contact reproducibility (canonical CD276 numbering)'); save(fig,args.out,'Figure3_contact_heatmaps')
    # Figure 4: scatter plus 3-D structural examples.
    fig=plt.figure(figsize=(13,5.2)); ax=fig.add_subplot(1,3,1)
    for a in 'AB':
        rr=[r for r in per if r['arm']==a]; ax.scatter(f(rr,'mean_HT_iptm'),f(rr,'samples_contact_ge2'),s=38,c=COL[a],alpha=.8,label=f'Arm {a}')
    ax.set_xlabel('Mean H–T ipTM'); ax.set_ylabel('AF3 samples with ≥2 selected contacts'); ax.set_title('Candidate comparison'); ax.legend(frameon=False); ax.grid(alpha=.25)
    for a,task,seed,sample,slot in [('A','283','202','1',2),('B','101','202','1',3)]:
        ax=fig.add_subplot(1,3,slot,projection='3d'); c=atom_coordinates(structure_path(args.scratch,a,task,seed,sample));
        for chain,color,label in [('T','#808080','B7-H3'),('H',COL[a],'heavy'),('L','#2ca25f','light')]:
            xyz=np.array([[x[0],x[1],x[2]] for x in c[chain]]); ax.scatter(xyz[:,0],xyz[:,1],xyz[:,2],s=2 if chain=='T' else 4,c=color,label=label,alpha=.45 if chain=='T' else .8)
        hits=contact_residues(c,a); target=np.array([[x[0],x[1],x[2]] for x in c['T'] if (86 if a=='A' else 188)+x[3]-min(x2[3] for x2 in c['T']) in hits]);
        if len(target): ax.scatter(target[:,0],target[:,1],target[:,2],s=28,c='#f0c419',label='selected contacts')
        ax.set_title(f'Arm {a}, RF2 task {task}\nAF3 seed {seed}, sample {sample}'); ax.set_axis_off(); ax.legend(frameon=False,fontsize=7,loc='upper left')
    fig.suptitle('Figure 4. Candidate comparison and representative AF3 structures\nComputational structural predictions; examples are not experimentally confirmed binders',fontsize=11); save(fig,args.out,'Figure4_candidate_structures')
    manifest={'figures':['Figure1_validation_funnel','Figure2_interface_confidence','Figure3_contact_heatmaps','Figure4_candidate_structures'],'representative_structures':{'Arm A':'RF2 task 283, AF3 seed 202 sample 1','Arm B':'RF2 task 101, AF3 seed 202 sample 1'},'source_tables':['per_input.tsv','per_sample.tsv'],'note':'All figures are computational structural predictions; no affinity or biological activity is inferred.'}
    (args.out/'figure_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__': main()
