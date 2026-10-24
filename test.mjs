import fs from 'fs';
const f=process.argv[2]||'stories/woodstock.json';const S=JSON.parse(fs.readFileSync(f,'utf8'));
const err=[];const ids=new Set(S.sources.map(s=>s.id));
for(const k of ['meta','images','sources','start','scenes','endings'])if(!(k in S))err.push('missing '+k);
const all={...S.scenes,...S.endings};
for(const[id,n]of Object.entries(all)){if(n.image&&!S.images[n.image])err.push(id+': bad image');(n.sources||[]).forEach(s=>ids.has(s)||err.push(id+': bad source '+s));
 (n.choices||[]).forEach(c=>all[c.next]||err.push(id+': bad next '+c.next));}
const stops=new Set((S.route||[]).map(r=>r.stop));for(const[id,n]of Object.entries(S.scenes)){if(!stops.has(n.stop))err.push(id+': missing/unknown stop');}
(S.route||[]).forEach((r,i)=>{if(!r.address||!r.maps||!r.name||!r.blurb)err.push('route '+r.stop+' incomplete');
 if(r.stop!==i+1)err.push('route out of order at '+r.stop);(r.sources||[]).forEach(s=>ids.has(s)||err.push('route '+r.stop+': bad source '+s));
 if(r.quiz&&!(r.quiz.options&&r.quiz.options[r.quiz.answer]))err.push('route '+r.stop+': bad quiz');
 if(r.photo&&!(r.photo.src&&fs.existsSync(r.photo.src)))err.push('route '+r.stop+': photo file missing '+(r.photo&&r.photo.src));});
if(S.route&&S.route.length!==25)err.push('expected 25 tour stops, got '+S.route.length);
const paths=[];function walk(id,p,seen){if(seen.has(id)){err.push('loop at '+id);return}const n=all[id];if(S.endings[id]){paths.push([...p,id]);return}
 n.choices.forEach(c=>walk(c.next,[...p,id],new Set([...seen,id])))}
walk(S.start,[],new Set());
const CH=S.chapters||{};if(Object.keys(CH).length!==25)err.push('expected 25 chapters, got '+Object.keys(CH).length);
for(const[k,c]of Object.entries(CH)){const before=paths.length;walk(c.start,[],new Set());const ps=paths.slice(before);
 if(ps.some(p=>all[p.at(-1)].chapter!==+k))err.push('chapter '+k+' ends outside its stop');
 const sc=new Set(ps.flat().filter(x=>S.scenes[x]));if(sc.size<2||sc.size>4)err.push('chapter '+k+' has '+sc.size+' scenes');
 sc.forEach(x=>{const n=S.scenes[x].choices.length;if(n<2||n>3)err.push(x+': '+n+' choices');if(S.scenes[x].stop!==+k)err.push(x+': wrong stop')});
 if(!all[ps[0].at(-1)].history?.length)err.push('chapter '+k+' no true history');
 if(c.depotScene&&!S.scenes[c.depotScene])err.push('chapter '+k+' bad depotScene');}
if(S.finale&&!(S.finale.title&&S.images[S.finale.image]))err.push('bad finale');
const reached=new Set(paths.flat());Object.keys(all).forEach(k=>reached.has(k)||err.push('unreachable '+k));
console.log(JSON.stringify({stops:(S.route||[]).length,chapters:Object.keys(CH).length,pathCount:paths.length,paths:paths.map(p=>p.join('>')),endings:[...new Set(paths.map(p=>p.at(-1)))],errors:err},null,1));
if(err.length)process.exit(1);
