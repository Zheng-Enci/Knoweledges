# Vite 禁用 CSS 代码分割：解决生产环境样式加载顺序混乱问题 🔧

本文档讲解 Vite 构建工具中 CSS 代码分割（CSS Code Splitting）的运行机制，分析其导致生产环境样式加载顺序混乱、ElementPlus 默认样式覆盖自定义样式的根本原因，并通过在 `vite.config.mjs` 中设置 `cssCodeSplit: false` 彻底解决下拉框不显示时间段的实际问题 🔧
This document explains the CSS Code Splitting mechanism in Vite build tool, analyzes how it causes style loading order chaos in production and ElementPlus default styles overriding custom styles, and thoroughly resolves the dropdown time-period display issue by setting `cssCodeSplit: false` in `vite.config.mjs` 🔧

---

## 术语表 / Terminology

| 术语 / Term | 说明 / Description |
|-------------|-------------------|
| **CSS Code Splitting** | 将 CSS 按照 JS Chunk 拆分到多个独立文件，实现按需加载 |
| **cssCodeSplit** | Vite 的 `build.cssCodeSplit` 配置项，控制是否启用 CSS 代码分割 |
| **CSS Chunk** | 构建后生成的独立 CSS 文件，与 JS Chunk 一一对应 |
| **CSS Cascade** | 浏览器按照样式表加载顺序和选择器优先级决定最终样式的机制 |
| **Specificity** | CSS 选择器的优先级权重，决定冲突时哪个样式生效 |
| **ElementPlus** | 基于 Vue 3 的 UI 组件库，提供 Dropdown、Select 等组件 |
| **Vite** | 基于 ESM 的前端构建工具，默认启用 CSS 代码分割 |
| **Lazy Import** | 动态导入组件的方式，会触发 CSS Chunk 的异步加载 |

---

## 章节阅读路线图 / Chapter Reading Roadmap

1. **Vite CSS 代码分割机制** / CSS Code Splitting Mechanism → 理解 Vite 默认如何拆分 CSS
2. **CSS 加载顺序混乱问题** / CSS Loading Order Chaos → 分析生产环境样式失效的根因
3. **解决方案：禁用 CSS 代码分割** / Solution: Disable CSS Code Splitting → 配置 `cssCodeSplit: false`
4. **实际案例：ElementPlus 下拉框修复** / Real Case: ElementPlus Dropdown Fix → 完整修复流程复盘
5. **总结** / Summary → 核心要点回顾

---

## 1. Vite CSS 代码分割机制 / CSS Code Splitting Mechanism

> **Note:** 本章讲解 Vite 默认的 CSS 代码分割工作原理 / This chapter explains how Vite's default CSS code splitting works.

### 1.1 什么是 CSS 代码分割 / What is CSS Code Splitting

CSS 代码分割（CSS Code Splitting）是 Vite 在生产构建时默认启用的一项优化技术。它的核心思想是：**将每个异步 JS Chunk 中引用的 CSS 提取出来，生成独立的 CSS 文件，随对应的 JS Chunk 一起按需加载**。

Vite 官方文档对此的描述是：

> Vite automatically extracts the CSS used by modules in an async chunk and generates a separate file for it. The CSS file is automatically loaded via a `<link>` tag when the associated async chunk is loaded.

也就是说，当某个异步组件被懒加载（Lazy Import）时，Vite 会自动插入一个 `<link>` 标签来加载该组件对应的 CSS 文件。

**直观类比** ：想象一个外卖配送系统

- **不分割（单文件）** ：所有菜品打包在一个大箱子里，一次全部送到 → 加载快但首屏负担重
- **代码分割（多文件）** ：每道菜单独打包，点哪道送哪道 → 按需配送，首屏轻量

### 1.2 Vite 构建时的 CSS 拆分流程 / Build-Time CSS Splitting Process

Vite 基于 Rollup 进行生产构建，CSS 拆分的大致流程如下：

```
源码中的 CSS/SCSS/Less 文件
       ↓
Rollup 构建阶段：分析 import 关系
       ↓
识别异步边界（如 import() 动态导入）
       ↓
每个异步 Chunk 的 CSS → 提取为独立的 .css 文件
       ↓
同步入口的 CSS → 合并到主 CSS 文件
       ↓
构建产物：多个 JS Chunk + 多个 CSS Chunk
```

举个具体例子，假设项目结构如下：

```javascript
// main.js - 入口文件
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 异步导入组件
const Dashboard = () => import('./views/Dashboard.vue')
const Settings = () => import('./views/Settings.vue')
```

当 `cssCodeSplit: true`（默认值）时，构建产物大致为：

