#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess, html

ROOT = Path(__file__).resolve().parent
SRC = Path('/Users/junyeongcho/Desktop/2026 CAMX')
ASSETS = ROOT / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

images = {
 'airtech-1': 'AIRTECH/IMG_0305.HEIC',
 'stm-1': 'STM/IMG_0327.heic', 'stm-2': 'STM/IMG_0328.HEIC',
 'teubert-1': 'CCM Technology by TEUBERT/IMG_0339.HEIC', 'teubert-2': 'CCM Technology by TEUBERT/IMG_0340.HEIC',
 'krempel-1': 'KEMPEL/IMG_0338.HEIC',
 'polynt-1': 'Polynt/IMG_0317.HEIC',
 'agci-1': 'AGCI/IMG_0377.HEIC', 'agci-2': 'AGCI/IMG_0376.HEIC',
 'parson-1': 'Parson adhesive/IMG_0380.HEIC', 'parson-2': 'Parson adhesive/IMG_0382.HEIC',
 'kelvinite-1': 'Kelvinite/IMG_0386.HEIC', 'kelvinite-2': 'Kelvinite/IMG_0390.HEIC', 'kelvinite-3': 'Kelvinite/IMG_0391.HEIC',
 'cotton-1': 'Cottontoday/IMG_0332.HEIC', 'cotton-2': 'Cottontoday/IMG_0333.HEIC',
 'exxon-1': 'Exonmobile/IMG_0321.HEIC', 'exxon-2': '2026 수상 5_ Exonmobile/IMG_0363.HEIC', 'exxon-3': '2026 수상 5_ Exonmobile/IMG_0364.HEIC',
 'mast-1': 'MAST technologies/IMG_0325.HEIC',
 'vulcan-1': 'Vulcan Shield Global/IMG_0342.HEIC', 'vulcan-2': 'Vulcan Shield Global/IMG_0343.HEIC',
 'andritz-1': 'Andritz/IMG_0371.HEIC',
 'color-1': 'COLOR Master/IMG_0379.HEIC',
 'cropper-1': 'James Cropper/IMG_0395.HEIC', 'cropper-2': '2026 수상 6_James Cropper/IMG_0367.HEIC',
 'toray-1': 'Toray/IMG_0309.HEIC', 'toray-2': 'Toray/IMG_0313.HEIC',
 'rebuild-1': 'RE BUILD/IMG_0331.HEIC',
}

for key, rel in images.items():
    out = ASSETS / f'{key}.jpg'
    if not out.exists():
        subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','82','--resampleHeightWidthMax','1800',str(SRC/rel),'--out',str(out)], check=True, stdout=subprocess.DEVNULL)
for old in ASSETS.glob('*.jpg'):
    if old.stem not in images:
        old.unlink()

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
 dict(key='cropper', name='James Cropper Advanced Materials', cat='기능성 베일 · 내화 소재 · 재활용 탄소섬유', booth='EE20', product='TECNOFIRE® · EMITEC™ · SurfaceTec™ · UNIMAT', status='2025 연속 관찰 / Awards 출품', bullets=['1845년 설립된 첨단 복합소재 및 친환경 패키징 솔루션 기업으로, 전시품은 화재 방호·EMI 차폐·복합재 표면 엔지니어링 소재로 구성.','TECNOFIRE®는 복합재 내부에 함께 성형하는 0.5 mm급 팽창성 화재 방호 매트. 약 450°C에서 초기 두께의 최대 35배까지 팽창해 단열 탄화층을 형성하며 EV 배터리 열폭주·운송·항공 분야에 적용.','EMITEC™은 Ni-Cu 코팅 탄소섬유 베일 기반의 초경량 EMI 차폐재로, 약 60 dB급 차폐 성능을 제시하며 금속 메쉬와 알루미늄 포일 대체를 목표로 함.','SurfaceTec™은 PE·PEI 등 열가소성 기반 표면 베일로, 사용 섬유와 수지 조합에 따라 표면 품질·내마모·기능성을 부여. 2026년에는 재활용 탄소섬유를 정렬한 UNIMAT Awards 출품품도 전시.','2025년 확인 제품군과 비교하면 TECNOFIRE·EMITEC의 기본 방향은 동일하며, 올해는 정렬형 재활용 탄소섬유 기술이 추가된 점이 주요 변화.'], takeaway='', sources='현장 촬영·브로슈어 / James Cropper Advanced Materials 공식자료'),
 dict(key='toray', name='Toray Group', cat='소재 · 부품 | 자동차 / 항공·우주', booth='—', product='CFRP 구조재·압력용기·열가소성 복합재', status='적용 확장', bullets=['압력용기 오버랩, 자전거 프레임, 압축성형 판재 등 다양한 CFRP 응용을 전시.','고성능 섬유에서 중간재·성형품까지 연결하는 수직 통합 역량이 강점.','모빌리티에서는 고압 저장·경량 구조와 빠른 성형이 동시에 요구되는 흐름을 보여줌.'], takeaway='단일 소재 성능보다 중간재 형태와 성형 공정까지 포함한 시스템 제안이 대형 공급사의 차별점.', sources='현장 촬영 / toray.com'),
 dict(key='rebuild', name='Re:Build Manufacturing', cat='부품 · 공정 | 자동차 / 항공·우주', booth='—', product='대형 CFRP 구조·자동화 제조', status='대형 부품', bullets=['대형 CFRP 적재함과 구조 부품을 통해 설계·공정·생산 통합 역량을 전시.','대형 부품의 경량화와 부품 수 절감을 실제 형상으로 제시.','재료 공급보다 설계에서 양산 셀까지 연결하는 제조 서비스 모델이 핵심.'], takeaway='대형 자동차 부품의 사업화에는 소재 선정과 동시에 설계·치공구·자동화 파트너 구조가 중요.', sources='현장 촬영 / rebuildmanufacturing.com'),
]

