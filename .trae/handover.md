# 项目交接文档

> 创建时间：2026-07-27（第二次更新）
> 创建人：小恩
> 目标读者：接手本项目的新对话

---

## 项目背景

用户在做一个**试卷"未作答空白答题区"自动定位**任务：
- **模型**：Qwen3-VL-Plus（多模态大模型，grounding 任务）
- **输入**：作业/试卷图片（样例：小学二年级数学"解决问题"单元，3072×4096）
- **目标**：识别图片中**所有"未作答"的空白答题区**（填空题 "=" 后空白、客观题括号内空白、答题框内空白作答区），输出 bbox 坐标
- **预期输出**：`{"empty_positions": [{"bbox_2d": [x1, y1, x2, y2]}]}`，只圈空白区域，不圈题目文字/符号/题号
- **预期正确结果**：6 个填空题空白 + 3 个答题框内空白 = **9 个 bbox**

---

## 在做什么

**当前焦点**：调 Qwen3-VL-Plus 的 prompt，稳定输出 9 个**位置精准 + 尺寸正常**的 bbox（不漏圈、不乱圈、不框题目文字、不出现异常窄框）。

**当前进展**：已基本解决异常窄框和框住题目文字的问题，最近一轮测试结果：
- 6 个填空题 bbox：width 48-49，紧贴横线上方空白，不含题目文字
- 3 个计算题答题框 bbox：y1 从框内空白起始位置开始（相比上轮下移 ~21px），成功排除顶部题目文字行

---

## 已完成

### 1. 异常窄框问题已解决
- **根因**：prompt 的 `width ≤ 1/3` 约束没有下限，VLM 把 "=" 后空白识别为"单像素列"
- **处理**：用户要求**删除所有 width 约束**（而非加下限），删除了 prompt 中两处 width 上下限（关键约束 + bbox 范围）
- **结果**：填空题 bbox width 从 2px 恢复到 46-49px，正常

### 2. Prompt 文件清理
- 用户要求 `prompt_empty_positions.md` **只保留 prompt 本身**，删除所有 metadata、标题、说明、注意事项
- 当前文件结构：System Message（上半段）+ separator + User Message（末尾一句）的纯 prompt 内容

### 3. Prompt 持续迭代
| 轮次 | 改动 | 效果 |
|---|---|---|
| 上一会话 v1-v4 | 前 4 轮迭代 | 均不稳定，有漏圈/窄框/过度包含问题 |
| 本轮第 1 轮 | 删除全部 width 约束 | 窄框消失，但 bbox 包含题目文字 |
| 本轮第 2 轮 | 新增「bbox 紧贴空白作答区域」+ 填空题改为「上方的空白作答区」 | bbox 大幅收窄（83-154→46-49），不再框题目 |
| 本轮第 3 轮 | 新增「计算题（答题框型）：下半部分空白作答区」+「y1 从框内空白起始位置开始」 | 答题框 y1 下移 ~21px，排除顶部题目文字 |

### 4. 画图脚本
- `draw_bbox_strict.py` — 已更新为最新的 9 个 bbox 坐标，直接覆盖 `result_bbox_strict.png`

---

## 卡在哪

**当前核心瓶颈**：Qwen3-VL-Plus 行为仍有**随机性**：
- 同 prompt 不同次调用结果有差异（已观察到填空题 bbox 宽度在 46-83 之间波动）
- 本次会话只在同一张测试图上验证，没有在其他类型的试卷图片（不同 layout、不同题型）上测试泛化能力
- 尚未在 production 环境中集成测试

**剩余问题**：
- 答题框类型判别：VLM 仍将 3 个计算题答题框标注为"主观题答题框"（label 不准确，但 bbox 位置正确）
- prompt 目前依赖 few-shot 示例中"底部 4 个填空题"的描述，对底部密集题目的覆盖还有待验证

---

## 下一步计划

按优先级：

1. **【高】测试泛化能力** — 在当前 prompt 下，换 2-3 张不同题型/不同 layout 的试卷图片测试，验证 prompt 的通用性
2. **【中】优化 label 准确性** — VLM 输出中的 `label` 字段（如"主观题答题框"）与实际题型不匹配，如果 label 用于下游流程需要修正
3. **【低】评估是否换 pipeline** — 如果 VLM 方案在多图测试中仍不稳定，可考虑 OCR（PP-OCR/PaddleOCR）+ Grounding DINO 的 hybrid pipeline
4. **【低】加 temperature=0** — 减少 VLM 输出的随机性，提高 consistency

---

## 踩过的坑

### 1. Width 约束导致异常窄框
- **问题**：prompt 中 `width ≤ 1/3` 的约束没有下限，VLM 产出 width=2px 的框
- **教训**：VLM 对上界约束理解准确，但没有下限约束时会产生极端值
- **当前方案**：用户决定**完全删除 width 约束**，让 VLM 自由判断空白区域大小

### 2. 反漏检 vs 反乱圈的平衡
- 反漏检（宁多圈）→ 易出噪声框
- 反乱圈（宁少圈）→ 易漏真实空白
- 当前选择：不设硬性 width 约束，通过"紧贴空白作答区域"来间接控制

### 3. Prompt 文件只需保留 prompt 本身
- 用户要求 prompt 文件只有纯 prompt 内容，不要加标题、说明、注意事项等元信息
- 新接手者注意：`prompt_empty_positions.md` 的内容就是直接发给 VLM 的 System Message + User Message

### 4. 答题框型题目需区分为上下两部分
- 答题框内上方通常是题目文字，下方是空白作答区
- bbox 的 y1 应从空白起始位置开始，不能从框的顶部开始
- prompt 需显式说明「排除上半部分的题目文字」

### 5. VLM 行为有随机性
- 同样 prompt 不同次跑结果有差异
- 调 prompt 单次结果不能定论，至少跑 3-5 次取共识

---

## 关键文件索引

| 文件路径 | 用途 |
|---|---|
| `c:\Users\zheng\OneDrive\Desktop\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\prompt_empty_positions.md` | **当前 VLM prompt**（纯 prompt 内容，无 metadata） |
| `c:\Users\zheng\OneDrive\Desktop\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\draw_bbox_strict.py` | 画 bbox 标注图脚本，含最新 9 个 bbox 坐标 |
| `c:\Users\zheng\OneDrive\Desktop\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\result_bbox_strict.png` | 最新标注图（9 框，填空题 46-49px，答题框 y1 下移） |
| `c:\Users\zheng\OneDrive\Desktop\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Weixin Image_20260727100849_223_55.png` | 原始测试图（小学数学试卷） |

---

## Git 历史（最近 commit）

```
8f1096a docs: strengthen empty-positions prompt with full-scan enforcement  (上一会话)
9ebe676 docs: strengthen empty-positions prompt (strict + few-shot)        (上一会话)
ba730b9 chore: sync project state                                          (上一会话)
```

> **注意**：本轮 prompt 修改（删除 width 约束 + 紧贴空白 + 答题框型定义）**尚未 commit**，接手后请先 `git status` 确认变更状态，并按规范 commit。

---

## 续接建议

接手新对话时：
1. 先读 `prompt_empty_positions.md` 了解当前 prompt 状态（纯 prompt，无 metadata）
2. 看 `result_bbox_strict.png` 了解最新标注效果
3. 建议先用 2-3 张不同试卷测泛化能力
4. 任何 bbox 改动都必须 `git add` + `git commit`（commit message 用英文，不允许 `git push`）
