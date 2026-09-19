"""Collect public metadata from exhibitor-linked company websites."""
import concurrent.futures
import html
import json
import re
import ssl
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = 'Mozilla/5.0 (compatible; CAMXResearch/1.0)'


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.h1 = ''
        self.meta = {}
        self.links = []
        self.in_title = False
        self.in_h1 = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'title': self.in_title = True
        if tag == 'h1' and not self.h1: self.in_h1 = True
        if tag == 'meta':
            key = (d.get('name') or d.get('property') or '').lower()
            if key in {'description', 'og:description', 'twitter:description'}:
                self.meta[key] = d.get('content', '')
        if tag == 'a' and d.get('href'):
            self.links.append(d['href'])

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'h1': self.in_h1 = False

    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_h1: self.h1 += data


def fetch(row):
    url = row['website']
    if not url: return {'id': row['id'], 'status': 'no_link'}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml'})
        with urllib.request.urlopen(req, timeout=12, context=ssl.create_default_context()) as response:
            final = response.url
            content_type = response.headers.get('Content-Type', '')
            if 'html' not in content_type.lower():
                return {'id': row['id'], 'status': 'non_html', 'url': final}
            data = response.read(700000)
            charset = response.headers.get_content_charset() or 'utf-8'
        parser = Metadata()
        parser.feed(data.decode(charset, 'replace'))
        desc = parser.meta.get('description') or parser.meta.get('og:description') or parser.meta.get('twitter:description') or ''
        desc = re.sub(r'\s+', ' ', html.unescape(desc)).strip()[:700]
        title = re.sub(r'\s+', ' ', html.unescape(parser.title)).strip()[:220]
        h1 = re.sub(r'\s+', ' ', html.unescape(parser.h1)).strip()[:220]
        return {'id': row['id'], 'status': 'ok', 'url': final, 'title': title, 'description': desc, 'h1': h1}
    except Exception as exc:
        return {'id': row['id'], 'status': 'error', 'error': str(exc)[:120]}


if __name__ == '__main__':
    rows = json.loads((ROOT / 'data/official-details.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        result = list(pool.map(fetch, rows))
    (ROOT / 'data/company-sites.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    from collections import Counter
    print(Counter(r['status'] for r in result))
    print('Useful metadata:', sum(bool(r.get('description')) for r in result))
