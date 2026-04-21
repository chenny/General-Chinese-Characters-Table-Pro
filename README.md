# 🦞 通用汉字规范表 · 小龙虾技能库
# General-Chinese-Characters-Table-Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![字符数](https://img.shields.io/badge/%E6%8E%B6%E5%BD%95%E6%B1%89%E5%AD%97-8105%E5%AD%97-red.svg)]()
[![数据来源](https://img.shields.io/badge/%E6%95%B0%E6%8D%AE%E6%9D%A5%E6%BA%90-%E5%9B%BD%E5%AE%B6%E8%AF%AD%E5%A7%94-green.svg)]()

```
          ___
     ====/ 📖 \====
    ( 🦞  看字典  )
     \__________/
      ||      ||
    ~~~~~  ~~~~~
  "夹住字，就别松手！"
```

> 本仓库收录《通用规范汉字表》（2013版）全部 **8105 个** 规范汉字，
> 并内置一套 **🦞 小龙虾技能** 工具链，提供快速检索、多格式导出、规范性校验等能力。

---

## 📊 字表概览

| 级别 | 数量 | 说明 |
|:---:|:---:|:---|
| 🔴 一级字表 | **3500** 字 | 覆盖日常出版物 99% 以上用字 |
| 🟡 二级字表 | **3000** 字 | 满足一般性阅读需求 |
| 🔵 三级字表 | **1605** 字 | 专门术语、人名、地名等特殊用字 |
| **合计** | **8105** 字 | GB/T 13000 · 国家标准 |

---

## 📁 目录结构

```text
General-Chinese-Characters-Table-Pro/
├── data/
│   ├── level_1.json          # 一级字表（3500字）
│   ├── level_2.json          # 二级字表（3000字）
│   ├── level_3.json          # 三级字表（1605字）
│   ├── full_table.csv        # 完整汇总表（8105字）
│   └── raw.csv               # 原始数据备份
├── scripts/
│   ├── build_data.py         # 🛠️ 数据初始化（CSV → JSON）
│   ├── search_tool.py        # 🔍 快速检索工具
│   ├── processor.py          # ⚙️ 数据处理 & 导出
│   └── formatter.sh          # ⚡ 自动化格式化流水线
├── docs/
│   ├── intro.md              # 规范表背景介绍
│   └── crayfish_guide.md     # 🦞 小龙虾技能使用手册
├── output/                   # 生成文件输出目录
├── LICENSE
└── README.md
```

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/General-Chinese-Characters-Table-Pro.git
cd General-Chinese-Characters-Table-Pro
```

### 2. 初始化数据（首次使用）

```bash
# 如果仓库内已有 data/*.json，可跳过此步
python3 scripts/build_data.py data/raw.csv

# 一键格式化 + 校验 + 构建索引
bash scripts/formatter.sh all
```

### 3. 使用小龙虾检索

```bash
# 查"龙"字
python3 scripts/search_tool.py --query 龙

# 查 8 画的所有一级字
python3 scripts/search_tool.py --strokes 8 --level 1

# 查所有多音字（限制显示50条）
python3 scripts/search_tool.py --polyphonic

# 字表统计总览
python3 scripts/search_tool.py --stats
```

**示例输出：**
```
🦞 查询结果（共 1 条，显示前 1 条）：
─────────────────────────────────────────────────────────────────
  [3126] 龙  拼音: lóng       笔画:  5  级别: 一级（常用）
```

### 4. 导出与校验

```bash
# 检测一段文字的规范性
python3 scripts/processor.py --check-text "龙虾味道鲜美"

# 导出一级字 Markdown 表格
python3 scripts/processor.py --export-md 1

# 导出 SQL
python3 scripts/processor.py --export-sql

# 笔画分布统计
python3 scripts/processor.py --stroke-dist
```

---

## 🌟 小龙虾技能清单

| 技能名称 | 文件 | 核心能力 |
|:---|:---|:---|
| 🔍 **快速检索** | `search_tool.py` | 按汉字/拼音/笔画/级别/多音字多维检索 |
| ⚙️ **数据处理** | `processor.py` | 建索引、导出 MD/SQL、规范性校验、笔画统计 |
| ⚡ **格式化流水线** | `formatter.sh` | 自动校验 + 格式化 + 生成 Excel 友好 CSV |
| 🏗️ **数据构建** | `build_data.py` | 原始 CSV → 分级 JSON + full_table.csv |

---

## 📦 数据字段说明

```json
{
  "id":        "3126",        // 序号（4位补零）
  "char":      "龙",          // 汉字
  "pinyin":    "lóng",        // 标准拼音（多音字用 | 分隔）
  "initial":   "L",           // 首字母（大写）
  "strokes":   5,             // 楷书笔画数
  "level":     1,             // 字表级别：1/2/3
  "polyphonic": false         // 是否多音字
}
```

---

## 🎯 应用场景

- 📚 **出版校验**：自动检测稿件中是否有非规范字
- 🎓 **教育测评**：按级别出题，测试学生识字掌握情况
- 🖥️ **字体设计**：字库最小化，按级别分层加载
- 🔍 **NLP 预处理**：语料规范化，过滤超纲用字
- 🌐 **国际中文教育**：HSK 词表与规范字表的交叉分析

---

## 📄 数据来源

数据依据《通用规范汉字表》（2013年6月，国家语言文字工作委员会）官方文本数字化整理。  
如有出入，以官方原始文件为准。

---

## 📜 License

[MIT License](LICENSE) — 自由使用，欢迎 Star & Fork 🦞

---

```
    🦞 小龙虾寄语：
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    汉字八千，字字有根。
    规范立身，文明传承。
    小龙虾虽小，夹字不松手！
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
