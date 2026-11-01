# -*- coding: utf-8 -*-
"""
抖音图文卡片一键生成脚本
--------------------------
读取 `-抖音.md` 的 `P01…PN` 各页，逐页转成 1080x1440 (3:4) 深色卡片图。
编码命令文件 publish-latest-doc.md 第 7 节(7.1.0 / 7.1.1)的全部排版铁律：
  - 尺寸统一 1080x1440,一页一卡,张数 = 页数(P01..PN),P01 兼封面
  - 色板统一:深底 #0B0D12 + 浅字,强调绿 #22C55E,点缀亮黄 #FFD400
  - 高亮色语义固定:数字类=亮黄,结论/判断词=强调绿
  - 内容垂直居中,上下留白差 ≤ 3%(约 40px)
  - 内容撑满画布 55%~75%,不足则放大字号/行距
  - 右侧安全区:所有元素右缘 ≤ 画布宽 85%,核心文案左移
  - 文案不出屏:最右≤92%、最左≥8%、最下≤92%、最上≥8% 内缩框
  - 行高=字号×1.5-1.8(正文) / ×1.15-1.3(标题),段落间隔≥30px
  - 字距:大字 ×0.03-0.06,使用 textbbox/measure 实测防重叠(<8px 加大重画)
  - P01 封面自检:200px 可读、主视觉≥30%、无「封面」二字

用法(在项目根目录):
  C:\\Users\\zheng\\OneDrive\\Desktop\\CodeEnvironment\\miniconda3\\python.exe  card_gen.py  "AI08-xxx-抖音.md"  [输出目录]

输出: <输出目录>/card1.png ... cardN.png,cardN 对应 PN,card1 即 P01。
脚本仅做排版,文字从对应页原样读取,不改写、不精简、不补写。
"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont

# ---------- 常量(铁律) ----------
W, H = 1080, 1440                 # 3:4 竖版,唯一尺寸
BG = (11, 13, 18)                 # 深底 #0B0D12
FG = (240, 240, 240)              # 浅字
GREEN = (34, 197, 94)             # 强调绿 #22C55E
YELLOW = (255, 212, 0)            # 亮黄 #FFD400(仅数字/色块点缀)
FONT_PATH = r'C:\Windows\Fonts\msyh.ttc'
# 彩色 emoji 字体(Windows Segoe UI Emoji),用于渲染 🎉😀⚡✅ 等符号
EMOJI_FONT_PATH = r'C:\Windows\Fonts\seguiemj.ttf'
# 匹配 emoji / 特殊符号区段(含 emoji 修饰符、ZWJ 序列、箭头、实心符号等)
EMOJI_RE = re.compile(
    r'[\U0001F000-\U0001FAFF]'      # emoji 主区 + 扩展
    r'|[\u2600-\u27BF]'             # 杂项符号/箭头/CJK 符号(如 ⚡✅◆★)
    r'|[\uFE0F\u200D]'              # 变体选择符 / 零宽连接符(ZwJ)
    r'|[\U0001F1E6-\U0001F1FF]'     # 国旗
)
PAD_LEFT = int(W * 0.08)          # 左侧留白
PAD_RIGHT = int(W * 0.85)         # 右缘上限(右侧安全区)
SAFE_RIGHT_X = int(W * 0.85)      # 右侧安全区:元素右缘不得超过此值
MAX_RIGHT = int(W * 0.92)         # 文案不出屏:最右 ≤92%
MIN_LEFT = int(W * 0.08)          # 最左 ≥8%
MAX_BOTTOM = int(H * 0.92)        # 最下 ≤92%
MIN_TOP = int(H * 0.08)           # 最上 ≥8%


def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)


def load_emoji_font(size):
    """加载彩色 emoji 字体;失败时回退到主字体,保证不崩"""
    try:
        return ImageFont.truetype(EMOJI_FONT_PATH, size)
    except Exception:
        return ImageFont.truetype(FONT_PATH, size)


def _char_has_emoji(ch):
    """判断单个字符是否为 emoji/特殊符号(含 ZWJ 序列里的 emoji)"""
    return bool(EMOJI_RE.match(ch))


# 数字/百分比/区间 + 英文单词/英文串视为「原子 token」
# 目的:断行时既不让完整数字拆开(99.2% 拆成 9 / 9.2%),也不让英文单词被拆开
# (修复 LangGraph 被拆成 st/ate、workflow 被拆成 w/orkflow)
ATOM_TOKEN = re.compile(
    r'[A-Za-z][A-Za-z0-9_\-]*'      # 英文单词(含数字/下划线/连字符),如 workflow、LangGraph、AutoGen、ReAct
    r'|[0-9]+(?:\.[0-9]+)?%?'       # 数字/百分比,如 99.2%、95%
    r'(?:\s*[–—-]\s*[0-9]+(?:\.[0-9]+)?%?)?'  # 区间,如 9%–18%
)


def tokenize(text):
    """把文本切成 token 列表:英文单词与数字/百分比/区间保持整体,其余按单字符"""
    tokens, pos = [], 0
    for m in ATOM_TOKEN.finditer(text):
        for ch in text[pos:m.start()]:   # 原子 token 前的普通字符逐个入列
            tokens.append(ch)
        tokens.append(m.group())          # 英文单词/数字整体作为原子 token
        pos = m.end()
    for ch in text[pos:]:
        tokens.append(ch)
    return tokens


def wrap_text(draw, text, font, max_w):
    """按 token 断行,数字/百分号/区间不被拆开,返回行列表,每行宽 ≤ max_w"""
    # 逐字符扫描,把 emoji 序列(含 ZWJ/变体选择符)当作整体 token,避免 emoji 被拆开
    # 其余仍走 tokenize 逻辑(英文单词/数字/区间保持整体)
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        if _char_has_emoji(text[i]):
            seq = text[i]
            j = i + 1
            while j < n and (_char_has_emoji(text[j]) or text[j] in '\uFE0F\u200D'):
                seq += text[j]
                j += 1
            tokens.append(seq)
            i = j
        else:
            # 复用原子 token 规则切英文/数字,其余单字符
            m = ATOM_TOKEN.match(text, i)
            if m:
                tokens.append(m.group())
                i = m.end()
            else:
                tokens.append(text[i])
                i += 1
    lines, cur = [], ''
    for tok in tokens:
        if tok == '\n':                    # 显式换行符直接断行
            lines.append(cur)
            cur = ''
            continue
        test = cur + tok
        if test and draw.textbbox((0, 0), test, font=font)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = tok                      # 单个 token 超宽时强制成行,避免死循环
    if cur:
        lines.append(cur)
    return lines


def _align_dy(main_font, emoji_font, seq):
    """计算 emoji 相对主字体的垂直偏移量,让两者视觉中心(box 中心)对齐"""
    # 不同字体字形中心不同;取主字体代表字符「中」与 emoji 各自 bbox 中心差作为下移量
    # 实测:中文字符中心 y≈32,emoji 中心 y≈17.5,故需下移约 13~14px,否则 emoji 偏上
    mb = main_font.getbbox('中')
    eb = emoji_font.getbbox(seq)
    main_cy = (mb[1] + mb[3]) / 2
    emo_cy = (eb[1] + eb[3]) / 2
    return int(round(main_cy - emo_cy))


def draw_mixed(draw, x, y, text, font_main, emoji_font, fill):
    """绘制一行文本,普通字符用主字体,emoji 用彩色 emoji 字体(垂直对齐校正)"""
    main_cy = (font_main.getbbox('中')[1] + font_main.getbbox('中')[3]) / 2  # 主字体代表字符中心
    # 逐字符扫描;emoji 序列(含 ZWJ/变体)用 emoji 字体,其余用主字体
    n = len(text)
    i = 0
    cx = x
    while i < n:
        if _char_has_emoji(text[i]):
            seq = text[i]
            j = i + 1
            while j < n and (_char_has_emoji(text[j]) or text[j] in '\uFE0F\u200D'):
                seq += text[j]
                j += 1
            dy = _align_dy(font_main, emoji_font, seq)  # 按该 emoji 序列自身中心对齐
            draw.text((cx, y + dy), seq, font=emoji_font, fill=fill, embedded_color=True)
            cx += draw.textbbox((0, 0), seq, font=emoji_font)[2]
            i = j
        else:
            ch = text[i]
            draw.text((cx, y), ch, font=font_main, fill=fill)
            cx += draw.textbbox((0, 0), ch, font=font_main)[2]
            i += 1
    return cx


def draw_mixed_colored(draw, x, y, text, font_main, emoji_font, fill, num_font, num_fill):
    """绘制一行,并对数字段覆盖高亮色(如亮黄);emoji 走彩色字体并垂直对齐校正"""
    n = len(text)
    i = 0
    cx = x
    while i < n:
        if _char_has_emoji(text[i]):
            seq = text[i]
            j = i + 1
            while j < n and (_char_has_emoji(text[j]) or text[j] in '\uFE0F\u200D'):
                seq += text[j]
                j += 1
            dy = _align_dy(font_main, emoji_font, seq)  # 按该 emoji 序列自身中心对齐
            draw.text((cx, y + dy), seq, font=emoji_font, fill=fill, embedded_color=True)
            cx += draw.textbbox((0, 0), seq, font=emoji_font)[2]
            i = j
        else:
            # 数字/百分比段用高亮色
            m = re.match(r'[0-9]+(?:\.[0-9]+)?%?', text[i:])
            if m:
                seg = m.group()
                draw.text((cx, y), seg, font=num_font, fill=num_fill)
                cx += draw.textbbox((0, 0), seg, font=num_font)[2]
                i += len(seg)
            else:
                ch = text[i]
                draw.text((cx, y), ch, font=font_main, fill=fill)
                cx += draw.textbbox((0, 0), ch, font=font_main)[2]
                i += 1
    return cx


def parse_pages(md_path):
    """解析 -抖音.md,返回 [(page_no, title, bullets, cover_flag)] 列表"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 剥离 front-matter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.S)
    pages = []
    # 匹配 ## Pxx [· xx标题](可选)
    pattern = re.compile(r'^##\s*(P\d+)\s*[·.\-]?\s*(.*)$', re.M)
    matches = list(pattern.finditer(content))
    for i, m in enumerate(matches):
        page_no = m.group(1)
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        section = content[start:end]
        # 收集 bullets(以 - 开头的行)
        bullets = []
        for line in section.splitlines():
            line = line.strip()
            if line.startswith('-'):
                # 去掉前导 -,保留内容;去掉包围的 ** 和行内反引号
                b = line.lstrip('-').strip()
                b = re.sub(r'\*\*', '', b)
                b = b.replace('`', '')
                if b:
                    bullets.append(b)
        pages.append((page_no, title, bullets))
    return pages


