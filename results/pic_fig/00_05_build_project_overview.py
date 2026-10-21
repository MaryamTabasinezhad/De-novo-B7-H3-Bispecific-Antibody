#!/usr/bin/env python3
"""Data-derived 16:9 overview; editable native PowerPoint shapes + vector SVG.
Layout adapted from ab42-binder-design build_editable_slide.py (b046eb1).
No inference runs; all counts are from tracked tables and the 18 October audit.
Run from project root after sourcing config/hpc/rorqual.sh.
"""
import csv,json,subprocess,zipfile
from pathlib import Path
from xml.sax.saxutils import escape as E
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
STEM='00_05_b7h3_project_overview'
rows=list(csv.DictReader((ROOT/'results/06_02_af3_validation_shortlist/per_input.tsv').open(),delimiter='\t'))
assert len(rows)==69 and sum(int(r['n_samples']) for r in rows)==276
counts={a:sum(1 for _ in csv.DictReader((ROOT/f'results/05_01_rf2_qc_20260927/arm_{a.lower()}.tsv').open(),delimiter='\t')) for a in 'AB'}
assert counts=={'A':1176,'B':1188}
audit=list(csv.DictReader((ROOT/'results/07_03_fab_AB_pairs/07_03_output_audit_20261017.tsv').open(),delimiter='\t'))
assert len(audit)==1160 and sum(r['artifact_status']=='complete' for r in audit)==164
navy='102B46';blue='0072B2';muted='546B7E';text='263E53';bg='F3F6FA';white='FFFFFF';purple='8056A8';teal='008878';grid='DFE7ED'
NS='http://schemas.openxmlformats.org/presentationml/2006/main';A='http://schemas.openxmlformats.org/drawingml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships';PKG='http://schemas.openxmlformats.org/package/2006/relationships'
S=5080;parts=[];svg=[];serial=1
# SVG and PowerPoint share the same scene; all text, points and bars are editable.
def shape(x,y,w,h,fill=None,label='',size=24,color=text,bold=False,kind='rect',stroke=None):
 global serial
 serial+=1
 def solid(c):return f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
 fillxml=solid(fill) if fill else '<a:noFill/>'
 line=f'<a:ln w="6350">{solid(stroke)}</a:ln>' if stroke else '<a:ln><a:noFill/></a:ln>'
 body=''
 if label:
  body=f'<p:txBody><a:bodyPr wrap="none" lIns="0" rIns="0" tIns="0" bIns="0" anchor="t"/><a:lstStyle/><a:p><a:pPr/><a:r><a:rPr lang="en-US" sz="{round(size*40)}" b="{int(bold)}">{solid(color)}<a:latin typeface="Arial"/></a:rPr><a:t>{E(label)}</a:t></a:r><a:endParaRPr/></a:p></p:txBody>'
 geom={'rect':'rect','round':'roundRect','circle':'ellipse'}[kind]
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{serial}" name="{E(label[:65]) if label else geom}"/><p:cNvSpPr txBox="{int(bool(label))}"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{round(x*S)}" y="{round(y*S)}"/><a:ext cx="{round(w*S)}" cy="{round(h*S)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fillxml}{line}</p:spPr>{body}</p:sp>')
 if fill or stroke:
  attrs=f'fill="#{fill}"' if fill else 'fill="none"'
  if stroke:attrs+=f' stroke="#{stroke}" stroke-width="1.25"'
  if kind=='circle':svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" {attrs}/>')
  else:svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{14 if kind=="round" else 0}" {attrs}/>')
 if label:svg.append(f'<text x="{x}" y="{y+size*.94}" font-size="{size}" font-weight="{700 if bold else 400}" fill="#{color}">{E(label)}</text>')
def txt(x,y,s,n=24,c=text,b=False):shape(x,y,2300-x,n*1.4,label=s,size=n,color=c,bold=b)
def line(x1,y1,x2,y2,c=grid,width=2):
 # Axis/grid lines are thin editable rectangles.
 shape(min(x1,x2),min(y1,y2),max(abs(x2-x1),width),max(abs(y2-y1),width),c)
