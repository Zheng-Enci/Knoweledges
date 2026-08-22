#!/usr/bin/env python3
"""
render-md.py — 将 Markdown 嵌入 HTML 模板并在浏览器中渲染

用法:
    python render-md.py <相对路径/某某.md>

流程:
    1. 读取指定 .md 文件
    2. 将内容嵌入内建 HTML 模板（JS 模板字面量）
    3. 在同目录生成 <文件名>.rendered.html
    4. 自动在默认浏览器打开

注意:
    - 自包含，不依赖外部模板文件
    - 需要网络加载 marked.js（CDN）
    - 生成的 .rendered.html 可分享给他人直接打开渲染
"""

import sys
import os
import json
import webbrowser
import argparse

# 内建 HTML 模板（对应原 md-renderer.html）
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MD Renderer</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  /* ===================== Theme Variables ===================== */
  :root,
  [data-theme="dark"] {
    --bg:          #1e1e2e;
    --surface:     #181825;
    --surface2:    #282840;
    --text:        #cdd6f4;
    --text-dim:    #a6adc8;
    --text-muted:  #6c7086;
    --accent:      #89b4fa;
    --accent2:     #a6e3a1;
    --accent3:     #cba6f7;
    --warn:        #f9e2af;
    --danger:      #f38ba8;
    --code-bg:     #11111b;
    --border:      #45475a;
    --shadow:      0 8px 32px rgba(0,0,0,.4);
    --header-bg:   rgba(30,30,46,.92);
    --scrollbar-thumb: #45475a;
    --scrollbar-hover:  #6c7086;
    --btn-bg:      #313244;
    --btn-hover:   #45475a;
  }

  [data-theme="light"] {
    --bg:          #eff1f5;
    --surface:     #e6e9ef;
    --surface2:    #dce0e8;
    --text:        #4c4f69;
    --text-dim:    #5c5f77;
    --text-muted:  #9ca0b0;
    --accent:      #1e66f5;
    --accent2:     #40a02b;
    --accent3:     #8839ef;
    --warn:        #df8e1d;
    --danger:      #d20f39;
    --code-bg:     #dce0e8;
    --border:      #ccd0da;
    --shadow:      0 8px 32px rgba(0,0,0,.1);
    --header-bg:   rgba(239,241,245,.92);
    --scrollbar-thumb: #bcc0cc;
    --scrollbar-hover:  #9ca0b0;
    --btn-bg:      #ccd0da;
    --btn-hover:   #bcc0cc;
  }

  /* ===================== Reset & Base ===================== */
  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans SC",
                 "PingFang SC", "Microsoft YaHei", sans-serif;
    line-height: 1.8;
    font-size: 16px;
    transition: background .25s, color .25s;
  }

  /* ===================== Scrollbar ===================== */
  ::-webkit-scrollbar { width: 8px; height: 8px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb {
    background: var(--scrollbar-thumb);
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover { background: var(--scrollbar-hover); }

  /* ===================== Header ===================== */
  .header {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: var(--header-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 0 24px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: background .25s;
  }

  .header-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    white-space: nowrap;
    letter-spacing: .5px;
  }

  .header-path {
    flex: 1;
    font-size: 13px;
    color: var(--text-muted);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding: 0 8px;
    font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  /* ===================== Buttons ===================== */
  .btn {
    background: var(--btn-bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    cursor: pointer;
    transition: background .15s, color .15s, border-color .15s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
    font-family: inherit;
  }
  .btn:hover { background: var(--btn-hover); }

  .btn-icon {
    width: 36px; height: 36px;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    font-size: 18px;
    line-height: 1;
  }

  /* ===================== File Picker ===================== */
  .file-picker { display: none; }

  /* ===================== Main Content ===================== */
  .main {
    max-width: 960px;
    margin: 0 auto;
    padding: 80px 24px 80px;
  }

  /* ===================== State Screens ===================== */
  .state-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 50vh;
    text-align: center;
    gap: 16px;
    color: var(--text-muted);
  }
  .state-screen .icon { font-size: 48px; line-height: 1; }
  .state-screen .hint  { font-size: 14px; max-width: 480px; }
  .state-screen .sub   { font-size: 13px; color: var(--text-muted); }

  .error-icon { color: var(--danger); }

  .loading-indicator {
    display: inline-block;
    width: 32px; height: 32px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin .8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* ===================== Markdown Content ===================== */
  .content { animation: fadeIn .3s ease; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

  .content h1 {
    font-size: 2.2em;
    text-align: center;
    color: var(--accent);
    margin-bottom: 8px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--border);
  }

  .content h1 + p {
    text-align: center;
    color: var(--text-muted);
    margin-bottom: 32px;
  }

  .content h2 {
    font-size: 1.6em;
    color: var(--accent2);
    margin-top: 48px;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }

  .content h3 {
    font-size: 1.3em;
    color: var(--accent);
    margin-top: 32px;
    margin-bottom: 12px;
  }

  .content h4 {
    font-size: 1.1em;
    color: var(--accent3);
    margin-top: 20px;
    margin-bottom: 8px;
  }

  .content p { margin-bottom: 14px; }
  .content a { color: var(--accent); text-decoration: none; }
  .content a:hover { text-decoration: underline; }

  .content ul,
  .content ol { margin: 8px 0 16px 24px; }
  .content li { margin-bottom: 4px; }

  .content blockquote {
    border-left: 3px solid var(--accent);
    padding: 8px 16px;
    margin: 16px 0;
    background: var(--surface2);
    border-radius: 0 8px 8px 0;
    color: var(--text-dim);
  }

  .content img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 16px 0;
  }

  .content hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
  }

  .content strong { color: var(--warn); }

  /* ===================== Tables ===================== */
  .content table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: .95em;
  }
  .content th,
  .content td {
    padding: 10px 14px;
    text-align: left;
    border: 1px solid var(--border);
  }
  .content th {
    background: var(--surface2);
    color: var(--accent);
    font-weight: 600;
  }
  .content tr:nth-child(even) td { background: var(--surface); }

  /* ===================== Code ===================== */
  .content code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", Consolas, monospace;
    font-size: .88em;
    color: var(--danger);
  }

  .content pre {
    background: var(--code-bg);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 16px 0;
    border: 1px solid var(--border);
  }
  .content pre code {
    background: none;
    padding: 0;
    color: var(--text);
    font-size: .86em;
    line-height: 1.6;
  }

  .content :not(pre) > code {
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    word-break: break-word;
  }

  /* ===================== Responsive ===================== */
  @media (max-width: 640px) {
    .header { padding: 0 12px; gap: 8px; }
    .header-title { font-size: 12px; }
    .header-path { font-size: 11px; }
    .main { padding: 72px 12px 40px; }
    .content h1 { font-size: 1.6em; }
    .content h2 { font-size: 1.3em; }
    .btn { font-size: 12px; padding: 4px 10px; }
    .btn-icon { width: 32px; height: 32px; font-size: 16px; }
  }

</style>
</head>
<body>

<!-- ==================== Header ==================== -->
<header class="header">
  <span class="header-title">MD Renderer</span>
  <span class="header-path" id="filePath">-- no file loaded</span>
  <div class="header-actions">
    <button class="btn btn-icon" id="btnTheme" title="Toggle theme">&#9728;&#65039;</button>
  </div>
</header>

<!-- ==================== Main Content Area ==================== -->
<main class="main" id="main">
  <div class="state-screen" id="welcome">
    <div class="icon">&#128196;</div>
    <div class="hint">
      Drop a <code>.md</code> file here, or click the file picker button below
      to open a document from your local filesystem.
    </div>
    <button class="btn" id="btnOpenFile" style="margin-top:16px;font-size:15px;padding:10px 24px;">
      &#128194; Open MD File
    </button>
    <div class="sub" style="margin-top:16px;">
      Or append <code>?file=path/to/doc.md</code> to the URL.
    </div>
  </div>
  <div class="content" id="content" style="display:none"></div>
</main>

<!-- ==================== Hidden File Input ==================== -->
<input type="file" accept=".md" id="fileInput" class="file-picker">

<script>
  (function() {
    'use strict';

    // =============================
    //  State
    // =============================
    const state = {
      currentFile: null,  // relative path string
    };

    // =============================
    //  DOM refs
    // =============================
    const $ = id => document.getElementById(id);
    const main        = $('main');
    const content     = $('content');
    const welcome     = $('welcome');
    const filePath    = $('filePath');
    const btnTheme    = $('btnTheme');
    const fileInput   = $('fileInput');

    // =============================
    //  Theme
    // =============================
    function getTheme() {
      return localStorage.getItem('md-renderer-theme') || 'dark';
    }

    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('md-renderer-theme', theme);
      btnTheme.textContent = theme === 'dark' ? '\\u2600\\ufe0f' : '\\ud83c\\udf19';
    }

    function toggleTheme() {
      setTheme(getTheme() === 'dark' ? 'light' : 'dark');
    }

    // init theme
    setTheme(getTheme());

    // =============================
    //  Helpers
    // =============================
    function showError(msg) {
      content.style.display = 'none';
      welcome.style.display = 'flex';
      welcome.innerHTML = `
        <div class="icon error-icon">\u26a0\ufe0f</div>
        <div class="hint">${msg}</div>
        <div class="sub">Try another file or check the path.</div>
      `;
    }

    function showLoading() {
      content.style.display = 'none';
      welcome.style.display = 'flex';
      welcome.innerHTML = `
        <div><span class="loading-indicator"></span></div>
        <div class="hint">Loading document...</div>
      `;
    }

    function renderMarkdown(mdText, fileRelPath) {
      content.innerHTML = marked.parse(mdText);
      content.style.display = 'block';
      welcome.style.display = 'none';
      filePath.textContent = fileRelPath || '-- loaded from file picker';
      state.currentFile = fileRelPath || null;
      // update URL without reload
      if (fileRelPath) {
        const u = new URL(window.location);
        u.searchParams.set('file', fileRelPath);
        window.history.replaceState({}, '', u);
      }
    }

    // =============================
    //  Load from URL param
    // =============================
    function loadFromUrl() {
      const u = new URL(window.location);
      const file = u.searchParams.get('file');
      if (!file) return false;

      showLoading();
      fetch(file)
        .then(r => {
          if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.statusText}`);
          return r.text();
        })
        .then(md => renderMarkdown(md, file))
        .catch(err => showError(`Failed to load <code>${file}</code>: ${err.message}`));
      return true;
    }

    // =============================
    //  File input handler
    // =============================
    fileInput.addEventListener('change', function(e) {
      const f = this.files[0];
      if (!f) return;
      state.currentFile = null;
      const reader = new FileReader();
      reader.onload = function(ev) {
        renderMarkdown(ev.target.result, f.name);
      };
      reader.onerror = function() {
        showError(`Failed to read <code>${f.name}</code>.`);
      };
      reader.readAsText(f);
      this.value = ''; // allow re-selecting same file
    });

    // =============================
    //  Open File button -> trigger file input
    // =============================
    document.getElementById('btnOpenFile').addEventListener('click', function() {
      fileInput.click();
    });

    // =============================
    //  Drag & drop
    // =============================
    document.addEventListener('dragover', function(e) { e.preventDefault(); });
    document.addEventListener('drop', function(e) {
      e.preventDefault();
      const f = e.dataTransfer.files[0];
      if (!f || !f.name.endsWith('.md')) {
        showError('Please drop a valid <code>.md</code> file.');
        return;
      }
      state.currentFile = null;
      const reader = new FileReader();
      reader.onload = function(ev) {
        renderMarkdown(ev.target.result, f.name);
      };
      reader.onerror = function() {
        showError(`Failed to read <code>${f.name}</code>.`);
      };
      reader.readAsText(f);
    });

    // =============================
    //  Theme toggle
    // =============================
    btnTheme.addEventListener('click', toggleTheme);

    // =============================
    //  Keyboard shortcuts
    // =============================
    document.addEventListener('keydown', function(e) {
      if (e.key === 't' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        toggleTheme();
      }
    });

    // =============================
    //  Init: load from URL or show welcome
    // =============================
    if (!loadFromUrl()) {
      // show welcome state (already displayed in HTML)
    }
  })();
</script>
</body>
</html>"""


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='将 Markdown 嵌入 HTML 并打开浏览器渲染')
    parser.add_argument('md_path', help='Markdown 文件路径（支持相对路径）')
    args = parser.parse_args()

    # 获取 md 文件的绝对路径
    md_path = os.path.abspath(args.md_path)
    if not os.path.isfile(md_path):
        print(f"错误: 文件不存在 → {md_path}")
        sys.exit(1)

    # 读取 md 文件内容
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 输出路径: md 文件同目录，生成 <文件名>.rendered.html
    md_dir = os.path.dirname(md_path)
    md_basename = os.path.splitext(os.path.basename(md_path))[0]
    output_name = f"{md_basename}.rendered.html"
    output_path = os.path.join(md_dir, output_name)

    # 将 md 内容转义为 JS 模板字面量（反引号字符串）安全
    # 需要转义: 反斜杠、反引号、${ 插值表达式
    escaped = md_content.replace('\\', '\\\\') \
                        .replace('`', '\\`') \
                        .replace('${', '\\${')

    # 注入自动渲染脚本（在 marked 加载后执行）
    auto_render = f'''
<script>
(function() {{
    'use strict';
    var mdContent = `{escaped}`;
    var content = document.getElementById('content');
    var welcome = document.getElementById('welcome');
    var filePath = document.getElementById('filePath');
    content.innerHTML = marked.parse(mdContent);
    content.style.display = 'block';
    welcome.style.display = 'none';
    filePath.textContent = {json.dumps(os.path.basename(md_path))};
}})();
</script>
'''

    # 从内建模板创建 HTML，在 </body> 前注入脚本
    html = HTML_TEMPLATE.replace('</body>', auto_render + '\n</body>')

    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ 已生成: {output_path}")

    # 在默认浏览器中打开
    file_url = 'file://' + output_path.replace('\\', '/')
    webbrowser.open(file_url)
    print(f"✓ 已在浏览器中打开: {file_url}")


if __name__ == '__main__':
    main()
