#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static CAMX report from reviewed content and original photo assets."""
from pathlib import Path
import html,json
from card_layout import card_html,CARD_SCRIPT
R=Path(__file__).resolve().parent
e=html.escape
C=json.loads((R/'report-data.json').read_text())
F=json.loads((R/'frontmatter.json').read_text())
sections=list(dict.fromkeys(c['section'] for c in C))
def page(s,cls='',id=''):return f'<section class="page {cls}" id="{id}">{s}</section>'

def sample_html(p):
 x,y,w,h=p.get('frame',[0,0,1,1]);ih=1000/p['imageRatio']
 view=f'{x*1000:.3f} {y*ih:.3f} {w*1000:.3f} {h*ih:.3f}'
 image=f'<image href="{e(p["src"])}" width="1000" height="{ih}"/>'
 if p.get('rotate')==-90:
  view=f'0 0 {h*ih:.3f} {w*1000:.3f}'
  image=f'<g transform="translate(0 {w*1000}) rotate(-90) translate({-x*1000} {-y*ih})">{image}</g>'
 vx,vy,vw,vh=view.split();clip='frame-'+Path(p['src']).stem
 image=f'<defs><clipPath id="{clip}"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}"/></clipPath></defs><g clip-path="url(#{clip})">{image}</g>'
 return f'<figure><svg class="sample-photo" viewBox="{view}" role="img" aria-label="{e(p["caption"])}"><title>{e(p["caption"])}</title>{image}</svg><figcaption>{e(p["caption"])}</figcaption></figure>'

