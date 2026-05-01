# M5-markconv自定义CSS样式指南 📝

本文档介绍 markconv 支持的自定义 CSS 样式功能，用于美化 HTML 和 PDF 输出。

---

## 1 快速开始 🚀

### 基本用法

```python
from markconv import MDConverter

converter = MDConverter(css_file="custom.css")
converter.to_html("input.md", "output.html")
converter.to_pdf("input.md", "output.pdf")
```

### 创建 CSS 文件

```css
/* custom.css */
body {
    color: #2c3e50;
    background-color: #f8f9fa;
}

h1, h2, h3 {
    color: #e74c3c;
    border-bottom: 2px solid #e74c3c;
    padding-bottom: 10px;
}

pre {
    background-color: #2d2d2d;
    color: #f8f8f2;
    border-radius: 8px;
}
```

---

## 2 样式加载原理 📋

markconv 的样式加载顺序如下，后加载的样式会覆盖前面的：

### 加载顺序

1. **内置默认样式**：基础排版、代码高亮、表格、引用块、链接等
2. **自定义 CSS 文件**：通过 `css_file` 参数传入，插入在 `<style>` 标签末尾

### CSS 插入位置

```html
<style>
    /* 内置默认样式 */
    body { ... }
    
    /* 自定义 CSS 插入位置 */
    body { color: #2c3e50; }
</style>
```

---

## 3 内置样式详解 🎨

### 基础排版

```css
body {
    font-family: 'Microsoft YaHei', 'SimHei', Arial, sans-serif;
    line-height: 1.6;
    margin: 20px;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
```

### 标题样式

```css
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 20px;
    margin-bottom: 10px;
}
```

### 代码样式

```css
code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Consolas', 'Monaco', monospace;
}

pre {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
}

.codehilite {
    background-color: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 15px 0;
}
```

### 代码高亮颜色

```css
.codehilite .k { color: #900; font-weight: bold; }
.codehilite .nf { color: #069; font-weight: bold; }
.codehilite .nb { color: #008080; }
.codehilite .s2 { color: #d14; }
.codehilite .m { color: #099; }
.codehilite .c { color: #60a0b0; font-style: italic; }
```

### 表格样式

```css
table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}
```

### 引用块样式

```css
blockquote {
    border-left: 4px solid #ddd;
    margin: 0;
    padding-left: 20px;
    color: #666;
}
```

### 链接样式

```css
a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
```

### 图片样式

```css
img {
    max-width: 100%;
    height: auto;
}
```

---

## 4 自定义 CSS 方法 🔧

### 方法一：使用 CSS 文件（推荐）

```python
from markconv import MDConverter

converter = MDConverter(css_file="custom.css")
converter.to_html("document.md", "output.html")
converter.to_pdf("document.md", "output.pdf")
```

### 方法二：动态生成 CSS

```python
import tempfile
import os
from markconv import MDConverter

css_content = """
body {
    background-color: #f0f0f0;
    color: #333;
}
h1 {
    color: #e74c3c;
}
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8') as f:
    f.write(css_content)
    css_file = f.name

try:
    converter = MDConverter(css_file=css_file)
    converter.to_html("document.md", "output.html")
finally:
    os.unlink(css_file)
```

---

## 5 常用样式示例 💡

### 示例一：深色主题

```css
body {
    background-color: #1a1a2e;
    color: #eaeaea;
}

h1, h2, h3 {
    color: #16213e;
    border-bottom: 2px solid #0f3460;
}

pre, .codehilite {
    background-color: #0d1117;
    color: #c9d1d9;
    border: 1px solid #30363d;
}

code {
    background-color: #343942;
    color: #e6edf3;
}

a {
    color: #58a6ff;
}

table {
    border-color: #30363d;
}

th {
    background-color: #21262d;
}

blockquote {
    border-left-color: #30363d;
    color: #8b949e;
}
```

### 示例二：学术文档样式

```css
body {
    font-family: 'Times New Roman', 'SimSun', serif;
    font-size: 12pt;
    line-height: 1.5;
    max-width: 210mm;
    margin: 0 auto;
    padding: 25mm;
    text-align: justify;
}

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

p {
    text-indent: 2em;
    margin: 0;
}

table {
    margin: 20px auto;
    font-size: 10pt;
}
```

### 示例三：商务报告样式

```css
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

h1 {
    color: var(--primary-color);
    font-size: 28px;
    border-bottom: 3px solid var(--primary-color);
}

th {
    background-color: var(--primary-color);
    color: white;
}

tr:nth-child(even) {
    background-color: #f8f9fa;
}
```

### 示例四：阅读友好样式

```css
body {
    font-size: 18px;
    line-height: 1.8;
    color: #2c3e50;
    background-color: #fafafa;
    max-width: 800px;
}

h1 { font-size: 32px; margin-top: 50px; }
h2 { font-size: 26px; margin-top: 40px; }
h3 { font-size: 22px; margin-top: 30px; }

p { margin: 20px 0; }

pre {
    background-color: #f4f4f4;
    border-left: 4px solid #007acc;
    padding: 20px;
}

img {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    border-radius: 4px;
}
```

---

## 6 PDF 专属样式 📄

### 渲染注意事项

PDF 使用 `pdfkit` 和 `wkhtmltopdf` 渲染，部分 CSS 属性支持有限：

**支持的属性**：字体、颜色、背景色、边距、边框、宽度、高度、文本对齐

**有限支持的属性**：CSS3 动画和过渡、某些高级选择器、flexbox

### 打印优化

```css
@page {
    size: A4;
    margin: 20mm;
}

pre, blockquote, table {
    page-break-inside: avoid;
}

h1, h2, h3 {
    page-break-after: avoid;
}

img {
    page-break-inside: avoid;
    max-width: 100% !important;
}

* {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
}
```

---

## 7 HTML 专属样式 🌐

### 响应式设计

```css
@media screen and (max-width: 768px) {
    body {
        padding: 10px;
        font-size: 16px;
    }
    
    h1 { font-size: 24px; }
    pre { padding: 10px; font-size: 14px; }
}

@media (prefers-color-scheme: dark) {
    body {
        background-color: #1a1a2e;
        color: #eaeaea;
    }
}
```

### 交互效果

```css
html {
    scroll-behavior: smooth;
}

pre:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: box-shadow 0.3s ease;
}

img:hover {
    transform: scale(1.02);
    transition: transform 0.3s ease;
}
```

---

## 8 Mermaid 图表样式 📊

### HTML 中的 Mermaid

```css
.mermaid {
    display: flex;
    justify-content: center;
    margin: 20px 0;
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
}
```

### PDF 中的 Mermaid

```css
div[style*="text-align: center"] img {
    max-width: 90%;
    margin: 20px auto;
    display: block;
}
```

---

## 9 最佳实践 ✨

### 样式优先级

```css
/* 使用具体选择器提高优先级 */
body.custom-theme {
    color: #2c3e50;
}
```

### 跨平台字体

```css
body {
    font-family: 
        -apple-system,
        BlinkMacSystemFont,
        'Segoe UI',
        'Microsoft YaHei',
        'SimHei',
        Arial,
        sans-serif;
}
```

### 性能优化

```css
/* 避免复杂选择器 */
.highlight-text {
    color: red;
}
```

---

## 10 完整示例

```python
from markconv import MDConverter

converter = MDConverter(css_file="styles/custom.css")
converter.to_html("document.md", "output/document.html")
converter.to_pdf("document.md", "output/document.pdf")

print("转换完成！")
```

---

最后更新时间：2026-05-01
