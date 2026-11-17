# Lịch làm việc: Update logic hiển thị thông báo nội bộ (#12217) — @cuong61n

Redmine: http://quanly.dnsmedia.vn/issues/12217 (Đào Thúy tạo 17/11/2026, trạng thái Redmine "Chờ Duyệt giá" — A Nam bảo ưu tiên làm trước, chưa đổi trạng thái).
Phạm vi: mục 1, 2, 4 của task. **Mục 3 (Tin nhắn chat) KHÔNG làm — A Nam làm.**
Thiết kế: `~/Downloads/meeting-mobile_v2.pen` bảng #12217 (web W1–W3, app A1–A5, bám ảnh chụp màn thật); ảnh đối chiếu ở `~/Downloads/12217-ref/`.
Quyết định đã chốt (17/11/2026): lên lịch cho người nhận của thông báo đã gửi; thông báo bị thay thế/hết hạn vẫn lên lịch; mục 4 do mình làm.

## Phase 1 — Thông báo nội bộ: Thời gian áp dụng + biến mẫu
- BE
  - [x] (17/11) Migration `2026_11_17_000001_add_apply_period_to_self_notifications_table` thêm `apply_from`, `apply_to` (date, nullable) + index `(status, apply_from, apply_to)`; đã migrate DB local
  - [x] (17/11) `SelfNotificationService::store/update` lưu 2 trường; FormRequest tạo + sửa: cả hai cùng trống hoặc cùng có, `apply_to` >= `apply_from` (đã thử 4 trường hợp, đúng)
  - [x] (17/11) `DetailSelfNotificationResource` trả 2 trường + điền biến mẫu (dd/mm/yyyy); `PrintTemplateVariable` thêm `TU_NGAY_AP_DUNG`, `DEN_NGAY_AP_DUNG` (khớp key 2 nơi)
- FE
  - [x] (17/11) `SelfNotificationForm.vue` (dùng chung Thêm/Sửa/Xem): 2 ô `date-picker` đặt trước "File đính kèm", copy pattern ô "Hạn đăng ký" ngay trên (màn cũ dùng vue2-datepicker, không dùng V2Base); "Đến ngày" chặn chọn trước "Từ ngày", BE trả 422 hiện dưới ô
  - [x] (17/11) Màn xem dùng chung form nên hiện 2 ô (disabled); màn nhân viên xem nội dung in nên khoảng ngày xuất hiện qua 2 biến mẫu

## Phase 2 — Lịch làm việc: thông báo nội bộ lên lịch
- BE
  - [x] (17/11) `NoticeWorkItems::calendarItems()` (file mới, theo khuôn `TimesheetWorkItems`) + nối vào `WorkCalendarService::getAll()` + cho phép `notice` ở `MyTodoController::calendar`: status=2, có đủ apply_from/to, người xem nằm trong `self_notification_recipients` (qua employee_info_id), khoảng ngày giao nhau; 1 truy vấn `whereExists` + eager load người gửi. Đã thử: người nhận 1 / không nhận 0 / tuần khác 0 / biên 21-22/11 đúng / chưa gửi 0
  - [x] (17/11) Không cần sửa 4 lớp đó — mục thông báo dựng thẳng mảng item (status theo NGÀY: Sắp áp dụng / Đang áp dụng / Hết thời gian áp dụng) giống phiếu chấm công
- FE
  - [x] (17/11) FE: `work-item-types.js` thêm loại `notice` (hồng #db2777, icon ri-megaphone-line) → chip lọc + thẻ + thanh nhiều ngày tự có; `NoticeDrawerBody.vue` mới + nối `WorkItemDetailDrawer` (header loa, dữ liệu lấy từ item không gọi API, nút "Xem thông báo" mở `/human/self-notification/{id}/read`); `index.vue` mở drawer cho `notice`; sửa `CalendarFilterToolbar` + `WorkCalendarTab` cho chip tự xuống dòng (9 chip không còn vừa 1 hàng, nút Tạo mới giữ góc phải). Đã kiểm Playwright: tuần/tháng hiện thanh hồng đúng 17→20/11, drawer + nút xem + màn Thêm thông báo đều đúng thiết kế

## Phase 3 — Tạo nhắc việc cho nhiều người
- BE
  - [x] (17/11) `MyTodoService::createCopiesForEmployees()` gọi trong transaction của `storeTodo()`: mỗi nhân viên trong `employee_ids` (bỏ trùng, bỏ chính người tạo, bỏ id 0) nhận 1 nhắc việc ĐỘC LẬP vào loại mặc định "Việc cá nhân" của họ (`ensureDefaultLists`); sao chép tiêu đề/mô tả/ngày-giờ hạn/các bước (chưa xong); KHÔNG sao chép liên hệ + lịch lãnh đạo; chỉ việc cấp 1. Người nhận tự sửa/tick/xoá bản của mình
  - [x] (17/11) `StorePersonalTodoRequest`: `employee_ids` array tối đa 200, mỗi phần tử tồn tại ở `employees`. Đã thử: người tạo + 2 người = 3 bản, mỗi bản đúng list của chủ, 2 bước con mỗi bản, trùng/chính mình/id 0 bị bỏ
- FE web
  - [x] (17/11) `TodoFormModal.vue`: khối "Nhắc cho nhân viên" (chỉ khi TẠO MỚI) dùng `CheckboxMultiSelect` có sẵn (chip + tìm + checkbox), nguồn `store.employees` (đã nạp lúc đăng nhập, không gọi thêm API), bỏ chính mình, nhãn `employeeOptionText` = "Tên - Mã phòng - Mã NV". Đã kiểm Playwright: chọn 2 người, bấm Tạo nhắc việc → DB có đúng 3 bản
- FE app (TPE_APP): [ ] chưa làm — A1 Lịch/A2 Lọc/A3 Form/A4 Chọn nhân viên/A5 Nội dung thông báo (xem thiết kế)

## Việc còn mở / lưu ý
- Các bản nhắc việc KHÔNG liên kết với nhau (người tạo sửa/xoá không ảnh hưởng người nhận) — chờ user chốt có cần cột "cùng một lần giao" không
- Người nhận chưa có thông báo "bạn được giao nhắc việc" (task không yêu cầu; nhắc hạn chung vẫn chạy theo WorkReminderService)
- Thử trên DB local bằng dữ liệu tạm "[TEST #12217]" — đã xoá

## Kiểm
- [x] (17/11) BE: người nhận / không nhận / tuần khác / biên ngày / chưa gửi / không có ngày áp dụng (không lên lịch) — đúng. Web: Playwright tuần+tháng+drawer+màn xem+form Thêm thông báo+popup nhắc việc — đúng thiết kế

### Checkpoint — 17/11/2026
Vừa hoàn thành: Phase 1 (thời gian áp dụng + biến mẫu), Phase 2 (thông báo lên lịch — BE + web), Phase 3 (nhắc việc nhiều người — BE + web); đã kiểm Playwright + DB local
Đang làm dở: chưa có (chưa commit/push theo quy định)
Bước tiếp theo: FE app TPE_APP (A1–A5 trong thiết kế); chờ user chốt có liên kết các bản nhắc việc không
Blocked: không
