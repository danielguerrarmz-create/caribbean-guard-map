// Read-only browser regression check. Run in desktop or mobile iframe via CUA evaluate.
// Returns failures instead of modifying the page. All glyphs and backings must share
// the geographic marker's center; changing hierarchy must never shift an anchor.
() => {
  const failures = [];
  const tiers = {};
  let checked = 0;
  const near = (a,b) => Math.abs(a-b) < .75;
  for (const marker of document.querySelectorAll('#map .projected-marker,#map .access-marker,#map .rip-reference-marker,#map .station-marker')) {
    const disc = marker.querySelector('.symbol') || marker.querySelector('span');
    const svg = disc?.querySelector('svg');
    if (!svg) continue;
    const m=marker.getBoundingClientRect(), d=disc.getBoundingClientRect(), s=svg.getBoundingClientRect();
    if (!m.width || !d.width || !s.width || getComputedStyle(marker).visibility==='hidden') continue;
    checked++;
    const kind=svg.getAttribute('data-icon');
    tiers[kind]={disc:Math.round(d.width),glyph:Math.round(s.width)};
    if (!near(m.x+m.width/2,d.x+d.width/2) || !near(m.y+m.height/2,d.y+d.height/2)) failures.push(`${kind}: backing moved off geographic anchor`);
    if (!near(s.x+s.width/2,d.x+d.width/2) || !near(s.y+s.height/2,d.y+d.height/2)) failures.push(`${kind}: glyph is off-center`);
    if (s.width>d.width-4 || s.height>d.height-4) failures.push(`${kind}: insufficient glyph padding`);
  }
  const candidates=[...document.querySelectorAll('#map .leaflet-marker-icon')].filter(n=>
    (n.matches('.access-marker,.projected-place,.projected-rescue')||n.querySelector('.station-marker'))&&
    n.getBoundingClientRect().width&&getComputedStyle(n).visibility!=='hidden');
  for(let i=0;i<candidates.length;i++)for(let j=i+1;j<candidates.length;j++){
    const a=candidates[i],b=candidates[j];
    // Rescue representatives must be separated too; their siblings are counted.
    const x=a.getBoundingClientRect(),y=b.getBoundingClientRect();
    if(x.left<y.right+5.5&&x.right>y.left-5.5&&x.top<y.bottom+5.5&&x.bottom>y.top-5.5)
      failures.push(`marker clearance: ${a.title} / ${b.title}`);
  }
  for(const n of document.querySelectorAll('.cg-marker-suppressed')){
    if(n.getAttribute('tabindex')!=='-1'||n.getAttribute('aria-hidden')!=='true')failures.push('suppressed marker remains accessible');
  }
  const shafts=document.querySelectorAll('.cg-rip-shaft').length;
  const pulses=[...document.querySelectorAll('.cg-rip-dashes')];
  if (shafts!==pulses.length) failures.push('some visible rip currents have no dashed motion class');
  return {checked,tiers,shafts,pulses:pulses.length,failures,
    motion:pulses.slice(0,1).map(p=>({name:getComputedStyle(p).animationName,state:getComputedStyle(p).animationPlayState,offset:getComputedStyle(p).strokeDashoffset}))};
}
