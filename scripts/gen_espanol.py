#!/usr/bin/env python3
"""espanol 学习包生成器。

产出:
- data/espanol/days.json(数据驱动,页面按日期取当天课),自带 schema 校验
- vault「Charlotte」的 补充词.md(obsidian-spaced-repetition 间隔复习,去重保留已有 SR 标签)

用法:
  python3 scripts/gen_espanol.py --start 2026-08-17 --days 7
  python3 scripts/gen_espanol.py --no-vault   # 跳过 vault 同步

节奏:每周 5 天学(一三五精听 / 二四阅读)+ 周末休息;每天 补充词 + 输入 + 写作。
"""
import argparse, json, os, re, sys
from datetime import date, timedelta

WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]
VAULT = "/Users/charlotte/Library/Mobile Documents/iCloud~md~obsidian/Documents/Charlotte"
SR_FILE = os.path.join(VAULT, "📝 Personal", "西语学习", "补充词.md")

# 真实语料源(精听 → YouTube;阅读 → Difusión 分级读物)
YOUTUBE_PEPPA = "https://www.youtube.com/results?search_query=peppa+pig+español"
YOUTUBE_JUAN = "https://www.youtube.com/results?search_query=Español+con+Juan"

# ===== 第一周:动物主题(A1→A2 过渡,西班牙本土西语)=====
WEEK1_CURRICULUM = {
    "一": {
        "title": "精听 · 谈论动物",
        "extras": [
            {"es": "el perro", "zh": "狗", "ex": "Tengo un perro pequeño."},
            {"es": "el gato", "zh": "猫", "ex": "Mi gato es negro."},
            {"es": "el pájaro", "zh": "鸟", "ex": "El pájaro canta por la mañana."},
            {"es": "el pez", "zh": "鱼", "ex": "Tengo dos peces en casa."},
            {"es": "la mascota", "zh": "宠物", "ex": "¿Tienes mascota?"},
            {"es": "cuidar", "zh": "照顾", "ex": "Cuido a mi perro todos los días."},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 聊宠物",
            "source": {"type": "video", "label": "小猪佩奇(西语版)", "url": YOUTUBE_PEPPA},
            "script": [
                ["¿Tienes mascota?", "你有宠物吗?"],
                ["Sí, tengo un perro y dos gatos.", "有,我有一只狗和两只猫。"],
                ["¿Cómo se llama tu perro?", "你的狗叫什么?"],
                ["Se llama Lobo. Es muy cariñoso.", "它叫洛博,很亲人。"],
                ["¿Y los gatos?", "那猫呢?"],
                ["Son pequeños y muy traviesos.", "它们很小,很调皮。"],
            ],
            "hint": "同一段反复听,不看字幕能全听懂再换下一个;再看一条真实视频磨耳朵。",
        },
        "writing": {"prompt": "用今天学的词写 3 句:你家有什么宠物 / 动物?(¿Qué animales tienes?)"},
    },
    "二": {
        "title": "阅读 · 动物园一日",
        "extras": [
            {"es": "el zoo", "zh": "动物园", "ex": "Vamos al zoo el domingo."},
            {"es": "salvaje", "zh": "野生的", "ex": "El león es un animal salvaje."},
            {"es": "la granja", "zh": "农场", "ex": "Mi abuelo tiene una granja."},
            {"es": "el caballo", "zh": "马", "ex": "El caballo corre mucho."},
            {"es": "la vaca", "zh": "牛", "ex": "La vaca da leche."},
            {"es": "tener miedo de", "zh": "害怕", "ex": "Tengo miedo de los elefantes."},
        ],
        "input": {
            "kind": "read", "label": "阅读 · 动物园一日",
            "source": {"type": "book", "label": "Difusión 分级读物(A1)", "url": ""},
            "text": "El domingo, Marta y su hermano van al zoo. Les gustan mucho los animales. Primero ven a los leones, que son muy grandes. Después, van a la granja del zoo y dan de comer a las cabras. Su hermano quiere ver a los elefantes, pero Marta tiene miedo de ellos. Al final, compran un helado y vuelven a casa contentos.",
            "questions": [
                {"q": "Van al zoo el domingo.", "zh": "他们周日去动物园", "a": True},
                {"q": "Marta tiene miedo de los elefantes.", "zh": "玛尔塔害怕大象", "a": True},
                {"q": "Compran palomitas al final.", "zh": "最后他们买了爆米花", "a": False},
            ],
            "hint": "读 1-2 遍,然后做判断题;答案第二天核对。有余力翻 1-2 页真实分级读物。",
        },
        "writing": {"prompt": "写 3 句:你最喜欢的动物和为什么。(Me gusta… porque…)"},
    },
    "三": {
        "title": "精听 · 宠物店",
        "extras": [
            {"es": "el conejo", "zh": "兔子", "ex": "El conejo come zanahorias."},
            {"es": "adoptar", "zh": "领养", "ex": "Quiero adoptar un perro."},
            {"es": "el veterinario", "zh": "兽医", "ex": "Llevo al gato al veterinario."},
            {"es": "dar de comer", "zh": "喂食", "ex": "Doy de comer a los peces."},
            {"es": "la jaula", "zh": "笼子", "ex": "El pájaro está en la jaula."},
            {"es": "ladrar", "zh": "叫(狗吠)", "ex": "El perro ladra mucho."},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 宠物店",
            "source": {"type": "video", "label": "小猪佩奇(西语版)", "url": YOUTUBE_PEPPA},
            "script": [
                ["Buenas tardes, ¿busca algo?", "下午好,您找什么?"],
                ["Sí, quiero adoptar un gato pequeño.", "是的,我想领养一只小猫。"],
                ["Tenemos dos gatitos muy cariñosos.", "我们有两只很亲人的小猫。"],
                ["¿Y qué comen?", "它们吃什么?"],
                ["Comen pienso y beben mucha agua.", "吃猫粮,喝很多水。"],
                ["Perfecto, me llevo el gris, por favor.", "太好了,我就要那只灰色的。"],
            ],
            "hint": "同一段反复听,不看字幕能全听懂再换下一个;再看一条真实视频磨耳朵。",
        },
        "writing": {"prompt": "写 3 句:你想养什么宠物?(Quiero adoptar…)"},
    },
    "四": {
        "title": "阅读 · 露西亚家的动物",
        "extras": [
            {"es": "la tortuga", "zh": "乌龟", "ex": "La tortuga vive muchos años."},
            {"es": "la serpiente", "zh": "蛇", "ex": "La serpiente no tiene patas."},
            {"es": "morder", "zh": "咬", "ex": "El perro no muerde."},
            {"es": "la pata", "zh": "爪子 / 腿(动物)", "ex": "El gato tiene cuatro patas."},
            {"es": "el animal doméstico", "zh": "家养动物", "ex": "El perro es un animal doméstico."},
            {"es": "gritar", "zh": "喊叫", "ex": "Cuando ve una araña, grita."},
        ],
        "input": {
            "kind": "read", "label": "阅读 · 露西亚家的动物",
            "source": {"type": "book", "label": "Difusión 分级读物(A1)", "url": ""},
            "text": "En casa de Lucía hay muchos animales. Tiene una tortuga que se llama Mancha, dos pájaros y un acuario con peces de colores. A su hermano le encantan los reptiles y quiere una serpiente, pero su madre dice que no. A Lucía, en cambio, le dan miedo las arañas. Por eso, cuando ve una, grita y llama a su padre.",
            "questions": [
                {"q": "Lucía tiene una tortuga llamada Mancha.", "zh": "露西亚有一只叫曼查的乌龟", "a": True},
                {"q": "Su hermano quiere un perro.", "zh": "她哥哥想要一只狗", "a": False},
                {"q": "A Lucía le dan miedo las arañas.", "zh": "露西亚害怕蜘蛛", "a": True},
            ],
            "hint": "读 1-2 遍,然后做判断题;答案第二天核对。有余力翻 1-2 页真实分级读物。",
        },
        "writing": {"prompt": "写 3 句:你害怕什么动物?(Tengo miedo de… / Me dan miedo…)"},
    },
    "五": {
        "title": "精听 · 遛狗",
        "extras": [
            {"es": "pasear", "zh": "遛(狗)", "ex": "Paseo al perro por la mañana."},
            {"es": "la correa", "zh": "牵引绳", "ex": "El perro lleva correa."},
            {"es": "la pelota", "zh": "球", "ex": "Al perro le gusta la pelota."},
            {"es": "el parque", "zh": "公园", "ex": "Los perros corren en el parque."},
            {"es": "obedecer", "zh": "服从", "ex": "Mi perro obedece bien."},
            {"es": "correr detrás de", "zh": "追着…跑", "ex": "Corre detrás de la pelota."},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 遛狗",
            "source": {"type": "video", "label": "Español con Juan(西班牙慢速)", "url": YOUTUBE_JUAN},
            "script": [
                ["¿Dónde paseas a tu perro?", "你在哪遛狗?"],
                ["En el parque, cerca de mi casa.", "在我家附近的公园。"],
                ["¿Va sin correa?", "它不拴绳吗?"],
                ["Sí, pero obedece muy bien.", "不拴,但它很听话。"],
                ["¿Le gusta jugar a la pelota?", "它喜欢玩球吗?"],
                ["¡Muchísimo! Corre detrás de la pelota todo el día.", "超级喜欢!整天追着球跑。"],
            ],
            "hint": "同一段反复听,不看字幕能全听懂再换下一个;再看一条真实视频磨耳朵。",
        },
        "writing": {"prompt": "写 3 句:你每天怎么照顾宠物 / 动物?(Cuido a… / Doy de comer a…)"},
    },
}


