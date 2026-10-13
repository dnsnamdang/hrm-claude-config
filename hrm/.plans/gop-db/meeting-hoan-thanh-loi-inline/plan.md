# Meeting — Hoàn thành: báo đỏ inline từng trường thiếu (nhánh gop_db)

## Phase 1 — FE
- [x] Bấm Hoàn thành còn thiếu: đổ lỗi theo key BE vào formError → ô thiếu viền/chữ đỏ ngay dưới trường (Điểm danh từng dòng, Câu 1–4 khảo sát, Các nội dung khác, Tài liệu, Kết luận); sửa tới đâu tắt đỏ tới đó
- [x] Toast chỉ báo chung "Vui lòng kiểm tra lại dữ liệu nhập" (bỏ toast liệt kê chi tiết)
- [x] Bấm Hoàn thành lần 2+ (lỗi không đổi) không nhảy tab/cuộn → handleComplete tự gọi jumpToFirstError mỗi lần bấm
- [x] Test Playwright meeting #44 (local): Điểm danh, Biên bản, Kết luận, Câu 1/4 OK — Câu 2/3 chưa test được vì DB local chưa có danh mục nhóm ngành

## Phase 2 — FE: KH cá nhân tự vào "Thành phần — Phía Khách hàng" (GeneralInfo.vue)
- [x] Chọn KH cá nhân → tự thêm dòng (tên + SĐT KH), thay dòng liên hệ tự thêm cũ; đổi sang KH doanh nghiệp / bấm ⓧ bỏ KH → gỡ dòng đó
- [x] Dòng KH cá nhân cố định như Người chủ trì: ẩn nút xoá, khoá ô Họ tên
- [x] Fix kèm: đổi KH cá nhân → doanh nghiệp không tự điền Người liên hệ (customer_type cũ còn sót) + updateOrReplaceCustomerMember gán theo index không vẽ lại (đổi sang splice)
