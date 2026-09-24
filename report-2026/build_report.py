#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the static CAMX report from reviewed content and original photo assets."""
from pathlib import Path
import html,json,hashlib
from card_layout import card_html,CARD_SCRIPT
R=Path(__file__).resolve().parent
e=html.escape
C=json.loads((R/'report-data.json').read_text())
F=json.loads((R/'frontmatter.json').read_text())
EXTRA=json.loads((R/'overview-extra.json').read_text())
css_version=hashlib.sha256((R/'report.css').read_bytes()).hexdigest()[:10]
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
 return f'<figure><svg class="sample-photo" width="{vw}" height="{vh}" viewBox="{view}" role="img" aria-label="{e(p["caption"])}"><title>{e(p["caption"])}</title>{image}</svg><figcaption>{e(p["caption"])}</figcaption></figure>'

def foot(n):return f'<footer>CAMX 2026 REPORT <span>{n:02}</span></footer>'
rows=[]
for theme,section in enumerate(sections,1):
 members=[(i,c) for i,c in enumerate(C,1) if c['section']==section]
 links=''.join(f'<a href="#company-{c["key"]}"><span>{i:02}</span>{e(c["name"])}</a>' for i,c in members)
 additional=[c for c in EXTRA if c['section']==section]
 links+=''.join(f'<div class="overview-unlinked"><span>—</span>{e(c["name"])}</div>' for c in additional)
 rows.append(f'<tr><th scope="row"><b class="theme-{theme}">{e(section)}</b><small>{len(members)+len(additional)}개 업체</small></th><td><div class="overview-companies">{links}</div></td></tr>')
summary=page('<div class="legacy-head"><span></span><b>2</b><h1>주요 전시 업체 요약</h1></div><p class="overview-intro">총 28개 방문 업체 · 6개 분야</p><table class="overview-table"><thead><tr><th>분야</th><th>참관 업체</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'+foot(3),'company-overview')
out=[F['summary1'],F['summary2'],summary]
for company_no,c in enumerate(C,1):
 n=company_no+3
 photos=c['photos']; take=c.get('takeaways',[]); follow=c.get('followup','');compare=c.get('comparison','')
 dense=bool(compare or len(c['bullets'])>=5)
 cls='detail-page'+(' dense' if dense else '')+(' has-takeaway' if take else '')+(' has-followup' if follow else '')+(' no-photos' if not photos else '')+(' has-card' if c.get('card') else '')+(' text-only' if c['key']=='nabaltec' else '')
 contact=('<div class="card-meta"><span>부스 담당자</span>'+card_html(c['card'],c['key'])+'</div>') if c.get('card') else (f'<div><span>부스 담당자</span><b>{e(c["person"])}</b></div>' if c.get('person') else '')
 meta=f'<div class="meta {"no-contact" if not contact else ""}"><div><span>본사 · 사업장 위치</span><b>'+ '<br>'.join(e(x) for x in c['location'])+'</b></div>'+contact+f'<div><span>핵심 전시품</span><b>{e(c["product"])}</b><span class="contact-label">회사 홈페이지</span><b><a href="{e(c["website"])}">{e(c["website"].split("//")[-1].split("/")[0])}</a></b></div></div>'
 comparison=f'<div class="comparison"><b>2025년 대비 확인된 변화</b>{e(compare)}</div>' if compare else ''
 text='<article><h2>업체 개요</h2><p class="company-profile">'+e(c['profile'])+'</p><h2>전시품 및 기술 내용</h2><ul>'+''.join('<li>'+e(x)+'</li>' for x in c['bullets'])+'</ul>'+comparison+'</article>'
 if photos:
  visual=f'<div class="photos count-{len(photos)}">'+''.join(sample_html(p) for p in photos)+'</div>'
 elif c['key']=='nabaltec':
  visual=''
 else:
  focus={'saertex':('공급·적용 확인','북미 생산 NCF와 적층 설계 지원 역량을 확인. 현대·기아 적용 이력에 대한 답변은 북미 담당자의 확인 범위에 한정.'),'magestic':('적용 범위','형상 추종·주름 및 장비 경로 검토를 지원. 기하학적 드레이핑과 장비 동작 검토 기능으로, 구조 강도 해석과는 구분.')}[c['key']]
  visual=f'<aside class="discussion-panel"><h3>{e(focus[0])}</h3><p>{e(focus[1])}</p><small>주요 상담 내용</small></aside>'
 takeaway='<div class="takeaway"><b>핵심 시사점</b><ul>'+''.join('<li>'+e(t)+'</li>' for t in take)+'</ul></div>' if take else ''
 followup=f'<div class="followup"><b>후속 컨택 포인트</b><p>{e(follow)}</p></div>' if follow else ''
 out.append(page(f'<header><span class="section-no">{company_no:02}</span><h1>{e(c["name"])}</h1><span class="category theme-{sections.index(c["section"])+1}"><small>SECTION</small>{e(c["section"])}</span></header>'+meta+'<div class="detail-grid">'+text+visual+'</div>'+takeaway+followup+foot(n),cls,'company-'+c['key']))
(R/'index.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 참관 보고서</title><link rel="stylesheet" href="report.css"></head><body>'+''.join(out)+CARD_SCRIPT+'</body></html>')
print(f'Built {len(out)} pages / {len(C)} companies')

cards=json.loads((R/'business-cards.json').read_text())
names={c['key']:c['name'] for c in C};names.update(cfr='Carbon Fiber Recycling',avanco='AVANCO')
gallery=''.join('<article id="'+e(k)+'"><h2>'+e(names[k])+'</h2>'+card_html(card,k)+'</article>' for k,card in cards.items())
(R/'cards.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CAMX 2026 명함 모음</title><link rel="stylesheet" href="report.css"></head><body><main class="card-gallery">'+gallery+'</main>'+CARD_SCRIPT+'</body></html>')

# Cache-bust the stylesheet so published corrections appear immediately.
for filename in ['index.html','cards.html']:
 p=R/filename
 p.write_text(p.read_text().replace('href="report.css"',f'href="report.css?v={css_version}"'))
