---
alwaysApply: false
description: 规范文档中引用本地图片时使用GitCode Raw URL格式，包含URL转换规律和步骤说明
---
# GitCode 图片 URL 转换规范

## 规则说明

当文档中需要引用本地图片时，不能使用本地路径引用，必须使用 GitCode Raw URL 格式。

## URL 转换规律

### 基础格式

```
https://raw.gitcode.com/{用户名}/{仓库名}/raw/master/{相对路径}
```

### 转换步骤

1. **确定基础 URL**：`https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/`

2. **提取相对路径**：从项目根目录开始的路径（去掉本地绝对路径前缀）
   - 本地路径：`f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\Transformer\01d_chapter5_activation_functions.png`
   - 相对路径：`Transformer/01d_chapter5_activation_functions.png`

### 示例

**本地路径：**
```
Transformer/01d_chapter5_activation_functions.png
```

**转换后 URL：**
```
https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Transformer/01d_chapter5_activation_functions.png
```

## Markdown 引用格式

```markdown
![图片描述](GitCode_Raw_URL)
```

**示例：**
```markdown
![三种常用激活函数对比](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Transformer/01d_chapter5_activation_functions.png)
```

## 注意事项

- 图片必须先推送到 GitCode 远程仓库，URL 才能正常访问
- 路径分隔符统一使用正斜杠 `/`（即使 Windows 系统使用反斜杠 `\`）
- URL 编码必须完整，不能遗漏任何中文字符或特殊字符
