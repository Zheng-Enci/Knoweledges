# -*- coding: utf-8 -*-
"""
抖音图文卡片一键生成脚本 (HTML + 浏览器截图版)
------------------------------------------------
读取 `-抖音.md` 的 `P01…PN` 各页，逐页转成 1080x1440 (3:4) 深色卡片图，输出 PNG。
用 HTML/CSS 排版 + Playwright 驱动系统 Chrome 截图，替代 PIL 手绘方案。
相对 PIL 的优势：emoji 由浏览器原生对齐（font-family 含 Segoe UI Emoji），
渐变色/圆角/阴影/图表等样式自由度大，断行/行高/居中全由 CSS 接管。

排版铁律（与 card_gen.py 保持一致）：
  - 尺寸 1080x1440,一页一卡,P01 兼封面
  - 色板:深底 #0B0D12 + 浅字 #F0F0F0,强调绿 #22C55E,亮黄 #FFD400(数字)
  - 内容垂直居中;右侧安全区:右缘 ≤85%;文案不出屏 ≤92%/≥8%
  - 正文行高 1.6,标题行高 1.25;关键词加粗高亮,数字段亮黄

用法(项目根目录):
  C:\\...\\miniconda3\\python.exe  card_gen_html.py  "AI08-xxx-抖音.md"  [输出目录]

依赖: pip install playwright; 复用系统 Chrome,无需 playwright install 下载内核。
输出: <输出目录>/card1.png ... cardN.png,cardN 对应 PN,card1 即 P01。
脚本仅做排版,文字从对应页原样读取,不改写、不精简、不补写。
"""
import sys, os, re
from playwright.sync_api import sync_playwright

# ---------- 常量(铁律,与 card_gen.py 对齐) ----------
W, H = 1080, 1440                    # 3:4 竖版,唯一尺寸
BG = '#0B0D12'                       # 深底
FG = '#F0F0F0'                       # 浅字
GREEN = '#22C55E'                    # 强调绿
YELLOW = '#FFD400'                   # 亮黄(数字/色块)
FONT_MAIN = '"Microsoft YaHei","PingFang SC","Noto Sans SC",sans-serif'
FONT_EMOJI = '"Segoe UI Emoji","Apple Color Emoji","Noto Color Emoji",sans-serif'

# 高亮语义色映射(生成侧三类:数字/术语/结论);数字类=亮黄,结论/判断类=强调绿
# 术语类未单独着色时回落浅色,与现实规范一致
VERDICT_WORDS = re.compile(
    r'不会|不容|值得|别|不|必须|只能|优先|更|最|只有|关键|胜|输|省|烧|坑|退'
    r'|唯一|绝对|根本|正好|始终|一味|普遍'
)

# ---------- HTML 模板 ----------
# 用 @@KEY@@ 占位,str.replace 注入,避免与 CSS 花括号冲突(单花括号即可)
TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="utf-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: @W@px; height: @H@px; }
body {
  width: @W@px; height: @H@px;
  background: @BG@;
  color: @FG@;
  font-family: @FONT_MAIN@;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}
.emoji { font-family: @FONT_EMOJI@; }
.card {
  width: 100%; height: 100%;
  padding: @PAD_TOP@px @PAD_RIGHT@px @PAD_BOTTOM@px @PAD_LEFT@px;
  display: flex; flex-direction: column; justify-content: center;
}
.title {
  color: @GREEN@;
  font-weight: 700;
  font-size: @TITLE_SIZE@px;
  line-height: 1.25;
  letter-spacing: 1px;
  margin-bottom: @TITLE_MB@px;
  padding-left: 20px;
  border-left: 8px solid @GREEN@;
  word-break: break-word;
}
.cover-title {
  color: @GREEN@;
  font-weight: 800;
  font-size: @COVER_TITLE_SIZE@px;
  line-height: 1.3;
  letter-spacing: 1px;
  margin-bottom: @COVER_TITLE_MB@px;
  padding-left: 24px;
  border-left: 12px solid @GREEN@;
  word-break: break-word;
}
.body { display: flex; flex-direction: column; gap: @BODY_GAP@px; }
.item { display: flex; align-items: flex-start; line-height: 1.6; font-size: @BODY_SIZE@px; }
.idx {
  color: @GREEN@;
  font-weight: 700;
  flex: 0 0 auto;
  width: @IDX_W@px;
  text-align: center;
  line-height: 1.6;
}
.txt { flex: 1 1 auto; word-break: break-word; }
.num { color: @YELLOW@; font-weight: 700; }
.verdict { color: @GREEN@; font-weight: 700; }
</style>
</head>
<body>
<div class="card">
  @TITLE_BLOCK@
  <div class="body">@BULLETS@</div>