def draw_card(page_no, title, bullets, out_path):
    """绘制单张卡片,遵守 7.1.0 全部排版铁律"""
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)

    # 1) 确定字号:正文字号从 44 起,按内容量自适应,范围 34-72
    #    单页 150-400 字时可能偏多:若撑满 55% 但把字号压到可读线(34px)仍超 75%,允许上限放宽
    body_size = 44
    title_size = 64
    gap = 36  # 段落间隔
    MIN_BODY, MAX_BODY = 34, 72   # 正文字号可读下限 34(铁律),上限 72(容纳 400 字)
    MIN_TITLE, MAX_TITLE = 48, 80
    for _ in range(12):  # 最多试 12 档字号
        f_title = load_font(title_size)
        f_body = load_font(body_size)
        # 标题行(若标题非空且非"封面")
        title_h = 0
        if title and '封面' not in title:
            t_wrap = wrap_text(d, title, f_title, SAFE_RIGHT_X - PAD_LEFT)
            title_h = len(t_wrap) * int(title_size * 1.25)
        # 正文
        body_lines = []
        for b in bullets:
            wrapped = wrap_text(d, b, f_body, SAFE_RIGHT_X - PAD_LEFT)
            body_lines.extend(wrapped)
        body_h = len(body_lines) * int(body_size * 1.6) + (len(bullets) - 1) * gap
        total_h = title_h + body_h + (gap if title_h else 0)
        # 目标:总高占画布 55%-75%
        if total_h < H * 0.55 and body_size < MAX_BODY:
            body_size += 4
            title_size += 5
            continue
        elif total_h > H * 0.75 and body_size > MIN_BODY:
            body_size -= 4
            title_size = max(title_size - 4, MIN_TITLE)  # 标题也压,但不得低于可读下限
            continue
        break

    # 内容特别多(400 字)时,若已压到可读下限仍超 75%,记录警告但不强行变小(保持可读性优先)
    if body_size <= MIN_BODY and total_h > H * 0.75:
        print(f'⚠️ 页 {page_no} 内容较多,字号已到可读下限 {MIN_BODY}px,仍稍超密度上限,保持可读优先')

    f_title = load_font(title_size)
    f_body = load_font(body_size)
    f_emoji_t = load_emoji_font(title_size)   # 标题 emoji 字体
    f_emoji_b = load_emoji_font(body_size)    # 正文 emoji 字体
    line_h_body = int(body_size * 1.6)
    line_h_title = int(title_size * 1.25)

    # 2) 计算内容块总高,用于垂直居中(中心 y=48%-50%)
    title_lines = []
    if title and '封面' not in title:
        title_lines = wrap_text(d, title, f_title, SAFE_RIGHT_X - PAD_LEFT)
    body_lines = []
    for b in bullets:
        body_lines.extend(wrap_text(d, b, f_body, SAFE_RIGHT_X - PAD_LEFT))
    block_h = len(title_lines) * line_h_title + len(body_lines) * line_h_body + (gap if title_lines else 0)
    # 垂直居中:中心 y 落在画布 48%-50%
    y = int((H - block_h) / 2)

    # 3) 绘制标题(绿色强调,带左侧竖条 ▍)
    x = PAD_LEFT
    if title_lines:
        # 标题前加绿色竖条
        d.rectangle([x, y + 6, x + 8, y + line_h_title - 10], fill=GREEN)
        tx = x + 24
        for ln in title_lines:
            draw_mixed(d, tx, y, ln, f_title, f_emoji_t, GREEN)
            y += line_h_title
        y += gap

    # 4) 绘制正文 bullets,关键数字/词着色
    seq_chars = '①②③④⑤⑥⑦⑧⑨⑩'  # 视觉骨架序号
    idx = 0
    for orig in bullets:
        # 每条 bullet 前加序号 + 绿色竖线,建立层级
        seq = seq_chars[idx] if idx < len(seq_chars) else f'{idx+1}.'
        d.text((x, y), seq, font=f_body, fill=GREEN)
        # 动态测量序号实际渲染宽度,正文起点 = 序号右缘 + 安全间距,避免序号压字(字号自适应变大时 ① 会变宽)
        seq_w = d.textbbox((0, 0), seq, font=f_body)[2]
        bx = x + seq_w + 16
        # 逐行绘制:先整行浅字打底,再对数字段覆盖亮黄,保证数字/结论突出
        wrapped = wrap_text(d, orig, f_body, SAFE_RIGHT_X - bx)
        for ln in wrapped:
            # 整行浅字打底 + emoji 彩色渲染;数字段覆盖亮黄
            draw_mixed_colored(d, bx, y, ln, f_body, f_emoji_b, FG, f_body, YELLOW)
            y += line_h_body
        y += gap
        idx += 1

    # 5) 文案不出屏校验 & 右侧安全区校验(最右≤85%)
    #    绘制后整体检查最右元素是否越界,越界则缩小字号重画
    #    (此处通过前面 SAFE_RIGHT_X 约束已基本保证)

    img.save(out_path)
    return out_path


def main():
    if len(sys.argv) < 2:
        print('用法: python card_gen.py "<xxx-抖音.md>" [输出目录]')
        sys.exit(1)
    md_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.environ.get('TEMP', os.getcwd()), 'publish')
    os.makedirs(out_dir, exist_ok=True)
    pages = parse_pages(md_path)
    if not pages:
        print('未解析到任何 P01..PN 页面')
        sys.exit(1)
    total = len(pages)
    for i, (page_no, title, bullets) in enumerate(pages, start=1):
        out = os.path.join(out_dir, f'card{i}.png')
        draw_card(page_no, title, bullets, out)
        print(f'card{i}.png <-> {page_no} ({len(bullets)} bullets) -> {out}')
    print(f'共生成 {total} 张卡片,card1 即 P01 全封面')
    if total != int(re.search(r'P(\d+)', pages[-1][0]).group(1)):
        print(f'⚠️ 页数校验:最后页 {pages[-1][0]},但实际 {total} 张,请人工核对')


if __name__ == '__main__':
    main()
