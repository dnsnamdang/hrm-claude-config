#!/bin/bash
# 1 BƯỚC TEST = 1 lần gọi script này, ngay sau MỖI thao tác (chạm / vuốt / gõ / hot reload).
#   step.sh <run.log> "<tên bước>" [giây chờ, mặc định 1.5]
# Làm 3 việc:
#   1. Chụp màn, thu về đúng kích thước ĐIỂM (393 rộng) → toạ độ trên ảnh = toạ độ chạm mobile-mcp, không phải nhân hệ số.
#   2. In MỌI lỗi Flutter mới xuất hiện trong run.log kể từ bước trước (exception, tràn layout, setState sau dispose…).
#      Bản debug chỉ in lỗi ra log rồi vẫn vẽ tiếp; bản release cùng lỗi đó = đứng hình / ô xám → CÓ LỖI LÀ BƯỚC FAIL.
#   3. In các request API mới (để biết thao tác có gọi đúng API, có lỗi 4xx/5xx không).
# Ảnh: <thư mục run.log>/shots/NN-<tên>.png  — đọc ảnh bằng Read để kiểm bằng mắt.
set -u
LOG=${1:?run.log}; NAME=${2:-step}; WAIT=${3:-1.5}
UDID=${UDID:-$(xcrun simctl list devices booted | grep -oE '[0-9A-F-]{36}' | head -1)}
DIR=$(dirname "$LOG"); MARK="$LOG.mark"; mkdir -p "$DIR/shots"
sleep "$WAIT"
N=$(ls "$DIR/shots" | wc -l | tr -d ' '); N=$((N + 1))
OUT=$(printf '%s/shots/%02d-%s.png' "$DIR" "$N" "$(echo "$NAME" | tr ' /' '__')")
xcrun simctl io "$UDID" screenshot "$OUT" >/dev/null 2>&1
sips --resampleWidth "${POINT_WIDTH:-393}" "$OUT" >/dev/null 2>&1
FROM=$(cat "$MARK" 2>/dev/null || echo 0); TO=$(wc -l < "$LOG" | tr -d ' '); echo "$TO" > "$MARK"
NEW=$(sed -n "$((FROM + 1)),${TO}p" "$LOG")
ERR=$(echo "$NEW" | grep -E "EXCEPTION CAUGHT|Another exception|was thrown|RenderFlex overflowed|overflowed by|setState\(\) called after dispose|Unhandled Exception|Failed assertion|Null check operator|type '.*' is not a subtype|RangeError|Bad state" | sort | uniq -c | head -20)
API=$(echo "$NEW" | grep -E "^(🎉|⛔️) (GET|POST|PUT|PATCH|DELETE) " | sed -E 's/\?.{60,}//' | cut -c1-140 | uniq -c | head -15)
APIERR=$(echo "$NEW" | grep -E "^⛔️ (Error Code|Json):" | cut -c1-200 | head -6)
echo "== BƯỚC $N: $NAME  →  $OUT"
if [ -n "$ERR" ]; then echo "❌ LỖI FLUTTER MỚI (bước FAIL, đọc run.log dòng $((FROM + 1))–$TO):"; echo "$ERR"; else echo "✅ không có lỗi Flutter mới"; fi
[ -n "$API" ] && { echo "API (🎉 = 2xx, ⛔️ = lỗi):"; echo "$API"; }
[ -n "$APIERR" ] && { echo "⚠️ API LỖI — màn PHẢI hiện thông báo lỗi đúng chỗ, tắt trạng thái đang tải:"; echo "$APIERR"; }
exit 0