</div>
</body>
</html>'''

# ---------- 工具函数 ----------
def _add_highlight(html_text):
    """把文本中 `**x**` 高亮段和数字段转换成带语义色的 HTML span"""
    # 只允许两种实际着色:数字类=亮黄(.num),结论/判断类=强调绿(.verdict)
    # 其余高亮段(如纯术语名)保持默认浅色,不染色,避免颜色泛滥失焦
    def repl_bold(m):
        inner = m.group(1)
        if re.match(r'^[\d%.,\-–—\s×x倍个量级%]+$', inner):   # 纯数字/百分比/倍数 → 亮黄
            return f'<span class="num">{inner}</span>'
        if _is_verdict(inner):                                # 结论/判断词 → 强调绿
            return f'<span class="verdict">{inner}</span>'
        # 术语/普通名词高亮:保留加粗但不动色(默认浅色),避免第三种颜色
        return f'<b>{inner}</b>'
    # 未加 ** 包裹的裸露数字段(区间/百分比/绝对值)也染亮黄
    def repl_num(m):
        return f'<span class="num">{m.group(0)}</span>'
    s = re.sub(r'\*\*(.+?)\*\*', repl_bold, html_text)
    # 只匹配:数字前是行首或非文字字符(避免"到/点水"里的零宽数字误伤);跳过已是 span 内数字
    s = re.sub(r'(?<![\w\u4e00-\u9fff%<])([0-9]+(?:\.[0-9]+)?\s*%?)(?:\s*[–—-]\s*[0-9]+(?:\.[0-9]+)?\s*%?)?',
               repl_num, s)
    return s


def _is_verdict(text):
    """判断高亮词是否属于结论/判断类(用强调绿)，否则数字类/术语类"""
    return bool(VERDICT_WORDS.search(text))


def _emoji_wrap(html_text):
    """把裸 emoji 字符包一层 .emoji span，让浏览器用彩色 emoji 字体渲染并对齐"""
    out = []
    i, n = 0, len(html_text)
    emoji_re = re.compile(r'[\U0001F000-\U0001FAFF]|[\u2600-\u27BF]|[\uFE0F\u200D]|[\U0001F1E6-\U0001F1FF]')
    while i < n:
        ch = html_text[i]
        # 先跳过已包在 span 里的字符
        m = emoji_re.match(ch)
        if m:
            j = i + 1
            while j < n and (emoji_re.match(html_text[j]) or html_text[j] in '\uFE0F\u200D'):
                j += 1
            out.append(f'<span class="emoji">{html_text[i:j]}</span>')
            i = j
        else:
            out.append(ch)
            i += 1
    return ''.join(out)


def _escape(html_text):
    # 仅转义会影响 HTML 结构的字符，保留中文/英文/emoji
    return html_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# LaTeX 兜底:把 $...$ 内的常用命令转成可读 Unicode 数学,避免 HTML 渲染反斜杠源码
_GREEK = {r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\Delta': 'Δ', r'\delta': 'δ',
          r'\theta': 'θ', r'\lambda': 'λ', r'\mu': 'μ', r'\rho': 'ρ', r'\sigma': 'σ',
          r'\phi': 'φ', r'\omega': 'ω', r'\epsilon': 'ε', r'\pi': 'π'}
_OPS = {r'\cdot': '·', r'\times': '×', r'\pm': '±', r'\infty': '∞', r'\leq': '≤',
        r'\geq': '≥', r'\approx': '≈', r'\neq': '≠', r'\sqrt': '√', r'\le': '≤', r'\ge': '≥'}


def _latex_to_html(html_text):
    """把 $...$ 包裹的 LaTeX 公式转成可读的 Unicode 文本,供 HTML 直接显示"""
    def conv(m):
        s = m.group(1)
        s = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1) / (\2)', s)   # 分式→除式 (x-μ) / (σ)
        for cmd, ch in _OPS.items():    s = s.replace(cmd, ch)             # 运算符命令→符号
        for cmd, ch in _GREEK.items():  s = s.replace(cmd, ch)             # 希腊字母命令→Unicode
        s = s.replace('^', '').replace('{', '').replace('}', '')           # 去掉幂记号与花括号
        s = s.replace('\\', '').replace('$', '').replace("'", '′')         # 清残留反斜杠/撇转成撇号
        return s.strip()
    # 仅处理成对 $...$;未闭合的 $ 保持原样,不破坏页面
    return re.sub(r'\$(.+?)\$', conv, html_text)


def parse_pages(md_path):
    """解析 -抖音.md,返回 [(page_no, title, bullets, is_cover)] 列表"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.S)  # 剥离 front-matter
    pages = []
    pattern = re.compile(r'^##\s*(P\d+)\s*[·.\-]?\s*(.*)$', re.M)
    matches = list(pattern.finditer(content))
    for i, m in enumerate(matches):
        page_no = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]
        bullets = []
        for line in section.splitlines():
            line = line.strip()
            if line.startswith('-'):
                b = line.lstrip('-').strip()
                b = re.sub(r'\*\*', '**', b)      # 保留高亮标记,交给 HTML 层解析
                b = b.replace('`', '')
                b = re.sub(r'^(大标题|副标题|核心数字)[:：]\s*', '', b)   # 剥离 P01 字段前缀标签,只留内容
                if b:
                    bullets.append(b)
        pages.append((page_no, title, bullets, '封面' in title))
    return pages


def build_html(page_no, title, bullets, is_cover):
    """把单页数据渲染成一段完整 HTML"""
    # 封面页(is_cover)单独版式:第一条 bullet 提升为封面大标题,其余为列表
    title_block = ''
    items = []
    if is_cover and bullets:
        # 首条 = 封面大标题;用大字号 .cover-title,去序号
        # 测宽铁律:按可用内容宽(约 77% 画布宽)估算标题字符宽,自动收缩字号,防止主题词被断行
        raw = bullets[0]
        cn = sum(1 for ch in raw if '\u4e00' <= ch <= '\u9fff')
        other = len(raw) - cn
        units = cn + other * 0.55 + 0.15 * len(raw)          # 中文宽 + 西文宽 + 字距估算
        cover_size = int((W * 0.77) / max(1, units))         # 自动收缩到不超右缘
        cover_size = max(44, min(78, cover_size))            # 限幅:最小 44,最大 78
        cover_title = _add_highlight(_emoji_wrap(_latex_to_html(_escape(raw))))
        title_block = f'<div class="cover-title" style="font-size:{cover_size}px;margin-bottom:96px">{cover_title}</div>'
        # 其余条目作为列表,保留序号,但封面大标题已去序号,故副标题/核心数字从 ① 重新计
        rest = bullets[1:]
        for idx, b in enumerate(rest, start=1):
            seq = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩'][idx - 1] if idx <= 10 else f'{idx}.'
            txt_html = _add_highlight(_emoji_wrap(_latex_to_html(_escape(b))))
            items.append(f'<div class="item" style="font-size:54px;line-height:1.75;margin-top:44px"><div class="idx">{seq}</div><div class="txt">{txt_html}</div></div>')
    else:
        # 正文页:给非封面且有标题的页补一个标题块
        if title and not is_cover and '封面' not in title:
            title_block = f'<div class="title">{_escape(title)}</div>'
        for idx, b in enumerate(bullets, start=1):
            seq = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩'][idx - 1] if idx <= 10 else f'{idx}.'
            txt_html = _add_highlight(_emoji_wrap(_latex_to_html(_escape(b))))
            items.append(f'<div class="item"><div class="idx">{seq}</div><div class="txt">{txt_html}</div></div>')
    html = TEMPLATE
    html = html.replace('@TITLE_BLOCK@', title_block)
    html = html.replace('@BULLETS@', '\n'.join(items))
    # 大小/配色注入(单位统一在模板里写,这里只给数字)
    html = html.replace('@W@', str(W)).replace('@H@', str(H))
    html = html.replace('@BG@', BG).replace('@FG@', FG).replace('@GREEN@', GREEN).replace('@YELLOW@', YELLOW)
    html = html.replace('@FONT_MAIN@', FONT_MAIN).replace('@FONT_EMOJI@', FONT_EMOJI)
    html = html.replace('@PAD_LEFT@', str(int(W * 0.08)))
    html = html.replace('@PAD_RIGHT@', str(int(W * 0.15)))     # 右侧安全区 = 100% - 85%
    html = html.replace('@PAD_BOTTOM@', str(int(H * 0.08)))
    html = html.replace('@PAD_TOP@', str(int(H * 0.06)))
    html = html.replace('@BODY_SIZE@', '44')
    html = html.replace('@TITLE_SIZE@', '58')
    html = html.replace('@COVER_TITLE_SIZE@', '78')   # 封面大标题更大
    html = html.replace('@TITLE_MB@', '40')
    html = html.replace('@COVER_TITLE_MB@', '56')     # 封面大标题下留白更大
    html = html.replace('@BODY_GAP@', '36')
    html = html.replace('@IDX_W@', '60')
    return html


def render_page(html, out_path, chromium_exec=None):
    """用 Playwright + 系统 Chrome 把 HTML 渲染成 PNG(deviceScaleFactor=2 高清)"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=chromium_exec,
            headless=True,
            args=['--force-color-profile=srgb', '--hide-scrollbars', '--font-render-hinting=none'],
        )
        page = browser.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        page.set_content(html, wait_until='load')
        # 等字体(含 emoji)加载
        page.evaluate('document.fonts.ready.then(()=>{})')
        page.wait_for_timeout(300)
        page.screenshot(path=out_path, full_page=False)
        browser.close()


def main():
    if len(sys.argv) < 2:
        print('用法: python card_gen_html.py "<xxx-抖音.md>" [输出目录]')
        sys.exit(1)
    md_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.environ.get('TEMP', os.getcwd()), 'publish')
    os.makedirs(out_dir, exist_ok=True)
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if not os.path.exists(chrome):
        raise FileNotFoundError(f'找不到系统 Chrome: {chrome},请自行指定 chromium_exec')
    pages = parse_pages(md_path)
    if not pages:
        print('未解析到任何 P01..PN 页面')
        sys.exit(1)
    total = len(pages)
    for i, (page_no, title, bullets, is_cover) in enumerate(pages, start=1):
        html = build_html(page_no, title, bullets, is_cover)
        out = os.path.join(out_dir, f'card{i}.png')
        tmp_html = os.path.join(out_dir, f'_tmp_{page_no}.html')
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html)
        render_page(html, out, chromium_exec=chrome)
        os.remove(tmp_html)  # 清理临时 html,只留 PNG
        print(f'card{i}.png <-> {page_no} ({len(bullets)} bullets) -> {out}')
    print(f'共生成 {total} 张卡片,card1 即 P01 全封面')


if __name__ == '__main__':
    main()
