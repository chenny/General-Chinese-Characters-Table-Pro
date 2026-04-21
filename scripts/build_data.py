#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_data.py — 构建 data/ 目录下的 JSON 和 CSV 文件
Usage: python3 scripts/build_data.py <源CSV路径>
"""

import csv
import json
import sys
import os
import shutil

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "../data/raw.csv")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

buckets = {1: [], 2: [], 3: []}
all_rows = []

with open(SRC, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        level = int(row.get("几级字", 0) or 0)
        polyphonic = int(row.get("多音数", 0) or 0)
        entry = {
            "id":        row.get("序号", "").strip(),
            "char":      row.get("汉字", "").strip(),
            "pinyin":    row.get("发音", "").strip(),
            "initial":   row.get("首字母", "").strip(),
            "strokes":   int(row.get("笔画数", 0) or 0),
            "level":     level,
            "polyphonic": polyphonic > 1,
        }
        all_rows.append(entry)
        if level in buckets:
            buckets[level].append(entry)

# 写分级 JSON
level_names = {1: "level_1", 2: "level_2", 3: "level_3"}
for lv, rows in buckets.items():
    path = os.path.join(DATA_DIR, f"{level_names[lv]}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"✅ {level_names[lv]}.json — {len(rows)} 字")

# 写完整 CSV（full_table.csv）
full_csv = os.path.join(DATA_DIR, "full_table.csv")
with open(full_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id","char","pinyin","initial","strokes","level","polyphonic"])
    writer.writeheader()
    writer.writerows(all_rows)
print(f"✅ full_table.csv — 共 {len(all_rows)} 字")

# 复制原始文件备份
raw_bak = os.path.join(DATA_DIR, "raw.csv")
if os.path.abspath(SRC) != os.path.abspath(raw_bak):
    shutil.copy2(SRC, raw_bak)
    print(f"✅ 原始文件已备份至 data/raw.csv")