profiles = {
 'airtech': ('1973년 설립된 복합재 제조 공정용 툴링·진공백 보조재 전문기업으로, 항공·자동차·풍력용 대형 복합재 공정 솔루션을 공급한다.', 'https://airtech.com'),
 'stm': ('Swift Textile Metalizing은 1955년부터 전도성 금속도금 직물을 개발해 온 미국 기업이다. 유연한 직물 특성을 유지하면서 EMI/RF 차폐와 정전기 제어 기능을 구현한다.', 'https://www.swift-textile.com'),
 'teubert': ('독일 Teubert는 입자발포와 복합재 성형 장비를 개발하는 설비 기업이다. 전시에서는 연속섬유 프로파일을 생산하는 CCM 공정과 장비 구성을 소개했다.', 'https://teubert.de/en/composites'),
 'krempel': ('Krempel은 전기 절연재와 고기능 복합재를 공급하는 독일 소재 기업이다. 모빌리티용 난연 구조재와 배터리 보호 부품을 KremGuard 제품군으로 전개한다.', 'https://krempel.com/en/products/composites/kremguard'),
 'polynt': ('Polynt는 불포화 폴리에스터·비닐에스터와 SMC/BMC 컴파운드를 공급하는 글로벌 화학 소재 기업이다. 자동차 대량 압축성형용 소재와 실제 성형 부품을 함께 전시했다.', 'https://www.polynt.com'),
 'agci': ('AGCI가 소개한 Kynol은 노볼로이드계 페놀 섬유 제조사로, 용융하지 않고 탄화하는 내열·난연 섬유와 분말·직물 제품을 공급한다.', 'https://kynol.com'),
 'parson': ('Parson Adhesives는 금속·복합재·플라스틱용 구조용 접착제를 개발하는 미국 기업이다. 전시품은 유리섬유 복합재와 금속의 고온 이종재 접합을 중심으로 구성됐다.', 'https://www.parsonadhesives.com'),
 'kelvinite': ('Highland Plastics의 Kelvinite는 박막에서도 난연성과 전기 절연성을 확보하도록 설계한 FRPP 및 복합재 제품군이다. 시트·롤·컴파운드와 배터리용 다층 Flame Shield를 공급한다.', 'https://highlandplastics.com/materials/kelvinite/'),
 'cotton': ('Cotton Incorporated는 면섬유의 용도를 의류 밖의 산업재로 확장하는 연구·기술 지원 조직이다. CAMX에서는 면섬유를 열가소성 수지 보강재로 사용한 자동차 내장용 성형품을 제시했다.', 'https://cottonworks.com/product-innovation/advanced-materials/'),
 'exxon': ('ExxonMobil Product Solutions의 Proxxima™는 저점도 2액형 폴리올레핀 열경화 수지 플랫폼이다. 빠른 함침과 짧은 경화를 이용해 자동차 구조·배터리 부품의 고속 생산을 목표로 한다.', 'https://www.proxxima.com'),
 'mast': ('MAST Technologies는 RF 흡수체, EMI 차폐재와 열관리 소재를 설계·시험하는 미국 기능성 소재 기업이다. 주파수 조건에 맞춘 엘라스토머·폼·코팅형 제품을 공급한다.', 'https://masttechnologies.com'),
 'vulcan': ('Vulcan Shield Global은 연속 알루미나 섬유와 고온용 직물·테이프를 공급한다. 싱가포르 본사와 헝가리 생산 거점을 기반으로 직조 조직과 치수를 맞춤 설계한다.', 'https://www.vulcanshield.com'),
 'andritz': ('ANDRITZ Schuler는 프레스와 자동화 생산라인을 공급하는 설비 기업이다. 복합재 분야에서는 SMC·GMT·RTM용 유압 프레스와 공정 추적 시스템을 턴키로 제공한다.', 'https://www.andritz.com'),
 'color': ('Color Master는 컬러 농축제와 기능성 첨가제 마스터배치·컴파운드를 제조한다. 전시에서는 난연제와 가공조제를 포함한 맞춤형 농축 솔루션을 소개했다.', 'https://www.color-master.com'),
 'cropper': ('James Cropper Advanced Materials는 탄소섬유·유리섬유 기반 부직포와 기능성 베일을 개발한다. 내화 TECNOFIRE, 전도성 EMITEC, 정렬형 재활용 탄소섬유 UNIMAT가 주요 제품군이다.', 'https://advancedmaterials.jamescropper.com'),
 'toray': ('Toray는 탄소섬유, 프리프레그, 열가소성 복합재와 성형 기술을 공급하는 글로벌 소재 기업이다. 전시에서는 고압 저장용기와 모빌리티 구조재 등 실제 적용품을 폭넓게 제시했다.', 'https://www.toray.com'),
 'rebuild': ('Re:Build Manufacturing은 제품 설계부터 복합재 공정·자동화·생산까지 연결하는 미국 제조 엔지니어링 기업이다. 대형 CFRP 자동차 구조물을 통해 통합 제조 역량을 보여줬다.', 'https://rebuildmanufacturing.com'),
}

