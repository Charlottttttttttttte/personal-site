#!/usr/bin/env python3
"""espanol 学习包生成器。

产出:
- data/espanol/days.json(多周合并,按日期去重、Día 连续编号),自带 schema 校验
- vault「Charlotte」的 补充词.md(obsidian-spaced-repetition 间隔复习,保留历史)

用法:
  python3 scripts/gen_espanol.py --start 2026-08-18 --week 1   # 生成/更新第一周
  python3 scripts/gen_espanol.py --start 2026-08-24 --week 2   # 追加第二周(合并进 days.json)
  python3 scripts/gen_espanol.py --no-vault                     # 跳过 vault 同步

节奏:每周 5 天学(一三五精听 / 二四阅读)+ 周末休息。
输入素材:真实语料(西剧/动画字幕、西语童话/书),来源在 input.source。
"""
import argparse, json, os, re, sys
from datetime import date, timedelta

WEEKDAYS = ["一", "二", "三", "四", "五", "六", "日"]
VAULT = "/Users/charlotte/Library/Mobile Documents/iCloud~md~obsidian/Documents/Charlotte"
SR_FILE = os.path.join(VAULT, "📝 Personal", "西语学习", "补充词.md")
LESSONS_DIR = os.path.join(VAULT, "📝 Personal", "西语学习", "学习包")
OUT_DEFAULT = "data/espanol/days.json"

# ===== 真实语料来源 =====
PEPPA_E49 = "https://spanishboom.com/spanish-cartoons-with-transcription/peppa-pig-s01-e49"
PEPPA_E49_VIDEO = "https://www.youtube.com/results?search_query=peppa+pig+español+nos+vamos+a+la+compra"
CERDITOS = "https://www.thespanishexperiment.com/stories/threepigs"

# ===== 第一周:动物主题(A1→A2 过渡)=====
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
            "source": {"type": "video", "label": "小猪佩奇(西语版)", "url": "https://www.youtube.com/results?search_query=peppa+pig+español"},
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
            "hint": "读 1-2 遍,然后做判断题;答案第二天核对。",
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
            "source": {"type": "video", "label": "小猪佩奇(西语版)", "url": "https://www.youtube.com/results?search_query=peppa+pig+español"},
            "script": [
                ["Buenas tardes, ¿busca algo?", "下午好,您找什么?"],
                ["Sí, quiero adoptar un gato pequeño.", "是的,我想领养一只小猫。"],
                ["Tenemos dos gatitos muy cariñosos.", "我们有两只很亲人的小猫。"],
                ["¿Y qué comen?", "它们吃什么?"],
                ["Comen pienso y beben mucha agua.", "吃猫粮,喝很多水。"],
                ["Perfecto, me llevo el gris, por favor.", "太好了,我就要那只灰色的。"],
            ],
            "hint": "同一段反复听,不看字幕能全听懂再换下一个。",
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
            "hint": "读 1-2 遍,然后做判断题;答案第二天核对。",
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
            "source": {"type": "video", "label": "Español con Juan(西班牙慢速)", "url": "https://www.youtube.com/results?search_query=Español+con+Juan"},
            "script": [
                ["¿Dónde paseas a tu perro?", "你在哪遛狗?"],
                ["En el parque, cerca de mi casa.", "在我家附近的公园。"],
                ["¿Va sin correa?", "它不拴绳吗?"],
                ["Sí, pero obedece muy bien.", "不拴,但它很听话。"],
                ["¿Le gusta jugar a la pelota?", "它喜欢玩球吗?"],
                ["¡Muchísimo! Corre detrás de la pelota todo el día.", "超级喜欢!整天追着球跑。"],
            ],
            "hint": "同一段反复听,不看字幕能全听懂再换下一个。",
        },
        "writing": {"prompt": "写 3 句:你每天怎么照顾宠物 / 动物?(Cuido a… / Doy de comer a…)"},
    },
}

