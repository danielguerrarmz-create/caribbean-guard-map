"""Read-only source inspection and independent image registration for the supplied PDF.
Writes review artifacts only; publishing geometry is a separate step.
"""
import json, math, sys
from pathlib import Path
import cv2
import numpy as np
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/pdf-review'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = Path(sys.argv[1])
page = pymupdf.open(SOURCE)[0]
# Render the vector document at one quarter scale for feature matching.
pix = page.get_pixmap(matrix=pymupdf.Matrix(.25, .25), alpha=False)
scan = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3)
tiles = list((ROOT / 'web/tiles/15').glob('*/*.jpg'))
xs = [int(p.parent.name) for p in tiles]; ys = [int(p.stem) for p in tiles]
x0,y0=min(xs),min(ys)
ref = np.zeros(((max(ys)-y0+1)*256,(max(xs)-x0+1)*256,3),np.uint8)
for p in tiles:
    im=cv2.imread(str(p)); x=(int(p.parent.name)-x0)*256; y=(int(p.stem)-y0)*256
    ref[y:y+256,x:x+256]=cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
def prep(a):
    return cv2.createCLAHE(2,(8,8)).apply(cv2.cvtColor(a,cv2.COLOR_RGB2GRAY))
sift=cv2.SIFT_create(nfeatures=30000,contrastThreshold=.015)
k1,d1=sift.detectAndCompute(prep(scan),None)
k2,d2=sift.detectAndCompute(prep(ref),None)
matcher=cv2.FlannBasedMatcher(dict(algorithm=1,trees=5),dict(checks=80))
matches=[m for m,n in matcher.knnMatch(d1,d2,k=2) if m.distance < .7*n.distance]
src=np.float32([k1[m.queryIdx].pt for m in matches])
dst=np.float32([k2[m.trainIdx].pt for m in matches])
order=np.random.default_rng(7).permutation(len(matches))
hold=order[::5]; train=np.setdiff1d(order,hold)
M,mask=cv2.estimateAffinePartial2D(src[train],dst[train],method=cv2.RANSAC,ransacReprojThreshold=4,maxIters=100000,confidence=.9999)
if M is None: raise RuntimeError('No reliable registration')
proj=cv2.transform(src.reshape(-1,1,2),M).reshape(-1,2)
err=np.linalg.norm(proj-dst,axis=1)*156543.03392*math.cos(math.radians(9.65))/2**15
report={'source':SOURCE.name,'page_size':list(page.rect),'render_scale':.25,
 'reference_zoom':15,'origin_tile':[x0,y0],'affine_render_to_tile_pixels':M.tolist(),
 'matches':len(matches),'training_inliers':int(mask.sum()),
 'holdout_count':len(hold),'holdout_errors_m':err[hold].tolist(),
 'holdout_consistent_count':int((err[hold]<20).sum()),
 'consistent_match_pdf_x_range':(src[err<20,0]*4).tolist(),
 'accepted':bool(mask.sum()>=20 and len(hold)>=5 and (err[hold]<20).mean()>=.8),
 'warning':'Do not publish a transform unless accepted is true. Image registration measures agreement with cached imagery, not surveyed hazard accuracy.'}
(OUT/'registration.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['consistent_match_pdf_x_range','holdout_errors_m']},indent=2))
print('Holdout median/p90 metres', np.median(err[hold]),np.percentile(err[hold],90))
print('Consistent x range', (src[err<20,0].min()*4,src[err<20,0].max()*4))
