#!/usr/bin/env bash
# 🦞 通用汉字规范表 · 自动化格式化工具
# Usage: bash scripts/formatter.sh [all|json|csv|validate]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR/.."
DATA="$ROOT/data"
OUT="$ROOT/output"

mkdir -p "$OUT"

CYAN='\033[0;36m'; GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
log()  { echo -e "${CYAN}[formatter]${NC} $*"; }
ok()   { echo -e "${GREEN}✅${NC} $*"; }
fail() { echo -e "${RED}❌${NC} $*"; exit 1; }

# ─── 检查 python3 ─────────────────────────────────────────
PY=$(which python3 2>/dev/null || which python 2>/dev/null || echo "")
[ -z "$PY" ] && fail "未找到 Python，请先安装 Python 3.x"

# ─── 子命令 ───────────────────────────────────────────────

do_json() {
    log "格式化 JSON 文件（pretty-print）..."
    for f in "$DATA"/level_*.json; do
        tmp=$(mktemp)
        "$PY" -c "import json,sys; d=json.load(open(sys.argv[1],'r',encoding='utf-8')); json.dump(d,open(sys.argv[1],'w',encoding='utf-8'),ensure_ascii=False,indent=2); print(sys.argv[1])" "$f"
        ok "$(basename "$f")"
    done
}

do_csv() {
    log "将 full_table.csv 转换为带 BOM 的 UTF-8（Excel 友好）..."
    SRC="$DATA/full_table.csv"
    DST="$OUT/full_table_excel.csv"
    [ -f "$SRC" ] || fail "full_table.csv 不存在，请先运行 build_data.py"
    "$PY" - <<'PYEOF'
import csv, os
src = os.path.join(os.environ.get("DATA","data"), "full_table.csv")
dst = os.path.join(os.environ.get("OUT","output"), "full_table_excel.csv")
with open(src, encoding="utf-8") as fi, open(dst, "w", encoding="utf-8-sig", newline="") as fo:
    fo.write(fi.read())
print(f"  → {dst}")
PYEOF
    ok "Excel 友好版已生成 → output/full_table_excel.csv"
}

do_validate() {
    log "校验 JSON 数据完整性..."
    "$PY" - <<'PYEOF'
import json, os, sys
DATA = os.environ.get("DATA", "data")
total = 0
for lv, expected in [(1,3500),(2,3000),(3,1605)]:
    path = os.path.join(DATA, f"level_{lv}.json")
    if not os.path.exists(path):
        print(f"  ❌ level_{lv}.json 不存在"); sys.exit(1)
    data = json.load(open(path, encoding="utf-8"))
    total += len(data)
    status = "✅" if len(data)==expected else "⚠️"
    print(f"  {status} level_{lv}.json: {len(data)} 字（期望 {expected}）")
print(f"\n  总计 {total}/8105 字")
if total != 8105:
    print("  ⚠️  总数不符，请检查数据源！"); sys.exit(1)
else:
    print("  ✅ 数据校验通过！")
PYEOF
}

do_build_index() {
    log "构建查询索引..."
    DATA="$DATA" "$PY" "$SCRIPT_DIR/processor.py" --build-index
}

# ─── 主流程 ───────────────────────────────────────────────
CMD="${1:-all}"
export DATA OUT

case "$CMD" in
    json)      do_json ;;
    csv)       do_csv ;;
    validate)  do_validate ;;
    index)     do_build_index ;;
    all)
        do_validate
        do_json
        do_csv
        do_build_index
        ok "全部格式化完成！"
        ;;
    *)
        echo "Usage: bash formatter.sh [all|json|csv|validate|index]"
        exit 1
        ;;
esac
