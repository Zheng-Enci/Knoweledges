# Python PDF处理入门指南

## 目录
1. [PDF基础概念](#pdf基础概念)
2. [核心PDF处理库](#核心pdf处理库)
3. [库的选择建议](#库的选择建议)
4. [常见问题解决](#常见问题解决)
5. [总结](#总结)

---

## PDF基础概念

### 什么是PDF？
PDF（Portable Document Format）是一种文档格式，可以在任何设备上保持一致的显示效果。

### PDF的主要特点：
- **跨平台**：Windows、Mac、Linux都能正常显示
- **格式固定**：不会因为软件不同而改变布局
- **支持多媒体**：可以包含文字、图片、表格等

### PDF的常见类型：
- **文本PDF**：可以直接复制文字
- **扫描PDF**：图片格式，需要OCR识别文字
- **混合PDF**：既有文字又有图片

---

## 核心PDF处理库

### 1. pypdf - 简单文本提取
**适用场景：** 提取PDF中的文字内容

**安装：**
```bash
pip install pypdf
```

**基础用法：**
```python
import pypdf

# 读取PDF文件
with open('document.pdf', 'rb') as file:
    reader = pypdf.PdfReader(file)
    
    # 获取页数
    print(f"总页数: {len(reader.pages)}")
    
    # 提取所有文字
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    print(text)
```

**优点：** 简单易用，速度快
**缺点：** 对复杂布局支持有限

### 2. pdfplumber - 表格数据提取
**适用场景：** 从PDF中提取表格数据

**安装：**
```bash
pip install pdfplumber
```

**基础用法：**
```python
import pdfplumber

# 打开PDF文件
with pdfplumber.open('document.pdf') as pdf:
    # 处理第一页
    page = pdf.pages[0]
    
    # 提取文字
    text = page.extract_text()
    print("文字内容:")
    print(text)
    
    # 提取表格
    tables = page.extract_tables()
    if tables:
        print("\n表格数据:")
        for table in tables:
            for row in table:
                print(row)
```

**优点：** 表格提取效果好
**缺点：** 处理速度较慢

### 3. PyMuPDF - 高性能处理
**适用场景：** 需要快速处理大量PDF文件

**安装：**
```bash
pip install PyMuPDF
```

**基础用法：**
```python
import fitz  # PyMuPDF

# 打开PDF文件
doc = fitz.open('document.pdf')

# 遍历所有页面
for page_num in range(doc.page_count):
    page = doc[page_num]
    
    # 提取文字
    text = page.get_text()
    print(f"第{page_num + 1}页:")
    print(text)
    
    # 提取图片
    image_list = page.get_images()
    print(f"本页有 {len(image_list)} 张图片")

doc.close()
```

**优点：** 速度快，功能强大
**缺点：** 学习曲线较陡

### 4. reportlab - PDF生成
**适用场景：** 创建新的PDF文档

**安装：**
```bash
pip install reportlab
```

**基础用法：**
```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# 创建PDF文档
doc = SimpleDocTemplate("output.pdf", pagesize=A4)
styles = getSampleStyleSheet()

# 创建内容
story = []
story.append(Paragraph("我的第一个PDF文档", styles['Title']))
story.append(Paragraph("这是使用Python生成的PDF文档。", styles['Normal']))

# 生成PDF
doc.build(story)
print("PDF已生成: output.pdf")
```

**优点：** 功能强大，支持复杂布局
**缺点：** 学习成本高

---

## 库的选择建议

### 根据需求选择：

| 需求 | 推荐库 | 理由 |
|------|--------|------|
| 简单文字提取 | pypdf | 最简单，适合初学者 |
| 提取表格数据 | pdfplumber | 表格处理效果好 |
| 处理大量文件 | PyMuPDF | 速度快，性能好 |
| 创建PDF文档 | reportlab | 功能最全面 |

### 学习建议：
1. **初学者**：从pypdf开始
2. **需要表格**：学习pdfplumber
3. **性能要求高**：使用PyMuPDF
4. **要生成PDF**：学习reportlab

---

## 常见问题解决

### 1. 安装问题

**问题：** pip安装失败
**解决：**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install pypdf -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

**问题：** PyMuPDF安装失败
**解决：**
```bash
# Windows用户可能需要安装Microsoft Visual C++
# 或者使用conda安装
conda install -c conda-forge pymupdf
```

### 2. 编码问题

**问题：** 中文显示乱码
**解决：**
```python
# 保存时指定编码
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
```

### 3. 文件权限问题

**问题：** 无法读取PDF文件
**解决：**
```python
import os

# 检查文件是否存在
if os.path.exists('document.pdf'):
    print("文件存在")
else:
    print("文件不存在")

# 检查文件权限
if os.access('document.pdf', os.R_OK):
    print("文件可读")
else:
    print("文件不可读")
```

### 4. 内存不足

**问题：** 处理大文件时内存不足
**解决：**
```python
# 分页处理
def process_large_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        
        # 每次只处理一页
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"处理第{i+1}页...")
            # 处理当前页的内容
            # 不要一次性保存所有内容
```

---

## 总结

### 核心要点：
1. **pypdf**：最简单的文字提取工具
2. **pdfplumber**：最好的表格提取工具
3. **PyMuPDF**：最快的处理工具
4. **reportlab**：最强大的PDF生成工具

### 学习路径：
1. 先学会用pypdf提取文字
2. 需要表格时学习pdfplumber
3. 需要高性能时学习PyMuPDF
4. 需要生成PDF时学习reportlab

### 实用建议：
- 从简单需求开始
- 遇到问题先查文档
- 多练习，多尝试
- 不要一开始就追求复杂功能

---

**作者：** 厦门工学院人工智能创作坊 --郑恩赐  
**日期：** 2025-9-23