enriched = {
 'airtech': ['복합재 툴링과 진공백 성형에 필요한 프리프레그·필름·백·실란트 등 공정재를 공급하는 전문기업.', '전시품은 BMG Carbon Prepreg로 제작한 탄소섬유 툴과 실제 성형 샘플, 고온 성형용 진공백 공정재로 구성.', '탄소섬유 툴은 금속 툴보다 열팽창 거동을 복합재 부품과 가깝게 맞출 수 있어 대형 부품의 반복 성형과 치수 관리에 사용.', '항공·우주, 풍력, 자동차 및 해양 분야의 오토클레이브·OOA·인퓨전 공정에 보조재와 툴링 시스템을 함께 공급.'],
 'stm': ['1955년부터 금속도금 직물을 생산한 미국 기능성 섬유 기업으로, 군수·항공·의료·산업용 EMI/RF 차폐재를 공급.', '전시품은 은 또는 은-니켈을 도금한 직물·부직포·테이프·후크앤루프와 복합재 적층용 얇은 전도성 시트로 구성.', 'EnCap™ 공정은 각 섬유 표면을 금속으로 완전히 감싸는 분자 결합층을 형성해 직물의 유연성·신축성을 유지하면서 반복 가능한 전도성을 확보.', '부직포는 기재와 코팅에 따라 약 2.0–5.0 oz/yd²이며, 전도성 후크앤루프는 회사 자료상 체적저항 0.02 Ω·cm를 제시.', '현장 설명 기준 전 제품을 북미에서 생산하며, 항공 복합재 통합·EMI 가스켓·케이블 랩·장비 하우징·정전기 방지에 적용.'],
 'teubert': ['독일의 입자발포·복합재 성형설비 기업으로, 연속섬유 열가소성 프로파일을 생산하는 CCM 장비와 성형 샘플을 전시.', 'Continuous Compression Molding은 필름·UD 테이프 또는 직접 용융 수지를 연속 공급해 가열과 압축을 단계적으로 수행.', '직선 프로파일뿐 아니라 곡률, 가변 단면, 국부 보강이 포함된 복잡 형상 샘플을 통해 기존 인발성형과 다른 형상 자유도를 제시.', '회사 자료상 최대 25 bar·500°C 조건과 1% 미만 기공률을 목표로 하며, 장척 보강재·프레임·구조 프로파일 생산에 적용.'],
 'krempel': ['전기 절연재와 고기능 복합재를 공급하는 독일 기업으로, 난연 프리프레그 KremGuard와 복합재 튜브·패널 샘플을 전시.', 'KremGuard는 에폭시계 프리프레그로 할로겐·페놀·포름알데히드 없이 높은 화염·연기·독성(FST) 성능을 확보하도록 설계.', '회사 자료에는 FAR 25, AITM, EN 45545 HL3 및 UL 94 V-0 등 운송 분야 난연 요구에 대응하는 제품군이 제시됨.', '허니컴 패널, 전기 절연 구조재, 철도·항공 내장재와 배터리 하우징처럼 구조 성능과 화재 안전을 함께 요구하는 부품에 적용.'],
 'polynt': ['불포화 폴리에스터·비닐에스터·특수수지와 SMC/BMC를 공급하는 글로벌 복합재 소재 기업.', '전시품은 압축성형한 자동차 외장·구조 부품과 표면 품질을 보여주는 SMC 샘플로 구성.', 'Polynt SMC는 불포화 폴리에스터·비닐에스터 또는 에폭시 수지에 무기 충전재와 유리·탄소섬유를 조합한 성형용 시트이며, 공급 폭은 회사 자료상 약 135–150 cm.', 'SMCarbon®은 탄소섬유 강화 에폭시·비닐에스터 SMC 제품군으로 강성·경량·열적 안정성을 목표로 함.', '배터리 커버·하우징용 SMC에는 저수축·유리/탄소섬유 구성이 제시되며, 외관 부품에는 Class-A 표면용 저수축 첨가제 시스템을 적용.'],
 'agci': ['Kynol®은 노볼로이드계 페놀 섬유를 생산하는 소재 브랜드로, 열에 녹아 흐르지 않고 탄화하는 내열·난연 특성이 핵심.', '전시품은 Kynol 단섬유·분말·직물과 페놀계 적층판, 탄화 소재 샘플로 구성.', '섬유·펠트·직물은 화염 차단과 단열, 분말은 수지·고무 조성물의 난연 및 마찰재 충전용으로 사용할 수 있음.', '현장 담당자는 엘라스토머와의 상용성을 장점으로 설명했으나, 아라미드 섬유와 비교해 가격 차이가 크지 않아 원가 우위는 제한적.', '방화복·고온 필터·단열재·마찰재·가스켓 및 복합재 난연층에 적용.'],
 'parson': ['금속·복합재·플라스틱용 2액형 구조용 접착제를 개발하는 미국 기업으로, Partite®와 Parbond® 제품군을 운영.', '전시품은 GF–GF 적층판 접착 샘플과 카트리지형 접착제, 이종재 접합 조건을 정리한 시험 자료로 구성.', '현장 설명 기준 GF–GF, GF–Metal, Metal–Metal 조합에서 400°F(약 204°C) 이상까지 접착 성능 유지를 강조.', '메타크릴레이트계 구조용 접착제는 별도 기계 체결을 줄이고 넓은 면적에 하중을 분산할 수 있으며, 대형 패널·차량·선박·산업 구조물에 적용.', '실제 적용 전에는 피착재별 표면처리, 접착층 두께, 경화시간과 고온·습열 노화 조건의 확인이 필요.'],
 'kelvinite': ['Highland Plastics의 난연 폴리프로필렌 및 복합재 제품군으로, 박막 시트·롤·사출/압출 컴파운드와 배터리용 Flame Shield를 공급.', 'K2100은 할로겐·안티몬·브롬이 없는 팽창성 FRPP. 회사 자료상 0.25 mm에서 UL 94 VTM-0, 0.43 mm에서 V-0이며 탄화·무적하 방식으로 화염 장벽을 형성.', 'Composite Flame Shield는 팽창성층과 구조층을 조합한 다단 차열재로, 회사는 UL 2596 Torch & Grit 10회 전 사이클 통과와 셀 간 열폭주 전파 억제를 제시.', '기존 사용 경험과 현장 설명을 통해 BETR 통과 샘플, 맞춤 설계, 미국 생산 및 회사 기준 약 4주 리드타임을 확인.', '반면 전시 복합재 샘플에서는 보강 직물 내부 미함침과 큰 공극·층간 불연속이 관찰돼 내화 성능과 별개로 함침성·접착·생산성 검증이 필요.'],
 'cotton': ['미국 면화 산업의 연구·기술 지원 조직으로, 면섬유를 의류 밖의 산업용 복합재 보강재로 확장하는 개발을 수행.', '전시품은 면섬유와 PP를 조합해 압축성형한 트레이·판재·자동차 내장 형상 샘플로 구성.', '면섬유의 낮은 밀도와 열전도도, 촉감, 재생 가능한 원료라는 특성을 활용하며 일반적인 열가소성 성형 공정 적용 가능성을 제시.', '도어트림·트렁크 라이너·패키지 트레이 등 비구조 내장재가 대표 적용처이며, 흡습·냄새·치수 안정성과 장기 내구가 평가 항목.'],
 'exxon': ['ExxonMobil Product Solutions의 Proxxima™는 저점도 2액형 폴리올레핀 열경화 수지 플랫폼으로, 빠른 함침과 제어 가능한 경화를 목표로 함.', '전시품은 TFP 보강재와 HP-RTM으로 제작한 EV 배터리 하우징, 구조 패널 및 공정 개념 샘플로 구성.', '회사·Fraunhofer 자료상 점도는 약 20 cP까지 낮출 수 있으며, HP-RTM·VARTM·Wet Compression·Pultrusion·Filament Winding에 적용 가능.', '유리·탄소·천연섬유에 대응하고 내충격·내약품·저흡습 특성을 제공하며, 일부 공정은 2분 이내 경화 가능성을 제시.', 'CAMX Awards 출품 기술로 소개됐으며 배터리 케이스 세부 적층·사이클·접합 기술은 다음 주 후속 미팅에서 확인 예정.'],
 'mast': ['RF 흡수체·EMI 차폐재·열관리 소재를 설계하고 자체 시험하는 AS9100D 인증 미국 기업.', '전시품은 자성 충전 실리콘 시트, 탄소 충전 폼, 표면파 흡수체와 접착형 RF 흡수 샘플로 구성.', 'MF11 탄소 충전 망상 폼은 두께별 1–40 GHz 대역을 대응하며 0.375–1.25 in 규격과 PSA 부착 옵션을 제공.', 'MR11 tuned-frequency 시트는 1–40 GHz 범위에서 특정 공진 주파수에 맞춰 조성·두께를 설계하며 일반적으로 약 20 dB 감쇠를 목표로 함.', '안테나·레이돔·전자장비 하우징·항공 구조 내부의 반사파, 공진과 안테나 간 간섭 저감에 적용.'],
 'vulcan': ['연속 알루미나 섬유와 고온용 직물·테이프·3D 직조품을 공급하는 소재 기업으로, 싱가포르 본사와 헝가리 유럽 생산 거점을 운영.', '전시품은 연속 알루미나 섬유 토우, 평직·능직 직물과 두께가 다른 고온 차단용 섬유 샘플로 구성.', '공식 규격은 약 1,200°C 연속 사용, 폭 0.8–1.2 m, 면중량 180–1,600 g/m²를 제시하며 3D 직물은 약 0.8–10 mm 두께까지 설계 가능.', '현장 설명 기준 요구 폭·두께·직조 조직으로 맞춤 제작할 수 있고 유럽 및 싱가포르 공급망을 통해 고온 단열·화염 차단 구조에 적용.', '세라믹계 연속섬유 특성상 절곡·취급성, 수지 함침 및 가공비는 실제 적층 샘플로 확인할 필요.'],
 'andritz': ['ANDRITZ Schuler는 금속·복합재 성형 프레스와 자동화 라인을 공급하는 글로벌 설비 기업.', '전시품은 대형 경량 구조 부품과 SMC·GMT·RTM용 유압 압축성형 프레스의 턴키 생산 개념.', '브로슈어는 섬유강화 플라스틱이 동등한 강재 부품보다 최대 약 50% 경량화될 수 있다고 설명하며, 압력·평행도·온도 재현성을 핵심 장비 성능으로 제시.', 'Metris Track & Trace는 부품 ID와 원재료·공정·품질 데이터를 연결하고, Energy Monitor는 부품·금형·설비 상태별 에너지 사용량을 분석.', '자동차 대형 SMC/GMT 구조물, 항공 복합재와 고속 RTM 생산라인에 프레스·이송·데이터 시스템을 통합 적용.'],
 'color': ['컬러 농축제, 기능성 첨가제 마스터배치와 맞춤 컴파운드를 제조하는 미국 소재 기업.', '전시품은 수지별 색상·첨가제 농축 펠릿 샘플과 난연·가공조제 제품군으로 구성.', '난연 농축제는 할로겐계와 비할로겐계 시스템을 제공하며 폴리올레핀·스티렌계 및 일부 엔지니어링 플라스틱의 공정 조건에 맞춰 조정 가능.', '마스터배치는 분말 직접 투입보다 계량·분산과 작업환경 관리에 유리하지만, 섬유강화 수지에서는 점도·물성·표면 품질 변화 확인이 필요.', '추후 난연제와 Processing Aid의 MB 및 Powder 타입 기술자료와 샘플을 공급받아 비교할 계획.'],
 'cropper': ['1845년 설립된 첨단 복합소재 및 친환경 패키징 솔루션 기업으로, 전시품은 화재 방호·EMI 차폐·복합재 표면 엔지니어링 소재로 구성.', 'TECNOFIRE®는 복합재 내부에 함께 성형하는 0.5 mm급 팽창성 화재 방호 매트. 약 450°C에서 초기 두께의 최대 35배까지 팽창해 단열 탄화층을 형성.', 'EMITEC™은 Ni-Cu 코팅 탄소섬유 베일 기반의 초경량 EMI 차폐재로 약 60 dB급 차폐 성능을 제시하며 금속 메쉬와 알루미늄 포일 대체를 목표로 함.', 'SurfaceTec™은 PE·PEI 등 열가소성 기반 표면 베일로, 사용 섬유와 수지 조합에 따라 표면 품질·내마모·기능성을 부여.', '2025년 대비 TECNOFIRE·EMITEC의 큰 변화는 없으며, 2026년에는 재활용 탄소섬유를 정렬한 UNIMAT/VECTIS 기술이 CAMX Awards 출품품으로 추가.'],
 'toray': ['탄소섬유·프리프레그·열가소성 복합재와 성형·해석 기술을 공급하는 글로벌 첨단소재 기업.', '전시품은 CFRP 오버랩 압력용기, 자전거 프레임, 압축성형 판재와 항공·모빌리티 구조 샘플로 구성.', 'TORAYCA® regular tow·Z600, ZOLTEK™ PX35 large tow, 직물, 열경화/열가소성 프리프레그, CF-SMC 등 다양한 중간재를 공급.', 'High-cycle RTM, 오토클레이브·OOA, 프레스·사출·필라멘트 와인딩에 대응하며 드레이핑과 CF-SMC 유동 해석도 함께 제공.', '고압 수소 저장용기, 항공 구조, UAM, 스포츠 부품과 자동차 구조재에 적용하며 소재·공정·평가를 통합 개발.'],
 'rebuild': ['제품 설계·재료·복합재 공정·자동화·생산을 통합 제공하는 미국 제조 엔지니어링 기업.', '전시품은 대형 CFRP 픽업트럭 적재함과 경량 구조 패널, 휴대형 복합재 보강·수리 기술로 구성.', '대형 일체형 구조를 통해 금속 조립체의 부품 수와 체결부를 줄이고 형상 자유도와 경량화를 확보하는 제조 방식을 제시.', '항공·방산·모빌리티 분야에서 시제품 이후의 공정 설계, 치공구, 자동화 셀과 양산 이관까지 지원.', 'CAMX Awards 출품에서는 현장 적용이 가능한 보강·수리 시스템과 공정 자동화 개념을 함께 소개.'],
}

