const DIRECTORY='https://camx2026.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?exhid=';
const MARKETS=['전체','항공·우주','자동차','AI'];
const SEGMENTS=['전체','소재','공정','부품'];
const PAGE_SIZE=40;
let savedFavorites=[];try{savedFavorites=JSON.parse(localStorage.getItem('camx-favorites')||'[]')}catch{}
const state={records:[],translations:{},aboutSummaries:{},favorites:new Set(savedFavorites),lang:localStorage.getItem('camx-language')==='en'?'en':'ko',market:'전체',segment:'전체',scope:'all',query:'',shown:PAGE_SIZE,selected:null};
const $=s=>document.querySelector(s);
const t=(key,...args)=>{const value=window.CAMX_TEXT[state.lang][key];return typeof value==='function'?value(...args):value};
const label=value=>window.CAMX_TEXT[state.lang].labels[value]||value;
const escapeHtml=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize=v=>String(v??'').normalize('NFKC').toLocaleLowerCase().replace(/\s+/g,' ').trim();
function safeUrl(v){try{const u=new URL(v);return u.protocol==='https:'?u.href:'#'}catch{return '#'}}
const keyFor=r=>r.id?`id-${r.id}`:`past-${r.name.toLowerCase().replace(/[^a-z0-9]+/g,'-')}`;
const directoryUrl=r=>r.id?DIRECTORY+r.id:null;
const translationKey=r=>r.id?`id-${r.id}`:`past-${r.name}`;
function profileText(r,field){if(!r[field])return '';return state.translations[translationKey(r)]?.[field]?.[state.lang]||t('translationUnavailable')}
function categoryText(category){return state.translations._categories?.[category]?.[state.lang]||category}
function boothText(booth){if(!booth)return t('noBooth');return state.lang==='ko'?booth.replace('Building C, Level 1 — ','C동 1층 · '):booth.replace(' — ',' · ')}
function applyStaticLanguage(){
  document.documentElement.lang=state.lang;
  document.title=state.lang==='ko'?'CAMX 2026 전시회 업체 탐색':'CAMX 2026 Exhibitor Explorer';
  document.querySelector('meta[name="description"]').content=state.lang==='ko'?'CAMX 2026 전시회 업체 탐색. 항공·우주, 자동차, AI 분야별 참가업체 검색.':'Explore CAMX 2026 exhibitors by aerospace, automotive, AI, materials, process and components.';
  document.querySelectorAll('[data-i18n]').forEach(element=>{element.textContent=t(element.dataset.i18n)});
  document.querySelectorAll('[data-i18n-placeholder]').forEach(element=>{element.placeholder=t(element.dataset.i18nPlaceholder)});
  document.querySelectorAll('[data-i18n-aria]').forEach(element=>{element.setAttribute('aria-label',t(element.dataset.i18nAria))});
  document.querySelectorAll('[data-lang]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.lang===state.lang)));
  $('#snapshot-count').textContent=t('snapshotCount',state.records.filter(r=>r.verification==='확인됨').length);
}

function filtered(){const q=normalize(state.query);return state.records.filter(r=>{
  if(state.scope==='all'&&!r.id)return false;
  if(state.market!=='전체'&&!r.markets.includes(state.market))return false;
  if(state.segment!=='전체'&&!r.segments.includes(state.segment))return false;
  if(state.scope==='prior'&&!r.priorAttendance)return false;
  if(state.scope==='uncertain'&&(!r.id||r.verification==='확인됨'))return false;
  if(state.scope==='favorite'&&!state.favorites.has(keyFor(r)))return false;
  const translated=state.translations[translationKey(r)]||{};
  const words=[r.name,r.about,r.companyDescription,r.exhibit2026,r.award2026,r.direction,...r.categories,...r.markets,...r.segments,...Object.values(translated).flatMap(x=>Object.values(x))];
  return !q||normalize(words.join(' ')).includes(q);
})}
function renderFilters(){
  $('#market-filters').innerHTML=MARKETS.map(x=>`<button class="chip ${state.market===x?'active':''}" data-market="${escapeHtml(x)}" type="button" aria-pressed="${state.market===x}">${escapeHtml(label(x))}</button>`).join('');
  $('#segment-filters').innerHTML=SEGMENTS.map(x=>`<button class="chip ${state.segment===x?'active':''}" data-segment="${escapeHtml(x)}" type="button" aria-pressed="${state.segment===x}">${escapeHtml(label(x))}</button>`).join('');
  document.querySelectorAll('[data-scope]').forEach(b=>{const active=b.dataset.scope===state.scope;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))})
  $('#favorite-count').textContent=state.favorites.size;
}
function cardHtml(r){const badges=r.id?[]:[`<span class="badge absent">${t('notListed')}</span>`];
  if(r.priorAttendance)badges.push(`<span class="badge report">${t('priorBadge')}</span>`);
  badges.push(r.verification==='확인됨'?`<span class="badge">${escapeHtml([...r.markets,...r.segments].slice(0,3).map(label).join(' · '))}</span>`:`<span class="badge uncertain">${t('infoMissing')}</span>`);
  const description=profileText(r,'companyDescription')||profileText(r,'about');
  const products=r.categories.slice(0,3).map(category=>`<span>${escapeHtml(categoryText(category))}</span>`).join('');
  const saved=state.favorites.has(keyFor(r));
  return `<button type="button" class="company-card ${state.selected===keyFor(r)?'selected':''}" data-key="${escapeHtml(keyFor(r))}" aria-label="${escapeHtml(r.name)} ${t('viewDetails')}"><span class="card-top"><span class="card-name">${escapeHtml(r.name)}</span><span class="card-location">${saved?'<i aria-hidden="true">★</i>':''}${r.booth?`<span class="card-booth"><small>${t('boothLabel')}</small>${escapeHtml(r.booth.replace(/^Building C, Level 1 — /,''))}</span>`:''}</span></span><span class="card-meta">${badges.join('')}</span>${products?`<span class="card-products">${products}</span>`:''}${description?`<span class="card-summary">${escapeHtml(description.slice(0,170))}${description.length>170?'…':''}</span>`:''}</button>`
}
function renderList(){const rows=filtered();$('#result-count').textContent=t('resultCount',rows.length);
  $('#company-list').innerHTML=rows.length?rows.slice(0,state.shown).map(cardHtml).join(''):`<div class="no-results">${t('noResults')}</div>`;
  $('#more-button').hidden=rows.length<=state.shown;$('#more-button').textContent=t('more',Math.min(PAGE_SIZE,rows.length-state.shown));
  $('#clear-button').hidden=!state.query&&state.market==='전체'&&state.segment==='전체'&&state.scope==='all';
}
function section(title,body,note=''){return `<section class="detail-section"><h4>${escapeHtml(title)}</h4>${note?`<small>${escapeHtml(note)}</small>`:''}<p>${escapeHtml(body)}</p></section>`}
function camxSection(r){
  const full=profileText(r,'about');
  const short=state.aboutSummaries[translationKey(r)]?.[state.lang];
  if(!short)return section(t('camxIntro'),full,t('camxNote'));
  return `<section class="detail-section"><h4>${escapeHtml(t('camxIntro'))}</h4><small>${escapeHtml(t('camxSummaryNote'))}</small><p>${escapeHtml(short)}</p><details class="camx-full"><summary>${escapeHtml(t('camxShowFull'))}</summary><p>${escapeHtml(full)}</p></details></section>`;
}
function link(label,url,primary=false){return url&&safeUrl(url)!=='#'?`<a class="${primary?'primary':''}" href="${escapeHtml(safeUrl(url))}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)} ↗</a>`:''}
function renderDetail(){const r=state.records.find(x=>keyFor(x)===state.selected),panel=$('#detail-panel');
  if(!r){panel.innerHTML=`<div class="empty-detail"><span>↗</span><strong>${t('emptyTitle')}</strong><p>${t('emptyCopy')}</p></div>`;return}
  const known=r.verification==='확인됨',tags=known?[...r.markets,...r.segments].map(label):[t('infoMissing'),...r.segments.map(label)];
  const extraLinks=r.extraSources.map(s=>link(state.lang==='ko'?s.label:new URL(s.url).hostname.replace(/^www\./,''),s.url));
  const links=[link(t('companySite'),r.companySource||r.website,true),link(t('camxPage'),directoryUrl(r)),...extraLinks].filter(Boolean).join('');
  const verificationText=r.verification==='외부 자료 확인 어려움'?t('siteInsufficient'):r.verification==='분야 확인 어려움'?t('fieldInsufficient'):r.verification==='2026 참가 미확인'?t('priorOnly'):t('verified');
  const favorite=state.favorites.has(keyFor(r));
  panel.innerHTML=`<div class="detail-content"><p class="detail-kicker">${t('profileKicker')}</p><div class="detail-title-row"><h3>${escapeHtml(r.name)}</h3><button class="detail-close" type="button" aria-label="${t('closeDetail')}">×</button></div><div class="detail-tags">${tags.map(tag=>`<span>${escapeHtml(tag)}</span>`).join('')}</div><div class="status-line ${known?'':'unlisted'}"><span>${r.id?t('attending'):t('notListed')}</span><span>${escapeHtml(boothText(r.booth))}</span></div><button type="button" class="favorite-toggle ${favorite?'saved':''}" data-favorite="${escapeHtml(keyFor(r))}" aria-pressed="${favorite}">${favorite?'★':'☆'} ${favorite?t('favoriteSaved'):t('favoriteSave')}</button>${r.priorAttendance?section(t('prior'),t('priorText')):''}${r.categories.length?section(t('camxCategories'),r.categories.map(categoryText).join(' · ')):''}${r.companyDescription?section(t('companyIntro'),profileText(r,'companyDescription'),r.descriptionSource==='company_site'?t('companySiteNote'):t('editorialNote')):''}${r.about?camxSection(r):''}${r.exhibit2026?section(t('exhibit'),profileText(r,'exhibit2026')):''}${r.award2026?section(t('award2026Detail'),profileText(r,'award2026'),t('awardCandidateNote')):''}${r.direction?section(t('latest'),profileText(r,'direction'),t('latestNote')):''}${section(t('dataStatus'),verificationText)}<div class="links">${links}</div></div>`;
}
function applyFilter(){state.shown=PAGE_SIZE;renderFilters();renderList();if(state.selected&&!filtered().some(r=>keyFor(r)===state.selected))closeDetail()}
function selectRecord(key,updateHash=true){state.selected=key;document.querySelectorAll('.company-card').forEach(c=>c.classList.toggle('selected',c.dataset.key===key));renderDetail();if(updateHash)history.replaceState(null,'',`#company=${encodeURIComponent(key)}`);if(matchMedia('(max-width: 700px)').matches)$('#detail-panel').scrollTop=0}
document.querySelectorAll('[data-featured]').forEach(button=>button.addEventListener('click',()=>{const key=button.dataset.featured;const record=state.records.find(r=>keyFor(r)===key);if(!record)return;state.market='전체';state.segment='전체';state.scope='all';state.query=record.name;$('#search-input').value=record.name;applyFilter();selectRecord(key);$('#database').scrollIntoView({behavior:'smooth',block:'start'})}));
$('#show-prior').addEventListener('click',()=>{state.market='전체';state.segment='전체';state.scope='prior';state.query='';$('#search-input').value='';applyFilter();$('#database').scrollIntoView({behavior:'smooth',block:'start'})});
function closeDetail(){state.selected=null;renderDetail();document.querySelectorAll('.company-card').forEach(c=>c.classList.remove('selected'));history.replaceState(null,'',location.pathname+location.search)}
async function loadData(){try{const [response,translations,summaries]=await Promise.all([fetch('data/research.json?v=20260922-db'),fetch('data/translations.json?v=20260922-db'),fetch('data/about_summaries.json?v=20260922-db')]);if(!response.ok||!translations.ok||!summaries.ok)throw Error(t('loadError'));state.records=await response.json();state.translations=await translations.json();state.aboutSummaries=await summaries.json();
  $('#stat-all').textContent=state.records.filter(r=>r.id).length.toLocaleString(state.lang==='ko'?'ko-KR':'en-US');$('#stat-report').textContent=state.records.filter(r=>r.priorAttendance).length;$('#stat-match').textContent=state.records.filter(r=>r.priorAttendance&&r.id).length;applyStaticLanguage();applyFilter();const key=decodeURIComponent(location.hash.replace(/^#company=/,''));if(key&&state.records.some(r=>keyFor(r)===key))selectRecord(key,false)
}catch(e){$('#result-count').textContent=t('loadError');$('#company-list').innerHTML=`<div class="no-results">${escapeHtml(e.message)} ${t('refresh')}</div>`}}
$('#market-filters').addEventListener('click',e=>{const b=e.target.closest('[data-market]');if(b){state.market=b.dataset.market;applyFilter()}});
$('#segment-filters').addEventListener('click',e=>{const b=e.target.closest('[data-segment]');if(b){state.segment=b.dataset.segment;applyFilter()}});
document.querySelectorAll('[data-scope]').forEach(b=>b.addEventListener('click',()=>{state.scope=b.dataset.scope;applyFilter()}));
$('#search-input').addEventListener('input',e=>{state.query=e.target.value;applyFilter()});
$('#clear-button').addEventListener('click',()=>{state.query='';state.market='전체';state.segment='전체';state.scope='all';$('#search-input').value='';applyFilter();$('#search-input').focus()});
$('#more-button').addEventListener('click',()=>{state.shown+=PAGE_SIZE;renderList()});
$('#company-list').addEventListener('click',e=>{const c=e.target.closest('[data-key]');if(c)selectRecord(c.dataset.key)});
$('#detail-panel').addEventListener('click',e=>{if(e.target.closest('.detail-close'))closeDetail();const b=e.target.closest('[data-favorite]');if(b){const key=b.dataset.favorite;if(state.favorites.has(key))state.favorites.delete(key);else state.favorites.add(key);localStorage.setItem('camx-favorites',JSON.stringify([...state.favorites]));renderFilters();renderDetail();if(state.scope==='favorite')renderList()}});
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();$('#search-input').focus()}if(e.key==='Escape'&&state.selected)closeDetail()});
window.addEventListener('hashchange',()=>{const key=decodeURIComponent(location.hash.replace(/^#company=/,''));if(state.records.some(r=>keyFor(r)===key))selectRecord(key,false);else closeDetail()});
document.querySelectorAll('[data-lang]').forEach(button=>button.addEventListener('click',()=>{state.lang=button.dataset.lang;localStorage.setItem('camx-language',state.lang);applyStaticLanguage();renderFilters();renderList();renderDetail()}));
applyStaticLanguage();
loadData();
