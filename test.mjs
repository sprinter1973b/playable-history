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
const paths=[];(function walk(id,p,seen){if(seen.has(id)){err.push('loop at '+id);return}const n=all[id];if(S.endings[id]){paths.push([...p,id]);return}
 n.choices.forEach(c=>walk(c.next,[...p,id],new Set([...seen,id])))})(S.start,[],new Set());
const reached=new Set(paths.flat());Object.keys(all).forEach(k=>reached.has(k)||err.push('unreachable '+k));
console.log(JSON.stringify({stops:(S.route||[]).length,paths:paths.map(p=>p.join('>')),endings:[...new Set(paths.map(p=>p.at(-1)))],errors:err},null,1));
if(err.length)process.exit(1);
