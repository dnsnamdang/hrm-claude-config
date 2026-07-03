# Cho phép trùng hàng hóa — Nghiệm thu theo tháng

**Phụ trách:** @khoipv · **Ngày:** 2026-06-30 · **Phạm vi:** thuần FE

## Mục tiêu
Loại NT "Theo tháng" (`FormByMonth.vue`) cho phép chọn **lặp lại cùng mặt hàng** (vì cùng mặt
hàng có thể nằm trên nhiều hóa đơn khác nhau trong kỳ).

## Quyết định lớn
- Bỏ loại trừ ở popup chọn hàng → mỗi lần confirm thêm dòng mới (kể cả mặt hàng đã có).
- Mỗi dòng có khóa `uid` riêng (2 dòng có thể cùng `product_id`).
- "Còn lại"/"Đã NT" **trừ dần theo dòng** (giống FormByInvoiceDetail); vượt SL theo phần còn lại đã trừ.
- **Trùng theo cặp (mặt hàng + số hóa đơn)**, chỉ trong cùng biên bản: 2 hàng khác nhau dùng chung
  1 số HĐ OK; chỉ chặn cùng hàng + cùng số HĐ lặp. Cross-report giữ khóa theo số hóa đơn.
- **BE có sửa**: `assertNoDuplicateInvoiceNumbers` dupSelf đổi sang cặp cho `TYPE_THANG` (loại khác giữ).

## Spec chi tiết
`docs/superpowers/specs/2026-06-30-acceptance-report-month-duplicate-goods-design.md`
