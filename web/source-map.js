/* Source-page coordinates deliberately use CRS.Simple, never WGS84.
   This view preserves document placement while geographic registration is pending. */
let lang=navigator.language.startsWith('es')?'es':'en';
const map=L.map('source-map',{crs:L.CRS.Simple,minZoom:-7,maxZoom:0,zoomSnap:.25,zoomControl:false});
L.control.zoom({position:'bottomright'}).addTo(map);
const names={
  rescue_station:['Equipo de rescate','Rescue equipment'],
  proposed_rescue_station:['Equipo propuesto','Proposed equipment'],
  proposed_cg_station:['Estación CG propuesta','Proposed CG station'],
  unclassified_facility:['Símbolo sin definir','Unclassified facility'],
  rip_current:['Corriente de resaca','Rip current'],strong_current_area:['Corrientes fuertes','Strong currents'],
  main_road:['Carretera principal','Main road'],side_road:['Camino lateral','Side road'],
  pedestrian:['Sendero peatonal','Footpath'],location:['Ubicación','Location']
};
const groups={hazards:L.layerGroup().addTo(map),rescue:L.layerGroup().addTo(map),proposals:L.layerGroup().addTo(map),access:L.layerGroup(),places:L.layerGroup()};
const definitions=[['hazards','rip_current','Resacas y corrientes','Rips and currents'],['rescue','rescue_station','Equipo de rescate','Rescue equipment'],['proposals','proposed_rescue_station','Propuestas / sin definir','Proposals / undefined'],['access','pedestrian','Caminos y accesos','Roads and access'],['places','location','Ubicaciones','Locations']];
let data, bounds;
function markerScale(){document.getElementById('source-map').classList.toggle('overview', map.getZoom() < -4);}
map.on('zoomend',markerScale);
const tr=(es,en)=>lang==='es'?es:en;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const xy=p=>[-p[1],p[0]];
function fit(){if(bounds)map.fitBounds(bounds,{paddingTopLeft:[15,15],paddingBottomRight:[20,30],animate:false});}
function popup(f){
 const proposed=f.kind.startsWith('proposed');
 let body=tr('Símbolo del mapa fuente; no confirma disponibilidad ni personal.','Source-map symbol; it does not confirm availability or staffing.');
 if(proposed)body=tr('Propuesto en el documento. No cuenta como equipo ni servicio disponible.','Proposed in the document. It is not available equipment or an operating service.');
 if(f.kind==='unclassified_facility')body=tr('La leyenda original no define este símbolo. Su función y estado requieren confirmación.','The original legend does not define this symbol. Its function and status need confirmation.');
 if(f.kind==='rip_current'||f.kind==='strong_current_area')body=tr('Peligro señalado en el documento. No es una observación del mar de hoy.','Hazard marked in the source document. This is not an observation of today’s sea.');
 if(f.kind==='location'||['main_road','side_road','pedestrian'].includes(f.kind))body=tr('Referencia del documento. No confirma acceso público ni transitabilidad.','Document reference. It does not confirm public access or passability.');
 if(f.number==='4.1')body+=' '+tr('El documento repite el número 4.1 en dos puntos.','The document repeats number 4.1 at two locations.');
 return `<div class="source-pop"><strong>${esc(names[f.kind][lang==='es'?0:1])}${f.number?' '+esc(f.number):''}</strong>${esc(body)}<small>08102026_FULL MAP DRAFT.pdf · ${tr('Página 1','Page 1')}</small></div>`;
}
function draw(){
 Object.values(groups).forEach(g=>g.clearLayers());
 if(!data)return;
 for(const f of data.features){
  const k=f.kind, pts=f.coordinates?.map(xy);
  let shape, group;
  if(k==='rip_current'){
   group=groups.hazards;shape=L.polyline(pts,{color:'#e53943',weight:2.5,dashArray:'6 5'});
   if(pts.length>1){const a=pts[pts.length-2],b=pts[pts.length-1],angle=Math.atan2(b[1]-a[1],b[0]-a[0])*180/Math.PI;
    L.marker(b,{interactive:false,keyboard:false,icon:L.divIcon({className:'',iconSize:[16,16],iconAnchor:[8,8],html:`<svg viewBox="0 0 16 16" style="transform:rotate(${angle}deg)"><path d="m8 1 6 13-6-3-6 3Z" fill="#e53943" stroke="white" stroke-width="1"/></svg>`})}).addTo(group);}
  }else if(k==='strong_current_area'){group=groups.hazards;shape=L.polygon(pts,{color:'#b92535',weight:2,dashArray:'5 4',fillColor:'#d63b47',fillOpacity:.3});
  }else if(['main_road','side_road','pedestrian'].includes(k)){
   group=groups.access;shape=L.polyline(pts,{color:k==='main_road'?'#4eb9f4':'#d0eaf9',weight:k==='main_road'?3:1.5,dashArray:k==='pedestrian'?'4 5':null});
  }else{
   group=k==='rescue_station'?groups.rescue:k==='location'?groups.places:groups.proposals;
   const symbol=k==='unclassified_facility'?'unknown':k;
   shape=L.marker(xy(f.point),{keyboard:true,title:names[k][lang==='es'?0:1]+(f.number?' '+f.number:''),icon:L.divIcon({className:'source-marker',iconSize:[30,30],iconAnchor:[15,15],html:CGSymbols.badge(symbol)+(f.number?`<span class="station-number">${esc(f.number)}</span>`:'')})});
  }
  shape.bindPopup(popup(f)).addTo(group);
 }
 // Use original text positions rather than uncertain nearest-label joins.
 for(const label of data.labels){
  if(label.color!==14863170&&label.color!==14863171)continue;
  const p=[label.box[0],label.box[1]];
  L.marker(xy(p),{interactive:false,keyboard:false,icon:L.divIcon({className:'source-label',html:esc(label.text),iconSize:[180,18],iconAnchor:[0,0]})}).addTo(groups.places);
 }
}
function ui(){
 document.documentElement.lang=lang;
 document.getElementById('lang').textContent=tr('EN','ES');
 document.getElementById('subtitle').textContent=tr('Mapa completo anotado','Full annotated map');
 document.getElementById('title').textContent=tr('Mapa anotado','Annotated map');
 document.getElementById('note').textContent=tr('Anotaciones del documento original. No es un mapa GPS ni indica condiciones actuales.','Original document annotations. This is not a GPS map or current conditions.');
 document.getElementById('back').textContent=tr('Volver a las playas','Back to beaches');
 document.getElementById('reset').textContent=tr('Ver toda la costa','Show whole coast');
 document.getElementById('controls').innerHTML=definitions.map(([id,icon,es,en])=>`<label>${CGSymbols.badge(icon)}<input type="checkbox" data-layer="${id}" ${map.hasLayer(groups[id])?'checked':''}>${tr(es,en)}</label>`).join('');
 document.querySelectorAll('[data-layer]').forEach(input=>input.onchange=()=>{const g=groups[input.dataset.layer];input.checked?g.addTo(map):map.removeLayer(g);});
 draw();
}
document.getElementById('lang').onclick=()=>{lang=lang==='es'?'en':'es';ui();};
document.getElementById('reset').onclick=fit;
window.addEventListener('resize',()=>{map.invalidateSize();fit();});
ui();
fetch('data/full-map-source.json').then(r=>{if(!r.ok)throw Error(r.status);return r.json();}).then(d=>{
 data=d;bounds=[[-d.height,0],[0,d.width]];
 const r=d.image_rect;L.imageOverlay('data/full-map-background.jpg',[[-r[3],r[0]],[-r[1],r[2]]]).addTo(map);
 map.setMaxBounds(L.latLngBounds(bounds).pad(.2));fit();draw();
}).catch(()=>{document.getElementById('load-state').textContent=tr('No se pudo cargar el mapa. Vuelve a intentar con conexión.','The map could not load. Try again with a connection.');});
