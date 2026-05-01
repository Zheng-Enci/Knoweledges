# 自定义 CSS 样式指南 Custom CSS Guide

本文档详细介绍如何在 markconv 中使用自定义 CSS 样式来美化 HTML 和 PDF 输出。

This document details how to use custom CSS styles in markconv to beautify HTML and PDF outputs.

---

## 📖 目录 Table of Contents

1. [快速开始 Quick Start](#快速开始-quick-start)
2. [CSS 工作原理 How CSS Works](#css-工作原理-how-css-works)
3. [内置样式详解 Built-in Styles](#内置样式详解-built-in-styles)
4. [自定义 CSS 方法 Custom CSS Methods](#自定义-css-方法-custom-css-methods)
5. [常用样式示例 Common Style Examples](#常用样式示例-common-style-examples)
6. [PDF 专属样式 PDF Specific Styles](#pdf-专属样式-pdf-specific-styles)
7. [HTML 专属样式 HTML Specific Styles](#html-专属样式-html-specific-styles)
8. [Mermaid 图表样式 Mermaid Diagram Styles](#mermaid-图表样式-mermaid-diagram-styles)
9. [最佳实践 Best Practices](#最佳实践-best-practices)

---

## 快速开始 Quick Start

### 基本用法 Basic Usage

```python
from markconv import MDConverter

# 方法1：使用 CSS 文件 Method 1: Using CSS file
converter = MDConverter(css_file="custom.css")
converter.to_html("input.md", "output.html")
converter.to_pdf("input.md", "output.pdf")

# 方法2：不使用自定义样式（使用默认样式）Method 2: No custom styles (use defaults)
converter = MDConverter()
converter.to_html("input.md", "output.html")
```

### 创建自定义 CSS 文件 Create Custom CSS File

创建 `custom.css` 文件：Create a `custom.css` file:

```css
/* custom.css */

/* 修改正文颜色 Change body text color */
body {
    color: #2c3e50;
    background-color: #f8f9fa;
}

/* 修改标题颜色 Change heading colors */
h1, h2, h3 {
    color: #e74c3c;
    border-bottom: 2px solid #e74c3c;
    padding-bottom: 10px;
}

/* 修改代码块样式 Change code block styles */
pre {
    background-color: #2d2d2d;
    color: #f8f8f2;
    border-radius: 8px;
}
```

---

## CSS 工作原理 How CSS Works

### 样式加载顺序 Style Loading Order

markconv 的样式按照以下顺序加载（后面的样式会覆盖前面的）：

Styles are loaded in the following order (later styles override earlier ones):

1. **内置默认样式 Built-in Default Styles**
   - 基础排版样式（字体、行高、边距）
   - 代码高亮样式（codehilite）
   - 表格、引用块、链接等基础样式

2. **自定义 CSS 文件 Custom CSS File**
   - 通过 `css_file` 参数传入的 CSS 文件内容
   - 插入在 `<style>` 标签的末尾，覆盖默认样式

### CSS 插入位置 CSS Insertion Point

在生成的 HTML 中，自定义 CSS 被插入在这里：

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        /* 内置默认样式（约 200+ 行） */
        body { ... }
        h1, h2, h3 { ... }
        /* ... 其他默认样式 ... */
        
        /* 自定义 CSS 插入位置 Insertion point for custom CSS */
        /* ===== 您的自定义 CSS 从这里开始 ===== */
        body { color: #2c3e50; }
        /* ... */
    </style>
</head>
```

---

## 内置样式详解 Built-in Styles

### 1. 基础排版样式 Base Typography

```css
/* 正文样式 Body styles */
body {
    font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;  /* 中文字体支持 */
    line-height: 1.6;          /* 行高 */
    margin: 20px;              /* 外边距 */
    color: #333;               /* 文字颜色 */
    max-width: 1200px;         /* 最大宽度 */
    margin: 0 auto;            /* 水平居中 */
    padding: 20px;             /* 内边距 */
}
```

### 2. 标题样式 Heading Styles

```css
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;            /* 标题颜色 */
    margin-top: 20px;          /* 上边距 */
    margin-bottom: 10px;       /* 下边距 */
}
```

### 3. 代码样式 Code Styles

```css
/* 行内代码 Inline code */
code {
    background-color: #f4f4f4; /* 背景色 */
    padding: 2px 6px;          /* 内边距 */
    border-radius: 3px;        /* 圆角 */
    font-family: 'Consolas', 'Monaco', monospace;  /* 等宽字体 */
}

/* 代码块 Code blocks */
pre {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;          /* 水平滚动 */
}

/* 代码高亮容器 Code highlight container */
.codehilite {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 15px 0;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}
```

### 4. 代码高亮颜色 Code Highlight Colors

```css
/* 关键字 Keyword */
.codehilite .k { color: #900; font-weight: bold; }

/* 函数名 Function name */
.codehilite .nf { color: #069; font-weight: bold; }

/* 内置名称 Built-in name */
.codehilite .nb { color: #008080; }

/* 字符串 String */
.codehilite .s2 { color: #d14; }

/* 数字 Number */
.codehilite .m { color: #099; }

/* 注释 Comment */
.codehilite .c { color: #60a0b0; font-style: italic; }
```

### 5. 表格样式 Table Styles

```css
table {
    border-collapse: collapse;  /* 合并边框 */
    width: 100%;                /* 宽度 */
    margin: 20px 0;             /* 外边距 */
}

th, td {
    border: 1px solid #ddd;     /* 边框 */
    padding: 8px;               /* 内边距 */
    text-align: left;           /* 左对齐 */
}

th {
    background-color: #f2f2f2;  /* 表头背景色 */
}
```

### 6. 引用块样式 Blockquote Styles

```css
blockquote {
    border-left: 4px solid #ddd;  /* 左边框 */
    margin: 0;
    padding-left: 20px;           /* 左内边距 */
    color: #666;                  /* 文字颜色 */
}
```

### 7. 链接样式 Link Styles

```css
a {
    color: #3498db;               /* 链接颜色 */
    text-decoration: none;        /* 无下划线 */
}

a:hover {
    text-decoration: underline;   /* 悬停下划线 */
}
```

### 8. 图片样式 Image Styles

```css
img {
    max-width: 100%;              /* 最大宽度 */
    height: auto;                 /* 高度自适应 */
}
```

### 9. 分隔线样式 Horizontal Rule Styles

```css
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
}
```

---

## 自定义 CSS 方法 Custom CSS Methods

### 方法 1：使用 CSS 文件 Method 1: Using CSS File

**推荐方式 Recommended method**

```python
from markconv import MDConverter

# 创建转换器，指定 CSS 文件
converter = MDConverter(css_file="custom.css")

# 转换为 HTML 和 PDF
converter.to_html("document.md", "output.html")
converter.to_pdf("document.md", "output.pdf")
```

### 方法 2：仅 HTML 导出使用自定义样式 Method 2: HTML Export Only

```python
from markconv import MDConverter

converter = MDConverter()

# HTML 使用自定义样式
converter.to_html("document.md", "output.html")

# PDF 使用默认样式（PDF 也会读取 css_file）
# 注意：PDF 导出也会使用 MDConverter 初始化时的 css_file
```

### 方法 3：动态生成 CSS Method 3: Dynamic CSS Generation

```python
import tempfile
import os
from markconv import MDConverter

# 动态生成 CSS 内容
css_content = """
body {
    background-color: #f0f0f0;
    color: #333;
}
h1 {
    color: #e74c3c;
}
"""

# 创建临时 CSS 文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8') as f:
    f.write(css_content)
    css_file = f.name

try:
    # 使用临时 CSS 文件
    converter = MDConverter(css_file=css_file)
    converter.to_html("document.md", "output.html")
    converter.to_pdf("document.md", "output.pdf")
finally:
    # 清理临时文件
    os.unlink(css_file)
```

---

## 常用样式示例 Common Style Examples

### 示例 1：深色主题 Dark Theme

```css
/* dark-theme.css */

/* 页面背景 Page background */
body {
    background-color: #1a1a2e;
    color: #eaeaea;
}

/* 标题颜色 Heading colors */
h1, h2, h3, h4, h5, h6 {
    color: #16213e;
    border-bottom: 2px solid #0f3460;
    padding-bottom: 10px;
}

/* 代码块背景 Code block background */
pre, .codehilite {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
}

/* 行内代码 Inline code */
code {
    background-color: #343942;
    color: #e6edf3;
}

/* 链接颜色 Link colors */
a {
    color: #58a6ff;
}

/* 表格样式 Table styles */
table {
    border-color: #30363d;
}

th {
    background-color: #21262d;
}

td {
    border-color: #30363d;
}

/* 引用块 Blockquote */
blockquote {
    border-left-color: #30363d;
    color: #8b949e;
}
```

### 示例 2：学术文档样式 Academic Document Style

```css
/* academic.css */

/* 页面设置 Page settings */
body {
    font-family: 'Times New Roman', 'SimSun', serif;
    font-size: 12pt;
    line-height: 1.5;
    max-width: 210mm;  /* A4 宽度 */
    margin: 0 auto;
    padding: 25mm;     /* 页边距 */
    text-align: justify;  /* 两端对齐 */
}

/* 标题样式 Heading styles */
h1 {
    font-size: 18pt;
    text-align: center;
    margin-bottom: 20pt;
}

h2 {
    font-size: 14pt;
    border-bottom: 1px solid #000;
    padding-bottom: 5pt;
}

h3 {
    font-size: 12pt;
    font-weight: bold;
}

/* 段落首行缩进 Paragraph indentation */
p {
    text-indent: 2em;
    margin: 0;
}

/* 代码字体 Code font */
pre, code {
    font-family: 'Courier New', monospace;
    font-size: 10pt;
}

/* 表格居中 Table centering */
table {
    margin: 20px auto;
    font-size: 10pt;
}

/* 图片居中 Image centering */
img {
    display: block;
    margin: 20px auto;
}
```

### 示例 3：商务报告样式 Business Report Style

```css
/* business.css */

/* 品牌色 Brand colors */
:root {
    --primary-color: #0056b3;
    --secondary-color: #6c757d;
    --accent-color: #28a745;
}

body {
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    color: #333;
    line-height: 1.6;
}

/* 标题带品牌色 Headings with brand color */
h1 {
    color: var(--primary-color);
    font-size: 28px;
    border-bottom: 3px solid var(--primary-color);
    padding-bottom: 10px;
}

h2 {
    color: var(--primary-color);
    font-size: 22px;
    margin-top: 30px;
}

h3 {
    color: var(--secondary-color);
    font-size: 18px;
}

/* 强调文本 Emphasis text */
strong {
    color: var(--primary-color);
}

/* 高亮背景 Highlight background */
mark {
    background-color: #fff3cd;
    padding: 2px 4px;
}

/* 表格样式 Table styles */
table {
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th {
    background-color: var(--primary-color);
    color: white;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}

/* 引用块样式 Blockquote styles */
blockquote {
    background-color: #f8f9fa;
    border-left: 4px solid var(--accent-color);
    padding: 15px 20px;
    margin: 20px 0;
    border-radius: 0 4px 4px 0;
}
```

### 示例 4：阅读友好样式 Reading Friendly Style

```css
/* reading-friendly.css */

/* 大字体和舒适的行高 Large font and comfortable line height */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
    font-size: 18px;
    line-height: 1.8;
    color: #2c3e50;
    background-color: #fafafa;
    max-width: 800px;  /* 限制行宽，提高可读性 */
}

/* 标题层级清晰 Clear heading hierarchy */
h1 {
    font-size: 32px;
    margin-top: 50px;
}

h2 {
    font-size: 26px;
    margin-top: 40px;
}

h3 {
    font-size: 22px;
    margin-top: 30px;
}

/* 段落间距 Paragraph spacing */
p {
    margin: 20px 0;
}

/* 列表样式 List styles */
ul, ol {
    padding-left: 30px;
}

li {
    margin: 10px 0;
}

/* 代码块样式 Code block styles */
pre {
    background-color: #f4f4f4;
    border-left: 4px solid #007acc;
    padding: 20px;
    overflow-x: auto;
}

/* 图片阴影 Image shadow */
img {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    border-radius: 4px;
}

/* 链接样式 Link styles */
a {
    color: #007acc;
    border-bottom: 1px dotted #007acc;
    transition: all 0.3s ease;
}

a:hover {
    background-color: #e6f3ff;
    border-bottom-style: solid;
}
```

---

## PDF 专属样式 PDF Specific Styles

### PDF 渲染注意事项 PDF Rendering Notes

PDF 使用 `pdfkit` 和 `wkhtmltopdf` 进行渲染，某些 CSS 属性可能支持不完整：

PDF uses `pdfkit` and `wkhtmltopdf` for rendering, some CSS properties may have limited support:

**支持的属性 Supported properties:**
- 字体、颜色、背景色 Fonts, colors, background colors
- 边距、内边距 Margins, padding
- 边框 Borders
- 宽度、高度 Width, height
- 文本对齐 Text alignment

**有限支持的属性 Limited support:**
- CSS3 动画和过渡 CSS3 animations and transitions
- 某些高级选择器 Some advanced selectors
- flexbox（部分支持）Flexbox (partial support)

### PDF 打印优化 Print Optimization

```css
/* pdf-print.css */

/* 页面设置 Page settings */
@page {
    size: A4;
    margin: 20mm;
}

/* 避免元素跨页断行 Avoid page breaks inside elements */
pre, blockquote, table {
    page-break-inside: avoid;
}

/* 标题避免在页面底部 Headings avoid bottom of page */
h1, h2, h3 {
    page-break-after: avoid;
}

/* 图片避免跨页 Images avoid page breaks */
img {
    page-break-inside: avoid;
    max-width: 100% !important;
}

/* 打印时隐藏的元素 Elements hidden when printing */
.no-print {
    display: none;
}

/* 确保背景色打印 Print background colors */
* {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
```

---

## HTML 专属样式 HTML Specific Styles

### 响应式设计 Responsive Design

```css
/* responsive.css */

/* 移动端适配 Mobile adaptation */
@media screen and (max-width: 768px) {
    body {
        padding: 10px;
        font-size: 16px;
    }
    
    h1 {
        font-size: 24px;
    }
    
    pre {
        padding: 10px;
        font-size: 14px;
    }
    
    table {
        font-size: 14px;
    }
}

/* 暗黑模式 Dark mode */
@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a2e;
        color: #eaeaea;
    }
    
    pre, .codehilite {
        background-color: #0d1117;
    }
}
```

### 交互效果 Interactive Effects

```css
/* interactive.css */

/* 平滑滚动 Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* 代码块悬停效果 Code block hover effect */
pre:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: box-shadow 0.3s ease;
}

/* 图片悬停效果 Image hover effect */
img:hover {
    transform: scale(1.02);
    transition: transform 0.3s ease;
}

/* 链接动画 Link animation */
a {
    position: relative;
    transition: color 0.3s ease;
}

a::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: currentColor;
    transition: width 0.3s ease;
}

a:hover::after {
    width: 100%;
}
```

---

## Mermaid 图表样式 Mermaid Diagram Styles

### HTML 中的 Mermaid 样式 Mermaid Styles in HTML

HTML 导出使用 Mermaid.js 在浏览器中渲染图表：

HTML export uses Mermaid.js to render diagrams in the browser:

```css
/* mermaid-html.css */

/* Mermaid 图表容器 Mermaid diagram container */
.mermaid {
    display: flex;
    justify-content: center;
    margin: 20px 0;
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
}

/* 图表标题 Diagram title */
.mermaid-title {
    text-align: center;
    font-weight: bold;
    margin-bottom: 10px;
}
```

### PDF 中的 Mermaid 样式 Mermaid Styles in PDF

PDF 中的 Mermaid 图表被渲染为图片，可以通过包裹元素的样式控制：

Mermaid diagrams in PDF are rendered as images and can be controlled through wrapper element styles:

```css
/* mermaid-pdf.css */

/* Mermaid 图片居中 Center Mermaid images */
div[style*="text-align: center"] img {
    max-width: 90%;
    margin: 20px auto;
    display: block;
}

/* Mermaid 图片背景 Background for Mermaid images */
div[style*="text-align: center"] {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}
```

---

## 最佳实践 Best Practices

### 1. CSS 文件组织 CSS File Organization

```
project/
├── markdown/
│   └── document.md
├── css/
│   ├── default.css      # 基础样式
│   ├── dark-theme.css   # 深色主题
│   ├── academic.css     # 学术样式
│   └── business.css     # 商务样式
└── output/
    └── document.html
```

### 2. 样式优先级管理 Style Priority Management

```css
/* 使用 !important 谨慎覆盖 Careful override with !important */
/* 不推荐 Not recommended */
body {
    color: red !important;
}

/* 推荐：提高选择器特异性 Recommended: Increase selector specificity */
body.custom-theme {
    color: #2c3e50;
}

/* 或者使用更具体的选择器 Or use more specific selectors */
html body {
    color: #2c3e50;
}
```

### 3. 跨平台字体设置 Cross-platform Font Settings

```css
/* 中文字体栈 Chinese font stack */
body {
    font-family: 
        -apple-system,          /* macOS/iOS 系统字体 */
        BlinkMacSystemFont,     /* macOS Chrome */
        'Segoe UI',             /* Windows 系统字体 */
        'Microsoft YaHei',      /* Windows 中文字体 */
        'SimHei',               /* 备选黑体 */
        'SimSun',               /* 备选宋体 */
        Arial,                  /* 西文备选 */
        sans-serif;             /* 通用无衬线 */
}

/* 代码字体 Code font stack */
code, pre {
    font-family: 
        'Consolas',             /* Windows */
        'Monaco',               /* macOS */
        'Courier New',          /* 通用 */
        monospace;
}
```

### 4. 调试技巧 Debugging Tips

```python
# 查看生成的 HTML 中的 CSS View CSS in generated HTML
from markconv import MDConverter

converter = MDConverter(css_file="custom.css")

# 使用 export_to_string 查看完整 HTML
from markconv.parsers import MarkdownParser
from markconv.exporters import HTMLExporter

parser = MarkdownParser()
exporter = HTMLExporter(css_file="custom.css")

parsed = parser.parse_file("document.md")
html_content = exporter.export_to_string(parsed)

# 保存并查看 CSS 部分 Save and view CSS section
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(html_content)
```

### 5. 性能优化 Performance Optimization

```css
/* 避免使用过于复杂的选择器 Avoid overly complex selectors */
/* 不推荐 Not recommended */
body > div.container > div.content > p > span {
    color: red;
}

/* 推荐 Recommended */
.highlight-text {
    color: red;
}

/* 压缩 CSS（生产环境）Minify CSS (production) */
body{font-family:Arial,sans-serif;line-height:1.6;color:#333}
```

---

## 完整示例代码 Complete Example Code

```python
# example.py
from markconv import MDConverter

# 使用自定义 CSS 文件 Use custom CSS file
converter = MDConverter(css_file="styles/custom.css")

# 转换为 HTML Convert to HTML
converter.to_html(
    input_path="document.md",
    output_path="output/document.html"
)

# 转换为 PDF（同样使用自定义 CSS）Convert to PDF (also uses custom CSS)
converter.to_pdf(
    input_path="document.md",
    output_path="output/document.pdf"
)

print("转换完成！Conversion completed!")
```

---

## 常见问题 FAQ

**Q: 自定义 CSS 对 PDF 也有效吗？**
A: 是的，PDF 导出同样会应用自定义 CSS 文件中的样式。

**Q: 如何覆盖内置样式？**
A: 在自定义 CSS 中使用相同的选择器，或者使用更具体的选择器。

**Q: CSS 文件路径可以是相对路径吗？**
A: 可以，相对路径是相对于当前工作目录的。

**Q: 支持哪些 CSS 选择器？**
A: 支持大多数标准 CSS2/3 选择器，但 PDF 渲染可能不支持某些高级选择器。

**Q: 可以使用 CSS 框架吗？**
A: 可以，但需要将框架 CSS 内容复制到自定义 CSS 文件中，目前不支持外部 CSS 链接。

---

## 参考链接 Reference Links

- [MDN CSS 文档](https://developer.mozilla.org/zh-CN/docs/Web/CSS)
- [CSS-Tricks](https://css-tricks.com/)
- [wkhtmltopdf CSS 支持](https://wkhtmltopdf.org/)

---

*本文档最后更新于 2026-05-01*
*This document was last updated on 2026-05-01*
