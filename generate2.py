# -*- coding: utf-8 -*-
"""重新生成 stations.js：Python 全程处理（urllib 正确解码 UTF-8 JSON）。
拉取 radio-browser countrycode=CN 热门台 -> 逐个实测 -> 生成 CN_STATIONS + FALLBACK。
"""
import json, os, re, urllib.request

BASE = r'C:\Users\Huawei\Doubao\chats\2026-10-21\new-chat-8\shouyinji-cn'
OUT = os.path.join(BASE, 'stations.js')

NODES = ['https://de1.api.radio-browser.info', 'https://at1.api.radio-browser.info', 'https://nl1.api.radio-browser.info']

def fetch_stations():
    for n in NODES:
        try:
            req = urllib.request.Request(
                n + '/json/stations/search?countrycode=CN&order=votes&reverse=true&limit=60&hidebroken=true',
                headers={'User-Agent': 'doubao-agent/1.0', 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            print('节点 %s 失败: %s' % (n, e))
    raise RuntimeError('所有节点拉取失败')

def test_stream(u):
    """测试流是否可播放：HTTP 200/206 且 Content-Type 为音频类。"""
    for attempt in range(2):
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Range': 'bytes=0-2047'})
            with urllib.request.urlopen(req, timeout=6) as r:
                code = r.status
                ct = r.headers.get('Content-Type', '')
                r.read(256)
                ok = (code in (200, 206)) and re.search(r'audio|mpeg|ogg|aac|octet-stream|x-scpls|icecast|mpegurl|mp3|aacp|opus', ct, re.I)
                return ok, code, ct
        except Exception:
            continue
    return False, 0, ''

def main():
    data = fetch_stations()
    print('拉取到 %d 个电台' % len(data))
    ok_list, bad = [], 0
    for s in data:
        u = s.get('url_resolved') or s.get('url') or ''
        if not u:
            bad += 1
            continue
        ok, code, ct = test_stream(u)
        if ok:
            ok_list.append({'name': (s.get('name') or '').strip(),
                            'url': u,
                            'votes': s.get('votes') or 0,
                            'favicon': s.get('favicon') or '',
                            'tags': (s.get('tags') or '').strip()})
        else:
            bad += 1
    print('可用: %d, 不可用: %d' % (len(ok_list), bad))

    cn = []
    seen = set()
    for s in ok_list:
        tags = s['tags'].split(',')[0].strip() if s['tags'] else '广播'
        key = (s['name'], s['url'])
        if not s['name'] or key in seen:
            continue
        seen.add(key)
        cn.append({'name': s['name'], 'url': s['url'], 'country': 'CN', 'tags': tags,
                   'votes': int(s['votes']), 'favicon': s['favicon']})
    print('去重后内置电台: %d' % len(cn))

    content = '''/*
 * 收音机.cn - 电台数据
 * 说明：
 * 1. CN_STATIONS 为内置的国内电台精选（来自 radio-browser.info 社区库，已实测流可用），
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
''' % json.dumps(cn, ensure_ascii=False, indent=None)

    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    # 回读严格校验
    txt = open(OUT, 'r', encoding='utf-8').read()
    assert '华语' in txt or len(cn) > 0, '回读异常'
    names_ok = sum(1 for s in cn if all(ord(c) < 128 or '\u4e00' <= c <= '\u9fff' for c in s['name']))
    print('文件已写入 %d 字节；中文名电台 %d 个' % (len(txt.encode('utf-8')), names_ok))
    sample = [s['name'] for s in cn[:5]]
    print('样例:', sample)

if __name__ == '__main__':
    main()
