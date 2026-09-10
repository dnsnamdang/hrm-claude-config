# Plan — Fix lỗi API filter khách hàng ở màn Công việc của tôi (/assign/my-job)

## Phase 1 — FE
- [x] Bỏ `assign/customers/search?limit=20000&customer_type=2&all_business=1` ở `pages/assign/my-job/components/MeetingsTab.vue` (nạp 12.290 KH tổ chức ≈ 2,7 MB JSON, thỉnh thoảng BE trả 500, chặn hàng đợi `php -S` làm mọi API khác của màn chờ theo)
- [x] Bỏ đúng lệnh gọi đó ở `pages/assign/my-job/components/MeetingUpcomingModal.vue` (popup "Meeting sắp tới lịch")
- [x] Đổi ô lọc Khách hàng ở cả 2 chỗ sang `V2BaseSelectRemote` + `fetchCustomers(q, limit=30, customer_type=2, all_business=1)` theo khuôn `/assign/bom-list` (component tự gắn `dropdownParent` khi nằm trong modal nên không cần `V2BaseSelectInModal`)
- [x] Giữ label KH đã chọn bằng `customerInitialOption`; reset khi bấm "Đặt lại" và khi đóng popup

## Phase 2 — FE (2 màn còn lại cùng lỗi nạp 20.000 KH)
- [x] `pages/assign/meeting/index.vue` (Danh sách Meeting) — đổi ô lọc KH sang `V2BaseSelectRemote`; màn này có nhớ filter (`filterStateMixin`, key `assign_meeting`) nên lưu thêm label KH ở key `assign_meeting_customer_label` để khôi phục khi quay lại màn. File này là **CRLF**, đã giữ nguyên line ending
- [x] `pages/assign/report/solutions-work-summary-by-department/index.vue` (Báo cáo tổng hợp giải pháp theo phòng ban) — bỏ `loadCustomers()` gọi ở `created`, đổi sang `V2BaseSelectRemote` + `fetchCustomers(q, limit=30)`; xoá label khi bấm "Làm mới"

### Checkpoint — 2026-09-04
Vừa hoàn thành: fix filter KH ở cả 4 chỗ — my-job (MeetingsTab + MeetingUpcomingModal), /assign/meeting, báo cáo tổng hợp giải pháp theo phòng ban. Đã test trên trình duyệt: không còn request `limit=20000`, gõ mới gọi `limit=30`, chọn KH lọc đúng, "Làm mới" xoá sạch
Đang làm dở: —
Bước tiếp theo: (ngoài phạm vi) `GET /api/v1/assign/meeting` đang trả **500** trên DB gộp — `SQLSTATE[42S22] Unknown column 'type'` khi query `meeting_attachments` (migration cột `type` chưa chạy trên `local_hrm_erp`)
Blocked:
