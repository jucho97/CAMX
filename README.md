# CAMX 2026 전시회 업체 탐색

[웹페이지](https://jucho97.github.io/CAMX/) · 2026년 9월 19일 기준 정적 데이터베이스

첫 화면은 CAMX 참가업체의 공개 자료에서 읽히는 복합재 기술 동향을 먼저 제시합니다. 수지·섬유 순환 활용, 성형 효율, 설계 데이터와 AI 운영, 적용 분야별 성능 검증의 네 가지 사례 뒤에 자사 자동차 복합소재와 연결되는 지점을 정리합니다. 구분 필터의 기본 전체에는 2026 참가 업체만 표시하고, 2025 참관 주요 업체 필터에서는 해당 13곳과 2026 명단에서 찾지 못한 4곳을 함께 볼 수 있습니다.

기술 동향 카드의 업체명을 누르면 아래 데이터베이스에서 해당 업체의 조사 내용을 엽니다. 외부 발표 자료 링크는 업체 상세 화면에 보관합니다.

자사 연관 사례로는 [L&L Products](https://www.llproducts.com/articles/addressing-ev-structural-demands-with-advanced-composites/)의 전기차 구조 보강, [Avient](https://www.avient.com/news/avient-accelerates-composite-design-new-simulation-ready-material-cards-and-enhanced-polystrand-thermoplastic-tapes-camx-2026)의 열가소성 테이프·물성 카드, [Trimer](https://trimer-tech.com/markets/)의 빠른 성형 수지를 소개합니다. [ExxonMobil·McCLARIN의 2025 CAMX Combined Strength 수상 기술](https://www.iacmi.org/bright-idea-polyolefin-thermoset-resin-power-performance/)은 자동차 Class-A 복합재 후드입니다. [CAMX 공식 어워즈 페이지](https://www.thecamx.org/awards/)는 ExxonMobil·Fraunhofer ICT의 배터리 구조부품용 FRP 설계를 2026 후보작으로 표시하며, 수상 발표는 9월 22일 예정입니다. 상단 동향은 사례 기반 해석이며 전체 업체의 기술 비중이나 시장 규모를 평가한 결과는 아닙니다.

## 데이터 범위

- [CAMX 2026 공식 디렉터리](https://camx2026.mapyourshow.com/8_0/explore/exhibitor-gallery.cfm)의 505개 항목을 각각 열어 업체명, 부스, 등록 소개, 제품 분류, 회사 링크를 확인했습니다. `ACE Awards`, `CAMX Awards`, `CAMX Exhibitor Lounge`는 업체가 아닌 시상·편의 항목이므로 검색 목록에서 제외해 2026 항목 502개를 표시합니다. 원본 기록은 보관합니다.
- 디렉터리에 회사 링크가 있는 318곳의 개별 사이트를 조회했습니다. 첫 조회에서 280곳에 접근했고 222곳의 공개 소개 문구를 수집했습니다. 설명이 없거나 접속이 실패한 링크 102곳의 본문과 대체 주소를 다시 확인했습니다. 링크가 없는 업체 중 11곳은 회사 공식 자료를 개별 검색으로 확인해 추가했습니다.
- 회사 자료와 산업 분야 근거를 모두 확인한 177곳을 **항공·우주, 자동차, AI** 아래 **소재, 공정, 부품**으로 교차 분류했습니다. 2026년 명단의 나머지 325곳은 구분의 **기타**에 표시하고, 2025년에만 확인된 4곳은 **2025 참관 주요 업체**에서 볼 수 있습니다. 확인이 부족한 상세 카드에는 **정보 부족**으로 표시합니다. 회사 링크가 없고 독립 자료로 확인되지 않은 업체에는 임의의 검색 결과를 연결하지 않았습니다.
- 사용자 제공 2025년 참관 보고서는 **2025 참관 주요 업체** 13곳의 업체명 확인에만 사용했습니다. 이 중 9곳이 2026년 공식 명단에 있고, 4곳은 현재 명단에서 찾지 못했습니다. 보고서의 제품 설명과 비교 내용은 공개 데이터에 넣지 않았습니다.
- 일부 업체의 2026 등록 전시 정보와 최근 발표는 개별 회사 자료를 별도로 확인해 한국어로 요약했습니다. 각 업체 상세 화면에 원문 링크가 있습니다. 최신 발표가 확인되지 않은 업체에 개발 방향을 추정해 쓰지 않았습니다.
- 화면에서 한국어와 영어를 선택할 수 있습니다. 업체 소개·CAMX 등록 문구·제품 분류·추가 조사 메모의 번역문을 정적 데이터로 저장했습니다. 번역문은 원문 링크와 구분해 표시하며 자동 번역의 정확성은 원문에서 확인할 수 있습니다.
- 긴 CAMX 등록 소개 201건은 핵심 기술·제품 문장을 바탕으로 짧은 한국어·영어 요약을 먼저 표시합니다. 전체 등록 번역문은 업체 상세에서 펼칠 수 있고, 검색에는 기존 전체 문구가 계속 포함됩니다. 요약은 `scripts/summarize_camx.py`로 재생성합니다.

## 파일

- `data/official-details.json`: CAMX 상세 페이지 505개에서 수집한 원자료
- `data/company-sites.json`: 개별 회사 사이트의 접근 결과와 공개 메타데이터
- `data/recheck-direct.json`, `data/manual-sources.json`: 설명이 없던 사이트의 재확인 결과와 검증한 회사 공식 자료
- `data/editorial.json`: 독립 출처로 보강한 17개 업체의 한국어 요약
- `data/prior-attendance-2025.json`: 2025년 보고서에서 확인된 업체명만 저장
- `data/research.json`: 사이트가 읽는 통합 데이터 506개 항목
- `data/translations.json`: 한국어·영어 업체별 번역문
- `data/about_summaries.json`: 긴 CAMX 등록 소개의 한국어·영어 요약
- `scripts/enrich_sites.py`, `scripts/recheck_direct.py`, `scripts/build_research.py`, `scripts/translate_profiles.py`: 자료 갱신 스크립트

## 실행

별도 프레임워크가 없는 HTML/CSS/JavaScript 페이지입니다.

```sh
python3 -m http.server 8765
```

브라우저에서 `http://localhost:8765/`를 엽니다. `scripts/build_research.py`를 실행하면 수집 자료에서 통합 JSON을 다시 생성합니다. 데이터가 바뀌면 `scripts/translate_profiles.py`를 실행해 번역 파일도 갱신합니다.
