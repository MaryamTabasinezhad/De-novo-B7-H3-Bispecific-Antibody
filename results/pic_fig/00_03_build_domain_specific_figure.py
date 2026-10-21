#!/usr/bin/env python3
"""Precise SVG corrections of the user-selected 00_01 mechanism illustration.

Run from any directory; requires existing rsvg-convert and Pillow for inspection.
Domain positions are drawing coordinates, not structure-derived epitope mappings.
"""
from pathlib import Path
import base64, json, math, subprocess
from xml.sax.saxutils import escape
from PIL import Image
P=Path(__file__).resolve().parent
source=P/'00_01_b7h3_biparatopic_mechanisms.png'
W,H=1191,1321
GREEN='#009c88';PURPLE='#9144de';GRAY='#8d939b';INK='#29343c'
svg=[];targets={};antibodies=[]

def add(s):svg.append(s)
def rect(x,y,w,h,fill='white'):
 add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>')
def path(d,stroke='#778590',width=2,fill='none',extra=''):
 add(f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
def circle(x,y,r,fill,stroke='none',sw=1):
 add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def text(x,y,s,size=16,fill=INK,anchor='start',bold=False):
 add(f'<text x="{x}" y="{y}" font-family="Liberation Sans,Arial,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{fill}">{escape(s)}</text>')
def membrane(d):
 path(d,'#c8d7e4',15);path(d,'#7ba7cc',2)
 # Parallel bilayer highlight, avoiding a dense texture in the small panels.
 path(d,'#e8f1f8',7)
def antigen(name,x,y,step=27,r=10.5,direction=(0,1),anchor_extension=42):
 """(x,y) is distal domain 1. Vector points toward cell membrane."""
 dx,dy=direction
 domains=[(x+dx*step*i,y+dy*step*i) for i in range(4)]
 start=domains[-1];end=(start[0]+dx*anchor_extension,start[1]+dy*anchor_extension)
 path(f'M {start[0]},{start[1]} L {end[0]},{end[1]}','#467caa',3)
 circle(*end,3.2,'#8dc9f8','#426c96',.8)
 for i,(cx,cy) in reversed(list(enumerate(domains))):
  add(f'<ellipse id="{name}_domain_{i+1}" cx="{cx}" cy="{cy}" rx="{r}" ry="{r+1.3}" fill="url(#antigenBlue)" stroke="#286bb7" stroke-width="1.4"/>')
 targets[name]={'domains':domains,'direction':direction,'radius':r}
 return domains

def contact(target,domain,side):
 """Endpoint lies on bead perimeter: an explicit, visible domain contact."""
 t=targets[target];cx,cy=t['domains'][domain-1]
 sx,sy=side;norm=math.hypot(sx,sy)
 return (cx+sx/norm*t['radius'],cy+sy/norm*(t['radius']+1.3))

def paired_branch(start,end,color,width=3.6):
 dx=end[0]-start[0];dy=end[1]-start[1];length=math.hypot(dx,dy)
 nx=-dy/length;ny=dx/length
 for off in [-2.5,2.5]:
  a=(start[0]+nx*off,start[1]+ny*off);b=(end[0]+nx*off,end[1]+ny*off)
  d=f'M {a[0]},{a[1]} L {b[0]},{b[1]}'
  path(d,'#4b5360',width+1.8);path(d,color,width)

def antibody(name,hinge,green,purple,fc,green_binding=None,purple_binding=None,fc_binding=None):
 # Each intact antibody is constructed with exactly one branch of each type.
 for color,binding,expected in [(GREEN,green_binding,1),(PURPLE,purple_binding,3)]:
  if binding:
   target,domain,side=binding
   assert domain==expected,(name,color,domain)
   endpoint=green if color==GREEN else purple
   assert math.dist(endpoint,contact(target,domain,side))<1e-6
 paired_branch(hinge,fc,GRAY,4.0)
 paired_branch(hinge,green,GREEN)
 paired_branch(hinge,purple,PURPLE)
 circle(*hinge,4.5,'#a4a9ad','#4b5360',1)
 antibodies.append({'id':name,'hinge':hinge,'green_tip':green,'purple_tip':purple,'fc_tip':fc,
  'green_binding':green_binding,'purple_binding':purple_binding,'fc_binding':fc_binding})

def patch(t,domain,side,color):
 cx,cy=contact(t,domain,side);circle(cx,cy,3.2,color,'white',.7)

def bound_antibody(name,hinge,g,p,fc,fc_binding=None):
 # g and p are (target,domain,side), or explicit free endpoints.
 gb=g if isinstance(g[0],str) else None;pb=p if isinstance(p[0],str) else None
 gt=contact(*g) if gb else g;pt=contact(*p) if pb else p
 if gb:patch(*g,GREEN)
 if pb:patch(*p,PURPLE)
 antibody(name,hinge,gt,pt,fc,gb,pb,fc_binding)

# Original entire canvas; only selected antibody-containing interiors are replaced.
encoded=base64.b64encode(source.read_bytes()).decode()
add(f'<image width="{W}" height="{H}" href="data:image/png;base64,{encoded}"/>')
# A uniform antibody in the top overview.
rect(512,36,137,126)
antibody('overview',(580,94),(543,53),(617,53),(580,147))
# Compact color/domain key in the free strip above the mechanism panels.
rect(302,324,588,27)
text(380,343,'Green Fab: domain 1',15,GREEN,bold=True)
text(613,343,'Purple Fab: domain 3',15,PURPLE,bold=True)

# CLUSTERING — intermolecular bridging at different domain heights.
rect(13,399,373,226)
membrane('M 22,583 Q 200,542 379,583')
for i,x in enumerate([78,199,320]):antigen(f'cluster_{i}',x,447,27,10.8,anchor_extension=42)
# Each green binds a distal site on one antigen and purple the third site on its neighbor.
bound_antibody('cluster_ab_1',(137,467),('cluster_0',1,(1,-.7)),('cluster_1',3,(-1,0)),(151,414))
bound_antibody('cluster_ab_2',(258,467),('cluster_1',1,(1,-.7)),('cluster_2',3,(-1,0)),(273,414))
# The small explanatory inset is domain-order information, not a binding metric.
rect(25,590,345,24)
text(198,607,'Domains counted from outer tip toward membrane',11,'#657584',anchor='middle')

# INTERNALIZATION — a clear, intact bridged complex inside a membrane pit.
rect(13,701,373,237)
membrane('M 23,779 C 80,778 84,897 199,899 C 315,897 319,779 378,779')
antigen('internal_left',118,765,25,10.5,anchor_extension=23)
antigen('internal_right',266,765,25,10.5,anchor_extension=23)
bound_antibody('internal_ab',(185,783),('internal_left',1,(1,-.4)),('internal_right',3,(-1,0)),(210,716))
# Short endocytic direction arrow.
path('M 199,866 L 199,884','#657584',2,extra='marker-end="url(#arrowGray)"')

# PUTATIVE INTERACTION BLOCKADE — cis binding uses the same two domain assignments.
rect(414,398,363,228)
membrane('M 424,580 Q 600,537 768,580')
antigen('blockade',508,447,26,10.8,anchor_extension=44)
bound_antibody('blockade_ab',(564,470),('blockade',1,(.8,-.7)),('blockade',3,(1,0)),(603,417))
# Unknown partner, not an asserted HER-family receptor.
path('M 686,539 L 686,576','#d99250',3)
for i,(x,y) in enumerate([(684,531),(689,507),(678,484),(671,461),(658,439)]):
 circle(x,y,8.5,'url(#partnerOrange)','#ee9139',1.2)
text(704,470,'Partner',15);text(704,489,'unknown',15)
path('M 590,512 L 660,512','#6b747b',2,extra='stroke-dasharray="4 4"')
path('M 617,503 L 633,520 M 633,503 L 617,520','#ba3434',3)

# PUTATIVE SIGNALING MODULATION — dual domain binding, no kinase attribution.
rect(414,699,363,239)
membrane('M 424,851 Q 598,813 768,851')
antigen('modulation',547,735,23.5,10.2,anchor_extension=26)
bound_antibody('modulation_ab',(603,757),('modulation',1,(1,-.4)),('modulation',3,(1,0)),(647,709))
path('M 550,855 L 550,895','#67717a',2,extra='stroke-dasharray="4 4" marker-end="url(#arrowGray)"')
path('M 540,875 L 560,875','#b43535',3)
text(594,918,'Context dependent',16,anchor='middle')

# ADCC / ADCP — two Fab contacts on B7-H3; only Fc engages the effector receptor.
def effector_panel(y0,name,cell_fill,cell_stroke):
 rect(807,399 if name=='adcc' else 701,371,227 if name=='adcc' else 237)
 text(817,y0-10,'Tumor cell',16)
 text(1114,y0-10,'NK cell' if name=='adcc' else 'Macrophage',16,anchor='middle')
 # Tumor and effector membranes retain the left/right arrangement of the reference.
 path(f'M 817,{y0} C 873,{y0+50} 873,{y0+140} 817,{y0+190} L 814,{y0+190} L 814,{y0} Z','#9db8cf',2,'#eef5fb')
 path(f'M 1140,{y0} C 1084,{y0+57} 1084,{y0+139} 1140,{y0+191} L 1171,{y0+191} L 1171,{y0} Z',cell_stroke,2,cell_fill)
 # Small interior organelles are illustrative, not measured data.
 for x,yy,r in [(1150,35,9),(1137,74,6),(1151,113,11),(1148,157,7)]:
  circle(x,y0+yy,r,cell_stroke,'none')
 target=f'{name}_target';antigen(target,978,y0+94,27,10.8,direction=(-1,0),anchor_extension=40)
 fc=(1025,y0+33)
 bound_antibody(f'{name}_ab',(951,y0+38),(target,1,(0,-1)),(target,3,(0,-1)),fc,fc_binding='FcγR')
 # Receptor U embraces only the gray Fc endpoint and has a separate cellward stalk.
 path(f'M 1019,{y0+22} L 1019,{y0+39} Q 1027,{y0+48} 1035,{y0+39} L 1035,{y0+22}',GREEN,7)
 path(f'M 1027,{y0+45} L 1111,{y0+70}',GREEN,7)
 text(1041,y0+96,'FcγR',16)
 if name=='adcc':
  for i,(x,dy) in enumerate([(1050,114),(1031,135),(1060,148),(1024,161)]):circle(x,y0+dy,4.8,'#ffb22c','#ec921b',.7)
  path(f'M 1090,{y0+154} Q 1045,{y0+180} 1001,{y0+152}','#6b747b',3,extra='marker-end="url(#arrowGray)"')
 else:
  path(f'M 1109,{y0+137} Q 1070,{y0+166} 1020,{y0+162}','#8a7881',3,extra='marker-end="url(#arrowGray)"')
effector_panel(425,'adcc','#e9eafd','#babee9')
effector_panel(733,'adcp','#faeaf4','#d8aac7')

# CDC — two crosslinking antibodies with C1q attached to gray Fc only.
rect(807,1005,371,247)
membrane('M 817,1211 Q 989,1169 1168,1211')
for i,x in enumerate([849,929,1009,1089]):antigen(f'cdc_{i}',x,1090,25,9.5,anchor_extension=43)
bound_antibody('cdc_ab_1',(890,1090),('cdc_0',1,(.6,-.8)),('cdc_1',3,(-1,0)),(919,1048),fc_binding='C1q')
bound_antibody('cdc_ab_2',(1049,1090),('cdc_2',1,(.6,-.8)),('cdc_3',3,(-1,0)),(1030,1048),fc_binding='C1q')
# C1q bouquet: schematic multivalent Fc recognition, not atomic stoichiometry.
for end in [(919,1048),(941,1058),(1007,1058),(1030,1048)]:
 path(f'M 975,1019 Q 975,1035 {end[0]},{end[1]}','#ad5a86',5)
 circle(*end,7.5,'#d18aad','#9f4f79',1)
path('M 975,1009 L 975,1025','#ad5a86',9)
text(994,1024,'C1q',16)
# Membrane attack complex at right.
for x in [1121,1129,1137,1145,1153]:
 path(f'M {x},1218 L {x+7},1179','#205c8a',9)
 path(f'M {x},1218 L {x+7},1179','#3d9bce',5)
text(1120,1166,'MAC',16)

# Validate all bound Fab endpoints against the explicit domain geometry.
assert len(antibodies)==10
for ab in antibodies:
 for color,expected in [('green',1),('purple',3)]:
  binding=ab[color+'_binding']
  if binding:
   t,domain,side=binding
   assert len(targets[t]['domains'])==4 and domain==expected
   assert math.dist(ab[color+'_tip'],contact(t,domain,side))<1e-6
assert all(ab['green_binding'] and ab['purple_binding'] for ab in antibodies if ab['id']!='overview')

defs='''<defs>
<radialGradient id="antigenBlue" cx="30%" cy="24%" r="78%"><stop offset="0" stop-color="#c3f1ff"/><stop offset=".48" stop-color="#7bc4ff"/><stop offset="1" stop-color="#448ae8"/></radialGradient>
<radialGradient id="partnerOrange" cx="30%" cy="20%"><stop offset="0" stop-color="#fff0c4"/><stop offset="1" stop-color="#ffc36f"/></radialGradient>
<marker id="arrowGray" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 L 10,5 L 0,10 Z" fill="#657584"/></marker>
</defs>'''
stem='00_03_b7h3_domain_specific_fab_binding'
svgfile=P/(stem+'.svg')
svgfile.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>B7-H3 biparatopic antibody: green domain 1, purple domain 3</title>{defs}'+''.join(svg)+'</svg>')
pngfile=P/(stem+'.png')
subprocess.run(['rsvg-convert','-w',str(W*2),'-h',str(H*2),'-o',str(pngfile),str(svgfile)],check=True)
(P/'00_03_fab_domain_geometry.json').write_text(json.dumps({'convention':'schematic extracellular domains numbered distal tip (1) to membrane-proximal (4)', 'source':source.name,'targets':targets,'antibodies':antibodies,'not_structure_derived':True},indent=2)+'\n')
with Image.open(pngfile) as im:
 assert im.size==(W*2,H*2);im.verify()
print('Saved',pngfile.name,'and editable overlay SVG; verified',len(antibodies),'intact antibodies,',len(targets),'four-domain antigens; green=1, purple=3.')
