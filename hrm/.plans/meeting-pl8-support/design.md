# Design (tóm tắt) — PL8 Quản lý Meeting: 4 task hỗ trợ

Nhánh: `tpe-develop-assign` (hrm-api + hrm-client) · Phụ trách: @dnsnamdang · Ngày: 2026-08-14
Spec chi tiết: `docs/superpowers/specs/2026-08-14-meeting-pl8-support-design.md`

## Phạm vi

| Redmine | Nội dung | Loại |
| --- | --- | --- |
| #10884 | Đổi placeholder trường Tên meeting | FE only |
| #11015 | Kéo thả sắp xếp thành phần tham gia (2 bảng) | BE + FE |
| #11045 | Icon Info + Tooltip mô tả cho Loại meeting | FE only |
| #11014 | Bắt buộc nhập biên bản + tự động hủy cuộc họp | BE + FE |

## Quyết định lớn

1. **#11015 — thứ tự lưu ở DB, không suy từ id.** Thêm cột `meeting_employees.sort_order` và đặt
   `orderBy('sort_order')` ngay trong 2 relation `company_members` / `customer_members` của entity
   `Meeting`. Nhờ vậy tab Thông tin, tab Điểm danh và bản In biên bản dùng chung một thứ tự mà
   **không phải sửa 3 nơi** (MeetingAttendance.vue lặp theo mảng, blade in đọc trực tiếp relation).
   FE dùng `vuedraggable` (đã có trong project) với `group` riêng cho từng bảng + `pull/put = false`
   → chặn kéo chéo bảng ở mức thư viện, không cần validate tay.

2. **#11045 — component riêng, KHÔNG sửa V2BaseSelect dùng chung.** Tạo `components/MeetingTypeSelect.vue`
   bọc `V2BaseSelect` / `V2BaseSelectInModal` và truyền `extraSettings` (`templateResult`,
   `templateSelection`, `escapeMarkup`). Vì `V2BaseSelect` chỉ đẩy `{id, text}` xuống select2 nên
   mô tả được tra ngược theo id qua map trong component (closure đọc live, không snapshot —
   `v-select2-component` không watch prop `settings`).
   Tooltip: dropdown select2 append ra `<body>` nên không dùng được b-tooltip → 1 tooltip singleton
   `utils/meetingTypeInfoTooltip.js` + listener uỷ quyền ở `document` theo attribute `data-mt-info`.
   6 màn filter đổi nguồn options từ `training/master-select?table=meeting_types` sang
   `assign/meeting_types/getAll` vì `MasterDataSelectResource` (dùng chung toàn project) không trả `description`.

3. **#11014 — tái dùng khối "Cấu hình hạn" có sẵn.** 2 tham số mới (`meeting_report_lock_days` mặc định 1,
   `meeting_report_warning_hours` mặc định 3) thêm vào `general_regulations` và ghép vào endpoint
   `assign/my-job/deadline-config` đang có → được **lịch sử thay đổi miễn phí** (chỉ cần thêm key vào
   `DEADLINE_TRACKED_FIELDS` + nhãn ở `DeadlineConfigHistoryModal.vue`).
   Hạn = `end_date + lock_days`. Job `assign:meeting-report-deadline` chạy **15 phút/lần** (hạn mỗi cuộc họp
   rơi vào giờ khác nhau, không gom về 1 mốc cố định trong ngày được).
   Phạm vi auto hủy: chỉ trạng thái **Lên lịch (1) / Chốt lịch (2)**; nháp (0) và Hoàn thành (3) / Hủy (4)
   nằm ngoài. Cấu hình đọc theo `company_id` **của meeting**, không theo công ty user đang đăng nhập
   (job chạy CLI không có auth).
   **KPI**: không phải sửa gì — `Meeting::REPORT_STATUSES = [CHOT_LICH, HOAN_THANH]` đã loại trạng thái Hủy.

## Lệch so với mô tả Redmine (đã xử lý theo convention team)

- Redmine #11014 ghi nội dung thông báo `⏰ [MET] Nhắc nhở: {Tên}. Sẽ bị HỦY nếu không HOÀN THÀNH...`.
  Theo `.claude/skills/notification-convention`: **không chèn emoji**, nhóm hành động phải nằm trong 14 giá trị
  cho phép, tổng nội dung ≤ 120 ký tự. Đã đổi thành:
  - Nhắc nhở → `[MET] Nhắc báo cáo: <b>{Tên}</b>. Chưa có biên bản, sẽ tự hủy lúc {H:i d/m}.`
  - Auto hủy → `[MET] Hủy: <b>{Tên}</b>. Quá hạn nhập biên bản.`

## Việc cần làm khi deploy

1. `php artisan migrate` (3 migration: `meeting_employees.sort_order`, 2 cột cấu hình
   `general_regulations`, 2 cột mốc thời gian `meetings`)
2. Build lại FE bằng **Node 14.21.3**
3. Đảm bảo cron `schedule:run` đang chạy (command mới `assign:meeting-report-deadline`)