# ===== 第二周:真实语料(佩奇去购物 / 三只小猪)=====
WEEK2_CURRICULUM = {
    "一": {
        "title": "精听 · 小猪佩奇:去购物(1)",
        "extras": [
            {"es": "la compra", "zh": "购物 / 买的东西", "ex": "Nos vamos a la compra."},
            {"es": "el carrito", "zh": "购物车", "ex": "A George le encanta ir en el carrito."},
            {"es": "la lista", "zh": "清单", "ex": "Hay cuatro cosas en la lista."},
            {"es": "encontrar", "zh": "找到", "ex": "Lo encontraré todo.", "note": "encontrar → yo encuentro" },
            {"es": "la cebolla", "zh": "洋葱", "ex": "Lo siguiente son cebollas."},
            {"es": "tachar", "zh": "划掉", "ex": "Voy a tacharlos de la lista."},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 佩奇:去购物(1)",
            "source": {"type": "video", "label": "小猪佩奇 S01E49 去购物(真实台词)", "url": PEPPA_E49_VIDEO},
            "script": [
                ["Nos vamos a la compra.", "我们去购物。"],
                ["¿Papi, puedo ir yo también en el carrito?", "爸爸,我也能坐购物车吗?"],
                ["Ya eres muy mayor para eso, Peppa.", "你已经很大了,佩奇。"],
                ["Nos ayudarás a hacer la compra.", "你会帮我们购物。"],
                ["¡Sí! ¡Yo la haré!", "好的!我来!"],
                ["Hay apuntadas cuatro cosas en la lista.", "清单上记着四样东西。"],
                ["Unos tomates, spaghettis, cebollas y fruta.", "西红柿、意大利面、洋葱和水果。"],
                ["Peppa, primero hay que buscar tomates.", "佩奇,先要找西红柿。"],
                ["¡Ya los veo! Aquí están los tomates, mami.", "我看到了!西红柿在这,妈妈。"],
                ["Muy bien, Peppa. Ahora mételos en el carro.", "很好,佩奇。现在把它们放进购物车。"],
            ],
            "hint": "这是《小猪佩奇》的真实台词,反复听;再点上方链接看原片(带双语字幕站)。",
        },
        "writing": {"prompt": "写 3 句:你去超市会买什么?(Compro… / Necesito…)"},
    },
    "二": {
        "title": "阅读 · 三只小猪(1)",
        "extras": [
            {"es": "la paja", "zh": "稻草", "ex": "El primer cerdito construyó una casa de paja."},
            {"es": "la madera", "zh": "木头", "ex": "El segundo cerdito usó madera."},
            {"es": "el ladrillo", "zh": "砖", "ex": "La casa de ladrillos es muy fuerte."},
            {"es": "el granjero", "zh": "农夫", "ex": "El granjero le dio la paja."},
            {"es": "soplar", "zh": "吹", "ex": "El lobo sopló y sopló."},
            {"es": "derrumbar", "zh": "弄塌", "ex": "El lobo derrumbó la casa."},
        ],
        "input": {
            "kind": "read", "label": "阅读 · 三只小猪(1)",
            "source": {"type": "book", "label": "三只小猪(西语童话,带英译+音频)", "url": CERDITOS},
            "text": "Érase una vez una mamá cerda que tenía tres cerditos. No había suficiente comida, así que los cerditos tuvieron que ir a buscar su suerte. El primer cerdito encontró a un granjero con un atado de paja y le pidió: «¿Podría darme esa paja para construir una casa?» Como dijo «por favor», el granjero le dio la paja. El cerdito construyó una casa de paja y se echó una siesta. De pronto llegó el gran lobo malo: «¡Cerdito, ábreme la puerta!» El cerdito no abrió, y el lobo sopló y sopló y derrumbó la casa.",
            "questions": [
                {"q": "La mamá cerda tenía tres cerditos.", "zh": "猪妈妈有三只小猪", "a": True},
                {"q": "El primer cerdito construyó una casa de madera.", "zh": "第一只小猪盖了木头房子", "a": False},
                {"q": "El lobo derrumbó la casa de paja.", "zh": "狼吹倒了稻草房子", "a": True},
            ],
            "hint": "真实西语童话(有音频可听),读 1-2 遍做判断题;想听全文点上方链接。",
        },
        "writing": {"prompt": "写 3 句:你最喜欢的童话/故事是哪个?为什么?(Me gusta el cuento de… porque…)"},
    },
    "三": {
        "title": "精听 · 小猪佩奇:去购物(2)",
        "extras": [
            {"es": "la comida preferida", "zh": "最喜欢的食物", "ex": "Los spaghettis son la comida preferida."},
            {"es": "las chuches", "zh": "糖果(西班牙口语)", "ex": "Yo no veo chuches en la lista."},
            {"es": "no me acuerdo", "zh": "我不记得", "ex": "La verdad es que no me acuerdo."},
            {"es": "el dinosaurio", "zh": "恐龙", "ex": "No hay dinosaurios en los supermercados."},
            {"es": "meter en el carro", "zh": "放进购物车", "ex": "Tienes que meterlos en el carro."},
            {"es": "lo siguiente", "zh": "下一项", "ex": "¿Qué va ahora en la lista?"},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 佩奇:去购物(2)",
            "source": {"type": "video", "label": "小猪佩奇 S01E49(真实台词)", "url": PEPPA_E49_VIDEO},
            "script": [
                ["Los spaghettis son la comida preferida de Peppa y George.", "意大利面是佩奇和乔治最喜欢的食物。"],
                ["¿Dónde estarán los spaghettis?", "意大利面会在哪呢?"],
                ["¡Ya los veo! Mira, mami, aquí están.", "我看到了!看,妈妈,在这。"],
                ["Muy bien. Ahora tienes que meterlos en el carro.", "很好。现在你得把它们放进购物车。"],
                ["¿Qué va ahora en la lista, Peppa?", "清单上现在是什么,佩奇?"],
                ["¡Chuches!", "糖果!"],
                ["Yo no veo chuches en la lista.", "我在清单上没看到糖果。"],
                ["Tienes muchas en casa, Peppa.", "你家里已经有很多了,佩奇。"],
                ["La verdad es que no me acuerdo.", "说实话,我不记得了。"],
                ["No hay dinosaurios en los supermercados.", "超市里可没有恐龙。"],
            ],
            "hint": "真实台词,反复听;再点上方链接看原片。",
        },
        "writing": {"prompt": "写 3 句:你最喜欢的食物是什么?(Mi comida preferida es…)"},
    },
    "四": {
        "title": "阅读 · 三只小猪(2)",
        "extras": [
            {"es": "el techo", "zh": "屋顶", "ex": "El lobo subió al techo."},
            {"es": "la chimenea", "zh": "烟囱", "ex": "Bajó por la chimenea."},
            {"es": "la olla", "zh": "锅", "ex": "Cayó en una olla de sopa."},
            {"es": "la sopa", "zh": "汤", "ex": "La sopa estaba muy caliente."},
            {"es": "escalar / subir", "zh": "爬上", "ex": "El lobo escaló al techo."},
            {"es": "huir", "zh": "逃跑", "ex": "El lobo salió huyendo."},
        ],
        "input": {
            "kind": "read", "label": "阅读 · 三只小猪(2)",
            "source": {"type": "book", "label": "三只小猪(西语童话,带英译+音频)", "url": CERDITOS},
            "text": "El segundo cerdito encontró a un granjero que llevaba un atado de madera y le pidió: «¿Podría darme esa madera?» El granjero le dio la madera, y el cerdito construyó una casa de madera. El lobo llegó, tocó la puerta y dijo: «¡Cerdito, ábreme la puerta!» El cerdito no abrió, y el lobo sopló y sopló y derrumbó también esta casa. El tercer cerdito, el más trabajador, construyó una casa de ladrillos. El lobo sopló y sopló, pero no pudo derrumbarla. Entonces subió al techo y bajó por la chimenea… ¡y cayó en una olla de sopa muy caliente! El lobo salió huyendo y nunca volvió.",
            "questions": [
                {"q": "El segundo cerdito construyó una casa de ladrillos.", "zh": "第二只小猪盖了砖房子", "a": False},
                {"q": "El lobo no pudo derrumbar la casa de ladrillos.", "zh": "狼吹不倒砖房子", "a": True},
                {"q": "El lobo cayó en una olla de sopa.", "zh": "狼掉进了汤锅里", "a": True},
            ],
            "hint": "真实西语童话,读 1-2 遍做判断题;想听全文点上方链接。",
        },
        "writing": {"prompt": "写 3 句:形容你的家 / 房间。(Mi casa tiene… / Mi habitación es…)"},
    },
    "五": {
        "title": "精听 · 小猪佩奇:去购物(3)",
        "extras": [
            {"es": "la fruta", "zh": "水果", "ex": "Lo que falta es fruta."},
            {"es": "la sandía", "zh": "西瓜", "ex": "Hay una sandía muy grande."},
            {"es": "la tarta", "zh": "蛋糕", "ex": "La tarta de chocolate tiene buena pinta."},
            {"es": "el postre", "zh": "甜点", "ex": "Pensé que sería un buen postre."},
            {"es": "tener buena pinta", "zh": "看起来不错", "ex": "¡Tiene muy buena pinta!"},
            {"es": "goloso", "zh": "嘴馋的", "ex": "¡Qué goloso, papi!"},
        ],
        "input": {
            "kind": "listen", "label": "精听 · 佩奇:去购物(3)",
            "source": {"type": "video", "label": "小猪佩奇 S01E49(真实台词)", "url": PEPPA_E49_VIDEO},
            "script": [
                ["Sólo queda una cosa en la lista.", "清单上只剩一样东西了。"],
                ["Lo que falta por comprar es fruta.", "还缺的要买的是水果。"],
                ["Tú elegirás la fruta, George.", "你来选水果,乔治。"],
                ["Hay manzanas, naranjas, plátanos y una sandía muy grande.", "有苹果、橙子、香蕉和一个很大的西瓜。"],
                ["Esta es la caja donde se paga toda la compra.", "这是付所有东西钱的地方。"],
                ["Peppa, ¿has puesto tú la tarta de chocolate en el carro?", "佩奇,是你把巧克力蛋糕放进购物车的吗?"],
                ["Yo no, mami.", "不是我,妈妈。"],
                ["Pensé que sería un buen postre.", "我想它会是个不错的甜点。"],
                ["¡Qué goloso, papi!", "爸爸你真馋!"],
                ["Lo apunto ahora en la lista y arreglado.", "我现在把它记上清单,搞定。"],
            ],
            "hint": "真实台词,反复听;再点上方链接看原片。",
        },
        "writing": {"prompt": "写 3 句:写一次你购物 / 逛街的经历。(Ayer fui a… y compré…)"},
    },
}

