/* A printed QR identifies a fixed sign, never the phone's live GPS position. */
(function(global){
  'use strict';
  function resolve(id, records, accesses, references){
    const sign=records.find(record=>record.id===id);
    if(!sign||!['draft','verified'].includes(sign.status))return null;
    const access=accesses.find(record=>record.id===sign.accessId);
    const reference=references.find(record=>record.id===sign.referenceId);
    if(!access||!reference||!Array.isArray(sign.point)||sign.point.length!==2||
      !sign.point.every(Number.isFinite)||Math.abs(sign.point[0])>180||Math.abs(sign.point[1])>90)return null;
    return {sign,access,reference};
  }
  function link(base,id){
    if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id))throw new Error('Invalid sign identifier');
    const url=new URL(base);
    if(!['http:','https:'].includes(url.protocol))throw new Error('Invalid map URL');
    url.search='';url.hash='';url.searchParams.set('sign',id);
    return url.href;
  }
  global.CGSignposts={resolve,link};
})(typeof window==='undefined'?globalThis:window);
