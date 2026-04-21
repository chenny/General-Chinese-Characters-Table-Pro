# 🦞 小龙虾技能使用手册

> 小龙虾（Crayfish）技能是本仓库内置的一套数据处理 & 检索工具链，得名于"小龙虾"——虽然小，但爪子锋利、效率极高，夹住什么就处理什么。

---

## 环境要求

- Python 3.8+（建议 3.10+）
- 无需任何第三方依赖，只用标准库

---

## 快速上手

### Step 1 — 构建数据文件

```bash
# 从原始 CSV 生成分级 JSON + full_table.csv
python3 scripts/build_data.py /path/to/通用规范汉字表.csv

# 构建查询索引（可选，提升 search_tool 速度）
python3 scripts/processor.py --build-index
```

### Step 2 — 检索汉字

```bash
# 查单字
python3 scripts/search_tool.py --query 龙

# 查拼音（支持首字母）
python3 scripts/search_tool.py --pinyin long
python3 scripts/search_tool.py --pinyin L

# 按笔画
python3 scripts/search_tool.py --strokes 8

# 仅三级字
python3 scripts/search_tool.py --level 3

# 多条件组合：8画的一级字
python3 scripts/search_tool.py --strokes 8 --level 1

# 所有多音字
python3 scripts/search_tool.py --polyphonic --limit 100

# 统计信息
python3 scripts/search_tool.py --stats
```

### Step 3 — 数据处理 & 导出

```bash
# 笔画分布统计
python3 scripts/processor.py --stroke-dist

# 导出一级字 Markdown 表格
python3 scripts/processor.py --export-md 1

# 导出 SQL 建表 + INSERT
python3 scripts/processor.py --export-sql

# 检测一段文字的规范性
python3 scripts/processor.py --check-text "这段文字包含𠅻等生僻字吗？"
```

### Step 4 — 一键格式化

```bash
# 格式化所有数据文件 + 生成 Excel 友好 CSV + 校验数据完整性
bash scripts/formatter.sh all

# 单独运行某一步
bash scripts/formatter.sh validate   # 只校验
bash scripts/formatter.sh csv        # 只生成 Excel 版 CSV
```

---

## 各技能介绍

### 🔍 search_tool.py — 快速检索

| 参数 | 说明 |
|:---|:---|
| `--query` | 按汉字查，可多字同时查 |
| `--pinyin` | 按拼音或首字母查 |
| `--strokes N` | 按笔画数精确匹配 |
| `--level 1/2/3` | 按字表级别筛选 |
| `--polyphonic` | 仅列出多音字 |
| `--stats` | 字表总览统计 |
| `--limit N` | 控制最大输出行数（默认50） |

---

### 🛠️ processor.py — 数据处理器

| 参数 | 说明 |
|:---|:---|
| `--build-index` | 将三级 JSON 合并为统一索引文件 |
| `--export-md LEVEL` | 导出指定级别为 Markdown 表格 |
| `--export-sql` | 生成 MySQL 建表语句 + INSERT |
| `--stroke-dist` | 控制台输出笔画分布柱状图 |
| `--check-text TEXT` | 检测文本中汉字是否在规范表内 |

---

### ⚡ formatter.sh — 自动化流水线

| 命令 | 说明 |
|:---|:---|
| `all` | 完整流水线（推荐初始化时使用） |
| `validate` | 校验三个 JSON 字数是否正确 |
| `json` | 重新 pretty-print 所有 JSON |
| `csv` | 生成 Excel 友好（UTF-8 BOM）CSV |
| `index` | 仅重建查询索引 |

---

## 常见问题

**Q: 运行后提示"数据文件缺失"？**  
A: 请先执行 `python3 scripts/build_data.py /path/to/源文件.csv`

**Q: Excel 打开 CSV 显示乱码？**  
A: 使用 `bash scripts/formatter.sh csv` 生成 `output/full_table_excel.csv`（带 BOM）

**Q: 如何导入 MySQL？**  
A: 先运行 `python3 scripts/processor.py --export-sql`，然后 `mysql -u root -p < output/chinese_chars.sql`

---

> 🦞 **小龙虾语录**：夹住字，就别松手。
