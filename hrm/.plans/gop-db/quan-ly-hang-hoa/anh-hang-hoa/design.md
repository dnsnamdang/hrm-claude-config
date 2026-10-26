# Ảnh hàng hoá — hiện ảnh đại diện ở chi tiết + bấm ảnh xem cỡ đầy đủ

@namdangit · nhánh `gop_db` · chỉ hrm-client · không BE / migration / quyền. Ngày 24/10/2026.

## Lỗi
https://hrm.eteksofts.com/master-data/products/44829 — ô "Hình ảnh" tab Thông tin chung trống.
`ProductTabGeneral.vue` chỉ vẽ `product.galleries`, bỏ qua `product.avatar`. Hàng ERP cũ để ảnh đại diện riêng
ở `products.avatar`, `product_galleries` rỗng ⇒ ô trống. Đo DB local (dump prod 21/10): **28.569** hàng `status<>0`
có avatar URL mà 0 dòng `product_galleries`. Hàng 4014 (prod): có cả 2 ⇒ chi tiết mất avatar.

## Quyết định đã chốt (user 24/10)
- Ảnh ở chi tiết = **avatar + galleries**: avatar đứng đầu khi URL chưa nằm trong galleries (hàng lưu từ HRM:
  `ProductWriteService::writeGalleries` đặt avatar = ảnh đầu ⇒ không lặp).
- Bấm ảnh (chi tiết + ô Ảnh ở 6 màn danh sách `ProductListPage`) ⇒ `FilePreviewModal` — khuôn N140 của
  `ProductPickerPanel::previewImage`. Thay cho mở tab mới. Ô không có ảnh: không bấm được, con trỏ thường.
- Helper dùng chung `openImagePreview(modalRef, url, name)` ở `utils/file-preview.js` (gắn tạm `.jpg` khi URL không đuôi).

## Ghi chú
- Gallery đường dẫn tương đối `/uploads/...` cần `ERP_URL` (`ErpAsset::url`) — prod có, local thiếu ⇒ ảnh vỡ chỉ ở local.
- Escape đóng popup chỉ khi focus đã vào b-modal (sau `shown`) — e2e phải chờ focus.
