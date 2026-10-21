# 收音机.cn — 网络收音机站点

中文域名 **收音机.cn**（punycode：`xn--wbvu8bd34f.cn`）的在线网络收音机站点，纯静态单页应用，无需后端服务器。

## 功能
- 在线收听中国及全球电台直播（电台数据来自社区维护的 [radio-browser.info](https://www.radio-browser.info) 真实数据库，实时、免费、无需注册）
- 分类浏览：中文电台 / 中国大陆 / 全球热门 / 音乐 / 新闻
- 关键词搜索（支持中文台名、英文台名、标签）
- 收藏电台（保存在浏览器 localStorage）
- 播放器固定底栏，支持音量调节
- 内置备用电台（SomaFM 公开 MP3 流），在线电台库不可用时仍可收听

## 技术栈
纯 HTML + CSS + JavaScript，零依赖（无框架、无构建），单文件应用 + 一个电台数据文件。

## 目录结构
```
shouyinji-cn/
├── index.html     # 播放器页面（含全部功能）
├── stations.js    # 备用电台列表（可自行添加电台）
├── sitemap.xml
├── robots.txt
└── README.md
```

## 如何添加自己的电台
编辑 `stations.js`，在 `FALLBACK_STATIONS` 数组中按格式追加后提交即可：
```js
{name:'电台名', url:'https://你的广播流地址', country:'CN', tags:'类型标签', votes:0, favicon:''}
```

## 部署（GitHub Pages + 自定义域名）
1. 推送本目录到 GitHub 仓库 `mfujun2025/shouyinji-cn`
2. 仓库 Settings → Pages → Source 选择 `Deploy from a branch`，分支 `main`，目录 `/ (root)`
3. 自定义域名填 `xn--wbvu8bd34f.cn`（收音机.cn 的 punycode 形式），等待 DNS 校验
4. 在域名 DNS（当前为西部数码）配置解析：
   - 主域 A 记录（4 条，指向 GitHub Pages）：
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - `www` 子域 CNAME 记录 → `mfujun2025.github.io`
5. HTTPS 证书由 GitHub 自动签发（Let's Encrypt，支持 IDN 域名），通常几分钟内生效

## 说明
- 电台音频流来自各广播电台的公开频道，本站不存储音频内容。
- 部分电台流在浏览器中可能受源站限制无法播放，属源站行为，切换其他电台即可。
- 若某电台长期失效，可在 radio-browser.info 提交标记或在本站列表外换台。
