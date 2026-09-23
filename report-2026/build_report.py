#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess, html

ROOT = Path(__file__).resolve().parent
SRC = Path('/Users/junyeongcho/Desktop/2026 CAMX')
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

images = {
 'airtech-1': 'AIRTECH/IMG_0305.HEIC', 'airtech-2': 'AIRTECH/IMG_0402.HEIC',
 'stm-1': 'STM/IMG_0327.heic', 'stm-2': 'STM/IMG_0328.HEIC',
 'teubert-1': 'CCM Technology by TEUBERT/IMG_0339.HEIC', 'teubert-2': 'CCM Technology by TEUBERT/IMG_0340.HEIC',
 'krempel-1': 'KEMPEL/IMG_0338.HEIC', 'krempel-2': 'KEMPEL/IMG_0416.HEIC',
 'polynt-1': 'Polynt/IMG_0317.HEIC', 'polynt-2': 'Polynt/IMG_0318.HEIC',
 'agci-1': 'AGCI/IMG_0377.HEIC', 'agci-2': 'AGCI/IMG_0376.HEIC',
 'parson-1': 'Parson adhesive/IMG_0380.HEIC', 'parson-2': 'Parson adhesive/IMG_0382.HEIC',
 'kelvinite-1': 'Kelvinite/IMG_0386.HEIC', 'kelvinite-2': 'Kelvinite/IMG_0390.HEIC', 'kelvinite-3': 'Kelvinite/IMG_0391.HEIC',
 'cotton-1': 'Cottontoday/IMG_0332.HEIC', 'cotton-2': 'Cottontoday/IMG_0333.HEIC',
 'exxon-1': 'Exonmobile/IMG_0321.HEIC', 'exxon-2': 'Exonmobile/IMG_0322.HEIC', 'exxon-3': '2026 수상 5_ Exonmobile/IMG_0362.HEIC',
 'mast-1': 'MAST technologies/IMG_0325.HEIC', 'mast-2': 'MAST technologies/IMG_0407.HEIC',
 'vulcan-1': 'Vulcan Shield Global/IMG_0342.HEIC', 'vulcan-2': 'Vulcan Shield Global/IMG_0343.HEIC',
 'andritz-1': 'Andritz/IMG_0371.HEIC', 'andritz-2': 'Andritz/IMG_0372.HEIC',
 'color-1': 'COLOR Master/IMG_0379.HEIC', 'color-2': 'COLOR Master/IMG_0425.HEIC',
 'cropper-1': 'James Cropper/IMG_0395.HEIC', 'cropper-2': '2026 수상 6_James Cropper/IMG_0366.HEIC',
 'toray-1': 'Toray/IMG_0309.HEIC', 'toray-2': 'Toray/IMG_0313.HEIC',
 'rebuild-1': 'RE BUILD/IMG_0331.HEIC', 'rebuild-2': 'RE BUILD/IMG_0403.HEIC',
 'award-1': '2026 수상 1/IMG_0348.HEIC', 'award-2': '2026 수상 2/IMG_0350.HEIC',
 'award-3': '2026 수상 3/IMG_0352.HEIC', 'award-4': '2026 수상 4/IMG_0355.HEIC',
 'award-7': '2026 수상 7/IMG_0368.HEIC',
}

for key, rel in images.items():
    out = ASSETS / f'{key}.jpg'
    if not out.exists():
        subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','82','--resampleHeightWidthMax','1800',str(SRC/rel),'--out',str(out)], check=True, stdout=subprocess.DEVNULL)

