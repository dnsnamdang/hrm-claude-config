# Plan — PL8 Quản lý Meeting (4 task hỗ trợ Redmine)

Nhánh: `tpe-develop-assign` (cả hrm-api + hrm-client) · Phụ trách: @dnsnamdang

## Phase 1 — #10884 Placeholder Tên meeting

### FE
- [x] `GeneralInfo.vue`: đổi placeholder trường Tên meeting sang chuỗi mới

## Phase 2 — #11015 Kéo thả sắp xếp thành phần tham gia

### BE
- [x] Migration thêm `sort_order` vào `meeting_employees` (index `meeting_id, type, sort_order`)
- [x] `MeetingEmployee`: thêm `sort_order` vào `$fillable`
- [x] `Meeting`: 2 relation `company_members` / `customer_members` order theo `sort_order` rồi `id`
- [x] `MeetingService::syncCompanyMembers` / `syncCustomerMembers`: gán `sort_order` theo thứ tự mảng FE gửi
- [x] `MeetingResource`: trả `sort_order` (qua model), print + attendance kế thừa thứ tự từ relation

### FE
- [x] `GeneralInfo.vue`: bảng Phía Công ty dùng `draggable` (tbody), cột handle 6 chấm trước STT
- [x] `GeneralInfo.vue`: bảng Phía Khách hàng dùng `draggable`, handle 6 chấm + STT
- [x] Group riêng từng bảng (`company-members` / `customer-members`) → không kéo chéo
- [x] STT render theo index → tự cập nhật; thêm mới luôn push cuối danh sách
- [x] Ẩn handle khi `isShow`
- [x] `MeetingAttendance.vue` + In biên bản: đã kế thừa thứ tự (không cần sửa thêm)

## Phase 3 — #11045 Icon Info + Tooltip Loại meeting

### BE
- [x] Không cần sửa (`meeting_types/getAll` đã trả `description`)

### FE
- [x] `utils/meetingTypeInfoTooltip.js`: tooltip singleton (delegated hover, append body)
- [x] `components/MeetingTypeSelect.vue`: wrap V2BaseSelect/V2BaseSelectInModal, icon `i` cuối mỗi dòng dropdown + cạnh text đã chọn, ẩn khi chưa chọn
- [x] Áp dụng: `GeneralInfo.vue` (tạo/sửa/chi tiết)
- [x] Áp dụng filter: `meeting/index.vue`, `report/meeting-by-employees`, `report/meeting-by-projects`
- [x] Áp dụng filter: `solutions/.../MeetingsTab.vue`, `solution-modules/.../MeetingsTab.vue`, `MeetingUpcomingModal.vue`
- [x] Các màn filter đổi nguồn options sang `assign/meeting_types/getAll` để có `description`

## Phase 4 — #11014 Bắt buộc biên bản + tự động hủy meeting

### BE
- [x] Migration `general_regulations`: `meeting_report_lock_days` (default 1), `meeting_report_warning_hours` (default 3)
- [x] `GeneralRegulation`: thêm 2 field vào `$fillable`
- [x] Migration `meetings`: `report_deadline_notified_at`, `auto_cancelled_at`
- [x] `MyJobService`: get/save deadline-config + `DEADLINE_TRACKED_FIELDS` thêm 2 field
- [x] `Meeting`: helper `reportDeadline()`, `isReportOverdue()`, hằng `DEFAULT_REPORT_LOCK_DAYS/WARNING_HOURS`
- [x] `MeetingService::notifyReportReminder()` + `autoCancelOverdueMeeting()`
- [x] Command `assign:meeting-report-deadline` (nhắc trước X giờ + auto hủy quá hạn)
- [x] `Kernel`: schedule command 15 phút/lần
- [x] `MeetingController::update`: chặn cập nhật biên bản khi quá hạn (422)
- [x] `MeetingResource`: trả `report_deadline`, `is_report_locked`, `report_lock_days`, `report_warning_hours`
- [x] KPI: đã loại `HUY` sẵn qua `Meeting::REPORT_STATUSES` — không sửa

### FE
- [x] `settings/index.vue`: 2 input cấu hình mới trong tab Cấu hình hạn
- [x] `DeadlineConfigHistoryModal.vue`: nhãn 2 field mới
- [x] `MeetingReport.vue`: banner hạn nhập biên bản (còn hạn / quá hạn)

## Phase 5 — Fix phát hiện khi test thực tế (2026-08-14)

- [x] **BUG 1 (nặng)** `MeetingService::notifyMeetingEmployees` — `EmployeeInfoService::sendNotification`
      đọc `auth()->user()->employee_info_id` khi không chỉ định người gửi. Job chạy CLI không có auth
      → "Attempt to read property employee_info_id on null": meeting **bị hủy nhưng KHÔNG có thông báo nào**,
      và nhánh nhắc nhở throw trước khi set cờ → nhắc mãi không bao giờ thành công.
      Fix: không có auth thì lấy người tạo meeting làm người gửi, fallback chế độ `$command=true`.
- [x] **BUG 2** `autoCancelOverdueMeeting` — lỗi gửi thông báo làm job đếm sai ("hủy 0" dù đã hủy).
      Fix: bọc try/catch + `Log::error`, giữ nguyên kết quả hủy.
- [x] **BUG 3 (UX)** Banner hạn biên bản hiện cả với cuộc họp **chưa diễn ra**. Spec: hạn chỉ bắt đầu tính
      SAU khi cuộc họp kết thúc. Fix: thêm `Meeting::isReportPending()` + field `is_report_pending`
      (2 transformer) và FE chỉ hiện banner khi `is_report_pending`.
- [x] **BUG 4 (vệ sinh diff)** 3 file FE gốc dùng CRLF (`meeting/index.vue`, `settings/index.vue`,
      `report/meeting-by-projects/index.vue`) bị script sửa đổi hết sang LF → diff phình ~8.900 dòng.
      Đã trả lại CRLF, diff còn đúng ~263 dòng thêm / 53 xoá.
- [x] **BUG 5 (UI, user phản hồi)** Ô input màn `/assign/settings` trông như bị disable.
      Nguyên nhân **có sẵn từ trước** (không do 4 task này): rule scoped `settings/index.vue:2085`
      đặt nền trạng thái nhập được `#f8fafc`, gần trùng nền disabled `#f1f5f9` → không phân biệt được.
      Fix (user chọn phạm vi cả màn): nhập được `#ffffff` + viền `#cbd5e1` (đúng mặc định `V2BaseInput`),
      disabled `#e2e8f0` + chữ `#94a3b8`. Verify: 8 ô nhập được → trắng, 16 ô disabled thật
      (bảng Mức độ ưu tiên chế độ xem) → xám rõ rệt; focus vẫn viền + glow xanh; `v-model.number` OK.
      ⚠️ Ảnh hưởng cả 3 tab của màn Cấu hình phân hệ giao việc (ngoài phạm vi 4 task Redmine).

## Phase 6 — Chỉnh theo phản hồi user (2026-08-14)

- [x] **#11045 đổi icon**: bỏ vòng tròn chữ `i` tự vẽ → dùng **`ri-information-line`** 14px màu `#94a3b8`
      (giống icon info ở các màn báo cáo).
- [x] **#11045 đổi tooltip**: dựng lại bằng **đúng bộ class popover bootstrap**
      (`popover b-popover bs-popover-{right|left} info-popover` + `.arrow` + `.popover-body`) thay vì
      div đen tự style → khớp tuyệt đối với popover ở `/assign/report/meeting-by-projects`
      (đã đo: nền `#fff`, viền `#dee2e6`, radius 4px, max-width 420px, font 10.24px, body `#111`,
      padding 11.2/12.8, line-height 15.36, arrow 8×16) mà không hard-code giá trị nào.
- [x] **Tách icon khỏi dấu ×**: `.mt-selection-row { padding-right: 10px }` → khoảng cách icon → × đo
      được **10px** (trước là 0, dính sát nhau).
- [x] Sửa 3 bẫy định vị phát hiện khi test: `z-index` popover (1060) thấp hơn dropdown select2 (9999)
      → ép `10050` (không sửa thì popover lật sang trái sẽ bị dropdown che mất);
      bù `margin-left` của `.bs-popover-right` (khoảng hở bị cộng đôi 16px);
      bù `margin-top` của `.arrow` (arrow lệch 5px).
- [x] Verify 4 ca biên: bên phải / lật trái / sát lề trên / sát lề dưới — arrow chạm icon 0px,
      thân popover cách 8px, không tràn viewport. AC1–AC4 chạy lại pass hết, 0 lỗi console.

## Đã test thực tế (2026-08-14, DB `hrm_prod_local`, FE :3000 / BE :8000)

| Hạng mục | Kết quả |
| --- | --- |
| 3 migration | Chạy sạch; backfill `sort_order` 167 dòng liên tục 1..n đúng thứ tự id cũ |
| #10884 | Placeholder mới đúng ở cả màn Tạo mới và Sửa |
| #11015 AC1 | Handle 6 chấm đứng TRƯỚC cột STT ở cả 2 bảng |
| #11015 AC2 | Kéo DNS Admin từ vị trí 1 → 4, STT tự đánh lại 1..5, Lưu → DB `sort_order` khớp |
| #11015 AC3 | Kéo chéo sang bảng Khách hàng bị từ chối (cả DOM lẫn state Vue giữ nguyên) |
| #11015 AC4 | Tab Điểm danh + API `/print` đều đúng thứ tự đã kéo |
| #11045 AC1 | Chưa chọn → 0 icon trên màn |
| #11045 AC2 | 6/6 dòng dropdown có icon ở cuối; hover → tooltip đúng mô tả dòng đó, nằm trong viewport |
| #11045 AC3 | Chọn xong → icon cạnh text, tooltip đúng; `form.meeting_type_id` nhận giá trị (không dính bẫy tên event Vue 2) |
| #11045 AC4 | Filter màn danh sách (lọc ra 8 dòng) + báo cáo theo nhân viên: 6/6 dòng có icon, 0 lỗi console |
| #11014 job | Quá hạn → hủy + `[MET] Hủy: <b>{tên}</b>. Quá hạn nhập biên bản.` cho 5 thành viên nội bộ (KH không nhận) |
| #11014 job | Trước hạn 3h → `[MET] Nhắc báo cáo: ...` chỉ cho người tạo; chạy lại KHÔNG gửi trùng |
| #11014 job | Meeting chưa kết thúc / đã Hoàn thành / đã Hủy: không đụng tới |
| #11014 API | Guard 423 chặn cập nhật meeting quá hạn; meeting còn hạn vẫn lưu 200 |
| #11014 cấu hình | 2 input mới đúng vị trí/đơn vị; lưu OK; gửi 0 hoặc rỗng → lùi về mặc định 1/3 |
| #11014 lịch sử | Popup hiện "Hạn nhập biên bản meeting sau (ngày): 1 → 2" + đủ 2 nhãn mới trong bộ lọc |
| Console FE | Không phát sinh lỗi mới (4 warning sẵn có: `hasCustomer` prop/computed, `rows` type, `fields` collision) |

Dữ liệu test đã khôi phục nguyên trạng (meetings 13/18, thành viên, cấu hình, lịch sử, notification).

### Checkpoint — 2026-08-14
Vừa hoàn thành: code 4 task + migrate + test end-to-end (BE tinker/API + UI Playwright), fix 3 bug phát hiện khi test.
4 issue Redmine đã chuyển "Đang tiến hành".
Đang làm dở: —
Bước tiếp theo: user review. Khi deploy production: chạy 3 migration, bật cron `schedule:run`,
**rà soát meeting cũ quá hạn trước khi bật cron** (xem cảnh báo dưới).
Blocked:

### ⚠️ Lưu ý khi bật trên production
Ngay lần cron đầu tiên, MỌI meeting đang ở trạng thái Lên lịch/Chốt lịch có `end_date` quá hạn
(mặc định > 1 ngày) sẽ bị tự động Hủy hàng loạt và bắn thông báo cho toàn bộ thành viên nội bộ.
Local đang có 1 meeting như vậy (#13); production nhiều khả năng có nhiều hơn. Cần chốt với nghiệp vụ:
dọn/đóng meeting tồn trước, hoặc chỉ áp dụng auto hủy cho meeting kết thúc từ ngày bật tính năng trở đi.