section_map = {
 'krempel':'난연·내화 소재', 'agci':'난연·내화 소재', 'kelvinite':'난연·내화 소재',
 'vulcan':'난연·내화 소재', 'cropper':'난연·내화 소재',
 'stm':'EMI·RF 기능성 소재', 'mast':'EMI·RF 기능성 소재',
 'polynt':'수지·컴파운드·천연소재', 'cotton':'수지·컴파운드·천연소재',
 'exxon':'수지·컴파운드·천연소재', 'color':'수지·컴파운드·천연소재',
 'airtech':'성형 공정·설비', 'teubert':'성형 공정·설비', 'andritz':'성형 공정·설비',
 'parson':'접착·조립',
 'toray':'구조부품·항공우주 응용', 'rebuild':'구조부품·항공우주 응용',
}
section_order = ['난연·내화 소재','EMI·RF 기능성 소재','수지·컴파운드·천연소재','성형 공정·설비','접착·조립','구조부품·항공우주 응용']
company_order = ['krempel','agci','kelvinite','vulcan','cropper','stm','mast','polynt','cotton','exxon','color','airtech','teubert','andritz','parson','toray','rebuild']
companies.sort(key=lambda c: company_order.index(c['key']))

captions = {
 'agci-1':'Kynol® 노볼로이드 내열·난연 섬유 직물', 'agci-2':'Kynol® 페놀계 적층판 및 성형 샘플',
 'airtech-1':'BMG Carbon Prepreg 기반 복합재 툴 샘플',
 'stm-1':'금속도금 직물 기반 EMI 차폐 시트', 'stm-2':'테이프·부직포·직물형 전도성 차폐 소재',
 'teubert-1':'CCM Double-stage 공정의 복잡 단면 프로파일', 'teubert-2':'연속 압축성형 장척 구조 프로파일',
 'krempel-1':'KremGuard 난연 복합재 성형 샘플',
 'polynt-1':'SMC 압축성형 외장·구조 부품 샘플',
 'parson-1':'GF–GF 구조용 접착 시험 샘플', 'parson-2':'Partite® 구조용 접착제 제품 샘플',
 'kelvinite-1':'Torch 시험 후 탄화된 Kelvinite Flame Shield', 'kelvinite-2':'Kelvinite 보강 직물 복합재 샘플', 'kelvinite-3':'Kelvinite 다층 차열 판재 샘플',
 'cotton-1':'면섬유 강화 열가소성 압축성형 트레이', 'cotton-2':'면섬유–PP 내장용 성형 패널',
 'exxon-1':'Proxxima™ 수지 적용 EV 배터리 하우징', 'exxon-2':'Proxxima™ 배터리 구조부품 단면', 'exxon-3':'CAMX Awards 출품 배터리 케이스 샘플',
 'mast-1':'RF 흡수 엘라스토머·탄소 충전 폼 샘플',
 'vulcan-1':'연속 알루미나 섬유 직물 샘플', 'vulcan-2':'고온용 알루미나 섬유 토우·직조 샘플',
 'andritz-1':'압축성형 대형 경량 복합재 구조부품',
 'color-1':'Color Master 색상·기능성 마스터배치 펠릿',
 'cropper-1':'TECNOFIRE® 팽창 단계별 화재 방호 샘플', 'cropper-2':'UNIMAT 정렬형 재활용 탄소섬유 성형품',
 'toray-1':'CFRP 필라멘트 와인딩 압력용기', 'toray-2':'Toray 탄소섬유 적용 CFRP 프레임',
 'rebuild-1':'Re:Build 대형 CFRP 일체형 구조 패널',
}

