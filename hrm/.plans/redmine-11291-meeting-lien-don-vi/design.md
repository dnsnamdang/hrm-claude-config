# Design — Redmine #11291: Meeting liên đơn vị

@khoipv · Nhánh `fix-bug-11092026` (chỉ hrm-api) · 2026-09-11
Spec chi tiết: `docs/superpowers/specs/2026-09-11-redmine-11291-meeting-lien-don-vi-design.md`

## 1. Yêu cầu gốc (Redmine #11291 — Tính năng mới)
"[PL8 - Quản lý Meeting] Lịch meeting: Chọn thành viên liên đơn vị tham gia cuộc họp,
giao nhiệm vụ liên đơn vị và gửi thông báo tự động"

1. Chọn thành viên tham gia cuộc họp liên đơn vị — nhân sự toàn tập đoàn, lọc/tìm nhanh theo Đơn vị/Phòng ban.
2. Giao nhiệm vụ liên đơn vị từ Biên bản — "Người thực hiện" chọn được bất kỳ ai toàn tập đoàn.
3. Gửi thông báo tự động khi tạo/lưu cuộc họp và khi giao nhiệm vụ.
4. Thành viên được thêm vào cuộc họp (ở đơn vị nào cũng vậy) được xem chi tiết cuộc họp + nhiệm vụ.

## 2. Hiện trạng — 3/4 yêu cầu ĐÃ CÓ SẴN (đã rà code, không đoán)

| # | Hiện trạng | Bằng chứng |
| --- | --- | --- |
| 1 | ✅ Đã có | `MeetingController@getListEmployee` không lọc theo công ty người đăng nhập; `PopupStaff.vue` khởi tạo `company_id: undefined` + `V2BaseCompanyDepartmentFilter` với `is_all_company: true` → liệt kê mọi công ty, kèm lọc Phòng ban / Bộ phận / Chức vụ / Chức danh + tìm nhanh theo tên/mã |
| 2 | ✅ Đã có | Ô "Người thực hiện" ở `MeetingReport.vue` dùng **chính `PopupStaff`** (chế độ multiple) → cũng toàn tập đoàn |
| 3 | ⚠️ Một phần | `MeetingService::sendMeetingNotification()` bắn chuông toàn bộ `company_members` khi Lên lịch / Chốt lịch; `notifyMeetingChanges()` báo người bị ảnh hưởng khi bấm Lưu; có báo Hủy + nhắc hạn biên bản. **Chỉ chuông nội bộ, không Email/chat** |
| 3b | ❌ CHƯA CÓ | Lưu biên bản (`syncReports` / `syncReportExecutors`) không gửi gì cho người được giao |
| 4 | ✅ Đã có | `MeetingCriteria` (danh sách) và `Meeting::canView()` (chi tiết) đều cho qua nếu `company_members` chứa mình, không phụ thuộc công ty. Nhiệm vụ nằm trong chính màn chi tiết nên đi kèm |

## 3. Quyết định phạm vi (user chốt 2026-09-11)

- **Kênh thông báo: chỉ chuông nội bộ.** Không làm Email, không làm chat tích hợp (hệ thống chưa có
  tích hợp chat nào — nếu khách cần thì tách feature riêng).
- **Thời điểm báo nhiệm vụ: chỉ báo người MỚI được giao**, so tập trước/sau mỗi lần lưu.
  Lý do: sửa một lỗi chính tả trong biên bản mà bắn lại cho cả chục người là spam.
- **KHÔNG thêm cột Công ty/Đơn vị** vào popup chọn nhân sự và bảng thành viên — đọc lại nguyên văn
  issue thì không có dòng nào yêu cầu, user chốt "task không yêu cầu thì không làm".

→ Phạm vi thực thi còn đúng **1 việc: thông báo chuông cho người mới được giao nhiệm vụ**. Chỉ sửa BE.

## 4. Cách làm

`MeetingService` thêm 3 hàm (khuôn copy từ `notifyMeetingChanges()` sẵn có):
- `reportExecutorEmployeeIds()` — gom `executor_id` các dòng `meeting_report_executors` có
  `executor_type = 1`. Người thực hiện phía khách hàng (type = 2) bỏ qua vì `executor_id` của họ
  trỏ vào `meeting_employees` chứ không phải `employees` → lấy nhầm là bắn chuông cho một nhân sự
  nội bộ vô can trùng id.
- `notifyReportExecutors()` — diff mới − cũ, 1 thông báo / 1 người dù được giao nhiều dòng.
  Bỏ qua khi meeting ở trạng thái **Đang tạo** (nháp chỉ người tạo xem được → người khác bấm vào chỉ
  nhận 403) hoặc **Hủy**.
- `countReportTasksByExecutor()` — đếm số nhiệm vụ mỗi người để ghi đúng số trong nội dung.

`MeetingController`:
- `update()` chụp `$oldExecutorIds` **trước mọi `sync*()`** — `syncReports()` xoá sạch rồi ghi lại,
  chụp sau là mất tập cũ và lần lưu nào cũng bị coi là "vừa giao".
- Gọi `notifyReportExecutors()` **sau `DB::commit()`** và **ngoài khối `if/elseif` theo status**
  (giao nhiệm vụ xảy ra độc lập với đổi trạng thái), nhưng vẫn trong `if ($shouldNotify)` để
  cờ `send_notification = 0` tiếp tục có tác dụng.
- `store()`: tập cũ = rỗng → mọi người thực hiện đều là người mới.

Nội dung theo `.claude/skills/notification-convention`:
`[BBH] Tạo mới: <b>{tên cuộc họp ≤50}</b>. Bạn được giao N nhiệm vụ.`
Deep-link `/assign/meeting/{id}/show?active_tab=reports` — `MeetingForm.vue:1206` đọc `?active_tab`.

## 5. Điểm giữ nguyên có chủ đích
Không lọc bỏ chính người đang thao tác: ai tự giao nhiệm vụ cho mình vẫn nhận chuông — đồng nhất với
`notifyMeetingChanges()` hiện tại (cũng không lọc).
