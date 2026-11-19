# Báo giá: chặn lưu khi tổng phân bổ giảm giá vượt tổng giảm giá đơn hàng (#10603) — @cuong61n

Redmine #10603 — đang ở trạng thái **Phản hồi** (tester báo lại: chưa chặn lưu, hiển thị chưa đúng).

## Phase 1 — Điều tra
- [x] (03/11/2026) Rà code nhánh `gop_db` (cả 2 repo) + develop/tpe/tpe-develop-assign: CHƯA có chặn. Kết quả:
  - FE `pages/assign/quotations/_id/edit.vue`: chỉ hiện dòng đỏ "Đã phân bổ X / Y — Chênh lệch" + nút "Phân bổ lại", không chặn Lưu / Gửi duyệt.
  - BE `QuotationStoreRequest`/`QuotationUpdateRequest`: chỉ `allocated_discount_amount` `numeric|min:0`; `QuotationService` kiểm lúc gửi duyệt chỉ có giảm giá theo mặt hàng (method=1), không kiểm tổng phân bổ (method=2).
  - Trạng thái "Code xong chờ test" (06/2026) do người khác chuyển, không có commit nào làm việc này.

## Phase 2 — Sửa (chưa làm, chờ user chốt)
- [ ] BE: khi discount_method=2, tổng phân bổ (hàng hoá + dịch vụ + vận chuyển) > tổng GG → 422, chặn cả Lưu lẫn Gửi duyệt
- [ ] FE: hiện lỗi "Tổng phân bổ chiết khấu không được vượt quá Tổng chiết khấu đơn hàng." và không gọi API