CURRICULUMS = {"1": WEEK1_CURRICULUM, "2": WEEK2_CURRICULUM}


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
        entry = {"date": d.isoformat(), "weekday": wd}
        if wd in ("六", "日"):
            entry.update({"type": "rest", "title": "周末休息 · 复习"})
        else:
            entry["type"] = "listen" if wd in ("一", "三", "五") else "read"
            entry.update(curriculum[wd])
            entry["title"] = curriculum[wd]["title"]
        validate_day(entry)
        out.append(entry)
    return out


def merge_days(existing, new):
    """按日期合并:Día 连续编号。"""
    by_date = {}
    for d in existing:
        by_date[d["date"]] = d
    for d in new:
        by_date[d["date"]] = d
    merged = sorted(by_date.values(), key=lambda x: x["date"])
    for i, d in enumerate(merged, 1):
        d["day"] = i
    return merged


def sync_vault(days, out_path):
    """合并补充词进 vault(obsidian-spaced-repetition),去重保留已有 SR 标签。"""
    existing = {}
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"-\s+\*\*(.+?)\*\*", line)
                if m:
                    existing[m.group(1).strip()] = line.rstrip("\n")
    new_lines = list(existing.values())
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


def sync_lessons(days, out_dir):
    """把每天学习包写成 markdown 同步进 vault「学习包」目录(全量同步,先清后写,保证与 days.json 一致)。"""
    os.makedirs(out_dir, exist_ok=True)
    for f in os.listdir(out_dir):
        if f.endswith(".md"):
            os.remove(os.path.join(out_dir, f))
    written = 0
    for d in days:
        if d["type"] == "rest":
            continue
        wd = d["weekday"]
        kind = "精听" if d["type"] == "listen" else "阅读"
        src = (d["input"].get("source") or {})
        lines = [
            f"# {d['date']} 星期{wd} · {d['title']}",
            "",
            f"> Día {d['day']} · {kind}日",
        ]
        if src.get("label"):
            link = f" <{src['url']}>" if src.get("url") else ""
            lines.append(f"> 真实语料:{src['label']}{link}")
        lines += ["", "## 补充词(欧洲西语)"]
        for w in d["extras"]:
            note = f"(note: {w['note']})" if w.get("note") else ""
            lines.append(f"- **{w['es']}** — {w['zh']} — *{w['ex']}* {note}")
        lines.append("")
        inp = d["input"]
        lines.append(f"## {inp.get('label','')}")
        if inp["kind"] == "listen":
            for s in inp.get("script", []):
                lines.append(f"- {s[0]} — {s[1]}")
        else:
            lines.append("")
            lines.append(inp.get("text", ""))
            lines.append("")
            lines.append("### 判断题(答案已标)")
            for q in inp.get("questions", []):
                lines.append(f"- [ ] {q['q']} ({q['zh']}) → {'对' if q['a'] else '错'}")
        lines.append("")
        if inp.get("hint"):
            lines.append(f"> 💡 {inp['hint']}")
        lines += ["", "## 写作(3 句)", d["writing"]["prompt"], ""]
        fname = d["date"] + "-" + re.sub(r"[\s·:：/\\?]", "", d["title"]) + ".md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        written += 1
    return written


