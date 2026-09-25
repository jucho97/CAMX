# -*- coding: utf-8 -*-
"""Package the current explorer and data as a single offline HTML file."""
from pathlib import Path
import re,json,base64
root=Path(__file__).resolve().parent.parent
h=(root/'index.html').read_text()
h=re.sub(r'<script defer src="(?:i18n|app)\.js[^" ]*"></script>','',h)
h=re.sub(r'<link rel="stylesheet" href="styles.css[^" ]*">',lambda m:'<style>'+(root/'styles.css').read_text()+'</style>',h)
h=h.replace('href="favicon.svg"','href="data:image/svg+xml;base64,'+base64.b64encode((root/'favicon.svg').read_bytes()).decode()+'"')
a=(root/'app.js').read_text();start=a.index('const [response,translations,summaries]=');end=a.index("  $('#stat-all')",start)
a=a[:start]+"const embedded=JSON.parse(document.getElementById('embedded-data').textContent);state.records=embedded.records;state.translations=embedded.translations;state.aboutSummaries=embedded.summaries;\n"+a[end:]
d=json.dumps({key:json.loads((root/'data'/file).read_text()) for key,file in [('records','research.json'),('translations','translations.json'),('summaries','about_summaries.json')]},ensure_ascii=False).replace('<','\\u003c')
scripts='<script type="application/json" id="embedded-data">'+d+'</script><script>'+(root/'i18n.js').read_text().replace('</script','<\\/script')+'</script><script>'+a.replace('</script','<\\/script')+'</script>'
h=h.replace('</body>',scripts+'</body>');out=root/'output/html/CAMX-2026-Exhibitor-Explorer.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(h);print(out)
