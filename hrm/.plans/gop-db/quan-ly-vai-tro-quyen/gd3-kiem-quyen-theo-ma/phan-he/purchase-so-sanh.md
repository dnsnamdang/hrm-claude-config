# purchase — so sánh mốc trước / sau (GĐ3 Task 8.15)

- Trước: `purchase-truoc.json` (chụp 2 lần trên cây = HEAD rbac TanPhatDev e62a1448fe trước khi sửa: **0 ô khác** — mốc ổn định).
- Sau: `purchase-sau.json` (sau khi đổi code; 35 ô `erp.buy_service_contract.*` chụp lại sau sửa muộn biến phạm vi ở nhánh for-approve của `BuyServiceContract::searchByFilter`).
- Lệnh: `php tests/Support/ScopeSnapshot.php diff --before=purchase-truoc.json --after=purchase-sau.json` ⇒ **Khác nhau: 0 ô**.

## Kết quả
- 1694 ô (242 route × 7 tài khoản, toàn ERP): **1694/1694 khớp**, 0 lệch, không ô U8 (không tài khoản rehearsal nào có mã purchase ở phạm vi null).
- Trạng thái trước = sau: {200: 1674, 500: 20} = {200: 1674, 500: 20}.
- Ô lỗi sẵn cả trước lẫn sau (500): erp.inland_purchase_invoice.page.forApprove, erp.mw.orders/inland_order_notification_new/forCreator, erp.mw.orders/order_notification2/forCreator, erp.purchase_invoice.page.forApprove, erp.report.compare_supplier_debt_nation.search.
- Không route nào > 60 s (chậm nhất 31 s — trang show 6 id) ⇒ không bỏ route vì nặng.
- 153/242 route cho kết quả khác nhau giữa các tài khoản (mốc có nghĩa); phần còn lại là trang/route không lọc theo quyền (báo cáo duyệt giá mua ngoài, tình trạng trả hàng…) hoặc 7 TK cùng kết quả.

## Số tiêu biểu (so_dong trước = sau)
- `erp.root_order_request.searchData.all`: pv4=7823, pv3=6163, pv2=1235, pv1=243, tron=265, cty4=0, khong_ma=0
- `erp.purchase_invoice.searchData.all`: pv4=1320, pv3=1320, pv2=0, pv1=0, tron=1320, cty4=0, khong_ma=0
- `erp.inland_order_request.searchData.all`: pv4=943, pv3=934, pv2=18, pv1=0, tron=5, cty4=0, khong_ma=0
- `erp.inland_buy_contract_new.searchData.all`: pv4=0, pv3=0, pv2=0, pv1=0, tron=0, cty4=0, khong_ma=0
- `erp.custom_declaration.searchData.all`: pv4=780, pv3=780, pv2=0, pv1=0, tron=780, cty4=0, khong_ma=0
- `erp.insurance_contract.searchData.all`: pv4=0, pv3=0, pv2=0, pv1=0, tron=0, cty4=0, khong_ma=0
- `erp.report.supplier_debt.search`: pv4=3463, pv3=3139, pv2=0, pv1=0, tron=3463, cty4=0, khong_ma=0
- `erp.report.order_product.search`: pv4=0, pv3=0, pv2=0, pv1=4, tron=0, cty4=0, khong_ma=0
- `erp.home.approveList`: pv4=100, pv3=37, pv2=22, pv1=16, tron=29, cty4=0, khong_ma=0

## Phủ thêm bằng golden (code cũ ↔ code mới, cấp theo TỪNG mã)
- ERP `tests/Feature/Rbac/PurchaseScopeConversionTest`: 564 ca (searchByFilter × loại, canX × 13 trạng thái × 3 biến thể, hàm lọc báo cáo công nợ NCC, 98 trang blade/middleware qua HTTP — cờ + băm tập link menu, 18 JSON báo cáo, approveList) × mức none/flat/mix/only:mã/mã@s4…s1/null/c2 = 3.768 ô, sinh từ cây HEAD (gồm blade, 3 lần trùng) — code mới khớp; đối chứng `RBAC_LEGACY_SRC` (bản HEAD 86 file app/) cũng khớp.
- Ca thiếu tài khoản thật (chỉ golden): mã phạm vi null, mã ở công ty khác (c2), từng mã riêng, mức bộ phận cho mã có 4 mức.
