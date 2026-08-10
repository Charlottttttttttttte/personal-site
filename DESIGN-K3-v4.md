# 个人网站 · 视觉/交互设计规范 v4.0（摩天轮综合页 · K3 交付）

> 状态：**K3 设计细化 v4.0**（2026-08-05）· 在 demo-i（孟菲斯 + 摩天轮）基础上升级为综合页
> 分工：本规范由 K3 编写，实现者照抄；色值、字号、布局算法、粒子参数均已给定，不需要再自由发挥。
> 引用关系（不重写，照抄原文件）：
> - 孟菲斯页面组件（正在学 / 作品卡 / 页脚）→ `DESIGN-K3-v2.md` §3（demo-i 已实现，保留）
> - 瑞士国际主义 → `DESIGN-K3-v3.md` §1；包豪斯 → v3 §2；Y2K/Frutiger Aero → v3 §5。本规范 §4/§5 只给压缩参数，完整参数回原文件查
> - 页面骨架 / GSAP 写法 / importmap → `demo-i.html` 直接扩展

---

## 0. 统一约定（全页适用，沿用 v2/v3 §0，此处只列增量）

- 断点、字体加载、`100svh`、`tabular-nums`、`:focus-visible`、reduced-motion 总开关、ScrollTrigger `start:'top 80%', once:true`、`touchAction='pan-y'` 一行——全部照 v3 §0，不改。
- **每屏主角动效 ≤1 分配表（本页全量，见 §1.3）**：这条是 v4 的新增纪律，因为本页区块多、风格多，最容易"每屏都在抢戏"。
- 各风格小节的可交互元素 `:focus-visible` 强调色：孟菲斯区 `--ink`；瑞士小节 `--red`（v3 §1 色板）；包豪斯小节 `--blue`（v3 §2）；Y2K 小节 `--accent`（v3 §5）。
- 数字花园区块的强调色新增一个：`--leaf: #7FB77E`（叶绿，来自 v2 §2 动森色板——治愈插画的绿色与它同源，全页只此一处引绿，见 §3.5）。

---

## 1. 整体页面编排

### 1.1 区块顺序与风格归属

| # | 区块 | 风格 | 状态 | 页面底色 |
|:--|:---|:---|:---|:---|
| ① | Hero 摩天轮 + 星空粒子 | 孟菲斯 | 保留 + 加粒子（§2） | 现有米白渐变（不变） |
| ② | 正在学 | 孟菲斯 | 保留 | `--paper` + 波点 |
| ③ | 作品集 3 卡 | 孟菲斯 | 保留 | `--paper` + 波点 |
| ④ | 数字花园 | **孟菲斯主线延续**（图谱）+ 瑞士小节 + 治愈插画 | 新增（§3） | `--paper`，波点**减半**（见 1.2） |
| ⑤ | 风格档案 | 包豪斯小节 + Y2K 小节并列 | 新增（§4） | `--paper`，无波点 |
| ⑥ | 页脚 | 孟菲斯 | 保留 | `--paper` |

序号沿用现有 `.sec-num` 体系：01 正在学 / 02 作品集 / **03 数字花园 / 04 风格档案**，黑底倾斜 + 错位阴影样式不变（风格小节的标题在区块内部另行处理，不占全页序号）。

### 1.2 区块间过渡（怎么切才不跳戏）

核心思路：**孟菲斯是全页"主线皮肤"，三个风格小节是"区块内部的展品"**——小节换肤，区块外壳（标题栏、底色、边距）不换。

1. **③ 作品集 → ④ 数字花园**：不换底色，只把波点底纹在 ④ 区块内减半密度与透明度（`background-size: 34px→52px`，波点色 `rgba(23,23,26,.14)→.08`），视觉上"从游乐场走进植物园"。数字花园的主角图谱本身仍是孟菲斯语言（墨边 + pastel + 硬投影），过渡天然平滑。
2. **④ 内部三小节之间**：用 `1px` 细线 + 96px 留白分隔，不用色带。瑞士小节自带灰调，与孟菲斯图谱的对比就是过渡本身；治愈插画（绿）放在瑞士小节之后，作为"从精确回到温柔"的收尾。
3. **④ → ⑤ 风格档案**：本页唯一一次"硬切换"的暗示——⑤ 区块标题栏的 `.sec-num` 错位阴影色从 `--pink` 换成 `--yellow`（只此一处），配合标题文案"风格档案"完成语义切换；底色仍不动。
4. **⑤ → ⑥ 页脚**：页脚样式不变。Y2K 小节是⑤的收尾，其蓝白调与页脚的米白墨线不冲突，直接收。

