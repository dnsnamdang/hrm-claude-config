#!/usr/bin/env bash
# =============================================================================
# build_hrm_views.sh — Dựng schema VIEW cho HRM chạy trên DB đã merge (CÁCH A)
# =============================================================================
# Ý tưởng: sau khi gộp DB (base = ERP), 23 bảng HRM bị đổi tên -> hrm_*.
# Thay vì sửa ~150 điểm code HRM, tạo 1 schema view (hrm_view) chứa view 1-1:
#   - 23 bảng TÁCH  -> view trỏ  <merged>.hrm_<ten>
#   - mọi bảng khác -> view trỏ  <merged>.<ten>   (passthrough)
# HRM chỉ đổi DB_DATABASE = hrm_view (0 dòng code sửa). View 1-1 nên
# INSERT/UPDATE/DELETE + auto_increment vẫn chạy (đã smoke-test).
#
# CÁCH DÙNG:
#   ./build_hrm_views.sh <merged_schema> <view_schema> <table_list_file> -- <mysql client args...>
# VÍ DỤ (local):
#   ./build_hrm_views.sh erp_hrm_check hrm_view hrm-view-tables.txt -- -h127.0.0.1 -P3306 -uroot
# VÍ DỤ (server test): thay -h -u -p cho đúng.
#
# table_list_file = hrm-view-tables.txt (snapshot 639 tên bảng HRM gốc, kèm repo).
#   Vì sau khi merge_prod chạy, schema hrm_pro rỗng -> KHÔNG lấy list từ đó được nữa,
#   phải dùng file snapshot này.
# =============================================================================
set -euo pipefail

MERGED="${1:?Thiếu tên merged schema (vd erp_hrm_check)}"
VIEWDB="${2:?Thiếu tên view schema (vd hrm_view)}"
LIST="${3:?Thiếu file danh sách bảng (vd hrm-view-tables.txt)}"
shift 3
# bỏ dấu -- ngăn cách nếu có
[ "${1:-}" = "--" ] && shift
MYSQL_ARGS=("$@")

[ -f "$LIST" ] || { echo "LỖI: không thấy file '$LIST'"; exit 1; }

# 23 bảng TÁCH (khớp $TACH trong merge_prod.php)
TACH="company_employees company_roles customer_activity_types customer_business_fields \
customer_contact_has_bank_accounts customer_has_bank_accounts customer_has_vehicle_manufacts \
delivery_places employee_has_permissions employee_has_roles employee_manage_departments \
employees files groups module_mappings nations permissions print_templates \
role_has_permissions roles scopes settlement_contract_employees settlement_contracts"

is_tach(){ for t in $TACH; do [ "$t" = "$1" ] && return 0; done; return 1; }

# Sinh DDL ra biến, rồi nạp 1 lần
gen_sql(){
  echo "CREATE DATABASE IF NOT EXISTS \`$VIEWDB\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
  local n=0
  while IFS= read -r tbl; do
    tbl="$(echo "$tbl" | tr -d '[:space:]')"
    [ -z "$tbl" ] && continue
    if is_tach "$tbl"; then tgt="hrm_$tbl"; else tgt="$tbl"; fi
    echo "CREATE OR REPLACE SQL SECURITY DEFINER VIEW \`$VIEWDB\`.\`$tbl\` AS SELECT * FROM \`$MERGED\`.\`$tgt\`;"
    n=$((n+1))
  done < "$LIST"
  echo "-- Tổng view: $n" >&2
}

echo ">> Dựng $VIEWDB (view trỏ $MERGED) từ $LIST ..."
gen_sql | mysql "${MYSQL_ARGS[@]}"
CNT=$(mysql "${MYSQL_ARGS[@]}" -N -e "SELECT COUNT(*) FROM information_schema.views WHERE table_schema='$VIEWDB'")
echo ">> XONG. Số view trong $VIEWDB = $CNT"
echo ">> HRM: đổi DB_DATABASE=$VIEWDB. ERP: giữ DB_DATABASE=$MERGED. (xem HUONG-DAN-VIEW.md)"
