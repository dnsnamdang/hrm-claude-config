# Đơn hàng nguyên tắc: báo rõ hàng chưa có giá thay "Đã có lỗi xảy ra"

Không Redmine (người dùng nhờ) · @junfoke · ERP `TanPhatDev`, nhánh `gop_db`

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Xử lý: tạo ĐH nguyên tắc có hàng chưa có giá chỉ hiện "Đã có lỗi xảy ra" (2 thông báo) → hiện đúng câu server trả: "Hàng hoá SGCB-SGFM002 chưa có giá 'Đại lý cấp 2' tại … Vui lòng lấy hàng về / cập nhật giá bán cho công ty này trên HRM." Sửa `sale/firm/orders/formJs.blade.php` + `PrincipleOrderController.php` (tạo/sửa đơn trước ra `Hàng hoá #45664 … công ty #3`), bản Ztec y hệt (`ztect_orders/formJs.blade.php`, `ZtecPrincipleOrderController.php`). Không sửa bắt lỗi chung `public/js/app.js`. Commit `4151172a21`.
- [x] 30/10/2026 — Lỗi prod do chính fix trên: lập ĐH nguyên tắc báo "Missing Request ID" — `global: false` tắt luôn `ajaxSend` nên mất header `X-Request-ID` (middleware `PreventDuplicateSubmission`; Super Admin được cho qua nên test admin không thấy). Tự gắn lại header trong lệnh lưu ở 2 form. Commit `09e8875e53` — đã lên gop_db + develop_02.
- [ ] Popup chọn hàng ERP (`productPickerJs.blade.php`) cũng dùng `global: false` + POST → có thể dính cùng lỗi với user thường; phần của dnsnamdang, chưa sửa.
