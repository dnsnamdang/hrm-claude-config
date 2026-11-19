# Plan — Nhiệm vụ (Task) #11453

## Phase 1 — Phân loại Nhiệm vụ chung / cụ thể (BE)
- [x] Migration `add_task_type_and_batch_id_to_tasks_table`: `task_type` tinyint default 2 + `batch_id` varchar(36) nullable index; backfill bản ghi cũ = 2
- [x] `Task.php`: thêm `task_type` + `batch_id` vào `$fillable`, hằng `TYPE_GENERAL`/`TYPE_SPECIFIC` + mảng `TASK_TYPE`, accessor `task_type_text`
- [x] `TaskStoreRequest`: `task_type` required|in:1,2; `assignee_ids` required|array|min:1 khi type=1; `assignee_id` required khi type=2
- [x] `TaskUpdateRequest`: bỏ qua `task_type`/`assignee_ids` (không cho đổi loại, luôn 1 người)
- [x] `TaskService::store()`: tách `createSingleTask()`, sinh `batch_id` + lặp `assignee_ids` khi type=1, bắn thông báo riêng từng người
- [x] `TaskService::index()`: nhận filter `task_type`
- [x] `TaskResource` + `DetailTaskResource`: trả `task_type`, `task_type_text`, `batch_id`

## Phase 2 — Phân loại Nhiệm vụ chung / cụ thể (FE)
- [x] `CreateTaskModal.vue`: thêm ô "Loại nhiệm vụ *" đầu form (V2BaseSelect, mặc định Cụ thể), disabled khi Sửa/Xem
- [x] `CreateTaskModal.vue`: type=1 → Người thực hiện đổi sang MultiSearchPicker, payload `assignee_ids[]`; toast "Đã tạo N nhiệm vụ"
- [x] `pages/assign/tasks/index.vue`: thêm cột + ô lọc "Loại nhiệm vụ"

## Phase 3 — Đổi nhãn Task → Nhiệm vụ (FE)
- [x] `components/menu-sidebar.js`: "Task" → "Nhiệm vụ", "Cập nhật tiến độ Task" → "… Nhiệm vụ"
- [x] `pages/assign/tasks/` (index.vue, daily-report.vue, CreateTaskModal, ImportResultModal, TaskHistoryModal)
- [x] 3 bản `TasksTab.vue` (solutions / solution-modules / my-job) + nhãn tab ở 4 màn manager
- [x] Modal vệ tinh: TaskUpcomingModal ×3, PendingApprovalModal ×2, PendingApprovalCard, PeopleLateTasksModal ×3, CategoryLateTasksModal, DetailListModal ×2, OverviewTab ×3, ProgressTab, FilesTab ×2, TodayTasks
- [x] Báo cáo + bản in: task-manager-by-employees (index/print/TaskDetailModal), performance-by-employee (index/table/print), solution-versions (table/print)
- [x] Module khác: CreateIssueModal, IssueHistoryModal, TodoItem, TodoFilterBar, HandoverItemsTable, settings/index.vue, DeadlineConfigHistoryModal
- [x] Tự kiểm grep: không còn nhãn "Task"/"task" tiếng Việt lọt lưới (loại trừ route/biến/class/comment)

## Phase 4 — Đổi nhãn Task → Nhiệm vụ (BE)
- [x] `TaskService`: 8 chuỗi thông báo chuông
- [x] `TaskCommentController`: 4 chuỗi thông báo bình luận
- [x] Message lỗi: `TaskController:194`, `TaskService:410`, `TaskStoreRequest:148`, `TaskUpdateRequest:195`
- [x] 5 blade export: tasks, solution_manager_tasks, module_manager_tasks, my-job-tasks, task_manager_by_employees_report

---