def main():
    ap = argparse.ArgumentParser(description="生成/合并 espanol 学习包 days.json + vault 补充词")
    ap.add_argument("--start", required=True, help="起始日期 YYYY-MM-DD")
    ap.add_argument("--days", type=int, default=7, help="生成天数(默认一周)")
    ap.add_argument("--week", default="1", choices=["1", "2"], help="周课程(1=动物主题,2=真实语料)")
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--no-vault", action="store_true", help="跳过 vault 同步")
    args = ap.parse_args()

    start = date.fromisoformat(args.start)
    curriculum = CURRICULUMS[args.week]
    new_days = build(start, args.days, curriculum)

    existing = []
    if os.path.exists(args.out):
        with open(args.out, encoding="utf-8") as f:
            existing = json.load(f).get("days", [])
    merged = merge_days(existing, new_days)

    payload = {
        "meta": {"name": "espanol 学习包", "note": "由 scripts/gen_espanol.py 生成;--week 1/2 按周追加。"},
        "days": merged,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    study = [d for d in new_days if d["type"] != "rest"]
    print(f"OK: 本周 {len(study)} 学习日,days.json 共 {len(merged)} 天 → {args.out}")
    for d in study:
        print(f"  {d['date']} 星期{d['weekday']} [{d['type']}] {d['title']}")
    if not args.no_vault:
        total, kept = sync_vault(merged, SR_FILE)
        print(f"vault 补充词:共 {total} 条(保留 {kept},新增 {total - kept})")
        n = sync_lessons(merged, LESSONS_DIR)
        print(f"vault 学习包:同步 {n} 天 → {LESSONS_DIR}")


if __name__ == "__main__":
    sys.exit(main())
