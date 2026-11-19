# Nội dung thông báo đủ thông tin cơ bản — @cuong61n

Spec chi tiết: `docs/superpowers/specs/2026-10-22-notification-content-design.md`

- **Mục tiêu:** khách muốn đọc thông báo là nắm được tổng quan (vd đơn xin nghỉ: của ai, ngày nào, lý do). Rà TỪNG thông báo của hrm-api, viết lại câu.
- **Phạm vi:** mọi chỗ gửi thông báo nghiệp vụ trong hrm-api nhánh `develop` (~250 lời gọi, ~110 file: Finance, Assign, Training, Timesheet, MasterData, Decision, CustomerCare, Human, Rice, Payroll, Meeting, Console). Chỉ đổi nội dung; người nhận / thời điểm / url / type giữ nguyên.
- **Quyết định (22/10/2026):** tổng ≤ 180 ký tự (nới từ 120); chữ tự do dài cắt `...`, bản đủ ở `note_full` → bấm Xem thêm hiện đủ; làm luôn không duyệt trước.
- **Hạ tầng:** `NotificationMeta::build()` (cắt 50/180, note_full, helper ngày/tiền); app + web Xem thêm dùng note_full.
