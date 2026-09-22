"""Merge CAMX directory, company website metadata, and 2025 attendance names."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
official = json.loads((DATA / 'official-details.json').read_text())
sites = {x['id']: x for x in json.loads((DATA / 'company-sites.json').read_text())}
direct_path = DATA / 'recheck-direct.json'
direct = {x['id']: x for x in json.loads(direct_path.read_text())} if direct_path.exists() else {}
manual = {x['id']: x for x in json.loads((DATA / 'manual-sources.json').read_text())}
editorial = {x['name']: x for x in json.loads((DATA / 'editorial.json').read_text())}
editorial_by_id = {x['id']: x for x in editorial.values() if x.get('id')}
prior = set(json.loads((DATA / 'prior-attendance-2025.json').read_text()))
prior_ids = {x['id'] for x in editorial.values() if x.get('id') and x['name'] in prior}
NON_COMPANY_IDS = {'11587', '11589', '11588'}  # awards and exhibitor lounge

MARKETS = {
    '항공·우주': r'\baerospace\b|\baircraft\b|\baviation\b|\baeronautic|\bspacecraft\b|\bsatellite\b|\borbital\b|\bspace industry\b|\bspace launch\b|\bdefen[sc]e\b|\bairframe\b|항공|우주|위성',
    '자동차': r'\bautomotiv|\bvehicle|\bcar\b|\btruck\b|\btransportation\b|\bev\b|\bmobility\b|\bmotorsport|자동차|차량|모빌리티',
    'AI': r'\bartificial intelligence\b|\bmachine learning\b|\bai\b|\bdigital twin\b|인공지능|머신러닝',
}
SEGMENTS = {
    '소재': r'\bthermoplastic|\bprepreg|\bcore material|\bresin|\bgel coat|\breinforcement|\bfabric|\bglass fiber|\bcarbon fiber|\badhesive|\bsealant|\bfoam|\bmatrix material|\bnano material|\bpreform|\bbasalt|\bpolymer|\bchemical|\bfiber\b|\bfilament\b|\bfilm\b|\btape\b|\bhoneycomb\b|소재|수지|섬유|접착',
    '공정': r'\bmanufacturing process|\btooling|\bmold|\bautomation|\bautomated|\badditive manufacturing|\btransfer molding|\bout.of.autoclave|\btesting|\bcutting|\bpress(?:es|ing)?\b|\binfusion|\bfilament winding|\bpultrusion|\bcuring|\bprocess control|\bdesign|\bsimulation|\brobotic|\bsoftware|\bprojection|\blaboratory|공정|성형|자동화|설계|시뮬레이션|생산|최적화',
    '부품': r'\bcomponent|\bpart(?:s)?\b|\bstructure|\bpanel|\bblade|\bfastener|\bassembly|\bairframe|\bchassis|\bbody panel|\bwing|\bbracket|\bproduct(?:s)?\b|부품|구조물|패널',
}

def match(pattern, text):
    return bool(re.search(pattern, text, re.I))

records = []
for row in official:
    if row['id'] in NON_COMPANY_IDS:
        continue
    site = sites[row['id']]
    edit = editorial_by_id.get(row['id'], editorial.get(row['name'], {}))
    external = site.get('description', '')
    company_source = site.get('url') if site['status'] == 'ok' else None
    retry = direct.get(row['id'], {})
    if not external and retry.get('status') == 'found':
        found = retry['source']
        description = found['description']
        if (found['url'].startswith('https://') and
                re.search(r'composite|aerospace|automotiv|manufactur|fiberglass|fiber|resin|mold|material|engineering|technology|machin|polymer|adhesive|tooling|carbon|reinforc|chemical|testing|analysis|design|process|press|laminat', description, re.I) and
                not re.search(r'views, opinions|I love|cookie policy|privacy policy|subscribe to', description, re.I)):
            external = description
            company_source = found['url']
    manual_source = manual.get(row['id'])
    if manual_source and not external:
        external = manual_source['description']
        company_source = manual_source['url']
    extra_sources = [s for s in edit.get('sources', []) if 'mapyourshow.com' not in s['url']]
    independent = bool((company_source and len(external) >= 40) or extra_sources)
    market_text = ' '.join([row['name'], row['about'], ' '.join(row['categories']), external, edit.get('summary', ''), edit.get('direction', ''), edit.get('marketEvidence', '')])
    segment_text = ' '.join([row['name'], row['about'], ' '.join(row['categories']), external, edit.get('summary', '')])
    markets = [label for label, pattern in MARKETS.items() if match(pattern, market_text)]
    segments = [label for label, pattern in SEGMENTS.items() if match(pattern, segment_text)]
    if row['id'] == '10026' and 'AI' in markets:
        segments = ['공정']  # Plataine's sourced product is manufacturing planning software.
    if not independent:
        status = '외부 자료 확인 어려움'
    elif not markets or not segments:
        status = '분야 확인 어려움'
    else:
        status = '확인됨'
    # A failed external lookup is not enough to support an inferred industry.
    if status != '확인됨':
        markets = []
    record = {
        'id': row['id'], 'name': row['name'], 'booth': row['booth'],
        'website': row['website'] or (manual_source['url'] if manual_source else '') or edit.get('website', ''), 'about': row['about'],
        'categories': row['categories'],
        'companySource': company_source or (edit.get('website') if extra_sources else None), 'companyTitle': site.get('title', ''),
        'companyDescription': external or (edit.get('summary', '') if extra_sources else ''),
        'descriptionSource': 'editorial' if manual_source else ('company_site' if external else ('editorial' if extra_sources else 'none')),
        'markets': markets, 'segments': segments,
        'verification': status, 'priorAttendance': row['id'] in prior_ids or row['name'] in prior,
        'exhibit2026': edit.get('products2026', '') if edit.get('products2026') else '',
        'award2026': edit.get('award2026', '') if extra_sources else '',
        'direction': edit.get('direction', '') if extra_sources else '',
        'extraSources': extra_sources,
    }
    records.append(record)

matched_prior = {x['name'] for x in editorial.values() if x.get('id') in {r['id'] for r in records} and x['name'] in prior}
for name in sorted(prior - matched_prior):
    edit = editorial.get(name, {})
    records.append({
        'id': None, 'name': name, 'booth': '', 'website': edit.get('website', ''),
        'about': '', 'categories': [], 'companySource': None,
        'companyTitle': '', 'companyDescription': edit.get('summary', ''), 'descriptionSource': 'editorial',
        'markets': [], 'segments': [], 'verification': '2026 참가 미확인',
        'priorAttendance': True, 'exhibit2026': '', 'award2026': '', 'direction': edit.get('direction', ''),
        'extraSources': edit.get('sources', []),
    })

(DATA / 'research.json').write_text(json.dumps(records, ensure_ascii=False, separators=(',', ':')) + '\n')
print('records', len(records), 'verification', Counter(r['verification'] for r in records))
print('markets', Counter(x for r in records for x in r['markets']))
print('segments', Counter(x for r in records for x in r['segments']))
print('prior', sum(r['priorAttendance'] for r in records))