### 1.3 每屏主角动效 ≤1 分配表

| 屏 | 主角动效（唯一的"戏"） | 其余允许 |
|:--|:---|:---|
| ① Hero | 摩天轮转动 + 点击跳转（现有） | 星空粒子闪烁（算环境，见 §2 限制）、字符入场、SCROLL 箭头循环 |
| ② 正在学 | 进度条生长 + count-up（现有） | 阶段点弹入 |
| ③ 作品集 | 卡片入场 stagger（现有） | 按压 hover |
| ④a 知识图谱 | **无循环动效**——hover 高亮就是交互本身 | 入场 fade-up 一次 |
| ④b 瑞士小节 | 无（瑞士是静的，v3 §1.6） | 入场 fade-up 一次 |
| ④c 治愈插画 | 候鸟缓慢飘过（唯一循环，§3.5） | 无 |
| ⑤ 风格档案 | 无主角 | 两小节各自入场 fade-up 一次 |

---

## 2. Hero 星空粒子（在现有摩天轮场景里加 `THREE.Points`）

### 2.1 关键前提：Hero 底色是米白亮底，"星星"必须是深色的

现有 Hero 底是 `#FFF4DF → --paper` 的亮渐变，白色星星在上面不可见。参考素材"DNA 科技粒子"的观感是**稀疏的细小墨点 + 少量彩色点缓缓明灭**——在亮底上用深色粒子，成立且与孟菲斯墨线语言一致。**不改 Hero 底色，粒子配色如下。**

### 2.2 实现参数（照抄）

在 demo-i 的 three 模块里、创建 `park` 之后插入：

```js
// ---- 星空粒子：两层，亮底层上的"墨点星空" ----
const isMobileS = matchMedia('(max-width: 639px)').matches;
const STAR_N   = isMobileS ? 220 : 600;      // 粒子总数
const starGeo  = new THREE.BufferGeometry();
const pos = new Float32Array(STAR_N * 3);
const col = new Float32Array(STAR_N * 3);
const inkC   = new THREE.Color(0x17171A);
const pastel = [0xFF87AB, 0x6FB1FF, 0xFFD23F, 0x4ECDC4].map(c => new THREE.Color(c));
for (let i = 0; i < STAR_N; i++) {
  // 扁平椭球壳分布：半径 14–30，压扁 y（星星在摩天轮"天区"，不在脚下）
  const r = 14 + Math.random() * 16;
  const th = Math.random() * Math.PI * 2;
  const y = (Math.random() * .9 + .1) * 10 - 2;   // y ∈ [-2, 8]，偏上半空
  pos[i*3]   = Math.cos(th) * r;
  pos[i*3+1] = y;
  pos[i*3+2] = Math.sin(th) * r * .6 - 6;          // z 压扁并整体后置，远离相机(z≈7.6)
  // 80% 墨色小点，20% 取一个孟菲斯 pastel 色
  const c = Math.random() < .8 ? inkC : pastel[i % 4];
  col[i*3] = c.r; col[i*3+1] = c.g; col[i*3+2] = c.b;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(col, 3));
const starMat = new THREE.PointsMaterial({
  size: .09,                 // 世界单位；配合 sizeAttenuation
  sizeAttenuation: true,
  vertexColors: true,
  transparent: true,
  opacity: .55,              // 亮底上墨色点 .55 透明度刚好"有而不抢"
  depthWrite: false,
});
const stars = new THREE.Points(starGeo, starMat);
scene.add(stars);            // 加在 scene 不加在 park：拖拽转摩天轮，星空不转
```

动画循环内（现有 `setAnimationLoop` 里）加闪烁：

```js
if (!reduceMotion) {
  // 明灭：opacity 慢呼吸（不逐粒子闪，600 个逐粒子改色每帧是浪费；
  // 整层呼吸 + 粒子本身位置随机，观感已是"星星在闪"）
  starMat.opacity = .4 + Math.sin(spin * 2.1) * .15;   // 复用现有时钟 spin 不行，用 clock：
}
```

