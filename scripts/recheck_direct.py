"""Extract company page body text when metadata was empty or the first request failed."""
import concurrent.futures
import html
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.description = ''
        self.paragraphs = []
        self.capture = None
        self.buffer = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and (a.get('name', '').lower() == 'description' or a.get('property', '').lower() == 'og:description'):
            if not self.description: self.description = a.get('content', '')
        if tag in ('title', 'h1', 'p'):
            self.capture = tag
            self.buffer = ''

    def handle_endtag(self, tag):
        if self.capture == tag:
            value = re.sub(r'\s+', ' ', html.unescape(self.buffer)).strip()
            if tag == 'title': self.title = value
            if tag in ('h1', 'p') and 50 <= len(value) <= 1500: self.paragraphs.append(value)
            self.capture = None

    def handle_data(self, data):
        if self.capture: self.buffer += data


def host(url):
    return (urllib.parse.urlsplit(url).hostname or '').lower().removeprefix('www.')


def page_description(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'}), timeout=14) as response:
        if 'html' not in response.headers.get('Content-Type', '').lower(): return None
        body = response.read(550000).decode(response.headers.get_content_charset() or 'utf-8', 'replace')
        final = response.url
    p = PageParser(); p.feed(body)
    desc = re.sub(r'\s+', ' ', html.unescape(p.description)).strip()
    if len(desc) < 60:
        paragraphs = [x for x in p.paragraphs if not re.search('cookie|privacy policy|subscribe|javascript', x, re.I)]
        paragraphs.sort(key=lambda x: (bool(re.search('composite|aerospace|automotive|manufactur|resin|fiber|mold|material|AI', x, re.I)), len(x)), reverse=True)
        desc = paragraphs[0] if paragraphs else ''
    return {'url': final, 'title': p.title[:200], 'description': desc[:900]}


def variants(url):
    u = urllib.parse.urlsplit(url)
    hostname = u.hostname or ''
    path = u.path or '/'
    results = [url]
    if hostname.startswith('www.'):
        results.append(urllib.parse.urlunsplit(('https', hostname[4:], path, u.query, '')))
    else:
        results.append(urllib.parse.urlunsplit(('https', 'www.' + hostname, path, u.query, '')))
    if path == '/':
        results.extend(url.rstrip('/') + suffix for suffix in ('/about', '/about-us'))
    return list(dict.fromkeys(results))


def inspect(row):
    for url in variants(row['website'])[:4]:
        try:
            result = page_description(url)
            if result and len(result['description']) >= 60 and host(result['url']):
                return {'id': row['id'], 'status': 'found', 'source': result}
        except Exception:
            continue
    return {'id': row['id'], 'status': 'not_found'}


if __name__ == '__main__':
    rows = [x for x in json.loads((ROOT / 'data/research.json').read_text()) if x['id'] and x['website'] and x['verification'] == '외부 자료 확인 어려움']
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(inspect, rows))
    (ROOT / 'data/recheck-direct.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    print('rechecked', len(rows), 'found', sum(x['status'] == 'found' for x in results))
