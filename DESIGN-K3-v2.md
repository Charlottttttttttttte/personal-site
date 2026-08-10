# 个人网站 · 视觉/交互设计规范 v2.0（可爱路线 · K3 交付）

> 状态：**K3 设计细化 v2.0**（2026-08-04）· 替代 v1.0「墨·朱」暗色方向（v1.0 存档于 DESIGN-K3.md，不再执行）
> 依据：Charlotte 新需求「动森版、可爱一点」+ llm-wiki 风格素材（Animal Island UI / 15 种设计风格 Prompt 库）
> 分工：本规范由 K3 编写，DeepSeek 照规范实现；色值、字号、圆角、边框、阴影、字体名均已给定，不需要再自由发挥。
> 风格来源对照：动森可爱＝Animal Island UI；孟菲斯 / 像素艺术 / 有机自然＝15 种风格 Prompt 库的 #6 / #14 / #9。

---

## 0. 通用约定（四个风格都适用）

### 0.1 断点（与现有 demo 一致，不另起）

| 断点 | 范围 | 关键变化 |
|:---|:---|:---|
| 桌面 | ≥960px | 内容最大宽 1080px 居中；作品集 3 列；「正在学」两条左右并列 |
| 平板 | 640–959px | 作品集 2 列；「正在学」改上下堆叠；Hero 名缩一档 |
| 手机 | <640px | 作品集 1 列；`.section` 左右内边距 16px；Hero 名再缩一档；隐藏 Hero 右上角提示便签（`.hero-note`） |

- 首屏高度一律 `100svh`（禁 `100vh`，移动端地址栏抖动）
- 触控目标 ≥44px；可点击卡片必须有 `:focus-visible` 态（见 0.4）
- 数字一律 `font-variant-numeric: tabular-nums` 防跳动

### 0.2 动效总纪律

- 所有 GSAP 动画必须过 `prefers-reduced-motion` 检查：命中时 `gsap.set()` 直接到终态；3D 场景命中时关 `autoRotate`、停循环浮动（三个 demo 的 GSAP 部分已做到，沿用该写法）
- **CSS 动画也要检查**：`@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }` 加在样式表末尾（demo-e 的闪烁光标目前漏了，见 §6.3）
- **移动端滚动劫持修复（三个 demo 都要改）**：OrbitControls 会把 canvas 的 `touch-action` 设为 `none`，导致手机上手指按在第一屏无法纵向滚动页面。创建 controls 之后必须补一行：

```js
const controls = new OrbitControls(camera, renderer.domElement);
renderer.domElement.style.touchAction = 'pan-y';  // 放行纵向滚动，保留横向拖拽旋转
```

- ScrollTrigger 统一 `start: 'top 80%'`、`once: true`
- 每屏入场动画 ≤3 组（例如：区块标题 1 组 + 内容 1 组 + 进度条 1 组），循环动画每屏 ≤1 个（如滚动引导箭头）