> 注意：`spin` 在悬停时会暂停，闪烁不该停。用 `clock.elapsedTime`（在 `getDelta()` 后可读）：
> `starMat.opacity = .4 + Math.sin(clock.elapsedTime * 1.6) * .15;`
> 另加一层极慢自转：`stars.rotation.y = clock.elapsedTime * .01;`（rad/s，几乎不可觉，只防"死图"感）。

### 2.3 纪律与降级

- **闪烁只有"整层 opacity 呼吸"一种**，禁逐粒子随机闪（噪）、禁拖尾、禁连线（DNA 参考里的连线会把这个亮底页面弄脏，只取"粒子"不取"连线"）。
- **reduced-motion**：`opacity` 固定 `.5`，`rotation.y` 不自转，粒子静止散布。
- **移动端**：数量 600→220，`size .09→.12`（数量少了，单点略大补存在感）；pixelRatio 沿用现有 `min(devicePixelRatio, 2)`。
- **只加在 Hero**：数字花园/风格档案一律不加粒子（决策 4）。
- 层级：`stars` 的 z 分布在 -6 附近、`depthWrite:false`，摩天轮始终画在星前；粒子不加进 `clickables`，不影响点击跳转的 raycast（`intersectObjects(clickables)` 本来只查轿厢，天然不干扰）。
- 配额核算：Hero 屏彩色元素 = 名字跳色(1) + 黄 tag(2) + teal 便签(3) 已满——粒子里的 pastel 点只占 20% 且 size .09，算"底纹"不算彩色块；若评审认为超编，把 pastel 比例降到 10%。

---

## 3. 数字花园区块（本规范核心交付）

### 3.1 区块标题与引导文案

```html
<section class="section garden" id="garden">
  <div class="sec-head">
    <span class="sec-num fun">03</span>
    <h2 class="sec-title fun">数字花园</h2>
  </div>
  <p class="garden-lede">
    我的 Obsidian LLM-Wiki 在持续生长：<b class="fun">476</b> 个来源 ·
    <b class="fun">1057</b> 页 · <b class="fun">321</b> 个概念，全部双向链接。
    下面是其中一角——把鼠标放上去，看看概念之间怎么连在一起。
  </p>
  ...
```

- `.garden-lede`：正文 15px，max-width 640px，`opacity .78`，`margin-bottom: 40px`；三个数字 Fredoka 700 18px `--pink`（tabular-nums 已有）。
- 区块容器 `.garden` 加底纹变化（§1.2.1）：`background-image: radial-gradient(rgba(23,23,26,.08) 2px, transparent 2.2px); background-size: 52px;`。

### 3.2 知识图谱组件（核心交付）

#### 3.2.1 渲染方案：**内联 SVG，不用 Canvas、不用 d3**

15 节点 + 20 边，SVG 完胜：DOM 节点天然支持 hover / focus / aria，CSS 直接控样式，无需额外库（页面只依赖 CDN three + GSAP 的纪律不破）。Canvas 2D 在此规模没有任何收益，还要手写命中检测，排除。

```html
<div class="graph-wrap">
  <svg id="kg" viewBox="0 0 1000 640" role="img"
       aria-label="知识图谱：15 个概念节点与 20 条双向链接，悬停查看摘要">
  </svg>
  <div class="kg-tip" id="kgTip" role="tooltip" hidden></div>
</div>
```

`.graph-wrap { position: relative; }`，SVG 宽 100% 自适应，`aspect-ratio: 1000 / 640`。

#### 3.2.2 数据内嵌方式

直接内嵌在 HTML（静态站、GitHub Pages、免一次请求）：

```html
<script type="application/json" id="kg-data">
{ "nodes": [...], "edges": [...] }   <!-- /tmp/wiki_subgraph.json 原样粘贴 -->
</script>
```

```js
const KG = JSON.parse(document.getElementById('kg-data').textContent);
```

数据实况（实现者须知，来自 wiki_subgraph.json）：

- 15 节点，其中 `core: true` 5 个：`3D互动网页`、`Agent-Orchestration`、`html-in-canvas`、`vibe-coding`、`响应式设计`。
- **图是两个不连通分量**——这是真实数据的性质，布局必须处理：
  - 分量 A（10 节点，网页/前端簇）：3D互动网页、创意编程、html-in-canvas、vibe-coding、prompt-engineering、personal-operating-system、响应式设计、Bootstrap、HTML模板、Tailwind-CSS
  - 分量 B（5 节点，Agent 簇）：Agent-Orchestration、AI-Agent-Architecture、Agent-Loop、Agent-Team、多Agent协作
