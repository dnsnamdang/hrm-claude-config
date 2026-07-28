# Plan — Chuẩn hóa định dạng tiền tệ ERP màn Tạo/Cập nhật báo giá

Màn: QLDA TKT → Quản lý báo giá → Tạo/Cập nhật báo giá (`quotations/_id/edit.vue`).
Yêu cầu: comma nghìn + dot thập phân (vd 143,207.02); payload gửi số thô.

## Điều tra — HIỆN TRẠNG CODE ĐÃ ĐÚNG CHUẨN ERP (không cần sửa)
- `formatMoney` = `Intl.NumberFormat('en-US', { maximumFractionDigits: precision })` → comma nghìn + dot thập phân. TẤT CẢ ô hiển thị tiền (bảng chi tiết + khu TỔNG + Tổng hợp giá trị) đều dùng formatMoney.
- `V2BaseCurrencyInput` (dùng cho Giá nhập/Giá bán/Phân bổ CK...): format hiển thị comma nghìn + dot thập phân; `parseRawValue` bỏ dấu phẩy; emit `Number` thô qua v-model.
- VAT(%) = input `type=number` (0–100); Tỷ suất LN = `số + '%'` (dot thập phân tự nhiên của JS). Không cần comma.
- Rà toàn template: KHÔNG có formatter VN (vi-VN/toLocaleString) hay số tiền hiển thị thô nào.

## Verify (Playwright, real data qid=6 + component thật)
- AC1/AC3 (hiển thị): ô tiền thật = "1,763,345,250", "142,213,820", "119,000,000"... (comma nghìn) ✓; demo formatMoney precision 2 = "143,207.02" (comma + dot) ✓; không có định dạng VN (1.234,56) ✓
- AC2 (nhập): input currency hiển thị "119,000,000", "1,641,000"... ✓
- AC4 (payload): model giữ typeof number; payload map Number() → quoted_price=119000000 (số thô, không comma); allNumeric=true ✓

## Kết luận
Định dạng tiền tệ ERP ĐÃ được implement đầy đủ trong code hiện tại (formatMoney en-US + V2BaseCurrencyInput). 4/4 AC PASS. KHÔNG cần thay đổi code.
Khả năng cao: bản deploy dev-hrm.eteksofts.com (task tham chiếu) chưa nhận thay đổi này; code local (branch tpe-develop-assign) đã có.

### Checkpoint — 2026-07-09
Vừa hoàn thành: điều tra + verify đầy đủ 4 AC — code đã đạt chuẩn, không sửa gì.
Bước tiếp: chờ user xác nhận / chỉ field cụ thể nếu còn thấy sai trên bản deploy.
Blocked:
