---
name: 通用汉字规范表
version: 1.0.0
description: >
  通用规范汉字表技能包（8105字，2013国标版）。支持按汉字/拼音/笔画/级别/多音字检索，
  提供 JSON/CSV/SQL/Markdown 多格式导出，以及文本规范性校验。
  触发词：汉字检索、规范汉字、查汉字、汉字级别、多音字、笔画查询、汉字规范性、
  通用规范字表、GB/T13000、国标汉字、汉字导出、字表数据。
author: 锐道科技部
license: MIT
---

# 🦞 通用汉字规范表技能包

## 概述

本技能包收录《通用规范汉字表》（2013版）全部 8105 个汉字，
内置完整的检索、处理和导出工具链（小龙虾技能）。

## 数据文件

| 文件 | 内容 | 字数 |
|:---|:---|:---:|
| `data/level_1.json` | 一级字表 | 3500 |
| `data/level_2.json` | 二级字表 | 3000 |
| `data/level_3.json` | 三级字表 | 1605 |
| `data/full_table.csv` | 完整汇总表 | 8105 |
| `data/full_table_index.json` | 快查索引 | 8105 |

## 核心脚本

### 初始化（首次使用）

```bash
python3 scripts/build_data.py data/raw.csv
bash scripts/formatter.sh all
```

### 检索

```bash
python3 scripts/search_tool.py --query <汉字>
python3 scripts/search_tool.py --strokes <笔画数>
python3 scripts/search_tool.py --level <1|2|3>
python3 scripts/search_tool.py --polyphonic
python3 scripts/search_tool.py --stats
```

### 处理与导出

```bash
python3 scripts/processor.py --check-text "<文本>"   # 规范性校验
python3 scripts/processor.py --export-md <1|2|3>     # 导出 Markdown
python3 scripts/processor.py --export-sql             # 导出 SQL
python3 scripts/processor.py --stroke-dist            # 笔画分布
```

## 数据字段

```
id         序号（4位补零）
char       汉字（UTF-8）
pinyin     标准拼音（多音字用 | 分隔）
initial    首字母（大写）
strokes    楷书笔画数
level      字表级别 1/2/3
polyphonic 是否多音字（bool）
```

## 常见问题

- 数据文件缺失：运行 `python3 scripts/build_data.py`
- Excel 乱码：使用 `bash scripts/formatter.sh csv` 生成 BOM 版本
- 导入数据库：`python3 scripts/processor.py --export-sql` 后执行 SQL 文件
