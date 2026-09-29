#!/usr/bin/env python3
"""Summarize AF3 shortlist confidence and canonical epitope contacts."""
import argparse, csv, json, re
from pathlib import Path

EPITOPES = {'A': (86, {126,127,128,129}),
            'B': (188, {228,229,232,234,236,238,240,241})}

def atoms(path):
    lines = path.read_text().splitlines(); start = lines.index('_atom_site.group_PDB')
    heads=[]
    while start < len(lines) and lines[start].startswith('_atom_site.'):
        heads.append(lines[start].split('.',1)[1]); start += 1
    ix={h:i for i,h in enumerate(heads)}; out={c:[] for c in ('H','L','T')}
    for line in lines[start:]:
        if line.startswith('#'): break
        if not line.strip() or line.startswith('_') or line.startswith('loop_'): continue
        vals=line.split()
        if len(vals) < len(heads): continue
        chain=vals[ix['auth_asym_id']]
        if chain not in out or vals[ix['type_symbol']].upper() == 'H': continue
        try:
            xyz = (float(vals[ix['Cartn_x']]), float(vals[ix['Cartn_y']]),
                   float(vals[ix['Cartn_z']]))
            out[chain].append((xyz, int(vals[ix['auth_seq_id']])))
        except (ValueError, IndexError): continue
    return out

def contacts(path, arm):
    a=atoms(path); target=a['T']; antibody=[(xyz,c) for c in ('H','L') for xyz,_ in a[c]]
    if not target or not antibody: return (0,0,'-','-')
    # Small uniform spatial grid avoids requiring SciPy on the login node.
    radius=4.5; r2=radius*radius; grid={}
    cell=lambda xyz: tuple(int(v//radius) for v in xyz)
    for j,(xyz,_) in enumerate(target): grid.setdefault(cell(xyz),[]).append(j)
    start, selected=EPITOPES[arm]; min_t=min(r for _,r in target); hitres=set(); sel=set(); chains=set()
    for xyz,chain in antibody:
        c=cell(xyz); inds=[]
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                for dz in (-1,0,1):
                    for j in grid.get((c[0]+dx,c[1]+dy,c[2]+dz),[]):
                        tx=target[j][0]; dist=sum((xyz[k]-tx[k])**2 for k in range(3))
                        if dist <= r2: inds.append(j)
        if inds: chains.add(chain)
        for j in inds:
            can=start + target[j][1] - min_t; hitres.add(can)
            if can in selected: sel.add(can)
    return len(hitres),len(sel),','.join(map(str,sorted(sel))) or '-',','.join(sorted(chains)) or '-'

def floats(v): return [float(x) for x in v]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    rows=[]; samples=[]
    for d in sorted(args.root.glob('arm?_row*')):
        top=next(d.glob('*/*_summary_confidences.json'),None)
        rank=next(d.glob('*/*_ranking_scores.csv'),None)
        if not top or not rank: continue
        name=top.parent.name; arm=name[3]; task=name.split('task',1)[1]
        summary=json.loads(top.read_text()); scores=list(csv.DictReader(rank.open()))
        model_files=sorted(top.parent.glob('seed-*_sample-*/*_model.cif'))
        for mf in model_files:
            conf=json.loads(next(mf.parent.glob('*_summary_confidences.json')).read_text())
            m=re.match(r'seed-(\d+)_sample-(\d+)', mf.parent.name)
            if not m: continue
            seed, sample=m.groups()
            hr,sr,sres,chains=contacts(mf,arm)
            cp=conf['chain_pair_iptm']; pae=conf['chain_pair_pae_min']
            samples.append({'arm':arm,'rf2_task':task,'input':name,'seed':seed,'sample':sample,
                'ranking_score':conf['ranking_score'],'ptm':conf['ptm'],'iptm':conf['iptm'],
                'has_clash':int(conf['has_clash']),'fraction_disordered':conf['fraction_disordered'],
                'HL_iptm':cp[0][1],'HT_iptm':cp[0][2],'LT_iptm':cp[1][2],
                'HT_pae_min':pae[0][2],'LT_pae_min':pae[1][2],
                'target_contact_residues':hr,'selected_epitope_contacts':sr,
                'selected_epitope_residues':sres,'antibody_chains_with_contacts':chains})
        ss=[x for x in samples if x['input']==name]
        def mean(k): return sum(float(x[k]) for x in ss)/len(ss)
        rows.append({'arm':arm,'rf2_task':task,'input':name,'n_samples':len(ss),
            'n_clash_samples':sum(x['has_clash'] for x in ss),
            'mean_ranking_score':mean('ranking_score'),'mean_ptm':mean('ptm'),'mean_iptm':mean('iptm'),
            'mean_HL_iptm':mean('HL_iptm'),'mean_HT_iptm':mean('HT_iptm'),'mean_LT_iptm':mean('LT_iptm'),
            'mean_HT_pae_min':mean('HT_pae_min'),'mean_LT_pae_min':mean('LT_pae_min'),
            'samples_contact_ge1':sum(x['selected_epitope_contacts']>=1 for x in ss),
            'samples_contact_ge2':sum(x['selected_epitope_contacts']>=2 for x in ss),
            'samples_contact_ge3':sum(x['selected_epitope_contacts']>=3 for x in ss),
            'sample_epitope_residues':';'.join(f"{x['seed']}/{x['sample']}:{x['selected_epitope_residues']}" for x in ss)})
    args.out.mkdir(parents=True,exist_ok=True)
    def write(name, data):
        with (args.out/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t'); w.writeheader(); w.writerows(data)
    write('per_input.tsv',rows); write('per_sample.tsv',samples)
    print(json.dumps({'inputs':len(rows),'samples':len(samples),'arms':{a:sum(r['arm']==a for r in rows) for a in ('A','B')}}))

if __name__=='__main__': main()