| 文件 | 说明 |
|------|------|
| `index-[hash].js` | 主 JS 入口 Chunk |
| `index-[hash].css` | 主 CSS 文件（包含 ElementPlus 全局样式 + App 样式） |
| `Dashboard-[hash].js` | Dashboard 异步 JS Chunk |
| `Dashboard-[hash].css` | Dashboard 组件的 CSS Chunk |
| `Settings-[hash].js` | Settings 异步 JS Chunk |
| `Settings-[hash].css` | Settings 组件的 CSS Chunk |

### 1.3 cssCodeSplit 配置项 / The cssCodeSplit Option

`build.cssCodeSplit` 是 Vite 提供的一个 Boolean 类型的构建选项，用于控制 CSS 代码分割的行为：

```javascript
// vite.config.mjs
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    cssCodeSplit: true   // 默认值：启用 CSS 代码分割
  }
})
```

| 配置值 | 行为 | CSS 产物 |
|--------|------|----------|
| `true`（默认） | 异步 Chunk 的 CSS 提取为独立文件 | 多个 `.css` 文件 |
| `false` | 禁用分割，所有 CSS 合并到一个文件 | 单个 `.css` 文件 |

**当 `cssCodeSplit: true` 时** ：

- 每个异步 JS Chunk 对应一个独立的 CSS 文件
- CSS 文件通过 `<link>` 标签在 JS Chunk 加载时自动插入
- 优点：减少首屏 CSS 体积，支持按需加载
- 缺点：**CSS 文件的加载顺序不可控**

**当 `cssCodeSplit: false` 时** ：

- 项目中所有 CSS（包括异步组件的样式）全部合并到一个文件
- 该文件在 HTML 的 `<head>` 中通过一个 `<link>` 标签统一加载
- 优点：**样式加载顺序确定**，不会出现顺序混乱
- 缺点：单个 CSS 文件体积较大

> Vite 在使用 `build.lib` 库模式时，`cssCodeSplit` 会自动设为 `false`。

参考资料：

