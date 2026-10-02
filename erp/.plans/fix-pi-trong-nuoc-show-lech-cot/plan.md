# Fix bảng Hàng hóa màn view PI trong nước bị lệch cột

**Người phụ trách:** @junfoke — Repo `TanPhatDev`, màn `/admin/orders/inland_purchase_invoice/{id}/show`

## Hiện tượng
Ở màn XEM (không phải Sửa), bảng "1. Hàng hóa": cột **Bảo hành** hiển thị ngày (30/09/2026),
cột **Ngày DK về kho** trống, và bảng thừa 1 cột không tiêu đề ở cuối chứa số tháng bảo hành (12).

## Root cause
`resources/views/orders/inland_purchase_invoice/show.blade.php` — bảng readonly (từ dòng 853).
Header có **19 cột** (15 cột `rowspan` + VAT tách `%`/`Số tiền` + Bảo hành + Ngày DK về kho).
Hàng sản phẩm (dòng 890) đệm `<td colspan="11">` trong khi khoảng trống từ "Đơn giá bán" đến
"VAT/Số tiền" chỉ có **9 cột** → ô `guarantee` bị đẩy sang cột thứ 20 (cột thừa), kéo theo
`c.expected_time` của hàng giao hàng rơi vào cột Bảo hành. Bảng ở chế độ Sửa (dòng 249) dùng
đúng `colspan="9"` nên không lệch.

## Task
- [x] Sửa `colspan="11"` → `colspan="9"` (show.blade.php:893)
- [x] Sửa `colspan="21"` → `colspan="19"` cho dòng "Chưa có hàng hóa" ở cả 2 bảng (377, 988) — cho khớp 19 cột
- [ ] User mở lại PI (vd `/inland_purchase_invoice/3526/show`) xác nhận Bảo hành = số tháng,
      Ngày DK về kho = ngày, không còn cột thừa

## Checkpoint — 10/09/2026
Vừa hoàn thành: sửa 3 chỗ colspan trong `show.blade.php` (CRLF giữ nguyên, diff 3 dòng).
Chỉ đụng view, không đụng BE/JS.
Bước tiếp theo: user reload màn view PI để xác nhận.
Blocked: không
