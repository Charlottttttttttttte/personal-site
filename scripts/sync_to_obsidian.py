#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临池录库存 · Mac 自动拉取脚本
从 GitHub 拉取 data/shufa-inventory.json，生成 Obsidian《临池录/库存总览.md》。

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

REPO_RAW = "https://raw.githubusercontent.com/Charlottttttttttttte/personal-site/main/data/shufa-inventory.json"
OBS_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Charlotte/临池录"
)
OUT_FILE = os.path.join(OBS_DIR, "库存总览.md")

TYPE_LABEL = {"长卷": "长卷", "刀纸": "刀纸", "条屏": "条屏"}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "shufa-sync"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_md(items):
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


def main():
    try:
        data = fetch_json(REPO_RAW)
        items = data.get("items", [])
        if not items:
            print("仓库数据为空，跳过写入")
            return 1
        os.makedirs(OBS_DIR, exist_ok=True)
        with open(OUT_FILE, "w", encoding="utf-8") as f:
            f.write(to_md(items))
        print(f"✓ 已更新 {OUT_FILE}（{len(items)} 条）")
        return 0
    except Exception as e:
        print(f"✗ 拉取失败：{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
