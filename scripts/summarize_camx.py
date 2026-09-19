"""Build short, source-faithful excerpts from long translated CAMX listings.

The summaries contain only sentences already present in the corresponding
language's listing. The complete listing stays in translations.json.
"""

import json
import re
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
records = json.loads((DATA / 'research.json').read_text())
translations = json.loads((DATA / 'translations.json').read_text())

SIGNAL = re.compile(
    r'composit|thermoplast|thermoset|fiber|fibre|resin|prepreg|mold|mould|'
    r'automotive|vehicle|battery|tape|laminat|reinforc|manufactur|process|'
    r'simulation|recycl|adhesiv|core material|lightweight|testing|inspection|'
    r'복합재|열가소|열경화|섬유|수지|프리프레그|성형|자동차|차량|배터리|'
    r'테이프|적층|보강|제조|공정|시뮬레이션|재활용|접착|경량|검사|시험',
    re.I,
)
PROMO = re.compile(
    r'visit us|stop by|learn more|contact us|years of|since (19|20)\d\d|'
    r'world leader|world-class|we are proud|look forward|employees|facilities|'
    r'locations|our company|your company|\?$|'
    r'방문해|자세히 알아|문의|자부|세계적인|오랜 역사|혁신 리더|'
    r'직원|제조 시설|지점|귀사의|습니까\?$|논의를 시작|협력하십시오', re.I
)

# High-priority automotive examples receive a concise editorial paraphrase of
# the same CAMX listing. Each language is written separately for readability.
OVERRIDES = {
    'id-620': {
        'ko': 'L&L Products는 자동차와 항공우주 등에 쓰이는 구조 보강재, 접착·밀봉재 및 소음 저감 소재를 소개합니다. CAMX 등록 소개에는 PHASTER™, CCS™, InsituCore™ 등 복합재 부품용 기술이 언급됩니다.',
        'en': 'L&L Products lists structural reinforcements, bonding and sealing materials, and acoustic solutions for automotive and aerospace applications. Its CAMX listing names PHASTER™, CCS™ and InsituCore™ among its technologies.',
    },
    'id-9808': {
        'ko': 'Avient는 CAMX 2026에서 연속섬유 강화 열가소성·열경화성 복합재와 장섬유 소재를 선보입니다. Polystrand™ 테이프의 성형·구조 해석용 물성 카드와 새 나일론 6 테이프도 소개합니다.',
        'en': 'Avient will show continuous-fiber thermoplastic and thermoset composites and long-fiber materials at CAMX 2026. Its listing highlights simulation-ready Polystrand™ material cards and new Nylon 6 tapes.',
    },
    'id-11883': {
        'ko': 'ExxonMobil은 저점도와 빠른 경화 특성을 내세운 Proxxima™ 폴리올레핀 열경화성 수지를 소개합니다. 회사는 경량 부품 제조와 기존 열경화성 수지 대비 온실가스 배출 저감을 강조합니다.',
        'en': 'ExxonMobil presents its Proxxima™ polyolefin thermoset resin, emphasizing low viscosity and controllable fast cure. The listing also claims lighter components and lower cradle-to-gate emissions than many conventional thermoset resins.',
    },
}


def sentences(value):
    value = re.sub(r'\s+', ' ', value).strip()
    # Preserve the source wording, including numbers and units inside a sentence.
    return [s.strip() for s in re.split(r'(?<=[.!?。])\s+(?=[A-ZÀ-ÖØ-öø-ÿ가-힣0-9“"(])', value) if s.strip()]


def excerpt(value, lang):
    limit = 250 if lang == 'ko' else 360
    lines = sentences(value)
    if len(value) <= limit or len(lines) < 2:
        return None
    ranked = []
    for position, line in enumerate(lines[:12]):
        if len(line) < 35:
            continue
        signals = len(SIGNAL.findall(line))
        score = min(signals, 6) * 3 - min(position, 20) * .4
        if PROMO.search(line):
            score -= 5
        if len(line) > limit:
            score -= 2
        ranked.append((score, position, line))
    if not ranked:
        return None
    first = max(ranked, key=lambda item: (item[0], -item[1]))
    selected = [first]
    for candidate in sorted(ranked, key=lambda item: (-item[0], item[1])):
        if (candidate[1] == first[1] or abs(candidate[1] - first[1]) > 3 or
                PROMO.search(candidate[2]) or
                len(candidate[2]) + len(first[2]) + 1 > limit):
            continue
        selected.append(candidate)
        break
    result = ' '.join(item[2] for item in sorted(selected, key=lambda item: item[1]))
    if len(result) > limit:
        # A single very long sentence is shortened at a word boundary.
        result = result[:limit].rsplit(' ', 1)[0].rstrip(' ,;:') + '…'
    return result if len(result) < len(value) else None


output = {}
for record in records:
    if not record.get('about'):
        continue
    key = f"id-{record['id']}" if record.get('id') else f"past-{record['name']}"
    translated = translations.get(key, {}).get('about', {})
    if not translated:
        continue
    entry = OVERRIDES.get(key) or {lang: excerpt(translated.get(lang, ''), lang) for lang in ('ko', 'en')}
    if any(entry.values()):
        output[key] = entry

(DATA / 'about_summaries.json').write_text(json.dumps(output, ensure_ascii=False, separators=(',', ':')) + '\n')
print(f'{len(output)} CAMX introductions summarized')
