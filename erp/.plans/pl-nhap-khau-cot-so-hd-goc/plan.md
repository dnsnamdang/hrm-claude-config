# Plan — PL nhập khẩu: thêm cột + bộ lọc "Số HĐ gốc"

Màn "Danh sách phụ lục bổ sung HĐ nhập khẩu" (`buy_contract2`, type=annex_addition / PL_BO_SUNG=2)
thiếu cột "Số HĐ gốc" và bộ lọc theo số HĐ gốc. Khuôn theo inland (type 4/5).
DB `erp_new`: 195/195 phụ lục đã có sẵn `parent_code` → chỉ hiển thị/lọc, không đụng data.

## Tasks — ĐÃ XONG
- [x] 1. `resources/views/orders/buy_contract2/index.blade.php` — khi `type=='annex_addition'`:
  cột `parent_code`="Số hợp đồng" + `code`="Số phụ lục"; thêm filter text `parent_code`. Type khác giữ nguyên.
- [x] 2. `BuyContract2Controller@searchData` — thêm `editColumn('parent_code')` (link show) + đưa `parent_code` vào `rawColumns`.
- [x] 3. `BuyContract2::searchByFilter` — thêm nhánh lọc `parent_code` (dùng đúng `$request->parent_code`).
- [x] 4. Fix bug sẵn ở inland `InlandBuyContractNew.php:890` — filter `parent_code` đang `like` theo `$request->code` (copy nhầm biến) → sửa thành `$request->parent_code`.

## Kiểm chứng
- Lint sạch 3 file PHP.
- Filter `parent_code LIKE %GAOCHANG%` trên erp_new (type=2) → 14 phụ lục đúng (gồm record 877).
- Data không đụng (195/195 phụ lục NK đã có sẵn `parent_code`).