def validate_day(d):
    """schema 校验:学习日必须有 extras/input(含 source)/writing。"""
    assert d["type"] in ("listen", "read", "rest"), d["date"] + " type 非法"
    if d["type"] == "rest":
        return
    assert d["extras"] and len(d["extras"]) >= 3, d["date"] + " extras 太少"
    assert d["input"] and d["writing"], d["date"] + " 缺 input/writing"
    inp = d["input"]
    if inp["kind"] == "listen":
        assert inp.get("script") and all(len(s) == 2 for s in inp["script"]), d["date"] + " 精听 script 非法"
    elif inp["kind"] == "read":
        assert inp.get("text") and inp.get("questions"), d["date"] + " 阅读缺 text/questions"
    assert inp.get("source") and inp["source"].get("type") in ("video", "book"), d["date"] + " 缺 source"
    assert d["writing"].get("prompt"), d["date"] + " 缺写作提示"


def build(start, days, curriculum):
    out = []
    for i in range(days):
        d = start + timedelta(days=i)
        wd = WEEKDAYS[d.weekday()]
        entry = {"date": d.isoformat(), "day": i + 1, "weekday": wd}
        if wd in ("六", "日"):
            entry.update({"type": "rest", "title": "周末休息 · 复习"})
        else:
            entry["type"] = "listen" if wd in ("一", "三", "五") else "read"
            entry.update(curriculum[wd])
            entry["title"] = curriculum[wd]["title"]
        validate_day(entry)
        out.append(entry)
    return out