def dot(x,y,c,r=5):shape(x-r,y-r,2*r,2*r,c,kind='circle',stroke=white)
shape(0,0,2400,1350,bg);shape(0,0,2400,207,white)
txt(72,30,'CURRENT RESEARCH  /  COMPUTATIONAL ANTIBODY DESIGN',24,blue,True)
txt(72,75,'AI-designed biparatopic antibodies against B7-H3',58,navy,True)
txt(74,151,'Two distinct epitopes on human CD276  |  Goal: same-antigen engagement in a 1A + 1B IgG-Fc',30,muted)
txt(74,201,'RF2 SCREENING LIBRARY:  1,176 Arm A models   +   1,188 Arm B models   =   2,364 models',25,text,True)
cards=[('01  TARGET & EPITOPES','Human 4Ig B7-H3','A: IgV1  •  B: IgC1'),('02  DESIGN & SCREEN','RFantibody + ProteinMPNN','RF2 geometry + interface QC'),('03  ARM VALIDATION','AlphaFold 3','2 seeds × 2 samples per arm'),('04  DUAL-ARM MODELING','40 Arm A × 29 Arm B','Shared full 4Ig target'),('05  NEXT: IgG & ASSAYS','Pairing + Fc engineering','Binding, cis engagement, function')]
for i,(a,b,c) in enumerate(cards):
 x=72+i*455;shape(x,238,434,156,white,kind='round')
 txt(x+19,257,a,22,blue,True);txt(x+19,300,b,24,text,True);txt(x+19,345,c,21,muted)
for x,num,label,detail in [(72,'69','RF2-shortlisted arm candidates','40 Arm A + 29 Arm B'),(838,'276','AF3 arm-validation predictions','69 inputs × 4 stochastic samples'),(1604,'1,160','A+B pairwise inputs','164 completed • snapshot: 18 Oct 2026')]:
 hi=x==1604;fg=white if hi else navy
 shape(x,420,724,155,blue if hi else white,kind='round')
 txt(x+24,432,num,53,fg,True);txt(x+24,497,label,27,fg,True);txt(x+24,540,detail,21,'D7EAF6' if hi else muted)
txt(74,593,'ARM-LEVEL EVIDENCE  •  Cropped-target AF3 validation cohort; independent of the later full-target pair campaign',24,text,True)
dot(85,648,purple,8);txt(104,631,'Arm A: IgV1 FG loop (n = 40)',23)
dot(540,648,teal,8);txt(559,631,'Arm B: IgC1 patch (n = 29)',23)
txt(1500,631,'Computational shortlist ≠ confirmed binding',23,muted)
shape(62,674,1100,550,white,kind='round');shape(1238,674,1100,550,white,kind='round')
txt(88,687,'Antibody pairing vs. target-interface confidence',28,text,True)
txt(88,731,'Each point: one arm candidate, mean of four AF3 samples',22,muted)
# Left: two chain-pair ipTM scores, not global ipTM or an affinity estimate.
x0,x1,y0,y1=190,1110,1088,800
for v in [.75,.8,.85,.9,.95,1.0]:
 x=x0+(v-.75)/.25*(x1-x0);line(x,y1,x,y0);txt(x-20,y0+12,f'{v:.2f}',21,muted)
for v in [0,.1,.2,.3,.4]:
 y=y0-v/.4*(y0-y1);line(x0,y,x1,y);txt(x0-62,y-13,f'{v:.1f}',21,muted)
line(x0,y0,x1,y0,muted);line(x0,y1,x0,y0,muted)
for r in rows:
 x=x0+(float(r['mean_HL_iptm'])-.75)/.25*(x1-x0)
 y=y0-float(r['mean_HT_iptm'])/.4*(y0-y1)
 assert x0<=x<=x1 and y1<=y<=y0
 dot(x,y,purple if r['arm']=='A' else teal)
txt(111,770,'H–target ipTM',22,text,True)
txt(450,1131,'H–L ipTM (VH–VL pairing)',24,text,True)
txt(88,1180,'Strong H–L pairing; low target-interface confidence remains.',22,muted)
# Right: geometric selected-residue contacts, not binding validation.
txt(1264,687,'Recovery of the selected epitope',28,text,True)
txt(1264,731,'≥2 selected residues contacted within 4.5 Å; fraction of inputs',22,muted)
bottom,top=1088,800;left,right=1365,2275
for v in [0,25,50,75,100]:
 y=bottom-v/100*(bottom-top);line(left,y,right,y);txt(left-65,y-13,str(v)+'%',21,muted)