### Checkpoint — 2026-09-12
Vừa hoàn thành: **CODE XONG 4 PHASE** (BE + FE), migration đã chạy trên DB dev `hrm_prod_6_6`.
Đã kiểm thử BE bằng tinker: Nhiệm vụ chung 3 người → 3 bản ghi độc lập cùng `batch_id`, mã code riêng,
checklist/watcher/tag copy đủ, thông báo bắn đúng từng người; Nhiệm vụ cụ thể vẫn 1 bản ghi, `batch_id` NULL.
Dữ liệu test đã dọn sạch (tasks về 18 bản ghi ban đầu).
Đang làm dở: không có.
Bước tiếp theo: user kiểm thử trên giao diện :3005 — tạo Nhiệm vụ chung nhiều người, lọc theo
Loại nhiệm vụ, mở Sửa xem ô loại có bị khoá không. Sau đó quyết định có đổi tên quyền cho đồng bộ với
feature `issue-van-de` hay không.
Blocked: không có.

## Phase 5 — Sửa lỗi phát hiện khi kiểm thử giao diện (2026-09-12)
- [x] Màn Chi tiết nhiệm vụ chung KHÔNG hiện Người thực hiện — điều kiện `isGeneralTask && !isEdit` trúng cả chế độ Xem; sửa thành `&& !isReadOnly` (3 chỗ trong CreateTaskModal)
- [x] Dòng phân trang còn "20 task" — `itemLabel="task"` ở 9 file (index.vue + 3 TasksTab + 3 TaskUpcomingModal + 2 PendingApprovalModal)
- [x] Tên file Excel tải về còn `danh_sach_task.xls` — đổi thành `danh_sach_nhiem_vu.xls` ở 4 file FE + 4 controller BE
- [x] Nhãn sót: subtitle ProgressTab, 4 nhãn báo cáo task-manager-by-employees, placeholder CreateIssueModal, tab "Tasks (n)" + dòng rỗng ở HandoverItemsTable, "{{ n }} task" ở performance-by-employee, 2 chỗ `'task' : 'issue'` ở handover/receive
- [x] (ngoài phạm vi, user đồng ý sửa) `TaskController@export` eager-load sai `application.customerScope` → `customerScopes` — nút Xuất Excel màn Nhiệm vụ chết sẵn từ commit 5709824df (17/03/2026)

### Checkpoint — 2026-09-12 (sau kiểm thử UI)
Vừa hoàn thành: **KIỂM THỬ GIAO DIỆN PASS** trên :3005 (tài khoản DNS Admin). 8 case:
tạo Nhiệm vụ chung 3 người → 3 bản ghi độc lập · bỏ trống người thực hiện → lỗi inline "Vui lòng chọn
người thực hiện." · màn Sửa/Xem khoá ô Loại nhiệm vụ, người thực hiện về chọn-1 · sửa 1 bản không ảnh
hưởng 2 bản kia · lọc theo Loại nhiệm vụ (3 chung / 17 cụ thể) · tạo Nhiệm vụ cụ thể vẫn 1 bản ghi ·
nhãn đúng ở menu, danh sách, my-job, daily-report, modal · file Excel xuất ra đúng nhãn + đúng tên file.
Dữ liệu test GIỮ LẠI theo yêu cầu: TPE.TASK.NB.26.0018/0019/0020 (Nhiệm vụ chung) + 0021 (cụ thể).
Đang làm dở: không có.
Bước tiếp theo: user quyết có đổi tên quyền cho đồng bộ với `issue-van-de` không; sau đó commit.
Blocked: không có.

## Testcase (2026-09-15)
- [x] Bổ sung 42 testcase (TC-NV-001 → TC-NV-042) vào Google Sheet `Testcase _Quản lý dự án` → sheet `19.Task`, từ dòng 184 (gid=1955249925)
- [x] Sửa lại trình bày theo góp ý 15/09: bỏ icon ⚠️, xuống dòng thật trong ô (bước 1./2./3. và gạch đầu dòng); đã bổ sung quy ước vào `.claude/skills/testcase-documenter/SKILL.md` + `tc_engine.py`

## Phase 6 — Phản hồi Redmine #11453 (16/09/2026)
- [x] Phân quyền: 5 quyền nhóm `Task` → `display_name` + `group` đổi thành "Nhiệm vụ" (GIỮ NGUYÊN `name` chứa chữ 'task' vì là khoá check ở TaskService/FE + đã lưu trong `role_has_permissions`) — theo đúng tiền lệ nhóm `Vấn đề`
- [x] Bảng danh sách còn nhãn cũ "Mã-Tên task" / "Checklist/Task con" và KHÔNG hiện cột "Loại nhiệm vụ": nguyên nhân là cấu hình cột user lưu ở DB (`human/column-customizations`) là bản sao chép cả `label` — FE dùng thẳng nên nhãn mới trong code không bao giờ tới được user cũ. Thêm `utils/mergeColumnCustomization.js`: nhãn/khuôn lấy từ code, cấu hình user chỉ giữ thứ tự + ẩn/hiện, cột mới tự chèn đúng vị trí, cột đã gỡ tự loại. Áp cho `pages/assign/tasks/index.vue` + 3 `TasksTab` (solutions / solution-modules / my-job)
- [x] Báo cáo: "Số task được giao" (performance-by-employee: index/table/print + blade export), "Số task giao"/"Số task"/"Task / giờ" (solution-versions: table/print + blade export), "Giờ task"/"có task trong kỳ"/"N task" (task-manager-by-employees)
- [x] Nhãn sót khác: "Liên kết: N task" ở 4 bảng, toast "Xóa task thành công/Lỗi khi xóa task" ×3 TasksTab, "Bạn có chắc muốn xóa task", "TASK ĐANG PHỤ TRÁCH" ×2 HumanResourceTab, tooltip biểu đồ `${val} task`, placeholder "Tìm theo tên task, module..."
- [x] BE: nhãn lịch sử thay đổi 'Task cha'/'Task con', 'Cần phân thêm task', 'Task được chuyển sang', 'Có task đã được bàn giao...', 'Không thể tạo sub-task cho một sub-task'

### Checkpoint — 2026-09-16
Vừa hoàn thành: 4 điểm phản hồi của TPE trên Redmine #11453 (phân quyền, báo cáo hiệu suất, nhãn ở bảng danh sách, cột Loại nhiệm vụ).
Đang làm dở: không có.
Bước tiếp theo: chạy `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"` trên DB dev để nhãn quyền mới có hiệu lực, rồi kiểm thử giao diện.
Blocked: không có.

### Checkpoint — 2026-09-16 (sau kiểm thử UI)
Vừa hoàn thành: **KIỂM THỬ GIAO DIỆN PASS** trên :3005 (DB `hrm_prod_6_6`, tài khoản DNS Admin).
- Đã chạy `PermissionsTableSeeder` — 5 quyền nhóm Nhiệm vụ đổi đúng `display_name`/`group`, `role_has_permissions` giữ nguyên 8.125 dòng (731 dòng mồ côi có SẴN từ trước seed, đã đối chiếu với bản backup nên không phải do lần seed này).
- Màn Phân quyền: nhóm hiện là "Nhiệm vụ", 5 quyền đọc "Duyệt triển khai Nhiệm vụ", "Xem danh sách Nhiệm vụ theo tổng công ty/công ty/phòng ban/bộ phận".
- Màn /assign/tasks với cấu hình cột CŨ dựng sẵn (nhãn "Mã-Tên task", "Checklist/Task con", ẩn cột Người theo dõi, chưa có Loại nhiệm vụ): header ra đúng "Mã-Tên nhiệm vụ", "Checklist/Nhiệm vụ con", cột "Loại nhiệm vụ" TỰ chèn sau "Trạng thái", cột "Người theo dõi" vẫn ẩn theo đúng lựa chọn user. Popup "Tuỳ chỉnh cột" cũng đọc nhãn mới. Ô Checklist ra "Liên kết: 0 nhiệm vụ".
- Báo cáo hiệu suất NV theo dự án: "Số nhiệm vụ được giao"; Báo cáo phân bổ nguồn lực + Công việc của tôi: không còn chữ "task" nào trên giao diện.
- Dữ liệu test đã dọn: `column_customizations.tasks` của user 13 trả về NULL như trước.
Ảnh: `.plans/task-nhiem-vu/screenshots/tc11453-fix-*.png`
Đang làm dở: không có.
Bước tiếp theo: user duyệt → ghi chú phản hồi lên Redmine #11453 và chuyển trạng thái.
Blocked: không có.

## Phase 7 — Chỉnh hiển thị bảng danh sách nhiệm vụ (16/09/2026)
- [x] Cột "Dự án" quá hẹp (tên dự án bó xuống 4-5 dòng) → `width/minWidth: 200px`, bám width cột Dự án của `pages/assign/product-project/index.vue:405`
- [x] Khi cuộn ngang, cột ghim "Mã-Tên giải pháp" ĐÈ LÊN "Mã-Tên nhiệm vụ": `V2BaseDataTable.getStickyColumnStyle()` tính `left` của cột ghim bằng TỔNG `width`/`minWidth` **khai báo** của các cột ghim trước nó — `taskInfo` không khai width nên cộng 0, cả 2 cột cùng `left: 60px`. Khai `width/minWidth` cho `taskInfo` (300px) + `solutionInfo` (210px) → đo lại: 3 cột ghim nằm liền kề 255→315→615→825, hết chồng
- [ ] (CHƯA LÀM — cần user quyết) Lỗi gốc nằm ở component dùng chung `V2BaseDataTable`: nên đo width thật từ DOM thay vì đọc khai báo, vì mọi màn có cột ghim mà quên khai width đều dính lỗi này

## Fix nhỏ (2026-09-18) — popup nhiệm vụ mất nhãn Giải pháp / Dự án / Hạng mục
- [x] BE `DetailTaskResource`: trả thêm `solution_code/name`, `project_code/name`, `solution_module_code/name`; `TaskController::show` eager load `solution`, `modules`
- [x] FE `CreateTaskModal.vue`: bộ lọc `ALLOWED_SOLUTION_STATUSES_FOR_TASK` và `ALLOWED_MODULE_STATUSES_FOR_TASK` chỉ áp cho danh sách chọn mới, luôn giữ giá trị đang gắn
- [x] FE: thêm `ensureLinkedOptions()` — vá nhãn 4 ô liên kết từ dữ liệu API chi tiết (không gọi thêm request), vì options nạp 1 lần lúc mở popup và lọc `mine=1` nên `include_id` không bao giờ kịp gửi ở luồng Xem/Sửa

