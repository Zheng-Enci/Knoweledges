#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将P3B Markdown文档转换为HTML
"""

import re
from pathlib import Path

def escape_html(text):
    """转义HTML特殊字符"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def markdown_to_html(markdown_content):
    """将Markdown内容转换为HTML"""
    lines = markdown_content.split('\n')
    html_lines = []
    in_code_block = False
    code_language = ''
    in_table = False
    table_header = False
    in_list = False
    list_type = None  # 'ul' or 'ol'
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_stripped = line.strip()
        
        # 代码块处理 - 使用strip()来检测，支持缩进的代码块
        if line_stripped.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
                code_language = ''
            else:
                code_language = line_stripped[3:].strip()
                lang_class = f'language-{code_language}' if code_language else ''
                html_lines.append(f'<pre><code class="{lang_class}">')
                in_code_block = True
            i += 1
            continue
        
        if in_code_block:
            html_lines.append(escape_html(line))
            i += 1
            continue
        
        # 标题处理
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('# ').strip()
            # 生成ID（用于锚点）
            anchor_id = re.sub(r'[^\w\s-]', '', text.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            html_lines.append(f'<h{level} id="{anchor_id}">{text}</h{level}>')
            i += 1
            continue
        
        # 表格处理
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                table_header = True
            
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            tag = 'th' if table_header else 'td'
            html_lines.append('<tr>')
            for cell in cells:
                # 处理粗体
                cell = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cell)
                html_lines.append(f'<{tag}>{cell}</{tag}>')
            html_lines.append('</tr>')
            
            # 检查下一行是否是分隔符
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if '|' in next_line and '---' in next_line:
                    table_header = False
                    i += 1  # 跳过分隔符行
            else:
                table_header = False
            i += 1
            continue
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
                table_header = False
        
        # 引用块
        if line.startswith('>'):
            text = line[1:].strip()
            # 处理内联格式
            text = process_inline_formatting(text)
            html_lines.append(f'<blockquote>{text}</blockquote>')
            i += 1
            continue
        
        # 列表处理 - 改进以支持列表项内的代码块
        # 无序列表
        if line_stripped.startswith('- ') or line_stripped.startswith('* '):
            # 如果之前是其他类型的列表，先关闭
            if in_list and list_type != 'ul':
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
                list_type = 'ul'
            
            # 处理列表项内容
            text = line_stripped[2:].strip()
            text = process_inline_formatting(text)
            html_lines.append(f'<li>{text}')
            
            # 检查列表项是否包含多行内容（包括代码块）
            # 如果下一行不是新列表项，也不是空行，且不是新标题/表格等，则继续处理
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                
                # 如果是代码块开始
                if next_stripped.startswith('```'):
                    # 处理代码块
                    code_lang = next_stripped[3:].strip()
                    lang_class = f'language-{code_lang}' if code_lang else ''
                    html_lines.append(f'<pre><code class="{lang_class}">')
                    i += 1
                    # 继续读取直到代码块结束
                    while i < len(lines):
                        code_line = lines[i]
                        if code_line.strip().startswith('```'):
                            html_lines.append('</code></pre>')
                            i += 1
                            break
                        html_lines.append(escape_html(code_line))
                        i += 1
                    continue
                
                # 如果是新列表项（同类型或不同类型）
                if (next_stripped.startswith('- ') or next_stripped.startswith('* ') or 
                    re.match(r'^\d+\.\s', next_stripped)):
                    break
                
                # 如果是空行，可能是列表项结束，也可能是列表项内的空行
                if not next_stripped:
                    # 检查再下一行是否还是列表项内容
                    if i + 1 < len(lines):
                        next_next = lines[i + 1].strip()
                        # 如果下一行是代码块或继续是列表项内容，则保留空行
                        if (next_next.startswith('```') or 
                            next_next.startswith('- ') or next_next.startswith('* ') or
                            re.match(r'^\d+\.\s', next_next) or
                            next_next.startswith('#') or
                            (next_next.startswith('|') and '|' in next_next)):
                            break
                    html_lines.append('<br>')
                    i += 1
                    continue
                
                # 如果是新标题、表格等，列表项结束
                if (next_stripped.startswith('#') or 
                    (next_stripped.startswith('|') and '|' in next_stripped) or
                    next_stripped.startswith('>')):
                    break
                
                # 否则是列表项内容的延续（可能是缩进的文本或代码）
                # 检查是否是缩进的内容（列表项内的段落）
                if next_line and not next_stripped.startswith(('- ', '* ')) and not re.match(r'^\d+\.\s', next_stripped):
                    # 处理为列表项内的段落
                    content = process_inline_formatting(next_line.lstrip())
                    if content.strip():
                        html_lines.append(f'<br>{content}')
                    i += 1
                else:
                    break
            
            html_lines.append('</li>')
            
            # 检查列表是否结束
            if i >= len(lines) or not (lines[i].strip().startswith(('- ', '* '))):
                html_lines.append('</ul>')
                in_list = False
                list_type = None
            continue
        
        # 有序列表
        if re.match(r'^\d+\.\s', line_stripped):
            # 如果之前是其他类型的列表，先关闭
            if in_list and list_type != 'ol':
                html_lines.append(f'</{list_type}>')
                in_list = False
                list_type = None
            
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
                list_type = 'ol'
            
            # 处理列表项内容
            text = re.sub(r'^\d+\.\s', '', line_stripped)
            text = process_inline_formatting(text)
            html_lines.append(f'<li>{text}')
            
            # 检查列表项是否包含多行内容（包括代码块）
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.strip()
                
                # 如果是代码块开始
                if next_stripped.startswith('```'):
                    # 处理代码块
                    code_lang = next_stripped[3:].strip()
                    lang_class = f'language-{code_lang}' if code_lang else ''
                    html_lines.append(f'<pre><code class="{lang_class}">')
                    i += 1
                    # 继续读取直到代码块结束
                    while i < len(lines):
                        code_line = lines[i]
                        if code_line.strip().startswith('```'):
                            html_lines.append('</code></pre>')
                            i += 1
                            break
                        html_lines.append(escape_html(code_line))
                        i += 1
                    continue
                
                # 如果是新列表项（同类型或不同类型）
                if (next_stripped.startswith('- ') or next_stripped.startswith('* ') or 
                    re.match(r'^\d+\.\s', next_stripped)):
                    break
                
                # 如果是空行
                if not next_stripped:
                    # 检查再下一行是否还是列表项内容
                    if i + 1 < len(lines):
                        next_next = lines[i + 1].strip()
                        if (next_next.startswith('```') or 
                            next_next.startswith('- ') or next_next.startswith('* ') or
                            re.match(r'^\d+\.\s', next_next) or
                            next_next.startswith('#') or
                            (next_next.startswith('|') and '|' in next_next)):
                            break
                    html_lines.append('<br>')
                    i += 1
                    continue
                
                # 如果是新标题、表格等，列表项结束
                if (next_stripped.startswith('#') or 
                    (next_stripped.startswith('|') and '|' in next_stripped) or
                    next_stripped.startswith('>')):
                    break
                
                # 否则是列表项内容的延续
                if next_line and not next_stripped.startswith(('- ', '* ')) and not re.match(r'^\d+\.\s', next_stripped):
                    content = process_inline_formatting(next_line.lstrip())
                    if content.strip():
                        html_lines.append(f'<br>{content}')
                    i += 1
                else:
                    break
            
            html_lines.append('</li>')
            
            # 检查列表是否结束
            if i >= len(lines) or not re.match(r'^\d+\.\s', lines[i].strip()):
                html_lines.append('</ol>')
                in_list = False
                list_type = None
            continue
        
        # 空行
        if not line.strip():
            html_lines.append('<p></p>')
            i += 1
            continue
        
        # HTML标签处理（如<p align="right">）
        if line.strip().startswith('<') and line.strip().endswith('>'):
            html_lines.append(line)
            i += 1
            continue
        
        # 普通段落
        text = process_inline_formatting(line)
        html_lines.append(f'<p>{text}</p>')
        i += 1
    
    # 关闭未关闭的标签
    if in_code_block:
        html_lines.append('</code></pre>')
    if in_table:
        html_lines.append('</table>')
    if in_list and list_type:
        html_lines.append(f'</{list_type}>')
    
    return '\n'.join(html_lines)

