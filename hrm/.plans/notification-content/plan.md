# Plan — Nội dung thông báo đủ thông tin cơ bản

## Phase 1 — Hạ tầng
### BE
- [x] NotificationMeta: MAX_TOTAL 180, note_full, day/dayTime/range/money; EmployeeInfoService cho note_full đi qua
### FE
- [x] App: Xem thêm dùng note_full
- [x] Web: NotificationItem dùng note_full
### Docs
- [x] Skill notification-convention + CLAUDE.md: 120 → 180, note_full

## Phase 2 — Viết lại từng thông báo (BE)
- [x] Timesheet + Payroll + Human + Decision + Console
- [x] Assign
- [x] Finance
- [x] Training + Rice + Meeting + CustomerCare + MasterData
- [x] Rà chéo: php -l, grep còn title nối tay, test build() thực tế vài loại
- [ ] Bảng câu cũ → câu mới gửi user
- [x] Sửa thêm: build() không chấm thêm sau tên đã cắt '...'; khảo sát đào tạo + hoãn kỳ ĐGNL + 2 notifier tính giá (PTG/YCTG, giữ nhóm hành động N187)
- [x] Test: php -l 115 file; phpunit MasterData/Assign/Finance/CustomerCare/Human — fail còn lại là lỗi có sẵn ngoài phạm vi; e2e đơn xin nghỉ (rollback) ra đúng câu + note_full
- [x] Sửa: 7 chỗ kết quả duyệt/từ chối gửi nhầm người duyệt → gửi người tạo (PCT, PGV ×3, PDX ×3); báo giá tổng đổi employees.id → employee_info_id; phiếu giao việc gửi người duyệt 1 lần (không lặp theo nhân sự)
- [x] Push: tiêu đề `Nhóm hành động · Loại đối tượng` (NotificationMeta::OBJECT_LABELS) — vì tên chỉ còn mã phiếu
- [x] Test app: gửi 85 thông báo mẫu (mọi prefix) tới namdangit qua sendNotification thật; danh sách + chip + Xem thêm (note_full) đúng; push giả lập simctl hiện khay thông báo đúng
- [x] Push không lộ thông tin nhạy cảm trên màn hình chờ (SENSITIVE_PREFIXES): đơn nghỉ / lương / bảo hiểm / HĐLĐ / QĐ / hồ sơ / thu chi chỉ hiện người hoặc mã + "Mở ứng dụng để xem chi tiết"
- [ ] Chờ user quyết: prefix mới, gửi nhầm người nhận (7 chỗ), báo giá tổng sai loại id, module CSKH/HSTK/BL, thả cảm xúc giữ emoji

### Checkpoint — 22/10/2026
Vừa hoàn thành: viết lại ~230 thông báo trên 115 file hrm-api theo khuôn tên riêng + ghi chú đủ ai · khi nào · loại · lý do (≤ 180, note_full)
Đang làm dở: —
Bước tiếp theo: user quyết các mục "Chờ user quyết"; (tuỳ chọn) bảng câu cũ → câu mới cho khách
Blocked:
