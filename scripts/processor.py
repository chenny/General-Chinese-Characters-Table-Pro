#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小龙虾技能 — 通用汉字规范表 · 数据处理器
=============================================
功能：
  1. 将 full_table.csv 转为带索引的 JSON（加速查询）
  2. 导出 Markdown 格式字表
  3. 导出 SQL INSERT 语句
  4. 统计多音字、笔画分布

Usage:
    python3 scripts/processor.py --build-index          # 构建查询索引
    python3 scripts/processor.py --export-md level_1    # 导出一级字 Markdown
    python3 scripts/processor.py --export-sql           # 导出 SQL
    python3 scripts/processor.py --stroke-dist          # 笔画分布统计
    python3 scripts/processor.py --check-text "这是一段测试文本"  # 检测文本用字规范性
"""

import json
import csv
import argparse
import os
from collections import Counter, defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUT_DIR  = os.path.join(os.path.dirname(__file__), "../output")
os.makedirs(OUT_DIR, exist_ok=True)

LEVEL_NAMES = {1: "level_1", 2: "level_2", 3: "level_3"}
LEVEL_LABELS = {1: "一级（3500字）", 2: "二级（3000字）", 3: "三级（1605字）"}


# ─── 工具函数 ─────────────────────────────────────────────

def load_all() -> list[dict]:
    all_data = []
    for lv in [1, 2, 3]:
        path = os.path.join(DATA_DIR, f"{LEVEL_NAMES[lv]}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                all_data.extend(json.load(f))
    return all_data


def build_char_set(data: list[dict]) -> set[str]:
    return {d["char"] for d in data}


# ─── 子命令实现 ───────────────────────────────────────────

def cmd_build_index(data: list[dict]):
    """构建 full_table_index.json（按 char 索引）"""
    out = os.path.join(DATA_DIR, "full_table_index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"✅ 索引已构建 → {out}（{len(data)} 条）")


def cmd_export_md(data: list[dict], level: int):
    """导出指定级别字表为 Markdown"""
    rows = [d for d in data if d["level"] == level]
    out = os.path.join(OUT_DIR, f"{LEVEL_NAMES[level]}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# 通用规范汉字 {LEVEL_LABELS[level]}\n\n")
        f.write(f"> 共 **{len(rows)}** 字\n\n")
        f.write("| 序号 | 汉字 | 拼音 | 首字母 | 笔画 | 多音字 |\n")
        f.write("|:----:|:----:|:-----|:------:|:----:|:------:|\n")
        for r in rows:
            poly = "✔" if r["polyphonic"] else ""
            f.write(f"| {r['id']} | **{r['char']}** | {r['pinyin']} | {r['initial']} | {r['strokes']} | {poly} |\n")
    print(f"✅ Markdown 已导出 → {out}")


def cmd_export_sql(data: list[dict]):
    """导出 SQL INSERT 语句"""
    out = os.path.join(OUT_DIR, "chinese_chars.sql")
    with open(out, "w", encoding="utf-8") as f:
        f.write("-- 通用规范汉字表 (8105字)\n")
        f.write("CREATE TABLE IF NOT EXISTS chinese_chars (\n")
        f.write("  id       VARCHAR(4)   NOT NULL,\n")
        f.write("  char     VARCHAR(2)   NOT NULL,\n")
        f.write("  pinyin   VARCHAR(32),\n")
        f.write("  initial  VARCHAR(2),\n")
        f.write("  strokes  TINYINT,\n")
        f.write("  level    TINYINT,\n")
        f.write("  polyphonic BOOLEAN,\n")
        f.write("  PRIMARY KEY (id)\n")
        f.write(") CHARACTER SET utf8mb4;\n\n")
        f.write("INSERT INTO chinese_chars VALUES\n")
        rows_sql = []
        for r in data:
            poly = 1 if r["polyphonic"] else 0
            rows_sql.append(
                f"  ('{r['id']}','{r['char']}','{r['pinyin']}','{r['initial']}',{r['strokes']},{r['level']},{poly})"
            )
        f.write(",\n".join(rows_sql) + ";\n")
    print(f"✅ SQL 已导出 → {out}")


def cmd_stroke_dist(data: list[dict]):
    """笔画分布统计"""
    dist = Counter(d["strokes"] for d in data)
    print(f"\n{'─'*40}")
    print(f"  {'笔画数':<6}  {'字数':>6}  {'分布'}")
    print(f"{'─'*40}")
    for stroke in sorted(dist.keys()):
        bar = "█" * (dist[stroke] // 10)
        print(f"  {stroke:<6}  {dist[stroke]:>6}  {bar}")
    print(f"{'─'*40}\n")


def cmd_check_text(data: list[dict], text: str):
    """检测文本中的字，标注是否在规范表内及级别"""
    char_map = {d["char"]: d for d in data}
    print(f"\n🔍 文本规范性检测：「{text}」\n")
    unknown = []
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":  # 仅检测 CJK 汉字
            if ch in char_map:
                d = char_map[ch]
                print(f"  ✅ {ch}  级别={d['level']}  拼音={d['pinyin']}  笔画={d['strokes']}")
            else:
                unknown.append(ch)
                print(f"  ❓ {ch}  —— 不在规范表内")
    if unknown:
        print(f"\n⚠️  共 {len(unknown)} 字不在8105字规范表内：{''.join(unknown)}")
    else:
        print(f"\n✅ 所有汉字均在规范表内")


# ─── 入口 ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="🦞 通用汉字规范表 · 数据处理器")
    parser.add_argument("--build-index", action="store_true", help="构建查询索引 JSON")
    parser.add_argument("--export-md",   type=int, choices=[1,2,3], metavar="LEVEL", help="导出指定级别的 Markdown")
    parser.add_argument("--export-sql",  action="store_true", help="导出 SQL INSERT 语句")
    parser.add_argument("--stroke-dist", action="store_true", help="笔画数分布统计")
    parser.add_argument("--check-text",  type=str, metavar="TEXT", help="检测文本中汉字的规范性")
    args = parser.parse_args()

    data = load_all()
    if not data:
        print("❌ 数据文件缺失，请先运行 python3 scripts/build_data.py")
        return

    if args.build_index:
        cmd_build_index(data)
    if args.export_md:
        cmd_export_md(data, args.export_md)
    if args.export_sql:
        cmd_export_sql(data)
    if args.stroke_dist:
        cmd_stroke_dist(data)
    if args.check_text:
        cmd_check_text(data, args.check_text)
    if not any([args.build_index, args.export_md, args.export_sql,
                args.stroke_dist, args.check_text]):
        parser.print_help()


if __name__ == "__main__":
    main()
