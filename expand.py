# -*- coding: utf-8 -*-
"""扩充收音机.cn 内置国内电台。
- 读取现有 CN_STATIONS 作为基线（按 URL 去重，保留首次出现）
- 多条件拉取 radio-browser：CN 热门 / 华语语言 / 各类型标签
- 并发实测流可用性，追加新可用台
- 重新生成 stations.js，FALLBACK 原样保留
"""
import json, os, re, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE = r'C:\Users\Huawei\Doubao\chats\2026-10-21\new-chat-8\shouyinji-cn'
OUT = os.path.join(BASE, 'stations.js')

NODES = ['https://de1.api.radio-browser.info', 'https://at1.api.radio-browser.info', 'https://nl1.api.radio-browser.info']

def http_json(url, timeout=15):
    req = urllib.request.Request(url, headers={'User-Agent': 'doubao-agent/1.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))

def fetch_all():
    """多条件汇总，dict[url]=station"""
    agg = {}
    def add(data):
        for s in data:
            u = s.get('url_resolved') or s.get('url') or ''
            if not u:
                continue
            # 保留 votes 较高的一条
            if u not in agg or (s.get('votes') or 0) > (agg[u].get('votes') or 0):
                agg[u] = s
    queries = [
        '/json/stations/search?countrycode=CN&order=votes&reverse=true&limit=150&hidebroken=true',
        '/json/stations/search?language=chinese&order=votes&reverse=true&limit=100&hidebroken=true',
    ]
    for tag in ['news', 'music', 'oldies', 'talk', 'economics', 'traffic', 'storytelling']:
        queries.append('/json/stations/search?countrycode=CN&tag=' + urllib.parse.quote(tag) + '&order=votes&reverse=true&limit=60&hidebroken=true')
    for q in queries:
        for n in NODES:
            try:
                data = http_json(n + q)
                if data:
                    add(data)
                    break
            except Exception as e:
                print('拉取失败 %s: %s' % (n + q, e))
    return agg

def test_stream(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Range': 'bytes=0-2047'})
        with urllib.request.urlopen(req, timeout=6) as r:
            code = r.status
            ct = r.headers.get('Content-Type', '')
            r.read(256)
            ok = (code in (200, 206)) and re.search(r'audio|mpeg|ogg|aac|octet-stream|x-scpls|icecast|mpegurl|mp3|aacp|opus', ct, re.I)
            return bool(ok)
    except Exception:
        return False

def load_existing():
    txt = open(OUT, encoding='utf-8').read()
    start = txt.index('[', txt.index('var CN_STATIONS = ['))
    end = txt.index('];', start) + 1
    return json.loads(txt[start:end])

def main():
    existing = load_existing()
    # 现有按 URL 去重
    seen = set()
    base_list = []
    for s in existing:
        if s['url'] in seen:
            continue
        seen.add(s['url'])
        base_list.append(s)
    print('现有去重后: %d 台（原 %d）' % (len(base_list), len(existing)))

    agg = fetch_all()
    print('API 汇总去重: %d 台' % len(agg))
    new_candidates = [s for u, s in agg.items() if u not in seen]
    print('待测试新台: %d' % len(new_candidates))

    usable = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = list(ex.map(lambda s: (s, test_stream(s.get('url_resolved') or s.get('url'))), new_candidates))
    for s, ok in results:
        if ok:
            u = s.get('url_resolved') or s.get('url')
            tags = (s.get('tags') or '').split(',')[0].strip() or '广播'
            usable.append({'name': (s.get('name') or '').strip(), 'url': u, 'country': 'CN',
                            'tags': tags, 'votes': int(s.get('votes') or 0), 'favicon': s.get('favicon') or ''})
    print('实测可用新台: %d' % len(usable))

    merged = base_list + usable
    # 最终再按 URL 去重
    final, fseen = [], set()
    for s in merged:
        if s['url'] in fseen:
            continue
        fseen.add(s['url'])
        final.append(s)
    print('合并后总数: %d 台' % len(final))

    content = '''/*
 * 收音机.cn - 电台数据
 * 说明：
 * 1. CN_STATIONS 为内置的国内及华语电台精选（来自 radio-browser.info 社区库，已实测流可用），
 *    打开站点即可收听，不依赖网络请求。
 * 2. 站点首页默认还会从 radio-browser.info 在线拉取更多电台，两者互补。
 * 3. 如需添加自建电台，按格式在 CN_STATIONS 中追加即可，然后提交到 GitHub 自动生效：
 *    {name:'电台名', url:'https://你的广播流地址', country:'CN', tags:'类型', votes:0, favicon:''}
 */
var CN_STATIONS = %s;

/*
 * 备用电台列表（FALLBACK）：在线电台库不可用时的兜底，SomaFM 官方公开 MP3 流。
 */
var FALLBACK_STATIONS = [
  {name:'Groove Salad（电音氛围）', url:'https://ice1.somafm.com/groovesalad-128-mp3', country:'US', tags:'电子 · 氛围', votes:0, favicon:''},
  {name:'Drone Zone（空灵氛围）', url:'https://ice1.somafm.com/dronezone-128-mp3', country:'US', tags:'氛围 · 环境', votes:0, favicon:''},
  {name:'7" Soul（灵魂乐）', url:'https://ice1.somafm.com/7soul-128-mp3', country:'US', tags:'灵魂乐 · R&B', votes:0, favicon:''},
  {name:'Lush（舒缓人声）', url:'https://ice1.somafm.com/lush-128-mp3', country:'US', tags:'舒缓 · 人声', votes:0, favicon:''},
  {name:'Secret Agent（间谍爵士）', url:'https://ice1.somafm.com/secretagent-128-mp3', country:'US', tags:'爵士 · 电影配乐', votes:0, favicon:''},
  {name:'DEF CON（节拍电子）', url:'https://ice1.somafm.com/defcon-128-mp3', country:'US', tags:'电子 · 节拍', votes:0, favicon:''},
  {name:'Indie Pop Rocks（独立流行）', url:'https://ice1.somafm.com/indiepop-128-mp3', country:'US', tags:'独立流行', votes:0, favicon:''},
  {name:'Boot Liquor（美式根源）', url:'https://ice1.somafm.com/bootliquor-128-mp3', country:'US', tags:'乡村 · 根源', votes:0, favicon:''}
];
''' % json.dumps(final, ensure_ascii=False, indent=None)

    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    # 回读校验
    txt = open(OUT, encoding='utf-8').read()
    assert 'var CN_STATIONS = [' in txt
    print('文件已写入 %d 字节' % len(txt.encode('utf-8')))
    print('新增样例:', [s['name'] for s in usable[:8]])

if __name__ == '__main__':
    main()
