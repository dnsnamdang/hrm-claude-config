# Fix — Số tiền thanh toán không reload khi điều chỉnh giá trị HĐ

## Triệu chứng
Tab "Điều khoản thanh toán": cột **Số tiền** (= % × giá trị HĐ) tự cập nhật khi điều chỉnh giá trị HĐ (giảm giá, doanh số vượt trội, dịch vụ đi kèm, chi phí khác, vận chuyển), nhưng cột **Số tiền thanh toán** giữ giá trị cũ → tổng lệch → chặn "Tổng số tiền thanh toán phải bằng tổng số tiền".

## Root cause
JS class payment: cột "Số tiền" = `payment_amount` (luôn tính theo `total_after_vat`), cột "Số tiền thanh toán" = `amount` (getter trả `_amount` đã set, chỉ default = payment_amount khi `_amount` chưa set). Khi `_amount` đã có giá trị, lúc giá trị HĐ đổi `amount` không theo.

Phụ (WrServiceContract): `WRServiceContractPayment` getter `amount`/`amount2` dùng nhầm `this.parent.total_after_vat` (class cha `WRInformation` expose `total.after_vat`) → default `amount` ra 0.

## Quyết định (ý 1)
Giữ nguyên Số tiền thanh toán đã lưu khi mở lại HĐ (giá trị HĐ không đổi); **chỉ reload = Số tiền khi giá trị HĐ thực sự bị điều chỉnh trong phiên**. Thực hiện bằng `$watch` giá trị HĐ, bỏ qua lần khởi tạo (newVal===oldVal) → không đụng dữ liệu load.

## Phạm vi (ý 2): FirmContract + WrServiceContract

## Fix
- [x] `partials/classes/sale/firm/contract/FirmContract.blade.php` — `after()`: `$watch(total_after_vat)`, đổi → set mỗi payment `_amount = null` (getter tự trả về = payment_amount). Phủ cả create/edit/principle (dùng chung class, có `scope`). `payment_manage` truyền option dạng string → `this.scope` undefined → watch không đăng ký (an toàn).
- [x] `customercare/warranty_repair_information_requests/WRInformation.blade.php` — `after()`: `$watch(total.after_vat)` tương tự.
- [x] `customercare/warranty_repair_contracts/WRServiceContractPayment.blade.php` — sửa `total_after_vat` → `total.after_vat` ở `amount` (default) và `amount2`.

## Kiểm thử (user — cần chạy app)
- [ ] HĐ bán: điều chỉnh giảm giá / doanh số vượt trội / dịch vụ / chi phí / vận chuyển → Số tiền thanh toán tự = Số tiền, hết lỗi tổng lệch.
- [ ] HĐ dịch vụ (WrServiceContract): tương tự; default Số tiền thanh toán không còn ra 0.
- [ ] Mở lại HĐ đã lưu (edit/show) mà KHÔNG đổi giá trị → Số tiền thanh toán giữ nguyên giá trị đã lưu.
- [ ] Sửa tay Số tiền thanh toán rồi KHÔNG đổi giá trị HĐ → giá trị sửa tay được giữ; chỉ khi đổi giá trị HĐ mới reset.

### Checkpoint — 2026-06-09
Vừa hoàn thành: thêm $watch reset ở FirmContract + WRInformation; fix typo WRServiceContractPayment
Bước tiếp theo: user chạy thử 4 ca kiểm thử
Blocked:
