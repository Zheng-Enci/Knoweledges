# 阿里云百炼 Token Plan Standard 套餐

> 记录账号 `aliyun0575409114` 的百炼 Token Plan 订阅信息与可用模型清单，便于后续接入与参考。

## 套餐概览

| 项目 | 内容 |
|------|------|
| 套餐名称 | Standard 套餐 |
| 套餐状态 | 生效中 |
| 剩余天数 | 31 天 |
| 开始时间 | 2026-08-21 11:28:40 |
| 结束时间 | 2026-09-22 00:00:00 |
| 自动续费 | 未开启 |
| 业务空间 | 华北2（北京）· 默认业务空间 |
| 最后统计时间 | 2026-08-21 14:10:35 |

### 用量统计

- **7 天限额**：将于 2026-08-28 11:40:00 (UTC+8) 重置刷新
- **已用额度**：20.7%（0% / 50% / 90% / 100% 刻度）
- **额度补充**：暂无可用额外用量包，请先前去加购

## 接入配置

### 套餐专属 API Key

```
sk-sp-H.DIIHLE.****jBEZdUnZPjHuOIg
```

> 请妥善保存密钥信息，不要与他人共享或暴露在客户端代码中。为保护账户安全，可能会自动禁用任何公开泄漏的 API Key，也可随时重置生成新密钥。

### 套餐专属 Base URL

- **兼容 OpenAI 接口协议工具**：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **兼容 Anthropic 接口协议工具**：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

### 快速接入 AI 工具（Token Plan CLI）

1. **For Agent 安装**：请阅读 `https://bailian.aliyun.com/cli/install.md` 并按照说明安装阿里云百炼 CLI
2. **配置 Token Plan**：点击控制台下方「复制」或「重置」按钮获取套餐专属 API Key 进行配置
3. **开始使用**：示例——帮我生成一套电商多视角的营销主图，6 张夏日男装 T 恤图

## 可使用模型

当前订阅套餐只支持使用以下模型列表：

### 千问（Qwen）

| 模型 | 模型能力 | 备注 |
|------|----------|------|
| qwen3.8-max | 文本生成、推理模型、视觉理解 | 限时夜间5折 |
| qwen3.7-plus | 文本生成、推理模型、视觉理解 | |
| qwen3.7-max | 文本生成、推理模型 | |
| qwen3.6-flash | 文本生成、推理模型、视觉理解 | |
| qwen-image-3.0-pro | 图片生成 | |
| qwen-audio-3.0-asr-flash | 语音识别 | |
| qwen-audio-3.0-tts-plus | 实时语音合成、语音合成 | |
| qwen-audio-3.0-realtime-plus | 实时语音对话 | |

### 万相（Wan）

| 模型 | 模型能力 |
|------|----------|
| wan2.7-image | 图片生成 |
| wan2.7-image-pro | 图片生成 |

### HappyHorse

| 模型 | 模型能力 |
|------|----------|
| happyhorse-1.1-i2v | 视频生成 |
| happyhorse-1.1-t2v | 视频生成 |
| happyhorse-1.1-r2v | 视频生成 |

### DeepSeek

| 模型 | 模型能力 | 备注 |
|------|----------|------|
| deepseek-v4-pro-0813 | 文本生成、推理模型 | 限时夜间5折 |
| deepseek-v4-pro | 文本生成、推理模型 | |
| deepseek-v4-flash-0731 | 文本生成、推理模型 | |

### 智谱 AI（GLM）

| 模型 | 模型能力 |
|------|----------|
| glm-5.2 | 文本生成、推理模型 |
