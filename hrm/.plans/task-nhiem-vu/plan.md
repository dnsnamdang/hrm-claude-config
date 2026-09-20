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
