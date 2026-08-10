# 个人网站 · 视觉/交互设计规范 v3.0（经典/先锋路线 6 风格 · K3 交付）

> 状态：**K3 设计细化 v3.0**（2026-08-05）· 与 v2.0（可爱路线 4 风格）平行，供 Charlotte 横向比较；最终定稿只有一个风格
> 依据：llm-wiki「15 种设计风格 Prompt 库」——瑞士国际主义 #7 / 包豪斯 #8 / 玻璃拟态 #3 / 新拟态 #12 / Y2K·Frutiger Aero #11 / 酸性设计 #10
> 分工：本规范由 K3 编写，实现者照抄；色值、字号、圆角、阴影、字体名均已给定，不需要再自由发挥。
> 站点骨架：与 v2.0 相同（Hero 3D + 名字 + 定位语 + SCROLL 提示 → 正在学（D11/28 进度条 + Agent 平台 3 阶段刻度）→ 3 张作品卡 → 页脚），6 个 demo 只换视觉与 Hero 3D 场景，结构 HTML 可从 demo-d 复制。

---

## 0. 通用约定（6 个风格都适用，与 v2.0 §0 一致，照搬）

### 0.1 断点

| 断点 | 范围 | 关键变化 |
|:---|:---|:---|
| 桌面 | ≥960px | 内容最大宽 1080px 居中；作品集 3 列；「正在学」两条左右并列 |
| 平板 | 640–959px | 作品集 2 列；「正在学」上下堆叠；Hero 名缩一档 |
| 手机 | <640px | 作品集 1 列；`.section` 左右内边距 16px；Hero 名再缩一档；隐藏 Hero 右上角提示便签（`.hero-note`） |

- 首屏高度一律 `100svh`（禁 `100vh`，移动端地址栏抖动）
- 触控目标 ≥44px；可点击卡片必须有 `:focus-visible` 态（见 0.3）
- 数字一律 `font-variant-numeric: tabular-nums` 防跳动

### 0.2 动效总纪律

- 所有 GSAP 动画必须过 `prefers-reduced-motion` 检查：命中时 `gsap.set()` 直接到终态；3D 场景命中时关 `autoRotate`、停循环浮动与一切循环形变
- **CSS 动画也要检查**，样式表末尾统一加：

```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

- **移动端滚动劫持修复（必修）**：OrbitControls 会把 canvas 的 `touch-action` 设为 `none`。创建 controls 之后必须补一行：

```js
const controls = new OrbitControls(camera, renderer.domElement);
renderer.domElement.style.touchAction = 'pan-y';  // 放行纵向滚动，保留横向拖拽旋转
```

- ScrollTrigger 统一 `start: 'top 80%'`、`once: true`
- 每屏入场动画 ≤3 组；循环动画每屏 ≤1 个
- `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`；酸性风格例外（见 §7）

### 0.3 无障碍最低线

```css
.work-card:focus-visible { outline: 3px solid <风格强调色>; outline-offset: 3px; }
```

各风格强调色：瑞士 `--red` / 包豪斯 `--blue` / 玻璃 `--accent` / 新拟态 `--accent` / Y2K `--accent` / 酸性 `--pink`。

### 0.4 本批 6 风格共用克制框架

v2.0 §1 的「颜色有编制 / 装饰有配额 / 动效有主次」三条继续生效。本批一句话克制点汇总：

| 风格 | 最容易翻车的地方 | 克制点（一句话） |
|:---|:---|:---|
| 瑞士国际主义 | 做成"朴素"而非"精确" | 所有元素贴死网格线，红色全站只出现 3 次（进度、当前刻度、序号），多一次就俗 |
| 包豪斯 | 变成第二个孟菲斯 | 三色每屏各出现 ≤1 次，全站 0 圆角（阶段圆点除外），禁描边禁投影——用色块叠压表达层次 |
| 玻璃拟态 | 玻璃叠玻璃、背景太亮不透 | 背景必须深（L≤25%），玻璃只给卡片/进度轨/导航三级容器，背景光斑 ≤3 个 |
| 新拟态 | 对比度塌掉看不清 | 正文色不得浅于 `#4A5568`，阴影只有「凸起/凹陷」两种状态，彩色只有 1 个蓝 |
| Y2K | 高光叠太多变油腻 | 高光只加一层（顶部 45% 白色渐变），装饰每屏 ≤2 种，蓝天白云只留给 Hero |
| 酸性设计 | 霓虹糊满屏 | 霓虹三色只出现在 3D 灯光、渐变条、光晕三处，大面积保持黑灰铬，glitch 每屏 ≤1 |

---

## 1. 风格一：瑞士国际主义 Swiss（demo-g）

灵感：Prompt 库 #7——严格 12 列网格、Helvetica 大写、黑白灰 + 单一红、无装饰、对齐即设计。

### 1.1 色板

```css
:root {
  --paper: #FFFFFF;   /* 页面底：纯白 */
  --ink:   #111111;   /* 标题、正文 */
  --gray:  #767676;   /* 次级文字 */
  --line:  #E0E0E0;   /* 分隔线、网格线 */
  --track: #EFEFEF;   /* 进度轨底、刻度底 */
  --red:   #E30613;   /* 唯一彩色：瑞士红 */
}
```

