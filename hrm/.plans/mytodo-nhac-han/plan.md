# Nhắc hạn "Việc của tôi" (Mytodo) — @cuong61n

## Phase 1 — Chốt nghiệp vụ
- [x] (29/10/2026) Rà nhắc hạn hiện có, đề xuất, chốt hạn từng loại phiếu, quá hạn cách A, chống nhắc lặp, bản tin 07:30 (design.md)

- [x] (29/10/2026) Rà thông báo hiện có của Nhiệm vụ (TaskService, TaskCommentController, NotifyTaskReport), Vấn đề (IssueService, IssueCommentController), Meeting (MeetingService, MeetingReportDeadlineCommand, nhắc nhận phòng MeetingRoomBookingService), Nhắc việc cá nhân (không có): chỉ có thông báo theo sự kiện, chưa có nhắc hạn/quá hạn nào

- [x] (29/10/2026) Đề xuất cấu hình nhắc theo giờ (theo công ty, từng loại việc; Meeting tính phút) + khung giờ yên lặng 21:00–07:00 dồn vào bản tin; khuôn màn theo /meeting/settings (hub + Lịch sử). Chờ chốt

## Phase 2 — BE (hrm-api develop)
- [x] (29/10/2026) Quyền mới "Cấu hình nhắc hạn công việc" (PermissionsTableSeeder, type 4 = phân hệ Công việc)
- [x] (29/10/2026) Migration: cột nhắc trước (phút) cho 7 loại trong general_regulations + bảng work_reminder_logs (chống gửi trùng)
- [x] (29/10/2026) API cấu hình GET/POST assign/settings/work-reminders (theo công ty người đăng nhập, lịch sử CatalogHistoryService)
- [x] (29/10/2026) WorkReminderService + command assign:send-work-reminders (5 phút/lần): nhắc trước + quá hạn 1 lần, 7 loại
- [x] (29/10/2026) Command assign:send-work-digest 07:30 T2–T7: bản tin sáng + tổng quá hạn thứ Hai
- [x] (29/10/2026) Sửa MyTodoService: hạn theo design, phiếu giao công tác status 3 + giới hạn 30 ngày, trường đang diễn ra
- [x] (29/10/2026) Duyệt Phiếu giao việc / Phiếu giao công tác → báo "Tạo mới" cho người thực hiện / người đi

  - Đã kiểm local: chạy command với --at đúng mốc dữ liệu thử → nhắc PGV 357 (4h trước hạn chót), PCT 13330 (4h trước giờ về), nhắc việc cá nhân đúng 16:00, quá hạn 1 lần; chạy lại không trùng; bản tin 30/10 07:30 gửi 2 người, tổng quá hạn thứ Hai 02/11 gửi 12 người; API my-todo: phiếu giao công tác đã hiện, hạn = hạn chót/giờ về; duyệt phiếu báo 'Tạo mới' cho người được giao (gọi hàm trực tiếp)
  - Phát hiện: NotificationMeta::build() dùng strtoupper làm hỏng tiền tố có dấu ([VIỆC]) → xử lý riêng trong WorkReminderService, CHƯA sửa hàm dùng chung (chờ user)

## Phase 3 — Web + App
- [x] (29/10/2026) Web: màn Cấu hình nhắc hạn (khuôn /meeting/settings) + menu Thiết lập
- [x] (29/10/2026) Web + App: nhãn "Đang diễn ra · còn n ngày", "Đi … → về …" trên thẻ
  - Web: pages/assign/work-reminder-settings (copy khuôn /meeting/settings) + components/assign-components/WorkReminderSettingPanel.vue (giờ/phút ↔ phút BE) + menu Thiết lập (isShow quyền mới); TodoItem.vue thêm "Đi … → về …" / "Đang diễn ra, còn n …"
  - App: work_item.dart đọc start_at; work_item_card.dart thêm dòng thời gian + đang diễn ra
  - Đã kiểm: Playwright :3000 — màn cấu hình hiện 7 ô mặc định, lưu 12 giờ OK, bỏ trống ô Meeting báo "Bắt buộc phải nhập" đúng ô, Lịch sử ghi 1440 → 720; danh sách web + app simulator hiện nhãn đúng. Local đã gán quyền mới cho vai trò Super admin để thử
  - Còn: chạy migrate + seeder quyền + route:cache khi deploy; admin gán quyền "Cấu hình nhắc hạn công việc" cho vai trò; chưa thử bấm thông báo type work_reminder trên app; chưa sửa NotificationMeta::build (strtoupper hỏng chữ có dấu) — chờ user
  - Code CHƯA commit (hrm-api, hrm-client, TPE_APP develop)

## Phase 4 — Chỉnh theo góp ý (29/10/2026)
- [x] (29/10/2026) Tiền tố bản tin / nhắc cá nhân đổi [VIỆC] → [VIEC] (user chốt) → bỏ đoạn vá strtoupper, dùng thẳng NotificationMeta::build; không sửa hàm dùng chung
- [x] (29/10/2026) Bấm thông báo trên app: BE type `work_reminder.<loại>` (thay `work_reminder`) + "Tạo mới" lúc duyệt PGV/PCT dùng type `assign_job` / `assign_business` (trước copy nhầm `lateInEarlyOutApprove` → app mở màn duyệt Đi muộn về sớm); app thêm openWorkItemById + case trong notification_bloc. Đã bấm thử simulator: PGV Tạo mới → chi tiết Phiếu giao việc, bản tin VIEC → Việc của tôi, PCT Sắp đến hạn → chi tiết phiếu giao công tác
- [x] (29/10/2026) Màn cấu hình bỏ khuôn hub 2 cột (chỉ 1 nhóm): 1 V2BaseFormSection + bảng Loại việc / Nhắc trước (ô có đơn vị giờ|phút) / Mặc định, dòng Nhắc việc cá nhân cố định, V2Footer Lưu, unsavedChangesMixin (lưu xong chốt lại mốc, không tắt cảnh báo vĩnh viễn). Xoá WorkReminderSettingPanel.vue. Đã kiểm Playwright: hỏi chưa lưu khi thoát, lưu OK
- [x] (29/10/2026) Màn cấu hình bỏ cột Mặc định (user yêu cầu), bảng còn Loại việc / Nhắc trước, thu về 640px; đã xem lại trên :3000
- Phát hiện (chưa sửa, ngoài phạm vi): thông báo Chờ duyệt / Đã duyệt / Từ chối có sẵn của Phiếu giao việc + Phiếu giao công tác (AssignJobController, AssignBusinessController) dùng type `lateInEarlyOutApprove` → trên app bấm vào mở nhầm màn duyệt Đi muộn về sớm

### Checkpoint — 29/10/2026 16:50
Vừa hoàn thành: BE nhắc hạn + bản tin + cấu hình, web màn cấu hình + nhãn thẻ, app nhãn thẻ
Đang làm dở: —
Bước tiếp theo: user thử trên local; chốt sửa NotificationMeta::build; commit/push khi user cho phép
Blocked:
