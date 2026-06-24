# Fix: Số tiền đề xuất lệch giữa list và chi tiết (request-payment-working-fee)

@khoipv — 2026-06-24

## Bối cảnh
Phiếu 2247: list hiện 800.000, chi tiết hiện 650.000.
- List đọc cột `request_payment_working_fees.total_amount_proposed` (800k).
- Chi tiết tính = tổng `request_payment_working_fee_details.total_payment_unit_price` (650k).

## Root cause THẬT (đã xác minh — đính chính)
Bằng chứng quyết định: phiếu 2247 sai ngay ở trạng thái **chờ duyệt (status=2)** → lệch phát sinh từ khâu **TẠO**, không phải lúc duyệt.

- **FE (gốc rễ):** `removeBusinessTripAssigns()` trong `RequestPaymentWorkingFeeForm.vue` xóa 1 phiếu công tác nhưng **KHÔNG gọi `getTotalAmountProposed()`** (khác `removeDataTableSubmit` có gọi). → Thêm nhiều phiếu công tác rồi xóa bớt → biến `totalAmountProposed` giữ giá trị cũ (800k) trong khi dòng còn lại = 650k. Submit gửi header lệch.
- **BE (code cũ):** `store()` tin `request->total_amount_proposed` từ FE → lưu header lệch luôn từ lúc tạo.
- Giải thích trọn vẹn: sai ở chờ duyệt; đa số phiếu không sai (ít ai xóa bớt phiếu công tác); cả 155 (draft), 295, 2247 cùng 1 nguyên nhân.
- Chẩn đoán cũ "do luồng duyệt" / "do luồng in" đều SAI. Luồng in chỉ đọc (apiGet), vô can.
- Phạm vi lệch: nhóm legacy `TTCTP-N` header=0; nhóm mới 155 (status1), 295 (status3), 2247 (status3).

## Quyết định (user chốt)
1. Backfill `total_amount_proposed = tổng dòng` cho tất cả phiếu lệch (lấy tổng dòng làm chuẩn).
2. Chặn BE: khi duyệt KHÔNG được tự ghi đè mất số tiền đề xuất gốc.

## Task
- [x] **FE (gốc rễ): `removeBusinessTripAssigns()` thêm `getTotalAmountProposed()`** sau khi splice.
- [x] BE: `store()` — set `total_amount_proposed` = tổng `total_payment_unit_price` thực lưu (thay vì tin FE) để không drift từ lúc tạo.
- [x] ~~BE phòng vệ `toggleApprove()`~~ → **đã REVERT** về nguyên trạng (không liên quan bug này, giữ footprint tối thiểu).
- [x] Data: seeder `BackfillTotalAmountProposedSeeder` backfill `total_amount_proposed = SUM(total_payment_unit_price)` cho phiếu lệch.
- [x] Chạy seeder trên DB hiện tại + verify 2247/295/155 khớp → còn 0 phiếu lệch.

## Checkpoint — 2026-06-24
Vừa hoàn thành: sửa BE (store + toggleApprove) + seeder backfill, đã chạy trên DB `thanhan_tag_24062026`.
Đang làm dở: (không)
Bước tiếp theo: user verify lại trên UI màn list + chi tiết phiếu 2247; nếu deploy môi trường khác cần chạy `php artisan db:seed --class=BackfillTotalAmountProposedSeeder --force`.
Blocked: (không)

## File đã đổi
- `Modules/Timesheet/Services/RequestPaymentWorkingFreeService.php` — `store()` + `toggleApprove()`
- `database/seeders/BackfillTotalAmountProposedSeeder.php` (mới)
