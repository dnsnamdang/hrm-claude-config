# Đẩy trả báo giá / gói thầu về phòng trước — Design (TÓM TẮT)

**Người phụ trách:** @khoipv — 2026-07-09
**Spec chi tiết:** `docs/superpowers/specs/2026-07-09-day-tra-bao-gia-goi-thau-design.md`

## Mục tiêu

Màn `contract/quotation_render` + `contract/bid_package_render`: thêm nút **"Đẩy trả"** để phòng hợp đồng trả chứng từ về phòng trước sửa lại, bắt buộc nhập lý do.

## Quyết định lớn

- **Quyền:** `Phân công hợp đồng` HOẶC `Lập hợp đồng`.
- **Điều kiện:** chỉ khi chưa lập HĐ — báo giá status 9, gói thầu status 4.
- **Chuyển trạng thái:** báo giá 9→1 (Đang tạo, group null); gói thầu 4→2 (Đã giao NV, group null). Dự toán quay về đồng bộ (BG: →6 'Kế hoạch'; GT: →11 'Thầu'). Gói thầu còn revert báo giá nguồn 18→8 'Thầu' (mirror điều kiện project_type==1 của render).
- **Giữ nguyên:** phân công NV phụ trách HĐ, toàn bộ dữ liệu đã nhập.
- **Lưu lý do:** 3 cột mới `return_reason/returned_by/returned_at` trên `quotations` + `bid_packages` (migration, không FK). KHÔNG tái dùng `reason_deny`.
- **Hiển thị:** banner đỏ trên chi tiết BG/GT khi `return_reason != null`; clear khi gửi lại (BG→CHO_DUYET, GT→CHO_DUYET_KET_QUA). Lịch sử (`HistoryApproved*`, tái dùng cột `reason_deny` của bảng lịch sử) giữ vĩnh viễn.
- **Thông báo:** người tạo báo giá / NV thực hiện gói thầu.
- **API:** `PUT category/quotations/{id}/return-render` + `PUT category/bid_packages/{id}/return-render` (pattern giống `rejectBid` của feature Từ chối lập gói thầu).

## Lưu ý

- Code "gói thầu gộp nhiều báo giá" CHƯA có trên branch `thanhan-dev` hiện tại → thiết kế theo 1-1 `quotation_id`, để TODO khi merge phải lặp N báo giá nguồn.
- Không cần nhãn trạng thái mới → không rà statusMap/report.
