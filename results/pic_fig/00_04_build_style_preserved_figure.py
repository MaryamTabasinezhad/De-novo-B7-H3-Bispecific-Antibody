#!/usr/bin/env python3
"""Localized scientific corrections, preserving the artwork of figure 00_01.

Reuses the explicit-domain endpoint method of 00_03, but edits local molecular foregrounds and repairs antigen domain counts rather
than replacing entire panel interiors or the original cell/membrane artwork.
"""
from pathlib import Path
from collections import deque
from io import BytesIO
import base64,json,math,subprocess
from PIL import Image,ImageDraw,ImageFilter
P=Path(__file__).resolve().parent
stem='00_04_b7h3_original_style_corrected_binding'
source=P/'00_01_b7h3_biparatopic_mechanisms.png'
im=Image.open(source).convert('RGB');W,H=im.size
pix=im.load();mask=Image.new('L',im.size);mp=mask.load()

def blue(rgb):
 r,g,b=rgb;return b-r>22 and b-g>12 and g-r>10

def original_antibody(rgb):
 r,g,b=rgb
 return (max(rgb)-min(rgb)<43 and 35<min(rgb) and max(rgb)<248) or (b>r+12 and r>g+22) or (g>r+25 and g>b-15)

def pit_height(x):
 points=[(20,777),(60,782),(80,808),(100,844),(120,866),(160,887),(200,899),(240,888),(280,865),(300,839),(320,811),(340,787),(380,778)]
 for (x1,y1),(x2,y2) in zip(points,points[1:]):
  if x1<=x<=x2:return y1+(y2-y1)*(x-x1)/(x2-x1)
 return 780

kept_beads=[(89,464),(86,486),(84,509),(83,532),(166,463),(159,486),(152,508),(147,531),(216,479),(215,499),(215,519),(215,540),(290,480),(290,502),(289,524),(290,545),(361,480),(355,501),(348,522),(343,542),(104,739),(101,759),(94,780),(88,800),(218,806),(224,831),(230,858),(236,884),(519,466),(521,487),(522,508),(523,529),(896,448),(901,470),(901,493),(894,516),(899,748),(903,771),(903,794),(897,815)]
def on_kept_bead(x,y):return any(((x-cx)/14)**2+((y-cy)/15)**2<=1 for cx,cy in kept_beads)
regions=[('cluster',(20,409,374,538)),('internal',(61,710,335,833)),
 ('blockade',(510,408,613,502)),('modulation',(549,698,643,797)),
 ('adcc',(885,426,1018,516)),('adcp',(885,726,1018,823)),
 ('cdc',(860,1082,1093,1174))]
for name,(x1,y1,x2,y2) in regions:
 for y in range(y1,y2):
  for x in range(x1,x2):
   if name=='cluster' and 45<=x<=105 and 421<=y<=439:continue # original target label
   if name=='internal' and y>=pit_height(x)-12:continue # retain original lipid bilayer
   if name=='adcc' and x>=1003 and y>=476 and pix[x,y][1]>pix[x,y][0]+12 and pix[x,y][1]>pix[x,y][2]-15:continue # original FcγR
   if name=='adcp' and x>=1003 and y>=785 and pix[x,y][1]>pix[x,y][0]+12 and pix[x,y][1]>pix[x,y][2]-15:continue
   if name=='cdc':
    r,g,b=pix[x,y]
    if r>b+8 and r>g+20:continue # preserve the original C1q bouquet
   if not (blue(pix[x,y]) and on_kept_bead(x,y)):mp[x,y]=255