- `summary` 字段有截断（约 60 字），浮层直接展示即可，省略号感正好暗示"还有全文"。

#### 3.2.3 布局算法（手写，不用 d3；确定性、可实现）

**规则一句话：按连通分量分簇 → 每簇核心节点均匀放内环 → 非核心节点放外环其邻居的角平分方向 → 两轮质心松弛去重叠。**

逐步算法（页面加载时跑一次，15 节点成本可忽略；用固定伪随机种子保确定性——其实本算法无随机，天然确定）：

```
输入：nodes[], edges[]；画布 W=1000, H=640，padding P=70
1. 找连通分量：并查集或 BFS。得到簇列表 clusters，按节点数降序。
2. 簇排布：n 个簇沿水平均分画布。簇 k 的圆心 Ck = (W*(k+0.5)/n, H*0.5)。
   本数据 n=2：A 簇圆心 (250, 320)，B 簇圆心 (750, 320)。
3. 簇内布局：
   R1 = min(簇宽, H) * 0.16   // 核心环半径（本数据 ≈ 90）
   R2 = R1 * 2.1              // 外环半径（≈ 190）
   a) 核心节点：均匀放内环。第 j 个核心角 θj = 2π·j/coreCount - π/2（从正上方起）。
      只有 1 个核心的簇（B）：放圆心。
      A 簇 4 个核心：上/右/下/左（θ = -90°, 0°, 90°, 180°）。
   b) 非核心节点 v：
      - 取 v 的所有邻居角度集合 N(v)（已定位节点的 atan2 角，相对簇心）
      - v 的方向 = N(v) 角度的矢量平均（把各角转单位向量相加再取角；
        避免 0°/360° 环绕问题，禁直接算术平均）
      - 位置 = Ck + R2 · (cos θv, sin θv)；若 v 无邻居（本数据没有），均匀补位。
4. 两轮松弛（去重叠，每轮全节点扫一遍）：
   for pass in 1..2:
     对每个非核心节点 v：v.pos = lerp(v.pos, 邻居质心, 0.35)，
     然后把 |v.pos - Ck| 重投影回 [R1*1.4, R2*1.15] 区间（保环形层次）
5. 最小间距分离：对所有节点对跑 25 轮——
   若 dist(a,b) < 92（见节点尺寸），沿连线各推开 (92-dist)/2。
   （核心节点也参与被推，推完即可，不回投影。）
6. 整体 fit：求全节点包围盒，等比缩放+平移进 [P, W-P]×[P, H-P]。
```

实现提示：第 3b 步的"邻居"用无向邻接（edges 虽写成 source/target，wiki 双向链接语义上是无向的，**连线画成无箭头纯线**，见 3.2.4）。

#### 3.2.4 节点与连线样式（孟菲斯语言）

```css
/* 连线：墨色纯线，无箭头（双向链接 = 无向） */
.kg-edge { stroke: var(--ink); stroke-width: 2; opacity: .28; }
.kg-edge.hi { stroke-width: 3; opacity: .9; }

/* 节点：白底墨边圆 + pastel 填色 + 硬投影（SVG filter 太贵，用错位圆做硬投影） */
.kg-node { cursor: pointer; }
.kg-node .shadow { fill: var(--ink); }                 /* 错位 4px 的实心圆 = 硬投影 */
.kg-node .dot { fill: #fff; stroke: var(--ink); stroke-width: 3; }
.kg-node.core .dot { stroke-width: 4; }
.kg-node text {
  font: 700 15px 'Noto Sans SC', sans-serif; fill: var(--ink);
  text-anchor: middle; pointer-events: none;
}
```