- [Build Options - cssCodeSplit -- Vite](https://vite.dev/config/build-options) ⭐值得阅读
- [构建选项 - cssCodeSplit -- Vite 中文文档](https://cn.vite.dev/config/build-options)
- [CSS Code Splitting -- Vite Features](https://vite.dev/guide/features) ⭐值得阅读
- [Vite Code Splitting 详解 -- 博客园](https://www.cnblogs.com/Answer1215/p/18723238)
- [Vite 打包时遇到的坑 -- 掘金](https://juejin.cn/post/7646084756715405327)

---

## 2. CSS 加载顺序混乱问题 / CSS Loading Order Chaos

> **Note:** 本章分析 CSS 代码分割如何导致生产环境样式失效 / This chapter analyzes how CSS code splitting causes style failures in production.

### 2.1 CSS Cascade 与加载顺序的关系 / CSS Cascade and Loading Order

浏览器的 CSS 层叠（Cascade）机制决定了当多个样式规则作用于同一元素时，哪个样式最终生效。层叠算法考虑三个因素：

1. **Source Order（来源顺序）** ：后加载的样式表覆盖先加载的样式表
2. **Specificity（优先级）** ：ID 选择器 > Class 选择器 > 元素选择器
3. **Importance（`!important`）** ：标记了 `!important` 的样式最高优先

当两个样式规则的 **Specificity 相同** 时， **后加载的样式会覆盖先加载的样式** 。这就是 CSS 代码分割引发问题的核心原因。

**直观类比** ：想象两个画家在同一块画布上画画

- 先画的画家（先加载的 CSS）画了背景色
- 后画的画家（后加载的 CSS）覆盖了先画的内容
- 如果两个画家的“权力等级”相同（Specificity 相同），后画的就会覆盖先画的

### 2.2 代码分割如何破坏加载顺序 / How Code Splitting Breaks Loading Order

当 `cssCodeSplit: true` 时，构建产物包含多个独立的 CSS 文件。这些 CSS 文件通过 JavaScript 动态插入 `<link>` 标签来加载，而不是在 HTML 的 `<head>` 中静态声明。

问题就在于：**JavaScript 的执行顺序和 CSS Chunk 的加载顺序并不总是可预测的**。

```
生产环境 HTML 加载流程：

1. 加载 <head> 中的主 CSS 文件（index-[hash].css）
   ├── 包含 ElementPlus 全局样式
   └── 包含 main.js 中同步导入的自定义样式

2. 加载并执行主 JS 文件（index-[hash].js）
   └── JS 内部触发异步组件加载

3. 异步 JS Chunk 加载（Dashboard-[hash].js）
   └── JS 执行后动态插入 <link> 标签

4. 异步 CSS Chunk 加载（Dashboard-[hash].css）
   └── ⚠️ 这个 CSS 文件可能在 ElementPlus 样式之前或之后插入
```

**关键问题**：异步 CSS Chunk 的 `<link>` 标签是由 JavaScript 在运行时动态插入到 DOM 中的。这意味着：

- 开发环境：Vite Dev Server 通过 `<style>` 标签内联注入 CSS，按照 `import` 顺序执行，样式顺序确定
- 生产环境：CSS Chunk 变成独立的 `.css` 文件，通过 `<link>` 标签动态加载， **加载顺序可能与开发环境不一致**

### 2.3 ElementPlus 自定义样式被覆盖的根因 / Why ElementPlus Custom Styles Get Overridden

这是一个非常典型的场景。假设开发者在 `main.js` 中这样写：

```javascript
// main.js
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'      // ElementPlus 默认样式
import './styles/custom.css'               // 自定义样式（期望覆盖默认样式）
import App from './App.vue'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
```

在开发环境中，样式加载顺序是确定的：

```
开发环境样式加载顺序：
1. element-plus/dist/index.css  ← 先加载
2. custom.css                    ← 后加载，成功覆盖默认样式 ✅
```

但在生产环境中，当 `cssCodeSplit: true` 时，这些 CSS 可能被拆分到不同的 Chunk 中：

```
生产环境样式加载顺序（可能）：
1. index-[hash].css（包含 main.js 的同步样式）
2. JS 执行后动态插入异步 Chunk 的 CSS
   └── ElementPlus 的某些组件样式可能在异步 Chunk 中
       └── 后加载的 ElementPlus 样式覆盖了自定义样式 ❌
```

**具体到下拉框组件**：ElementPlus 的 Select/Dropdown 组件内部使用了 Popper.js 来渲染弹出层，弹出层的 DOM 通常被 Teleport 到 `<body>` 下。这意味着：

- 自定义样式作用在组件内部，被打包到主 CSS 文件
- ElementPlus 的下拉弹出层样式可能在异步 Chunk 中，动态插入的 `<link>` 标签晚于自定义样式加载
- **结果**：ElementPlus 默认样式后加载，覆盖了自定义样式，导致下拉框不显示正确的时间段

参考资料：

- [Vite injects css assets in wrong order with dynamic import -- GitHub](https://github.com/vitejs/vite/issues/3924) ⭐值得阅读
- [The order of `<link>` and `<style>` changes after build -- GitHub](https://github.com/vitejs/vite/issues/4890)
- [Precedence in CSS (When Order of CSS Matters) -- CSS-Tricks](https://css-tricks.com/precedence-css-order-css-matters/) ⭐值得阅读
- [Specificity - CSS -- MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Specificity)
- [Vite 中 ElementPlus 和 TailwindCSS 最佳实践 -- Whidy Writes](https://www.whidy.net/vite-use-elementplus-and-tailwindcss-best-practice-1st)
- [Vue3 项目打包后 CSS 样式丢失 -- CSDN](https://blog.csdn.net/m0_66879773/article/details/136654876)

---

## 3. 解决方案：禁用 CSS 代码分割 / Solution: Disable CSS Code Splitting

> **Note:** 本章详细讲解如何通过配置 `cssCodeSplit: false` 解决问题 / This chapter explains how to solve the problem by configuring `cssCodeSplit: false`.

### 3.1 核心配置 / Core Configuration

在 `vite.config.mjs`（或 `vite.config.js`、`vite.config.ts`）中设置 `build.cssCodeSplit` 为 `false`：

```javascript
// vite.config.mjs
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    cssCodeSplit: false   // 禁用 CSS 代码分割，所有 CSS 合并到单个文件
  }
})
```

这一行配置的作用：

- Vite 在生产构建时，将 **整个项目中所有 CSS**（包括同步和异步组件的样式）提取到一个统一的 CSS 文件中
- 该 CSS 文件在 HTML 的 `<head>` 中通过单个 `<link>` 标签静态加载
- **消除了动态插入 `<link>` 标签导致的加载顺序不确定性**

### 3.2 配置前后的构建产物对比 / Build Output Comparison

**配置前（`cssCodeSplit: true`，默认值）**：

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js          # 主 JS 入口
│   ├── index-[hash].css         # 主 CSS（同步样式）
│   ├── Dashboard-[hash].js      # 异步 Chunk
│   ├── Dashboard-[hash].css     # 异步 CSS Chunk ⚠️ 动态加载
│   ├── Settings-[hash].js       # 异步 Chunk
│   └── Settings-[hash].css      # 异步 CSS Chunk ⚠️ 动态加载
```

**配置后（`cssCodeSplit: false`）**：

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js          # 主 JS 入口
│   ├── index-[hash].css         # 所有 CSS 合并到一个文件 ✅
│   ├── Dashboard-[hash].js      # 异步 Chunk
│   └── Settings-[hash].js       # 异步 Chunk
```

注意：异步 JS Chunk 仍然存在，但不再附带独立的 CSS 文件——所有样式都已合并到 `index-[hash].css` 中。

### 3.3 为什么禁用分割能解决问题 / Why Disabling Splitting Solves the Problem

禁用 CSS 代码分割后，样式加载顺序问题被彻底解决，原因如下：

| 对比维度 | cssCodeSplit: true | cssCodeSplit: false |
|----------|-------------------|--------------------|
| CSS 文件数量 | 多个（每个 Chunk 一个） | 单个 |
| 加载方式 | 动态 `<link>` 插入 | 静态 `<head>` 加载 |
| 加载顺序 | 不可控，取决于 JS 执行时机 | 确定，按 `import` 顺序合并 |
| 开发/生产一致性 | ❗ 可能不一致 | ✅ 完全一致 |
| 首屏 CSS 体积 | 较小（按需加载） | 较大（全量加载） |

**根本原理**：当所有 CSS 合并到一个文件时，浏览器在解析 HTML 时一次性加载全部样式。CSS 文件内部的样式顺序由 Vite 按照源码中的 `import` 顺序决定，与开发环境保持一致。因此：

1. ElementPlus 默认样式先导入
2. 自定义样式后导入
3. 后导入的样式自然覆盖先导入的样式
4. 生产环境与开发环境行为完全一致

### 3.4 禁用分割的权衡 / Trade-offs of Disabling Splitting

禁用 CSS 代码分割并非没有代价，需要根据项目情况权衡：

| 场景 | 是否推荐禁用 | 原因 |
|------|------------|------|
| 小型/中型项目 | ✅ 推荐 | CSS 总量不大，单文件加载无明显影响 |
| 大型项目（CSS > 200KB） | ⚠️ 谨慎 | 首屏加载体积较大，可考虑手动拆分 |
| 多入口项目（MPA） | ✅ 推荐 | 避免多入口共享依赖导致的样式冲突 |
| 组件库 / Lib 模式 | ❌ 不推荐 | Vite 的 `build.lib` 模式默认禁用分割 |
| 依赖 UI 组件库的项目 | ✅ 推荐 | 彻底解决 UI 库样式覆盖问题 |

参考资料：

- [Build Options - cssCodeSplit -- Vite](https://vite.dev/config/build-options) ⭐值得阅读
- [CSS Code Splitting 禁用说明 -- Vite 中文文档](https://cn.vite.dev/config/build-options)
- [Vite 打包时遇到的坑，原来问题出在这里 -- 掘金](https://juejin.cn/post/7646084756715405327) ⭐值得阅读
- [Vite 打包之后 CSS 文件丢失 -- GitHub Issue #3296](https://github.com/vitejs/vite/issues/3296)
- [Vite 打包时遇到的 CSS 坑 -- 51CTO](https://blog.51cto.com/itchenhan/14648618)

---

## 4. 实际案例：ElementPlus 下拉框时间段不显示 / Real Case: ElementPlus Dropdown Time Period Not Displaying

> **Note:** 本章通过一个真实案例展示完整的排查与修复流程 / This chapter demonstrates the full debugging and fixing process through a real case.

### 4.1 问题描述 / Problem Description

在某个 Vue 3 + Vite + ElementPlus 项目中，有一个时间段选择器组件（基于 `el-select`），用户可以下拉选择时间段（如“上午”、“下午”、“晚上”等）。

**开发环境表现**：

- 下拉框正常显示当前选中的时间段 ✅
- 自定义样式正确覆盖 ElementPlus 默认样式 ✅
- 选中项的视觉效果与设计稿一致 ✅

**生产环境表现**：

- 下拉框不显示当前选中的时间段 ❌
- ElementPlus 默认样式覆盖了自定义样式 ❌
- 选中项的文字颜色、背景等与设计稿不一致 ❌

### 4.2 问题排查 / Debugging Process

**第1步：确认问题只出现在生产环境**

开发环境（`vite dev`）下，下拉框表现正常。这说明问题不是代码逻辑错误，而是构建过程引入的差异。

**第2步：检查构建产物**

执行 `vite build` 后检查 `dist/` 目录，发现多个 CSS 文件：

```
dist/assets/
├── index-[hash].css              # 主 CSS
├── TimeSelector-[hash].css       # 时间段选择器的 CSS Chunk
└── vendor-[hash].css             # ElementPlus 的 CSS Chunk
```

**第3步：检查生产环境样式加载顺序**

通过浏览器 DevTools 的 Network 面板，发现：

1. `index-[hash].css` 最先加载（包含自定义样式）
2. 异步 JS Chunk 加载后，动态插入了 `<link>` 标签加载 ElementPlus 组件的 CSS Chunk
3. ElementPlus 的 CSS Chunk **后加载**，其样式覆盖了自定义样式

**第4步：确认根因**

通过 DevTools 的 Elements 面板检查下拉框元素，发现：

- 自定义样式 `.el-select-dropdown__item.is-selected` 被 ElementPlus 默认样式覆盖
- 两者的 **Specificity 相同**，因此后加载的样式生效
- 在生产环境中，ElementPlus 默认样式因为动态 `<link>` 插入时机晚于自定义样式，所以覆盖了自定义样式

### 4.3 修复方案 / Fix Implementation

**修改 `vite.config.mjs`**：

```javascript
// vite.config.mjs
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    cssCodeSplit: false   // 禁用 CSS 代码分割，确保所有样式按正确顺序加载
  }
})
```

仅添加了 `cssCodeSplit: false` 一行配置，其余代码无需任何修改。

### 4.4 修复验证 / Fix Verification

重新执行 `vite build` 后：

**构建产物变化**：

```
dist/assets/
├── index-[hash].css              # 所有 CSS 合并到一个文件 ✅
├── TimeSelector-[hash].js        # 异步 JS Chunk（无配套 CSS 文件）
└── vendor-[hash].js              # 供应商 JS Chunk
```

**生产环境表现**：

- 下拉框正常显示当前选中的时间段 ✅
- 自定义样式正确覆盖 ElementPlus 默认样式 ✅
- 与开发环境效果完全一致 ✅

### 4.5 修复总结 / Fix Summary

| 维度 | 修复前 | 修复后 |
|------|--------|--------|
| **问题原因** | CSS 代码分割导致样式加载顺序混乱 | - |
| **解决方案** | - | `cssCodeSplit: false` |
| **修复效果** | ElementPlus 默认样式覆盖自定义样式 | 下拉框正确显示选中的时间段 |
| **代码改动量** | - | 1 行配置 |
| **副作用** | - | CSS 合并为单文件，体积略增 |

参考资料：

- [ElementPlus el-select odd behavior after build -- GitHub](https://github.com/element-plus/element-plus/discussions/15652)
- [修改 Element Plus 下拉框 el-select 样式 -- CSDN](https://blog.csdn.net/weixin_65982275/article/details/145061763)
- [Vite support | Vite 相关问题 -- GitHub Issue #2611](https://github.com/element-plus/element-plus/issues/2611)
- [Vue3 + Vite 项目打包后 CSS 样式丢失 -- CSDN](https://blog.csdn.net/m0_66879773/article/details/136654876) ⭐值得阅读

---

## 5. 总结 / Summary

本文档从原理到实践，完整讲解了通过禁用 CSS 代码分割解决生产环境样式加载顺序问题的全过程。核心要点回顾：

| 知识点 | 核心内容 |
|--------|----------|
| **CSS 代码分割** | Vite 默认将异步 Chunk 的 CSS 提取为独立文件，通过 `<link>` 动态加载 |
| **加载顺序混乱** | 动态 `<link>` 插入时机不可控，导致后加载的 CSS 覆盖先加载的样式 |
| **ElementPlus 样式覆盖** | 当 Specificity 相同时，后加载的样式表生效，默认样式覆盖了自定义样式 |
| **解决方案** | 在 `vite.config.mjs` 中设置 `cssCodeSplit: false`，一行配置彻底解决 |
| **修复效果** | 所有 CSS 合并到单个文件，加载顺序确定，生产环境与开发环境一致 |

> **Key Takeaways / 核心要点**
> - **CSS code splitting trades loading order predictability for smaller initial payload** / CSS 代码分割用加载顺序的可预测性换取更小的首屏体积
> - **When specificity is equal, the last-loaded stylesheet wins** / 当 Specificity 相同时，后加载的样式表生效
> - **Setting `cssCodeSplit: false` merges all CSS into one file, eliminating order issues** / 设置 `cssCodeSplit: false` 将所有 CSS 合并为一个文件，消除顺序问题
> - **Development and production environments should behave consistently** / 开发环境和生产环境应保持一致的行为

---

**最后更新时间**：2026-06-28
