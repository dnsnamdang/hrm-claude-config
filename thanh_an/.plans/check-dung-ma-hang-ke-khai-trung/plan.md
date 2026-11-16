# Check: Dừng 2 mã hàng hóa kê khai trùng — có ảnh hưởng báo giá đã làm không

Người phụ trách: @khoipv · Bắt đầu: 12/11/2026

## Câu hỏi
User dừng (khóa) 2 mã hàng hóa vì kê khai trùng → có ảnh hưởng báo giá mọi người đã làm không?

## Task
- [x] Đọc logic Dừng hàng hóa: `ProductService::lock()` chỉ đổi `products.status` = 3 (STATUS_INACTIVE) + ghi `product_history`, không xóa, không động vào bảng con / chứng từ
- [x] Soát báo giá: dòng hàng lưu sẵn ở `quotation_tab_products` (tên, mã, ĐVT, giá…), xem/sửa/in/xuất Excel không join `products` theo status → báo giá cũ giữ nguyên
- [x] Soát BE lưu / duyệt báo giá, gói thầu, HĐ: không rule nào chặn theo `products.status`
- [x] Soát FE popup chọn hàng (`ProductModal`, `ProductModalWithDuplicate`): gọi `category/products?status=2` → mã đã dừng không chọn mới được
- [x] Soát cung ứng: `SupplyProposalService::catalogItems()` chỉ lấy hàng đang hoạt động (hàng ngoài HĐ); hàng trong HĐ không lọc
- [x] Giá HĐ trước (`previous-contract-price`) tính theo `product_id` → lịch sử giá của mã đã dừng không chuyển sang mã giữ lại
- [x] DB local (`thanhan_stag_07052026`) là bản cũ, không có thao tác dừng mới → chưa tra được báo giá cụ thể đang dùng 2 mã
- [ ] Chờ user: cho 2 mã (mã nội bộ) để tra trên DB thật xem báo giá / gói thầu / HĐ nào đang dùng

## Kết luận
Không ảnh hưởng dữ liệu báo giá đã làm. Ảnh hưởng chỉ ở thao tác mới:
1. Không thêm được mã đã dừng vào báo giá / gói thầu / HĐ mới (popup chọn hàng chỉ hiện hàng đang hoạt động)
2. Báo giá đang làm dở có sẵn mã đã dừng vẫn lưu / gửi duyệt / duyệt được, và sẽ mang mã cũ xuống gói thầu / HĐ
3. Giá HĐ trước + báo cáo theo mã bị tách giữa 2 mã
4. Ai chỉ có quyền "Xem danh sách hàng hóa" sẽ không thấy mã đã dừng ở danh mục

### Checkpoint — 12/11/2026
Vừa hoàn thành: soát logic Dừng hàng hóa với báo giá / gói thầu / HĐ / cung ứng
Đang làm dở: —
Bước tiếp theo: user gửi 2 mã → tra chứng từ đang dùng trên DB thật
Blocked: thiếu 2 mã cụ thể + DB thật
