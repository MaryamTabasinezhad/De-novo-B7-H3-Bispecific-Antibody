#!/usr/bin/env python3
"""Preliminary Step 2 geometry record for the user-confirmed B7-H3 pair."""
from pathlib import Path
from collections import defaultdict
import csv, math
import numpy as np

ROOT=Path('/project/def-ghaedi/ghaedi/mab')
PATCHES={
 'A': {'label':'8H9-like exposed IgV1 FG-loop','residues':[126,127,128,129], 'evidence':'experimental 8H9 mapping plus coordinate exposure'},
 'B': {'label':'coordinate-derived exposed IgC1 patch 2','residues':[228,229,232,234,236,238,240,241], 'evidence':'coordinate-derived exposure screen'},
}
FILES=[('human_4ig_afdb_v6_oriented','data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb'),('human_4ig_20G5_fab2','data/processed/target_ensemble/human_4ig_20G5_fab2_oriented.pdb')]

def parse(path):
 d=defaultdict(list)
 for l in path.read_text().splitlines():
  if not l.startswith('ATOM  ') or l[21].strip()!='A': continue
  try:
   n=int(l[22:26]); p=np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])])
  except ValueError: continue
  d[n].append(p)
 return d

rows=[]
for model,rel in FILES:
 d=parse(ROOT/rel); centers={}
 for arm,spec in PATCHES.items():
  coords=np.concatenate([d[n] for n in spec['residues'] if n in d])
  centers[arm]=coords.mean(0)
  rows.append({'model':model,'arm':arm,'label':spec['label'],'canonical_residues':';'.join(map(str,spec['residues'])),'n_atoms':len(coords),'centroid_x_A':round(float(centers[arm][0]),3),'centroid_y_A':round(float(centers[arm][1]),3),'centroid_z_A':round(float(centers[arm][2]),3),'z_min_A':round(float(coords[:,2].min()),3),'z_max_A':round(float(coords[:,2].max()),3),'evidence':spec['evidence']})
 a,b=centers['A'],centers['B'];
 min_dist=min(float(np.linalg.norm(x-y)) for x in np.concatenate([d[n] for n in PATCHES['A']['residues']]) for y in np.concatenate([d[n] for n in PATCHES['B']['residues']]))
 dist=float(np.linalg.norm(a-b))
 rows.append({'model':model,'arm':'PAIR','label':'A/B preliminary same-antigen separation','canonical_residues':'A:126-129;B:228,229,232,234,236,238,240,241','n_atoms':'','centroid_x_A':round(dist,3),'centroid_y_A':round(min_dist,3),'centroid_z_A':'','z_min_A':'','z_max_A':'','evidence':'centroid distance / minimum heavy-atom distance; not a Fab reach result'})
with (ROOT/'metadata/candidate_regions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['region_id','arm','label','domain','canonical_residues','evidence_class','status','notes']); w.writeheader(); w.writerows([
  {'region_id':'B7H3-A','arm':'A','label':PATCHES['A']['label'],'domain':'IgV1','canonical_residues':'126-129','evidence_class':'experimental_contact + coordinate exposure','status':'user-confirmed preliminary','notes':'8H9-like FG-loop; R127 and F129 pass the independent exposure screen'},
  {'region_id':'B7H3-B','arm':'B','label':PATCHES['B']['label'],'domain':'IgC1','canonical_residues':'228,229,232,234,236,238,240,241','evidence_class':'coordinate-derived exposure','status':'user-confirmed preliminary','notes':'Adjacent to and partly overlapping the edge of the broader 20G5 region; not assumed identical'},
 ])
with (ROOT/'metadata/binder_epitope_evidence.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['binder','source','domain','canonical_region','evidence','resolution']); w.writeheader(); w.writerows([
  {'binder':'8H9/omburtamab','source':'PMC4705981','domain':'IgV1 / homologous IgV2','canonical_region':'126-129 (IRDF)','evidence':'experimental mapping and validation','resolution':'residue-level'},
  {'binder':'20G5','source':'PDB 9LY5/9LY6','domain':'IgC1 / corresponding IgC2','canonical_region':'approximately 177-188 and 214-230','evidence':'cryo-EM structure and mutational support','resolution':'structural contact region'},
  {'binder':'T3CL11','source':'PDB 9LME','domain':'membrane-distal IgV','canonical_region':'project preliminary 64-89 and 123-130','evidence':'2.4-A complex; partial module','resolution':'partial structure; preliminary canonical mapping'},
 ])
with (ROOT/'work/02_epitope_selection/epitope_pair_geometry.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('wrote',len(rows),'geometry rows')
