const DIRECTORY = 'https://camx2026.mapyourshow.com/8_0/exhibitor/exhibitor-details.cfm?exhid=';
const THEMES = ['전체', '소재', '공정', '부품', '항공', '자동차', 'AI', '건설', '풍력', '설계', '분류 전'];
const PAGE_SIZE = 45;
const state = { records: [], theme: '전체', scope: 'all', query: '', shown: PAGE_SIZE, selected: null };
const $ = (selector) => document.querySelector(selector);

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
}

function safeUrl(value) {
  try { const url = new URL(value); return url.protocol === 'https:' ? url.href : '#'; } catch { return '#'; }
}

function keyFor(record) { return record.id ? `id-${record.id}` : `past-${record.name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`; }

function currentUrl(record) { return record.id && /^\d+$/.test(record.id) ? DIRECTORY + record.id : null; }

function normalize(value) { return String(value ?? '').toLocaleLowerCase().normalize('NFKC').replace(/\s+/g, ' ').trim(); }

function getFiltered() {
  const query = normalize(state.query);
  return state.records.filter((record) => {
    if (state.theme !== '전체' && !(state.theme === '분류 전' ? !record.themes?.length : record.themes?.includes(state.theme))) return false;
    if (state.scope === 'report' && !record.products2025) return false;
    if (state.scope === 'current' && !record.id) return false;
    if (state.scope === 'unlisted' && (record.id || !record.products2025)) return false;
    if (!query) return true;
    return normalize([record.name, record.summary, record.products2025, record.products2026, record.direction, record.check, ...(record.themes || [])].join(' ')).includes(query);
  });
}

function renderFilters() {
  $('#theme-filters').innerHTML = THEMES.map((theme) => `<button class="chip ${state.theme === theme ? 'active' : ''}" data-theme="${escapeHtml(theme)}" type="button" aria-pressed="${state.theme === theme}">${escapeHtml(theme)}</button>`).join('');
  document.querySelectorAll('[data-scope]').forEach((button) => { const active = button.dataset.scope === state.scope; button.classList.toggle('active', active); button.setAttribute('aria-pressed', String(active)); });
}

function cardHtml(record) {
  const badges = [];
  if (record.products2025) badges.push('<span class="badge report">2025 보고서</span>');
  badges.push(record.id ? '<span class="badge">2026 참가 확인</span>' : '<span class="badge absent">올해 명단 미확인</span>');
  if (record.themes?.length) badges.push(`<span class="badge">${escapeHtml(record.themes.slice(0, 2).join(' · '))}</span>`);
  return `<button type="button" class="company-card ${state.selected === keyFor(record) ? 'selected' : ''}" data-key="${escapeHtml(keyFor(record))}" aria-label="${escapeHtml(record.name)} 상세 보기"><span class="card-top"><span class="card-name">${escapeHtml(record.name)}</span>${record.booth ? `<span class="card-booth">${escapeHtml(record.booth)}</span>` : ''}</span><span class="card-meta">${badges.join('')}</span>${record.summary ? `<span class="card-summary">${escapeHtml(record.summary)}</span>` : ''}</button>`;
}

function renderList() {
  const filtered = getFiltered();
  $('#result-count').textContent = `검색 결과 ${filtered.length.toLocaleString('ko-KR')}곳`;
  $('#company-list').innerHTML = filtered.length ? filtered.slice(0, state.shown).map(cardHtml).join('') : '<div class="no-results">검색 결과가 없습니다. 검색어 또는 필터를 바꿔 보세요.</div>';
  const more = $('#more-button');
  more.hidden = filtered.length <= state.shown;
  more.textContent = `더 보기 · ${Math.min(PAGE_SIZE, filtered.length - state.shown)}곳`;
  $('#clear-button').hidden = !state.query && state.theme === '전체' && state.scope === 'all';
}

function section(title, text) {
  return `<section class="detail-section"><h4>${escapeHtml(title)}</h4><p>${escapeHtml(text)}</p></section>`;
}

