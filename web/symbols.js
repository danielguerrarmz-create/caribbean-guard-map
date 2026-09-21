/* One SVG vocabulary for beach cards, map markers and the visible key.
   Color always has a second cue: shape, pictogram, text, or a dashed outline. */
(function(global){
  const paths={
    swimmer:'<circle cx="14" cy="8" r="2"/><path d="m5 15 5-4 5 3 4-1M3 19q2-2 4 0t4 0t4 0t4 0"/>',
    'no-swim':'<circle cx="12" cy="12" r="9"/><path d="m6 6 12 12M5 16q2-2 4 0t4 0t4 0"/><circle cx="14" cy="8" r="1.5"/>',
    'high-risk':'<circle cx="12" cy="5" r="2"/><path d="M8 10h8l2 4H6zM9 14l-2 7m8-7 2 7M5 21h14"/>',
    conditional:'<path d="m12 3 10 18H2Z"/><path d="M12 9v5m0 3v.1"/>',
    'lower-risk':'<path d="M2 14q2-2 4 0t4 0t4 0t4 0t4 0M2 19q2-2 4 0t4 0t4 0t4 0t4 0"/><path d="M12 3v6m0 2v.1"/>',
    unknown:'<circle cx="12" cy="12" r="9"/><path d="M9 8a3 3 0 1 1 4 3c-1 1-1 2-1 3m0 3v.1"/>',
    rescue_station:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m6 6 3 3m6 6 3 3M6 18l3-3m6-6 3-3"/>',
    proposed_rescue_station:'<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/><circle cx="12" cy="12" r="4"/><path d="m6 6 3 3m6 12 3-3"/>',
    proposed_cg_station:'<path d="M4 21V9l8-6 8 6v12Z" stroke-dasharray="3 2"/><path d="M9 14h6m-3-3v6"/>',
    rip_current:'<path d="M3 18q3-3 6 0t6 0t6 0M12 15V3m-4 4 4-4 4 4"/>',
    strong_current_area:'<path d="m12 3 10 18H2Z"/><path d="M7 16q2-2 4 0t4 0t3 0M12 8v4"/>',
    location:'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>',
    main_road:'<path d="M2 12h20" stroke-width="4"/>',
    side_road:'<path d="M2 9h20M2 15h20"/>',
    pedestrian:'<path d="M2 12h20" stroke-dasharray="3 3"/>',
    me:'<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3" fill="currentColor"/>'
  };
  const svg=(kind)=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${paths[kind]||paths.unknown}</svg>`;
  const badge=(kind,cls='')=>`<span class="symbol ${kind} ${cls}" aria-hidden="true">${svg(kind)}</span>`;
  global.CGSymbols={svg,badge};
})(window);
