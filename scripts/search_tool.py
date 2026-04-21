#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🦞 小龙虾技能 — 通用汉字规范表 · 快速检索工具
================================================
Usage:
    python3 scripts/search_tool.py --query 龙
    python3 scripts/search_tool.py --pinyin long
    python3 scripts/search_tool.py --strokes 8
    python3 scripts/search_tool.py --level 3
    python3 scripts/search_tool.py --polyphonic
    python3 scripts/search_tool.py --stats

示例组合查询：
    python3 scripts/search_tool.py --strokes 8 --level 1
"""

import json
import argparse
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
FULL_JSON = os.path.join(DATA_DIR, "full_table_index.json")
LEVEL_JSON = {
    1: os.path.join(DATA_DIR, "level_1.json"),
    2: os.path.join(DATA_DIR, "level_2.json"),
    3: os.path.join(DATA_DIR, "level_3.json"),
}

LEVEL_LABELS = {1: "一级（常用）", 2: "二级（较常用）", 3: "三级（专门用字）"}


def load_all() -> list[dict]:
    """加载全量数据，优先读 full_table_index.json，否则合并三级 JSON"""
    if os.path.exists(FULL_JSON):
        with open(FULL_JSON, encoding="utf-8") as f:
            return json.load(f)
    data = []
    for lv in [1, 2, 3]:
        path = LEVEL_JSON[lv]
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data.extend(json.load(f))
    return data


def fmt_entry(e: dict) -> str:
    poly = "（多音字）" if e.get("polyphonic") else ""
    return (
        f"  [{e['id']}] {e['char']}  "
        f"拼音: {e['pinyin']:<10} "
        f"笔画: {e['strokes']:>2}  "
        f"级别: {LEVEL_LABELS.get(e['level'], '?')} {poly}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="🦞 通用汉字规范表快速检索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--query", "-q", help="按汉字查询（支持多字，如 '龙虾'）")
    parser.add_argument("--pinyin", "-p", help="按拼音首字母或拼音查询（如 'long' 或 'L'）")
    parser.add_argument("--strokes", "-s", type=int, help="按笔画数查询")
    parser.add_argument("--level", "-l", type=int, choices=[1, 2, 3], help="按级别筛选")
    parser.add_argument("--polyphonic", action="store_true", help="仅列出多音字")
    parser.add_argument("--stats", action="store_true", help="显示字表统计信息")
    parser.add_argument("--limit", type=int, default=50, help="最多输出条数（默认50）")
    args = parser.parse_args()

    data = load_all()
    if not data:
        print("❌ 数据文件未找到，请先运行 python3 scripts/build_data.py")
        return

    if args.stats:
        print(f"\n📊 通用规范汉字表统计")
        print(f"{'─'*45}")
        for lv in [1, 2, 3]:
            cnt = sum(1 for d in data if d["level"] == lv)
            print(f"  {LEVEL_LABELS[lv]:<14}: {cnt:>5} 字")
        poly_cnt = sum(1 for d in data if d.get("polyphonic"))
        strk_max = max(d["strokes"] for d in data)
        print(f"  {'多音字合计':<14}: {poly_cnt:>5} 字")
        print(f"  {'最大笔画数':<14}: {strk_max:>5} 画")
        print(f"  {'总计':<14}: {len(data):>5} 字")
        print(f"{'─'*45}\n")
        return

    results = data

    # 多条件过滤
    if args.query:
        chars = set(args.query)
        results = [r for r in results if r["char"] in chars]

    if args.pinyin:
        kw = args.pinyin.upper()
        results = [r for r in results
                   if kw in r["pinyin"].upper() or kw == r["initial"].upper()]

    if args.strokes is not None:
        results = [r for r in results if r["strokes"] == args.strokes]

    if args.level:
        results = [r for r in results if r["level"] == args.level]

    if args.polyphonic:
        results = [r for r in results if r.get("polyphonic")]

    if not results:
        print("🔍 未找到匹配结果。")
        return

    print(f"\n🦞 查询结果（共 {len(results)} 条，显示前 {min(len(results), args.limit)} 条）：")
    print("─" * 65)
    for e in results[: args.limit]:
        print(fmt_entry(e))
    if len(results) > args.limit:
        print(f"  ... 还有 {len(results) - args.limit} 条，用 --limit N 查看更多")
    print()


if __name__ == "__main__":
    main()