# Repair source antigens that had fewer than four extracellular blue domains.
repair=Image.new('L',im.size);rd=ImageDraw.Draw(repair)
rd.polygon([(173,802),(202,808),(183,885),(148,888),(155,839)],fill=255)
rd.rectangle((296,736,327,817),fill=255)
rd.rectangle((550,725,580,795),fill=255)
for cx,cy in kept_beads:rd.ellipse((cx-14,cy-15,cx+14,cy+15),fill=255)
for box in [(853,1120,891,1184),(914,1141,943,1186),(965,1115,994,1184),(996,1140,1024,1186),(1036,1115,1079,1185)]:rd.rectangle(box,fill=255)
mp=ImageDraw.Draw(mask);mp.bitmap((0,0),repair,fill=255)
# A small halo removes antialiased gray/colored edges; protect unchanged antigen
# and membrane pixels unless they belong to the explicit four-domain repair.
mask=mask.filter(ImageFilter.MaxFilter(3));mp=mask.load();rp=repair.load()
for y in range(H):
 for x in range(W):
  if mp[x,y] and blue(pix[x,y]) and on_kept_bead(x,y) and not rp[x,y]:mp[x,y]=0
  if mp[x,y] and 45<=x<=105 and 421<=y<=439:mp[x,y]=0
  if mp[x,y] and 61<=x<=335 and 710<=y<=899 and y>=pit_height(x)-10 and not rp[x,y]:mp[x,y]=0
  if mp[x,y] and 900<=x<=1035 and 1005<=y<=1110:
   r,g,b=pix[x,y]
   if r>g+12 and b>g+8 and b<r+30:mp[x,y]=0
  if mp[x,y] and 815<=x<=1100 and 1182<=y<=1250:mp[x,y]=0
  if mp[x,y] and ((x>=1003 and 476<=y<=518) or (x>=1003 and 785<=y<=825)) and x<=1022 and pix[x,y][1]>pix[x,y][0]+12 and pix[x,y][1]>pix[x,y][2]-15:mp[x,y]=0
# Boundary propagation restores the local white/pale background without broad
# blank rectangles. All unmasked source pixels are retained exactly.
clean=im.copy();cp=clean.load();pending=set()
for y in range(H):
 for x in range(W):
  if mp[x,y]:pending.add((x,y))
q=deque()
for x,y in pending:
 if any(0<=x+dx<W and 0<=y+dy<H and not mp[x+dx,y+dy] for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):q.append((x,y))
filled=set()
while q:
 x,y=q.popleft()
 if (x,y) in filled:continue
 near=[]
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
  a,b=x+dx,y+dy
  if 0<=a<W and 0<=b<H and ((a,b) not in pending or (a,b) in filled):near.append(cp[a,b])
 if not near:q.append((x,y));continue
 # Antigen/antibody/cell edges must not bleed into the restored background.
 pale=[v for v in near if min(v)>228 and max(v)-min(v)<18]
 chosen=pale or [(255,255,255)]
 cp[x,y]=tuple(round(sum(v[c] for v in chosen)/len(chosen)) for c in range(3));filled.add((x,y))
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  a,b=x+dx,y+dy
  if (a,b) in pending and (a,b) not in filled:q.append((a,b))
assert len(filled)==len(pending)
# Verify the scope of the edit on the source raster, before adding new vectors.
assert all(cp[x,y]==pix[x,y] for y in range(H) for x in range(W) if not mp[x,y])

svg=[];defs=[];targets={};abs=[];serial=0
GREEN='#009d8b';PURPLE='#9c4be8'
def add(s):svg.append(s)
def image_data(image):
 b=BytesIO();image.save(b,format='PNG');return base64.b64encode(b.getvalue()).decode()
add(f'<image width="{W}" height="{H}" href="data:image/png;base64,{image_data(clean)}"/>')
# Shaded blue domains match the original illustration's visual material.
defs.append('<radialGradient id="blueDomain" cx="28%" cy="22%" r="85%"><stop offset="0" stop-color="#c6ecff"/><stop offset=".30" stop-color="#93caff"/><stop offset=".68" stop-color="#63a6ee"/><stop offset="1" stop-color="#427fcb"/></radialGradient>')
def set_target(name,points,rx=10.5,ry=11.5,redraw=False):
 assert len(points)==4
 targets[name]={'domains':points,'rx':rx,'ry':ry,'redrawn':True}
 # Retain the original membrane anchors, joining the last corrected bead locally.
 x,y=points[-1];px,py=points[-2];dx,dy=x-px,y-py;n=math.hypot(dx,dy)
 ex,ey=x+dx/n*20,y+dy/n*20
 add(f'<path d="M {x},{y} L {ex},{ey}" fill="none" stroke="#3678b7" stroke-width="3.6"/>')
 add(f'<path d="M {x-1},{y} L {ex-1},{ey}" fill="none" stroke="#87bdf0" stroke-width="1.6"/>')
 for i,(x,y) in enumerate(points):
  add(f'<ellipse id="{name}_domain_{i+1}" cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#blueDomain)" stroke="#3978bb" stroke-width="1.25"/>')