def foot(n):return f'<footer>CAMX 2026 REPORT · APPENDIX <span>{n:02}</span></footer>'
representatives=[
('난연·내화 소재',['kelvinite','nabaltec','pyrophobic'],'팽창·세라믹화 장벽으로 화염 차단. Kelvinite는 함침 개선, Nabaltec은 PP용 시험자료와 샘플 확보가 후속 과제.'),
('EMI·RF 기능성 소재',['stm','mast'],'STM은 유연한 차폐 시트를 100% 미국에서 생산. MAST는 주파수별 RF 흡수·차폐 소재를 맞춤 설계.'),
('섬유·직물·프리폼',['ngf','saertex','concordia'],'고열전도 피치계 섬유, 북미 생산 NCF, 열가소성 혼합 원사로 소재·공급 방식 다양화.'),
('수지·컴파운드·중간재',['avient','trimer','exxon'],'PET 내열 향상과 SMC용 수지 확대. 저점도 수지는 함침과 경화 제어를 결합해 성형 공정 개선.'),
('성형 공정·설비',['cannon','andritz','magestic'],'주입·압축성형 설비와 적층 시뮬레이션을 통해 성형 재현성과 작업 효율을 개선.'),
('접착·조립',['ll','parson'],'박막 접착재로 층간 손상을 억제하고, 고온용 접착제로 GF·금속 이종재 접합에 대응.'),
('구조부품·항공우주 응용',['rebuild','toray'],'연속 GF/PP 일체형 부품과 CFRP 구조 응용. 소재 공급부터 성형·후공정까지 연계하는 방향.')]
D={c['key']:c for c in C}
rows=''.join('<tr><td>'+e(s)+'</td><td>'+'<br>'.join(f'<a href="#company-{k}">{e(D[k]["name"])}</a>' for k in keys)+'</td><td>'+e(desc)+'</td></tr>' for s,keys,desc in representatives)
summary=page('<header><span class="section-no">2</span><h1>주요 전시 업체 요약</h1></header><p class="subhead">분야별 대표 업체 및 주요 확인 내용 · 상세 내용은 유첨 참조</p><table class="summary-table"><thead><tr><th>분야</th><th>대표 업체</th><th>주요 내용</th></tr></thead><tbody>'+rows+'</tbody></table><p class="subhead">James Cropper의 기능성 베일·UNIMAT 수상 기술은 난연·내화 소재 유첨에 함께 정리.</p>'+foot(3))
out=[F['summary1'],F['summary2'],summary]
for n,c in enumerate(C,4):
 photos=c['photos']; take=c.get('takeaways',[]); follow=c.get('followup','');compare=c.get('comparison','')
 dense=bool(compare or len(c['bullets'])>=5)
 cls='detail-page'+(' dense' if dense else '')+(' has-takeaway' if take else '')+(' has-followup' if follow else '')+(' no-photos' if not photos else '')+(' has-card' if c.get('card') else '')
 contact=('<div class="card-meta"><span>부스 담당자</span>'+card_html(c['card'],c['key'])+'</div>') if c.get('card') else (f'<div><span>부스 담당자</span><b>{e(c["person"])}</b></div>' if c.get('person') else '')
 meta=f'<div class="meta {"no-contact" if not contact else ""}"><div><span>본사 · 사업장 위치</span><b>'+ '<br>'.join(e(x) for x in c['location'])+'</b></div>'+contact+f'<div><span>핵심 전시품</span><b>{e(c["product"])}</b><span class="contact-label">회사 홈페이지</span><b><a href="{e(c["website"])}">{e(c["website"].split("//")[-1].split("/")[0])}</a></b></div></div>'
 comparison=f'<div class="comparison"><b>2025년 대비 확인된 변화</b>{e(compare)}</div>' if compare else ''
 text='<article><h2>업체 개요</h2><p class="company-profile">'+e(c['profile'])+'</p><h2>전시품 및 기술 내용</h2><ul>'+''.join('<li>'+e(x)+'</li>' for x in c['bullets'])+'</ul>'+comparison+'</article>'
 if photos:
  visual=f'<div class="photos count-{len(photos)}">'+''.join(sample_html(p) for p in photos)+'</div>'
 else:
  focus={'nabaltec':('검토 순서','PP용 시험 조건·배합 확인 → 기술 미팅 및 NDA → 샘플 평가. 인계 난연제와의 임의 병용보다 권장 처방 기준으로 출발.'),'saertex':('공급·적용 확인','북미 생산 NCF와 설계 지원은 확인. 현대·기아 적용 이력은 지역별 공급망을 구분해 추가 확인.'),'magestic':('적용 범위','형상 추종·주름·장비 경로를 검토하는 도구. 구조 강도 해석을 대체하는 기능으로 보지 않고 실제 적층 형상으로 검증.')}[c['key']]
  visual=f'<aside class="discussion-panel"><h3>{e(focus[0])}</h3><p>{e(focus[1])}</p><small>주요 상담 내용</small></aside>'
 takeaway='<div class="takeaway"><b>Take Away</b><ul>'+''.join('<li>'+e(t)+'</li>' for t in take)+'</ul></div>' if take else ''
 followup=f'<div class="followup"><b>후속 컨택 포인트</b><p>{e(follow)}</p></div>' if follow else ''
 out.append(page(f'<header><span class="section-no">{n:02}</span><h1>{e(c["name"])}</h1><span class="category theme-{sections.index(c["section"])+1}"><small>SECTION</small>{e(c["section"])}</span></header>'+meta+'<div class="detail-grid">'+text+visual+'</div>'+takeaway+followup+foot(n),cls,'company-'+c['key']))
(R/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 참관 보고서</title><link rel="stylesheet" href="report.css"></head><body>'+''.join(out)+CARD_SCRIPT+'</body></html>')
print(f'Built {len(out)} pages / {len(C)} companies')

cards=json.loads((R/'business-cards.json').read_text())
names={c['key']:c['name'] for c in C};names.update(cfr='Carbon Fiber Recycling',avanco='AVANCO')
gallery=''.join('<article id="'+e(k)+'"><h2>'+e(names[k])+'</h2>'+card_html(card,k)+'</article>' for k,card in cards.items())
(R/'cards.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 명함 모음</title><link rel="stylesheet" href="report.css"></head><body><main class="card-gallery">'+gallery+'</main>'+CARD_SCRIPT+'</body></html>')
