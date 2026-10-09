# Plan — Lọc kho hàng gửi (consignment)

## Bug fix 2026-09-25 — dropdown "Kho kế toán" rỗng ở phiếu xuất bán hàng

**Triệu chứng:** màn Tạo phiếu xuất hàng (PDNXK-35422, type 14 "Xuất bán hàng", cty 4)
báo "No results found" ở ô Kho kế toán → không tạo/duyệt được phiếu.

**Root cause:** `consignment_warehouse_js.blade.php` hardcode `CONSIGNMENT_TYPE_IDS = [14,12]`
dùng CHUNG cho cả màn nhập lẫn xuất. Nhưng ID 14 có 2 nghĩa (public/js/constant.js):
- EXPORT_TYPES: 14 = "Xuất bán hàng" (bình thường), 12 = "Xuất hàng gửi"
- IMPORT_TYPES: 14 = "Nhập hàng gửi"

→ Trên màn xuất, type 14 (Xuất bán hàng) bị coi nhầm là "loại gửi" → đòi kho ∈
`companies.consignment_warehouse_ids` (chưa cty nào cấu hình) → lọc rỗng. Lỗi HỆ THỐNG:
mọi phiếu "Xuất bán hàng" đều không chọn được kho. Regression từ commit merge 88bb8558d7.

**Fix (FE blade only, không đụng DB):**
- [x] `consignment_warehouse_js.blade.php` nhận `$direction` → export: `[12]`, import: `[14]`
- [x] 4 chỗ `@include` truyền `direction`: product_exports/{create,edit} = 'export';
      product_imports/{create,edit} = 'import'
- [x] Blade compile sạch (`compileString` + `php -l` OK)

**Kiểm chứng (data hrm_erp_gop, read-only):** cty 4 / kho 4 có acc-wh SG01(7), SG02(8) status=1;
với fix, type 14 export → isGuiType=false → hiện SG01/SG02. ✓

**Còn lại:** reload trình duyệt (blade tự recompile). Không cần cache:clear. Chưa commit.