line(left,bottom,right,bottom,muted)
summary={}
for arm in 'AB':
 subset=[r for r in rows if r['arm']==arm]
 summary[arm]={'inputs':len(subset),'contact_ge2_any_sample':sum(int(r['samples_contact_ge2'])>0 for r in subset),'contact_ge2_all_four':sum(int(r['samples_contact_ge2'])==4 for r in subset)}
for group,(key,label,center) in enumerate([('contact_ge2_any_sample','At least 1 of 4 samples',1585),('contact_ge2_all_four','All 4 samples',2050)]):
 for arm,dx,col in [('A',-93,purple),('B',17,teal)]:
  val=summary[arm][key];n=summary[arm]['inputs'];h=val/n*(bottom-top);x=center+dx
  if h:shape(x,bottom-h,82,h,col)
  txt(x-8,bottom-h-36,f'{val}/{n}',23,col,True)
 txt(center-150,1131,label,23,text,True)
txt(1264,1180,'Contact recovery is variable; it does not establish affinity.',22,muted)
shape(0,1230,2400,120,'E7EEF4')
txt(73,1246,'NEXT MILESTONE: validate simultaneous A+B binding on one B7-H3 molecule, assemble IgG-Fc and test experimentally.',25,text,True)
txt(73,1290,'Pipeline: RFantibody (RFdiffusion) → ProteinMPNN → RF2 → AlphaFold 3   |   Recorded results through 18 October 2026',23,muted)
(P/f'{STEM}.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2400" height="1350" viewBox="0 0 2400 1350"><g font-family="Arial, Liberation Sans, sans-serif">'+''.join(svg)+'</g></svg>')
subprocess.run(['rsvg-convert','-o',str(P/f'{STEM}.png'),str(P/f'{STEM}.svg')],check=True)
subprocess.run(['rsvg-convert','-f','pdf','-o',str(P/f'{STEM}.pdf'),str(P/f'{STEM}.svg')],check=True)
def rels(entries):return f'<Relationships xmlns="{PKG}">'+''.join(f'<Relationship Id="{i}" Type="{R}/{t}" Target="{p}"/>' for i,t,p in entries)+'</Relationships>'
empty='<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree>'
files={
'[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'+''.join(f'<Override PartName="/ppt/{path}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.{typ}+xml"/>' for path,typ in [('presentation','presentation.main'),('slides/slide1','slide'),('slideMasters/slideMaster1','slideMaster'),('slideLayouts/slideLayout1','slideLayout')])+'</Types>',
'_rels/.rels':rels([('rId1','officeDocument','ppt/presentation.xml')]),
'ppt/presentation.xml':f'<p:presentation xmlns:p="{NS}" xmlns:r="{R}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId2"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>',
'ppt/_rels/presentation.xml.rels':rels([('rId1','slide','slides/slide1.xml'),('rId2','slideMaster','slideMasters/slideMaster1.xml')]),
'ppt/slides/slide1.xml':f'<p:sld xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld>{empty.replace("<p:grpSpPr/>","<p:grpSpPr/>"+"".join(parts))}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>',
'ppt/slides/_rels/slide1.xml.rels':rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml')]),
'ppt/slideMasters/slideMaster1.xml':f'<p:sldMaster xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld>{empty}</p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles/></p:sldMaster>',
'ppt/slideMasters/_rels/slideMaster1.xml.rels':rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml')]),
'ppt/slideLayouts/slideLayout1.xml':f'<p:sldLayout xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}" type="blank" preserve="1"><p:cSld name="Blank">{empty}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>',
'ppt/slideLayouts/_rels/slideLayout1.xml.rels':rels([('rId1','slideMaster','../slideMasters/slideMaster1.xml')])}
with zipfile.ZipFile(P/f'{STEM}_editable.pptx','w',zipfile.ZIP_DEFLATED) as z:
 for path,content in files.items():ET.fromstring(content);z.writestr(path,content)
with (P/'00_05_arm_validation_plot_data.csv').open('w',newline='') as f:
 keys=['arm','input','n_samples','mean_HL_iptm','mean_HT_iptm','samples_contact_ge2']
 w=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");w.writeheader();w.writerows({k:r[k] for k in keys} for r in rows)
summary.update({'rf2_screened_models':counts,'af3_arm_predictions':276,'pair_inputs':1160,'pair_completed_snapshot_20261018':164,'pair_completion_is_not_scientific_acceptance':True})
(P/'00_05_overview_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));print('Native editable shapes:',serial-1)