def tip(target,domain,side):
 t=targets[target];x,y=t['domains'][domain-1];dx,dy=side;n=math.hypot(dx,dy)
 return x+dx/n*t['rx'],y+dy/n*t['ry']
def tube(a,b,color='gray',width=4.4):
 global serial
 serial+=1;key=f'material_{serial}'
 dx,dy=b[0]-a[0],b[1]-a[1];n=math.hypot(dx,dy);nx,ny=-dy/n,dx/n
 palette={'gray':['#5c636b','#a7adb4','#eef0f2','#9299a2','#5c6269'],
  'green':['#00675d','#20c8b1','#98f1e3','#009e8d','#00685e'],
  'purple':['#6730ac','#b877f2','#e5c7ff','#a04cdf','#6830ad']}[color]
 defs.append(f'<linearGradient id="{key}" gradientUnits="userSpaceOnUse" x1="{a[0]+nx*width}" y1="{a[1]+ny*width}" x2="{a[0]-nx*width}" y2="{a[1]-ny*width}">'+''.join(f'<stop offset="{i/4}" stop-color="{c}"/>' for i,c in enumerate(palette))+'</linearGradient>')
 for off in [-3.0,3.0]:
  x1,y1=a[0]+nx*off,a[1]+ny*off;x2,y2=b[0]+nx*off,b[1]+ny*off
  d=f'M {x1},{y1} L {x2},{y2}'
  add(f'<path d="{d}" stroke="{palette[0]}" stroke-width="{width+1.5}" stroke-linecap="round"/>')
  add(f'<path d="{d}" stroke="url(#{key})" stroke-width="{width}" stroke-linecap="round"/>')
def branch(hinge,end,color):
 dx,dy=end[0]-hinge[0],end[1]-hinge[1]
 # Match 00_01: paired gray constant domains and colored distal binding domains.
 a=(hinge[0]+dx*.10,hinge[1]+dy*.10);m=(hinge[0]+dx*.49,hinge[1]+dy*.49)
 c=(hinge[0]+dx*.55,hinge[1]+dy*.55)
 add(f'<path d="M {hinge[0]},{hinge[1]} L {a[0]},{a[1]}" stroke="#727982" stroke-width="2.2" stroke-linecap="round"/>')
 tube(a,m,'gray');tube(c,end,color)
def antibody(name,h,g,p,fc,fc_binding=None):
 gt,gd,gs=g;pt,pd,ps=p
 assert gd==1 and pd==3
 green=tip(*g);purple=tip(*p)
 m=((h[0]+fc[0])/2,(h[1]+fc[1])/2)
 add(f'<path d="M {h[0]},{h[1]} L {h[0]+(fc[0]-h[0])*.13},{h[1]+(fc[1]-h[1])*.13}" stroke="#727982" stroke-width="2.4"/>')
 tube((h[0]+(fc[0]-h[0])*.10,h[1]+(fc[1]-h[1])*.10),m,'gray',4.8)
 tube((h[0]+(fc[0]-h[0])*.57,h[1]+(fc[1]-h[1])*.57),fc,'gray',4.8)
 branch(h,green,'green');branch(h,purple,'purple')
 add(f'<circle cx="{h[0]}" cy="{h[1]}" r="2.5" fill="#9298a0" stroke="#5b636c" stroke-width=".8"/>')
 abs.append({'id':name,'hinge':h,'green':{'target':gt,'domain':gd,'tip':green},'purple':{'target':pt,'domain':pd,'tip':purple},'fc_tip':fc,'fc_binding':fc_binding})
# Existing 00_01 bead positions; four-domain count is retained, not approximated
# from apparent antibody binding height.
for name,points in {
 'c0':[(89,464),(86,486),(84,509),(83,532)],
 'c1':[(166,463),(159,486),(152,508),(147,531)],
 'c2':[(216,479),(215,499),(215,519),(215,540)],
 'c3':[(290,480),(290,502),(289,524),(290,545)],
 'c4':[(361,480),(355,501),(348,522),(343,542)],
 'i0':[(104,739),(101,759),(94,780),(88,800)],
 'i2':[(218,806),(224,831),(230,858),(236,884)],
 'block':[(519,466),(521,487),(522,508),(523,529)],
 'adcc':[(896,448),(901,470),(901,493),(894,516)],
 'adcp':[(899,748),(903,771),(903,794),(897,815)]}.items():set_target(name,points)
