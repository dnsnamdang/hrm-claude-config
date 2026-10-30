# App — Nhiệm vụ & Vấn đề (TPE_APP) — @cuong61n

Thiết kế: `~/Downloads/meeting-mobile.pen` NV-01…16, VD-01…10, CV-00b, CV-PD1/2 (đã sửa theo skill app-* ngày 30/10/2026).
Chuẩn: skill `app-ui-convention` + `app-list-page` / `app-form` / `app-detail-page` / `app-hrm-api`.

## Quyết định
- Vai trò (Tôi làm / Tôi giao / Tôi theo dõi / Tôi duyệt KQ — vấn đề: Tôi phụ trách xử lý / Tôi phát hiện / Tôi theo dõi / Tôi duyệt đóng) nằm trong bảng lọc (không hàng chip dưới ô tìm), mặc định vai trò đầu áp ngầm.
- Chi tiết hiện mã; thẻ danh sách không mã.
- Đổi trạng thái: nhiệm vụ PUT `assign/tasks/{id}` (như web, BE kiểm allowed_next_statuses); vấn đề PATCH `assign/issues/{id}/status`.
- Chữ + màu trạng thái / ưu tiên / tình trạng hạn do BE trả (bỏ task_status_helper map cứng).
- Pill trạng thái có ▾ chỉ khi không có nút đáy làm cùng việc (mỗi hành động 1 lối vào).
- Thanh nút đáy: nút trắng trái, nút chính phải; sheet: hành động trái, Hủy phải.

## BE cần bổ sung (hrm-api develop)
- DetailTaskResource / DetailIssueResource: status_text, status_color, priority text/color, tình trạng hạn text/color.
- comments_count ở list + detail (withCount).
