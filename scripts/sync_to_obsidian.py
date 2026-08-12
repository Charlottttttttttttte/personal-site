#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临池录 · Mac 自动拉取脚本
从 GitHub 拉取 data/shufa-inventory.json + data/shufa-records.json，
生成 Obsidian《临池录/库存总览.md》与《临池录/练习记录.md》。

由 launchd 定时触发（每 5 分钟），无需人工干预。
仓库为 public，无需令牌。

用法：
  python3 sync_to_obsidian.py            # 手动运行一次
"""
import json
import os
import sys
import urllib.request
from datetime import datetime

REPO_RAW_INV = "https://raw.githubusercontent.com/Charlottttttttttttte/personal-site/main/data/shufa-inventory.json"
REPO_RAW_REC = "https://raw.githubusercontent.com/Charlottttttttttttte/personal-site/main/data/shufa-records.json"
OBS_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Charlotte/临池录"
)
OUT_INV = os.path.join(OBS_DIR, "库存总览.md")
OUT_REC = os.path.join(OBS_DIR, "练习记录.md")

TYPE_LABEL = {"长卷": "长卷", "刀纸": "刀纸", "条屏": "条屏"}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "shufa-sync"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def inventory_md(items):
    lines = [
        "---",
        "type: 库存总览",
        f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "source: personal-site 自动同步",
        "---",
        "",
        "# 临池录 · 纸张库存总览",
        "",
        f"> 自动同步自个人网站（GitHub Pages），更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 纸张名称 | 类型 | 纸张ID | 剩余数量 | 单位 | 米数 | 尺寸规格 |",
        "|---------|------|--------|---------|------|------|---------|",
    ]
    for i in items:
        name = (i.get("name") or "").replace("|", "\\|")
        typ = TYPE_LABEL.get(i.get("type", ""), i.get("type", ""))
        pid = i.get("id") or ""
        qty = i.get("qty") or ""
        meters = i.get("meters")
        if i.get("type") == "长卷":
            unit = "卷" if not meters else "米"
            qty_disp = meters if meters else (qty or "")
        else:
            unit = "张"
            qty_disp = qty or ""
        meters_disp = f"{meters}" if meters else "—"
        spec = (i.get("spec") or "—").replace("|", "\\|")
        lines.append(
            f"| {name} | {typ} | {pid} | {qty_disp} | {unit} | {meters_disp} | {spec} |"
        )
    return "\n".join(lines) + "\n"


def records_md(records):
    valid = [r for r in records if not r.get("deleted")]
    valid.sort(key=lambda r: r.get("date", ""))
    total_meters = sum(r.get("meters") or 0 for r in valid)
    days = len(set(r.get("date") for r in valid))
    lines = [
        "---",
        "type: 练习记录",
        f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "source: personal-site 自动同步",
        "---",
        "",
        "# 临池录 · 练习记录",
        "",
        f"> 共 {len(valid)} 条记录 · {days} 天 · 累计 {total_meters:.1f} 米",
        f"> 自动同步自个人网站，更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 日期 | 类型 | 纸张 | 数量 | 米数 | 字体 | 字帖 | 备注 |",
        "|------|------|------|------|------|------|------|------|",
    ]
    for r in valid:
        date = r.get("date") or ""
        typ = "长卷" if r.get("type") == "scroll" else "单张"
        paper = (r.get("paperSnapshot") or {}).get("name", "") if r.get("paperSnapshot") else ""
        q = r.get("quantity") or {}
        qty = f"{q.get('number', '')}{q.get('unit', '')}"
        meters = r.get("meters") or 0
        cb = r.get("copybookSnapshot") or {}
        font = cb.get("fontName", "") if cb else ""
        cbn = cb.get("copybookName", "") if cb else ""
        note = (r.get("note") or "").replace("|", "\\|")
        paper = str(paper).replace("|", "\\|")
        cbn = str(cbn).replace("|", "\\|")
        lines.append(
            f"| {date} | {typ} | {paper} | {qty} | {meters:.1f} | {font} | {cbn} | {note} |"
        )
    return "\n".join(lines) + "\n"


def main():
    try:
        os.makedirs(OBS_DIR, exist_ok=True)
        # 库存
        try:
            inv = fetch_json(REPO_RAW_INV)
            items = inv.get("items", [])
            if items:
                with open(OUT_INV, "w", encoding="utf-8") as f:
                    f.write(inventory_md(items))
                print(f"✓ 已更新 {OUT_INV}（{len(items)} 条）")
        except Exception as e:
            print(f"⚠ 库存拉取失败：{e}")
        # 记录
        try:
            rec = fetch_json(REPO_RAW_REC)
            records = rec.get("records", [])
            with open(OUT_REC, "w", encoding="utf-8") as f:
                f.write(records_md(records))
            print(f"✓ 已更新 {OUT_REC}（{len(records)} 条）")
        except Exception as e:
            print(f"⚠ 记录拉取失败：{e}")
        return 0
    except Exception as e:
        print(f"✗ 同步失败：{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