set_target('i1',[(182,817),(176,836),(169,855),(163,875)],10.1,10.8,True)
set_target('i3',[(310,748),(312,768),(313,788),(315,808)],9.8,10.5,True)
set_target('mod',[(565,735),(565,755),(566,775),(567,795)],9.6,10.3,True)
for name,points in {
 'd0':[(867,1124),(870,1140),(873,1156),(876,1172)],
 'd1':[(929,1124),(929,1140),(929,1156),(929,1172)],
 'd2':[(979,1124),(979,1140),(979,1156),(979,1172)],
 'd3':[(1009,1124),(1009,1140),(1009,1156),(1009,1172)],
 'd4':[(1065,1124),(1060,1140),(1055,1156),(1050,1172)]}.items():set_target(name,points,8.1,8.7,True)
antibody('cluster_1',(122,464),('c0',1,(.8,-.6)),('c1',3,(-1,0)),(125,417))
antibody('cluster_2',(185,470),('c1',1,(.8,-.6)),('c2',3,(-1,0)),(202,418))
antibody('cluster_3',(253,482),('c2',1,(.8,-.6)),('c3',3,(-1,0)),(257,425))
antibody('cluster_4',(324,481),('c3',1,(.8,-.6)),('c4',3,(-1,0)),(327,426))
antibody('internal_1',(141,773),('i0',1,(.8,-.6)),('i1',3,(-1,0)),(166,725))
antibody('internal_2',(211,787),('i1',1,(.8,-.6)),('i2',3,(-1,0)),(235,737))
antibody('internal_3',(266,767),('i2',1,(.8,-.6)),('i3',3,(-1,0)),(279,716))
antibody('blockade',(572,474),('block',1,(1,-.3)),('block',3,(1,0)),(600,420))
antibody('modulation',(607,756),('mod',1,(1,-.4)),('mod',3,(1,0)),(641,710))
antibody('ADCC',(956,463),('adcc',1,(1,-.5)),('adcc',3,(1,0)),(1019,495),'FcγR')
antibody('ADCP',(957,770),('adcp',1,(1,-.5)),('adcp',3,(1,0)),(1019,802),'FcγR')
antibody('CDC_1',(896,1124),('d0',1,(.8,-.6)),('d1',3,(-1,0)),(915,1085),'C1q')
antibody('CDC_2',(953,1120),('d1',1,(.8,-.6)),('d2',3,(-1,0)),(948,1097),'C1q')
antibody('CDC_3',(994,1120),('d2',1,(.8,-.6)),('d3',3,(-1,0)),(987,1095),'C1q')
antibody('CDC_4',(1037,1120),('d3',1,(.8,-.6)),('d4',3,(-1,0)),(1018,1085),'C1q')
# Source overview antibody, lysosome, cell cycle, labels, cells, bilayers and
# all upper overview artwork are unchanged; the overview already has both colors.
assert len(abs)==15
for ab in abs:
 assert ab['green']['domain']==1 and ab['purple']['domain']==3
 assert len(targets[ab['green']['target']]['domains'])==4
 assert len(targets[ab['purple']['target']]['domains'])==4
svgfile=P/(stem+'.svg')
svgfile.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>Original-style B7-H3 schematic with corrected Fab-domain assignments</title><defs>'+''.join(defs)+'</defs>'+''.join(svg)+'</svg>')
subprocess.run(['rsvg-convert','-w',str(W*2),'-h',str(H*2),'-o',str(P/(stem+'.png')),str(svgfile)],check=True)
(P/'00_04_local_edit_geometry.json').write_text(json.dumps({'source':source.name,'method':'localized foreground cleanup and shaded vector replacement; original cell and membrane artwork retained','modified_background_pixels':len(pending),'all_unmasked_source_pixels_preserved':True,'domain_numbering':'outermost extracellular bead 1 toward membrane bead 4; conceptual only','targets':targets,'antibodies':abs,'overview_antibody':'original unchanged; one green and one purple Fab'},indent=2)+'\n')
with Image.open(P/(stem+'.png')) as result:assert result.size==(W*2,H*2);result.verify()
print('Saved',stem+'.png',';',len(abs),'corrected antibodies; original overview antibody retained; green=domain 1, purple=domain 3.')
