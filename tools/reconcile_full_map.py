"""Apply only visually matched source corrections to existing geographic features.
The full PDF's other coordinates remain in source-page space, not GPS.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
path=root/'web/data/cg-hazards.geojson'
data=json.loads(path.read_text(encoding='utf8'))
source='08102026_FULL MAP DRAFT.pdf, page 1 (user supplied)'
crosswalk={'cg:station/est1':('3.2',False),'cg:station/est2':('3.3',True),
           'cg:station/est3':('3.5',False),'cg:station/est4':('3.6',False)}
for f in data['features']:
    p=f['properties']
    if f['id'] in crosswalk:
        number,proposed=crosswalk[f['id']]
        p.update(source_number=number,proposed=proposed,status='proposed' if proposed else 'shown_existing',
                 classification_source=source,needs_confirmation=True)
    if p['kind']=='shaded_area_meaning_unknown':
        p.update(kind='strong_current_area',classification_source=source,
                 source_label='Area de Fuertes Corrientes / Area of Strong Currents',needs_confirmation=True)
data['properties']['full_map_reconciliation']={
    'source':source,'geographic_positions_changed':False,
    'note':'Four stations matched visually by access roads, bay and headland context. The new PDF supplies numbers and proposal status. The shaded bay is explicitly labeled strong currents. Remaining PDF features are retained in full-map-source.json in page coordinates; they are not registered GPS hazards.'}
path.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