def sync_vault(days, out_path):
    """把本周补充词合并进 vault 的 补充词.md(obsidian-spaced-repetition 间隔复习)。"""
    existing = {}  # es -> 原始行(保留 SR 标签)
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"-\s+\*\*(.+?)\*\*", line)
                if m:
                    existing[m.group(1).strip()] = line.rstrip("\n")
    new_lines = list(existing.values())  # 保留全部历史词条(按文件顺序)
    seen = set(existing.keys())
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    for d in days:
        if d["type"] == "rest":
            continue
        for w in d["extras"]:
            es = w["es"].strip()
            if es in seen:
                continue
            seen.add(es)
            note = f"(note: {w['note']}) " if w.get("note") else ""
            line = f"- **{es}** — {w['zh']} — *{w['ex']}* {note}<!--SR:!{tomorrow},1,300-->"
            new_lines.append(line)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# 补充词(欧洲西语)\n\n")
        f.write("> 由 `scripts/gen_espanol.py` 自动合并,请勿手改。复习用 obsidian-spaced-repetition 插件。\n\n")
        f.write("\n".join(new_lines) + "\n")
    return len(new_lines), len(existing)


def main():
    ap = argparse.ArgumentParser(description="生成 espanol 学习包 days.json + vault 补充词")
    ap.add_argument("--start", default="2026-08-17", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--days", type=int, default=7, help="生成天数(默认一周)")
    ap.add_argument("--out", default="data/espanol/days.json")
    ap.add_argument("--no-vault", action="store_true", help="跳过 vault 同步")
    args = ap.parse_args()

    start = date.fromisoformat(args.start)
    days = build(start, args.days, WEEK1_CURRICULUM)
    payload = {
        "meta": {
            "name": "espanol 学习包",
            "note": "由 scripts/gen_espanol.py 生成;每周/两周批量跑一次。",
        },
        "days": days,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    study = [d for d in days if d["type"] != "rest"]
    print(f"OK: {len(days)} 天({len(study)} 学习日)→ {args.out}")
    for d in study:
        print(f"  {d['date']} 星期{d['weekday']} [{d['type']}] {d['title']}")
    if not args.no_vault:
        total, kept = sync_vault(days, SR_FILE)
        print(f"vault 补充词:共 {total} 条(新 {total - kept},保留 {kept})→ {SR_FILE}")


if __name__ == "__main__":
    sys.exit(main())