function renderDetail() {
  const record = state.records.find((item) => keyFor(item) === state.selected);
  const panel = $('#detail-panel');
  if (!record) {
    panel.innerHTML = '<div class="empty-detail"><span>↗</span><strong>업체를 선택하세요</strong><p>전년도 제품, 올해 전시 내용과 출처를 한곳에서 볼 수 있습니다.</p></div>';
    return;
  }
  const sources = (record.sources || []).map((source) => `<a href="${escapeHtml(safeUrl(source.url))}" target="_blank" rel="noopener noreferrer">${escapeHtml(source.label)} ↗</a>`).join('');
  const links = [record.website ? `<a class="primary" href="${escapeHtml(safeUrl(record.website))}" target="_blank" rel="noopener noreferrer">회사 홈페이지 ↗</a>` : '', currentUrl(record) ? `<a href="${escapeHtml(currentUrl(record))}" target="_blank" rel="noopener noreferrer">CAMX 공식 업체 정보 ↗</a>` : ''].filter(Boolean).join('');
  if (!record.featured) {
    panel.innerHTML = `<div class="detail-content simple-detail"><p class="detail-kicker">2026 OFFICIAL DIRECTORY</p><div class="detail-title-row"><h3>${escapeHtml(record.name)}</h3><button class="detail-close" type="button" aria-label="상세 닫기">×</button></div><p class="detail-summary">공식 명단에 등재된 업체입니다.</p><div class="status-line"><span>2026 참가 확인</span><span>업체명 기준</span></div>${section('업체 정보', '제품과 분야별 상세 정보는 CAMX 공식 업체 페이지에서 확인하세요.')}<div class="links">${links}</div><section class="detail-section"><h4>데이터 범위</h4><p>이 업체는 공식 명단에서 이름과 상세 링크를 확인했습니다. 전시품·최신 동향은 아직 개별 검증 전입니다.</p></section></div>`;
    return;
  }
  panel.innerHTML = `<div class="detail-content"><p class="detail-kicker">${record.products2025 ? '2025 REPORT · 2026 COMPARISON' : '2026 RESEARCH NOTE'}</p><div class="detail-title-row"><h3>${escapeHtml(record.name)}</h3><button class="detail-close" type="button" aria-label="상세 닫기">×</button></div><p class="detail-summary">${escapeHtml(record.summary)}</p><div class="detail-tags">${(record.themes || []).map((theme) => `<span>${escapeHtml(theme)}</span>`).join('')}</div><div class="status-line ${record.id ? '' : 'unlisted'}"><span>${record.id ? '2026 참가 확인' : '2026 공식 명단에서 미확인'}</span><span>${record.booth ? `부스 ${escapeHtml(record.booth)}` : '부스 정보 없음'}</span></div>${record.products2025 ? section('2025년 참관 보고서', record.products2025) : ''}${record.products2026 ? section('2026년 전시 정보', record.products2026) : section('2026년 전시 정보', '공식 명단에서 출품 내용을 확인하지 못했습니다.')}${section('최근 동향 · 개발 방향', record.direction)}<div class="compare-box"><h4>전년 대비</h4><p>${escapeHtml(record.compare)}</p></div>${section('현장에서 확인할 것', record.check)}<div class="links">${links}</div><section class="detail-section"><h4>출처</h4><div class="source-list">${sources}${record.products2025 ? '<span style="font-size:11px;color:#74858c"> · 사용자 제공 2025 참관 보고서 4–5쪽</span>' : ''}</div></section></div>`;
}

function applyFilter() { state.shown = PAGE_SIZE; renderFilters(); renderList(); }

function selectRecord(key, updateHash = true) {
  state.selected = key;
  document.querySelectorAll('.company-card').forEach((card) => card.classList.toggle('selected', card.dataset.key === key));
  renderDetail();
  if (updateHash) history.replaceState(null, '', `#company=${encodeURIComponent(key)}`);
  if (window.matchMedia('(max-width: 700px)').matches) $('#detail-panel').scrollTop = 0;
}

function closeDetail() { state.selected = null; renderDetail(); document.querySelectorAll('.company-card').forEach((card) => card.classList.remove('selected')); history.replaceState(null, '', location.pathname + location.search); }

async function loadData() {
  try {
    const [rawResponse, featuredResponse] = await Promise.all([fetch('data/exhibitors-2026-raw.json'), fetch('data/featured.json')]);
    if (!rawResponse.ok || !featuredResponse.ok) throw new Error('데이터 파일을 열 수 없습니다.');
    const [raw, featured] = await Promise.all([rawResponse.json(), featuredResponse.json()]);
    const byId = new Map(featured.filter((record) => record.id).map((record) => [record.id, record]));
    state.records = [
      ...featured.map((record) => ({ ...record, featured: true })),
      ...raw.filter(([, id]) => !byId.has(id)).map(([name, id]) => ({ name, id, featured: false, themes: [] }))
    ];
    $('#stat-all').textContent = raw.length.toLocaleString('ko-KR');
    $('#stat-report').textContent = featured.filter((record) => record.products2025).length;
    $('#stat-match').textContent = featured.filter((record) => record.products2025 && record.id).length;
    $('#snapshot-count').textContent = `${featured.length}곳 심층 정리`;
    applyFilter();
    const key = decodeURIComponent(location.hash.replace(/^#company=/, ''));
    if (key && state.records.some((record) => keyFor(record) === key)) selectRecord(key, false);
  } catch (error) {
    $('#result-count').textContent = '데이터를 불러오지 못했습니다.';
    $('#company-list').innerHTML = `<div class="no-results">${escapeHtml(error.message)} 페이지를 새로고침해 주세요.</div>`;
  }
}

$('#theme-filters').addEventListener('click', (event) => { const button = event.target.closest('[data-theme]'); if (!button) return; state.theme = button.dataset.theme; applyFilter(); });
document.querySelectorAll('[data-scope]').forEach((button) => button.addEventListener('click', () => { state.scope = button.dataset.scope; applyFilter(); }));
$('#search-input').addEventListener('input', (event) => { state.query = event.target.value; applyFilter(); });
$('#clear-button').addEventListener('click', () => { state.query = ''; state.theme = '전체'; state.scope = 'all'; $('#search-input').value = ''; applyFilter(); $('#search-input').focus(); });
$('#more-button').addEventListener('click', () => { state.shown += PAGE_SIZE; renderList(); });
$('#company-list').addEventListener('click', (event) => { const card = event.target.closest('[data-key]'); if (card) selectRecord(card.dataset.key); });
$('#detail-panel').addEventListener('click', (event) => { if (event.target.closest('.detail-close')) closeDetail(); });
document.addEventListener('keydown', (event) => { if (event.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) { event.preventDefault(); $('#search-input').focus(); } if (event.key === 'Escape' && state.selected) closeDetail(); });
window.addEventListener('hashchange', () => { const key = decodeURIComponent(location.hash.replace(/^#company=/, '')); if (state.records.some((record) => keyFor(record) === key)) selectRecord(key, false); else closeDetail(); });
loadData();
