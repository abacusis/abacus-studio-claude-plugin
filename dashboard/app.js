'use strict';
const $ = id => document.getElementById(id);
const icons = {
  orchestrator:'<circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><path d="M12 8v4M5 16v-4h14v4"/>',
  'spec-writer':'<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6M9 16h6"/>',
  builder:'<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-14-2 16"/>',
  verifier:'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
  'code-reviewer':'<circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/>',
  'security-reviewer':'<path d="m12 2 8 4v6c0 6-8 10-8 10S4 18 4 12V6z"/>',
  'ui-reviewer':'<rect x="2" y="3" width="20" height="14" rx="1"/><path d="M8 22h8m-4-5v5"/>',
  'ux-reviewer':'<circle cx="6" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="6" cy="20" r="2"/><path d="M6 6v12m0-4c8 0 12 0 12-4"/>',
  'readiness-reviewer':'<path d="M5 22V3c5-4 9 4 15 0v11c-6 4-10-4-15 0"/>',
  git:'<circle cx="6" cy="4" r="2"/><circle cx="6" cy="20" r="2"/><circle cx="18" cy="4" r="2"/><path d="M6 6v12m12-12v4c0 4-12 0-12 6"/>'
};
function icon(name){return '<svg viewBox="0 0 24 24" aria-hidden="true">'+icons[name]+'</svg>';}
const names={orchestrator:'Orchestrator','spec-writer':'Spec Writer',builder:'Builder',verifier:'Verification','code-reviewer':'Code Review','security-reviewer':'Security Review','ui-reviewer':'UI Review','ux-reviewer':'UX Review','readiness-reviewer':'Readiness'};
const labels={working:'Working',idle:'Idle',returned:'Returned',stale:'No recent signal',ended:'Session ended',interrupted:'Interrupted',attention:'Needs attention',queued:'Queued',not_required:'Not required'};
const resultLabels={passed:'Passed',failed:'Failed',not_verified:'Not verified',blocked:'Blocked',note:'Note'};
let data=null, selected='orchestrator', tab='activity', online=false, pending=false, requestError='';
const cards={};
function make(tag,className,content){const node=document.createElement(tag);if(className)node.className=className;if(content!==undefined)node.textContent=content;return node;}
Object.entries(names).forEach(([role,name])=>{
  const card=make('button','agent');card.type='button';card.setAttribute('aria-pressed',String(role===selected));card.setAttribute('aria-controls','details');
  const mark=make('span','agent-icon');mark.innerHTML=icon(role);card.append(mark,make('span','agent-name',name),make('span','state','Idle'),make('span','agent-summary',''));
  card.addEventListener('click',()=>{selected=role;$('details').hidden=false;document.querySelector('main').classList.remove('details-closed');updateSelection();renderPanel();if(window.matchMedia('(max-width:850px)').matches){$('detail-name').focus({preventScroll:true});$('details').scrollIntoView({block:'start',behavior:'instant'});}});
  $(role==='orchestrator'?'coordinator':'specialists').append(card);cards[role]=card;
});
$('git-icon').innerHTML=icon('git');
function status(agent){return !online&&agent.status==='working'?'stale':agent.status;}
function updateSelection(){
  Object.entries(cards).forEach(([role,card])=>card.setAttribute('aria-pressed',String(role===selected)));
  const agent=data?.agents.find(a=>a.role===selected);
  $('detail-name').textContent=names[selected];$('detail-icon').innerHTML=icon(selected);
  const state=agent?status(agent):'idle';$('detail-status').textContent=(labels[state]||'Unknown')+(agent?.active_count>1?' · '+agent.active_count+' instances':'');$('detail-status').className='state '+state;
  $('detail-task').textContent=agent?.report.summary||'No task summary reported yet.';
  $('detail-provenance').textContent=agent?.report_stale?'Report predates the latest agent start. Recheck it before relying on results.':'Lifecycle events are observed; summaries and check results are coordinator-reported.';
}
function renderPanel(){
  const panel=$('panel');panel.replaceChildren();panel.setAttribute('aria-labelledby','tab-'+tab);
  if(!data){panel.append(make('p','empty-state','Waiting for recorded activity.'));return;}
  if(tab==='activity'){
    const events=data.events.filter(e=>e.role===selected);
    if(!events.length)panel.append(make('p','empty-state','No activity recorded for this agent. Idle does not mean a review passed.'));
    events.forEach(e=>{const row=make('div','event');const time=make('time','',new Date(e.time*1000).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'}));time.dateTime=new Date(e.time*1000).toISOString();const body=make('div','',e.summary);if(e.file)body.append(make('small','',e.file));body.append(make('small','',e.source==='hook'?'Observed hook event':'Coordinator report · not independent execution'));row.append(time,body);panel.append(row);});
  }else if(tab==='changes'){
    const paths=[...new Set(data.events.filter(e=>e.role===selected&&e.file).map(e=>e.file))];
    if(!paths.length)panel.append(make('p','empty-state','No file changes attributed to this agent. Attribution is available only when Claude supplies an agent identity for the file event. Use the bottom bar for the full working copy.'));
    paths.forEach(path=>panel.append(make('div','file-row',path)));
  }else{
    const agent=data.agents.find(a=>a.role===selected);const items=[...(agent?.report.findings||[]),...(agent?.report.checks||[])];
    if(agent?.report_stale)panel.append(make('p','notice','This report may be stale. Refresh affected checks before a readiness claim.'));
    if(!items.length)panel.append(make('p','empty-state','No checks reported yet. An agent returning does not mean its tests or review passed.'));
    items.forEach(item=>{const row=make('div','finding',item.title||'Untitled report');row.dataset.result=item.result;row.append(make('small','',(resultLabels[item.result]||'Unknown')+' · Coordinator-reported'));panel.append(row);});
  }
}
const tabs=['activity','changes','checks'];
function setTab(value){tab=value;tabs.forEach(t=>{$('tab-'+t).setAttribute('aria-selected',String(t===tab));$('tab-'+t).tabIndex=t===tab?0:-1;});renderPanel();}
tabs.forEach(t=>{$('tab-'+t).addEventListener('click',()=>setTab(t));$('tab-'+t).addEventListener('keydown',e=>{let index=tabs.indexOf(tab);if(e.key==='ArrowRight')index=(index+1)%3;else if(e.key==='ArrowLeft')index=(index+2)%3;else if(e.key==='Home')index=0;else if(e.key==='End')index=2;else return;e.preventDefault();setTab(tabs[index]);$('tab-'+tab).focus();});});
$('close-details').addEventListener('click',()=>{$('details').hidden=true;document.querySelector('main').classList.add('details-closed');cards[selected].focus();});
$('show-changes').addEventListener('click',()=>{const open=$('all-changes').hidden;$('all-changes').hidden=!open;$('show-changes').setAttribute('aria-expanded',String(open));});
function render(){
  data.agents.forEach(agent=>{const card=cards[agent.role];if(!card)return;const state=status(agent);const stateNode=card.querySelector('.state');stateNode.className='state '+state;stateNode.textContent=(labels[state]||'Unknown')+(agent.active_count>1?' · '+agent.active_count:'');const summary=agent.report.summary||'';card.querySelector('.agent-summary').textContent=summary;card.classList.toggle('has-summary',Boolean(summary));card.setAttribute('aria-label',agent.name+': '+stateNode.textContent);});
  $('project').textContent=data.agents.find(a=>a.role==='orchestrator')?.report.summary||data.project;
  $('empty').hidden=Boolean(data.session);$('offline').hidden=online;
  const age=data.session?Math.max(0,Math.floor((Date.now()/1000-data.session.seen)/60)):null;
  const fresh=online&&data.session&&age<data.stale_after/60&&data.session.state!=='ended';
  $('connection').dataset.fresh=String(Boolean(fresh));$('connection').textContent=!online?'Offline':!data.session?'No session yet':data.session.state==='ended'?'Session ended':fresh?'Receiving activity':'No recent signal';
  $('session-note').textContent=age===null?'Waiting for Claude':age<1?'Last signal just now':'Last signal '+age+' min ago';
  const git=data.git;$('change-count').textContent=git.available?git.visible_count+' local change'+(git.visible_count===1?'':'s'):'Local changes unavailable';
  $('commit-count').textContent=git.ahead===null?'Unpushed commits unknown':git.ahead+' commit'+(git.ahead===1?'':'s')+' ahead of cached upstream';
  $('git-note').textContent=git.note;$('all-changes').replaceChildren(make('h2','','Local working copy'));
  if(!git.files.length)$('all-changes').append(make('p','empty-state',git.available?'No visible working-copy changes. This does not prove the branch is pushed.':'Git status unavailable.'));
  git.files.forEach(file=>{const row=make('div','file-row',file.path);row.append(make('span','',file.status+' · '+(file.staged?'Staged':'Not staged')));$('all-changes').append(row);});
  if(git.hidden_count)$('all-changes').append(make('p','quiet','Credential, hidden, or generated paths omitted: '+git.hidden_count));
  if(git.truncated)$('all-changes').append(make('p','quiet','Showing the first 100 paths.'));
  const queued=data.requests.filter(r=>r.state==='queued');
  $('submit').disabled=!online||pending||queued.some(r=>r.action==='submit');$('request-publish').disabled=!online||pending||queued.some(r=>r.action==='request-publish');
  if(requestError){$('request-notice').hidden=false;$('request-notice').textContent=requestError;}
  else if(queued.length){$('request-notice').hidden=false;$('request-notice').textContent='Request queued. Return to Claude and send “Continue” to start '+queued.map(r=>r.action==='submit'?'Submit changes':'Request publish').join(' and ')+'. No Git or publishing action has run.';}
  else if(data.requests.length){$('request-notice').hidden=false;$('request-notice').textContent='Latest request delivered to Claude. Delivery is not execution or approval; check Claude for the outcome.';}
  updateSelection();renderPanel();
}
async function refresh(){
  try{const response=await fetch('api/state',{cache:'no-store'});if(!response.ok)throw Error();data=await response.json();online=true;render();}
  catch{online=false;$('offline').hidden=false;$('connection').textContent='Offline';$('connection').dataset.fresh='false';$('submit').disabled=true;$('request-publish').disabled=true;if(data)render();}
}
async function request(action){
  pending=true;$('submit').disabled=true;$('request-publish').disabled=true;
  try{const response=await fetch('api/request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action})});if(!response.ok)throw Error();requestError='';await refresh();}
  catch{requestError='Could not queue the request. Nothing was executed. Ask Claude to run '+(action==='submit'?'/abacus-studio:submit':'/abacus-studio:request-publish')+' instead.';$('request-notice').hidden=false;$('request-notice').textContent=requestError;}
  finally{pending=false;if(data){const queued=data.requests.filter(r=>r.state==='queued');$('submit').disabled=!online||queued.some(r=>r.action==='submit');$('request-publish').disabled=!online||queued.some(r=>r.action==='request-publish');}}
}
$('submit').addEventListener('click',()=>request('submit'));$('request-publish').addEventListener('click',()=>request('request-publish'));
updateSelection();refresh();setInterval(refresh,3000);
