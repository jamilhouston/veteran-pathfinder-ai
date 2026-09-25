'use strict';
const $ = id => document.getElementById(id);
const form = $('career-form');
let step = 0, csrf = '', record = null, busy = false;
const labels = {branch:'Service branch',role:'Military role',years:'Years of experience',responsibilities:'Responsibilities',education:'Education / credentials',interests:'Career interests',collaboration:'Collaboration',structure:'Structure',focus:'Focus',environment:'Work setting'};
const profile = () => Object.fromEntries(new FormData(form));
function el(tag,text,cls){const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
async function api(path,options={}){
  const response=await fetch(path,{...options,headers:{'Content-Type':'application/json','X-CSRF-Token':csrf,...options.headers}});
  const data=await response.json();
  if(!response.ok)throw new Error(data.error||'Something went wrong. Please try again.');
  return data;
}
function showStep(n){
  step=n;
  document.querySelectorAll('[data-panel]').forEach(p=>p.hidden=Number(p.dataset.panel)!==n);
  document.querySelectorAll('[data-step]').forEach(p=>p.classList.toggle('active',Number(p.dataset.step)===n));
  $('back').hidden=n===0;$('next').hidden=n===2;$('generate').hidden=n!==2;
  $('step-label').textContent=`STEP 0${n+1} OF 03`;$('status').textContent='';
  if(n===2){$('review').replaceChildren();for(const [key,value] of Object.entries(profile())){$('review').append(el('dt',labels[key]),el('dd',value||'Not provided'));}}
}
function validPanel(){
  for(const field of document.querySelectorAll(`[data-panel="${step}"] input,[data-panel="${step}"] textarea`)){
    if(!field.checkValidity()){field.reportValidity();return false;}
  }return true;
}
$('next').onclick=()=>{if(validPanel())showStep(step+1);};
$('back').onclick=()=>showStep(step-1);
$('sample').onclick=()=>{
  const sample={branch:'Army',role:'92Y — Unit Supply Specialist',years:'6',responsibilities:'Tracked inventory, coordinated supply requests, and trained new team members.',education:'Associate degree in business administration',interests:'Logistics, operations, project coordination',collaboration:'With a team',structure:'Clear routines',focus:'Systems and data',environment:'Hybrid'};
  for(const [key,value] of Object.entries(sample))form.elements[key].value=value;
  showStep(0);$('status').textContent='Sample loaded. Change any detail, then continue.';
};
$('mode').onchange=()=>{
  $('ai-consent-row').hidden=$('mode').value!=='ai';
  if($('mode').value!=='ai')$('ai-consent').checked=false;
};
function list(parent,items){const ul=el('ul','');for(const item of items)ul.append(el('li',item));parent.append(ul);}
function render(data){
  record=data;$('workspace').hidden=true;$('results').hidden=false;
  $('source-label').textContent=`${data.source==='ai'?'AI-ASSISTED':'DEMO MODE'} · ${data.notice}`;
  $('career-cards').replaceChildren();
  data.results.careers.forEach((c,i)=>{const card=el('article','','career');card.append(el('span',`PATH 0${i+1}`,'number'),el('h3',c.title),el('p',c.why),el('h4','Gaps to investigate'));list(card,c.gaps);card.append(el('h4','Your next step'),el('p',c.next_step));$('career-cards').append(card);});
  $('translations').replaceChildren();
  data.results.translations.forEach(t=>{const row=el('div','','translation');row.append(el('strong',t.military),el('p','→ '+t.civilian));$('translations').append(row);});
  $('summary').textContent=data.results.summary;$('bullets').replaceChildren();
  data.results.bullets.forEach(b=>$('bullets').append(el('li',b)));
  $('results').focus();
}
form.addEventListener('submit',async e=>{
  e.preventDefault();if(busy)return;
  if(step!==2){if(validPanel())showStep(step+1);return;}
  if(!$('consent').checked){$('status').textContent='Please consent to temporary processing before continuing.';return;}
  if($('mode').value==='ai'&&!$('ai-consent').checked){$('status').textContent='Please consent to external AI processing, or choose demo mode.';return;}
  busy=true;$('generate').disabled=true;$('back').disabled=true;$('sample').disabled=true;
  $('status').textContent='Preparing your career possibilities…';
  try{render(await api('/api/generate',{method:'POST',body:JSON.stringify({profile:profile(),mode:$('mode').value,consent:$('consent').checked,ai_consent:$('ai-consent').checked})}));}
  catch(err){$('status').textContent=err.message;}
  finally{busy=false;$('generate').disabled=false;$('back').disabled=false;$('sample').disabled=false;}
});
$('edit').onclick=()=>{$('workspace').hidden=false;$('results').hidden=true;showStep(0);$('workspace').scrollIntoView({behavior:'smooth'});};
function download(name,text,type){const url=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('export').onclick=async()=>{try{const data=await api('/api/export');download('pathfinder-career-plan.json',JSON.stringify(data,null,2),'application/json');$('privacy-status').textContent='Export downloaded. Store it somewhere private.';}catch(err){$('privacy-status').textContent=err.message;}};
$('download-resume').onclick=()=>{if(record)download('pathfinder-resume-draft.txt','RESUME DRAFT — verify every statement and fill placeholders\n\n'+record.results.summary+'\n\n'+record.results.bullets.map(b=>'• '+b).join('\n'),'text/plain');};
$('delete').onclick=async()=>{
  if(!confirm('Delete your career details and results, and end this guest session? Download anything you want to keep first.'))return;
  try{await api('/api/profile',{method:'DELETE'});record=null;form.reset();location.reload();}catch(err){$('privacy-status').textContent=err.message;}
};
(async()=>{try{
  const data=await api('/api/session');csrf=data.csrf;
  const aiOption=$('mode').querySelector('[value="ai"]');aiOption.disabled=!data.ai_available;
  $('mode-info').textContent=data.ai_available?'AI is available. Demo mode remains an option.':'Demo mode is ready. The app owner can add an API key to enable AI-assisted plans.';
  if(data.profile){for(const [k,v] of Object.entries(data.profile.profile))form.elements[k].value=v;render(data.profile);}
  setTimeout(()=>{record=null;form.reset();$('results').hidden=true;$('workspace').hidden=false;$('generate').disabled=true;$('next').disabled=true;$('status').textContent='Session expired. Reload this page to start a new guest session.';},Math.max(0,data.expires*1000-Date.now()));
}catch(err){$('status').textContent=err.message;$('next').disabled=true;}})();