def imgs(key, n=2):
    found=[f'assets/{key}-{i}.jpg' for i in range(1,n+1) if f'{key}-{i}' in images]
    return ''.join(f'<figure><img src="{p}" alt="{html.escape(captions[p.split("/")[-1].removesuffix(".jpg")])}"><figcaption>{html.escape(captions[p.split("/")[-1].removesuffix(".jpg")])}</figcaption></figure>' for p in found)

def page(content, cls=''):
    return f'<section class="page {cls}">{content}</section>'

summary1 = page('''<div class="contents-page"><aside><div class="contents-rule"></div><h1>Contents</h1><div class="contents-rule bottom"></div></aside><main><div class="report-title">▣ CAMX2026 출장 보고서</div><ol><li>Executive Summary</li><li>전시 개요 및 산업 Trend 확인</li><li>주요 전시 업체 요약</li></ol><div class="annex">[유첨]<br>－ 부스 방문 보고서 (17개 업체)</div><div class="company-name">한화첨단소재</div><div class="report-date">2026. 9.</div></main></div>''', 'template-page cover-template')

summary2 = page('''<div class="legacy-head"><span></span><b>1</b><h1>Executive Summary</h1></div><div class="legacy-body executive-placeholder"><ul><li>CAMX 2026 전시 전반의 핵심 내용 요약</li><li>주요 전시 작품 확인 결과 및 기술적 특징</li><li>참관 세미나의 핵심 발표 내용과 산업적 의미</li><li>복합재 소재·공정·부품 분야의 주요 기술 변화</li><li>주요 수상작과 신규 전시 기술</li><li>추가 검토 및 후속 협의가 필요한 기술</li></ul><div class="draft-note">※ 전시 작품 및 세미나 확인 후 내용 보완 예정</div></div><div class="legacy-page-no">1/3</div>''', 'template-page legacy-template')