### 0.3 字体加载（四个风格统一写法）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
```

中文字体（ZCOOL KuaiLe / Ma Shan Zheng / Noto Sans SC）文件大，Google Fonts 会自动分片按需加载，直接用即可；首屏标题在字体未就绪时会闪现系统字体，可接受，不做 font loading API 等待。

### 0.4 无障碍最低线

```css
.work-card:focus-visible { outline: 3px solid <风格强调色>; outline-offset: 3px; }
```

---

## 1. 新方向设计原则：怎么可爱而不腻

「可爱」翻车的路径只有一种——**每个元素都在撒娇**。一页里圆角、旋转、贴纸、阴影、跳色、弹性动效同时拉满，就腻了。四个风格共用以下克制框架：

### 1.1 三条通用原则

1. **颜色有编制**：每个风格色板 = 中性色（底/卡/字/线，≤4 个）+ 彩色（≤4 个）。彩色是"编制内人员"，除此之外禁新增色；每屏彩色元素 ≤3 处。
2. **装饰有配额**：每屏装饰性元素（贴纸、便签、旋转、图案背景、点缀图形）合计 ≤3 种。例如 Hero 屏已经有「旋转便签 + 波点背景」，就不要再加第三个。
3. **动效有主次**：每屏只允许 1 个"主角动效"（首屏是 3D 场景，正在学是进度条生长），其余动效（hover、入场）幅度小、时长短（≤0.3s 的用 transition，0.6–1.0s 的 GSAP 入场）。弹性缓动（back.out / elastic）只给主角和小元素，不给整屏内容。

### 1.2 各风格各自的克制点（一句话版）

| 风格 | 最容易做腻的地方 | 克制点 |
|:---|:---|:---|
| 动森可爱 | 绿色堆砌 + 全圆角 + 全贴纸 | 彩色限「叶绿 / 天蓝 / 木棕」3 个；贴纸便签每屏 ≤1 个；旋转角度 ≤2°；阴影只用绿色系硬投影（0 模糊），不用灰黑弥散阴影 |
| 孟菲斯 | 高饱和撞色 + 全元素旋转 | 彩色 4 个但**每屏彩色块 ≤3 处**，其余墨黑；黑色描边统一 3px；旋转幅度 -3°~3°；背景几何图案只用 1 种（波点），不加波浪线/半圆 |
| 像素艺术 | 满屏 Press Start 2P + 多彩像素 | 严格 Gameboy 四阶绿，禁第 5 色；像素字体只用于拉丁字母/数字/标签，**中文一律黑体粗字重**；所有动效用 `steps()` 阶梯缓动，禁用平滑缓动（平滑在像素风里等于穿帮） |
| 有机自然 | 阴影过厚显脏 + blob 过多 | 阴影全部柔和多层、禁硬边投影；blob 装饰每屏 ≤1 个（3D 场景里的不算）；手写体（Ma Shan Zheng）只给标题/注释，正文用黑体保可读性 |

---

## 2. 风格一：动森可爱（主推，对应 demo-c）

灵感：Animal Island UI（llm-wiki 实体页）——奶油底、叶绿、天空蓝、木棕，低多边形小岛。

### 2.1 色板

```css
:root {
  --cream:     #FFF9EC;  /* 页面底：奶油 */
  --card:      #FFFDF6;  /* 卡片底：比页面更亮半档 */
  --leaf:      #7FB77E;  /* 彩色①：叶绿（边框、标签底） */
  --leaf-deep: #5E9C5A;  /* 叶绿深色（强调文字、进度终点、hover） */
  --sky:       #AFDDE9;  /* 彩色②：天蓝（仅 Hero 渐变与 3D） */
  --wood:      #B58452;  /* 彩色③：木棕（仅 3D 树干与小图标） */
  --ink:       #5B4B3F;  /* 正文：暖深棕（不用纯黑，柔和） */
  --ink-dim:   #8C7B6A;  /* 次级文字 */
  --line:      #E7DCC3;  /* 分隔线/虚线：米色 */
  --track:     #E9E0CB;  /* 进度轨底、刻度底 */
}
```

纪律：页面 2D 部分只用 `--leaf / --leaf-deep` 一个彩色家族；`--sky / --wood` 是 3D 场景与 Hero 渐变专用，不进卡片和按钮。

### 2.2 字体

| 用途 | 字体 | 说明 |
|:---|:---|:---|
| 标题（区块标题、卡片标题、Hero 名） | ZCOOL KuaiLe | Google Fonts 中文可爱手写体，只有 400 一档，不要加 font-weight |
| 正文 | Noto Sans SC 400/500/700 | |
| 数字 / 英文标签 | Fredoka 500/600 | 天数 D11/28、序号、kicker，圆润英文配 KuaiLe |

字号阶梯：Hero 名 74 / 区块标题 36 / 卡片标题 21 / 正文 16 / 注释 13–14；平板 54 / 手机 40，区块标题手机 28。

### 2.3 Hero 3D 场景（低多边形小岛，demo-c 已实现，定稿参数）

- 场景元素与色值（`MeshLambertMaterial` + `flatShading: true`）：
  - 沙滩底座：压扁球 `SphereGeometry(2.15, 28, 18)`，`scale(1, .30, 1)`，色 `0xEBD3A0`
  - 草地：压扁球 `SphereGeometry(1.95, 28, 18)`，`scale(1, .26, 1)`，色 `0x7FB77E`
  - 树 1 棵：干 `CylinderGeometry(.24,.34,1.2,7)` 色 `0xB58452`；冠两球 `0x66A86A` / `0x8BC48A`
  - 小花 1 朵、石头 1 块（`IcosahedronGeometry(.22,0)` 色 `0xC9BFA9`）
  - 云 3 朵 + 太阳 1 个（`0xFFD166`）：**加在 scene 不加在 group**，拖拽转岛不转天——这是 demo-c 里最好的一个决定，保留
- 灯光：`HemisphereLight(0xffffff, 0xbcd9c4, 1.3)` + `DirectionalLight(0xffffff, 1.6)` 位置 (4,6,3)
- 相机 `(0, 1.8, 7)`，OrbitControls `target(0,.5,0)`，`autoRotateSpeed 0.6`，禁缩放/平移
- Hero 底：`linear-gradient(180deg, var(--sky) 0%, #CBE9F2 68%, var(--cream) 100%)`，3D renderer `alpha: true`
- 页面底纹：波点 `radial-gradient(rgba(127,183,126,.16) 1.5px, transparent 1.6px)`，`background-size: 26px`；<640px 降为 32px、透明度 .10
- 移动端：场景元素已很少，不删减；`pixelRatio` 上限 2

### 2.4 组件规范

**「正在学」进度条（叶尖胶囊条）**：

```css
.track { height: 16px; border-radius: 999px; background: var(--track);
         box-shadow: inset 0 2px 4px rgba(91,75,63,.12); }
.fill  { height: 100%; border-radius: 999px;
         background: linear-gradient(90deg, #A8D8A8, var(--leaf-deep)); }
.fill::after { /* 叶尖：与渐变终点同色的圆角三角叶 */
  content: ''; position: absolute; right: -7px; top: 50%; transform: translateY(-50%);
  width: 18px; height: 18px; background: var(--leaf-deep);
  border-radius: 18px 18px 0 18px; }
```

- 天数：`D11/28`，Fredoka 600 18px `--leaf-deep`；宽度 = 39%
- **阶段刻度（Agent 平台）**：圆点 14px，当前点 `--leaf-deep` + 外圈 `box-shadow: 0 0 0 4px rgba(94,156,90,.2)`，未达点 `--track`；连线高 4px 胶囊 `--track`；阶段名 12px，当前名 `--leaf-deep` 700 粗

**作品卡**：

```css
.work-card {
  background: var(--card); border: 3px solid var(--leaf); border-radius: 24px;
  padding: 26px 24px 22px;
  box-shadow: 0 8px 0 rgba(94,156,90,.14), 0 12px 22px rgba(91,75,63,.06);
}
.work-card:hover { transform: translateY(-6px);
  box-shadow: 0 14px 0 rgba(94,156,90,.16), 0 18px 28px rgba(91,75,63,.1); }
```

- 结构：序号胶囊（`--leaf` 底白字 Fredoka 13px）→ KuaiLe 标题 21px → 描述 14px `--ink-dim` → 底部 `2px dashed var(--line)` 分隔 + 标签行 + `→`
- hover 只位移**不旋转**（多张卡并列时旋转显乱，见 §6.1 修正 2）
- 硬投影用绿色系（动森"纸叠层"感），灰黑弥散阴影只做一层淡淡的陪衬

### 2.5 动效

- Hero 名逐字符 `y:26→0`，`back.out(1.6)`，stagger .045
- 进度条生长 1.0s `power3.out` + 天数 count-up 1.2s 同步；当前阶段点 `scale 0→1` `back.out(2.4)`
- 卡片入场 `y:34→0` stagger .1；箭头循环 bounce `sine.inOut`

---

## 3. 风格二：孟菲斯（对应 demo-d）

灵感：15 风格 Prompt 库 #6——明亮 pastel、几何图案、粗黑边、随机旋转、弹性 hover。

### 3.1 色板

```css
:root {
  --paper:  #FFF9F0;  /* 米白底 */
  --card:   #FFFFFF;
  --ink:    #17171A;  /* 墨黑：所有描边/硬阴影/正文，全站统一 */
  --pink:   #FF87AB;  /* 彩色①（由 demo 的 #FF5C8A 降饱和，见 §6.2 修正 1） */
  --yellow: #FFD23F;  /* 彩色②（由 #FFC82E 微调） */
  --blue:   #6FB1FF;  /* 彩色③（由 #3E9BFF 降饱和） */
  --teal:   #4ECDC4;  /* 彩色④（由 #00C2A8 微调） */
}
```

纪律：4 个彩色是"编制"，但**每屏彩色块 ≤3 处**（例如 Hero：名字跳色算 1、黄底 tag 算 2、teal 便签算 3——已满，其他元素全墨黑）。所有描边统一 `3px solid var(--ink)`，硬阴影统一 `Npx Npx 0 var(--ink)`。

### 3.2 字体

| 用途 | 字体 |
|:---|:---|
| 标题（拉丁）/ 数字 / 标签 | Fredoka 700/900 |
| 中文标题 / 正文 | Noto Sans SC（标题 900、正文 400/700），中文自动回退，写 `font-family: 'Fredoka','Noto Sans SC',sans-serif` |

字号阶梯：Hero 名 86 / 区块标题 34 / 卡片标题 21 / 正文 16；手机 44 / 26。

### 3.3 Hero 3D 场景（孟菲斯几何组合，demo-d 已实现，定稿参数）

- `MeshBasicMaterial` 平色 + `EdgesGeometry` 墨线描边（`0x17171A`）——不上灯光，孟菲斯要的是平面感
- 组合：粉球 `SphereGeometry(1.05,20,16)`、蓝环 `TorusGeometry(.9,.32,16,36)`、黄锥 `ConeGeometry(.9,1.8,5)`、teal 方块 + 2 个小点缀块，位置参 demo-d
- 整体轻浮 `sin(t*.8)*.06`；`autoRotateSpeed 0.8`（demo 的 1.4 偏快，见 §6.2 修正 4）
- Hero 底：`linear-gradient(180deg, #FFF4DF 0%, var(--paper) 90%)`；页面波点 `rgba(23,23,26,.14)` 34px

### 3.4 组件规范

- **进度条**：轨高 18px，`3px solid var(--ink)` + `box-shadow: 3px 3px 0 var(--ink)`；填充 `--yellow` 底 + 墨点纹 `radial-gradient(rgba(23,23,26,.35) 1.5px, transparent 1.6px) 12px`；天数 Fredoka 700 `--pink`
- **阶段刻度**：圆点 14px 白底 3px 墨边，当前点填 `--blue`；连线 5px `var(--ink)` opacity .18
- **作品卡**：白卡 `3px` 墨边、`border-radius: 14px`、`box-shadow: 6px 6px 0 var(--ink)`；右上贴纸圆 `--yellow` 56px 3px 墨边（`overflow:hidden` 裁 3/4）；hover = **按下**：`translate(4px,4px)` + 阴影缩到 `2px 2px 0`（demo 方向反了，见 §6.2 修正 2）；卡片底部分隔线 `3px solid var(--ink)`
- 装饰配额：区块序号（墨底倾斜 -3° + 粉色错位阴影）+ 标题后黄点 `●`，恰好 2 种，够了

### 3.5 动效

- Hero 名逐字符 `back.out(1.8)` stagger .05；tag `scale .8→1` `back.out(2)`
- hover 类全部 transition ≤.15s（按压感要快）；入场 GSAP ≤.7s

---

## 4. 风格三：像素艺术（对应 demo-e）

灵感：15 风格 Prompt 库 #14——Gameboy 四阶绿、Press Start 2P、RPG 界面、阶梯动效。

### 4.1 色板（严格 4 色，禁第 5 色）

```css
:root {
  --gb0: #0F380F;  /* 最深：正文、描边、硬阴影 */
  --gb1: #306230;  /* 深：次级文字、暗面 */
  --gb2: #8BAC0F;  /* 亮：卡片底、点缀 */
  --gb3: #9BBC0F;  /* 最亮：页面底、填充高光 */
}
```

### 4.2 字体

| 用途 | 字体 |
|:---|:---|
| 拉丁标题 / 数字 / 英文标签 | Press Start 2P（只有一个字重，禁止加粗） |
| **所有中文** | Noto Sans SC（标题 900、正文 500/700）——像素字体没有中文，中文用粗黑体是正确解，demo 已这样处理 |

字号：Hero 名 54（手机 26，letter-spacing 2px）/ 区块标题 30 / 卡片标题 20 / 正文 16；Press Start 2P 最小不低于 9px（8px 不可读，见 §6.3 修正 3）。

### 4.3 Hero 3D 场景（低分辨率像素草方块，demo-e 已实现，定稿参数）

- **像素感关键两步**：`renderer.setPixelRatio(0.5)` + **`#gl canvas { image-rendering: pixelated; }`**（缺后者浏览器会双线性插值变模糊，见 §6.3 修正 1）
- 草方块 `BoxGeometry(1.9,1.9,1.9)` 六面材质数组：顶 `0x9BBC0F`、底 `0x306230`、四侧 `0x8BAC0F`，外加深绿 `EdgesGeometry` 描边
- 漂浮小像素块 18 个（手机 10 个），四色轮换，各自反向慢转
- 整体弹跳 `Math.abs(sin(t*1.2))*.15`；`autoRotateSpeed 1`；灯光 Hemisphere + Directional
- Hero 叠加扫描线：`repeating-linear-gradient(0deg, rgba(15,56,15,.07) 0 2px, transparent 2px 4px)`
- 页面底纹：9px 网格双线 `rgba(15,56,15,.05)`

### 4.4 组件规范

- **XP 分段经验条**：轨高 22px，`4px solid var(--gb0)`、底 `--gb1`；填充 `--gb3` + 分段纹 `repeating-linear-gradient(90deg, var(--gb3) 0 9px, var(--gb1) 9px 12px)`，生长用 `steps(10)`
- **阶段刻度**：13px 方块 `rotate(45deg)`（卢比形），`3px solid var(--gb0)`，当前填 `--gb3` + `box-shadow: 0 0 0 3px var(--gb1)`；连线 6px `--gb0` opacity .25
- **作品卡（道具栏）**：`--gb2` 底、`4px solid var(--gb0)`、**无圆角**、`box-shadow: 6px 6px 0 var(--gb0)`；顶部高光条 `::before`；hover = 按下手柄：`translate(4px,4px)` + 阴影归零，`transition: .1s steps(2)`
- 像素切角工具类 `.chip { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }`
- 光标闪烁 `.cursor { animation: blink 1s steps(1) infinite; }`（reduced-motion 时必须关，见 §6.3 修正 2）

### 4.5 动效

- 一切缓动用阶梯：`steps(2)`（hover/箭头）、`steps(10)`（进度条）、`steps(11)`（count-up）；入场 fade-up 可用 `power2.out`（透明度不算穿帮）
- 禁用：back.out、elastic、smooth bounce——平滑弹性在像素风里穿帮

---

## 5. 风格四：有机自然风（demo-f 完整规范 · 尚无 demo，实现者照抄即可）

灵感：15 风格 Prompt 库 #9——大地色系、Soft UI、圆角 20px+、多层柔和阴影、blob 有机形态、手写体+圆润体。

### 5.1 色板

```css
:root {
  --sand:      #F6F1E7;  /* 页面底：米沙 */
  --card:      #FFFDF8;  /* 卡片底 */
  --clay:      #D4A373;  /* 彩色①：陶土（强调、进度、当前刻度） */
  --clay-deep: #B0804F;  /* 陶土深色（hover、文字强调） */
  --sage:      #CCD5AE;  /* 彩色②：鼠尾草绿（渐变副色、3D 副 blob） */
  --sage-deep: #96AC7B;  /* 鼠尾草深色（渐变终点） */
  --cream-2:   #E9EDC9;  /* 彩色③：浅苔色（仅 3D 第三 blob 与大面积色块） */
  --ink:       #4A4238;  /* 正文：暖褐黑 */
  --ink-dim:   #8B7F6F;  /* 次级文字 */
  --line:      #E4DACA;  /* 分隔线 */
  --track:     #EBE3D3;  /* 进度轨底 */
}
```

纪律：2D 页面彩色以 `--clay` 为主角，`--sage` 只做渐变副色和大面积点缀；`--cream-2` 不进文字。

### 5.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Sans+SC:wght@400;500;700&family=Quicksand:wght@500;600;700&display=swap" rel="stylesheet">
```

| 用途 | 字体 | 说明 |
|:---|:---|:---|
| 标题（区块标题、卡片标题、Hero 名） | Ma Shan Zheng | 中文手写体，只有 400，禁加 font-weight |
| 正文 | Noto Sans SC 400/500/700 | |
| 数字 / 英文标签 | Quicksand 600/700 | 圆润几何无衬线，配手写体 |

字号阶梯：Hero 名 72 / 区块标题 36 / 卡片标题 21 / 正文 16 / 注释 14；平板 52 / 手机 38，区块标题手机 28。

### 5.3 页面基底

- 背景 `--sand` 纯色 + **1 个装饰 SVG blob**（装饰配额只有它一个）：定位在「正在学」区块右上、`position: absolute`、`z-index: 0`、色 `--sage`、opacity .35、约 320px：

```html
<svg viewBox="0 0 200 200" width="320" aria-hidden="true">
  <path fill="#CCD5AE" d="M45.7,-58.9C58.9,-49.3,69,-34.4,72.6,-17.9C76.2,-1.4,73.3,16.7,64.9,30.4C56.5,44.1,42.6,53.4,27.3,59.5C12,65.6,-4.7,68.5,-20.3,63.9C-35.9,59.3,-50.4,47.2,-59.4,32C-68.4,16.8,-71.9,-1.5,-67.7,-17.4C-63.5,-33.3,-51.6,-46.8,-37.9,-56.2C-24.2,-65.6,-8.7,-70.9,4.7,-66.4C18.1,-61.9,32.5,-68.5,45.7,-58.9Z" transform="translate(100 100)"/>
</svg>
```

- 全站圆角 ≥16px（卡片 24px、进度条 999px、按钮 999px），禁直角、禁硬描边、禁硬阴影

### 5.4 Hero 3D 场景（呼吸 blob · 实现者照抄）

核心做法：**Icosahedron 顶点噪声形变**。Three.js r160 的 examples 自带 `SimplexNoise`，importmap 已映射 `three/addons/`，直接可用：

```js
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { SimplexNoise } from 'three/addons/math/SimplexNoise.js';

const noise = new SimplexNoise();
const isMobile = matchMedia('(max-width: 639px)').matches;

// 主 blob：细分 桌面 24 / 手机 12（越大越圆滑也越贵）
const geo = new THREE.IcosahedronGeometry(1.7, isMobile ? 12 : 24);
const base = geo.attributes.position.array.slice();  // 备份原始顶点
const blob = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({ color: 0xCCD5AE }));
scene.add(blob);