companies = [
 dict(key='airtech', name='Airtech International', cat='공정 · 소재 | 항공·우주 / 자동차', booth='AA8', product='복합재 툴링·진공백 공정재', status='공정 안정화', bullets=['BMG Carbon Prepreg 기반 툴링과 고온용 진공백 공정 솔루션을 전시.','대형 부품의 반복 성형에서 치수 안정성과 툴 수명 개선에 초점.','부품 소재 자체보다 양산 공정의 재현성과 보조재 통합 역량이 핵심.'], takeaway='대형 복합재 부품의 양산성 검토 시 툴링 수명·사이클·보조재 표준화를 함께 비교할 필요.', sources='현장 촬영·브로슈어 / airtech.com'),
 dict(key='stm', name='STM · Swift Textile Metalizing', cat='기능성 소재 · 부품 | 자동차 / 항공·우주', booth='—', product='금속도금 섬유 기반 EMI 차폐 시트', status='북미 공급망', bullets=['섬유 한 올씩 금속층을 형성하는 EnCap 공정으로 유연성과 전도성을 동시에 확보.','시트·테이프·직물 형태로 전장 부품과 배터리 주변 EMI/RF 차폐 적용 가능.','100% 북미 현지 생산이라는 점이 조달 안정성과 현지화 측면에서 의미가 큼.'], takeaway='경량 EMI 차폐가 필요한 배터리·전장 하우징에서 금속판 대체 가능성과 성형·접합성을 우선 확인.', sources='현장 촬영 / swift-textile.com'),
 dict(key='teubert', name='Teubert · CCM Technology', cat='공정 · 장비 | 자동차 / 산업', booth='—', product='연속 압축성형(CCM) 장비', status='연속 생산', bullets=['열가소성 필름·UD 테이프·직접 용융 사출을 이용한 연속 프로파일 성형.','곡률·가변 단면을 포함한 복잡 형상과 2단 압축 공정에 대응.','최대 25 bar·500°C, 낮은 기공률을 지향해 연속 생산성과 품질 재현성을 강조.'], takeaway='배터리 프레임·보강재처럼 길이가 긴 부품에서 압출 대비 섬유 연속성과 단면 자유도가 장점.', sources='현장 촬영 / teubert.de/en/composites'),
 dict(key='krempel', name='Krempel', cat='내화 소재 · 부품 | 자동차 / 철도 / 항공·우주', booth='—', product='KremGuard 저연·저독성 프리프레그', status='배터리 안전', bullets=['할로겐·페놀·포름알데히드가 없는 에폭시 프리프레그로 높은 FST 성능을 지향.','구조재와 허니컴 패널에 적용 가능하며 자동차 배터리 하우징 적용을 제시.','난연 규격 대응과 함께 구조 강성·성형성의 균형을 제품군으로 보여줌.'], takeaway='내화 단일 성능보다 구조재 일체화와 저연·저독성까지 포함한 배터리 하우징 평가 기준이 확대됨.', sources='현장 촬영 / krempel.com/en/products/composites/kremguard'),
 dict(key='polynt', name='Polynt', cat='소재 | 자동차', booth='—', product='SMC/BMC 수지·컴파운드', status='양산 소재', bullets=['자동차 외장·구조 부품용 SMC/BMC 소재와 성형 샘플을 전시.','표면 품질, 치수 안정성, 대량 압축성형에 적합한 수지 설계가 중심.','기존 금속 부품의 경량화뿐 아니라 부품 통합과 도장 품질까지 함께 제안.'], takeaway='현행 SMC 양산 기술과 직접 비교 가능한 기준 업체로, 표면·사이클·재활용 대응을 확인할 가치가 큼.', sources='현장 촬영 / polynt.com'),
 dict(key='agci', name='AGCI · Kynol', cat='내화 소재 | 자동차 / 산업', booth='—', product='노볼로이드계 페놀 섬유·분말', status='원가 검토', bullets=['용융되지 않고 수축과 연기 발생이 낮은 Kynol 노볼로이드 섬유를 전시.','섬유·직물·분말 형태로 엘라스토머 및 수지계와의 상용성이 우수.','현장 협의 기준 아라미드 섬유 대비 가격 차이가 크지 않아 경제성 우위는 제한적.'], takeaway='엘라스토머 복합화는 유망하나 동일 성능 기준의 아라미드 대비 원가·가공성 비교가 선행돼야 함.', sources='현장 촬영·상담 / kynol.com'),
 dict(key='parson', name='Parson Adhesives', cat='접착 · 공정 | 자동차 / 산업', booth='—', product='고온 구조용 접착제', status='접합 기술', bullets=['GF–GF, GF–Metal, Metal–Metal 이종재 접합용 구조용 접착제를 전시.','현장 설명 기준 400°F(약 204°C) 이상에서도 접착력 유지 성능을 강조.','기계적 체결을 줄여 경량화와 응력 분산에 유리하나 표면처리·경화 조건 검증이 필요.'], takeaway='배터리 케이스와 복합재 구조물의 이종재 접합 후보로 고온 노화·열사이클 시험을 제안.', sources='현장 촬영·상담 / parsonadhesives.com'),
 dict(key='kelvinite', name='Highland · Kelvinite', cat='내화 소재 · 부품 | 자동차', booth='N12', product='배터리 열폭주 차단용 수지·복합재', status='성능 우수 / 공정 리스크', bullets=['회사 자료상 K2100은 할로겐·안티몬·브롬이 없는 팽창성 FRPP로, 0.25 mm에서 UL 94 VTM-0, 0.43 mm에서 V-0를 충족하며 탄화·무적하 방식으로 화염 장벽을 형성.','Composite Flame Shield는 팽창성층과 구조층을 조합한 다단 차열 구조이며, 회사는 UL 2596 Torch & Grit 10회 전 사이클 통과와 셀 간 열폭주 전파 억제를 제시. K2100/2200 시트·롤, 사출·압출 컴파운드 및 맞춤 복합재로 공급 가능.','기존 사용 경험을 바탕으로 현장에서는 BETR 통과 샘플과 커스터마이징 가능성을 확인. 미국 생산, 회사 기준 4주 리드타임도 공급 측면의 장점.','다만 전시 샘플은 보강 직물 내부에 수지가 거의 침투하지 않아 큰 공극과 층간 불연속이 관찰됨. 내화성은 우수하지만 함침성·접착·성형 재현성·사이클타임은 여전히 양산 병목.'], takeaway='회사 공인 난연·전기 절연 성능과 실제 복합재 제조성은 별도로 평가해야 한다. 다음 단계는 공극률 단면 분석, 수지 유동/점도, 층간강도 및 양산 사이클 검증.', sources='현장 촬영·상담 / Highland Plastics Kelvinite 공식 제품자료(2026-09 확인)'),
 dict(key='cotton', name='Cotton Incorporated', cat='소재 | 자동차', booth='D31', product='면섬유 강화 열가소성 복합재', status='천연섬유', bullets=['면섬유를 PP 등 열가소성 수지의 보강재로 활용한 성형 패널을 전시.','경량, 낮은 열전도, 촉감과 지속가능성을 자동차 내장재 가치로 제시.','표준 성형 공정 적용 가능성을 강조하나 흡습·냄새·장기 내구 관리가 중요.'], takeaway='내장재의 저탄소·감성 품질에는 적합하며, 구조부품보다 비구조 패널에서 우선 검토 가능.', sources='현장 촬영 / cottonworks.com/product-innovation/advanced-materials/'),
 dict(key='exxon', name='ExxonMobil · Proxxima™', cat='수지 · 공정 · 부품 | 자동차', booth='U6', product='저점도 폴리올레핀 열경화 수지·배터리 하우징', status='수상 연계 / 후속 미팅', bullets=['약 20 cP까지 낮춘 2액형 폴리올레핀 열경화 수지로 빠른 함침과 제어 가능한 경화를 제시.','HP-RTM·Wet Compression·Pultrusion 등 다양한 공정과 유리·탄소·천연섬유에 대응.','배터리 하우징과 구조 부품에서 짧은 사이클, 내충격·내약품성을 결합한 적용을 강조.','CAMX Awards 출품 기술로 주목됐으며 다음 주 기술 미팅에서 재료·공정 세부를 확인할 예정.'], takeaway='자동차 복합재의 핵심 병목인 빠른 함침과 사이클 단축을 동시에 겨냥한 우선 검토 대상.', sources='현장 촬영 / proxxima.com / Fraunhofer ICT'),
 dict(key='mast', name='MAST Technologies', cat='기능성 소재 | 항공·우주 / 전자', booth='D19', product='RF 흡수체·EMI 차폐 엘라스토머/폼', status='전자파 대응', bullets=['주파수 대역별 RF 흡수 엘라스토머·폼과 차폐 소재를 전시.','소재 배합부터 시험까지 내부 수행해 응용 조건에 맞춘 커스터마이징을 강조.','레이더·통신·고전압 전장 증가에 따라 구조 복합재와 기능층의 통합 수요를 보여줌.'], takeaway='차폐뿐 아니라 흡수 성능을 설계하는 소재로, 전장 하우징의 주파수별 요구 정의가 먼저 필요.', sources='현장 촬영 / masttechnologies.com'),
 dict(key='vulcan', name='Vulcan Shield Global', cat='내화 소재 | 자동차 / 산업', booth='—', product='연속 알루미나 섬유 직물', status='맞춤 직조', bullets=['약 1,200°C 연속 사용을 목표로 하는 연속 알루미나 섬유 직물을 전시.','평직·능직·3D 직조 등 요구 형상과 중량으로 맞춤 제작 가능.','중국계 공급 배경을 가지면서 싱가포르 본사와 헝가리 유럽 생산 거점을 운영.','배터리 화염 차단층에 적용 가능하나 취급성·수지 함침·원가 검증이 필요.'], takeaway='고온 차단 성능과 맞춤 직조가 강점이며, 자사 공정에 맞는 폭·두께·표면처리 샘플 확보가 우선.', sources='현장 촬영·상담 / vulcanshield.com'),
 dict(key='andritz', name='ANDRITZ Schuler', cat='공정 · 장비 | 자동차 / 항공·우주', booth='D20', product='SMC·GMT·RTM 압축성형 프레스', status='양산 설비', bullets=['SMC·GMT·RTM 부품용 유압 프레스와 턴키 압축성형 시스템을 제시.','공정 데이터 추적, 원격 유지보수, 에너지 모니터링 등 디지털 운영을 통합.','대형 구조 부품에서 압력·온도·평행도 재현성과 자동화가 품질 경쟁력의 중심.'], takeaway='소재 전환만으로는 양산성이 확보되지 않으며, 프레스·이송·추적 시스템을 포함한 셀 단위 최적화가 필요.', sources='현장 촬영 / ANDRITZ Lightweight Technologies brochure'),
 dict(key='color', name='Color Master', cat='첨가제 · 소재 | 자동차', booth='E9', product='난연·가공조제 MB 및 컴파운드', status='샘플 요청', bullets=['색상 농축제와 난연·가공조제 마스터배치, 컴파운드 제품군을 전시.','할로겐·비할로겐 난연 시스템을 수지와 공정 조건에 맞춰 설계 가능.','추후 난연제 및 Processing Aid의 MB·Powder 타입 정보와 샘플을 요청할 계획.'], takeaway='자사 수지·섬유 시스템에서 분산성, 물성 저하, 표면 품질을 비교할 소량 샘플 평가가 적절.', sources='현장 촬영·상담 / color-master.com'),
 dict(key='cropper', name='James Cropper Advanced Materials', cat='기능성 소재 | 자동차 / 항공·우주', booth='EE20', product='TECNOFIRE·EMITEC·재활용 CF UNIMAT', status='2025 연속 관찰 / 수상 연계', bullets=['2025년 참관 주요 업체로, TECNOFIRE 내화재와 EMITEC 전도성 베일의 큰 방향 변화는 없음.','재활용·공정 스크랩 탄소섬유를 정렬한 UNIMAT와 VECTIS 정렬 기술을 전시.','CAMX Awards 출품은 재활용 탄소섬유의 성능 활용도를 높인 정렬형 소재가 핵심.','기존 내화·전도 기능재와 재활용 보강재를 포트폴리오로 묶는 방향이 확인됨.'], takeaway='신규성보다 기술 완성도와 제품군 확장이 의미 있으며, 기존 평가 결과와 연속 비교가 적절.', sources='현장 촬영 / advancedmaterials.jamescropper.com'),
 dict(key='toray', name='Toray Group', cat='소재 · 부품 | 자동차 / 항공·우주', booth='—', product='CFRP 구조재·압력용기·열가소성 복합재', status='적용 확장', bullets=['압력용기 오버랩, 자전거 프레임, 압축성형 판재 등 다양한 CFRP 응용을 전시.','고성능 섬유에서 중간재·성형품까지 연결하는 수직 통합 역량이 강점.','모빌리티에서는 고압 저장·경량 구조와 빠른 성형이 동시에 요구되는 흐름을 보여줌.'], takeaway='단일 소재 성능보다 중간재 형태와 성형 공정까지 포함한 시스템 제안이 대형 공급사의 차별점.', sources='현장 촬영 / toray.com'),
 dict(key='rebuild', name='Re:Build Manufacturing', cat='부품 · 공정 | 자동차 / 항공·우주', booth='—', product='대형 CFRP 구조·자동화 제조', status='대형 부품', bullets=['대형 CFRP 적재함과 구조 부품을 통해 설계·공정·생산 통합 역량을 전시.','대형 부품의 경량화와 부품 수 절감을 실제 형상으로 제시.','재료 공급보다 설계에서 양산 셀까지 연결하는 제조 서비스 모델이 핵심.'], takeaway='대형 자동차 부품의 사업화에는 소재 선정과 동시에 설계·치공구·자동화 파트너 구조가 중요.', sources='현장 촬영 / rebuildmanufacturing.com'),
]