def process_inline_formatting(text):
    """处理内联格式（粗体、斜体、代码、链接）"""
    # 如果包含完整的HTML标签，先提取并保留
    html_tags = []
    tag_pattern = r'<[^>]+>'
    
    def replace_tag(match):
        tag = match.group(0)
        placeholder = f'__HTML_TAG_{len(html_tags)}__'
        html_tags.append(tag)
        return placeholder
    
    # 临时替换HTML标签
    text_with_placeholders = re.sub(tag_pattern, replace_tag, text)
    
    # 链接处理 [text](url)
    text_with_placeholders = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text_with_placeholders)
    
    # 粗体 **text**
    text_with_placeholders = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', text_with_placeholders)
    
    # 斜体 *text* (不在代码块中)
    text_with_placeholders = re.sub(r'(?<!\*)\*([^\*]+)\*(?!\*)', r'<em>\1</em>', text_with_placeholders)
    
    # 内联代码 `code`
    text_with_placeholders = re.sub(r'`([^`]+)`', r'<code>\1</code>', text_with_placeholders)
    
    # 恢复HTML标签
    for i, tag in enumerate(html_tags):
        text_with_placeholders = text_with_placeholders.replace(f'__HTML_TAG_{i}__', tag)
    
    return text_with_placeholders

def extract_toc(markdown_content):
    """提取目录"""
    toc_items = []
    lines = markdown_content.split('\n')
    
    for line in lines:
        if line.startswith('##'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('# ').strip()
            anchor_id = re.sub(r'[^\w\s-]', '', text.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            toc_items.append((level, text, anchor_id))
    
    return toc_items

def generate_html(markdown_file_path):
    """生成HTML文件"""
    # 读取Markdown文件
    with open(markdown_file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 提取标题和目录
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "P3B文档"
    toc_items = extract_toc(markdown_content)
    
    # 转换Markdown为HTML
    content_html = markdown_to_html(markdown_content)
    
    # 生成目录HTML
    toc_html = '<nav class="toc"><h2>目录</h2><ul>'
    for level, text, anchor_id in toc_items:
        indent = (level - 2) * 20  # H2开始，每级缩进20px
        toc_html += f'<li style="padding-left: {indent}px;"><a href="#{anchor_id}">{text}</a></li>'
    toc_html += '</ul></nav>'
    
    # 生成完整HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.8;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            padding: 20px;
            gap: 30px;
        }}
        
        .toc {{
            flex: 0 0 250px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: sticky;
            top: 20px;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
        }}
        
        .toc h2 {{
            font-size: 18px;
            margin-bottom: 15px;
            color: #1e88e5;
            border-bottom: 2px solid #1e88e5;
            padding-bottom: 10px;
        }}
        
        .toc ul {{
            list-style: none;
        }}
        
        .toc li {{
            margin: 8px 0;
        }}
        
        .toc a {{
            color: #555;
            text-decoration: none;
            display: block;
            padding: 5px 10px;
            border-radius: 4px;
            transition: all 0.3s;
        }}
        
        .toc a:hover {{
            background-color: #e3f2fd;
            color: #1e88e5;
        }}
        
        .content {{
            flex: 1;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .content h1 {{
            font-size: 32px;
            color: #1e88e5;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #1e88e5;
        }}
        
        .content h2 {{
            font-size: 26px;
            color: #1e88e5;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }}
        
        .content h3 {{
            font-size: 22px;
            color: #424242;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        .content h4 {{
            font-size: 18px;
            color: #616161;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        
        .content p:empty {{
            margin-bottom: 10px;
        }}
        
        .content ul, .content ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        .content li {{
            margin: 8px 0;
        }}
        
        .content blockquote {{
            border-left: 4px solid #1e88e5;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
            background-color: #f5f5f5;
            padding: 15px 20px;
            border-radius: 4px;
        }}
        
        .content code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Consolas", "Monaco", "Courier New", monospace;
            font-size: 0.9em;
            color: #e53935;
        }}
        
        .content pre {{
            background-color: #2d2d2d;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}
        
        .content pre code {{
            background-color: transparent;
            padding: 0;
            color: #f8f8f2;
            font-size: 14px;
            line-height: 1.6;
        }}
        
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .content table th {{
            background-color: #1e88e5;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .content table td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .content table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .content table tr:hover {{
            background-color: #f0f0f0;
        }}
        
        .content a {{
            color: #1e88e5;
            text-decoration: none;
        }}
        
        .content a:hover {{
            text-decoration: underline;
        }}
        
        .content strong {{
            color: #1e88e5;
            font-weight: 600;
        }}
        
        /* 响应式设计 */
        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
                padding: 10px;
            }}
            
            .toc {{
                position: relative;
                max-height: none;
                margin-bottom: 20px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .content h1 {{
                font-size: 24px;
            }}
            
            .content h2 {{
                font-size: 20px;
            }}
        }}
        
        /* 平滑滚动 */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* 目录高亮 */
        .toc a.active {{
            background-color: #1e88e5;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        {toc_html}
        <article class="content">
            {content_html}
        </article>
    </div>
    
    <script>
        // 目录高亮当前章节
        window.addEventListener('scroll', function() {{
            const headings = document.querySelectorAll('.content h2, .content h3');
            const tocLinks = document.querySelectorAll('.toc a');
            
            let current = '';
            headings.forEach(heading => {{
                const rect = heading.getBoundingClientRect();
                if (rect.top <= 100) {{
                    current = heading.id;
                }}
            }});
            
            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {{
                    link.classList.add('active');
                }}
            }});
        }});
    </script>
</body>
</html>'''
    
    # 保存HTML文件
    output_path = markdown_file_path.with_suffix('.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML文件已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    markdown_file = Path('P3B-90%初学者参数传错位置？合格程序员都这样选择参数类型.md')
    if markdown_file.exists():
        generate_html(markdown_file)
    else:
        print(f"错误: 找不到文件 {markdown_file}")

