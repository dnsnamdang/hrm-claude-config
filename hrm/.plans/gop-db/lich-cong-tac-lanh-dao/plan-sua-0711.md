# Lịch làm việc lãnh đạo — đợt sửa 07/11/2026 (design.md §7)

> ⛔ CHƯA CÓ LỆNH CODE — hỏi riêng phạm vi trước Task 1. Không commit/push khi user chưa bảo.
> Nền: BE + web đã commit `91101f57d` (gop_db); app TPE_APP develop chưa commit (working tree).

## Chốt thêm 07/11 (user)
- **Ca dự phòng** (lãnh đạo không có bảng phân ca VÀ công ty chưa cấu hình Ca mặc định): **T2–T7, 08:30–12:00 / 13:00–17:30**. CN nghỉ.
- **Đổi tên CHỈ chữ hiển thị**: giữ mã quyền `assign.lich_cong_tac_lanh_dao.*`, bảng, route, tên file/class/thư mục `leader_schedule`.

## Luật tính buổi (dùng chung BE trả ra, app chỉ vẽ)
1. Nguồn ca: `shift_detail_employee_dates` (theo `employee_info_id` của lãnh đạo) join `working_shifts`, `->excludeAttendanceOnly()` — đúng cách `AttendanceTrait::sumDate`.
2. "Không có bảng phân ca" = **0 dòng** ca của người đó trong khoảng đang xem → dùng Ca mặc định công ty → nếu chưa cấu hình dùng ca dự phòng.
   Có ≥1 dòng trong khoảng → ngày không có dòng là ngày nghỉ (xám).
3. Mỗi ca → buổi: kết thúc ≤ 12:00 → chỉ sáng; bắt đầu ≥ 13:00 → chỉ chiều; còn lại → cả 2 buổi. Nhiều ca/ngày → OR.
4. **Thứ 7 luôn cả ngày** (sáng + chiều) với mọi lãnh đạo, bất kể bảng phân ca.
5. Vắng làm tròn theo buổi: khoảng vắng chạm trước 12:00 của ngày → vắng sáng; chạm từ 13:00 → vắng chiều. Chỉ tô vàng ở buổi CÓ ca; buổi ngoài ca vẫn xám.
6. Nhãn dưới dải: tên lịch (title) từ buổi vắng đầu tiên, cắt "…"; title null (bỏ "Gửi kèm tiêu đề") → "Vắng mặt".

## Hợp đồng API (chốt khi bắt đầu code 07/11)
- "Ca mặc định" = 1 **bảng phân ca** `shift_details` của công ty (có cờ + ca theo từng thứ: `monday`/`monday_working_shift_id`… `sunday`, T7 bỏ qua vì luôn cả ngày). Bỏ qua `start_at/end_at` hiệu lực của bảng (dùng như khuôn tuần).
- `GET assign/leader-schedules?from&to` thêm khoá `days`:
  `{"<employee_id>": {"Y-m-d": {"am": "off|present|absent", "pm": "off|present|absent"}}}` — đủ mọi lãnh đạo × mọi ngày trong khoảng.
  Vắng của 1 lịch ở ngày d: khoảng [from,to) với from = start_time nếu d là ngày đầu (không thì 00:00), to = end_time nếu d là ngày cuối (không thì 24:00). Vắng sáng nếu from < 12:00; vắng chiều nếu to > 13:00. Chỉ thành `absent` khi buổi đó có ca.
  Ca → buổi: end ≤ 12:00 → sáng; start ≥ 13:00 → chiều; còn lại cả 2 (ca đêm end<start → cả 2).
- `GET assign/leader-schedules/orders` thêm `default_shift_detail_id` (int|null) + `shift_details: [{id,name}]` (bảng phân ca của công ty đang chọn).
- `PUT assign/leader-schedules/orders` nhận thêm `default_shift_detail_id` (tuỳ chọn; có khoá → lưu; null = bỏ cấu hình; phải thuộc công ty đang chọn, sai → 422). Một nút Lưu cho cả màn cấu hình.