def imgs(key, n=2):
    found=[f'assets/{key}-{i}.jpg' for i in range(1,n+1) if (ASSETS/f'{key}-{i}.jpg').exists()]
    return ''.join(f'<figure><img src="{p}" alt="현장 촬영 사진"><figcaption>CAMX 2026 현장 촬영</figcaption></figure>' for p in found)

def page(content, cls=''):
    return f'<section class="page {cls}">{content}</section>'

summary1 = page('''<header><span class="section-no">01</span><h1>CAMX 2026 종합 요약</h1></header>
<div class="hero"><div><p class="eyebrow">COMPOSITES AND ADVANCED MATERIALS EXPO</p><h2>기술의 중심이<br><b>소재 단품</b>에서 <b>양산 시스템</b>으로 이동</h2><p>배터리 안전, 빠른 성형, 전자파 대응, 저탄소 소재가 각각 독립된 주제가 아니라 하나의 자동차 부품 설계 안에서 결합되는 흐름이 확인됐다.</p></div><div class="hero-stat"><strong>17</strong><span>주요 업체 상세 분석</span><strong>7</strong><span>Awards 출품 기술 검토</span><strong>115</strong><span>현장 사진 전수 확인</span></div></div>
<div class="trend-grid"><article><b>01</b><h3>배터리 열폭주 대응</h3><p>고내열 수지, 알루미나 직물, 내화 프리프레그가 구조재와 결합되는 방향.</p></article><article><b>02</b><h3>고속 함침·연속 생산</h3><p>저점도 수지, HP-RTM, CCM, 자동 압축성형으로 사이클과 재현성을 개선.</p></article><article><b>03</b><h3>EMI·RF 기능 통합</h3><p>금속도금 섬유와 흡수체를 하우징·커버의 기능층으로 통합.</p></article><article><b>04</b><h3>재활용·천연섬유</h3><p>재활용 CF 정렬재와 면섬유 복합재가 성능과 지속가능성을 함께 제시.</p></article></div>
<footer>CAMX 2026 REPORT <span>01</span></footer>''','summary')

summary2 = page('''<header><span class="section-no">02</span><h1>핵심 시사점 및 자사 연관성</h1></header>
<div class="insight-lead"><h2>자사 관점의 우선순위</h2><p>자동차 복합소재의 경쟁력은 난연 등급 하나보다 <b>함침성·사이클·접합·기능층·현지 공급망</b>을 동시에 만족하는지에 의해 결정된다.</p></div>
<table class="priority"><thead><tr><th>우선 검토축</th><th>CAMX에서 확인된 변화</th><th>자사 적용 판단 기준</th><th>관련 업체</th></tr></thead><tbody>
<tr><td><b>배터리 안전</b></td><td>화염 차단재가 구조 부품과 일체화</td><td>열폭주 차단 + 함침 + 생산성</td><td>Kelvinite · Krempel · Vulcan</td></tr>
<tr><td><b>고속 성형</b></td><td>20 cP급 수지와 연속 압축성형</td><td>공극률·2분 이내 사이클·재현성</td><td>ExxonMobil · Teubert · ANDRITZ</td></tr>
<tr><td><b>기능 통합</b></td><td>EMI/RF 시트·흡수체의 구조재 결합</td><td>주파수 성능·성형/접착·북미 조달</td><td>STM · MAST · James Cropper</td></tr>
<tr><td><b>이종재 접합</b></td><td>고온 접착으로 체결부품 축소</td><td>열노화·표면처리·GF/Metal 접착</td><td>Parson Adhesives</td></tr>
<tr><td><b>저탄소 소재</b></td><td>재활용 CF 정렬 및 천연섬유 적용</td><td>기계물성·흡습·원가·공급 안정성</td><td>James Cropper · Cotton Inc.</td></tr></tbody></table>
<div class="decision"><h3>결론</h3><p><b>우선 심화:</b> ExxonMobil, Kelvinite, STM, Vulcan Shield, Parson Adhesives</p><p><b>샘플 평가:</b> Color Master 난연/가공조제, Vulcan 맞춤 직물, STM EMI 시트</p><p><b>비교 관찰:</b> James Cropper는 2025 대비 큰 변화가 없어 연속성 중심으로 관리</p></div>
<footer>CAMX 2026 REPORT <span>02</span></footer>''')

rows=''.join(f'<tr><td>{i:02}</td><td><b>{html.escape(c["name"])}</b></td><td>{html.escape(c["cat"])}</td><td>{html.escape(c["product"])}</td><td><span class="badge">{html.escape(c["status"])}</span></td></tr>' for i,c in enumerate(companies,1))
summary3=page(f'''<header><span class="section-no">03</span><h1>주요 업체 전체 목록</h1></header><p class="subhead">분야별 핵심 업체 17개를 선정해 유첨에서 업체별 1페이지로 정리했다.</p><table class="company-list"><thead><tr><th>No.</th><th>업체</th><th>분야</th><th>핵심 전시</th><th>판단</th></tr></thead><tbody>{rows}</tbody></table><footer>CAMX 2026 REPORT <span>03</span></footer>''')

summary4=page('''<header><span class="section-no">04</span><h1>CAMX Awards 출품 기술</h1></header>
<div class="awards"><div class="award-list"><h2>7개 현장 출품 확인</h2><ol><li><b>Re:Form Composites</b> — 재활용 CFRP 기반 경량 화물 구조</li><li><b>Kaneka Aerospace</b> — 달 표토 기반 소재·제조 개념</li><li><b>Re:Build Manufacturing</b> — 휴대형 보강·자동 수리 시스템</li><li><b>연속 열가소성 복합재</b> — 연속 프로파일 및 링 구조</li><li><b>ExxonMobil Proxxima™</b> — 고속 함침 배터리 하우징</li><li><b>James Cropper UNIMAT</b> — 정렬형 재활용 탄소섬유 소재</li><li><b>Combined Strength</b> — 압력용기·토우 기반 구조</li></ol><div class="note">Awards는 업체 자체가 아니라 기술 출품·선정 프로그램이다. 본 보고서에서는 기술 의미가 큰 ExxonMobil과 James Cropper를 업체 상세 페이지에 연결했다.</div></div><div class="award-photos"><img src="assets/award-1.jpg"><img src="assets/award-3.jpg"><img src="assets/award-7.jpg"></div></div>
<footer>CAMX 2026 REPORT <span>04</span></footer>''')

detail=[]
for idx,c in enumerate(companies,5):
    n=3 if c['key'] in ('kelvinite','exxon') else 2
    bullets=''.join(f'<li>{html.escape(x)}</li>' for x in c['bullets'])
    detail.append(page(f'''<header><span class="section-no">{idx:02}</span><h1>{html.escape(c['name'])}</h1><span class="category">{html.escape(c['cat'])}</span></header>
    <div class="meta"><div><span>부스</span><b>{html.escape(c['booth'])}</b></div><div><span>핵심 제품</span><b>{html.escape(c['product'])}</b></div><div><span>검토 상태</span><b>{html.escape(c['status'])}</b></div></div>
    <div class="detail-grid"><article><h2>확인 내용</h2><ul>{bullets}</ul></article><div class="photos count-{n}">{imgs(c['key'],n)}</div></div>
    <div class="takeaway"><b>TAKE AWAY</b><p>{html.escape(c['takeaway'])}</p></div><div class="sources">Sources: {html.escape(c['sources'])}</div>
    <footer>CAMX 2026 REPORT · APPENDIX <span>{idx:02}</span></footer>''','detail-page'))

css='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e9e6e1;color:#282522;font-family:"Apple SD Gothic Neo","Noto Sans KR",Arial,sans-serif}body{counter-reset:page}.page{width:297mm;height:210mm;margin:12px auto;background:#fff;padding:14mm 16mm 11mm;position:relative;overflow:hidden;page-break-after:always;box-shadow:0 3px 20px #0002}header{height:15mm;display:flex;align-items:center;border-bottom:1.2px solid #c86932;gap:8px}.section-no{font:700 17px Georgia;color:#c45e25;border-right:1px solid #d9b39e;padding-right:9px}h1{font:700 22px Georgia,"Apple SD Gothic Neo";margin:0;letter-spacing:-.4px}.category{margin-left:auto;font-size:10px;color:#7a675c}.eyebrow{color:#b95927;font-size:9px;letter-spacing:1.6px}.hero{display:grid;grid-template-columns:1fr 54mm;gap:18mm;padding:12mm 4mm 8mm}.hero h2{font-size:29px;line-height:1.35;margin:3mm 0}.hero h2 b{color:#bd5b29}.hero p{font-size:12px;line-height:1.65}.hero-stat{border-left:1px solid #d7c9bf;padding-left:9mm;display:grid;grid-template-columns:18mm 1fr;align-items:center}.hero-stat strong{font:700 28px Georgia;color:#bd5b29}.hero-stat span{font-size:9px}.trend-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}.trend-grid article{background:#f5f1ec;padding:5mm;border-top:3px solid #bd5b29}.trend-grid article>b{font:700 14px Georgia;color:#bd5b29}.trend-grid h3{font-size:13px;margin:2mm 0}.trend-grid p{font-size:9.5px;line-height:1.55;margin:0}.insight-lead{padding:6mm 1mm 5mm;border-bottom:1px solid #ddd}.insight-lead h2{font-size:17px;margin:0 0 2mm;color:#b95828}.insight-lead p{font-size:12px;margin:0}.priority,.company-list{width:100%;border-collapse:collapse;margin-top:5mm}.priority th,.company-list th{background:#9f4e27;color:white;font-size:9px;padding:2.4mm}.priority td{font-size:9.2px;padding:3mm;border-bottom:1px solid #ddd}.decision{margin-top:5mm;background:#f5f1ec;padding:4mm 6mm;display:grid;grid-template-columns:18mm 1fr;gap:1mm 5mm}.decision h3{grid-row:1/4;margin:0;color:#b95828}.decision p{font-size:9.5px;margin:0}.subhead{font-size:10px;color:#665b54;margin:4mm 0 0}.company-list{margin-top:3mm}.company-list td{font-size:7.7px;padding:1.45mm 2mm;border-bottom:1px solid #e5e0dc}.company-list td:nth-child(1){text-align:center;color:#b95828}.badge{background:#eee6df;border-radius:10px;padding:1mm 2mm;white-space:nowrap}.awards{display:grid;grid-template-columns:1.2fr 1fr;gap:8mm;padding-top:7mm}.award-list h2{color:#b95828;font-size:17px;margin:0 0 3mm}.award-list ol{margin:0;padding-left:7mm}.award-list li{font-size:9.7px;padding:1.55mm 0;border-bottom:1px solid #eee}.note{font-size:8.5px;line-height:1.5;background:#f3eee9;padding:3mm;margin-top:4mm}.award-photos{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:3mm;height:135mm}.award-photos img{width:100%;height:100%;object-fit:cover}.award-photos img:first-child{grid-row:1/3}.meta{display:grid;grid-template-columns:25mm 1.25fr 1fr;margin-top:5mm;border:1px solid #d8d0ca}.meta div{padding:2.5mm 4mm;border-right:1px solid #ddd}.meta div:last-child{border:0}.meta span{display:block;font-size:7.5px;color:#8d7e75;margin-bottom:1mm}.meta b{font-size:9.5px}.detail-grid{display:grid;grid-template-columns:1fr 105mm;gap:7mm;margin-top:5mm;height:96mm}.detail-grid article{padding:3mm 2mm}.detail-grid h2{font-size:16px;color:#b95828;margin:0 0 4mm}.detail-grid ul{padding-left:6mm;margin:0}.detail-grid li{font-size:10.2px;line-height:1.55;margin-bottom:3.2mm}.photos{display:grid;gap:2.5mm;height:100%}.photos.count-2{grid-template-columns:1fr 1fr}.photos.count-3{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}.photos.count-3 figure:first-child{grid-row:1/3}.photos figure{margin:0;position:relative;overflow:hidden;background:#eee}.photos img{width:100%;height:100%;object-fit:cover}.photos figcaption{position:absolute;bottom:0;left:0;right:0;background:#0008;color:white;font-size:6.5px;padding:1mm 2mm}.takeaway{position:relative;z-index:3;margin-top:4mm;border-top:1.5px solid #b95828;background:#f4efeb;display:grid;grid-template-columns:28mm 1fr;align-items:center;padding:3.2mm 5mm}.takeaway b{font:700 11px Georgia;color:#b95828}.takeaway p{font-size:10px;margin:0;line-height:1.45}.sources{position:absolute;bottom:9mm;left:16mm;font-size:6.5px;color:#958a83}footer{position:absolute;bottom:4mm;left:16mm;right:16mm;border-top:1px solid #d7cec8;padding-top:1.5mm;font:7px Georgia;color:#8c817a}footer span{float:right;color:#b95828}@media print{body{background:white}.page{margin:0;box-shadow:none}}
'''

doc='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 참관 보고서</title><style>'''+css+'''</style></head><body>'''+summary1+summary2+summary3+summary4+''.join(detail)+'''</body></html>'''
(ROOT/'index.html').write_text(doc,encoding='utf-8')
print(f'Wrote {ROOT/"index.html"}: {4+len(companies)} pages, {len(images)} images')
