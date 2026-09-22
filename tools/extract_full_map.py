"""Extract PDF vectors in source-page coordinates for GPS projection and audit."""
import sys, json, hashlib, math
from pathlib import Path
from collections import Counter
import pymupdf

root=Path(__file__).resolve().parents[1]
source=Path(sys.argv[1]); doc=pymupdf.open(source); page=doc[0]
out=root/'web/data'; out.mkdir(exist_ok=True)
def near(c,t): return c is not None and max(abs(a-b) for a,b in zip(c,t))<.01
red=(1,0,0); orange=(.976,.612,.129); blue=(.071,.357,1); pale=(.627,.753,.976); yellow=(.886,.796,.259)
spans=[]
for block in page.get_text('dict')['blocks']:
    for line in block.get('lines',[]):
        for s in line['spans']:
            if s['bbox'][1] > 430:
                spans.append({'text':s['text'].strip(),'box':list(s['bbox']),'color':s['color']})
def center(r): return [(r[0]+r[2])/2,(r[1]+r[3])/2]
def points(d):
    result=[]
    for item in d['items']:
        kind=item[0]
        if kind=='l': result.extend([list(item[1]),list(item[2])])
        elif kind=='c':
            a,b,c,e=[list(p) for p in item[1:]]
            for j in range(13):
                t=j/12
                result.append([(1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*e[k] for k in range(2)])
    return [p for i,p in enumerate(result) if i==0 or p!=result[i-1]]
drawings=page.get_drawings()
# The PDF stores each dashed rip shaft and its filled triangular head as
# separate drawings. Some other red dashed marks have no head, and a few
# shafts run backward in PDF path order. Match the head before classifying or
# orienting a current; a 15-page-unit tolerance is smaller than the 30-unit
# head itself and avoids matching nearby arrows.
heads=[]
for drawing in drawings:
    box=drawing['rect']
    if near(drawing['fill'],red) and box.width<45 and box.height<45:
        heads.append(center(list(box)))
features=[]
for d in drawings:
    r=list(d['rect']); x,y=center(r)
    if y<430 and x>10900: continue # legend samples are not map features
    col,fill,typ=d['color'],d['fill'],d['type']
    kind=None; coords=None
    if near(col,red) and typ=='s':
        candidate=points(d)
        if candidate and heads:
            nearest=min((math.dist(endpoint,head),side)
                        for side,endpoint in enumerate((candidate[0],candidate[-1]))
                        for head in heads)
            if nearest[0]<15:
                kind='rip_current'
                coords=candidate[::-1] if nearest[1]==0 else candidate
    elif near(fill,orange) and typ=='f': kind='rescue_station'
    elif near(col,orange) and typ=='fs': kind='proposed_rescue_station'
    elif near(col,red) and near(fill,(1,1,1)): kind='proposed_cg_station'
    elif near(fill,red) and typ=='f' and d['rect'].width>35 and d['rect'].height>35:
        kind='unclassified_facility'
    elif near(fill,yellow): kind='location'
    elif near(col,blue): kind='main_road';coords=points(d)
    elif near(col,pale): kind='pedestrian' if d['dashes']!='[] 0' else 'side_road'; coords=points(d)
    elif near(fill,(.937,.329,.329)):kind='strong_current_area';coords=points(d)
    if kind is None:continue
    number=None; name=None
    if kind in ['rescue_station','proposed_rescue_station']:
        candidates=[s for s in spans if s['text'].replace('.','').isdigit() and math.dist(center(s['box']),[x,y])<80]
        if candidates:number=min(candidates,key=lambda s:math.dist(center(s['box']),[x,y]))['text']
    if kind=='location':
        candidates=[s for s in spans if s['text'] and not s['text'].replace('.','').isdigit() and math.dist(center(s['box']),[x,y])<180]
        if candidates:name=min(candidates,key=lambda s:math.dist(center(s['box']),[x,y]))['text']
    features.append({'id':f'pdf:{kind}/{d["seqno"]}', 'kind':kind,'point':[x,y],
                     'coordinates':coords,'number':number,'name':name,'source_page':1,
                     'authored':'sheet','reviewed':None,'needs_confirmation':True})
counts=dict(Counter(f['kind'] for f in features))
stations=Counter(f['number'] for f in features if 'rescue_station' in f['kind'])
data={'source':source.name,'sha256':hashlib.file_digest(source.open('rb'),'sha256').hexdigest(),
      'coordinate_system':'PDF page points; not latitude/longitude','width':page.rect.width,'height':page.rect.height,
      'image_rect':list(page.get_image_rects(page.get_images()[0][0])[0]),
      'counts':counts,'duplicate_station_labels':[k for k,v in stations.items() if v>1],
      'features':features,'labels':spans,
      'note':'Draft-source annotations. Station symbols do not confirm staffing or present equipment. Do not use page coordinates as GPS.'}
(out/'full-map-source.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print(json.dumps({'counts':counts,'duplicate_station_labels':data['duplicate_station_labels'],'features':len(features)},indent=2))