纪律：`--red` 全站出现 3 次——进度填充、当前阶段点、区块序号底色。除此之外一律黑白灰。

### 1.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

| 用途 | 字体 | 说明 |
|:---|:---|:---|
| 拉丁标题 / 数字 / 标签 | Inter 700/800 | Helvetica 的 Google 平替；标签类全大写 + `letter-spacing: .2em` |
| 中文标题 / 正文 | Noto Sans SC 700 / 400 | 中文不用大写字距，`letter-spacing: .04em` 即可 |

字号阶梯（强对比是灵魂）：区块拉丁标题 48 / Hero 名 72 / 卡片标题 20 / **正文 14** / 标签 11；平板 Hero 52 / 手机 36，区块标题手机 30。

### 1.3 网格（本风格的核心组件）

```css
.section { max-width: 1080px; margin: 0 auto; padding: 96px 24px;
  display: grid; grid-template-columns: repeat(12, 1fr); column-gap: 24px; }
.sec-head  { grid-column: 1 / 5; }     /* 标题占左 4 列 */
.sec-body  { grid-column: 5 / 13; }    /* 内容占右 8 列 */
.works     { grid-column: 1 / 13; display: grid;
             grid-template-columns: repeat(3, 1fr); gap: 24px; }
```

- 标题与内容左右分栏、顶部基线对齐——瑞士式的非对称平衡
- 959px 档：`.sec-head / .sec-body` 均改 `grid-column: 1 / 13` 上下堆叠；639px 档：column-gap 16px、`.section` padding 64px 16px

### 1.4 组件规范

**「正在学」进度条（直角红尺）**：

```css
.track { height: 8px; background: var(--track); border-radius: 0; }
.fill  { height: 100%; width: 39%; background: var(--red); border-radius: 0; }
```

- 无圆角、无渐变、无阴影；天数 `D11/28` Inter 700 18px `--ink`，右对齐于标签行
- **阶段刻度**：方点 `10px × 10px` 无圆角，未达 `--track` 实填，当前 `--red` 实填；连线 `1px solid var(--line)`，已过段 `1px solid var(--ink)`；阶段名 11px Inter 700 大写 `.2em`，当前名 `--ink`，未达名 `--gray`

**作品卡**：

```css
.work-card {
  background: var(--paper); border: 1px solid var(--line); border-radius: 0;
  border-top: 3px solid transparent;      /* 预留 hover 红条位置，防抖动 */
  padding: 24px 24px 20px;
  transition: border-color .2s ease;
}
.work-card:hover { border-color: var(--ink); border-top-color: var(--red); }
```

- 结构：序号 Inter 800 12px `--red`（`01 / 02 / 03`，无胶囊无底）→ 标题 20px 700 → 描述 14px `--gray` → 底部 `1px solid var(--line)` + 标签行（Inter 11px 大写 .2em `--gray`）+ `→`（hover 右移 4px）
- 禁阴影、禁圆角、禁位移——hover 只变色

**区块标题/序号**：序号 `01` Inter 800 48px `--red`；标题拉丁全大写 Inter 800 48px `.2em`（中文标题 Noto Sans SC 700 40px），两者左对齐同一基线。

**页脚**：`border-top: 1px solid var(--line)`，11px Inter 大写 `.2em` `--gray`，居中，padding 40px 24px。

### 1.5 Hero 3D 场景（网格坐标场 · 唯一红立方）

- 元素：
  - 网格：`GridHelper(10, 10, 0x111111, 0xE0E0E0)`（中轴线墨、其余浅灰），置于 `y = -1.2`
  - 红立方：`BoxGeometry(1, 1, 1)` + `MeshBasicMaterial({ color: 0xE30613 })`，放在网格面上（中心 `y = -0.7`）
  - 可选副元素：1 根 `LineSegments` 竖直标尺线（`0x111111`，高 3）立在原点
- 相机 `(5.5, 4.5, 7)`，`lookAt(0, -0.5, 0)`；OrbitControls `autoRotateSpeed 0.3`（全批最慢，瑞士是静的），禁缩放平移
- 动效：红立方沿网格 X 轴 `x = sin(t * .25) * 3` 缓慢往返（像光标扫过坐标纸）；无灯光（全部 Basic 材质）
- Hero 底：`--paper` 纯白，renderer `alpha: true`
- reduced-motion：立方停在 `x = 0`，关 autoRotate

### 1.6 动效

- 全部 `power2.out`，时长 ≤0.5s，只动 `opacity` + `y:12→0`；禁 back/elastic、禁旋转
- 进度条生长 0.8s `power2.out` + count-up 同步；无弹性
- 克制点：**动效幅度全批最小——精确感来自静止，不来自动**

---

## 2. 风格二：包豪斯 Bauhaus（demo-h）

灵感：Prompt 库 #8——红黄蓝三原色、圆/方/三角几何构成、Futura 系字体、直角无圆角、形式追随功能。

### 2.1 色板

```css
:root {
  --paper: #F4F1EA;   /* 页面底：微暖纸白（纯白太冷，纸白更接近包豪斯印刷品） */
  --card:  #FFFFFF;
  --ink:   #1A1A1A;
  --gray:  #8A8A8A;
  --red:   #E94B3C;
  --yellow:#F2C94C;
  --blue:  #2F80ED;
}
```

