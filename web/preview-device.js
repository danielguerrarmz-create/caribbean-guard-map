// Fixed, illustrative status values. These do not read device or user data.
const previewStage=document.getElementById('stage');
if(previewStage&&!previewStage.querySelector('.preview-status')){
  const status=document.createElement('div');
  status.className='preview-status';status.setAttribute('aria-hidden','true');
  status.innerHTML=`<span class="preview-clock">9:41</span><svg viewBox="0 0 76 17" fill="currentColor">
    <rect x="0" y="11" width="3" height="4" rx=".8"/><rect x="5" y="8" width="3" height="7" rx=".8"/><rect x="10" y="5" width="3" height="10" rx=".8"/><rect x="15" y="2" width="3" height="13" rx=".8"/>
    <path d="M24 5Q32-2 40 5M27 8Q32 3.5 37 8M30 11Q32 9 34 11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="32" cy="14" r="1.2"/>
    <rect x="47" y="2" width="25" height="13" rx="3" fill="none" stroke="currentColor" stroke-opacity=".65"/><rect x="49.5" y="4.5" width="20" height="8" rx="1.5"/><path d="M74 6v5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  </svg>`;
  previewStage.append(status);
}
