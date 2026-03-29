# M2-如何转换为PDF

通过上篇文档[M1-如何转换为HTML](https://juejin.cn/post/7621830586782892083)的学习，我们掌握了如何使用 markconv 将 Markdown 文档转换为 HTML 格式。现在让我们继续探索 markconv 的另一个强大功能——将 Markdown 转换为 PDF 格式！🚀

## 1. 概述 📚

将 Markdown 转换为 PDF 是 markconv 的另一个核心功能，PDF（Portable Document Format，便携式文档格式）是一种跨平台的文档格式，能够在各种设备上保持一致的显示效果。通过将 Markdown 转换为 PDF，我们可以方便地分享文档、打印输出，或者归档保存。📄

markconv 的 PDF 转换功能基于 wkhtmltopdf 引擎，这是一个开源的命令行工具，使用 WebKit 渲染引擎将 HTML 文档转换为 PDF 文件。它支持 HTML、CSS、JavaScript 等现代 Web 技术，能够生成高质量的 PDF 文档。这意味着我们可以在 Markdown 中使用丰富的样式和格式，转换后的 PDF 依然能够完美呈现！🎨

## 2. 环境准备 🔧

在使用 markconv 的 PDF 转换功能之前，我们需要先完成一些环境配置。别担心，配置过程很简单，只需要几分钟就能搞定！⏱️

### 2.1 安装 wkhtmltopdf 📦

wkhtmltopdf 是 markconv PDF 转换的核心引擎，我们需要先安装它。安装过程非常简单：

1. 访问 wkhtmltopdf 官方下载页面：https://wkhtmltopdf.org/downloads.html
2. 根据你的操作系统选择对应的安装包
3. 对于 Windows 用户，推荐下载 64 位版本：https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe
4. 运行安装程序，按照提示完成安装
5. 安装到默认路径：C:\Program Files\wkhtmltopdf\

安装完成后，wkhtmltopdf 会自动添加到系统环境变量中，markconv 就能够找到它了！✅

### 2.2 安装 Python 依赖 🐍

接下来，我们需要安装 markconv 的 Python 依赖包。打开命令行，执行以下命令：

```bash
pip install markconv
```

这个命令会安装 markconv 及其所有依赖，包括 pdfkit 等 PDF 转换相关的库。安装过程可能需要几分钟，耐心等待一下就好！⏳

### 2.3 验证安装 ✅

安装完成后，我们可以通过以下方式验证是否安装成功：

1. 打开命令行，输入 `wkhtmltopdf --version`，如果显示版本信息，说明 wkhtmltopdf 安装成功
2. 在 Python 中执行 `from markconv import MDConverter`，如果没有报错，说明 markconv 安装成功

如果遇到任何问题，可以检查一下环境变量配置是否正确，或者重新安装一下。💡

## 3. 基本使用方法 💡

现在我们已经完成了环境配置，可以开始使用 markconv 将 Markdown 转换为 PDF 了！使用方法和 HTML 转换非常相似，只需要几行代码就能完成。📝

### 3.1 导入 MDConverter 类 📦

首先，我们需要从 markconv 包中导入 MDConverter 类：

```python
from markconv import MDConverter
```

MDConverter 是 markconv 的核心转换器类，它负责将 Markdown 文档转换为目标格式。我们之前已经用它来转换为 HTML，现在我们用它来转换为 PDF。同一个类，不同的方法，是不是很方便？😊

### 3.2 创建转换器实例 🏗️

创建转换器实例非常简单，我们只需要调用 MDConverter 的构造函数：

```python
converter = MDConverter(css_file="custom.css")
```

这里我们同样可以指定自定义 CSS 文件，CSS 样式会应用到转换后的 PDF 中。这意味着我们可以完全控制 PDF 的外观和风格！🎨

CSS 示例文件 `custom.css`：

```css
/* custom.css */
body {
    background-color: #f5f5f5;
}
h1 {
    color: #e74c3c;
    border-bottom: 2px solid #e74c3c;
}
code {
    background-color: #2c3e50;
    color: #ecf0f1;
}
```

### 3.3 指定输入和输出文件路径 📁

接下来，我们需要指定输入的 Markdown 文件路径和输出的 PDF 文件路径：

```python
input_file = r'sample.md'
output_file = 'examples/sample.pdf'
```

这里有几个要点需要注意：

- **输入文件路径**：我们使用了原始字符串（r 前缀）来避免转义问题。这在 Windows 系统上特别有用，因为 Windows 的路径分隔符是反斜杠 `\`，而在 Python 中反斜杠是转义字符。🪟
- **输出文件路径**：如果输出目录不存在，markconv 会自动创建。这意味着我们不需要手动创建 `examples` 目录，程序会帮我们搞定！📁
- **相对路径**：这里使用的是相对路径，相对于当前工作目录。你也可以使用绝对路径。🔍

### 3.4 执行转换操作 ⚡

最后，我们调用 `to_pdf` 方法执行转换：

```python
converter.to_pdf(input_file, output_file)
```

`to_pdf` 方法接受两个参数：

- **input_file**：输入的 Markdown 文件路径 📄
- **output_file**：输出的 PDF 文件路径 📄

就这么简单！markconv 会在后台完成所有转换工作，包括将 Markdown 转换为 HTML，再使用 wkhtmltopdf 将 HTML 转换为 PDF。整个过程对我们来说是透明的，我们只需要调用一个方法就行了！🎉

## 4. 完整示例代码 📝

让我们把所有代码整合起来，看看完整的示例：

```python
# 从 markconv 包中导入 MDConverter 类
from markconv import MDConverter


def pdf_basic_example():
    """
    PDF 转换基本使用示例

    该函数演示了如何使用 MDConverter 将 Markdown 文件转换为 PDF 文件
    包括：
    - 创建转换器实例（支持自定义 CSS 样式）
    - 指定输入和输出文件路径
    - 执行转换操作
    - 使用自定义 CSS 文件美化输出
    """
    # 打印示例标题
    print("PDF 转换基本使用示例")
    # 打印分隔线
    print("=" * 50)

    # 创建 MDConverter 实例，传入自定义 CSS 文件路径
    # 参数说明：
    #   - css_file: 自定义 CSS 样式文件的路径
    #     程序会读取该文件内容并插入到生成的 HTML 的 <style> 标签中
    #     自定义样式会覆盖或补充内置的默认样式
    #   - encoding: 文件编码格式，默认为 'utf-8'
    converter = MDConverter(css_file="custom.css")

    # 定义输入的 Markdown 文件路径（使用原始字符串 r 避免转义问题）
    input_file = r'sample.md'
    # 定义输出的 PDF 文件路径（相对路径）
    output_file = 'examples/sample.pdf'

    # 调用 to_pdf 方法执行转换
    # 参数说明：
    #   - input_file: 输入的 Markdown 文件路径
    #   - output_file: 输出的 PDF 文件路径（如果目录不存在会自动创建）
    converter.to_pdf(input_file, output_file)

    print(f"PDF 文件已生成: {output_file}")


# 当脚本被直接运行时，执行示例函数
# 如果脚本被导入为模块，则不会执行
if __name__ == '__main__':
    pdf_basic_example()
```

这段代码非常清晰，每一步都有详细的注释说明。运行这段代码后，你会在 `examples` 目录下看到生成的 `sample.pdf` 文件。用 PDF 阅读器打开它，你就能看到转换后的效果了！🎉

## 5. 常见问题解答 ❓

### 5.1 转换速度慢怎么办？🐢

PDF 转换的速度取决于 Markdown 文档的复杂程度和计算机性能。如果你的文档包含大量图片、表格或复杂的样式，转换时间可能会长一些。这是正常现象，耐心等待就好！⏳

如果转换速度实在太慢，可以尝试以下方法：

- 简化 CSS 样式，减少复杂的布局和动画效果 🎨
- 压缩图片大小，减少文档体积 🖼️
- 使用性能更好的计算机 🖥️

### 5.2 中文显示乱码怎么办？🇨🇳

markconv 默认使用 UTF-8 编码，这已经能够很好地支持中文了。如果你的 PDF 中出现中文乱码，可能是以下原因：

- CSS 样式没有指定中文字体，可以尝试在 CSS 中添加字体设置 📝
- wkhtmltopdf 版本问题，确保安装的是最新版本 📦
- Markdown 文件编码问题，确保文件使用 UTF-8 编码保存 💾

### 5.3 如何设置 PDF 的页面大小和边距？📏

markconv 支持通过 CSS 来设置 PDF 的页面大小和边距。你可以在自定义 CSS 文件中添加以下样式：

```css
@page {
    size: A4;
    margin: 2cm;
}
```

这样就可以设置 PDF 的页面大小为 A4，边距为 2 厘米。你也可以根据需要调整这些参数！📐

## 6. 总结 📝

通过这篇文档的学习，我们掌握了如何使用 markconv 将 Markdown 文档转换为 PDF 格式。主要内容包括：

- 安装和配置 wkhtmltopdf 引擎 🔧
- 安装 markconv 及其依赖 📦
- 创建转换器实例并指定 CSS 样式文件 🏗️
- 指定输入和输出文件路径 📁
- 执行转换操作 ⚡
- 自定义 CSS 样式美化输出 🎨

markconv 的 PDF 转换功能基于 wkhtmltopdf 引擎，能够生成高质量的 PDF 文档。我们不需要复杂的配置，不需要学习繁琐的 API，只需要几行代码就能完成转换。这正是我们在[M0-markconv背景及链接目录](https://github.com/Zheng-Enci/Knoweledges/blob/main/mdtool/M0-markconv%E8%83%8C%E6%99%AF%E5%8F%8A%E9%93%BE%E6%8E%A5%E7%9B%AE%E5%BD%95.md)中提到的"简单易用"的体现！💪

接下来我们将学习更多关于 markconv 的功能，比如如何转换为 DOCX 等格式。敬请期待！🚀

---

最后更新时间：2026-03-29
