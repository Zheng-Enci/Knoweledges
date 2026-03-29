# M1-如何转换为HTML

通过上篇文档的学习，我们了解了 markconv 这个简单、高效、免费的 Markdown 转换工具库，以及为什么我们需要这样的工具。现在让我们深入探讨如何使用 markconv 将 Markdown 文档转换为 HTML 格式吧！🚀

## 1. 概述 📚

将 Markdown 转换为 HTML 是 markconv 最核心的功能之一，也是 markconv 开发的第一个功能。HTML（HyperText Markup Language，超文本标记语言）是网页的标准格式，通过将 Markdown 转换为 HTML，我们可以轻松地在浏览器中查看文档内容，或者将文档发布到网站上。🌐

markconv 提供了一个简单易用的 API，让我们只需要几行代码就能完成转换。更重要的是，它支持自定义 CSS 样式，这意味着我们可以完全控制 HTML 文档的外观和风格！🎨

## 2. 安装 markconv 📦

在使用 markconv 之前，我们需要先安装它。安装非常简单，只需要一行命令：

```bash
pip install markconv
```

安装完成后，你就可以在代码中直接使用 `markconv` 了！🎉

## 3. 基本使用方法 💡

本文只探讨如何将 Markdown 转换为 HTML 格式，其他格式（如 PDF、DOCX）的转换方法将在后续文档中介绍。📝

### 3.1 导入 MDConverter 类 📦

首先，我们需要从 markconv 包中导入 MDConverter 类：

```python
from markconv import MDConverter
```

MDConverter 是 markconv 的核心转换器类，它负责将 Markdown 文档转换为目标格式。目前支持转换为 HTML，未来还会支持 PDF、DOCX 等格式。🔄

### 3.2 创建转换器实例 🏗️

创建转换器实例非常简单，我们只需要调用 MDConverter 的构造函数：

```python
converter = MDConverter(css_file="custom.css")
```

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

`css_file` 参数指定了自定义 CSS 样式文件的路径，程序会读取该文件内容并插入到生成的 HTML 的 `<style>` 标签中。如果不提供 `css_file` 参数，markconv 会使用内置的默认样式。💡

### 3.3 指定输入和输出文件路径 📁

接下来，我们需要指定输入的 Markdown 文件路径和输出的 HTML 文件路径：

```python
input_file = r'sample.md'
output_file = 'examples/sample.html'
```

这里有几个要点需要注意：

- **输入文件路径**：我们使用了原始字符串（r 前缀）来避免转义问题。这在 Windows 系统上特别有用，因为 Windows 的路径分隔符是反斜杠 `\`，而在 Python 中反斜杠是转义字符。🪟
- **输出文件路径**：如果输出目录不存在，markconv 会自动创建。这意味着我们不需要手动创建 `examples` 目录，程序会帮我们搞定！📁
- **相对路径**：这里使用的是相对路径，相对于当前工作目录。你也可以使用绝对路径。🔍

### 3.4 执行转换操作 ⚡

最后，我们调用 `to_html` 方法执行转换：

```python
converter.to_html(input_file, output_file, wrap_html=True)
```

`to_html` 方法接受三个参数：

- **input_file**：输入的 Markdown 文件路径 📄
- **output_file**：输出的 HTML 文件路径 🌐
- **wrap_html**：是否生成完整的 HTML 文档 📦

`wrap_html` 参数很重要！当设置为 `True` 时，markconv 会生成完整的 HTML 文档，包括 `<!DOCTYPE>`、`<html>`、`<head>`、`<body>` 等标签。这样的 HTML 文件可以直接在浏览器中打开，或者发布到网站上。🌐

如果设置为 `False`，则只输出 HTML body 内容，适合嵌入到其他网页中。比如你可能有一个现有的网页模板，只需要将 Markdown 转换的内容嵌入到某个 `div` 中，这时就可以使用 `wrap_html=False`。🔗

## 4. 完整示例代码 📝

让我们把所有代码整合起来，看看完整的示例：

```python
# 从 markconv 包中导入 MDConverter 类
from markconv import MDConverter


def html_basic_example():
    """
    HTML 转换基本使用示例

    该函数演示了如何使用 MDConverter 将 Markdown 文件转换为 HTML 文件
    包括：
    - 创建转换器实例（支持自定义 CSS 样式）
    - 指定输入和输出文件路径
    - 执行转换操作
    - 使用自定义 CSS 文件美化输出
    """
    # 打印示例标题
    print("HTML 转换基本使用示例")
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
    # 定义输出的 HTML 文件路径（相对路径）
    output_file = 'examples/sample.html'


    # 调用 to_html 方法执行转换
    # 参数说明：
    #   - input_file: 输入的 Markdown 文件路径
    #   - output_file: 输出的 HTML 文件路径（如果目录不存在会自动创建）
    #   - wrap_html=True: 生成完整的 HTML 文档（包含 DOCTYPE、html、head、body 等标签）
    #     如果设置为 False，则只输出 HTML body 内容，适合嵌入到其他网页中
    converter.to_html(input_file, output_file, wrap_html=True)


# 当脚本被直接运行时，执行示例函数
# 如果脚本被导入为模块，则不会执行
if __name__ == '__main__':
    html_basic_example()
```

这段代码非常清晰，每一步都有详细的注释说明。运行这段代码后，你会在 `examples` 目录下看到生成的 `sample.html` 文件。用浏览器打开它，你就能看到转换后的效果了！🎉

## 5. 总结 📝

通过这篇文档的学习，我们掌握了如何使用 markconv 将 Markdown 文档转换为 HTML 格式。主要内容包括：

- 导入 MDConverter 类 📦
- 创建转换器实例并指定 CSS 样式文件 🏗️
- 指定输入和输出文件路径 📁
- 执行转换操作 ⚡
- 自定义 CSS 样式美化输出 🎨

markconv 的设计理念就是简单、高效、免费。我们不需要复杂的配置，不需要学习繁琐的 API，只需要几行代码就能完成转换。这正是我们在 [M0-markconv背景及链接目录](https://github.com/Zheng-Enci/Knoweledges/blob/main/mdtool/M0-markconv%E8%83%8C%E6%99%AF%E5%8F%8A%E9%93%BE%E6%8E%A5%E7%9B%AE%E5%BD%95.md) 中提到的"简单易用"的体现！💪

接下来我们将学习更多关于 markconv 的功能，比如如何转换为 PDF、DOCX 等格式。敬请期待！🚀

---

最后更新时间：2026-03-27