summary3 = page('''<div class="legacy-head"><span></span><b>2</b><h1>전시 개요 및 산업 Trend 확인</h1></div><div class="legacy-body overview-template"><section><h2>CAMX 2026 개요</h2><ul><li>행사 명: CAMX (Composites and Advanced Materials Expo)</li><li>일정 / 장소: Conference 2026년 9월 21–24일 / Exhibition 9월 22–24일<br>Georgia World Congress Center, Atlanta, Georgia</li><li>주최 / 주관: ACMA &amp; SAMPE</li><li>성격 / 규모: 북미 최대 복합재·첨단소재 전시회 / 약 500개 전시업체</li><li>프로그램 구성: 전시·기술 컨퍼런스·CAMX Awards·현장 시연</li></ul><div class="camx-logo">CAM<span>X</span></div></section><section><h2>시장 환경 변화에 따른 산업 Trend</h2><ul class="trend-placeholder"><li>전시 작품 확인 후 주요 소재·공정·부품 기술 동향 보완</li><li>세미나 발표 내용을 기반으로 시장·규제·응용 분야 변화 보완</li><li>CAMX Awards 및 주요 신규 기술의 공통 방향 보완</li></ul><div class="draft-note">※ 2026년 9월 23일 추가 참관 내용 반영 예정</div></section></div><div class="legacy-page-no">2/3</div>''', 'template-page legacy-template')

rows=''.join(f'<tr><td>{i:02}</td><td><b>{html.escape(c["name"])}</b></td><td>{html.escape(section_map[c["key"]])}</td><td>{html.escape(c["product"])}</td><td><span class="badge">{html.escape(c["status"])}</span></td></tr>' for i,c in enumerate(companies,1))
summary_company=page(f'''<header><span class="section-no">03</span><h1>주요 전시 업체 요약</h1></header><p class="subhead">6개 대표 Section으로 구분했으며, 각 업체의 세부 적용 산업은 유첨에서 별도로 표시했다.</p><table class="company-list"><thead><tr><th>No.</th><th>업체</th><th>대표 Section</th><th>핵심 전시</th><th>비고</th></tr></thead><tbody>{rows}</tbody></table><footer>CAMX 2026 REPORT <span>03</span></footer>''')