纪律：三原色每屏各出现 ≤1 次（例如「正在学」屏：红=进度填充、黄=当前阶段点、蓝=作品卡色条之一——已满，其余全墨/纸）。与孟菲斯的区别：孟菲斯 4 色 pastel + 墨描边 + 硬投影；包豪斯 3 原色实填 + 无描边无投影 + 直角。

### 2.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
```

| 用途 | 字体 | 说明 |
|:---|:---|:---|
| 拉丁标题 / 数字 / 标签 | Jost 600/700 | Futura 的 Google 平替（几何无衬线） |
| 中文标题 | Noto Sans SC 900 | |
| 正文 | Noto Sans SC 400/500 | |

字号阶梯：Hero 名 76 / 区块标题 34 / 卡片标题 21 / 正文 15 / 标签 12；平板 54 / 手机 38，区块标题手机 26。

### 2.3 组件规范

**「正在学」进度条（原色尺）**：

```css
.track { height: 12px; background: var(--card); border-radius: 0; }
.fill  { height: 100%; width: 39%; background: var(--blue); border-radius: 0; }
```

- 无描边无阴影；天数 `D11/28` Jost 700 18px `--ink`
- **阶段刻度（圆·方·三角，本风格签名组件）**：三个阶段各配一个几何形，14px，未达=纸白实填、当前=原色实填：
  - 阶段 1 圆：`border-radius: 50%`，当前填 `--red`
  - 阶段 2 方：直角，当前填 `--yellow`
  - 阶段 3 三角：`clip-path: polygon(50% 0, 100% 100%, 0 100%)`，当前填 `--blue`
  - 连线 `3px solid var(--ink)`；阶段名 13px，当前名 700 `--ink`，未达 `--gray`

**作品卡**：

```css
.work-card {
  background: var(--card); border: none; border-radius: 0;
  padding: 28px 24px 22px; position: relative;
  transition: transform .25s ease;
}
.work-card::before {           /* 顶部色条：三张卡依次红/黄/蓝 */
  content: ''; position: absolute; top: 0; left: 0;
  width: 64px; height: 8px; background: var(--red);   /* 第 2/3 张改 --yellow / --blue */
}
.work-card:hover { transform: translateY(-4px); }
```

- 结构：序号 Jost 700 13px `--gray`（`No.01`）→ 中文标题 900 21px → 描述 14px `--gray` → 底部 `3px solid var(--ink)` 分隔 + 标签 + `→`
- 禁描边禁投影（包豪斯层次靠色块与留白，不靠边线）；hover 只位移

**区块标题/序号**：序号放大几何形——`01` 配 16px 红圆、`02` 配 16px 黄方（Jost 700 数字叠在形旁），标题 Jost 700 34px；标题正下方一排小几何（圆/方/三角各 10px，红黄蓝，间距 8px）作为本风格唯一装饰。

**页脚**：顶部 4px 高三原色等分条 + 12px Jost 文本：

```css
.footer-note { border-top: 4px solid;
  border-image: linear-gradient(90deg, var(--red) 0 33.3%, var(--yellow) 33.3% 66.6%, var(--blue) 66.6% 100%) 1; }
