# finance — so sánh mốc trước / sau (GĐ3 Task 8.14)

- Trước: `finance-truoc.json` (chụp 2 lần trên cây = HEAD rbac 26d1bc1f5 / 17158a8c7d trước khi sửa: **0 ô khác** — mốc ổn định).
- Sau: `finance-sau.json` (sau khi đổi code; 77 ô `erp.warranty_payment.*` + `api.bill-payment*` chụp lại sau 2 sửa muộn — WarrantyPayment tên lạ ⇒ false, BillPayment(Authorization)Access).
- Lệnh: `php tests/Support/ScopeSnapshot.php diff --before=finance-truoc.json --after=finance-sau.json` ⇒ **Khác nhau: 0 ô**.

## Kết quả
- 1890 ô (270 route × 7 tài khoản): **1890/1890 khớp**, 0 lệch, không ô U8 (không tài khoản rehearsal nào có mã finance ở phạm vi null).
- Trạng thái trước = sau: {200: 1755, 403: 121, 500: 14}.
- Ô lỗi sẵn cả trước lẫn sau (500): erp.product_import.index, erp.self_inventory_request.page.all.
- Không route nào > 60 s (chậm nhất là trang `show` 6 id ~6–7 s/TK) ⇒ không bỏ route vì nặng.

## Số tiêu biểu (so_dong trước = sau)
- `erp.bill_payment.searchData.all`: pv4=1609, pv3=1312, pv2=0, pv1=0, tron=1609, cty4=0, khong_ma=0
- `erp.bill_payment_request.searchData.all`: pv4=5067, pv3=4620, pv2=2199, pv1=2, tron=5067, cty4=0, khong_ma=0
- `erp.product_import_request.searchData.all`: pv4=15451, pv3=10482, pv2=2121, pv1=165, tron=15451, cty4=0, khong_ma=0
- `erp.warehouse_import.searchData.all`: pv4=11557, pv3=7306, pv2=7306, pv1=0, tron=11557, cty4=0, khong_ma=0
- `api.bill-payments.index`: pv4=1609, pv3=1312, pv2=0, pv1=0, tron=1609, cty4=0, khong_ma=0
- `api.product-imports.index`: pv4=15770, pv3=10721, pv2=0, pv1=0, tron=15770, cty4=0, khong_ma=0
- `erp.home.approveList`: pv4=100, pv3=37, pv2=25, pv1=16, tron=76, cty4=5, khong_ma=0

## Phủ thêm bằng golden (code cũ ↔ code mới, cấp theo TỪNG mã)
- ERP `tests/Feature/Rbac/FinanceScopeConversionTest`: 298 ca (searchByFilter × loại, canX × 13 trạng thái × 3 biến thể, 41 trang blade qua HTTP — cờ + băm tập link menu, approveList) × mức none/flat/mix/only:mã/mã@s4…s1/null/c2 = 2.111 ô, sinh từ cây HEAD (gồm blade) — khớp.
- hrm-api `tests/Feature/Rbac/FinanceScopeConversionTest`: 244 ca × mức theo từng mã = 2.356 ô, sinh từ bản HEAD các file đã đổi (`RBAC_LEGACY_SRC`) — khớp.