detail=[]
for idx,c in enumerate(companies,5):
    requested=3 if c['key'] in ('kelvinite','exxon') else 2
    n=sum(1 for i in range(1,requested+1) if f"{c['key']}-{i}" in images)
    bullets=''.join(f'<li>{html.escape(x)}</li>' for x in enriched.get(c['key'],c['bullets']))
    profile, website = profiles[c['key']]
    detail.append(page(f'''<header><span class="section-no">{idx:02}</span><h1>{html.escape(c['name'])}</h1><span class="category">SECTION · {html.escape(section_map[c['key']])}</span></header>
    <div class="meta"><div><span>부스</span><b>{html.escape(c['booth'])}</b></div><div><span>핵심 전시품</span><b>{html.escape(c['product'])}</b></div><div><span>회사 홈페이지</span><b><a href="{html.escape(website)}" target="_blank">{html.escape(website.replace('https://','').replace('http://','').rstrip('/'))}</a></b></div></div>
    <div class="detail-grid"><article><h2>업체 개요</h2><p class="company-profile">{html.escape(profile)}</p><h2>전시품 및 기술 내용</h2><ul>{bullets}</ul></article><div class="photos count-{n}">{imgs(c['key'],n)}</div></div>
    <div class="sources">근거: {html.escape(c['sources'])}</div>
    <footer>CAMX 2026 REPORT · APPENDIX <span>{idx:02}</span></footer>''','detail-page'))

