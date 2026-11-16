import json, sys, urllib.request, urllib.parse, os, re
UA = 'FableAtelierStudy/0.1 (personal art study; no contact)'
import time
def fetch(url, tries=6):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()
        except Exception as e:
            time.sleep(8 * (i + 1))
    raise SystemExit('gave up: ' + url[:90])
def api(**p):
    p['format'] = 'json'
    return json.loads(fetch('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p)))
def search(q, n=12):
    d = api(action='query', list='search', srsearch=q + ' filetype:bitmap', srnamespace=6, srlimit=n)
    return [m['title'] for m in d['query']['search']]
def get(title, out, width=1000):
    d = api(action='query', titles=title, prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=width)
    pg = next(iter(d['query']['pages'].values()))
    ii = pg['imageinfo'][0]
    url = ii.get('thumburl') or ii['url']
    time.sleep(4)
    open(out, 'wb').write(fetch(url))
    em = ii.get('extmetadata', {})
    lic = em.get('LicenseShortName', {}).get('value', '?')
    art = re.sub('<[^>]+>', '', em.get('Artist', {}).get('value', '?'))[:60]
    return f"- `{out}` | {title} | {art.strip()} | {lic} | {ii['descriptionurl']}"
if sys.argv[1] == 'search':
    for t in search(' '.join(sys.argv[2:])): print(t)
else:
    out, title = sys.argv[2], ' '.join(sys.argv[3:])
    line = get(title, out)
    open('SOURCES.md', 'a').write(line + '\n'); print(line)