## Task A — hrm-api (gop_db)
- Migration mới `2026_11_09_000001_create_leader_schedule_settings_table.php`: `id, company_id (unique), shift_detail_id (nullable), updated_by, timestamps`.
- `LeaderScheduleService::workSessions(companyId, leaders, from, to)` → `[employee_id => [Y-m-d => ['am'=>bool,'pm'=>bool]]]` theo luật 1–4.
- `index` trả thêm `work_sessions`; mỗi schedule giữ `start_* / end_*` (app làm tròn theo luật 5) — hoặc BE trả sẵn `absent_sessions` (chọn BE trả sẵn để web/app không lệch).
- `GET/PUT v1/assign/leader-schedules/settings` (gate Q2): đọc/ghi `working_shift_id`; trả kèm danh sách ca chọn được.
- `messageFor`: 3 câu mới (§7) — sửa test nguyên văn.
- Catalog `assign.php`: đổi `name`/`feature` hiển thị → "Báo lịch làm việc lãnh đạo" / "Cấu hình lịch làm việc lãnh đạo" / "Lịch làm việc lãnh đạo". Cần `permission:catalog-sync` (dry-run trước) để tên trong DB đổi theo.
- Test: unit luật buổi (ca sáng-only, chiều-only, T7, không ca → mặc định → dự phòng, ngày nghỉ), feature `index` có `work_sessions`, settings 403/200, câu thông báo.

## Task B — hrm-client (gop_db)
- `TodoFormModal.vue`: nhãn ô tick "Báo lịch làm việc lãnh đạo"; câu confirm theo câu mới.
- `leader-schedule-config/index.vue`: đổi tiêu đề; thêm ô "Ca mặc định cho lịch làm việc lãnh đạo" (chọn 1 ca, gợi ý ca dự phòng khi trống), cảnh báo chưa lưu.
- `menu-sidebar.js`: nhãn menu.
- Playwright MCP đo DOM (namdangit), có ca không quyền Q2.

## Task C — TPE_APP (develop, working tree)
- Đổi chữ ở 10 file (§7 "Ảnh hưởng code").
- Controller: bỏ `CellState none|full|partial` → `SessionState { off, present, absent }` cho `am`/`pm`, lấy từ `work_sessions` + `absent_sessions`.
- `week_grid_view.dart`: ô chia 2 nửa (trái sáng/phải chiều), xanh/vàng/xám, dải + nhãn tên lịch, bỏ ô sọc.
- Khối "Hôm nay vắng", Theo ngày (LCT-03), Dòng thời gian (LCT-04): "Vắng sáng / Vắng chiều" thay giờ lẻ.
- Widget/unit test cập nhật; máy ảo (tpeLocal) so LCT-01/02/03/04/10.

## Rủi ro / ghi chú
- Lãnh đạo có ca ngoài khoảng xem nhưng 0 dòng trong tuần (VD nghỉ cả tuần) sẽ bị coi là "không có bảng phân ca" → hiện ca mặc định. Chấp nhận (hiếm), ghi lại.
- Query ca theo `employee_info_id`: leaders hiện trả `employee_id` → cần map sang `employee_info_id`.

## Tiến độ (07/11/2026 — user "làm": 3 repo, migration settings, catalog-sync)
- [x] A. hrm-api: `LeaderWorkSessions` (mới), `LeaderScheduleSetting` + migration `2026_11_09_000001` (ĐÃ CHẠY lẻ `--path` vào db_gop_6_11), controller `days` + Ca mặc định trong orders, request `default_shift_detail_id` (exists theo công ty), 3 câu thông báo mới, đổi chữ hiển thị (quyền, headline thông báo, lỗi 403/422). `permission:catalog-sync` ĐÃ CHẠY: sửa 2 tên, không đụng mã khác.
  Test mới: Unit `LeaderWorkSessionsTest` 7/7, Feature `LeaderScheduleDaysApiTest` 5/5, `LeaderScheduleRangeTest` 6/6.
  ⚠️ 12 ca cũ đỏ do DB: trên db_gop_6_11 role Super Admin đã có 2 quyền ⇒ namdangit (13) có quyền, các ca "13 không quyền → 403" sai giả định. Không do đợt sửa này (đều là ca phân quyền). PersonalContact 3 ca đỏ do rác dữ liệu (liên hệ "Anna Haro" từ simulator).
- [x] B. hrm-client: màn cấu hình thêm ô "Ca mặc định cho lịch làm việc lãnh đạo" (V2BaseSelect, 1 nút Lưu, cảnh báo chưa lưu tính cả ô ca), đổi chữ form + menu. Playwright MCP (namdangit 1440): ô 640×32, 15 bảng phân ca, gợi ý xám #6b7280; chọn → PUT mang `default_shift_detail_id: 28` → tải lại vẫn chọn; xoá → PUT null. NV 24 không quyền: GET/PUT orders 403, GET lịch 200.
- [x] C. TPE_APP: `SessionState`/`DaySessions`/`parseLeaderDays` (api service), controller bỏ CellState → `absentSessionLabel` "Vắng sáng/chiều/cả ngày", Bảng tuần ô chia đôi + dải + tên lịch ("Vắng mặt" khi ẩn tiêu đề), chú giải 3 trạng thái, Theo ngày / Dòng thời gian / sheet bỏ giờ lẻ, đổi chữ menu + form + câu xem trước. Test leader_schedule + my_todo 109/109 (trước 103), analyze 173 info (không đổi), thêm `week_grid_view_test.dart`.
  Máy ảo iPhone 18 Pro tpeLocal (Claude kiểm): menu "Lịch làm việc lãnh đạo"; lịch thử 09/11 14:00 → 11/11 10:00 ra T2 sáng xanh/chiều vàng, T3 vàng, T4 sáng vàng/chiều xanh, T7 xanh, CN xám, tên lịch dưới dải vừa 402pt; Dòng thời gian + sheet "Thứ 2, 09/11 chiều – Thứ 4, 11/11/2026 sáng". Đã xoá todo thử 604. Chế độ Theo ngày chưa nhìn trên máy ảo (lịch thử ngoài hôm nay) — có widget test.

### Checkpoint — 07/11/2026 23:05
Vừa hoàn thành: §7 cả 3 repo (chưa commit).
Đang làm dở: —
Bước tiếp theo: user xem máy ảo / so LCT-01; quyết: nhãn tên lịch kéo dài tới dải kế tiếp (không chỉ bằng dải); trùng tên tab "Lịch làm việc" của Việc của tôi; sửa 12 ca test phân quyền cũ (giả định NV 13 không quyền) — việc riêng; deploy: chạy migration settings + `~/build_tpe.sh` (catalog-sync đổi tên quyền).
Blocked: 

## Chốt thêm 07/11 tối (user)
- Trùng tên tab "Lịch làm việc" (Việc của tôi) với "Lịch làm việc lãnh đạo": CHẤP NHẬN, giữ nguyên.
- Nhãn dưới dải: phương án A — kéo tới dải kế tiếp / hết hàng.
- [x] Lỗi phát hiện khi chụp minh hoạ (user cho sửa `week_grid_view.dart` + test): 2 lịch có buổi vắng liền nhau bị nối thành 1 dải, mất tên lịch trước. Sửa: chỉ nối buổi khi cùng 1 lịch (`_owners` dùng chung cho dải + nhãn); chỗ nhãn < 28pt ghi thẳng "…" (Flutter cắt mất cả dấu …). Ca test mới "2 lịch sát nhau" đỏ trên code cũ (khe 0) → xanh; leader_schedule + my_todo 110/110, analyze 173. Máy ảo: 2 dải riêng, "…" dưới dải nửa buổi, chạm mở đúng "Họp HĐQT · Vắng chiều". Đã xoá todo thử 605/606.
- [x] 12 ca test phân quyền cũ đỏ do DB (user "Làm", chỉ file test hrm-api): thêm `stripLeaderSchedulePermissions()` vào trait `GrantsLeaderSchedulePermission` — gỡ 2 quyền LCT khỏi mọi `role_has_permissions` + `employee_has_permissions` trong transaction, gọi sau `parent::setUp()` ở 6 lớp test. Feature/LeaderSchedule 54/54 xanh; Unit 6/6 + 7/7. DB thật sau khi chạy: vẫn 8 người có quyền, 0 role tạm sót.

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành: code + kiểm (Playwright web, máy ảo app, e2e my-todo) → ĐÃ COMMIT + PUSH 08/11: hrm-api gop_db `cc12bd91d`, hrm-client gop_db `2a4b888ff`, TPE_APP develop `73b82b4` (rebase lên 14 commit develop: gộp thẻ meeting "Đã báo vắng" + `!closed`; giữ TodoListPickerSheet thay showAppPickSheet; sinh lại notification.freezed).
Đang làm dở: —
Bước tiếp theo: deploy — migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, `~/build_tpe.sh` (catalog-sync đổi tên 2 quyền LCT), thêm key ẩn menu mới ở Cài đặt phân hệ nếu chưa bàn giao; build app mới. Còn treo nhẹ: kiểm máy thật (Gọi / Lưu danh bạ máy / Android) cho Danh bạ.
Blocked:

## Góp ý test máy thật 08/11 (user) — đã sửa, CHƯA COMMIT
- "Chưa nhận thông báo": ĐÚNG THIẾT KẾ — người tạo lịch không nhận (§3.6); lịch 977 ghi đủ 427 thông báo cho NV khác. Local không push được vì FIREBASE_CREDENTIALS local trỏ thư mục cũ — CỐ Ý GIỮ hỏng: app tpeProd dùng chung topic `topics_development_` ⇒ local push sẽ tới máy thật nhân viên (memory local-firebase-push-toi-may-prod). Đã thử sửa rồi hoàn tác ~10 phút, không push nào đi.
- [x] Nút Lưu quay ~5s khi báo lịch (QUEUE sync cả prod): `LeaderScheduleService::announce` gửi trong `app()->terminating()` (console/test vẫn gửi ngay để Queue::fake bắt); `MyTodoController::traVeNgay()` gắn Content-Length cho store/update/toggle/destroy todo (php -S local không có fastcgi_finish_request). Đo: POST lịch 0,65s, 427 thông báo vẫn ghi đủ sau response. Test LeaderSchedule 54/54.
- [x] App: sửa nhắc việc xong đóng luôn chi tiết, về màn đã mở (Lịch làm việc / danh sách / danh bạ) — `personal_todo_detail_page._edit`. Máy ảo: Lịch → chi tiết → Sửa → Lưu ⇒ về thẳng Lịch.
- ĐÍNH CHÍNH 08/11 (SSH đọc prod): prod tpe `QUEUE_CONNECTION=database` + worker `tpe-worker.conf`, php-fpm 8.1 ⇒ prod VỐN không treo nút Lưu; treo + "Lịch làm việc không thấy ngay" chỉ ở local (`QUEUE=sync` + `php -S` không nhận request mới khi tiến trình đang chạy terminating ~10s). Giữ thay đổi terminating + Content-Length (vô hại trên prod, đỡ local).
- ĐÃ COMMIT + PUSH 08/11: hrm-api gop_db `7ee51d6a5` (terminating + Content-Length), TPE_APP develop `1ae3033` (sửa xong về đúng màn + chọn danh bạ máy ở sheet đầu).

### Checkpoint — 08/11/2026 (wrap up 2)
Vừa hoàn thành: góp ý test máy thật iPhone 14 Pro Max — Lưu báo lịch không treo (terminating + Content-Length), sửa nhắc việc xong về đúng màn, chọn danh bạ máy ở sheet đầu (user đã thử OK). ĐÃ PUSH: hrm-api gop_db `7ee51d6a5`, TPE_APP develop `1ae3033`. Prod tpe: php-fpm 8.1 + QUEUE=database có worker ⇒ prod không treo.
Đang làm dở: — (tiến trình còn chạy cho máy thật: API `php -S 0.0.0.0:8001` PID 39832; `flutter run --release` iPhone PID 57178 — tắt theo PID khi không cần)
Bước tiếp theo: deploy prod (5 migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, ~/build_tpe.sh catalog-sync, key ẩn menu mới, build app); đẩy .plans bằng ~/bin/push-plans.sh.
Blocked:

## Sửa 09/11 — xem lịch theo công ty hồ sơ (design §8)
- [x] BE `LeaderScheduleController::index` dùng `profileCompanyId()` (employee_infos.company_id, lùi về company_role); meta/orders giữ công ty đang chọn.
- [x] Test `LeaderScheduleDaysApiTest::test_xem_lich_theo_cong_ty_ho_so_khong_theo_cong_ty_dang_chon` (2 chiều; fixture thêm company_employees cho NV 25 ở công ty 4 vì holders() chỉ tính người làm ở công ty). LeaderSchedule 55/55 (chạy trước rebase).
- [x] ĐÃ COMMIT + PUSH 09/11: hrm-api gop_db `9403ff65b`.
- [ ] Kiểm local: web chọn công ty khác công ty hồ sơ → app Lịch làm việc lãnh đạo vẫn ra lãnh đạo công ty hồ sơ (ghi company_role tài khoản test, trả lại sau).

### Checkpoint — 09/11/2026 (wrap up 3)
Vừa hoàn thành: API xem lịch lấy lãnh đạo theo công ty hồ sơ — đã push hrm-api gop_db `9403ff65b`. Không FE/app, không migration.
Đang làm dở: —
Bước tiếp theo: kiểm local web đổi công ty + app máy ảo; deploy prod cùng đợt (không thêm migration).
Blocked:

## Lỗi 10/11 — bỏ tick "Gửi kèm tiêu đề" sau khi đã báo, thông báo cũ vẫn lộ tiêu đề (CHƯA SỬA)
Kịch bản user: tạo lịch có tick tiêu đề → gửi thông báo có tiêu đề → sửa lịch bỏ tick → thông báo trên màn hình vẫn hiện tiêu đề.
- [x] Tái hiện (tinker, transaction + rollback, Queue::fake, lịch #1147 / 429 thông báo): sau khi bỏ tick `leader_show_title=0` lưu đúng; **0 lô job thông báo mới**; thông báo cũ trong `notifications` vẫn `note_full` = tiêu đề + câu đề nghị; màn Lịch làm việc lãnh đạo (`schedulesBetween`) đã trả `title=null` — đúng.
- Nguyên nhân: `LeaderScheduleService::announce()` chỉ so khoảng vắng (`rangeOf` trước/sau); chỉ đổi `leader_show_title` ⇒ `$before == $after` ⇒ return null. Thông báo đã gửi lưu cứng nội dung trong `notifications.data` (bảng 660k dòng, chỉ index notifiable_type/id — tìm theo `data LIKE` sẽ quét).
- [ ] Chờ user chốt hướng: (A) sửa nội dung thông báo cũ của lịch tại chỗ, không gửi mới (push đã hiện không thu hồi được) · (B) gửi thêm thông báo "thay đổi" (thông báo cũ vẫn lộ tiêu đề, ~429 người nhận thêm 1 tin) · (C) cả hai. User đang muốn làm rõ trước khi chọn.
- [ ] Sau khi chốt: xin phép code riêng (repo · file · có/không migration), thêm test vào `MyTodoLeaderScheduleTest`.

### Checkpoint — 10/11/2026 (wrap up 4)
Vừa hoàn thành: tái hiện + tìm nguyên nhân lỗi bỏ tick tiêu đề không cập nhật thông báo (không sửa code, DB đã rollback — kiểm lại leader_show_title #1147 = 1).
Đang làm dở: chờ user làm rõ / chốt hướng A/B/C.
Bước tiếp theo: user chốt hướng → hỏi cho phép code → sửa announce() + test. Vẫn còn: kiểm local web đổi công ty + app (sửa 09/11).
Blocked: chờ quyết định user.
