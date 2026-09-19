"""Build offline English/Korean translations for public exhibitor text."""
import concurrent.futures
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CACHE = DATA / '.translation-cache.json'
FIELDS = ('about', 'companyDescription', 'exhibit2026', 'direction')
HEADERS = {'User-Agent': 'Mozilla/5.0'}
CATEGORY_KO = {
    'Aerospace':'항공·우주','Glass Fibers':'유리섬유','Thermoplastics':'열가소성 소재',
    'Tooling, Mold and Plugs':'툴링·금형·플러그','Tools and Tooling Equipment':'툴링 장비',
    'Automated Fiber Placement':'자동 섬유 적층','Automation Equipment':'자동화 장비',
    'Manufacturing Process Development':'제조 공정 개발','Prepreg Manufacturing/Handling Equipment':'프리프레그 제조·취급 장비',
    'Prepregs':'프리프레그','Material Research and Development':'소재 연구개발',
    'Core Materials':'코어 소재','Resin and/or Gel Coat':'수지·겔코트','Reinforcements':'보강재',
    'Fabrics':'직물','Out-of-Autoclave (OOA)':'비오토클레이브 공정','Additive Manufacturing':'적층 제조',
    'Carbon Fiber Systems':'탄소섬유 시스템','Adhesives & Sealants':'접착제·실란트',
    'Design Product Development Services':'설계·제품 개발 서비스','Resin Transfer Molding':'수지 이송 성형',
    'Carbon Fibers':'탄소섬유','Testing Equipment':'시험 장비','Testing Laboratory':'시험 연구소',
    'Cutting Equipment':'절단 장비','Presses/Compression':'프레스·압축 성형','First Time Exhibitor':'첫 참가업체',
    'Foams':'발포 소재','MRO - Maintenance, Repair, Operations':'유지보수·수리·운영',
    'Consulting Services':'컨설팅','Matrix Materials':'매트릭스 소재',
    'Filament Winding Equipment':'필라멘트 와인딩 장비','Repair':'수리','Education/Training':'교육·훈련',
    'Process Control':'공정 제어','Sporting Equipment':'스포츠 장비','Ovens/Dryers/Furnaces':'오븐·건조기·로',
    'Cure Initiators/Catalysts':'경화 개시제·촉매','Electrical/Electronic':'전기·전자',
    'Mold Release Systems':'이형 시스템','Preforms':'프리폼','Nano Materials':'나노 소재',
    'Assembly/Bonding Equipment':'조립·접합 장비','Braiding, Knitting/Stitching':'브레이딩·편직·스티칭',
    'Fabricating Supplies':'제조 소모품','Temperature Monitoring/Recording':'온도 모니터링·기록',
    'Blenders/Mixers':'혼합 장비','Infusion Equipment':'인퓨전 장비','Pultrusion Machinery':'인발 성형 기계',
    'Laser Projection':'레이저 투영','Safety Equipment and Supplies':'안전 장비·용품',
    'Air Pollution Control':'대기오염 방지','Ventilating Equipment/Dust/Odor Control':'환기·분진·악취 제어',
    'Infrared Curing Systems':'적외선 경화 시스템','Fasteners':'체결 부품'
}


def key(text, lang):
    return hashlib.sha256((lang + '\0' + text).encode()).hexdigest()


def already_target(text, lang):
    if lang == 'ko':
        return bool(re.search('[가-힣]', text)) and not bool(re.search('[\u4e00-\u9fff]', text))
    if re.search('[가-힣\u4e00-\u9fff\u3040-\u30ff]', text): return False
    if not text.isascii(): return False
    return len(re.findall(r'\b(the|and|for|with|are|is|of|our|we|to|in|from|this|that|provide|manufacture|materials)\b', text, re.I)) >= 2


def chunks(text, limit=1450):
    if len(text) <= limit: return [text]
    chunks_out = []
    remaining = text
    while remaining:
        if len(remaining) <= limit:
            chunks_out.append(remaining)
            break
        cut = max(remaining.rfind('\n', 0, limit), remaining.rfind('. ', 0, limit), remaining.rfind('。', 0, limit))
        if cut < limit // 2: cut = limit
        else: cut += 1
        chunks_out.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    return chunks_out


def translate_chunk(text, lang):
    query = urllib.parse.urlencode({'client': 'gtx', 'sl': 'auto', 'tl': lang, 'dt': 't', 'q': text})
    url = 'https://translate.googleapis.com/translate_a/single?' + query
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.load(response)
    output = ''.join(piece[0] or '' for piece in payload[0]).strip()
    if not output: raise ValueError('empty translation')
    return output


def translate_one(text, lang):
    if already_target(text, lang): return text
    for attempt in range(3):
        try: return '\n\n'.join(translate_chunk(chunk, lang) for chunk in chunks(text))
        except Exception:
            if attempt == 2: return None
            time.sleep(1.5 * (attempt + 1))


if __name__ == '__main__':
    records = json.loads((DATA / 'research.json').read_text())
    texts = {x[field] for x in records for field in FIELDS if x.get(field)}
    texts.update(x for row in records for x in row['categories'])
    existing = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    tasks = [(text, lang) for text in texts for lang in ('ko', 'en') if key(text, lang) not in existing]
    print('unique texts', len(texts), 'translation tasks', len(tasks), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(translate_one, text, lang): (text, lang) for text, lang in tasks}
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            text, lang = futures[future]
            result = future.result()
            if result: existing[key(text, lang)] = result
            if i % 50 == 0 or i == len(tasks):
                CACHE.write_text(json.dumps(existing, ensure_ascii=False))
                print('completed', i, '/', len(tasks), 'successful', len(existing), flush=True)
    output = {}
    for row in records:
        k = 'id-' + row['id'] if row['id'] else 'past-' + row['name']
        output[k] = {field: {lang: existing.get(key(row[field], lang), '') for lang in ('ko', 'en')}
                     for field in FIELDS if row.get(field)}
    output['_categories'] = {category: {'ko': CATEGORY_KO.get(category, existing.get(key(category, 'ko'), '')), 'en': category}
                             for category in sorted({x for row in records for x in row['categories']})}
    (DATA / 'translations.json').write_text(json.dumps(output, ensure_ascii=False, separators=(',', ':')) + '\n')
    missing = sum(not value for entry in output.values() for field in entry.values() for value in field.values())
    print('missing translations', missing, flush=True)
