/* One 24-unit maritime vocabulary for beach cards, map marks and forecast.
   Flat strokes, optical simplicity and text labels keep color from carrying
   meaning alone. These are project pictograms, not certified safety signs. */
(function(global){
  const paths={
    swimmer:'<circle cx="15" cy="7" r="1.6"/><path d="m5 14 5-4 5 2 4-1M3 18q2-1.5 4 0t4 0t4 0t4 0t2 0"/>',
    'no-swim':'<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12M5.5 16.5q2-1.5 4 0t4 0t4 0"/>',
    'high-risk':'<circle cx="12" cy="5.5" r="1.7"/><path d="M7 11h10M8 14h8M9.5 14l-2 6m7-6 2 6M5.5 20h13"/>',
    conditional:'<path d="M12 3 21 20H3Z"/><path d="M12 9v5m0 3v.2"/>',
    'lower-risk':'<path d="M3 14q2-1.8 4 0t4 0t4 0t4 0t4 0M3 19q2-1.8 4 0t4 0t4 0t4 0t4 0"/><path d="M12 4v5m0 2v.2"/>',
    unknown:'<circle cx="12" cy="12" r="9"/><path d="M9.4 9a2.7 2.7 0 1 1 4.4 2.1c-1 .7-1.8 1.2-1.8 2.5m0 3v.2"/>',
    rescue_station:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.8 5.8 3.4 3.4m5.6 5.6 3.4 3.4m-12.4 0 3.4-3.4m5.6-5.6 3.4-3.4"/>',
    proposed_rescue_station:'<circle cx="12" cy="12" r="9" stroke-dasharray="3 2.5"/><circle cx="12" cy="12" r="4"/><path d="m5.8 5.8 3.4 3.4m5.6 5.6 3.4 3.4"/>',
    proposed_cg_station:'<path d="M4 20V9l8-6 8 6v11Z" stroke-dasharray="3 2.5"/><path d="M9 14h6m-3-3v6"/>',
    rip_current:'<path d="M3 19q2-1.6 4 0t4 0t4 0t4 0t4 0M12 15V4m-4 4 4-4 4 4"/>',
    strong_current_area:'<path d="M12 3 21 20H3Z"/><path d="M7 16q2-1.6 4 0t4 0t2 0M12 8v4"/>',
    location:'<path d="M18.5 10c0 4.5-6.5 10.5-6.5 10.5S5.5 14.5 5.5 10a6.5 6.5 0 1 1 13 0Z"/><circle cx="12" cy="10" r="2"/>',
    main_road:'<path d="M2 12h20" stroke-width="4"/>',
    side_road:'<path d="M2 9h20M2 15h20"/>',
    pedestrian:'<path d="M2 12h20" stroke-dasharray="3 3"/>',
    me:'<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3" fill="currentColor"/>',
    wave:'<path d="M2 10q2.5-2 5 0t5 0t5 0t5 0M2 16q2.5-2 5 0t5 0t5 0t5 0"/>',
    period:'<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>',
    from:'<path d="M12 20V4m-5 5 5-5 5 5"/>',
    temp:'<path d="M14 14V6a2 2 0 0 0-4 0v8a4 4 0 1 0 4 0Z"/><path d="M12 10v7"/>'
  };
  const svg=(kind)=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${paths[kind]||paths.unknown}</svg>`;
  const badge=(kind,cls='')=>`<span class="symbol ${kind} ${cls}" aria-hidden="true">${svg(kind)}</span>`;
  global.CGSymbols={svg,badge};
})(window);