css='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e9e6e1;color:#282522;font-family:"Apple SD Gothic Neo","Noto Sans KR",Arial,sans-serif}body{counter-reset:page}.page{width:297mm;height:210mm;margin:12px auto;background:#fff;padding:14mm 16mm 11mm;position:relative;overflow:hidden;page-break-after:always;box-shadow:0 3px 20px #0002}header{height:15mm;display:flex;align-items:center;border-bottom:1.2px solid #c86932;gap:8px}.section-no{font:700 17px Georgia;color:#c45e25;border-right:1px solid #d9b39e;padding-right:9px}h1{font:700 22px Georgia,"Apple SD Gothic Neo";margin:0;letter-spacing:-.4px}.category{margin-left:auto;font-size:10px;color:#7a675c}.eyebrow{color:#b95927;font-size:9px;letter-spacing:1.6px}.hero{display:grid;grid-template-columns:1fr 54mm;gap:18mm;padding:12mm 4mm 8mm}.hero h2{font-size:29px;line-height:1.35;margin:3mm 0}.hero h2 b{color:#bd5b29}.hero p{font-size:12px;line-height:1.65}.hero-stat{border-left:1px solid #d7c9bf;padding-left:9mm;display:grid;grid-template-columns:18mm 1fr;align-items:center}.hero-stat strong{font:700 28px Georgia;color:#bd5b29}.hero-stat span{font-size:9px}.trend-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}.trend-grid article{background:#f5f1ec;padding:5mm;border-top:3px solid #bd5b29}.trend-grid article>b{font:700 14px Georgia;color:#bd5b29}.trend-grid h3{font-size:13px;margin:2mm 0}.trend-grid p{font-size:9.5px;line-height:1.55;margin:0}.insight-lead{padding:6mm 1mm 5mm;border-bottom:1px solid #ddd}.insight-lead h2{font-size:17px;margin:0 0 2mm;color:#b95828}.insight-lead p{font-size:12px;margin:0}.priority,.company-list{width:100%;border-collapse:collapse;margin-top:5mm}.priority th,.company-list th{background:#9f4e27;color:white;font-size:9px;padding:2.4mm}.priority td{font-size:9.2px;padding:3mm;border-bottom:1px solid #ddd}.decision{margin-top:5mm;background:#f5f1ec;padding:4mm 6mm;display:grid;grid-template-columns:18mm 1fr;gap:1mm 5mm}.decision h3{grid-row:1/4;margin:0;color:#b95828}.decision p{font-size:9.5px;margin:0}.subhead{font-size:10px;color:#665b54;margin:4mm 0 0}.company-list{margin-top:3mm}.company-list td{font-size:7.7px;padding:1.45mm 2mm;border-bottom:1px solid #e5e0dc}.company-list td:nth-child(1){text-align:center;color:#b95828}.badge{background:#eee6df;border-radius:10px;padding:1mm 2mm;white-space:nowrap}.awards{display:grid;grid-template-columns:1.2fr 1fr;gap:8mm;padding-top:7mm}.award-list h2{color:#b95828;font-size:17px;margin:0 0 3mm}.award-list ol{margin:0;padding-left:7mm}.award-list li{font-size:9.7px;padding:1.55mm 0;border-bottom:1px solid #eee}.note{font-size:8.5px;line-height:1.5;background:#f3eee9;padding:3mm;margin-top:4mm}.award-photos{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:3mm;height:135mm}.award-photos img{width:100%;height:100%;object-fit:cover}.award-photos img:first-child{grid-row:1/3}.meta{display:grid;grid-template-columns:25mm 1.25fr 1fr;margin-top:5mm;border:1px solid #d8d0ca}.meta div{padding:2.5mm 4mm;border-right:1px solid #ddd}.meta div:last-child{border:0}.meta span{display:block;font-size:7.5px;color:#8d7e75;margin-bottom:1mm}.meta b{font-size:9.5px}.detail-grid{display:grid;grid-template-columns:1fr 105mm;gap:7mm;margin-top:5mm;height:96mm}.detail-grid article{padding:3mm 2mm}.detail-grid h2{font-size:16px;color:#b95828;margin:0 0 4mm}.detail-grid ul{padding-left:6mm;margin:0}.detail-grid li{font-size:10.2px;line-height:1.55;margin-bottom:3.2mm}.photos{display:grid;gap:2.5mm;height:100%}.photos.count-1{grid-template-columns:1fr}.photos.count-2{grid-template-columns:1fr 1fr}.photos.count-3{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}.photos.count-3 figure:first-child{grid-row:1/3}.photos figure{margin:0;position:relative;overflow:hidden;background:#eee}.photos img{width:100%;height:100%;object-fit:cover}.photos figcaption{position:absolute;bottom:0;left:0;right:0;background:#0008;color:white;font-size:6.5px;padding:1mm 2mm}.takeaway{position:relative;z-index:3;margin-top:4mm;border-top:1.5px solid #b95828;background:#f4efeb;display:grid;grid-template-columns:28mm 1fr;align-items:center;padding:3.2mm 5mm}.takeaway b{font:700 11px Georgia;color:#b95828}.takeaway p{font-size:10px;margin:0;line-height:1.45}.sources{position:absolute;bottom:9mm;left:16mm;font-size:6.5px;color:#958a83}footer{position:absolute;bottom:4mm;left:16mm;right:16mm;border-top:1px solid #d7cec8;padding-top:1.5mm;font:7px Georgia;color:#8c817a}footer span{float:right;color:#b95828}.template-page{font-family:Georgia,"Apple SD Gothic Neo",serif}.cover-template{padding:0}.contents-page{height:100%;display:grid;grid-template-columns:42% 58%}.contents-page aside{background:#f8f5f2;padding:31mm 11mm}.contents-rule{height:1px;background:#e97731;width:100%;margin-bottom:2mm}.contents-rule.bottom{margin-top:18mm}.contents-page aside h1{font:700 37px Arial;color:#ed752d;margin:0}.contents-page main{position:relative;padding:44mm 20mm}.report-title{background:#f8e0cf;padding:10mm 5mm;font-size:24px;box-shadow:2px 2px 5px #0003}.contents-page ol{font-size:14px;line-height:2.15;margin:5mm 0 0;padding-left:11mm}.annex{font-size:13px;line-height:2;margin:10mm 0 0 10mm}.company-name{position:absolute;bottom:24mm;left:33mm;font-size:11px}.report-date{position:absolute;bottom:19mm;right:17mm;font-size:11px}.legacy-head{height:16mm;margin:7mm 4mm 0;display:flex;align-items:center;border-bottom:1.5px solid #ef7a31}.legacy-head>span{width:3mm;height:8mm;background:#ef7a31;margin-right:2mm}.legacy-head>b{background:#ef7a31;color:white;border-radius:50%;width:8mm;height:8mm;text-align:center;line-height:8mm;font-size:9px}.legacy-head h1{font-size:18px;font-weight:400}.legacy-body{padding:9mm 17mm}.executive-placeholder ul{font-size:13px;line-height:2.15;margin:0}.executive-placeholder li{padding-left:3mm}.draft-note{margin-top:8mm;color:#a4978f;font-size:10px;background:#f6f2ef;padding:4mm}.legacy-page-no{position:absolute;right:18mm;bottom:12mm;font-size:8px}.overview-template section{position:relative;margin-bottom:6mm}.overview-template h2{font-size:13px;font-weight:400;border-left:3px solid #ef7a31;padding-left:3mm}.overview-template ul{font-size:10.5px;line-height:1.75;margin:2mm 0;padding-left:7mm}.camx-logo{position:absolute;right:10mm;top:9mm;background:#173a61;color:white;font:bold 30px Arial;padding:2mm 4mm}.camx-logo span{color:#ee9920}.trend-placeholder li{border-bottom:1px dotted #d3cbc5;padding:2mm 0}.meta{grid-template-columns:24mm 1.25fr 1fr}.meta a{color:#8f421f;text-decoration:none}.detail-grid{height:121mm;grid-template-columns:1fr 102mm;margin-top:4mm}.detail-grid article{padding:1mm 2mm}.detail-grid h2{font-size:13px;margin:0 0 2mm}.detail-grid h2:nth-of-type(2){margin-top:4mm}.company-profile{font-size:10.1px;line-height:1.62;margin:0;background:#f6f2ef;padding:3mm 4mm;border-left:2px solid #c86932}.detail-grid ul{padding-left:5mm}.detail-grid li{font-size:9.7px;line-height:1.56;margin-bottom:2.5mm}.photos{align-content:stretch}.photos figure{background:#f2f0ed}.photos img{object-fit:contain;background:#f2f0ed}.photos.count-1{grid-template-columns:1fr}.photos.count-2{grid-template-columns:1fr 1fr}.photos.count-3{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}.sources{bottom:9mm}.takeaway{display:none}@media print{body{background:white}.page{margin:0;box-shadow:none}}
'''

doc='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 참관 보고서</title><style>'''+css+'''</style></head><body>'''+summary1+summary2+summary3+summary_company+''.join(detail)+'''</body></html>'''
(ROOT/'index.html').write_text(doc,encoding='utf-8')
print(f'Wrote {ROOT/"index.html"}: {4+len(companies)} pages, {len(images)} images')
