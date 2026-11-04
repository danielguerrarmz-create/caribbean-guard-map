// Read-only label audit for an overview with visible map area.
() => {
 const visible=n=>n.getBoundingClientRect().width&&getComputedStyle(n).visibility!=='hidden'&&getComputedStyle(n).display!=='none';
 const labels=[...document.querySelectorAll('#map .lbl.zone')].filter(visible);
 const obstacles=[...document.querySelectorAll('#map .leaflet-marker-icon:not(.lbl),#map .rescue-count')].filter(visible);
 const hits=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;
 const failures=[];
 for(let i=0;i<labels.length;i++){
   const a=labels[i].getBoundingClientRect();
   if(obstacles.some(n=>hits(a,n.getBoundingClientRect())))failures.push(labels[i].innerText+': marker overlap');
   if(labels.slice(0,i).some(n=>hits(a,n.getBoundingClientRect())))failures.push(labels[i].innerText+': label overlap');
 }
 return {names:labels.map(n=>n.querySelector('strong')?.textContent||n.innerText),visible:labels.length,failures};
}