```

### 2.4 Hero 3D 场景（正交平面构成 · 圆方三角叠压）

与孟菲斯的关键区别：**正交相机 + 纯 2D 形 + 无描边无灯光**，像一张会呼吸的包豪斯海报。

- 相机：`OrthographicCamera`（`frustumSize 6`，`left/right/top/bottom` 按 aspect 算），位置 `(0, 0, 10)` 正视，不开 OrbitControls 旋转（海报不可转），只保留 `touch-action` 与禁用缩放
- 元素（全部 `MeshBasicMaterial`，无灯光）：
  - 红圆盘：`CircleGeometry(1.5, 48)` 色 `0xE94B3C`，位置 `(-1.1, 0.3, 0)`
  - 蓝方块：`PlaneGeometry(1.9, 1.9)` 色 `0x2F80ED`，位置 `(0.9, -0.5, 0.1)`（z 略前，叠压圆盘边缘）
  - 黄三角：`CircleGeometry(1.1, 3)` 色 `0xF2C94C`，位置 `(0.2, 1.3, 0.2)`，`rotation.z = .3`
  - 墨细线 2 根：`PlaneGeometry(4.6, .06)` 色 `0x1A1A1A`，横竖各一，做构成骨架，z 最后
- 动效：整体 group `rotation.z = sin(t * .2) * .03` 极慢呼吸；三形各自 `position.y` ±0.08 正弦错位漂移
- Hero 底：`--paper` 纸白，renderer `alpha: true`
- 移动端：三形 `scale .8` 居中，不删减

### 2.5 动效

- 入场：`opacity 0→1` + `y:20→0`，0.6s `power3.out`，stagger .08；禁弹性
- 进度条生长 0.9s `power3.out`；阶段几何点 `scale 0→1` `power2.out`（不用 back，包豪斯不弹）
- hover 全部 transition ≤.25s
- 克制点：**三原色是唯一的装饰，动效不许再加戏**

---

## 3. 风格三：玻璃拟态 Glassmorphism（demo-i）

灵感：Prompt 库 #3——深色底 + 流动渐变光斑 + `backdrop-filter: blur(20px)` 毛玻璃卡片。铁律：**背景要暗，玻璃才显透**。

### 3.1 色板

```css
:root {
  --bg:        #14122B;  /* 页面底：深紫黑（光斑之外的区域也够暗） */
  --glow-1:    #667eea;  /* 光斑①：蓝 */
  --glow-2:    #764ba2;  /* 光斑②：紫 */
  --glow-3:    #f093fb;  /* 光斑③：粉（仅 Hero 3D 用） */
  --glass:     rgba(255,255,255,.08);   /* 玻璃面 */
  --glass-brd: rgba(255,255,255,.18);   /* 玻璃 1px 边 */
  --text:      #F2F3FF;
  --text-dim:  rgba(235,238,255,.6);
  --accent:    #A8BFFF;  /* 强调：浅蓝（文字/当前态） */
}
```

### 3.2 页面基底（玻璃感的前提）

```css
body { background: var(--bg); color: var(--text); }
.glow { position: fixed; border-radius: 50%; filter: blur(90px); z-index: -1; pointer-events: none; }
.glow.g1 { width: 44vw; height: 44vw; background: var(--glow-1); opacity: .5; top: -10vw; left: -8vw; }
.glow.g2 { width: 38vw; height: 38vw; background: var(--glow-2); opacity: .45; bottom: 5vh; right: -6vw; }
```

- 固定定位大光斑 2 个（+ Hero 3D 里 1 个粉色球 = 全站光斑 3 个，满额）
- <640px：`.glow` 只保留 g1，`filter: blur(60px)`，opacity 降 .35

### 3.3 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

Inter 600/700 拉丁标题数字；Noto Sans SC 中文。字号：Hero 名 68 / 区块标题 32 / 卡片标题 20 / 正文 15 / 标签 12；平板 48 / 手机 34。

### 3.4 组件规范

**玻璃工具类（所有玻璃容器共用）**：

```css
.glass {
  background: var(--glass);
  backdrop-filter: blur(20px) saturate(140%);
  -webkit-backdrop-filter: blur(20px) saturate(140%);
  border: 1px solid var(--glass-brd);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,.24);
}
```

**「正在学」进度条**：

```css
.track { height: 12px; border-radius: 999px; background: rgba(255,255,255,.1);
         border: 1px solid var(--glass-brd); }