- 半径：**核心节点 34，普通节点 26**（第 3.2.3 节最小间距 92 由此得出：34+26+32 余量）。
- 硬投影：每个节点 = 两个圆，`.shadow` 圆 `cx+4, cy+4`，`.dot` 圆压其上——SVG 里表达孟菲斯硬投影的标准做法，比 `filter: drop-shadow` 便宜且风格准确。
- pastel 填色规则（彩色有编制）：填色按**簇**分，不按心情分——
  - A 簇（网页/前端）：`.dot` 填 `--blue`(#6FB1FF) 的 35% 透明版（`fill-opacity:.35`），核心节点 `.55`
  - B 簇（Agent）：填 `--teal`(#4ECDC4)，透明度同上
  - 核心节点外再加一圈 `stroke: var(--yellow)` 3px 的"光环圆"（r+7，`fill:none`）——5 个核心一眼可辨；黄环是本屏第 3 处彩色，满额
- hover / 高亮态：
  - 当前节点 `.dot` 填色 `fill-opacity` 升 `1`（实填）
  - 相邻节点与相连边加 `.hi`；**非相邻节点和边 opacity 降到 `.18`**（淡出背景，图谱阅读的标准手法）
  - 实现：纯 JS 切 class，transition 交给 CSS `.kg-node, .kg-edge { transition: opacity .18s ease; }`
- 节点标签：中文名直接显示（`3D互动网页` 等）；英文 id 长的（`AI-Agent-Architecture`）**显示截断为 14 字符 + …** 且 13px，全名进 tooltip 标题。标签放节点正下方 `dy = r + 18`。

#### 3.2.5 hover 摘要浮层

```css
.kg-tip {
  position: absolute; max-width: 300px; z-index: 5;
  background: var(--card); border: 3px solid var(--ink); border-radius: 14px;
  box-shadow: 5px 5px 0 var(--ink); padding: 14px 16px 12px;
  font-size: 13px; line-height: 1.65; pointer-events: none;   /* 不挡鼠标 */
}
.kg-tip b { display: block; font-size: 15px; margin-bottom: 4px; }
.kg-tip .kg-tip-tag {
  font-family: 'Fredoka'; font-size: 11px; color: var(--pink);
  letter-spacing: .08em;
}
```

- 定位：浮层出现在节点右上方（`left = nodePx.x + 20, top = nodePx.y - tipHeight - 12`）；节点在视图右 1/3 时翻到左侧（`left = nodePx.x - tipWidth - 20`）；上方放不下就翻下方。节点像素坐标由 SVG `getBoundingClientRect()` + viewBox 比例换算（`px = rect.left + (x/1000)*rect.width`，容器内则用相对坐标同理）。
- 内容：`<b>节点名</b>` + `<span class="kg-tip-tag">CORE CONCEPT</span>`（仅核心节点）+ summary 文本。
- 触发：`mouseenter`/`focus` 显示，`mouseleave`/`blur` 隐藏；隐藏用 `hidden` 属性，不做淡出动画（孟菲斯 hover 要快，≤.15s）。
- 触屏：第一次点按 = 显示该节点浮层；点按空白处 = 收起。无跳转（v1 图谱不挂外链，见 §6 待拍板）。

#### 3.2.6 移动端降级（<640px）

- SVG viewBox 不变、等比缩小即可，但：节点半径 34/26 → 26/20（改 JS 常量，`transform` 不用动），标签 15px → 12px。
- **非核心节点标签默认隐藏**（`.kg-node:not(.core) text { display:none }`），点按时随浮层出现——15 个标签挤在 390px 宽里不可读。
- 浮层 `max-width: 240px`，贴边时 `left/right` 最少留 12px。
- 触控目标：节点热区 = 透明扩大圆（`r+10` 的透明圆，hit area ≥ 36px，配合浮层文案可读，44px 硬指标在图谱这种密集组件上放宽到 36，记录在案）。
- 不做双指缩放/拖拽平移（`touch-action: pan-y` 默认即放行页面滚动，SVG 不劫持）。

#### 3.2.7 可访问性

- SVG 根 `role="img"` + `aria-label`（见 3.2.1）。
- 每个节点 `<g class="kg-node" tabindex="0" role="button" aria-label="概念：响应式设计，查看摘要">`，内部含 `<title>响应式设计</title>`。
- `:focus-visible`：`outline` 画不进 SVG 圆，用光环圆代——`.kg-node:focus-visible .dot { stroke: var(--pink); stroke-width: 5; }` 且同样弹出浮层（focus 触发与 hover 同一函数）。
- Tab 顺序 = JSON 节点顺序（核心 5 个在前，把 JSON 里 core 节点排序提前即可）。

### 3.3 瑞士小节：AI 工具收藏清单

内容（6 条，均出自她 llm-wiki 出现过的真实工具链）：

| # | 工具 | 一行说明 |
|:--|:---|:---|
| 01 | Obsidian | 数字花园本体，476 来源 1057 页的家 |
| 02 | Kimi Code | 主力编程搭子，本网站就是它帮忙搭的 |
| 03 | Cursor | AI 编辑器，vibe coding 入门工具 |
| 04 | edge-tts | 免费 TTS，给知识卡片配语音 |
| 05 | Claude / ChatGPT | 概念拆解与写作的第一读者 |
| 06 | Three.js + GSAP | 这个页面的摩天轮和动效 |

视觉压缩参数（**完整参数照抄 v3 §1，此处只给"缩成一个小版块"的差量**）：

- 容器：`.swiss-panel` 白底，`border: 1px solid #E0E0E0`（v3 `--line`），无圆角无阴影，`padding: 40px`（手机 24px 16px）。与外围孟菲斯区块的关系：它是"展品"，不倾斜、不贴纸、不硬投影。
- 小节标题：`TOOLS` Inter 800 20px 大写 `letter-spacing:.2em` + 中文副标"AI 工具收藏" Noto Sans SC 700 15px `#767676`；标题下方 24px 处一条 `1px solid #E0E0E0` 通栏线。
- 清单：每行 = 12 列网格（v3 §1.3 压缩版）：序号 Inter 800 12px `--red`(#E30613) 占 1 列｜工具名 Inter 700 15px `#111` 占 4 列｜说明 14px `#767676` 占 7 列；行高 44px，行间 `1px solid var(--line)`。
- **红色配额**：瑞士纪律"红色全站 3 次"在小节内换算为"每版块 1 次"——本小节红色只给序号列（6 个序号同属一个元素级，记 1 次）。其余全黑白灰。
- 手机：三列改两行（序号+工具名一行，说明缩进第二行），行高自适应。
- 动效：无循环；入场 `opacity + y:12→0` 0.5s `power2.out` 一次（v3 §1.6）。
- `:focus-visible` 强调色 `--red`。

### 3.4 治愈插画：接住星星的小树 + 候鸟

位置与构图：放在瑞士小节**之后、区块末尾**，通栏但高度克制（SVG 高 180px，手机 140px），`margin-top: 72px`。叙事："候鸟有来回，人生无返程"——但这是花园，鸟是**飞回来**的那一群：画面右侧一群候鸟向左飞，左侧一棵小树伸着枝丫，枝头顶一颗星。

```html
<div class="garden-coda">
  <svg viewBox="0 0 1000 180" aria-hidden="true"><!-- 下述元素 --></svg>
  <p class="coda-note">候鸟有来回，人生无返程。<span>——把学到的都种在这里</span></p>
</div>
```

SVG 元素（全部 `fill`，无描边，简约治愈系）：

- 地面线：`rect` 高 3，宽 1000，色 `#D8E6CF`（叶绿 15% 感觉的浅苔），y=150。
- 小树：干 `path M110,150 C112,120 108,105 110,88` 粗 7 圆头，色 `#8A7B66`（暖棕，比 v2 木棕浅一档）；冠 = 3 个叠压圆 r 30/24/18，色 `--leaf`(#7FB77E) / `#96C795` / `#AFD8AE`，中心 (110, 70) 附近错落；一根斜枝 `path M110,105 C135,95 150,85 168,72` 粗 4 同色干。
- 星：枝头 (172, 66) 放一颗四角星（`path` 自绘或 `✦` 形 polygon，径 16），色 `--yellow`(#FFD23F)——**这是本屏第 3 处彩色**（图谱的蓝簇、teal 簇之后，黄在此），满额。
- 候鸟 5 只：简约"人"字曲线 `path M0,0 Q6,-7 12,0 Q18,-7 24,0` 描边 3px 圆头 `#7A8B74`（灰绿），不填色；从 x=880 到 x=560 递减排开、逐只略小（24→16px 宽），营造纵深。
- `.coda-note`：14px `opacity .7` 居中，margin-top 16px；`<span>` 部分 12px `opacity .6`。

动效（本屏唯一循环，§1.3 已分配）：

- 雁群整体 `x: 0 → -40` 12s `sine.inOut` yoyo 无限（像在空中缓缓起伏着飞）；星星 `opacity .7↔1` 2.4s 呼吸。
- **reduced-motion**：全部静止（总开关已覆盖 CSS 动画；若用 GSAP 写则过 `reduceMotion` 检查）。

---

## 4. 风格档案区块

### 4.1 区块标题与叙述

```html
<section class="section archive" id="archive">
  <div class="sec-head">
    <span class="sec-num fun sec-num-alt">04</span>
    <h2 class="sec-title fun">风格档案</h2>
  </div>
  <p class="garden-lede">做这个网站时试过的设计风格，每个都留下一小块。
    上半部分也是我的 AI 概念笔记——设计史和机器学习，一起学。</p>
```

`.sec-num-alt { box-shadow: 3px 3px 0 var(--yellow); }`（错位阴影粉→黄，仅此处，见 §1.2.3）。

### 4.2 布局：上下两小节，不并列

包豪斯小节（5 概念）内容密度高于 Y2K 小节（3 卡），**上下排**比左右并列稳：

```
.archive .bauhaus-panel { margin-bottom: 56px; }
@media (min-width: 960px) {
  /* 桌面可选：若 Charlotte 想更"档案柜"，改 grid 2 列 5:7，见 §6 待拍板 */
}
```

两小节都是"展品面板"：白卡容器 + 各自风格的内容，外壳统一 `border: 3px solid var(--ink); border-radius: 14px; box-shadow: 6px 6px 0 var(--ink); padding: 36px`（孟菲斯外壳装非孟菲斯内容——这是"档案"的语义：展品放在统一的柜子里）。手机 padding 24px 18px。

### 4.3 包豪斯小节：5 个 AI 概念（圆方三角构成）

内容（5 个概念，配几何形——形与概念的关系是"构成感"而非图解，别硬拗含义）：

| 形 | 概念 | 一句话 |
|:--|:---|:---|
| 圆 · 红 | 大语言模型 LLM | 概率预测下一个词，却能涌现推理 |
| 方 · 黄 | 提示工程 | 输入质量决定输出质量 |
| 三角 · 蓝 | AI Agent | 模型 + 工具 + 循环 = 自主执行 |
| 圆 · 墨线 | RAG | 先检索，再生成，减少幻觉 |
| 方 · 墨线 | 多智能体协作 | 把大任务拆给一队专家 Agent |

视觉压缩参数（完整照 v3 §2，差量如下）：

- 面板内标题：`KONSTRUKTION` Jost 700 16px 大写 `.2em` + 中文"五个 AI 概念" Noto Sans SC 900 18px `#1A1A1A`；面板内底 `background: #F4F1EA`（v3 `--paper` 纸白，与外壳白卡区分）。
- 概念条：桌面 5 列 grid `gap: 20px`；每列 = 几何形（40px）居上 + 概念名 900 16px + 一句话 13px `#8A8A8A`。
- 几何形画法（照 v3 §2.3）：圆 `border-radius:50%`、方直角、三角 `clip-path: polygon(50% 0,100% 100%,0 100%)`；实填三原色 `#E94B3C / #F2C94C / #2F80ED`。
- **三色纪律换算**：v3 "每屏各色 ≤1 次" → 本小节内红/黄/蓝各恰好 1 次（前三形）；第 4/5 形用 `#1A1A1A` 墨线 3px 描边、纸白填——5 个形不撞纪律。
- 全小节 0 圆角（几何形除外）、禁描边禁投影（墨线形是"线稿"，不算描边装饰，特许）。
- 手机：5 列 → 2 列网格（第 5 个独占一行居中）→ 390px 以下 1 列、形 32px。
- 动效：入场 fade-up stagger .06 一次；无循环。
- `:focus-visible` 强调色 `--blue`(#2F80ED)。

### 4.4 Y2K 小节：LLM-Wiki 概念出口水珠卡

内容（3 张水珠卡，每张 = 一个图谱核心概念的"出口"——卡面文案直接取自图谱数据）：

| 卡 | 概念 | 卡面引文（summary 首句截 40 字） |
|:--|:---|:---|
| 01 | vibe-coding | 用 AI 辅助完成软件开发的新兴方式——开发者用自然语言描述需求… |
| 02 | Agent-Orchestration | 让多个 AI Agent 像一个团队一样分工、调度、协作的模式… |
| 03 | 响应式设计 | 一套代码适配手机、平板、桌面等不同屏幕尺寸… |

视觉压缩参数（完整照 v3 §5，差量如下）：

- 面板内标题：`AERO EXIT` Baloo 2 800 16px `.2em` `--accent`(#3B9CD6) + 中文"从 Wiki 出口潜入" Noto Sans SC 700 18px `--ink`(#1C3D52)。
- 面板内底：`linear-gradient(180deg, #EAF6FC 0%, #FFFFFF 100%)`（`--sky-pale`→白，**不用蓝天白云满铺**——v3 纪律"蓝天白云只留给 Hero"，小节用它的淡化版）。
- 水珠卡 3 张：桌面 3 列 grid gap 24px；参数直接照抄 v3 §5.4 `.work-card`（半透明白 + `backdrop-filter: blur(8px)` + 18px 圆角 + 顶部 40% 高光带 + `overflow:hidden`）。
  - 卡面结构：序号 Baloo 2 800 13px `--accent`（`01`）→ 概念名 700 18px `--ink` → 引文 13px `--dim`(#5B7A8F) → 底部 `1px solid var(--silver)`(#C9D4DD) + `进入 Wiki →`。
  - 高光只此一层（45% 顶部白），装饰 `✦` 每张卡右上 14px `--sky`(#87CEEB)（3 张统一，记装饰 1 种）。
  - hover：`translateY(-5px)` + 阴影加深（v3 §5.4 原值）。
- 手机：3 列 → 1 列；`backdrop-filter` 降到 `blur(6px)`（低端机掉帧，v3 §3.5 同理）。
- 动效：入场 `opacity + y:22→0 + scale .98→1` 0.7s `power3.out` 一次；无循环。
- `:focus-visible` 强调色 `--accent`(#3B9CD6)。
- 链接目标：v1 一律 `href="#"` 占位 + `aria-disabled`，或链到 `#garden` 图谱（推荐后者，页内闭环）；真实 wiki 外链见 §6 待拍板。

---

## 5. 字体与依赖增量

在 demo-i 现有 `Fredoka + Noto Sans SC` 之外，新增 Google Fonts（一个 link 合并）：

```html
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700;900&family=Inter:wght@700;800&family=Jost:wght@600;700&family=Baloo+2:wght@700;800&display=swap" rel="stylesheet">
```

（Inter = 瑞士小节，Jost = 包豪斯小节，Baloo 2 = Y2K 小节。中文字重不动。）

JS 依赖：不新增。图谱手写 SVG + 布局算法，零库。

---

## 6. 待 Charlotte 拍板

1. **图谱节点点击行为**：v1 设计为"只有浮层、无跳转"。是否给核心节点挂真实 wiki 页面链接（需要 wiki 有可公开访问的 URL；纯本地 Obsidian 则维持无跳转）。
2. **Y2K 水珠卡出口**：链到页内 `#garden`（推荐，闭环）还是留 `#` 占位等真实 wiki 外链。
3. **⑤ 风格档案桌面布局**：上下排（本规范默认）还是 5:7 网格左右并列（更"档案柜"，但包豪斯 5 概念在窄列里会挤）。
4. 瑞士小节工具清单 6 条内容是否照录（§3.3 表），尤其是"Kimi Code 帮忙搭的"这句自述。

---

## 7. 实现者自查清单（照 v3 §8 惯例）

1. Hero：星星静止/闪烁两态都看过（模拟 reduced-motion 开关各一次）；悬停摩天轮暂停转动时**星星闪烁不停**（用的是 `clock.elapsedTime` 不是 `spin`）。
2. 图谱：15 节点全渲染、5 个核心有黄环；hover 任一节点，非相邻节点淡出；Tab 能走完全部 15 个节点且浮层跟随；手机上非核心标签隐藏、点按出浮层。
3. 图谱布局输出应为两簇左右分布（A 簇 10 节点在左、B 簇 5 节点在右）；若两簇重叠，检查第 3.2.3 节第 2 步簇圆心计算。
4. 三小节 `:focus-visible` 描边色分别是红/蓝/蓝（§0）。
5. 彩色配额抽查：④ 屏 = 图谱蓝簇 + teal 簇 + 插画黄星（3，满）；⑤ 屏 = 包豪斯三色（3，满）；瑞士小节红只出现在序号。
6. 手机 <640px 整页纵向滚动无劫持（three 的 `touchAction='pan-y'` 一行还在；SVG 图谱不拦滚动）。
