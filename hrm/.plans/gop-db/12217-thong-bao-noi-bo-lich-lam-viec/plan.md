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
  - [x] (17/11, sửa theo yêu cầu) `SelfNotificationForm.vue` (dùng chung Thêm/Sửa/Xem): "Thời gian áp dụng" là MỘT hàng — 2 `date-picker` cạnh nhau "Từ ngày → Đến ngày" (mỗi ô nửa chiều rộng, lỗi 422 hiện dưới đúng ô), đặt trước "File đính kèm"; bản đầu là 2 hàng riêng (đã gộp). Ghi chú cũ: 2 ô `date-picker`, copy pattern ô "Hạn đăng ký" ngay trên (màn cũ dùng vue2-datepicker, không dùng V2Base); "Đến ngày" chặn chọn trước "Từ ngày", BE trả 422 hiện dưới ô
  - [x] (17/11) Màn xem dùng chung form nên hiện 2 ô (disabled); màn nhân viên xem nội dung in nên khoảng ngày xuất hiện qua 2 biến mẫu

## Phase 2 — Lịch làm việc: thông báo nội bộ lên lịch
- BE
  - [x] (17/11) `NoticeWorkItems::calendarItems()` (file mới, theo khuôn `TimesheetWorkItems`) + nối vào `WorkCalendarService::getAll()` + cho phép `notice` ở `MyTodoController::calendar`: status=2, có đủ apply_from/to, người xem nằm trong `self_notification_recipients` (qua employee_info_id), khoảng ngày giao nhau; 1 truy vấn `whereExists` + eager load người gửi. Đã thử: người nhận 1 / không nhận 0 / tuần khác 0 / biên 21-22/11 đúng / chưa gửi 0
  - [x] (17/11) Không cần sửa 4 lớp đó — mục thông báo dựng thẳng mảng item (status theo NGÀY: Sắp áp dụng / Đang áp dụng / Hết thời gian áp dụng) giống phiếu chấm công
- FE
  - [x] (17/11) FE: `work-item-types.js` thêm loại `notice` (hồng #db2777, icon ri-megaphone-line) → chip lọc + thẻ + thanh nhiều ngày tự có; `NoticeDrawerBody.vue` mới + nối `WorkItemDetailDrawer` (header loa, dữ liệu lấy từ item không gọi API, nút "Xem thông báo" mở `/human/self-notification/{id}/read`); `index.vue` mở drawer cho `notice`; sửa `CalendarFilterToolbar` + `WorkCalendarTab` cho chip tự xuống dòng (9 chip không còn vừa 1 hàng, nút Tạo mới giữ góc phải). Đã kiểm Playwright: tuần/tháng hiện thanh hồng đúng 17→20/11, drawer + nút xem + màn Thêm thông báo đều đúng thiết kế

## Phase 3 — Tạo nhắc việc cho nhiều người
Quy tắc (user chốt 17/11/2026): KHÔNG chọn ai → chỉ tạo cho người tạo; ĐÃ chọn người nhận → KHÔNG tạo cho người tạo, muốn có bản của mình thì tự chọn mình trong danh sách (danh sách có cả chính mình).
- BE
  - [x] (17/11) `MyTodoService::storeTodo()` + `selectedEmployeeIds()` + `createCopiesForEmployees()`: mỗi nhân viên được chọn (bỏ trùng, bỏ id không hợp lệ) nhận 1 nhắc việc ĐỘC LẬP vào loại mặc định "Việc cá nhân" của họ (`ensureDefaultLists`); bản của người tạo CHỈ tạo khi không chọn ai hoặc tự chọn mình; sao chép tiêu đề/mô tả/ngày-giờ hạn/các bước (chưa xong), KHÔNG sao chép liên hệ + lịch lãnh đạo; chỉ việc cấp 1. Người nhận tự sửa/tick/xoá bản của mình. Không có bản của người tạo thì trả bản đầu tiên vừa tạo cho controller
  - [x] (17/11) `StorePersonalTodoRequest`: `employee_ids` array, mỗi phần tử tồn tại ở `employees` (sai → 422, không tạo gì). (18/11: đã BỎ trần 200 — không giới hạn số người nhận)
  - [x] (17/11) **Liên kết ngầm**: migration `2026_11_17_000002_add_assign_group_to_personal_todos_table` thêm `personal_todos.assign_group` (uuid, index); mọi bản của cùng 1 lần giao (kể cả bản của người tạo nếu tự chọn mình) chung 1 mã nhóm, không giao cho ai thì NULL; không hiện ở giao diện (để biết các bản cùng một lần giao — báo cáo tiến độ, sửa/huỷ cả nhóm sau này)
  - [x] (17/11) **Thông báo "bạn được giao nhắc việc"**: `MyTodoService::notifyAssignees()` gửi sau khi lưu xong (cùng cách báo lịch lãnh đạo: `app()->terminating`, lỗi từng người chỉ ghi log): `[VIEC] Tạo mới: <tiêu đề>. Người giao: A. Hạn: 14:30 21/11/2026` dựng bằng `NotificationMeta::build` + `EmployeeInfoService::sendNotification` (chuông web + socket + push); `type = work_reminder.personal`, `id` = id bản nhắc việc CỦA người nhận (app có sẵn đường mở: `openWorkItemById('personal', id)`), `url = /assign/my-todo`. Người tạo không tự nhận thông báo. Đã chạy 2 lệnh tự kiểm của skill `notification-convention` (rỗng); push local KHÔNG đi thật vì queue `database` và không có worker
- FE web
  - [x] (17/11) `TodoFormModal.vue`: khối "Nhắc cho nhân viên" (chỉ khi TẠO MỚI) dùng `CheckboxMultiSelect` có sẵn, nguồn `store.employees` (không gọi thêm API), CÓ cả chính mình (thêm mục của mình từ hồ sơ nếu store thiếu, vd admin), nhãn `employeeOptionText`
- FE app (TPE_APP, nhánh `tpe`)
  - [x] (17/11) Lịch: `WorkType` thêm `notice` (hồng #DB2777, icon campaign) → thẻ + chấm tuần + bảng Lọc lịch tự có; `openWorkItem` mở `InternalNotificationDetailRoute` (màn "Nội dung thông báo" có sẵn); màn đó thêm dải "Thời gian áp dụng" (model `ApiSelfNotificationData` + `applyFrom/applyTo`, build_runner)
  - [x] (17/11) `personal_todo_form_page.dart`: khối "Nhắc cho nhân viên" (chỉ tạo mới) dùng lại `MeetingEmployeePickerRoute` (chọn nhiều); dòng người nhận = avatar chữ cái đầu + nhãn "Tên - Mã phòng - Mã NV", nút "Thêm người" viền xanh lá, viền thẻ xanh theo thiết kế A3; payload `employee_ids`
  - [x] (17/11) Đã bấm thật trên iPhone ảo (flavor tpeLocal): thẻ thông báo trên Lịch → màn nội dung có dải ngày; form nhắc việc chọn 2 người → lưu → DB đúng 2 bản, người tạo không có bản

## Phase 4 — Thiết kế lại "Nhắc cho" (18/11/2026, user chốt)
Quy tắc: mặc định ẩn danh sách, nút gạt **Chính mình** (mặc định) | **Nhiều người**; chọn Nhiều người → tick sẵn chính mình nhưng BỎ được; bắt buộc còn ≥ 1 người ("Chọn ít nhất 1 người"); gạt về Chính mình → RESET (như lúc đầu); KHÔNG giới hạn số người; chọn người bằng popup/màn có BỘ LỌC nhiều điều kiện + Chọn tất cả theo bộ lọc. Thiết kế: `~/Downloads/meeting-mobile_v2.pen` (W3-v2a/b/c, A3-v2a/b, A4-v2, A4-v2b); app KHÔNG có nhóm "Gợi ý thành phần tham dự".
- BE
  - [x] (18/11) Bỏ trần 200 ở `StorePersonalTodoRequest`; `createCopiesForEmployees` nạp list "Việc cá nhân" + sort_order theo lô (1 query mỗi loại thay vì mỗi người); đo local 1.299 nhân viên: tạo bản ~2,1s trong request, thông báo ~3,6s sau khi trả kết quả
  - [x] (18/11) Endpoint mới `GET assign/meeting/employee-filter-options` (Công ty/Phòng ban/Bộ phận/Chức vụ/Chức danh, 1 request) cho bảng lọc ở app; `getListEmployee` đã sẵn các tham số lọc + `get_all`
- FE web
  - [x] (18/11) `TodoFormModal.vue`: nút gạt `V2BaseSegmented` Chính mình | Nhiều người; Nhiều người → khung chip (chip mình ghi "(Bạn)", bỏ được bằng ×) + đếm "Đã chọn n người" + nút "Chọn nhân viên" mở `PopupStaff` (copy pattern từ `pages/assign/meeting/components/MeetingParticipants.vue:233`: `multiple`, `initial-selected`, `default-current-company`, `@selected-multiple`) — popup chỉ mount khi sang "Nhiều người" (lazy, không gọi API nhân sự lúc mở form); lỗi đỏ "Chọn ít nhất 1 người"; gạt về Chính mình thì xoá sạch danh sách; payload chỉ gửi `employee_ids` khi Nhiều người
  - [x] (18/11) `CheckboxMultiSelect.vue` thêm tuỳ chọn `max`/`showCount` (mặc định tắt, không ảnh hưởng chỗ khác) — hiện không còn màn nào dùng
- FE app (TPE_APP)
  - [x] (18/11) `personal_todo_form_page.dart`: nút gạt `MeetingSegmented` Chính mình | Nhiều người; tick sẵn chính mình (tra `employees.id` theo mã NV, nhãn "Bạn" riêng), bỏ được; chặn Lưu khi trống + viền đỏ + "Chọn ít nhất 1 người"; gạt về Chính mình → reset; danh sách dài chỉ hiện 5 người đầu + "Xem thêm n người" / "Thu gọn"
  - [x] (18/11) `meeting_employee_picker_page.dart` thêm cờ `filterable` (mặc định tắt — Meeting giữ nguyên): `ListFilterBar` + bảng lọc chung `showFilterSheet` (`employee_pick_filter.dart`: Công ty→Phòng ban→Bộ phận, Chức vụ, Chức danh) + chip tiêu chí + thanh "Chọn tất cả (n)/Bỏ chọn" lấy MỌI trang qua `get_all`; không có nhóm gợi ý. Bảng lọc dùng đúng `showFilterSheet` chung (Công ty→Phòng ban→Bộ phận gom 1 dòng, Chức vụ, Chức danh; danh mục 1 request `employee-filter-options`, nạp lazy khi mở bảng lọc)
- Kiểm
  - [x] (18/11) E2E `todo-multi` viết lại theo luồng mới — 34/34 đạt (mặc định ẩn + popup chỉ mount khi sang Nhiều người, tick sẵn mình "(Bạn)", bỏ mình + báo "Chọn ít nhất 1 người" không gọi API, popup lọc 5 ô, tìm, Chọn tất cả >1 trang, reset khi gạt về, payload không có employee_ids ở Chính mình, 250 người → 250 bản, sửa không có khối). Chạy lúc máy quá tải thì vài ca hết giờ/bị đẩy ra trang chọn phân hệ → chạy lại riêng nhóm "Giao diện web"
  - [x] (18/11) App: bấm tay trên simulator iOS (flavor tpeLocal, API 127.0.0.1:8000, TK cannt.kd1): mặc định Chính mình · sang Nhiều người tick sẵn mình · bỏ mình + Lưu → báo lỗi đỏ · lọc công ty TPE = 398 nhân sự (khớp web) · Chọn tất cả (398) · tìm "Nguyễn" + Chọn tất cả = 252 (không trùng người tick sẵn) · Xem thêm 247 người · Lưu thật → DB 252 bản (1 bản người tạo), 1 nhóm assign_group · gạt về Chính mình reset. Lưu ý: tắt hộp thoại thông báo, simulator chập chờn khi máy quá tải (load >150)

## Việc còn mở / lưu ý
- Các bản nhắc việc độc lập (người tạo sửa/xoá không tự ảnh hưởng người nhận); đã có liên kết ngầm `assign_group` nhưng CHƯA có tính năng nào dùng nó (báo cáo tiến độ / sửa-huỷ cả nhóm chưa làm — chờ yêu cầu)
- Bật "Báo lịch làm việc lãnh đạo" mà chọn người nhận không gồm mình → không có bản của mình nên lịch lãnh đạo không được tạo (chưa chặn ở FE)
- Màn Lịch app hiện cuối tuần có thể chỉ thấy chấm hồng cho ngày thuộc khoảng áp dụng; thẻ "Thông báo nội bộ" lặp mỗi ngày trong khoảng (giống phiếu nhiều ngày)
- Bấm thông báo trên chuông web mở `/assign/my-todo` (chưa trỏ thẳng tới việc: trang chưa có query mở theo id); app thì mở đúng chi tiết nhắc việc
- Thử trên DB local bằng dữ liệu tạm "[TEST #12217]" — đã xoá

## Kiểm
- [x] (17/11) E2E Playwright bộ `e2e/tests/notice-12217/` (3 spec + helper, dữ liệu thử tiền tố E2E12217, tự dọn): `notice-form` (Phase 1: API 422/biên/ngày rỗng/sửa/biến mẫu + UI thứ tự ô, bảng biến, lỗi dưới ô, ô lịch chặn ngày, sửa/xem), `notice-calendar` (Phase 2: API ai thấy gì, biên ngày, lọc loại/trạng thái, nhiều tài khoản cannt/manhnv, UI chip/thanh/drawer/điều hướng kỳ/toolbar/menu Tạo mới), `todo-multi` (Phase 3: API quy tắc chọn/không chọn/chọn mình/trùng/sai/việc con/độc lập khi tick-xoá/lịch người nhận + liên kết ngầm assign_group + thông báo cho người nhận (đúng người, đúng id/type/url, người tạo không tự nhận, 422 không gửi) + UI popup chọn, chip, tìm, tạo, mở lại, sửa không có khối)
- [x] (17/11) App: bấm tay trên simulator iOS (xem mục FE app)

## Phát hành (17/11/2026)
- [x] (17/11) E2E đạt: `notice-form` 21, `notice-calendar` 21, `todo-multi` 32 (chạy từng spec; chạy cả 3 cùng lúc lúc máy quá tải load 65 thì hết giờ chờ — lỗi môi trường, không phải lỗi code)
- [x] (17/11) Web: commit riêng file của #12217 lên `gop_db` (api `775bca2cd`, client `22b5c0cf0`) → merge `gop_db` → `develop` không xung đột (api `7cb1d52c8`, client `1ab15079b`); không đụng 152 file (api) / 8 file (client) chưa commit của người khác
- [x] (17/11) Deploy server dev (`~/build_tpe.sh`): kéo develop, migrate 2 migration mới (`apply_period`, `assign_group`) OK, route:cache, permission:catalog-sync, queue:restart, build FE xong (commit client `1ab15079b`); site dev + API mới phản hồi đúng
- [x] (17/11) App (TPE_APP): commit `26252bc` lên `tpe` → merge vào `develop` (tiến thẳng) + bump `TpeDev.xcconfig` 2.2.6+165 (`4ee0561`); build IPA `tpeDev` (Tân Phát ERP-HRM, `com.tanphat.erp.hrm.app`), kiểm đúng version/profile App Store, upload TestFlight bằng khoá ASC API: UPLOAD SUCCEEDED (Delivery UUID `c3db5919-18b9-4bca-9a49-e7d3560ef137`); chờ Apple xử lý 10–30 phút rồi gán nhóm tester

### Checkpoint — 17/11/2026
Vừa hoàn thành: Phase 4 (18/11) thiết kế lại "Nhắc cho" — BE + web + app + e2e 34/34 + pen; CHƯA commit/deploy (code Phase 4 còn ở working tree: hrm-api, hrm-client, TPE_APP nhánh develop)
Đang làm dở: chưa có
Bước tiếp theo: user xem lại; nếu duyệt thì commit riêng file #12217 → merge/deploy dev + bump build app (166) lên TestFlight; chốt có làm báo cáo tiến độ / sửa-huỷ cả nhóm nhắc việc (assign_group) không
Blocked: không

## Xử lý dữ liệu prod — TB #19 (20/11/2026) — @cuong61n
- [x] (20/11) Sếp yêu cầu đưa TB #19 "Nghỉ Ngày Văn hóa Việt Nam 24/11" (mã `008/2026/TB-TPE`, người tạo Nguyễn Thị Duyên) về "Đang tạo" để gửi lại, vì #19 chưa có apply_from/apply_to nên không lên lịch nhắc việc. Đã kiểm prod `hrm_erp_gop` (chỉ đọc): status 2, 403 người nhận không trùng, apply_from/apply_to NULL.
- [x] (20/11) Prod: `self_notifications.id=19` status 2 → 1 (1 dòng; mã, người tạo, 403 recipient giữ nguyên). Người gửi lại: Duyên (người tạo, canEdit chỉ cho người tạo + status 1).
- Hệ quả đã báo user và user CHẤP NHẬN: Duyên gửi lại ở `SelfNotificationService::update()` thì thêm 403 recipient mới mà không xoá cũ → danh sách "Thông báo của tôi" hiện #19 2 dòng, `index?employee_id=` cũng trùng; mã sinh lại (008→009); chuông/push gửi lần 2 cho 403 người. Chưa vá code.
- [ ] Việc còn lại: Duyên điền "Thời gian áp dụng" rồi gửi lại; sau đó (nếu cần) dọn recipient trùng của #19 và vá `update()` (xoá recipient cũ + giữ mã cũ) — chờ user duyệt.
