const DIRECTORY='https://camx2026.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?exhid=';
const MARKETS=['전체','항공','자동차','AI','정확한 확인이 어려운 부분'];
const SEGMENTS=['전체','소재','공정','부품'];
const PAGE_SIZE=40;
const state={records:[],market:'전체',segment:'전체',scope:'all',query:'',shown:PAGE_SIZE,selected:null};
const $=s=>document.querySelector(s);
const escapeHtml=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize=v=>String(v??'').normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
function safeUrl(v){try{const u=new URL(v);return u.protocol==='https:'?u.href:'#'}catch{return '#'}}
const keyFor=r=>r.id?`id-${r.id}`:`past-${r.name.toLowerCase().replace(/[^a-z0-9]+/g,'-')}`;
const directoryUrl=r=>r.id?DIRECTORY+r.id:null;

function filtered(){const q=normalize(state.query);return state.records.filter(r=>{
  if(state.market==='정확한 확인이 어려운 부분'){if(r.verification==='확인됨')return false}
  else if(state.market!=='전체'&&!r.markets.includes(state.market))return false;
  if(state.segment!=='전체'&&!r.segments.includes(state.segment))return false;
  if(state.scope==='prior'&&!r.priorAttendance)return false;
  if(state.scope==='current'&&!r.id)return false;
  if(state.scope==='uncertain'&&r.verification==='확인됨')return false;
  return !q||normalize([r.name,r.about,r.companyDescription,r.exhibit2026,r.direction,...r.categories,...r.markets,...r.segments].join(' ')).includes(q);
})}
function renderFilters(){
  $('#market-filters').innerHTML=MARKETS.map(x=>`<button class="chip ${state.market===x?'active':''}" data-market="${escapeHtml(x)}" type="button" aria-pressed="${state.market===x}">${escapeHtml(x)}</button>`).join('');
  $('#segment-filters').innerHTML=SEGMENTS.map(x=>`<button class="chip ${state.segment===x?'active':''}" data-segment="${escapeHtml(x)}" type="button" aria-pressed="${state.segment===x}">${escapeHtml(x)}</button>`).join('');
  document.querySelectorAll('[data-scope]').forEach(b=>{const active=b.dataset.scope===state.scope;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))})
}
function cardHtml(r){const badges=[r.id?'<span class="badge">2026 참가</span>':'<span class="badge absent">2026 명단 미확인</span>'];
  if(r.priorAttendance)badges.push('<span class="badge report">2025 참가 확인</span>');
  badges.push(r.verification==='확인됨'?`<span class="badge">${escapeHtml([...r.markets,...r.segments].slice(0,3).join(' · '))}</span>`:'<span class="badge uncertain">확인 어려움</span>');
  const description=r.companyDescription||r.about||'';
  return `<button type="button" class="company-card ${state.selected===keyFor(r)?'selected':''}" data-key="${escapeHtml(keyFor(r))}" aria-label="${escapeHtml(r.name)} 상세 보기"><span class="card-top"><span class="card-name">${escapeHtml(r.name)}</span>${r.booth?`<span class="card-booth">${escapeHtml(r.booth.replace(/^Building C, Level 1 — /,''))}</span>`:''}</span><span class="card-meta">${badges.join('')}</span>${description?`<span class="card-summary">${escapeHtml(description.slice(0,170))}${description.length>170?'…':''}</span>`:''}</button>`
}
function renderList(){const rows=filtered();$('#result-count').textContent=`검색 결과 ${rows.length.toLocaleString('ko-KR')}곳`;
  $('#company-list').innerHTML=rows.length?rows.slice(0,state.shown).map(cardHtml).join(''):'<div class="no-results">검색 결과가 없습니다. 필터나 검색어를 바꿔 보세요.</div>';
  $('#more-button').hidden=rows.length<=state.shown;$('#more-button').textContent=`더 보기 · ${Math.min(PAGE_SIZE,rows.length-state.shown)}곳`;
  $('#clear-button').hidden=!state.query&&state.market==='전체'&&state.segment==='전체'&&state.scope==='all';
}
function section(title,body,note=''){return `<section class="detail-section"><h4>${escapeHtml(title)}</h4>${note?`<small>${escapeHtml(note)}</small>`:''}<p>${escapeHtml(body)}</p></section>`}
function link(label,url,primary=false){return url&&safeUrl(url)!=='#'?`<a class="${primary?'primary':''}" href="${escapeHtml(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)} ↗</a>`:''}
function renderDetail(){const r=state.records.find(x=>keyFor(x)===state.selected),panel=$('#detail-panel');
  if(!r){panel.innerHTML='<div class="empty-detail"><span>↗</span><strong>업체를 선택하세요</strong><p>회사 정보와 확인된 출처를 볼 수 있습니다.</p></div>';return}
  const known=r.verification==='확인됨',tags=known?[...r.markets,...r.segments]:['정확한 확인이 어려운 부분',...r.segments];
  const links=[link('회사 사이트',r.companySource||r.website,true),link('CAMX 2026 업체 정보',directoryUrl(r)),...r.extraSources.map(s=>link(s.label,s.url))].filter(Boolean).join('');
  const intro=r.companyDescription||r.about?.slice(0,200)||'확인 가능한 회사 소개 자료가 없습니다.';
  const verificationText=r.verification==='외부 자료 확인 어려움'?'회사 사이트의 설명 자료를 확인하지 못했습니다. CAMX 소개만으로 산업 분야를 확정하지 않았습니다.':r.verification==='분야 확인 어려움'?'회사 자료는 확인했으나 항공·자동차·AI 또는 소재·공정·부품 분야를 명확히 연결하기 어렵습니다.':r.verification==='2026 참가 미확인'?'2025 참가만 확인되었습니다. 2026 공식 명단에서는 같은 업체를 찾지 못했습니다.':'CAMX 디렉터리와 개별 회사 자료 또는 발표를 함께 확인했습니다.';
  panel.innerHTML=`<div class="detail-content"><p class="detail-kicker">CAMX 2026 · COMPANY PROFILE</p><div class="detail-title-row"><h3>${escapeHtml(r.name)}</h3><button class="detail-close" type="button" aria-label="상세 닫기">×</button></div><p class="detail-summary">${escapeHtml(intro)}</p><div class="detail-tags">${tags.map(t=>`<span>${escapeHtml(t)}</span>`).join('')}</div><div class="status-line ${known?'':'unlisted'}"><span>${r.id?'2026 참가 확인':'2026 명단 미확인'}</span><span>${r.booth?escapeHtml(r.booth):'부스 정보 없음'}</span></div>${r.priorAttendance?section('2025 참가','제공된 2025 참관 보고서에 업체명이 확인됩니다.'):''}${r.companyDescription?section('회사 소개',r.companyDescription,r.descriptionSource==='company_site'?'개별 회사 사이트의 공개 소개 문구':'회사 발표 자료를 바탕으로 한 요약'):''}${r.about?section('CAMX 등록 소개',r.about,'2026 공식 업체 디렉터리 등록 문구'):''}${r.categories.length?section('CAMX 등록 제품 분류',r.categories.join(' · ')):''}${r.exhibit2026?section('2026 등록 전시 정보',r.exhibit2026):''}${r.direction?section('최근 발표 · 개발 방향',r.direction,'아래 회사 발표 자료 기준'):''}${section('확인 상태',verificationText)}<div class="links">${links}</div></div>`;
}
function applyFilter(){state.shown=PAGE_SIZE;renderFilters();renderList()}
function selectRecord(key,updateHash=true){state.selected=key;document.querySelectorAll('.company-card').forEach(c=>c.classList.toggle('selected',c.dataset.key===key));renderDetail();if(updateHash)history.replaceState(null,'',`#company=${encodeURIComponent(key)}`);if(matchMedia('(max-width: 700px)').matches)$('#detail-panel').scrollTop=0}
function closeDetail(){state.selected=null;renderDetail();document.querySelectorAll('.company-card').forEach(c=>c.classList.remove('selected'));history.replaceState(null,'',location.pathname+location.search)}
async function loadData(){try{const response=await fetch('data/research.json');if(!response.ok)throw Error('데이터 파일을 열 수 없습니다.');state.records=await response.json();
  $('#stat-all').textContent=state.records.filter(r=>r.id).length.toLocaleString('ko-KR');$('#stat-report').textContent=state.records.filter(r=>r.priorAttendance).length;$('#stat-match').textContent=state.records.filter(r=>r.priorAttendance&&r.id).length;$('#snapshot-count').textContent=`${state.records.filter(r=>r.verification==='확인됨').length}곳 교차 확인`;applyFilter();const key=decodeURIComponent(location.hash.replace(/^#company=/,''));if(key&&state.records.some(r=>keyFor(r)===key))selectRecord(key,false)
}catch(e){$('#result-count').textContent='데이터를 불러오지 못했습니다.';$('#company-list').innerHTML=`<div class="no-results">${escapeHtml(e.message)} 페이지를 새로고침해 주세요.</div>`}}
$('#market-filters').addEventListener('click',e=>{const b=e.target.closest('[data-market]');if(b){state.market=b.dataset.market;applyFilter()}});
$('#segment-filters').addEventListener('click',e=>{const b=e.target.closest('[data-segment]');if(b){state.segment=b.dataset.segment;applyFilter()}});
document.querySelectorAll('[data-scope]').forEach(b=>b.addEventListener('click',()=>{state.scope=b.dataset.scope;applyFilter()}));
$('#search-input').addEventListener('input',e=>{state.query=e.target.value;applyFilter()});
$('#clear-button').addEventListener('click',()=>{state.query='';state.market='전체';state.segment='전체';state.scope='all';$('#search-input').value='';applyFilter();$('#search-input').focus()});
$('#more-button').addEventListener('click',()=>{state.shown+=PAGE_SIZE;renderList()});
$('#company-list').addEventListener('click',e=>{const c=e.target.closest('[data-key]');if(c)selectRecord(c.dataset.key)});
$('#detail-panel').addEventListener('click',e=>{if(e.target.closest('.detail-close'))closeDetail()});
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();$('#search-input').focus()}if(e.key==='Escape'&&state.selected)closeDetail()});
window.addEventListener('hashchange',()=>{const key=decodeURIComponent(location.hash.replace(/^#company=/,''));if(state.records.some(r=>keyFor(r)===key))selectRecord(key,false);else closeDetail()});
loadData();
