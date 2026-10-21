/*
 * 收音机.cn - 备用电台列表（FALLBACK）
 * 说明：
 * 1. 站点默认从 radio-browser.info 社区电台库在线拉取（真实、海量、自动更新），
 *    本站单页无需服务器，电台数据无需手工维护。
 * 2. 下方 FALLBACK_STATIONS 是"在线电台库暂时不可用"时的兜底频道，
 *    均为 SomaFM 官方公开的 MP3 直播流，稳定且允许网页播放。
 * 3. 如需添加自建电台（例如你自己的广播流），在数组中按同样格式追加即可：
 *    {name:'电台名', url:'https://你的流地址/stream', country:'CN', tags:'类型', votes:0, favicon:''}
 *    然后提交到 GitHub 仓库即可自动生效。
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
