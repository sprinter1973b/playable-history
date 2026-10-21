// Playable History engine: loads ?story=stories/x.json (default stories/woodstock.json)
(function(){
const app=document.getElementById('app');
const url=new URLSearchParams(location.search).get('story')||'stories/woodstock.json';
let S,cur,steps=0,path=[];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function art(id){const a=(S.images||{})[id];if(!a)return'';
 const inner=a.svg?a.svg:`<img src="${esc(a.src)}" alt="">`;
 return `<figure class="art" role="img" aria-label="${esc(a.alt)}">${inner}</figure>`;}
function src(ids){return (ids||[]).map(i=>{const s=S.sources.find(x=>x.id===i);return s?`<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)}</a>`:''}).join(' · ');}
const stop=n=>{const r=(S.route||[]).find(x=>x.stop===n);return r?r:null};
const gm=r=>'https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(r.maps);
function stopLine(n){const r=stop(n);if(!r)return'';return `<p class="stop"><span class="tag">Tour stop ${r.stop}</span> ${esc(r.name)} · ${esc(r.address)} · <a href="${esc(gm(r))}" target="_blank" rel="noopener">Open in Google Maps</a></p>`;}
function mapBtn(){return (S.route||[]).length?'<button id="map">🗺 Walk to the stops</button>':''}
function map(){const R=S.route||[],h=60+R.length*70;
 const dots=R.map((r,i)=>`<g><circle cx="40" cy="${40+i*70}" r="18" fill="#8c3b1f"/><text x="40" y="${46+i*70}" font-size="16" text-anchor="middle" fill="#fff" font-family="Georgia">${r.stop}</text><text x="72" y="${46+i*70}" font-size="15" fill="#2b2420" font-family="Georgia">${esc(r.name.length>34?r.name.slice(0,33)+'…':r.name)}</text></g>`).join('');
 app.innerHTML=`<div class="top"><button id="back">← Back to the story</button></div><h2 tabindex="-1">Walk to the next stop</h2>
 <p class="meta">Stops follow the numbering of the Historic Downtown Woodstock Walking Tour. Only the stops in this story are shown; the line is a simple guide, not to scale.</p>
 <svg viewBox="0 0 340 ${h-20}" role="img" aria-label="Route of tour stops ${R.map(r=>r.stop).join(', ')}" style="width:100%;background:#fffaf2;border-radius:10px"><line x1="40" y1="40" x2="40" y2="${40+(R.length-1)*70}" stroke="#8a6a45" stroke-width="4" stroke-dasharray="8 6"/>${dots}</svg>
 <ol class="route">${R.map(r=>`<li value="${r.stop}"><strong>${esc(r.name)}</strong><br>${esc(r.address)}<br><a href="${esc(gm(r))}" target="_blank" rel="noopener">Open in Google Maps</a></li>`).join('')}</ol>${foot()}`;
 document.getElementById('back').onclick=()=>cur?show(cur):start();app.querySelector('h2').focus();scrollTo(0,0);}
function bindMap(){const m=document.getElementById('map');if(m)m.onclick=map;}
function top(){const pct=Math.min(100,Math.round(steps/(S.meta.expectedSteps||5)*100));
 return `<div class="top"><div class="bar" role="progressbar" aria-label="Story progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}"><div style="width:${pct}%"></div></div><button id="rs" aria-label="Restart story">↺ Restart</button></div>`;}
function bind(){const r=document.getElementById('rs');if(r)r.onclick=start;bindMap();}
function start(){steps=0;path=[];cur=null;const m=S.meta;
 app.innerHTML=`${art(m.coverImage)}<span class="tag">${esc(m.museum)}</span><h1>${esc(m.title)}</h1><p>${esc(m.intro)}</p>
 <p class="meta">${esc(m.characterNote)}</p><button class="primary" id="go">Begin the story</button>${mapBtn()}${foot()}`;bindMap();
 document.getElementById('go').onclick=()=>show(S.start);app.querySelector('h1').focus?.();}
function show(id){cur=id;const n=S.scenes[id]||S.endings[id];if(!n){app.innerHTML='<p>Story error: missing "'+esc(id)+'"</p>';return;}
 if(S.endings[id])return end(n);
 app.innerHTML=`${top()}${art(n.image)}<p class="meta">${esc(n.when||'')}</p><h2 tabindex="-1">${esc(n.title)}</h2>${stopLine(n.stop)}${n.text.map(p=>`<p>${esc(p)}</p>`).join('')}
 ${n.fact?`<div class="fact"><strong>True history:</strong> ${esc(n.fact)}<div class="meta">${src(n.sources)}</div></div>`:''}
 <p><strong>${esc(n.prompt||'What do you do?')}</strong></p>${n.choices.map((c,i)=>`<button data-i="${i}">${esc(c.label)}</button>`).join('')}${mapBtn()}`;
 bind();app.querySelectorAll('button[data-i]').forEach(b=>b.onclick=()=>{const c=n.choices[+b.dataset.i];steps++;path.push(c.label);show(c.next);});
 app.querySelector('h2').focus();scrollTo(0,0);}
function end(n){steps=S.meta.expectedSteps||5;const m=S.meta;
 app.innerHTML=`${top()}${art(n.image)}<span class="tag">Ending</span><h2 tabindex="-1">${esc(n.title)}</h2>${n.text.map(p=>`<p>${esc(p)}</p>`).join('')}
 <div class="fact"><strong>What really happened</strong>${n.history.map(p=>`<p>${esc(p)}</p>`).join('')}<div class="meta">${src(n.sources)}</div></div>
 <a class="btn primary" href="${esc(m.cta.url)}" target="_blank" rel="noopener">${esc(m.cta.label)}</a>
 <button id="again">Play again and choose differently</button>${mapBtn()}${foot()}`;
 bind();document.getElementById('again').onclick=start;app.querySelector('h2').focus();scrollTo(0,0);}
function foot(){return `<footer><details><summary>Sources &amp; credits</summary><ul>${S.sources.map(s=>`<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.title)}</a></li>`).join('')}</ul><p>${esc(S.meta.credits)}</p></details></footer>`;}
fetch(url).then(r=>r.json()).then(j=>{S=j;document.title=j.meta.title;start();}).catch(e=>app.innerHTML='<p>Could not load story: '+esc(e.message)+'</p>');
if('serviceWorker' in navigator&&location.protocol.startsWith('http'))navigator.serviceWorker.register('sw.js').catch(()=>{});
})();
