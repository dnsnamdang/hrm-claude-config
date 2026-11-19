# Phiếu giao việc trong ngày: tự tính Hoàn thành / Quá hạn theo dữ liệu chấm công (#12120) — @cuong61n

Nguồn: Redmine #12120 (TPE Lệ tạo, Nguyễn Huyền giao 18/11/2026). Phân hệ Công việc, nền tảng Web App.
Màn: Văn phòng số › Công việc › Giao việc – công tác › Phiếu giao việc trong ngày; liên thông "Lịch làm việc của tôi" (`/assign/my-todo`).

## Quyết định đã chốt (user, 20/11/2026)
- Chấm công hợp lệ = có ≥ 1 lượt check-in thành công (`timesheets.accept = 1`), gắn phiếu qua `job_type='jobassignment'` + `job_id` = id phiếu; KHÔNG cần check-out.
- Tính THEO TỪNG NGƯỜI: ai chấm công thì phiếu của người đó Hoàn thành.
- Đã chấm công mà chưa Nhập kết quả vẫn là Hoàn thành, không bắt buộc nhập kết quả.
- Khớp chấm công theo `timesheets.employee_info_id = employee_infos.ssn` (KHÔNG theo employee_infos.id — xem memory).
- Tính live khi đọc (không thêm cột, không cron). Phiếu không lưu trạng thái Hoàn thành/Quá hạn; `status` chỉ là trạng thái duyệt.

## Phase 1 — BE
- [x] (20/11/2026) `TimesheetWorkItems`: thêm cờ `my_checkin` (EXISTS timesheets của chính người xem), `hasDone()` = có KQ hoặc có chấm công; sửa `statusInfo`/`statusGroup`
- [x] (20/11/2026) `TimesheetWorkItems::listItems`: lọc done/pending theo hasDone (có chấm công → vào "done", rút khỏi "pending")
- [x] (20/11/2026) `TimesheetWorkItems::calendarItems`: `is_overdue` phiếu giao việc so THEO GIỜ (now > giờ "Đến ngày" muộn nhất), không so theo ngày
- [x] (20/11/2026) `WorkReminderService` nhánh `ts_job`: không nhắc nhập KQ / quá hạn với người đã chấm công
- [x] (20/11/2026) Rà chỗ khác tính "xong" của ts_job (Agent tool, MyTodoService…)
- [x] (20/11/2026) Kiểm: php -l; test tinker phiếu có / không chấm công, 2 người cùng phiếu; index `timesheets(job_id, job_type)` đã có (migration 2026_09_16_000002)

## Ghi chú
- Không sửa FE: FE/app đọc `status_group` + `is_overdue` do BE trả.

## Kết quả kiểm (20/11/2026, DB local, tinker trong transaction rồi rollback)
- Phiếu #29970 (1 người, chưa KQ): chưa chấm công → `doing` / "Đã duyệt" / quá hạn, nằm ở list pending; thêm 1 dòng timesheets (accept=1, job_type=jobassignment, employee_info_id=ssn) → `done` / "Hoàn thành", hết quá hạn, chuyển sang list done.
- Phiếu #29272 (2 người): A chấm công → `done`; B chưa chấm → vẫn `doing` ("Đã duyệt"). Truy vấn nhắc việc `ts_job` chỉ còn trả B.
- Test mở rộng (20/11/2026, transaction + rollback): quá hạn theo giờ — kết thúc 1h trước = quá hạn, 2h nữa = chưa, 3 ngày trước = quá hạn; chấm công `accept=0` / `job_type` khác / `job_id` khác / ghi theo `employee_infos.id` (không phải ssn) KHÔNG được tính; chấm công đúng → `done` "Hoàn thành"; chấm công + có KQ → "Đã nhập kết quả"; chỉ có KQ → `done`; `WorkReminderService::collect('ts_job')` thật chỉ trả người chưa chấm; qua `MyTodoService::getAll` (tab pending/done/tất cả, `is_overdue=1`) và `WorkCalendarService::getAll` đều đúng, không lỗi SQL.
- Chưa kiểm: cron nhắc chạy thật, giao diện web/app bằng mắt.

## Triển khai
- [x] (20/11/2026) Commit `91cfe2135` (chỉ 2 file) làm trên worktree tạm từ `origin/gop_db` (worktree gop_db-main có sửa dở của phiên khác, không đụng), push `gop_db` (fast-forward `729a7ced6..91cfe2135`).
- [x] (20/11/2026) PROD (hrm.eteksofts.com): kiểm trước repo sạch, HEAD = origin/gop_db; chạy `~/build_tpe.sh` (log `~/build_tpe_2011_12120.log`): "Nothing to migrate", worker restart, frontend không đổi nên bỏ qua build. Kiểm sau: HEAD `91cfe2135`, code mới có mặt, API 401 (cần đăng nhập), log laravel không lỗi mới.
- Trạng thái: ĐÃ deploy PROD 20/11/2026. Chưa lên dev / develop; chờ user/QA test trên prod.
- [x] (20/11/2026) User: merge gop_db mới nhất vào develop + build dev. Merge `origin/gop_db` → `develop` bằng worktree tạm, 0 xung đột: hrm-api `a11693231`, hrm-client `e38a3da10` (đã push). Dev (`~/build_tpe.sh`, log `~/build_tpe_2011_dev.log`): migrate `2026_11_25_000001_add_source_message_id_to_issues_table`, build frontend xong; HEAD server dev khớp origin/develop. Trạng thái: ĐÃ deploy dev + prod 20/11/2026. Chưa xem UI dev bằng mắt.

## Vòng 2 — tester báo: PGV quá giờ kết thúc, chưa chấm công, chưa nhập KQ mà không vào Quá hạn (20/11/2026, @cuong61n)
- Nguyên nhân: tab "Công việc của tôi" (danh sách) tự phân nhóm Quá hạn ở FE chỉ so NGÀY hạn với hôm nay (`TodoMainList.vue` `due < today`, thẻ đếm `index.vue`). Vòng 1 chỉ sửa tab Lịch (`calendarItems`) nên phiếu quá giờ nhưng còn trong ngày vẫn ở "Hôm nay".
- [x] (20/11/2026) BE `TimesheetWorkItems::listItem`: trả `is_overdue` cho phiếu giao việc (nhóm todo/doing và giờ kết thúc < hiện tại).
- [x] (20/11/2026) FE `TodoMainList.vue` + `index.vue` (thẻ đếm): `item.is_overdue === true || due < today` → nhóm Quá hạn.
- Làm trên stack cổng 3002 (worktrees/gop_db-client, nhánh gop_db) + API 8003 (worktrees/gop_db-api) theo yêu cầu user; worktree có sửa dở của phiên khác (comment/mention) nên KHÔNG ff/stash — chỉ chép 2 file BE từ origin/gop_db rồi sửa tiếp. Đã hoàn lại sửa nhầm ở cây gop_db-main (cổng 3000).
- Kiểm: API 8003 phiếu A (quá giờ) `is_overdue=true`, B (chưa đến giờ) `false`, C (đã chấm công) không còn ở danh sách chưa xong. Playwright cổng 3002 (namdangit): A nằm nhóm QUÁ HẠN, B ở HÔM NAY + TUẦN NÀY, thẻ "Quá hạn" tính cả A. Dữ liệu thử `[TEST-12120]` (job_assignment_notes 30046–30048 + 1 dòng timesheets) để lại local.
- CHƯA commit/push/deploy. Chưa làm: phiếu công tác (PCT) quá giờ — task #12120 chỉ ghi Phiếu giao việc, chờ user chốt; app TPE_APP danh sách (`ui/my_todo/my_todo_list_view.dart:198` cũng so theo ngày) — chờ user chốt.
- [x] (20/11/2026) User chốt: phiếu công tác (PCT = `business_trip_assigns`, mã `PCT<id>`) làm tương tự PGV. `TimesheetWorkItems`: PCT có cờ `my_checkin` (timesheets `job_type='business_trip'`, `job_id` = id phiếu, `accept=1`, `employee_info_id`=ssn); lọc "xong/chưa xong" của PGV và PCT dùng chung closure `$applyDoneFilter`; quá hạn theo GIỜ cho cả 2 loại qua `isPastEnd()` (giờ kết thúc `00:00:00` coi là chỉ có ngày → hết hạn cuối ngày đó); `is_overdue` ở danh sách trả cho cả PCT. `WorkReminderService` nhánh `ts_business` bỏ người đã chấm công. KHÔNG làm "Phiếu giao công tác" bên Giao việc (`assign_requests`, job_type `new_business_trip`) — loại khác.
  - Kiểm (tinker, rollback): PCT quá giờ về chưa CC → doing/Quá hạn; chưa tới giờ → không; quá giờ + đã CC → Hoàn thành; quá giờ + có KQ → "Đã nhập kết quả"; CC `accept=0` / `job_type` khác không tính; `to_time` 00:00 hôm nay chưa quá hạn; nhắc `ts_business` chỉ còn phiếu chưa xong; chạy lại test PGV cũ vẫn đạt. Playwright cổng 3002: PCT-1 vào QUÁ HẠN, PCT-2 ở HÔM NAY, PCT-3 (đã CC) không ở danh sách chưa xong. Dữ liệu thử `[TEST-12120]` PCT 11408–11410 để lại local.
  - Trạng thái: sửa ở worktrees/gop_db-api + gop_db-client (cổng 8003/3002), CHƯA commit/push/deploy.
- [x] (20/11/2026) User: app cũng so sánh GIỜ giống web. TPE_APP: `ui/my_todo/my_todo_list_view.dart` (nhóm Quá hạn: `it.isOverdue || d.isBefore(today)`) + `ui/my_todo/widget/work_item_card.dart` (tô đỏ dòng hạn ở tab danh sách: thêm `it.isOverdue`). Chỉ phiếu giao việc / phiếu đi công tác có cờ `is_overdue` từ BE, loại khác vẫn theo NGÀY. `dart analyze lib/ui/my_todo` sạch.
  - Kiểm: iOS simulator iPhone 15 (riêng, không đụng iPhone 15 Pro đang có phiên khác dùng — sau đó user bảo tắt iPhone 15 Pro) + Android emulator Pixel_4_API_29, flavor tpeLocal trỏ API 8003 (`--dart-define=APP_API_BASE_URL`), TK namdangit: PGV-A (quá giờ, chưa CC) và PCT-1 (quá giờ về, chưa CC) vào QUÁ HẠN + dòng "Hạn … hôm nay" đỏ; PGV-B và PCT-2 (chưa tới giờ) ở HÔM NAY; phiếu đã chấm công không nằm trong danh sách chưa xong. Log Flutter iOS: 0 lỗi; log Android: app 0 lỗi (1 dòng FATAL EXCEPTION thuộc tiến trình khác — lệnh `uiautomator dump` tự chạy khi debug đụng UI automation của mobile-mcp, không phải app). `dart analyze lib/ui/my_todo`: 0 lỗi mới (1 info `prefer_const_constructors` ở contacts/new_contact_sheet.dart có từ trước). Lưu ý: lần mở đầu trên iOS báo "Mất kết nối mạng" do API 8003 (php -S 1 luồng) kẹt hàng đợi ~20s → connectTimeout; kéo tải lại là hết, không phải lỗi code.
  - Trạng thái: CHƯA commit/push; app cần build + phát hành bản mới thì máy khách mới có (nhánh app đang đứng: feature/app-phe-duyet, nhiều sửa dở của người khác — khi commit chỉ lấy 2 file này).

## Triển khai vòng 2 + PCT + app (20/11/2026)
- [x] App: commit `453c5bf` (2 file `ui/my_todo`) làm trên worktree tạm từ origin/develop, đã push `develop` (nhánh feature/app-phe-duyet đang có sửa dở của người khác nên không đụng). CHƯA đưa sang `tpe`, CHƯA build/phát hành app — user tự quyết lúc nào build.
- [x] Web: BE `e3b240dd9` (PCT hoàn thành/quá hạn theo chấm công, `is_overdue` ở danh sách, giờ 00:00 = chỉ có ngày) + FE `3c5ef850d` (nhóm Quá hạn + thẻ đếm theo `is_overdue`) đã push `gop_db`. Làm bằng worktree tạm từ origin/gop_db (2 worktree gop_db dùng chung có sửa dở của phiên khác, không ff/stash).
- [x] PROD TPE (hrm.eteksofts.com) theo yêu cầu user "build prod TPE là được": kiểm trước repo sạch (client chỉ có `yarn.lock` sửa sẵn từ lần build trước, không đụng), chạy `~/build_tpe.sh` (log `~/build_tpe_2011_12120_web.log`): "Nothing to migrate", build frontend xong. Kiểm sau: api `e3b240dd9`, client `3c5ef850d`, code mới có mặt, web 200, API 401 (cần đăng nhập). Build cũng kéo theo 1 commit của người khác đang chờ trên gop_db: `ad5dc5743` Tri Lee "lọc dữ liệu theo công ty ĐANG THAO TÁC" (api) và `b621e464f` "gợi ý @tag hiện tối đa 50 người" (client).
- Chưa làm: merge gop_db → develop + build dev (user chỉ bảo build prod); chưa kiểm bằng mắt trên prod.
