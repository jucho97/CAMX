"""Render original card photographs with CSS perspective and clipping; no rewritten text."""
from html import escape as e

def solve(a,b):
 a=[list(row)+[v] for row,v in zip(a,b)]
 n=len(b)
 for i in range(n):
  k=max(range(i,n),key=lambda k:abs(a[k][i]));a[i],a[k]=a[k],a[i]
  d=a[i][i];a[i]=[v/d for v in a[i]]
  for j in range(n):
   if j!=i:
    d=a[j][i];a[j]=[u-d*v for u,v in zip(a[j],a[i])]
 return [row[-1] for row in a]

def card_html(c,key='',link=True):
 ratio=c.get('ratio',1.75);height=1000/ratio;A=[];B=[]
 src=[(x*1000,y*1000/c['imageRatio']) for x,y in c['quad']]
 for (x,y),(u,v) in zip(src,[(0,0),(1000,0),(1000,height),(0,height)]):
  A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
 a,b,tx,d,ee,ty,g,h=solve(A,B)
 matrix=[a,d,0,g,b,ee,0,h,0,0,1,0,tx,ty,0,1]
 style=f'--card-ratio:{ratio};--card-width:{32 if ratio<1 else 64}mm;--card-scale:{(32 if ratio<1 else 64)*96/25.4/1000}'
 content=f'<div class="business-card" style="{style}"><div class="card-scene" style="height:{height}px"><img src="{e(c["src"])}" alt="{e(c["name"])} 명함" style="transform:matrix3d('+','.join(f'{x:.12g}' for x in matrix)+')"></div></div>'
 return f'<button class="card-button" type="button" aria-label="{e(c["name"])} 명함 크게 보기" onclick="openCard(this)">{content}</button>' if link else content

CARD_SCRIPT='''<dialog id="card-dialog"><button class="close-card" onclick="this.closest('dialog').close()">닫기 ×</button><div id="card-view"></div></dialog><script>function openCard(button){const target=document.getElementById('card-view');target.replaceChildren(button.querySelector('.business-card').cloneNode(true));document.getElementById('card-dialog').showModal()}document.getElementById('card-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)e.currentTarget.close()});</script>'''