.fill  { height: 100%; width: 39%; border-radius: 999px;
         background: linear-gradient(90deg, var(--glow-1), #A78BFA);
         box-shadow: 0 0 12px rgba(102,126,234,.55); }
```

- 天数 Inter 600 18px `--accent`
- **阶段刻度**：圆点 14px，未达 `rgba(255,255,255,.1)` + 1px `--glass-brd` 边；当前点 `background: linear-gradient(135deg, var(--glow-1), var(--glow-2))` + `box-shadow: 0 0 10px rgba(102,126,234,.6)`；连线 2px `rgba(255,255,255,.15)`；阶段名 12px `--text-dim`，当前名 `--text` 600

**作品卡**：`.glass` + `padding: 26px 24px 22px`；hover `transform: translateY(-4px); border-color: rgba(255,255,255,.35);`（transition .3s ease）。

- 结构：序号 Inter 600 12px `--accent`（`01 →`）→ 标题 20px 700 `--text` → 描述 14px `--text-dim` → 底部 `1px solid var(--glass-brd)` + 标签 + `→`
- **禁玻璃叠玻璃**：卡片内的标签不再给玻璃底，纯文字

**区块标题/序号**：序号 Inter 700 13px `--accent` + `·`；标题 32px 700 `--text`；标题下一条 40px × 3px 渐变线（`--glow-1 → --glow-2`，圆角 2px）。

**页脚**：`border-top: 1px solid var(--glass-brd)`，12px `--text-dim`，居中。

### 3.5 Hero 3D 场景（漂移渐变球群 + CSS 毛玻璃文字面板）

玻璃感由 **CSS `backdrop-filter`** 完成（WebGL 做毛玻璃成本高且没必要），3D 只负责提供"玻璃后面的流动色彩"：

- 元素：3 个大球 `SphereGeometry(1.4, 48, 32)`，`MeshBasicMaterial` 色 `0x667eea / 0x764ba2 / 0xF093FB`，位置呈三角分布 `(±1.8, ±0.8, 0)`
- 动效：每球 `position` 沿各自相位正弦漂移（幅度 ±0.5，周期 6–9s），不旋转不形变——像失焦的霓虹灯球
- 相机 `(0, 0, 6)` 固定，**不用 OrbitControls**（玻璃风不打断沉浸）；鼠标视差：`camera.position.x/y` 向 `mouseX * .3` lerp（系数 .04），手机无视差
- Hero 文字面板：`.hero-overlay` 内包一个 `.glass` 面板（padding 40px 48px），毛玻璃直接糊在 3D 球群上——这就是"玻璃显透"的瞬间
- Hero 底：`--bg`，renderer `alpha: true`；3D 之外 Hero 四角补 2 个 CSS `.glow` 光斑增强
- 移动端：球 3→2 个（去掉粉球）；`blur(20px)` 降 `blur(12px)`（backdrop-filter 在低端机掉帧）
- reduced-motion：球静止在初始位，视差关闭

### 3.6 动效

- 入场 `opacity` + `y:24→0`，0.8s `power3.out`；进度条生长 1.1s
- Hero 面板 `scale .96→1` + 淡入 0.9s（玻璃浮现）
- 克制点：**全站只有"浮现"一种动效语法，禁弹禁转——玻璃是静的**

---

## 4. 风格四：新拟态 Neumorphism（demo-j）

灵感：Prompt 库 #12——浅灰单色系、凸起/凹陷双阴影、圆角 16–20px、无硬边框。口诀：**左上白，右下黑**。

### 4.1 色板（单色系）

```css
:root {
  --bg:      #E0E5EC;   /* 页面底 = 卡片底 = 一切底（同色是新拟态的前提） */
  --hi:      #FFFFFF;   /* 左上亮影 */
  --lo:      #B8BFC9;   /* 右下暗影 */
  --text:    #4A5568;   /* 正文（不得再浅，保对比度） */
  --dim:     #8A97A8;   /* 次级文字（仅用于 ≥14px 文本） */
  --accent:  #6D8EF0;   /* 唯一彩色：柔和蓝 */
}
```

阴影令牌：

```css
:root {
  --raise: -6px -6px 12px var(--hi),  6px 6px 12px var(--lo);        /* 凸起 */
  --sink:  inset -4px -4px 8px var(--hi), inset 4px 4px 8px var(--lo); /* 凹陷 */
}
```

### 4.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

Nunito 700/800 拉丁数字标签（圆润配软 UI）；Noto Sans SC 中文。字号：Hero 名 66 / 区块标题 30 / 卡片标题 20 / 正文 15 / 标签 12；平板 46 / 手机 32。

### 4.3 组件规范

**「正在学」进度条（凹槽嵌凸条）**：

```css
.track { height: 16px; border-radius: 999px; background: var(--bg);
         box-shadow: var(--sink); padding: 3px; }
.fill  { height: 100%; width: 39%; border-radius: 999px; background: var(--accent);
         box-shadow: 2px 2px 5px var(--lo); }
```

- 天数 Nunito 800 18px `--accent`
- **阶段刻度**：圆钮 18px，未达=凹陷（`background: var(--bg); box-shadow: var(--sink)`），当前=凸起蓝（`background: var(--accent); box-shadow: var(--raise)`）；连线 6px 胶囊 `--bg` + `box-shadow: var(--sink)`；阶段名 13px，当前名 `--accent` 700

**作品卡（凸起 → 按下变凹陷，本风格签名交互）**：

```css
.work-card {
  background: var(--bg); border: none; border-radius: 20px;
  padding: 28px 26px 24px; box-shadow: var(--raise);
  transition: box-shadow .2s ease, transform .2s ease;
}
.work-card:hover { box-shadow: var(--sink); transform: scale(.99); }
```

- 结构：序号 Nunito 800 13px `--accent`（`01.`）→ 标题 700 20px → 描述 14px `--dim` → 底部无分隔线（用 12px 高凹陷细槽代替：`height: 2px; border-radius: 2px; background: var(--bg); box-shadow: var(--sink)`）+ 标签 + `→`
- 卡片内的序号胶囊/标签若要用底，一律凹陷；同一张卡上凸起元素 ≤1 个

**区块标题/序号**：序号放在 44px 凸起圆钮里（Nunito 800 15px `--accent`）；标题 Noto Sans SC 700 30px `--text`。

**页脚**：顶部 2px 凹陷槽分隔，12px `--dim` 居中。

### 4.4 Hero 3D 场景（软灰丘陵 · 同色软阴影）

- 元素：3 个压扁球 `SphereGeometry(1.6, 48, 32)`，`scale(1, .42, 1)`，`MeshStandardMaterial({ color: 0xE0E5EC, roughness: .9, metalness: 0 })`，位置错开 `(0,0,0) / (2.2,-.1,.8) / (-2.1,-.05,-.6)`；全部 `castShadow + receiveShadow`
- 地面：`PlaneGeometry(30, 30)` 同色 `0xE0E5EC`，`receiveShadow`，`y = -0.75`——丘陵影子落在同色地面上，就是 3D 版"左上白右下黑"
- 灯光：`HemisphereLight(0xffffff, 0xcfd6e0, .9)` + `DirectionalLight(0xffffff, 1.6)` 位置 `(4, 7, 3)`，`castShadow`，`shadow.mapSize 1024`，`renderer.shadowMap.type = THREE.PCFSoftShadowMap`（软边阴影是灵魂）
- 动效：三球 `scale.y` 在 `.38–.48` 间慢呼吸（相位各差 2π/3），不起伏位置
- 相机 `(0, 3.4, 6.2)`，`target(0,0,0)`，`autoRotateSpeed 0.4`；Hero 底 `--bg`，renderer `alpha: false` 直接 `setClearColor(0xE0E5EC)`（页面与场景同色无缝）
- 移动端：球细分降 24；阴影 mapSize 512
- reduced-motion：呼吸停在中位，关 autoRotate

### 4.5 动效

- 入场 `opacity` + `y:18→0`，0.7s `power2.out`；禁弹性（软 ≠ 弹）
- 进度条生长 1s `power2.out`；阶段当前钮 `scale .6→1` 0.5s `power2.out`
- 克制点：**全站只有凸起和凹陷两种状态，彩色只有一个蓝——每屏蓝色 ≤2 处**

---

## 5. 风格五：Y2K / Frutiger Aero（demo-k）

灵感：Prompt 库 #11——蓝天白云、光泽半透明、气泡、水感玻璃（比玻璃拟态更"塑料高光"）。

### 5.1 色板

```css
:root {
  --sky:      #87CEEB;   /* 天蓝主色 */
  --sky-deep: #4FA8D8;   /* 天蓝深档（渐变、强调 hover） */
  --sky-pale: #EAF6FC;   /* 页面底：极浅蓝白 */
  --white:    #FFFFFF;
  --silver:   #C9D4DD;   /* 银灰：边框、刻度 */
  --ink:      #1C3D52;   /* 深蓝黑：正文（不用纯黑，水感更透） */
  --dim:      #5B7A8F;   /* 次级文字 */
  --accent:   #3B9CD6;   /* 强调蓝 */
}
```

### 5.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

Baloo 2 700/800 拉丁标题数字（2000 年代圆润亲和）；Noto Sans SC 中文。字号：Hero 名 70 / 区块标题 32 / 卡片标题 21 / 正文 15 / 标签 12；平板 50 / 手机 36。

### 5.3 光泽工具写法（全站唯一一层高光）

```css
.glossy {
  background: linear-gradient(180deg, rgba(255,255,255,.85) 0%, rgba(255,255,255,.25) 45%, rgba(255,255,255,0) 100%);
  border: 1px solid rgba(255,255,255,.9);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.9), 0 4px 14px rgba(79,168,216,.25);
}
```

### 5.4 组件规范

**「正在学」进度条（水柱条）**：

```css
.track { height: 18px; border-radius: 999px; background: var(--white);
         border: 1px solid var(--silver); overflow: hidden; }
