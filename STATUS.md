# 项目交接文档（STATUS）

> 更新：2026-08-04 · 用途：新终端/新会话接手本项目时的状态快照
> 核心目录：`/Users/charlotte/personal-site/`

---

## 项目是什么

三周目标（验收 2026-08-25）：用 vibe coding 做出**「作品集 + 数字花园」个人网站**（静态站 + Three.js 3D 首屏 + GSAP 动画，GitHub Pages 部署），同时掌握 5 个 AI 概念（验收时能不看 wiki 讲清）。

## 团队分工

| 角色 | 谁 |
|:---|:---|
| 视觉/交互设计细化 + 最终 review | K3（读 DESIGN.md，产出 DESIGN-K3.md） |
| 实现 + 跑腿 + 工具化验证 | DeepSeek（本会话） |
| 每日一考（对话形式，5 概念） | DeepSeek |
| 验收 | Charlotte（8/25） |

## 已完成（Day 1）

1. **仓库**：`~/personal-site/`（git 已初始化，有提交检查点）
2. **DESIGN.md**：给 K3 的设计交付文档（任务范围 + 已确认决策 + 人物背景）
3. **网站骨架**：`index.html`（3D 首屏/正在学/作品集/数字花园/关于/Footer）、`css/style.css`（暗色占位样式）、`js/main.js`（Three.js 线框+粒子+鼠标视差，GSAP 滚动入场）——JS 语法已校验，本地服务 200 通过
4. **概念页补齐**（Obsidian `LLM-Wiki/wiki/concepts/`）：HTML动画、Agent-Orchestration 从空壳重写；3D互动网页、响应式布局补实现要点
5. **作品集三样已定**：财经知识卡片 / 书法练习打卡（含 AI 角度检测模型）/ Obsidian LLM-Wiki

## 当前阻塞点（等 K3）

K3 会话正在做视觉/交互设计。它抛了 4 个决策（风格基调 / 3D 首屏形态 / 标题字体 / Agent 进度表达），用户已要求它**先出 2 个 demo**（`demo-a.html` 墨·朱暗色 / `demo-b.html` 杂志风浅色）给用户看效果再拍板。

**接手后先检查：** `~/personal-site/` 下有没有 `demo-a.html` / `demo-b.html` / `DESIGN-K3.md`——有则说明 K3 已交付，可开工实现。

## 下一步（按顺序）

1. 等 K3 demo 交付 → 用户选风格 → 把正式版样式替换进骨架（配色/字体/3D 方案/动效清单）
2. 补三张作品卡的素材：财经卡片图（`LLM-Wiki/raw/learning/财经/assets/`）、书法打卡可视化、LLM-Wiki 图谱截图
3. 部署 GitHub Pages（远）：仓库推到 GitHub 后启用 Pages
4. **每日一考（明天起）**：5 概念 = vibe coding / 3D互动网页 / HTML动画 / 响应式布局 / Agent 编排；错题进 `LLM-Wiki/raw/learning/<主题>/错题本.md`，间隔复习 1/3/7/14/30 天

## 相关位置

- 项目仓库：`/Users/charlotte/personal-site/`
- 设计交付文档：`/Users/charlotte/personal-site/DESIGN.md`
- Obsidian wiki：`/Users/charlotte/Library/Mobile Documents/iCloud~md~obsidian/Documents/Charlotte/LLM-Wiki/`
- 财经学习项目：`.../LLM-Wiki/raw/learning/财经/`
