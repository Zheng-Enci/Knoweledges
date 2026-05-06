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
https://raw.gitcode.com/{用户名}/{仓库名}/raw/master/{相对路径（URL编码）}
```

### 转换步骤

1. **确定基础 URL**：`https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/`

2. **提取相对路径**：从项目根目录开始的路径（去掉本地绝对路径前缀）
   - 本地路径：`f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\一起学Transformer\01d-前馈神经网络-代码实现_第5章激活函数可视化.png`
   - 相对路径：`一起学Transformer/01d-前馈神经网络-代码实现_第5章激活函数可视化.png`

3. **URL 编码**：将中文字符和特殊字符转换为百分号编码
   - 中文字符 → UTF-8 百分号编码（如 `一起学` → `%E4%B8%80%E8%B5%B7%E5%AD%A6`）
   - 斜杠 `/` → `%2F`
   - 其他特殊字符同理

### 示例

**本地路径：**
```
一起学Transformer/01d-前馈神经网络-代码实现_第5章激活函数可视化.png
```

**转换后 URL：**
```
https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/%E4%B8%80%E8%B5%B7%E5%AD%A6Transformer%2F01d-%E5%89%8D%E9%A6%88%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C-%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B0_%E7%AC%AC5%E7%AB%A0%E6%BF%80%E6%B4%BB%E5%87%BD%E6%95%B0%E5%8F%AF%E8%A7%86%E5%8C%96.png
```

## Markdown 引用格式

```markdown
![图片描述](GitCode_Raw_URL)
```

**示例：**
```markdown
![三种常用激活函数对比](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/%E4%B8%80%E8%B5%B7%E5%AD%A6Transformer%2F01d-%E5%89%8D%E9%A6%88%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C-%E4%BB%A3%E7%A0%81%E5%AE%9E%E7%8E%B0_%E7%AC%AC5%E7%AB%A0%E6%BF%80%E6%B4%BB%E5%87%BD%E6%95%B0%E5%8F%AF%E8%A7%86%E5%8C%96.png)
```

## 注意事项

- 图片必须先推送到 GitCode 远程仓库，URL 才能正常访问
- 路径分隔符统一使用正斜杠 `/`（即使 Windows 系统使用反斜杠 `\`）
- URL 编码必须完整，不能遗漏任何中文字符或特殊字符