.fill  { height: 100%; width: 39%; border-radius: 999px; position: relative;
         background: linear-gradient(180deg, #A5DCF5 0%, var(--accent) 100%); }
.fill::before {  /* 顶部白色高光带：水感的唯一来源 */
  content: ''; position: absolute; top: 2px; left: 4px; right: 4px; height: 45%;
  border-radius: 999px; background: rgba(255,255,255,.55); }
```

- 天数 Baloo 2 800 18px `--accent`
- **阶段刻度（玻璃珠）**：圆点 16px，`background: radial-gradient(circle at 35% 30%, #fff 0%, #BFE3F5 45%, var(--sky) 100%)` + `border: 1px solid var(--silver)`；当前点把渐变终点换成 `--accent` + `box-shadow: 0 0 8px rgba(59,156,214,.5)`；连线 4px 胶囊 `var(--silver)`，已过段 `var(--sky)`；阶段名 13px `--dim`，当前名 `--accent` 700

**作品卡（水珠卡）**：

```css
.work-card {
  background: rgba(255,255,255,.6);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,.9); border-radius: 18px;
  padding: 26px 24px 22px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.9), 0 6px 18px rgba(79,168,216,.18);
  transition: transform .25s ease, box-shadow .25s ease;
}
.work-card::before {  /* 顶部高光带，每张卡都有 */
  content: ''; position: absolute; top: 0; left: 12px; right: 12px; height: 40%;
  border-radius: 18px 18px 0 0; pointer-events: none;
  background: linear-gradient(180deg, rgba(255,255,255,.7), rgba(255,255,255,0));
}
.work-card:hover { transform: translateY(-5px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.9), 0 12px 26px rgba(79,168,216,.3); }
```

- `overflow: hidden` 别忘了加（高光带要裁进圆角）
- 结构：序号 Baloo 2 800 13px `--accent`（`01`）→ 标题 700 21px `--ink` → 描述 14px `--dim` → 底部 `1px solid var(--silver)` + 标签 + `→`
- 卡片右上装饰：`✦` 字符 16px `--sky`（装饰配额 1/2，另一个是 Hero 3D 里的气泡）

**区块标题/序号**：序号 Baloo 2 800 14px 白字，放在 `radial-gradient(circle at 35% 30%, #fff, var(--accent))` 36px 玻璃珠圆里；标题 Baloo 2 700 32px `--ink`。

**页脚**：顶部 SVG 白浪分隔线（`viewBox="0 0 1440 60"` 单条正弦波，填 `--white`，置于 `background: linear-gradient(180deg, var(--sky-pale), var(--sky))` 的页脚区上缘），12px `--dim`。

### 5.5 Hero 3D 场景（气泡上升）

- 背景：Hero 底 `linear-gradient(180deg, #BDE5F9 0%, var(--sky) 55%, var(--sky-pale) 100%)`，renderer `alpha: true`
- 元素：气泡 14 个（手机 8 个），`SphereGeometry(r, 24, 18)`，`r` 随机 .12–.5，`MeshPhongMaterial({ color: 0xDFF2FB, transparent: true, opacity: .32, shininess: 120, specular: 0xFFFFFF })`——Phong 高光点就是塑料水珠感
- 动效：每泡 `y` 从 -4 匀速升到 +4.5 后回底循环，速度 .15–.45 随机，`x` 附加 `sin(t + phase) * .2` 摆动；不旋转
- 点缀：四角星 3 颗（`ShapeGeometry` 自绘十字星或直接 `✦` 纹理 Sprite），白色 opacity .8，`scale` 在 .8–1.2 慢闪烁
- 灯光：`HemisphereLight(0xffffff, 0x87CEEB, 1.1)` + `DirectionalLight(0xffffff, 1.2)` 位置 (3, 5, 4)
- 相机 `(0, 0, 6.5)` 固定，不用 OrbitControls（气泡会自动动，交互配额留给鼠标视差：`camera.position.x` 向 `mouseX * .25` lerp）
- reduced-motion：气泡静止散布，视差关闭

### 5.6 动效

- 入场 `opacity` + `y:22→0` + `scale .98→1`，0.7s `power3.out`
- 进度条生长 1s `power2.out`；天数 count-up 1.2s
- Hero 名可用 `back.out(1.4)` 轻弹（Y2K 允许一点俏皮，但只此一处）
- 克制点：**高光只有一层（45% 顶部白），蓝天白云只给 Hero——正文区块统一 `--sky-pale` 收住**

---

## 6. 风格六：酸性设计 Acid（demo-l）

灵感：Prompt 库 #10——深底 + 霓虹粉紫绿液态渐变、铬金属、尖锐黑体、层叠遮挡排版。

### 6.1 色板

```css
:root {
  --bg:     #0B0B0F;   /* 页面底：近黑 */
  --panel:  #131318;   /* 卡片底 */
  --pink:   #FF3CAC;   /* 霓虹粉 */
  --purple: #784BA0;   /* 霓虹紫 */
  --green:  #2BFF88;   /* 青绿 */
  --text:   #EDEDF2;
  --dim:    #8B8B96;
  --line:   rgba(255,255,255,.12);
}
/* 铬渐变（文字/边框用，不可做 background-clip 以外的滥用） */
--chrome: linear-gradient(180deg, #F5F5F7 0%, #9A9AA5 45%, #E8E8EC 60%, #6E6E78 100%);
```

纪律：霓虹三色只出现在——① 3D 场景灯光、② 液态渐变条（进度填充/卡片顶条）、③ 当前态光晕。其余一切黑灰铬。

### 6.2 字体

```html
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=ZCOOL+QingKe+HuangYou&family=Noto+Sans+SC:wght@400;500&display=swap" rel="stylesheet">
```

| 用途 | 字体 | 说明 |
|:---|:---|:---|
| 拉丁标题 / 数字 | Orbitron 700/900 | 酸性标配几何科技体 |
| **中文标题** | ZCOOL QingKe HuangYou | 尖锐油墨黑体，Google Fonts 上最接近酸性中文的方案，只有 400，禁加粗 |
| 正文 | Noto Sans SC 400/500 | 保可读性 |

字号：Hero 名 64（Orbitron 900，`.06em` 字距）/ 区块中文标题 40 / 卡片标题 22 / 正文 15 / 标签 11（Orbitron `.2em`）；平板 46 / 手机 32。

### 6.3 组件规范

**「正在学」进度条（液态金属管）**：

```css
.track { height: 10px; background: var(--panel); border: 1px solid var(--line); border-radius: 2px; }
.fill  { height: 100%; width: 39%; border-radius: 2px;
         background: linear-gradient(90deg, var(--pink), var(--purple), var(--green));
         background-size: 200% 100%;
         animation: liquid 3s linear infinite; }   /* 流动；reduced-motion 时被 §0.2 关停 */
@keyframes liquid { to { background-position: 200% 0; } }
```

- 天数 Orbitron 700 16px `--pink`
- **阶段刻度（铬珠）**：圆点 14px，`background: conic-gradient(from 210deg, #F5F5F7, #9A9AA5, #E8E8EC, #6E6E78, #F5F5F7)` + `border: 1px solid var(--line)`；当前点加 `box-shadow: 0 0 12px var(--pink)`；连线 1px `--line`，已过段 1px `--dim`；阶段名 11px Orbitron `.2em` `--dim`，当前名 `--text`

**作品卡**：

```css
.work-card {
  background: var(--panel); border: 1px solid var(--line); border-radius: 4px;
  padding: 26px 24px 22px; position: relative;
  transition: transform .2s ease, border-color .2s ease;
}
.work-card::before {  /* 顶部 3px 液态渐变条 */
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--pink), var(--purple), var(--green));
}
.work-card:hover { transform: translateY(-3px); border-color: var(--pink); }
```

- 结构：序号 Orbitron 700 11px `--dim`（`#01`）→ 中文标题 QingKe HuangYou 22px `--text` → 描述 14px `--dim` → 底部 `1px solid var(--line)` + 标签（Orbitron 10px `.2em` `--dim`）+ `→`（hover 转 `--pink`）
- 可选铬字：卡片序号用 `background: var(--chrome); -webkit-background-clip: text; color: transparent;`——三张卡统一用或统一不用

**区块标题/序号（层叠遮挡，本风格签名）**：

```css
.sec-title { position: relative; font-family: 'ZCOOL QingKe HuangYou'; font-size: 40px; color: var(--text); }
.sec-title::before {  /* 背后放大的描边幻影字 */
  content: attr(data-ghost); position: absolute; left: -8px; top: -14px; z-index: -1;
  font-size: 64px; color: transparent;
  -webkit-text-stroke: 1px rgba(255,60,172,.35); white-space: nowrap;
}
```

- 每个区块标题加 `data-ghost="正在学"` 等属性即自动生效；序号 Orbitron 900 13px `--pink`（`01 /`）

**页脚**：`border-top: 1px solid var(--line)`，11px Orbitron `.2em` `--dim`，居中。

### 6.4 Hero 3D 场景（铬环面结 · 霓虹边光）

- 元素：`TorusKnotGeometry(1.3, .42, 220, 32)` + `MeshStandardMaterial({ color: 0xFFFFFF, metalness: 1, roughness: .12 })`
- **铬质感关键**：必须给 envMap，否则金属是全黑。用 three 自带环境（importmap 已映射 `three/addons/`）：

```js
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), .04).texture;
```

- 霓虹边光：`PointLight(0xFF3CAC, 30)` 位置 `(-4, 2, 3)` + `PointLight(0x2BFF88, 20)` 位置 `(4, -2, 2)`——两盏灯在铬面上拉出粉/绿反射，这是酸性感的来源
- 动效：`rotation.x = t * .15`、`rotation.y = t * .22` 慢转
- 相机 `(0, 0, 5.2)`；OrbitControls `autoRotateSpeed 0.6`，禁缩放平移
- Hero 底：`--bg` 纯黑 + 一层极淡噪点（可选：`repeating-conic-gradient(rgba(255,255,255,.015) 0 .0001%, transparent 0 .0002%)`，`background-size: 180px`）
- 移动端：`TorusKnotGeometry(1.3, .42, 120, 20)`；`setPixelRatio(Math.min(devicePixelRatio, 1.5))`（金属 + envMap 是全批最重的场景，降一档保帧）
- reduced-motion：停止自转，关 autoRotate，灯光保留（静态铬也成立）

### 6.5 动效

- 入场：`opacity` + `y:26→0`，0.6s `power3.out`，stagger .07
- Hero 名逐字符 `clipPath` 由下往上刷出（`inset(100% 0 0 0) → inset(0)`），0.5s stagger .04——比弹性更符合酸性
- 进度条生长 1s + 液态流动常驻；glitch（若加）只给 Hero 名一次入场：3 帧位移 ±3px，`steps(1)`
- 克制点：**霓虹只勾边不铺面——大面积永远是黑灰铬**

---

## 7. 实现难度与选择建议

| 风格 | 实现难度 | 风险点 | K3 备注 |
|:---|:---|:---|:---|
| 瑞士国际主义 | ★ 最低 | 几乎没有；难在"精确"——间距歪 2px 就破功 | 最耐看、最像"数字花园长出来之前的测量图纸" |
| 包豪斯 | ★★ | 正交相机参数；禁描边后层次全靠色块，间距要大胆 | 与「学习者」人设气质契合 |
| 玻璃拟态 | ★★ | `backdrop-filter` 需 `-webkit-` 前缀；低端机掉帧 | 最"科技产品"，但与其它 5 个比略显常见 |
| 新拟态 | ★★ | 对比度（正文色别再浅）；同色页面分区全靠阴影 | 交互（按下凹陷）最有趣 |
| Y2K | ★★★ | 高光层次多，CSS 量最大 | 最怀旧亲切，适合个人主页 |
| 酸性设计 | ★★★ | envMap 依赖 `RoomEnvironment`；中文黄山体气质两极 | 最出挑，但与"财经/书法"内容反差最大 |

## 8. 给实现者的统一提醒

1. 骨架 HTML 从 `demo-d.html` 复制：区块结构、GSAP 部分（含 `reduceMotion` 检查、`touchAction = 'pan-y'` 一行）、importmap 全部保留，只换 `:root` 色板、组件 CSS、字体 link 与 3D 模块
2. 作品卡放 3 张（财经知识卡片 / 书法练习打卡 / Obsidian LLM-Wiki），文案照 demo-d
3. 每个 demo 自查三件事：手机 <640px 首屏能否纵向滚动（touch-action）、`Cmd+Shift+R` 强制刷新后 reduced-motion 模拟下无循环动画、键盘 Tab 到作品卡有 `:focus-visible` 描边
4. 6 个 3D 场景互不重复：网格红立方（瑞士）/ 正交圆方三角（包豪斯）/ 漂移光球+CSS 毛玻璃（玻璃）/ 同色软丘陵（新拟态）/ 上升气泡（Y2K）/ 铬环面结（酸性）；与 v2.0 已用场景（小岛/孟菲斯几何组/像素方块/呼吸 blob）也不重复
5. 各风格"一句话克制点"汇总在 §0.4，实现完逐条自查

## 9. 待 Charlotte 拍板

1. 6 选 1（或与 v2.0 四风格混选）作为整站定稿
2. 酸性/瑞士两版的中文标题气质差异大（黄山体 vs 黑体），建议先看 demo 再定
3. 若定瑞士或包豪斯，Hero 的 `↻ 拖拽玩玩` 便签建议删（两风格都不该有贴纸感元素）
