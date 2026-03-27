# mdtool

一个强大的 Markdown 转换工具库。

**版本**: v0.1.0

## 背景

在日常开发中，我们经常需要将 Markdown 文档转换为其他格式（如 HTML、PDF、DOCX 等），但现有的解决方案存在诸多痛点：

- **配置繁琐**：许多库需要复杂的配置和依赖管理，学习成本高
- **中文支持差**：部分工具对中文显示支持不佳，需要额外配置字体和编码
- **样式定制困难**：自定义样式需要深入了解工具的内部机制
- **收费限制**：一些在线工具和商业软件需要付费，功能受限
- **依赖繁重**：某些库依赖过多，安装和使用都不够轻量

为了解决这些问题，我开发了 **mdtool** —— 一个简单、高效、免费的 Markdown 转换工具库。

## 简介

mdtool 是一个 Python 库，旨在提供简单易用的 Markdown 转换功能。该库支持将 Markdown 文档转换为多种格式，方便用户在不同场景下使用。

**当前版本支持**：
- Markdown → HTML

**计划支持**：
- Markdown → PDF
- Markdown → DOCX
- 更多格式...

## 项目地址

- **Gitee**: `https://gitee.com/zheng-enci050704/mdtool`
- **GitHub**: `https://github.com/Zheng-Enci/mdtool`
- **GitCode**: `https://gitcode.com/ZhengEnCi/mdtool`

## 功能特性

- 📝 **简单易用**：提供简洁的 API 接口
- 🚀 **高性能**：基于高效的转换引擎
- 🔧 **可扩展**：支持自定义转换器和插件
- 📦 **轻量级**：最小化依赖，易于集成
- 🎨 **样式灵活**：支持自定义 CSS 样式
- 🌐 **中文友好**：内置中文字体支持，UTF-8 编码

## 安装

### 从源码安装

```bash
# 选择一个源进行克隆
git clone `https://github.com/Zheng-Enci/mdtool.git`
# 或
git clone `https://gitee.com/zheng-enci050704/mdtool.git`
# 或
git clone `https://gitcode.com/ZhengEnCi/mdtool.git`

# 安装依赖
cd mdtool
pip install -r requirements.txt
```

### 使用安装脚本（推荐国内用户）

项目提供了一个安装脚本，使用清华源加速依赖下载：

```bash
cd mdtool
python installl_requirements.py
```

该脚本会自动从清华源安装 `requirements.txt` 中的所有依赖项，速度更快。

### 依赖项

- Python 3.13+

## 快速开始

查看 `examples/` 目录获取完整示例。

## 开发计划

- [x] 实现 Markdown 到 HTML 的转换
- [x] 支持自定义 CSS 样式
- [x] 支持中文显示
- [x] 自动创建输出目录
- [ ] 添加更多代码高亮主题
- [ ] 支持自定义主题模板
- [ ] 添加命令行工具
- [ ] 完善单元测试
- [ ] 发布到 PyPI

## 项目结构

```
mdtool/
├── mdtool/                          # 主包目录
│   ├── __init__.py                 # 包初始化文件 (v0.1.0)
│   ├── html_converter.py           # HTML转换器核心模块
│   ├── parsers/                    # 解析器模块
│   │   ├── __init__.py
│   │   └── markdown_parser.py      # Markdown解析器
│   └── exporters/                  # 导出器模块
│       ├── __init__.py
│       └── html_exporter.py        # HTML导出器
├── examples/                       # 示例代码
│   └── html_example/
│       ├── html_example.py         # HTML转换示例
│       ├── sample.md               # 示例Markdown文件
│       ├── custom.css              # 自定义CSS样式
│       └── examples/
│           └── sample.html         # 生成的HTML文件
├── Note/                           # 笔记目录
│   └── Update_logs/               # 更新日志
├── README.md                       # 项目说明文档
├── requirements.txt                # 依赖列表
├── installl_requirements.py        # 安装脚本
└── main.py                         # 主程序入口
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

## 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**：本项目正在积极开发中，API 可能会有变化。建议关注版本更新日志。

最后更新时间：2026-03-27