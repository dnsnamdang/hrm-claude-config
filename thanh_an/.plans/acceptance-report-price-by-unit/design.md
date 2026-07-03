# BBNT lấy đơn giá theo product_id + unit_id

**Phụ trách:** @khoipv · **Ngày:** 2026-06-30 · **Phạm vi:** BE + FE + migration

## Mục tiêu
Sửa lỗi BBNT lấy nhầm đơn giá khi cùng 1 mặt hàng nằm trong HĐ ở nhiều đơn vị tính/giá khác nhau
(vd product 26: Hộp @1.500.000 và mL @30.000) → chi tiết hiển thị ≠ tổng đã lưu (màn danh sách).

## Quyết định lớn
- Khóa giá/SL theo `product_id + unit_id` thay vì chỉ `product_id` ở cả meta (hiển thị) lẫn lúc lưu.
- Thêm cột `unit_id` vào `acceptance_report_items` (migration, không khóa ngoại) để tính tiền + prefill đúng.
- Có fallback theo `product_id` cho dữ liệu cũ (item chưa có `unit_id`).

## Spec chi tiết
`docs/superpowers/specs/2026-06-30-acceptance-report-price-by-unit-design.md`