## Phản hồi #17 (2026-10-16, nhánh develop) — thông báo nhiệm vụ
- [x] `TaskService::handleStatusNotification`: 8 câu thông báo trạng thái → `buildNotificationContent('TASK', …)` theo skill notification-convention
- [x] Giao nhiệm vụ cho A ở trạng thái "Chờ phê duyệt triển khai" (tạo mới / Nháp → Chờ phê duyệt) thì báo luôn cho A, không đợi duyệt
- [x] `sendTaskNotification`: `array_unique` người nhận (ảnh tester có 2 thông báo giống hệt)
- [x] Test API local 16/10: tạo NV giao cho A ở Chờ phê duyệt → người duyệt nhận `[TASK] Chờ duyệt…`, A nhận `[TASK] Tạo mới… Chờ phê duyệt triển khai. Hạn: …`; ở Chờ bắt đầu → A nhận `[TASK] Tạo mới… Hạn: …`; duyệt triển khai → A nhận `[TASK] Đã duyệt…`; tên >50 ký tự tự cắt `...`. Đã xoá NV + thông báo test
- Chưa làm (ngoài phản hồi #17): 4 thông báo bình luận ở `TaskCommentController` vẫn câu tự do

## Thu hồi / Hủy nhiệm vụ (2026-11-18, nhánh gop_db) — @cuong61n
Nghiệp vụ: **Thu hồi** = người nhận CHƯA bấm "Bắt đầu làm" (Chờ phê duyệt triển khai / Chờ bắt đầu) → về Nháp để sửa / giao người khác / xóa. **Hủy** = người nhận ĐÃ bắt đầu (Đang thực hiện / Tạm dừng / Từ chối kết quả) → Hủy, báo người làm, đóng hẳn không sửa nữa. Chỉ người giao thực hiện; Hủy bắt buộc lý do. User chốt 18/11.
- [x] BE `Task`: hằng `RECALLABLE_STATUSES` / `CANCELLABLE_STATUSES`; `getAllowedNextStatuses()` thêm Nháp (Thu hồi) và Hủy cho người giao; `canEdit()` = false khi đã Hủy (2026-11-18)
- [x] BE `TaskService::update`: việc đã Hủy → 423; Hủy thiếu lý do (`status_note`) → 422 "Vui lòng nhập lý do huỷ."; lịch sử Thu hồi tự ghi chú "Thu hồi nhiệm vụ"; thông báo cho người nhận (nhóm `Hủy`, quy ước không có nhóm "Thu hồi") (2026-11-18)
- [x] FE `taskPanelHelpers.transitionAction`: nút "Thu hồi" (secondary) + "Hủy" (danger, popup lý do bắt buộc); `TaskPanel` + `TaskGroupListView` gửi lý do qua `reasonField` (2026-11-18)
- Chỗ hiển thị: mọi nơi dùng `allowed_next_statuses` (panel chi tiết, menu Đổi trạng thái trong danh sách nhóm chat) tự có 2 nút, không sửa riêng từng màn
- [ ] Chờ test: màn `pages/assign/tasks` (danh sách cũ) chưa thêm nút; chưa test UI bằng Playwright (chờ user bảo)
- Trạng thái: sửa trên worktree gop_db-api / gop_db-client, chưa commit
- [x] App `TPE_APP` (nhánh tpe, 2026-11-18) `ui/work/task/work_task_detail_page.dart`: thêm bước "Thu hồi" (xác nhận) + "Hủy" (sheet "Hủy nhiệm vụ", lý do bắt buộc gửi `status_note`, nút đỏ, nút kia "Đóng"); hiện trong pill "Đổi trạng thái" theo `allowed_next_statuses`. `dart analyze` sạch; chưa bấm thử simulator, chưa commit
- [x] Test 2026-11-18 (local, API worktree gop_db-api cổng 8003, DB local_hrm_erp; đã dọn dữ liệu thử): **API** Thu hồi (Chờ bắt đầu + Chờ duyệt TK → Nháp, có lịch sử "Thu hồi nhiệm vụ" + thông báo), Hủy (Đang thực hiện/Tạm dừng), Hủy thiếu lý do → 422, sửa/đổi trạng thái việc đã Hủy → 423/403. **Web Playwright** (panel): nút Thu hồi/Hủy, popup "Hủy nhiệm vụ" + ô lý do bắt buộc + nút "Hủy"/"Đóng", sau Hủy panel khoá. **App iOS simulator iPhone 15 Pro**: Thu hồi (popup xác nhận → Nháp + Xoá/Giao việc), Hủy qua pill Đổi trạng thái (trống lý do báo đỏ, có lý do → Huỷ, khoá). Chưa test: Android, menu Đổi trạng thái ở danh sách nhóm chat, tài khoản không phải người giao
- [x] Test bổ sung 2026-11-18 (app iOS simulator, API worktree cổng 8003): (1) **Tài khoản KHÔNG phải người giao** (Đào Thị Thúy là người làm, DNS Admin giao): việc Chờ bắt đầu chỉ có Tạm dừng / Bắt đầu, pill chỉ có Bắt đầu · Tạm dừng · Từ chối nhận việc; việc Đang thực hiện chỉ có Tạm dừng / Tiến độ / Hoàn thành, pill chỉ có Hoàn thành · Tạm dừng · Từ chối nhận việc → KHÔNG có Thu hồi / Hủy. (2) **Chat nhóm** (nút 📋 "Việc của nhóm"): danh sách nhóm hiện đủ 4 việc, mở việc do mình giao từ nhóm vẫn có Thu hồi. Lưu ý môi trường: DB local thiếu migration chat/workspace của phiên khác (chat_message_hides, mention_all, chat_message_links, meetings/issues.workspace_id) → đã chạy riêng từng file với --path; dữ liệu thử (nhóm [TEST-HUY], việc, hội thoại) đã xoá
- [x] App 2026-11-18: nút **Hủy** đưa lên thanh nút đáy (nút đỏ cuối, cạnh nút chính) cho khớp web (Tạm dừng · Tiến độ · Báo kết quả · Hủy) — user chọn thay vì để trong pill. Người giao cũng là người làm vẫn được Hủy (BE cho phép). `work_task_detail_page.dart` `_footer` / `_footerActs`; `dart analyze` sạch; đã kiểm trên iOS simulator với task TPE.TASK.NB.26.0993
- [x] App 2026-11-18 (thay cho dòng "Hủy ở thanh đáy" phía trên): thanh nút đáy **kiểu D** (user chọn trên bản vẽ Pencil `meeting-mobile_v2.pen`, frame "Chi tiết nhiệm vụ · Thanh nút đáy — các kiểu"): có nút chính và từ 2 hành động phụ trở lên (hoặc có Hủy) → đáy chỉ [nút chính][nút ⋮ chỉ icon]; sheet liệt kê Tạm dừng · Cập nhật tiến độ · Hủy nhiệm vụ (đỏ). Sheet "Hủy nhiệm vụ": 2 nút Hủy / Đóng rộng bằng nhau (`equalButtons` ở `work_edit_sheet.dart`). Tách `_sheetMenu` dùng chung với menu ⋮ header. Nút ⋮ chỉ icon là ngoại lệ có chủ ý của quy tắc "nút luôn kèm chữ" (user chốt). Web giữ 4 nút như cũ. `dart analyze` sạch, đã xem trên iOS simulator
- [x] **Đã deploy prod 2026-11-18** (hrm.eteksofts.com, nhánh gop_db): BE commit `6e3f146af` (merge `78b24e17b`), FE commit `5afbc4a41` (merge `0e767d365`); chạy `~/build_tpe.sh` (không có migration mới, route:cache + queue:restart + build FE xong, `hrm-client-tpe` khởi động lại). Web 200, API 401 khi chưa đăng nhập (bình thường). **App** đẩy nhánh `develop` commit `c5f04d0` (chưa phát hành bản build/TestFlight). Chưa kiểm tay Thu hồi/Hủy trên prod
- [x] **App phát hành 2026-11-19** (HRM TPE `tpeProd`, version 2.4.0, **build 112**, build từ `tpe` = `develop` = `0ce2db5`): iOS đã lên TestFlight (build 112 VALID, app đặt tên ETEK SOFTS trên App Store Connect), Android đã gửi Google xét duyệt kênh production (versionCode 112). Gồm Thu hồi/Hủy nhiệm vụ + thanh nút đáy mới + các commit chat của người khác. Build 111 (lên TestFlight 18/11 ngoài ý muốn) vẫn còn. Chưa gán build 112 vào nhóm tester external TestFlight
- [x] **Play đổi tên cửa hàng 2026-11-19**: tên trang thông tin mặc định (vi) `HRM TPE` → `ETEK SOFTS`, làm trên Play Console qua Playwright (tài khoản dịch vụ API không có quyền sửa trang cửa hàng → 403). Lần gửi mã **#68** "Danh sách cửa hàng" đang "Đang xem xét". Bản 112 (mã #67) đã "Đã xuất bản". Icon cửa hàng đã là logo ETEK SOFTS nên giữ nguyên; mục khai báo AI giữ như cũ ("Không gắn nhãn")
- [x] **Play từ chối đổi tên (#68, 19/11)**: lý do "Chính sách quyền riêng tư không hợp lệ — thông tin ứng dụng/nhà phát triển không trùng khớp" (trang freeprivacypolicy.com chỉ nói "HRM TPE", không có ETEK SOFTS / tên pháp nhân). Xử lý: tạo `hrm-client/static/privacy-policy.html` (nội dung cũ, nêu ETEK SOFTS (tên cũ HRM TPE), package, CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT, email cntt.tanphat@gmail.com) → commit `b37aa3b41` nhánh gop_db, deploy prod, URL https://hrm.eteksofts.com/privacy-policy.html (HTTP 200). Play Console: đặt URL chính sách mới + gửi lại cùng thay đổi tên (2 thay đổi), đang chạy kiểm tra nhanh ≤13 phút rồi vào hàng xét duyệt. Chờ Google
- [x] **Play đã duyệt (19/11 09:57, lần gửi #69 "Đã xuất bản")**: tên cửa hàng = ETEK SOFTS + URL chính sách mới https://hrm.eteksofts.com/privacy-policy.html. Deploy web prod xong 09:58 (marker b37aa3b41)

## Vấn đề (Issue) đổi trạng thái / đổi người phụ trách ⇒ báo vào chat nhóm — @cuong61n (2026-11-19)

Nghiệp vụ: nhiệm vụ trong nhóm đổi trạng thái đã có tin hệ thống vào chat nhóm; Vấn đề của nhóm (có `workspace_id`) đổi trạng thái hoặc đổi người phụ trách thì nhóm không thấy gì. Làm cho Vấn đề báo giống nhiệm vụ.
- [x] Chốt mốc báo trạng thái (2026-11-19): Đang xử lý · Đã xử lý xong · Hoàn thành · Từ chối · Đã đóng · Mở lại. KHÔNG báo Mới ghi nhận / Đã phân công (phân công báo bằng tin riêng bên dưới). Khớp `Task::WORKSPACE_ANNOUNCE_STATUSES`
- [x] BE (nhánh gop_db, worktree gop_db-api, 2026-11-19): `Issue::WORKSPACE_ANNOUNCE_STATUSES`; `IssueService::announceInWorkspace` (dùng chung: có `workspace_id`, nhóm chưa đóng, lỗi chỉ ghi log) cho 2 hành động `issue_status_changed` + `issue_assignee_changed`; `SyncWorkspaceChat` thêm câu + meta (chữ + màu trạng thái, tên người cũ/mới), không phát conversation.updated cho cả nhóm
- [x] Đổi người phụ trách (user yêu cầu 2026-11-19): chỉ có 1 đường duy nhất là `changeStatus` với status=assigned và người phụ trách khác trước. Lần đầu phân công ⇒ "đã được A phân công cho B"; đổi người ⇒ "đổi người phụ trách từ: A → B"; giao lại đúng người cũ ⇒ không báo
- [x] FE web (gop_db-client): `components/chat/ChatMessageItem.vue` dòng tin Vấn đề mờ, bấm mở IssuePanel (`open-issue`), icon theo mốc; dùng lại class dòng nhiệm vụ nên không thêm CSS
- [x] App TPE_APP (nhánh tpe, worktree tpe_app): `ui/chat/widget/system_pill.dart` + nối `onOpenIssue` ở `chat_room_page.dart`, cả tin trạng thái lẫn tin đổi người phụ trách
- [x] Test BE: `IssueStatusWorkspaceMessageTest` 5 case (mỗi mốc 1 tin + đúng câu/meta/màu; ngoài nhóm / nhóm đóng không báo; phân công lần đầu; đổi người; giao lại cùng người không báo) pass; `TaskStatusWorkspaceMessageTest` 3, `IssueV2ApiTest` 67, `ChatIssueCardTest` 16 pass (chạy từng file riêng — artisan chỉ chạy file đầu khi truyền nhiều file)
- [x] Test app: `chat_room_widgets_test.dart` thêm 2 test (tin trạng thái, tin đổi người phụ trách) — 15/15 pass; `fvm flutter analyze` 2 file sửa sạch
- [x] Test web Playwright (2026-11-19, :3002 → API :8003, nhóm `[TEST-ISSUECHAT]`): đổi trạng thái bằng giao diện (Báo đã xử lý → Hoàn thành, Mở lại) và API (Đang xử lý, Đã đóng) đều ra đúng tin, mã + tên đậm, 2 trạng thái đúng màu; bấm dòng mở đúng panel Vấn đề; đổi người phụ trách bằng popup → tin "đổi người phụ trách từ: DNS Admin → Nguyễn Văn Mởn", trạng thái vẫn Đã phân công, không thêm tin trạng thái
- [x] Sửa môi trường local: DB thiếu cột `issues.source_message_id` (migration GĐ35 `2026_11_25_000001` của phiên khác chưa chạy) làm gửi mọi tin chat ở local trả 400 — đã chạy riêng file đó bằng `--path` (idempotent). Dev/prod phải có migration này khi deploy tính năng chat
- [x] App đồng bộ câu chữ với web (2026-11-19, user chỉ ra app khác web): `system_pill.dart` đổi sang câu đầy đủ "Nhiệm vụ/Vấn đề **mã** đã được **tên đầy đủ** cập nhật từ: A → B" (mã + tên đậm, 2 trạng thái tô màu BE, icon theo mốc khớp web `taskIcon`/`issueIcon`, giờ cuối dòng) — áp CẢ tin Nhiệm vụ (trước đây app dùng câu gọn "mã · Admin: A → B") lẫn Vấn đề; 3 test cũ cập nhật theo câu mới, toàn bộ `test/ui/chat` 382/382 pass. Nếu muốn giữ câu gọn ở app thì chỉ cần hoàn lại file này
- [x] Test simulator (2026-11-19, user cho dùng thiết bị đang bật; iPhone 15 iOS 17.5 + Android emulator-5554; app `flutter run` của phiên khác từ TPE_APP/app, API :8003, TK DNS Admin): hot reload bản sửa tạm vào TPE_APP rồi HOÀN TÁC bằng git checkout 2 file (không đụng 6 file đang sửa của phiên kia). iOS: 8 dòng tin Vấn đề hiển thị đúng (5 tin trạng thái, 1 tin đổi người phụ trách, 1 tin đóng từ app), bấm dòng mở đúng chi tiết Vấn đề (cả dòng trạng thái lẫn dòng đổi người phụ trách); đóng Vấn đề từ app (Xử lý → Đã đóng + lý do, bàn phím ảo không che nút) ⇒ tin "Đã phân công → Đã đóng" xuất hiện khi vào lại nhóm. Android: danh sách + nhóm + 8 dòng giống iOS và giống web
- [ ] CHƯA test: realtime socket local (app báo "Đang kết nối lại", web tin không tự hiện, phải tải lại — socket không chạy ở local, chưa xác minh); app không có màn Đổi người phụ trách riêng nên đổi người phụ trách chỉ test từ web
- [x] Quyết định đã chốt (2026-11-19): người nhận mới khi đổi người phụ trách chỉ cần chuông có sẵn (`notifyAssigned`), KHÔNG @nhắc tên trong tin nhóm, KHÔNG tự thêm vào nhóm
- Dữ liệu thử local còn lại: nhóm id 71 `[TEST-ISSUECHAT]`, hội thoại 74, issue 266/267, 1 tin chữ "[TEST] xin chao" — để test app, dọn sau
- [x] Đã đẩy + deploy (2026-11-19): API commit `2a8e93a1c` + web commit `594716ec4` lên nhánh `gop_db`; chạy `~/build_tpe.sh` trên prod (hrm.eteksofts.com) thoát mã 0 — fast-forward đúng 4 file API, không có migration chờ, route:cache + catalog-sync (949 quyền, không đổi) OK, `hrm-client-tpe` khởi động lại, web 200; prod trước đó đúng bằng origin nên chỉ mang commit của tôi
- [x] App đẩy lên git, CHƯA build: nhánh `tpe` commit `31e9c8d`, nhánh `develop` commit `a237582` (cherry-pick sạch, 3 file giống hệt bản đã test)
- [x] Dọn file local đã có trên remote (gop_db-api, gop_db-client, tpe_app, TPE_APP) — còn giữ 5 file Catalog quyền ở gop_db-api và 2 file task ở TPE_APP vì chưa có trên remote (việc dở của phiên khác)