// 每帧形变：沿顶点法线方向位移
function morph(t) {
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const ox = base[i*3], oy = base[i*3+1], oz = base[i*3+2];
    const n = noise.noise3d(ox * .8 + t * .25, oy * .8 + t * .25, oz * .8);
    const k = 1 + n * .22;                       // 形变幅度 .22，别超 .3（超了像肿瘤）
    pos.setXYZ(i, ox * k, oy * k, oz * k);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();                    // 重算法线，光照才柔
}
```

- 副 blob 2 个：`SphereGeometry(.42, 24, 18)` 色 `0xD4A373` 和 `0xE9EDC9`，绕主 blob 缓慢公转（半径 2.6，角速度 .15 rad/s，相位差 π），自身不做噪声形变（配额：形变只给主角）
- 灯光：`HemisphereLight(0xffffff, 0xE9EDC9, 1.2)` + `DirectionalLight(0xffffff, 1.4)` 位置 (4,6,3)；材质 `MeshLambertMaterial`（**不要 flatShading**，有机风要圆滑高光）
- 相机 `(0, .4, 6)`；OrbitControls `target(0,0,0)`、`autoRotateSpeed 0.5`、禁缩放平移
- Hero 底：`linear-gradient(180deg, #EFE7D7 0%, var(--sand) 85%)`，renderer `alpha: true`
- 交互：拖拽旋转 + **鼠标视差**（`camera.position.x` 向 `mouseX * .4` lerp，系数 .05）；手机无 hover，仅拖拽
- reduced-motion：`morph(0)` 执行一次定型后停止逐帧形变、关 autoRotate、副 blob 静止；WebGL 失败时 Hero 降级为 §5.3 的 SVG blob + 标题淡入

### 5.5 组件规范

**「正在学」进度条（云朵软条）**：

```css
.track {
  height: 14px; border-radius: 999px; background: var(--track);
  box-shadow: inset 0 2px 5px rgba(74,66,56,.14);      /* 内凹 */
}
.fill {
  height: 100%; border-radius: 999px;
  background: linear-gradient(90deg, var(--sage) 0%, var(--clay) 100%);
  box-shadow: 0 2px 8px rgba(212,163,115,.45);          /* 柔和外发光，禁硬投影 */
}
```

- 天数 `D11/28`：Quicksand 700 18px `--clay-deep`；宽度 39%
- **阶段刻度**：圆点 16px，未达 `--track`，当前 `--clay` + `box-shadow: 0 0 0 5px rgba(212,163,115,.25)`；连线 4px 胶囊 `--track`，已过段填 `--sage`；阶段名 13px，当前名 `--clay-deep` 700

**作品卡（Soft UI 凸面卡）**：

```css
.work-card {
  background: var(--card); border: none; border-radius: 24px;
  padding: 28px 26px 24px;
  box-shadow: 0 2px 6px rgba(74,66,56,.05), 0 14px 34px rgba(74,66,56,.09);
  transition: transform .3s cubic-bezier(.34,1.56,.64,1), box-shadow .3s ease;
}
.work-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 10px rgba(74,66,56,.06), 0 22px 44px rgba(74,66,56,.12);
}
```

- 结构：序号 Quicksand 700 13px `--clay-deep`（`01.` 带点）→ Ma Shan Zheng 标题 21px → 描述 14px `--ink-dim` → 底部 `1px solid var(--line)` + 标签行 + `→`（hover 右移 4px、转 `--clay-deep`）
- 顶部可选一条 6px 圆角色带：`background: linear-gradient(90deg, var(--sage), var(--clay))`，宽 56px，三张卡都有或都没有
- 手写注释贴纸（可选，每屏 ≤1）：Ma Shan Zheng 14px `--clay-deep`，`transform: rotate(-2deg)`，无底无边框

### 5.6 动效（demo-f 用）

| # | 区块 | 效果 | 参数 |
|:--|:---|:---|:---|
| 1 | Hero 名 | 逐字符浮现 | `y:24→0` `back.out(1.4)` stagger .05 |
| 2 | 进度条 | 生长 + count-up | 1.2s `power2.out`（有机风不用 back，柔到底） |
| 3 | 卡片入场 | fade-up + 轻弹 | `y:30→0` 0.9s `power3.out` stagger .12 |
| 4 | 阶段当前点 | 弹入 | `scale 0→1` `back.out(2)` delay .3 |
| 5 | 滚动箭头 | 循环 | `y 0→8` 1.8s `sine.inOut` yoyo |
| 6 | 3D blob | 持续形变 | 见 §5.4，t 走时钟 |

弹性只出现在小元素（字符、刻度点）；区块级内容一律 `power2/3.out`。

---

## 6. Demo 评审（对照本规范逐条）

评审对象：主 agent 写的 demo-c / demo-d / demo-e。**结论先行：三个方向都成立，骨架（Hero 3D + 正在学 + 作品卡 + 959/639 断点 + reduced-motion 检查）与规范一致，可作为对应风格的底稿**；以下是需要修正的点。标注【共性】的项三个 demo 都要改。

### 6.0 共性修正（c/d/e 同改）

1. 【共性·必修】**移动端滚动劫持**：OrbitControls 会把 canvas `touch-action` 设为 `none`，手机上第一屏整屏无法纵向滚动。三个 demo 的 3D 模块里，创建 controls 后各加一行 `renderer.domElement.style.touchAction = 'pan-y';`（见 §0.2）。
2. 【共性】**`:focus-visible` 缺失**：`.work-card` 可点击但键盘聚焦无任何视觉反馈。按 §0.4 各补一条（强调色：c 用 `--leaf-deep`，d 用 `--ink`，e 用 `--gb0`）。若卡片实际是链接，把 `<div class="work-card">` 换成 `<a class="work-card">` 一并解决可聚焦性。
3. 【共性】**作品卡只有 1 张**：正式实现按 DESIGN.md §6 放 3 张（财经知识卡片 / 书法练习打卡 / Obsidian LLM-Wiki）。demo 阶段可接受，整站实现时补齐。
4. 【共性·小】`const isMobile = matchMedia(...)` 在 c/d 两个 3D 模块里声明后未使用（e 有用于像素块数量），删掉或物尽其用。

### 6.1 demo-c（动森可爱）——方向 ✅，最接近定稿

**好的地方（保留）**：

- 色板与规范 §2.1 完全一致，2D 部分守住了"只用叶绿一个彩色家族"的纪律
- 云和太阳挂在 `scene` 而非旋转 `group`——拖拽转岛不转天，是很对的细节
- `.fill::after` 叶尖与渐变终点同色 `var(--leaf-deep)`，衔接自然；`border-radius: 18px 18px 0 18px` 的叶形准确
- 虚线用法克制（卡片底部 `2px dashed var(--line)`、便签 `2px dashed var(--leaf)`），符合"贴纸每屏 ≤1"
- 3D 元素数量、灯光参数、`autoRotateSpeed 0.6` 均无需改

**修正清单**：

1. `.work-card:hover` 去掉 `rotate(-1deg)`，只留 `translateY(-6px)`。依据 §1.2：多张卡并列时各转 -1° 显乱；旋转配额留给 Hero 便签（`.hero-kicker` 的 -2°）。
2. 波点背景加移动端档：`@media (max-width: 639px)` 内 `body { background-size: 32px 32px; background-image: radial-gradient(rgba(127,183,126,.10) 1.5px, transparent 1.6px); }`——26px 波点在 390px 宽屏上偏密。
3. `.stage-seg`（4px `--track` 色）与 `.track` 底色相同，两条"正在学"的视觉重量不一致：把已过的段改为 `background: var(--leaf)`，未过段保持 `--track`，与 §2.4 规范对齐（规范里"已过段填色"demo 漏了）。
4. 【小】`.hero-name` 的 `text-shadow: 2px 2px 0 rgba(255,255,255,.55)` 在天空渐变深区（顶部 `--sky`）下白影略脏，改为 `rgba(255,249,236,.6)`（奶油色）更融。

### 6.2 demo-d（孟菲斯）——方向 ✅，配色需降饱和

**好的地方（保留）**：

- `MeshBasicMaterial` 平色 + `EdgesGeometry` 墨线，不上灯光——正确抓住孟菲斯"平面感"，3D 做法定稿
- 按压式 hover、贴纸圆 `::after`、序号倾斜 + 错位阴影，装饰数量符合规范配额
- 中文标题回退 Noto Sans SC 900 的字体栈写法正确

**修正清单**：

1. **色板降饱和**：`:root` 四彩色按 §3.1 替换——`--pink: #FF5C8A→#FF87AB`、`--yellow: #FFC82E→#FFD23F`、`--blue: #3E9BFF→#6FB1FF`、`--teal: #00C2A8→#4ECDC4`。现值荧光感偏重，更接近新粗野（风格 #2）而非孟菲斯（风格 #6 的"明亮 pastel"）。3D 场景里的 `0xFF5C8A / 0x3E9BFF / 0xFFC82E / 0x00C2A8` 同步换成新色。
2. **按压方向反了**：`.work-card:hover { transform: translate(-2px,-2px); box-shadow: 2px 2px 0 var(--ink); }`——卡片向左上移动而阴影在右下，视觉逻辑矛盾。改为 `transform: translate(4px,4px); box-shadow: 2px 2px 0 var(--ink);`（向阴影方向压下去，阴影 6px→2px 变小，才是"按下"）。
3. `controls.autoRotateSpeed = 1.4` 偏快，改 `0.8`（首屏是阅读场景，几何体转太快抢标题）。
4. `.hero-name .char` 四色轮换 + 黄底 tag + teal 便签：彩色块已 3 处满额，**不要再加**。现状合规，仅提醒实现作品集区时卡片贴纸圆统一用 `--yellow`，勿逐卡换色。
5. 【小】`.stage-seg` 用 `background: var(--ink); opacity: .18` 会得到半透明黑叠在米白底上发灰，改 `background: rgba(23,23,26,.15)` 效果相同但更直接；当前阶段前的段填 `var(--ink)` 实色以表达"已走过"。

### 6.3 demo-e（像素艺术）——方向 ✅，有一个必修的渲染问题

**好的地方（保留）**：

- 低分辨率渲染思路（`setPixelRatio(0.5)`）正确；阶梯缓动 `steps(10)` 进度条、`steps(2)` hover 完全符合像素纪律
- 草方块六面材质数组（顶亮/侧中/底深）+ 深绿描边，Gameboy 四色严格不超编
- 中文标题用黑体 900、像素字体只给拉丁/数字——正确解
- XP 分段条、45° 卢比刻度点、`.chip` 像素切角都是好语言

**修正清单**：

1. 【必修】**缺 `image-rendering: pixelated`**：`setPixelRatio(0.5)` 让缓冲减半，但浏览器把 canvas 拉伸回 CSS 尺寸时默认双线性插值——画面是"模糊"而不是"像素"。加 CSS：

```css
#gl canvas { image-rendering: pixelated; image-rendering: crisp-edges; }
```

2. 【必修】光标闪烁不受 reduced-motion 控制：`.hero-tag .cursor { animation: blink 1s steps(1) infinite; }` 是纯 CSS 动画，现有 JS 的 reduceMotion 检查管不到它。样式表末尾加 §0.2 的通用关停媒体查询（c/d 也建议加，d 无 CSS 循环动画、c 无，但加上做保险）。
3. `.work-foot` 的 Press Start 2P `font-size: 8px` 低于可读下限，改 `9px`（§4.2 规定像素字体最小 9px）；`.hero-note` 的 8px 同理改 9px。
4. `.fill` 内缩 `left/top/bottom: 3px` 与 `.track` 的 `4px` 边框之间会露出 1px `--gb1` 缝隙，像素屏上呈不规则细线。把 `.fill` 内缩改为 `left: 4px; top: 4px; bottom: 4px` 与边框对齐（或 track 加 `padding: 0` 并给 fill 统一 `inset: 4px auto 4px 4px`）。
5. 【小】`.hero-name` 手机档 `letter-spacing: 2px` 保持，但 `font-size: 26px` 下 "CHARLOTTE" 9 字符约 260px，390px 屏没问题；若后续改中文名，记得中文不走 Press Start 2P。

---

## 7. 给 DeepSeek 的实现顺序建议

1. 先按 §6.0 修三个 demo 的共性项（touch-action 一行是移动端硬性问题，优先）
2. Charlotte 拍板主推风格（K3 推荐：动森可爱为主线，像素艺术为备选——动森与"数字花园"概念天然同构）
3. 定稿风格 → 把对应 demo 扩展为整站 5 区块（结构见 DESIGN.md §4），组件参数全部从本规范 §2–§5 抄
4. demo-f（有机自然）若 Charlotte 想看，按 §5 实现，§5.4 的 blob 形变代码可直接运行（依赖 importmap 已配的 `three/addons/`）

## 8. 待 Charlotte 拍板

1. **主推风格**：动森可爱（推荐）/ 孟菲斯 / 像素艺术 / 有机自然——四选一作为整站定稿，其余 demo 存档
2. **动森 Hero 文案语言**：现状英文 kicker + 拉丁名 + 中文定位语，是否保持
3. **作品卡封面**：三个作品是否各配一张封面图（16:10 置卡片顶部），还是纯文字卡（推荐纯文字，三个项目都还没有合适封面物料）

其余项（色值、字号、动效参数、断点）按本规范执行，DeepSeek 可直接开工。
