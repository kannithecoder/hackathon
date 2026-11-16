/* Knowa offline cache: the page and the 3D library are kept after the first visit */
const V='knowa-v1';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(['/'])).catch(()=>{}))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
const keep=(req,res)=>{if(res&&(res.ok||res.type==='opaque')){const cp=res.clone();caches.open(V).then(c=>c.put(req,cp)).catch(()=>{})}return res};
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
  if(u.pathname.startsWith('/api/'))return;
  if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>keep('/',res)).catch(()=>caches.match('/').then(x=>x||new Response('Offline. Open Knowa once with internet first.',{status:503,headers:{'Content-Type':'text/plain'}}))));return}
  if(u.origin===location.origin){e.respondWith(fetch(r).then(res=>keep(r,res)).catch(()=>caches.match(r).then(x=>x||new Response('',{status:504}))));return}
  if(u.hostname==='cdnjs.cloudflare.com'){e.respondWith(caches.match(r).then(x=>x||fetch(r).then(res=>keep(r,res))))}
});
