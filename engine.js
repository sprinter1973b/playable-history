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
function mapBtn(){return (S.route||[]).length?`<button id="map">🗺 Walking Tour: all ${S.route.length} stops</button>`:''}
function photo(r){const p=r.photo;if(!p||!p.src)return'';
 return `<figure class="photo"><img src="${esc(p.src)}" alt="${esc(p.alt||r.name)}" loading="lazy" onerror="this.parentNode.remove()">${p.caption||p.credit?`<figcaption>${esc(p.caption||'')}${p.credit?` <span class="meta">Photo: ${esc(p.credit)}</span>`:''}</figcaption>`:''}</figure>`;}
function sceneFor(n){return Object.keys(S.scenes).find(k=>S.scenes[k].stop===n);}
let back=null;
function map(){const R=S.route||[],gap=44,h=60+R.length*gap;
 if(back===null)back=cur;
 const dots=R.map((r,i)=>`<g class="dot" data-s="${r.stop}" style="cursor:pointer"><circle cx="30" cy="${30+i*gap}" r="15" fill="${sceneFor(r.stop)?'#1f5f8c':'#8c3b1f'}"/><text x="30" y="${35+i*gap}" font-size="13" text-anchor="middle" fill="#fff" font-family="Georgia">${r.stop}</text><text x="56" y="${35+i*gap}" font-size="14" fill="#2b2420" font-family="Georgia">${esc(r.name.length>36?r.name.slice(0,35)+'…':r.name)}</text></g>`).join('');
 app.innerHTML=`<div class="top"><button id="back">← ${back?'Back to the story':'Back to start'}</button></div><h2 tabindex="-1">Walking Tour</h2>
 <p class="meta">All ${R.length} stops in the order of the Historic Downtown Woodstock Walking Tour. Tap a stop to read about it and answer a quick question. Blue stops are also part of the depot story. The line is a simple guide, not to scale.</p>
 <button class="primary" id="tourgo">Start the tour at stop ${R[0].stop}</button>
 <svg viewBox="0 0 340 ${h-20}" role="img" aria-label="Tour stops 1 to ${R.length}" style="width:100%;background:#fffaf2;border-radius:10px"><line x1="30" y1="30" x2="30" y2="${30+(R.length-1)*gap}" stroke="#8a6a45" stroke-width="4" stroke-dasharray="8 6"/>${dots}</svg>
 <ol class="route">${R.map(r=>`<li value="${r.stop}"><strong>${esc(r.name)}</strong><br>${esc(r.address)}<br><a href="${esc(gm(r))}" target="_blank" rel="noopener">Open in Google Maps</a> · <a href="#" class="open" data-s="${r.stop}">Read &amp; play</a></li>`).join('')}</ol>${foot()}`;
 document.getElementById('back').onclick=()=>{const c=back;back=null;c?show(c):start();};
 document.getElementById('tourgo').onclick=()=>tourStop(0);
 app.querySelectorAll('[data-s]').forEach(e=>e.onclick=ev=>{ev.preventDefault();tourStop(R.findIndex(r=>r.stop===+e.dataset.s));});
 app.querySelector('h2').focus();scrollTo(0,0);}
function tourStop(i){const R=S.route,r=R[i],q=r.quiz,sc=sceneFor(r.stop);
 app.innerHTML=`<div class="top"><button id="tl">☰ All stops</button><span class="meta" style="flex:1;text-align:right">Stop ${r.stop} of ${R.length}</span></div>
 ${photo(r)}<span class="tag">Tour stop ${r.stop}</span><h2 tabindex="-1">${esc(r.name)}</h2>
 <p class="stop">${esc(r.address)} · <a href="${esc(gm(r))}" target="_blank" rel="noopener">Open in Google Maps</a></p>
 <div class="fact"><strong>True history:</strong> ${esc(r.blurb)}<div class="meta">${src(r.sources)}</div></div>
 ${q?`<div class="quiz"><p><strong>${esc(q.q)}</strong></p>${q.options.map((o,k)=>`<button data-q="${k}">${esc(o)}</button>`).join('')}<p class="meta" id="qr" aria-live="polite"></p></div>`:''}
 ${sc?`<button id="play">▶ Play the depot story chapter at this stop</button>`:''}
 <div class="top">${i>0?`<button id="prev">← Stop ${R[i-1].stop}</button>`:''}<span style="flex:1"></span>${i<R.length-1?`<button id="next" class="primary">Walk on to stop ${R[i+1].stop} →</button>`:`<button id="tl2" class="primary">Tour complete ✓</button>`}</div>${foot()}`;
 const g=id=>document.getElementById(id);
 g('tl').onclick=map;if(g('tl2'))g('tl2').onclick=map;if(g('prev'))g('prev').onclick=()=>tourStop(i-1);if(g('next'))g('next').onclick=()=>tourStop(i+1);
 if(g('play'))g('play').onclick=()=>{back=null;steps=0;path=[];show(sc);};
 app.querySelectorAll('button[data-q]').forEach(b=>b.onclick=()=>{const k=+b.dataset.q,ok=k===q.answer;
  app.querySelectorAll('button[data-q]').forEach(x=>{x.disabled=true;if(+x.dataset.q===q.answer)x.classList.add('right');});if(!ok)b.classList.add('wrong');
  g('qr').textContent=ok?'Correct!':'Not quite. The answer is: '+q.options[q.answer]+'.';});
 app.querySelector('h2').focus();scrollTo(0,0);}
function bindMap(){const m=document.getElementById('map');if(m)m.onclick=()=>{back=cur;map();};}
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
