# Khảo sát chức năng Nhiệm vụ (Task) — bản web HRM, nhánh `gop_db`

> Khảo sát CHỈ ĐỌC ngày 29/10/2026, phục vụ thiết kế đưa Nhiệm vụ lên app mobile Flutter.
> Repo: `hrm-client` (Nuxt 2) và `hrm-api` (Laravel, module `Modules/Assign`), cả 2 đứng ở `gop_db`.
> Các file Nhiệm vụ đọc dưới đây KHÔNG nằm trong danh sách file đang sửa local (file sửa local chỉ thuộc
> phần giá/hàng hoá), nên nội dung khớp `origin/gop_db`.
> Quy ước căn cứ: `FE:` = `hrm-client/…`, `BE:` = `hrm-api/Modules/Assign/…` (trừ khi ghi rõ đường dẫn khác).

## Mục lục

1. [Lối vào, menu, route](#1-lối-vào-menu-route)
2. [Danh sách màn/popup và hành động](#2-danh-sách-mànpopup-và-hành-động)
3. [Form tạo/sửa — toàn bộ trường](#3-form-tạosửa--toàn-bộ-trường)
4. [Popup Nhập kết quả / Duyệt kết quả](#4-popup-nhập-kết-quả--duyệt-kết-quả)
5. [Vòng đời trạng thái](#5-vòng-đời-trạng-thái)
6. [Quyền và điều kiện thao tác](#6-quyền-và-điều-kiện-thao-tác)
7. [Màn danh sách: cột, bộ lọc, sắp xếp, thống kê](#7-màn-danh-sách-cột-bộ-lọc-sắp-xếp-thống-kê)
8. [Báo cáo tiến độ hằng ngày (daily report)](#8-báo-cáo-tiến-độ-hằng-ngày-daily-report)
9. [Bình luận](#9-bình-luận)
10. [Lịch sử thay đổi](#10-lịch-sử-thay-đổi)
11. [Thông báo / nhắc hạn](#11-thông-báo--nhắc-hạn)
12. [Quan hệ với đối tượng khác](#12-quan-hệ-với-đối-tượng-khác)
13. [API endpoint cho app](#13-api-endpoint-cho-app)
14. [Điểm lạ / bug / fail-open](#14-điểm-lạ--bug--fail-open)
15. [Gợi ý cho thiết kế app](#15-gợi-ý-cho-thiết-kế-app)

---

## 1. Lối vào, menu, route

### 1.1 Menu
- Sidebar nhóm **"Nhiệm vụ"** (`FE: components/menu-sidebar.js:39-61`):
  - `Nhiệm vụ` → `/assign/tasks`
  - `Vấn đề` → `/assign/issues`
  - `Phiếu bàn giao` / `Tạo bàn giao` / `Chờ tiếp nhận bàn giao` → `/assign/handover*`
  - `Cập nhật tiến độ nhiệm vụ` → `/assign/tasks/daily-report`
  - Không có `isShow` gate theo quyền → ai đăng nhập cũng thấy menu.
- Menu phân hệ Presale: `Nhiệm vụ` → `/assign/tasks`, `isShow: true` (`FE: components/subsystem-menu/presale.js:69-74`).
- Hai page khai `layout: 'default-sidebar'` (`FE: pages/assign/tasks/index.vue:380`, `daily-report.vue:212`).

### 1.2 Mọi nơi nhúng Nhiệm vụ (FE)

| Lối vào | File | Nhúng gì | Gọi API danh sách |
|---|---|---|---|
| Màn Nhiệm vụ | `pages/assign/tasks/index.vue` | `CreateTaskModal`, `ImportResultModal`, `TaskHistoryModal` | `GET assign/tasks` |
| Cập nhật tiến độ | `pages/assign/tasks/daily-report.vue` | — | `GET assign/tasks/daily-report` |
| Công việc của tôi — tab Nhiệm vụ | `pages/assign/my-job/components/TasksTab.vue` | 3 modal trên | `GET assign/my-job/task-list` (`:777`) |
| Công việc của tôi — Tổng quan "Nhiệm vụ hôm nay" | `my-job/components/TodayTasks.vue` (qua `OverviewTab.vue:18`) | chỉ hiển thị | `GET assign/my-job/today-tasks` (`my-job/index.vue:318`) |
| Công việc của tôi — popup "Nhiệm vụ sắp hết hạn" | `my-job/components/TaskUpcomingModal.vue` | 2 modal | `GET assign/my-job/task-upcoming-schedule` (`:424`) |
| Chi tiết Dự án — tab Nhiệm vụ | `prospective-projects/_id/manager.vue:106-109` → `components/assign/task/TaskListTab.vue` scope `{project_id}`, `can-create=!isProjectClosed` | 3 modal | `GET assign/tasks?prospective_project_id=` |
| Chi tiết Meeting — tab Nhiệm vụ | `meeting/components/MeetingForm.vue:131` → `TaskListTab` scope `{meeting_id}` | 3 modal | `GET assign/tasks?meeting_id=` |
| Biên bản họp — giao việc từ dòng biên bản | `meeting/components/MeetingReport.vue:1105-1120` | `CreateTaskModal.create(defaults)` điền sẵn `meeting_id, meeting_report_id, title, due_date, task_type, assignee_id(s)` | — |
| Giải pháp — tab Nhiệm vụ | `solutions/components/manager/TasksTab.vue` (tạo: `:870-874` khoá `solution_id, project_id`) | 3 modal | `GET assign/solutions/{id}/manager/tasks` (`:677`) |
| Giải pháp — thẻ Chờ duyệt | `solutions/components/manager/PendingApprovalCard.vue:85-108` | 2 modal | `GET assign/solutions/{id}/manager/pending-approvals` |
| Giải pháp — popup sắp hết hạn / trễ | `solutions/components/manager/TaskUpcomingModal.vue`, `CategoryLateTasksModal.vue`, `PeopleLateTasksModal.vue` | | `…/manager/tasks-upcoming`, `categories-late`, `people-late` |
| Giải pháp — tab Tệp | `solutions/components/manager/FilesTab.vue:442` | `view(..., {hideActions:true})` | |
| Hạng mục giải pháp — tab Nhiệm vụ | `solution-modules/_id/components/TasksTab.vue` (tạo `:793-797` khoá `solution_id, solution_module_id, project_id`) | 3 modal | `GET assign/solution-modules/{id}/manager/tasks` (`:600`) |
| Hạng mục — PendingApprovalModal, TaskUpcomingModal, FilesTab | `solution-modules/_id/components/*` | | |
| My-todo (lịch làm việc) | `pages/assign/my-todo/index.vue:342` | `create({start_date, due_date})` theo ô ngày bấm | |
| Bàn giao | `handover/add.vue:248`, `handover/_id/index.vue:152`, `handover/_id/receive.vue:133` | chỉ `view()` nhiệm vụ trong phiếu | |
| Báo cáo hiệu suất NV | `report/employee-work-performance/components/WorkDrillModal.vue:822` | `view(..., {hideActions:true})` | |
| Thông báo (chuông) | URL `/assign/tasks?open_task={id}[&comment_id=]` → `index.vue:1191-1205` mở popup Xem | | |
| Badge sidebar | `components/training-components/Sidebar.vue:371` | | `GET assign/tasks/daily-report/count` |

### 1.3 Route BE chính (`BE: Routes/api.php:1075-1096`)
Xem chi tiết ở [mục 13](#13-api-endpoint-cho-app). Toàn bộ nhóm `/assign/tasks` **không gắn `checkPermission`**; chỉ `POST /` có middleware `solutionMemberActive` (`api.php:1084`) — chặn 403 nếu user đã bị khoá khỏi giải pháp `solution_id` gửi lên (`hrm-api/app/Http/Middleware/CheckSolutionMemberActive.php:34-50`).

---

## 2. Danh sách màn/popup và hành động

### 2.1 Màn danh sách `/assign/tasks` (`FE: pages/assign/tasks/index.vue`)
- Toolbar: **Tạo mới** (`:62-67`, không gate quyền) · **Xuất Excel** (`:70-82`, mở popup chọn cột) · **Cấu hình cột** (`:83-91`).
- Dòng lọc nhanh `#left-actions` (`:97-141`): chip `Tổng: n`, `Quá hạn: n` + 4 nút vai trò (mục 7.3) + chip tag đang lọc.
- Click **Mã nhiệm vụ** → popup Xem (`:150-154`, `viewTask` `:1223`).
- Hành động dòng `getRowActions` (`:1245-1271`):

| Nút | Điều kiện hiện (cờ BE) | Hành vi |
|---|---|---|
| Sửa | `can_edit` | `CreateTaskModal.edit()` — **luôn** mở form tạo/sửa, kể cả trạng thái 4–9 (`:1275-1277`) |
| Xóa | `can_delete` | confirm `BaseConfirmModal` → `DELETE assign/tasks/{id}` (`:1291-1311`) |
| Nhập kết quả | `can_import_result` | `openTaskModal(item,false)` |
| Duyệt | `can_approve` | `openTaskModal(item,false)` |
| Lịch sử | luôn hiện | `TaskHistoryModal.open()` |

- `openTaskModal` (`:1227-1237`): trạng thái **4,5,6,7,8,9 → `ImportResultModal`**; 1,2,3,10 → `CreateTaskModal` (xem hoặc sửa).

### 2.2 Popup `CreateTaskModal` (`FE: pages/assign/tasks/components/CreateTaskModal.vue`)
3 chế độ: `create(defaults)` (`:2052`), `edit(task, commentId)` (`:2061`), `view(task, commentId, {hideActions})` (`:2070`).
- Tiêu đề: `{mã} — Thêm mới / Chỉnh sửa / Chi tiết nhiệm vụ` + pill trạng thái (màu FE tự map `:2932-2966`) + badge `Đơn giản/Nâng cao` (`:12-28`).
- Header: **Chế độ nâng cao / Chuyển về đơn giản** (`toggleMode`, `:31-34`) · **Xóa trắng** (khi tạo hoặc là người tạo, `:36-44`) · Đóng.
- Chế độ **Đơn giản** (`mode=1`): cột trái gồm các trường cơ bản (mục 3).
- Chế độ **Nâng cao** (`mode=2`, `:419-1412`): thêm Checklist, Nhiệm vụ con, Tệp đính kèm, Bình luận (chỉ khi xem/sửa, `:857-864`), cột phải 2 tab **Thiết lập** (Người duyệt KQ, Người theo dõi, Tags, Lặp lại, Yêu cầu báo cáo tiến độ) và **Liên kết & KPI** (liên kết nhiệm vụ). Mở ở chế độ Xem luôn ép `mode=2` (`:2163`).
- Khối **Lịch sử** `SystemInfoSection entity-type="task"` khi có `editId` (`:1416`).
- Footer (`:1420-1456`): **Xóa** (chỉ ở chế độ Xem + `can_delete`) · **Lưu** (tạo mới, hoặc sửa khi `can_edit || can_import_result || can_approve`) · **Lưu & Tiếp tục** (chỉ tạo mới — lưu xong reset form, giữ các giá trị khoá sẵn `:2895-2916`) · **Đóng**.
- Popup phụ: "Nhập số lượng" (thêm nhanh N dòng checklist/nhiệm vụ con, 1-50, `:1459-1462`), confirm xoá, confirm xoá trắng.
- Danh sách nhiệm vụ con thật (`subtasks`) hiện dạng thẻ, bấm mở `view()` nhiệm vụ con (`:576-610`, `openSubtask :2460`).

### 2.3 Popup `ImportResultModal` (`FE: pages/assign/tasks/components/ImportResultModal.vue`)
Dùng cho cả **Nhập kết quả** (người thực hiện) và **Duyệt kết quả** (người duyệt) và **Xem** trạng thái 4–9. Chi tiết [mục 4](#4-popup-nhập-kết-quả--duyệt-kết-quả).

### 2.4 Popup `TaskHistoryModal` (`FE: pages/assign/tasks/components/TaskHistoryModal.vue`)
Bọc `CatalogHistoryModal` đọc `assign/system-logs/task/{id}` (`:13`, `:33-36`).

### 2.5 Màn `/assign/tasks/daily-report` — "Nhập kết quả báo cáo tiến độ"
Chi tiết [mục 8](#8-báo-cáo-tiến-độ-hằng-ngày-daily-report).

### 2.6 Công việc của tôi — tab Nhiệm vụ (`FE: pages/assign/my-job/components/TasksTab.vue`)
- Nút: Tạo mới (`:137`), Xuất Excel (`:143`, `GET /api/v1/assign/my-job/task-list/export` `:695`), Cấu hình cột.
- Hành động dòng (`:838-893`): **Xem** (luôn), Sửa (`can_edit`), Nhập kết quả (`can_import_result`), Duyệt (`can_approve`), Lịch sử chỉnh sửa (luôn), Xoá (`can_delete`).
- 4 nút vai trò giống màn chính (`:40-80`), có cột "Vai trò của tôi" (`myRole` ← `my_role` BE).
- Bộ lọc (`:439-460`): Giải pháp, Dự án, Hạng mục, Người thực hiện, Người tạo, Trạng thái, Ưu tiên, Người duyệt KQ, Ngày cập nhật, Hạn hoàn thành.

### 2.7 Tab Nhiệm vụ của Dự án / Meeting (`FE: components/assign/task/TaskListTab.vue`)
- Dùng chung `GET assign/tasks` + `scopeQuery` (`:281-290`) nên phân quyền xem y màn chính.
- Bộ lọc (`:250-262`): Loại nhiệm vụ, Trạng thái, Ưu tiên, Người thực hiện, **Người giao** (= created_by), Người duyệt KQ, Hạn hoàn thành. Tìm nhanh "Tìm theo mã, tên nhiệm vụ" (BE bỏ tìm theo khách hàng khi có `prospective_project_id`/`meeting_id` — `TaskService.php:57-58`).
- Cột thay đổi theo scope: tab Dự án thêm cột Giải pháp, tab Meeting thêm cột Dự án (`:334-358`).
- Tạo mới truyền `scope-meeting-id` để màn Sửa khoá ô Meeting (`:126`).

---

## 3. Form tạo/sửa — toàn bộ trường

> FE **không validate phía client** — `handleSubmit` gửi thẳng, chỉ đổ lỗi 422 của BE vào `formErrors` (`CreateTaskModal.vue:2836-2926`). Dấu `*` trên nhãn FE lệch với BE ở vài trường (đánh dấu ⚠).

### 3.1 Trường cơ bản (cả 2 chế độ)

| # | Nhãn (FE) | Khoá payload | Kiểu control | `*` FE | Luật BE store (`TaskStoreRequest.php:42-112`) | Luật BE update (`TaskUpdateRequest.php:44-140`) | Nguồn danh mục / mặc định | Phụ thuộc |
|---|---|---|---|---|---|---|---|---|
| 1 | Loại nhiệm vụ | `task_type` | SearchPicker (`:71-80`) | có | `required\|integer\|in:1,2` | không có rule (không sửa được) | Hằng FE `1 Nhiệm vụ chung`, `2 Nhiệm vụ cụ thể` (`:1688-1693`); mặc định 2 | Khoá khi sửa/xem (`:79`). Đổi loại → xoá người thực hiện của loại kia (`:2386-2394`) |
| 2 | Tên công việc | `title` | V2BaseInput | có | `required\|string\|max:255` | `required\|string\|max:255` | — | |
| 3 | Giải pháp | `solution_id` | SearchPicker | không | `nullable\|integer\|exists:solutions,id` | `nullable\|…exists` | `GET assign/solutions/getAll?per_page=10000&mine=1` (+`id=`/`include_id=`), FE lọc trạng thái GP cho phép tạo việc (`:1510`, `:2531-2589`) và lọc theo dự án đang khoá | Chọn GP → tự điền Dự án theo GP, reset Hạng mục, reset Người duyệt nếu không thuộc nhân sự GP (`:2609-2641`) |
| 4 | Dự án/Nhóm | `project_id` | SearchPicker | không | `nullable\|integer\|exists:prospective_projects,id` | idem | `GET assign/prospective-projects/getAll?per_page=10000&mine=1` (`:2463-2499`) | **Khoá khi đã chọn Giải pháp** (`isProjectFieldDisabled :1812-1819`) |
| 5 | Hạng mục/Module | `solution_module_id` | SearchPicker | `*` khi GP có hạng mục | `required` nếu `solutions.has_modules`, ngược lại `nullable` (`:50`, `:176-183`) | `nullable` (không bắt buộc khi sửa) | `modules` trong response solutions/getAll, lọc trạng thái hạng mục `Đã duyệt`/`Chờ duyệt hồ sơ` (`:1512`, `:1884-1902`) | Chỉ mở khi đã chọn GP và GP có hạng mục |
| 6 | Meeting | `meeting_id` (+ `meeting_report_id` ẩn) | SearchPicker | không | `nullable\|exists:meetings,id` · `meeting_report_id nullable\|exists:meeting_reports,id` | idem | `GET assign/meeting/task-options?limit=200[&include_id=]` (`:2504-2522`; BE `Routes/Meeting/api.php:34` → `MeetingController::taskOptions :1165`) | Đổi meeting → bỏ `meeting_report_id` (`:2604-2608`). Khoá ở màn Sửa nếu task sinh từ dòng biên bản hoặc mở từ tab Meeting đó (`:1825-1833`) |
| 7 | Người thực hiện | `assignee_id` (NV cụ thể) / `assignee_ids[]` (NV chung) | SearchPicker / MultiSearchPicker (`:186-208`) | có | NV chung: `assignee_ids required\|array\|min:1`, `assignee_ids.* exists:employees`; NV cụ thể: `assignee_id required\|integer\|exists` (`:59-61`) | `assignee_id nullable` | `GET assign/tasks/employees` — NV đang làm (`employee_infos.status=1`) của công ty hiện tại, loại phòng ban `cooperation_type=2` (`TaskController.php:83-110`) | Chọn người thực hiện → tự thêm vào Người theo dõi (`:2377-2400`) |
| 8 | Trạng thái | `status` | SearchPicker (`:248-259`) | không | `required\|integer` (**không giới hạn giá trị**) | `required\|integer` + kiểm chuyển trạng thái ở service | Tạo mới: hằng FE `1 Nháp, 2 Chờ phê duyệt triển khai, 3 Chờ bắt đầu, 4 Đang thực hiện` (`:1903-1912`), mặc định 1. Sửa: `allowed_next_statuses` do BE trả | Ẩn khi xem; ở màn Sửa chỉ hiện khi có `allowed_next_statuses` và có ít nhất 1 cờ edit/import/approve (`:219-227`) |
| 9 | Mức độ ưu tiên | `priority` | SearchPicker | ⚠ không có `*` | `required\|integer` | `required\|integer` | Hằng FE `1 Bình thường, 2 Cao, 3 Khẩn cấp` (`:1519-1523`) | |
| 10 | Hạn hoàn thành | `due_date` | V2BaseDatePicker `YYYY-MM-DD` | ⚠ có `*` | `nullable\|date` + after: không ở quá khứ (`:126-139`) | `nullable\|date`; chặn quá khứ **chỉ khi task đang Nháp** (`:163-180`) | Mặc định hôm nay (`seedDates :2371-2375`) | Đổi hạn cha → ghi đè hạn mọi nhiệm vụ con (`watch :1915-1930`) |
| 11 | Giờ hạn | `due_time` | V2BaseDatePicker `HH:mm` | ⚠ có `*` | `nullable`; nếu ngày = hôm nay thì ≥ hiện tại (`:141-146`) | idem (chỉ khi Nháp) | Mặc định `17:00` | |
| 12 | Mô tả | `description` | V2BaseTextarea | không | `nullable\|string` | idem | | |
| 13 | Số giờ được giao | `estimated_hours` | V2BaseInput number step 0.5 | có | `required\|numeric\|min:0` | không có rule | | Dùng tính Hiệu suất |
| — | Ngày bắt đầu | `start_date` | **Ô đã comment-out** (`:300-325`) | — | rule comment-out (`:54`) | idem | FE tự gán hôm nay khi tạo (`:2373`) hoặc ngày từ lịch my-todo | Không sửa được trên UI |
| — | Chế độ | `mode` | nút toggle | — | không rule | | 1 Đơn giản / 2 Nâng cao, lưu vào task | |

Ràng buộc chéo (store + update): hạn nhiệm vụ con không được sau hạn nhiệm vụ cha (`TaskStoreRequest.php:148-167`, `TaskUpdateRequest.php:182-201`).

### 3.2 Trường chế độ Nâng cao

| Khối | Khoá payload | Control | Luật BE | Ghi chú |
|---|---|---|---|---|
| Checklist | `checklists[] {id?, content, is_done}` | ô nhập + Enter, sửa nội dung từng dòng, xoá, thêm nhanh N dòng (`:419-489`) | store `checklists.*.content required\|max:500`; update `nullable\|max:500`, thêm `is_done`, `result_note` | id tạm `temp_*` bị bỏ khi gửi (`:2854-2860`). BE không xoá dòng bị bỏ khỏi payload (chỉ update/create — `TaskService.php:629-661`) |
| Nhiệm vụ con | `children[] {id?, title, assignee_id, due_date, due_time, is_done}` | dòng nhập + bảng (`:491-704`) | store: `title required`, `assignee_id required\|exists`; update: `assignee_id nullable` | Lưu vào bảng `task_children`; khi task không còn ở Nháp/Chờ duyệt triển khai thì mỗi dòng **sinh thành task thật** (`parent_id`) — `createChildrenAsTasks` (`TaskService.php:805-840`). Đã có task con thật thì UI chuyển sang danh sách thẻ (`hasChildrenTasks`) |
| Tệp đính kèm | `attachments[] {name, attachment_type_id, file_name, file_path, file_type, file_size}` | bảng tự dựng (`:705-853`) | `name, attachment_type_id (exists:attachment_types), file_name, file_path, file_size` đều `required` | Upload trước qua store `uploadImage` (`:2722-2750`); đuôi cho phép jpg/jpeg/png/doc/docx/xls/xlsx/pdf/ppt/pptx, ≤ 50MB (`:2692-2707`). Loại tài liệu từ `GET assign/attachment-types/getAll` (`:2590-2600`). BE đồng bộ vào bảng `files` (`table='tasks'`) qua `TableFileHelper::syncForTable` (`TaskService.php:765-786`) |
| Người duyệt kết quả | `approver_id` | SearchPicker (`:898-919`) | `nullable\|exists:employees` | Mặc định = người tạo (`seedDefaults :2247-2258`). Nếu đã chọn GP: chỉ PM + staff GP + leader/staff hạng mục (`approverOptionsForSolution :1840-1864`) |
| Người theo dõi | `watchers[]` | MultiSearchPicker | `watchers.* exists:employees` | Mặc định có người tạo. Nguồn `$store.state.employees` |
| Thẻ (Tags) | `tags[]` (chuỗi tên) | nhập + Enter | `tags.* string\|max:100` | BE `Tag::firstOrCreate` theo slug (`TaskService.php:605-621`) |
| Lặp lại | `recurring {is_active, repeat_type, repeat_interval, end_type, week_days[], month_day, cron_expression, end_date, max_occurrences}` | checkbox + khối (`:1009-1203`) | store `repeat_type in:1,2,3,4`; **update `in:1,2,3`** | repeat_type 1 ngày/2 tuần/3 tháng/4 Tùy chỉnh (cron); end_type 1 không kết thúc/2 đến ngày/3 sau N lần (`Entities/Task/TaskRecurringRule.php`) |
| Yêu cầu báo cáo tiến độ | `progress_report {is_active, cycle_type, send_time, week_days[], month_day}` | checkbox + khối (`:1205-1305`) | `cycle_type in:1,2,3`, `send_time H:i:s` (BE tự thêm `:00` nếu gửi `H:i`), `month_day 1-31` | cycle 1 ngày/2 tuần/3 tháng (`TaskProgressReportRule.php`). Bật → task xuất hiện ở daily report |
| Liên kết nhiệm vụ | `linked[] {linked_task_id, link_type}` | chọn kiểu + tìm nhiệm vụ (`:1333-1410`) | không có rule | Kiểu FS/SS/FF/SF/RL (`TaskLink.php:18-30`). Nguồn tìm: `GET assign/tasks/getAll?per_page=10000` gọi ở `created()` (`:2523-2530`). BE xoá hết rồi tạo lại (`TaskService.php:788-802`) |

### 3.3 Hành vi lưu (BE)
- **Nhiệm vụ chung** (`task_type=1`): mỗi người trong `assignee_ids` thành 1 task độc lập, chung `batch_id` UUID; tệp upload 1 lần (`TaskService.php:354-372`). Toast "Đã tạo N nhiệm vụ thành công" (`CreateTaskModal.vue:2884-2891`).
- Mã: `{mã công ty}.TASK.NB.{yy}.{NNNN}` — luôn `NB` vì gọi `generateCode(false)` (`Task.php:327-352`, `TaskService.php:416`).
- Gắn `solution_version_id/code`, `module_version_id/code` theo version hiện hành (`TaskService.php:423-442`).
- Đồng bộ bảng `task_org_units` (org của người tạo/thực hiện/duyệt/theo dõi) phục vụ phân quyền xem cấp tổ chức (`:308-352`).
- Tính lại tiến độ hạng mục/giải pháp `ProgressCalculator` (`:457`, `:571-577`).
- Sửa: mọi trường dùng `$request->x ?? $task->x` (`:496-519`) → **không xoá được giá trị về rỗng** (xem mục 14).

---

## 4. Popup Nhập kết quả / Duyệt kết quả

`FE: pages/assign/tasks/components/ImportResultModal.vue` — tiêu đề "Nhập kết quả nhiệm vụ" / "Xem kết quả nhiệm vụ" (`:16`).

- Phần thông tin chỉ đọc: Tên, Ưu tiên, Dự án, Hạng mục, Người thực hiện, Hạn, Giờ hạn, Mô tả (`:45-165`).
- **Trạng thái**: SearchPicker từ `allowed_next_statuses` (`:52-64`, `:1374-1379`); chọn 6/8 (Hoàn thành) và không bật báo cáo tiến độ → tự set Tiến độ = 100 (`onStatusChange :1409-1417`).
- **Kết quả — Chế độ A (không bật báo cáo tiến độ)** (`:181-261`): Số giờ được giao (đọc) · **Số giờ làm thực tế `*`** · **Tiến độ (%) `*`** 0..100 (khoá khi chọn trạng thái hoàn thành) · Hiệu suất (đọc, = giao/thực tế×100) · **Kết quả thực hiện `*`**.
  ⚠ Dấu `*` chỉ là nhãn: BE `actual_hours nullable|numeric`, `result_text nullable` (`TaskUpdateRequest.php:47-50`).
- **Chế độ B (có báo cáo tiến độ)** (`:262-440`): bảng Nhật ký tiến độ theo lịch (Ngày · Số giờ làm · Tiến độ (%) · Ghi chú), chỉ dòng ≤ hôm nay sửa được (`isRowActive :1741-1757`); tổng giờ + "Tiến độ hiện tại (max)"; Kết quả thực hiện (tổng hợp).
- Checklist: tick Done từng mục (`:446-500`), gửi `checklists[{id,is_done,result_note}]`.
- Nhiệm vụ con: bảng chỉ đọc (tên, người làm, hạn, trạng thái) (`:508-570`).
- Tệp: 2 tab "Tệp giao việc" (chỉ tải) / "Tệp kết quả" (thêm/đổi/xoá/tải) (`:586-800`).
- Bình luận `comment-thread type="task"` (`:815`).
- Cột phải chỉ đọc: Người giao, Người duyệt KQ, Tags, Lặp lại, Yêu cầu báo cáo tiến độ, Liên kết, KPI (`:830-1080`).
- Footer: **Lưu** (khi không phải Xem) + Đóng (`:1094-1102`).
- Payload `handleSave` (`:1879-1906`): `PUT assign/tasks/{id}` với `is_import_result: true, actual_hours, progress_percent (= tiến độ log mới nhất nếu chế độ B), result_text, result_attachments[], progress_logs[], checklists[], status`.
- BE khi `is_import_result`: bỏ qua rule các trường giao việc (`TaskUpdateRequest.php:84-141`), kiểm `progress_logs` không giảm theo ngày (`:231-257`), chuyển sang 6/8 thì `progress_percent` phải = 100 (`:218-229`).
- Khi sang REVIEW: ghi `submitted_at`; sang DONE: `approved_at, approved_by, completed_at`; tính `performance_percent = round(estimated/actual×100)` (actual = tổng giờ log nếu bật báo cáo) (`TaskService.php:521-543`).
- ⚠ **Không có ô nhập Lý do** khi Từ chối kết quả / Từ chối triển khai — `reject_reason` không xuất hiện ở bất kỳ file FE nào trong phạm vi Nhiệm vụ, dù BE có cột và ghi vào note lịch sử (`TaskService.php:555-560`).

---

## 5. Vòng đời trạng thái

### 5.1 Danh sách trạng thái (`BE: Entities/Task/Task.php:96-166`)

| id | Tên | Màu BE (`status_color`) | Nhóm |
|---|---|---|---|
| 1 | Nháp | `#64748B` | nháp |
| 2 | Chờ phê duyệt triển khai | `#0EA5E9` | theo dõi |
| 3 | Chờ bắt đầu | `#64748B` | nháp |
| 4 | Đang thực hiện | `#2563EB` | đang thực hiện |
| 5 | Tạm dừng | `#F59E0B` | cảnh báo |
| 6 | Hoàn thành - Chờ duyệt | `#D97706` | chờ duyệt |
| 7 | Từ chối kết quả | `#DC2626` | từ chối |
| 8 | Hoàn thành | `#16A34A` | hoàn thành |
| 9 | Huỷ | `#6B7280` | đã đóng |
| 10 | Từ chối triển khai | `#DC2626` | từ chối |

Ưu tiên (`Task.php:175-183`): 1 Bình thường `#94A3B8` · 2 Cao `#F97316` · 3 Khẩn cấp `#DC2626`. API trả `priority_name`, `priority_color`.
Tình trạng hạn (`TaskResource.php:110-131`): "Trong hạn" `#16A34A` / "Quá hạn" `#DC2626`, bỏ trống với Nháp/Hoàn thành/Huỷ hoặc không có hạn.

⚠ Màu ở popup (`CreateTaskModal.vue:1667-1678`, `:2932-2951`; `ImportResultModal.vue:1593-1627`) là bảng màu **cũ tự map ở FE**, lệch với màu BE (vd 6 = tím `#7c3aed` thay vì `#D97706`). App nên dùng `status_color` BE.

### 5.2 Chuyển trạng thái hợp lệ (`Task::getAllowedNextStatuses`, `Task.php:471-563`)
Vai trò: **Tạo** = `created_by`; **Thực hiện** = `assignee_id`; **Duyệt triển khai** = có quyền `Duyệt triển khai task` VÀ phòng ban của người thực hiện thuộc `listManageDepartmentIdsWithOwn()`; **Duyệt KQ** = `approver_id`. "Chưa có KQ" = `hasAnyResult()` false (không có result_text, actual_hours, progress log, tệp kết quả — `:302-317`).

| Từ | Sang | Ai |
|---|---|---|
| 1 Nháp | 3 Chờ bắt đầu · 2 Chờ phê duyệt triển khai · 4 Đang thực hiện | Tạo |
| 2 Chờ phê duyệt triển khai | 3 Chờ bắt đầu · 10 Từ chối triển khai | Duyệt triển khai |
| 10 Từ chối triển khai | 2 · 3 · 4 | Tạo |
| 3 Chờ bắt đầu | 4 Đang thực hiện · 10 (nếu chưa có KQ) | Thực hiện |
| 3 Chờ bắt đầu | 5 Tạm dừng | Thực hiện hoặc Tạo |
| 4 Đang thực hiện | 5 Tạm dừng | Thực hiện hoặc Tạo |
| 4 Đang thực hiện | 6 Hoàn thành - Chờ duyệt (nếu có `approver_id`) / **8 Hoàn thành** (nếu không có người duyệt) · 10 (nếu chưa có KQ) | Thực hiện |
| 5 Tạm dừng | 4 · 3 | Thực hiện hoặc Tạo |
| 5 Tạm dừng | 10 (nếu chưa có KQ) | Thực hiện |
| 6 Hoàn thành - Chờ duyệt | 8 Hoàn thành · 7 Từ chối kết quả | Duyệt KQ |
| 7 Từ chối kết quả | 4 · 5 · 8 (chỉ khi không có người duyệt) | Thực hiện |
| 8 Hoàn thành | 7 Từ chối kết quả (rollback) | Tạo |
| 9 Huỷ | — | **Không có đường nào vào trạng thái 9** |

- Khởi tạo (POST): trạng thái lấy thẳng từ payload — FE chỉ cho 1/2/3/4 nhưng BE nhận mọi số nguyên (xem mục 14).
- Kiểm tra ở BE khi PUT: `newStatus ∉ allowed` → 403 "Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này." (`TaskService.php:470-475`); thêm chặn 10 khi đã có KQ (trừ từ 2) → 422 (`:478-487`).
- Khi sang trạng thái khác 1/2 → sinh nhiệm vụ con thật từ `task_children` (`:566-569`).

---

## 6. Quyền và điều kiện thao tác

### 6.1 Quyền hệ thống (`hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1162-1179`, group "Nhiệm vụ", type 4)

| `name` (khoá check) | Hiển thị | Dùng ở |
|---|---|---|
| `Duyệt triển khai task` | Duyệt triển khai Nhiệm vụ | chuyển 2→3/10, cờ `can_approve`, phạm vi xem tầng 1, người nhận thông báo chờ duyệt |
| `Xem danh sách task theo tổng công ty` | … theo tổng công ty | xem tất cả (`TaskService.php:185-187`) |
| `Xem danh sách task theo công ty` | … theo công ty | tầng 3 theo `current_company_role` (`:256-261`) |
| `Xem danh sách task theo phòng ban` | … theo phòng ban | tầng 3 phòng ban + bộ phận quản lý (`:262-269`) |
| `Xem danh sách task theo bộ phận` | … theo bộ phận | tầng 3 bộ phận quản lý (`:270-275`) |

**Không có quyền** tạo / sửa / xoá nhiệm vụ — ai đăng nhập cũng tạo được; sửa/xoá dựa vào vai trò cá nhân.

### 6.2 Phạm vi xem danh sách `GET assign/tasks` (`TaskService::applyPermissionScope`, `TaskService.php:182-248`)
- Luôn ẩn Nháp của người khác (`:28-39`).
- Có quyền tổng công ty → không giới hạn.
- Ngược lại thấy task thoả 1 trong:
  - Tầng 1: mình là tạo / thực hiện / duyệt KQ / theo dõi, hoặc (có quyền Duyệt triển khai và người thực hiện thuộc phòng mình quản lý); cộng task con của các task đó và task cha của chúng.
  - Tầng 2: task thuộc giải pháp mình là thành viên (cấp GP hoặc hạng mục) hoặc dự án mình là thành viên (`Helpers/TaskLinkScopeHelper.php`).
  - Tầng 3: task có ít nhất 1 người giữ vai trò thuộc đơn vị mình quản lý (bảng `task_org_units`), theo quyền cấp cao nhất.
- FE dùng 4 quyền xem để mở/khoá bộ lọc Công ty – Phòng ban – Bộ phận (`index.vue:926-933`).

### 6.3 Cờ thao tác trên từng task (BE trả, `TaskResource.php:102-106`, `DetailTaskResource.php:79-83`)

| Cờ | Điều kiện (`Task.php`) |
|---|---|
| `can_edit` | là người tạo VÀ task **không có task con thật** (`:224-230`) — không xét trạng thái |
| `can_delete` | là người tạo VÀ trạng thái Nháp VÀ không có task con (`:232-238`) |
| `can_import_result` | là người thực hiện VÀ trạng thái ∈ {3 Chờ bắt đầu, 4 Đang thực hiện, 7 Từ chối KQ} (`:240-247`) |
| `can_approve` | `canStartApprove()` (trạng thái 2 + quyền Duyệt triển khai + quản lý phòng người thực hiện, `:253-278`) HOẶC `canResultApprove()` (là `approver_id` + trạng thái 6, `:280-283`) |
| `allowed_next_statuses` | chỉ có ở API chi tiết (mục 5.2) |
| `my_role` | chuỗi "Người thực hiện, Người tạo, Người theo dõi, Người duyệt KQ" (`:621-645`) |

### 6.4 Kiểm tra ở BE theo endpoint
- `DELETE /{task}` và `delete_by_ids`: kiểm `canDelete()` (`TaskController.php:181-183`, `:199-204`).
- `PUT /{task}`: **chỉ** kiểm chuyển trạng thái — không kiểm `canEdit()` cho các trường còn lại (mục 14).
- `GET /{task}`, `GET /{task}/comments`, `POST /{task}/comments`, `GET system-logs/task/{id}`: không kiểm quyền xem.
- Daily report save: chỉ ghi task mà `assignee_id = mình` (`TaskService.php:991-992`).

### 6.5 Ẩn/hiện trên FE form
- Các ô giao việc disable khi `isEdit && !can_edit` (`CreateTaskModal.vue:92`, `:111`, `:207`, …).
- Nút Lưu ở màn Sửa hiện khi `can_edit || can_import_result || can_approve` (`:1433-1446`) → người Duyệt triển khai (trạng thái 2) mở popup Sửa, chỉ đổi được ô Trạng thái rồi Lưu.

---

## 7. Màn danh sách: cột, bộ lọc, sắp xếp, thống kê

### 7.1 Cột (`index.vue:709-924`, mặc định hiện hết; cấu hình cột lưu theo key `tasks`)
STT (sticky, khoá) · **Mã nhiệm vụ** (sticky, khoá, sort, link mở Xem) · Tên nhiệm vụ (sort, 2 dòng) · Tag (tối đa 4 chip + "+n tag") · Giải pháp (mã - tên) · Version GP (badge) · Dự án (mã - tên + dòng "PM: …") · Hạng mục/Module · Trạng thái (badge BE, sort) · Loại nhiệm vụ · Ưu tiên (badge BE, sort) · Tình trạng hạn (badge) · Người làm · Người theo dõi · Người duyệt · Người tạo · Ngày bắt đầu (sort) · Hạn hoàn thành (ngày · giờ + "Ước lượng: n ngày", sort) · Checklist/Nhiệm vụ con ("n checklist · n nhiệm vụ con", "Liên kết: n nhiệm vụ") · Ngày tạo (sort) · Người cập nhật · Ngày cập nhật (sort) · Hành động (khoá).

### 7.2 Bộ lọc (`index.vue:537-627`, panel `V2BaseSmartFilterPanel table="tasks" floating`)

| Ô | Key gửi BE | Giá trị | BE xử lý (`TaskService::index`) |
|---|---|---|---|
| Tìm nhanh | `keyword` | text — "Tìm theo mã nhiệm vụ, tên nhiệm vụ, tên/mã khách hàng của dự án" | like `title`, `code`, `prospective_projects.customer_name/customer_code` (`:55-69`) |
| Công ty – Phòng ban – Bộ phận | `company_id`, `department_id`, `part_id` | `V2BaseCompanyDepartmentFilter` (tắt ô NV) | task có ≥1 người giữ vai trò thuộc đơn vị (`task_org_units`, `:44-53`, `:282-287`) |
| Loại nhiệm vụ | `task_type` | 1/2 | `=` |
| Giải pháp | `solution_id` | `solutions/getAll?per_page=10000` | `=`; đổi GP → reset Version/Dự án/Hạng mục (`:966-972`) |
| Dự án | `prospective_project_id` | chỉ có khi đã chọn GP (`projectOptions :507-516`) | `project_id =` |
| Hạng mục/Module | `solution_module_id` | theo GP | `=` |
| Version giải pháp | `solution_version_id` | `GET assign/solutions/{id}/versions` → "V{code}" | `=` |
| Trạng thái | `status` | 10 trạng thái (hằng FE `:465-476`) | `=` |
| Mức độ ưu tiên | `priority` | 1/2/3 | `=` |
| Người thực hiện / Người duyệt KQ / Người tạo | `assignee_id` / `approver_id` / `created_by` | `$store.state.allEmployeesOptions` | `=` |
| Ngày cập nhật | `from_date`, `to_date` | date-range 1 ô | `whereDate(updated_at)` |
| Hạn hoàn thành | `deadline_from`, `deadline_to` | date-range 1 ô | `whereDate(due_date)` |
| Tag | `tags[]` | `MultiSearchPicker`, nguồn `GET assign/tasks/tags/getAll` | `whereHas tags.id in` |
| (ẩn) Theo dõi | `watching_id` | từ nút lọc nhanh | `whereHas watchers` |
| (khác) | `meeting_id`, `meeting_report_id`, `module_version_id` | từ tab nhúng | `=` |

Bộ lọc lưu localStorage key `assign_tasks`, hết hạn 10 phút (`index.vue:442-445`).

### 7.3 Lọc nhanh theo vai trò (`index.vue:452-462`, `:1123-1138`) — loại trừ nhau
`Nhiệm vụ tôi làm` (assignee_id = tôi) · `Nhiệm vụ tôi giao` (created_by) · `Nhiệm vụ tôi theo dõi` (watching_id) · `Nhiệm vụ tôi duyệt kết quả` (approver_id).

### 7.4 Sắp xếp, phân trang, thống kê
- Sort: `sort_field` ∈ `taskCode/code, taskName/title, status, priority, started_at/start_date, deadline/due_date, created_at, updated_at`, `sort_dir asc|desc`; mặc định `created_at desc`, chốt phụ `id desc` (`TaskService.php:146-173`).
- Phân trang `page`, `per_page` (mặc định 10 — `index.vue:406-413`), BE `TaskResource::apiPaginate`.
- Thống kê đầu bảng: `Tổng` = `meta.total`, `Quá hạn` = `overdue_total` (BE đếm trên cùng truy vấn lọc, scope `overdue` — `TaskController.php:56`, `Task.php:608-616`).
- Xuất Excel: popup chọn cột (27 cột `index.vue:641-671`) → `GET assign/tasks/export?…&fields[]=` → `DynamicExport`, file `danh_sach_task.xlsx` (`TaskController.php:240-271`).

### 7.5 Công việc của tôi (`MyJobService`)
- `task-list`: task mình là thực hiện/tạo/duyệt/theo dõi, ẩn Nháp người khác; lọc keyword, status, solution, project, module, assignee, approver, created_by, priority, watching_id, from/to_date; sort `created_at|updated_at|due_date` (`Services/MyJobService.php:590-677`).
- `today-tasks`: mình thực hiện, trạng thái đang chạy + Hoàn thành, `start_date = hôm nay` (`:684-704`).
- `task-upcoming-schedule`: mình thực hiện, trạng thái đang chạy, `due_date` trong [now, now + `general_regulations.task_due_days`] (`:497-583`).
- `task-status-statistics`: `{not_started, in_progress, completed}` của mình (`:712-736`).
- `task-trend-statistics`: 14 ngày `{dates[], created[], completed[]}` (`:790-845`).

---

## 8. Báo cáo tiến độ hằng ngày (daily report)

- Màn `FE: pages/assign/tasks/daily-report.vue` — tiêu đề "Nhập kết quả báo cáo tiến độ" (`:224`).
- Thẻ thống kê: Tổng nhiệm vụ · Chờ báo cáo · Đã hoàn thành (`:30-58`). Mỗi task là 1 khối thu gọn: mã, tên, badge trạng thái, dự án, hạn, giờ hạn, nhãn chu kỳ (`:75-104`).
- Bảng: NGÀY BÁO CÁO · SỐ GIỜ LÀM · TIẾN ĐỘ (%) · GHI CHÚ; **chỉ dòng hôm nay sửa được** (`is_editable`), dòng tương lai hiện "Chưa đến ngày báo cáo" (`:108-170`).
- Nút **Lưu** (đầu + cuối trang), **Đóng** → `/assign/tasks` (`:17`, `:194-198`).
- FE validate: tổng % các ngày trước + hôm nay ≤ 100 (`:284-306`) — tức hiểu % là **phần tăng thêm**.
- API:
  - `GET assign/tasks/daily-report` → mảng task: `{id, code, title, status, status_name, status_color, priority, due_date, due_time, start_date, progress_pct, total_progress_pct, project_name, assignee_name, report_rule{cycle_type, send_time}, progress_rows[{report_date, hours, progress_pct, note, is_today, is_past, is_future, is_editable}], is_reported_today}` (`TaskService.php:902-943`, `:1082-1140`). Điều kiện: mình là người thực hiện, trạng thái **4 Đang thực hiện**, bật báo cáo tiến độ, hôm nay là ngày báo cáo theo chu kỳ.
  - `POST assign/tasks/daily-report/save` body `{tasks:[{task_id, progress_logs:[{report_date, hours, progress_pct, note}]}]}` → `{success, errors[{task_id, error}]}` (`TaskService.php:981-1052`). Chỉ nhận dòng `report_date = hôm nay`; chặn tổng % > 100.
  - `GET assign/tasks/daily-report/count` → `{count}` số task chưa báo cáo hôm nay (`:948-976`).

---

## 9. Bình luận

- FE: `components/comments/CommentThread.vue` với `type="task"` → base `assign/tasks` (`:73`, `:97`); nhúng trong popup Sửa/Xem ở chế độ nâng cao và trong ImportResultModal.
- BE `Http/Controllers/Api/V1/TaskCommentController.php` (gói `actuallymab/laravel-comment`, bảng `comments`):
  - `GET /{task}/comments` → cây gốc + con 3 cấp, kèm tệp + reaction (`:22-41`).
  - `POST /{task}/comments` multipart: `comment required|max:5000`, `rate 1-5`, `parent_id exists:comments`, `files[] ≤ 50MB` (`:43-99`). Trả lời lồng tối đa 3 cấp. Mention dạng `@[Họ tên]` (khớp đúng `employee_infos.fullname`).
  - `PUT /{task}/comments/{id}`, `DELETE …`: chỉ tác giả (`:101-147`).
  - `POST …/react {emoji}`: bấm lại cùng emoji là gỡ (`:149-195`).
  - `PATCH …/approve`: duyệt bình luận, không kiểm ai được duyệt (`:197-209`).
- Thông báo: bình luận gốc → người tạo/thực hiện/duyệt/theo dõi; trả lời → tác giả bình luận cha; mention → người được nhắc; react → tác giả (`:235-390`). URL `/assign/tasks?open_task={id}&comment_id={cid}`, type `task_comment`, `task_comment_reply`, `task_comment_mention`, `task_comment_react`.

---

## 10. Lịch sử thay đổi

- Bảng `task_history`, ghi bởi `Services/TaskHistoryService.php`: action `create` · `update` (subset-diff theo nhãn trường, `is_subset=1`) · `change_status` (note = `reject_reason` nếu sang 7/10) (`:32-38`).
- Snapshot theo nhãn (`:51-91`): Loại nhiệm vụ, Tên công việc, Chế độ, Giải pháp, Dự án/Nhóm, Hạng mục/Module, Meeting, Nhiệm vụ cha, Người thực hiện, Mức độ ưu tiên, Ngày bắt đầu, Hạn hoàn thành, Giờ hạn, Mô tả, Số giờ được giao, Checklist, Nhiệm vụ con, Tệp đính kèm, Người duyệt kết quả, Người theo dõi, Thẻ, Lặp lại, Yêu cầu báo cáo tiến độ, Liên kết nhiệm vụ, Số giờ làm thực tế, Tiến độ (%), Kết quả thực hiện, Nhật ký tiến độ, Tệp kết quả.
- Đọc: `GET assign/system-logs/task/{id}` + `…/filter-options` (`Routes/api.php:606-608`, `SystemLogService::taskLogs :1214-1225`). `GET assign/tasks/{id}` cũng trả `history` đã format (`DetailTaskResource.php:126-128`, `:135-216`).

---

## 11. Thông báo / nhắc hạn

### 11.1 Đổi trạng thái (`TaskService::handleStatusNotification`, `TaskService.php:1212-1295`)
Nội dung chuẩn `[TASK] {Nhóm}: <b>{Tên}</b>. {Ghi chú}` (`buildNotificationContent`, `:1322-1325`), URL `/assign/tasks?open_task={id}`, type `task_status`, loại trừ người thao tác (`:1190-1205`).

| Sang | Điều kiện | Người nhận | Nội dung |
|---|---|---|---|
| 3 Chờ bắt đầu | từ 2 | người thực hiện | Đã duyệt: … Đã duyệt triển khai, chờ bắt đầu. |
| 3 Chờ bắt đầu | khác (vd tạo mới) và tạo ≠ thực hiện | người thực hiện | Tạo mới: … Hạn: HH:mm dd/mm/yyyy. |
| 2 Chờ phê duyệt triển khai | | người có quyền Duyệt triển khai của phòng người thực hiện | Chờ duyệt: … |
| 2 | từ null/Nháp, tạo ≠ thực hiện | người thực hiện | Tạo mới: … Chờ phê duyệt triển khai. Hạn… |
| 10 Từ chối triển khai | từ 2 | người tạo | Từ chối: … {người} không duyệt triển khai. |
| 10 | từ 3 | người tạo + người duyệt triển khai | Từ chối: … {người} từ chối triển khai. |
| 6 Chờ duyệt | | người duyệt KQ | Chờ duyệt: … Chờ duyệt kết quả. |
| 8 Hoàn thành | từ 6 | người thực hiện | Đã duyệt: … {người} đã duyệt kết quả. |
| 7 Từ chối KQ | từ 6 | người thực hiện | Yêu cầu làm lại: … {người} không duyệt kết quả. |

Không có thông báo cho: tạo thẳng ở 4 Đang thực hiện, 5 Tạm dừng, rollback 8→7 (không từ 6), task con sinh tự động.

### 11.2 Nhắc báo cáo tiến độ
- Command `assign:notify-task-report` (`hrm-api/app/Console/Commands/NotifyTaskReport.php`), lịch `cron('30 8,11,14,17 * * *')` giờ VN (`hrm-api/app/Console/Kernel.php:52-55`).
- Đếm task trạng thái 4 bật báo cáo, hôm nay đến kỳ, chưa có log `progress_pct>0` hôm nay → gửi mỗi người 1 thông báo "Bạn có **n** task cần báo cáo tiến độ hôm nay", URL `/assign/tasks/daily-report`, type `task_progress_report_reminder` (`:18-76`). Không dùng `send_time` của từng task.

### 11.3 Nhắc hạn
- Không có job nhắc sắp hết hạn / quá hạn riêng cho task. "Sắp hết hạn" chỉ là API kéo (my-job upcoming, số ngày `general_regulations.task_due_days`).
- **Không có job sinh nhiệm vụ lặp lại**: không file nào đọc `TaskRecurringRule` ngoài resource/service/history (đã grep `Modules`, `app`); cột `next_run_at`, `generated_count`, `recurring_parent_id` không được ghi.

### 11.4 Đăng ký thiết bị
- `POST /assign/fcm-tokens`, `DELETE /assign/fcm-tokens` (`Routes/api.php:1070-1073`) — đã có sẵn cho push mobile.

---

## 12. Quan hệ với đối tượng khác

| Quan hệ | Cột / bảng | Căn cứ |
|---|---|---|
| Dự án tiền khả thi | `tasks.project_id` → `prospective_projects` (`prospectiveProject()`, `project()`) | `Task.php:376-379`, `:565-568` |
| Giải pháp + version | `solution_id`, `solution_version_id/code` | `Task.php:361-364`, `TaskService.php:423-432` |
| Hạng mục giải pháp + version | `solution_module_id`, `module_version_id/code` (`modules()`) | `Task.php:371-374` |
| Cuộc họp / dòng biên bản | `meeting_id`, `meeting_report_id` (#11456) | `Task.php:573-584` |
| Task cha – con | `parent_id` (`parent()`, `subtasks()`); bảng nháp `task_children` (`children()`, `task_id_ref` trỏ task thật) | `Task.php:398-411`, `TaskService.php:805-840` |
| Nhiệm vụ chung | `batch_id` UUID nhóm N task cùng lần tạo | `TaskService.php:357-368` |
| Liên kết task ↔ task | `task_links (task_id, linked_task_id, link_type 1..5)` | `Entities/Task/TaskLink.php` |
| Người theo dõi | `task_watchers` | `Task.php:387-391` |
| Tags | `task_tags` ↔ `tags` | `Task.php:355-359` |
| Checklist | `task_checklists (content, is_done, done_at, result_note)` | `TaskChecklist.php` |
| Tệp giao việc | `files (table='tasks')` | `Task.php:413-418` |
| Tệp kết quả | `task_result_attachments` | `TaskResultAttachment.php` |
| Nhật ký tiến độ | `task_result_progress_logs (report_date, hours, progress_pct, note)` | `TaskResultProgressLog.php` |
| Quy tắc lặp / báo cáo | `task_recurring_rules`, `task_progress_report_rules` | entity cùng tên |
| Phạm vi tổ chức | `task_org_units` (snapshot org của các vai trò) | `TaskService.php:308-352` |
| Vấn đề (Issue) | `issues.task_id` → task (1 chiều, Task không khai quan hệ ngược) | `Entities/Issue.php:27`, `:402-405` |
| Bàn giao | `handover_items` itemable trỏ task (màn bàn giao chỉ mở Xem task) | `HandoverService.php`, FE `handover/*` |
| Tiến độ giải pháp/hạng mục | `ProgressCalculator::recalculate*` mỗi lần lưu/xoá | `TaskService.php:457`, `:571-577`, `:849-854` |
| Báo cáo | `assign/report/task-manager-by-employees`, hiệu suất NV, workload thành viên | `Routes/api.php:982-985`, `SolutionMemberWorkloadService.php` |

---

## 13. API endpoint cho app

Tiền tố `api/v1`, xác thực JWT. Response danh sách dạng `{data:[…], meta:{current_page, per_page, total, last_page, from, to}, …}` (`apiGetList`); response đơn `{data: …}` (`responseJson`).

### 13.1 Nhiệm vụ (`Routes/api.php:1075-1096`)

| Method | Path | Tham số chính | Trả về |
|---|---|---|---|
| GET | `assign/tasks` | mọi key bộ lọc ở 7.2 + `page, per_page, sort_field, sort_dir` | list `TaskResource` + `overdue_total` |
| GET | `assign/tasks/{id}` | — | `DetailTaskResource`: trường task + `allowed_next_statuses[{id,name,color}]`, `can_*`, `tags, watchers[{id,…,fullname}], checklists, children, subtasks (TaskResource), has_children_tasks, attachments, recurring, progress_report, assignee, approver, project, progress_logs, result_attachments, linked_tasks, approved_by_user, history` |
| POST | `assign/tasks` | payload mục 3 (JSON) | task vừa tạo; nhiệm vụ chung → mảng task |
| PUT | `assign/tasks/{id}` | sửa: payload mục 3; nhập KQ/duyệt/đổi trạng thái: `is_import_result:true` + `status, actual_hours, progress_percent, result_text, progress_logs[], result_attachments[], checklists[]`; có `reject_reason` (FE web chưa gửi) | `DetailTaskResource`; 403 chuyển trạng thái sai; 422 |
| DELETE | `assign/tasks/{id}` | — | 400 "Dữ liệu đã thay đổi…" nếu không `canDelete` |
| POST | `assign/tasks/delete_by_ids` | `ids[]` | bỏ qua im lặng task không xoá được |
| GET | `assign/tasks/export` | bộ lọc + `fields[]` | file xlsx |
| GET | `assign/tasks/getAll` | `keyword, project_id` | `[{id, code, name}]` (không phân trang) |
| GET | `assign/tasks/employees` | — | NV công ty hiện tại `{id, name, fullname, code, department_id, department_code, department_name, email, personal_telephone}` |
| GET | `assign/tasks/tags/getAll` | `q` | `[{id, name, slug}]` |
| GET | `assign/tasks/daily-report` | — | xem mục 8 |
| POST | `assign/tasks/daily-report/save` | `tasks[]` | `{success, errors[]}` |
| GET | `assign/tasks/daily-report/count` | — | `{count}` |
| GET/POST/PUT/DELETE | `assign/tasks/{id}/comments[/{cid}]` | xem mục 9 | |
| POST | `assign/tasks/{id}/comments/{cid}/react` | `emoji` | reactions |
| PATCH | `assign/tasks/{id}/comments/{cid}/approve` | — | |

### 13.2 Phụ trợ
| Method | Path | Ghi chú |
|---|---|---|
| GET | `assign/solutions/getAll?per_page=10000&mine=1[&id=|&include_id=]` | GP + `modules[]`, `staff`, `pm_id`, `has_modules`, `status`, `prospective_project_*` |
| GET | `assign/solutions/{id}/versions` | version GP |
| GET | `assign/prospective-projects/getAll?per_page=10000&mine=1` | dự án |
| GET | `assign/meeting/task-options?limit=200[&include_id=]` | cuộc họp user là thành viên |
| GET | `assign/attachment-types/getAll` | loại tài liệu |
| GET | `assign/system-logs/task/{id}` (+`/filter-options`) | lịch sử |
| GET | `assign/my-job/task-list` (+`/export`), `today-tasks`, `task-upcoming-schedule`, `task-status-statistics`, `task-trend-statistics` | `Routes/api.php:1396-1409` |
| GET | `assign/solutions/{id}/manager/tasks` (+`/export`), `tasks-upcoming`, `categories-late`, `people-late`, `task-status-stats`, `pending-approvals` | `Routes/api.php:446-474` |
| GET | `assign/solution-modules/{id}/manager/tasks` (+`/export`), `tasks-upcoming`, `people-late`, `task-status-stats`, `pending-approvals` | `Routes/api.php:875-882` |
| POST/DELETE | `assign/fcm-tokens` | đăng ký push |

### 13.3 Shape `TaskResource` (dòng danh sách, `TaskResource.php:25-107`)
`id, code, task_type, task_type_text, batch_id, title, description, project_id, meeting_id, meeting_code, meeting_name, meeting_report_id, parent_id, priority, priorityLevel(luôn null), status, status_text, status_color, priority_name, priority_color, solution_id, solution_name, solution_code, prospective_project_code, prospective_project_name, solution_employee_name, module_name, solution_version_code, module_version_code, assignee_id, assignee_name, approver_id, approver_name, projectPhases, created_by_name, updated_by_name, start_date (d/m/Y), due_date (d/m/Y), estimated_time, due_time (HH:mm), created_at, updated_at (d/m/Y H:i), tags[{id,name}], watcher_names, checklists_number, children_number, linked_number, in_progress, deadline_state_text, deadline_state_color, can_edit, can_delete, can_import_result, can_approve, my_role`.
Lưu ý: list trả ngày `d/m/Y`, chi tiết trả `start_date/due_date` thô `Y-m-d` và `due_time` `H:i:s` (`DetailTaskResource.php:42-44`).

---

## 14. Điểm lạ / bug / fail-open

> Chỉ ghi nhận, KHÔNG sửa. Mức: 🔴 bảo mật / mất dữ liệu · 🟠 sai nghiệp vụ · 🟡 lệch hiển thị / kỹ thuật.

**Bảo mật / fail-open**
1. 🔴 `PUT assign/tasks/{id}` không kiểm `canEdit()` cho các trường giao việc — service chỉ kiểm chuyển trạng thái (`TaskService.php:462-487`), controller không gate (`TaskController.php:127-148`), route không middleware (`api.php:1085`). Bất kỳ ai đăng nhập gửi PUT giữ nguyên `status` là sửa được tên, người thực hiện, hạn, người duyệt… của task người khác. Ẩn ô ở FE (`CreateTaskModal.vue:92…`) không phải chốt chặn.
2. 🔴 `GET assign/tasks/{id}` không kiểm phạm vi xem (`TaskController.php:150-175`) — đọc được mọi task, kể cả Nháp của người khác, kèm lịch sử, tệp, kết quả. Tương tự `GET/POST …/comments` (`TaskCommentController.php:22-99`) và `GET assign/system-logs/task/{id}` (`SystemLogController.php:30-37`).
3. 🔴 `POST assign/tasks` nhận `status` bất kỳ số nguyên (`TaskStoreRequest.php:53`) — tạo thẳng task ở 8 Hoàn thành / 6 Chờ duyệt, bỏ qua duyệt triển khai.
4. 🟠 `PATCH …/comments/{id}/approve` không kiểm ai được duyệt bình luận (`TaskCommentController.php:197-209`).
5. 🟠 `GET assign/tasks/getAll` không áp phạm vi xem — trả mã + tên mọi task không phải Nháp trên toàn hệ thống (`TaskService.php:863-897`); FE gọi `per_page=10000` mỗi lần dựng popup (`CreateTaskModal.vue:1932-1935`, `:2523-2530`).
6. 🟡 `GET assign/solutions/{id}/manager/tasks`: `getTaskListForSolution` chỉ lọc theo `solution_id`, không thấy kiểm thành viên trong service/controller (`SolutionService.php:1739-1747`, `SolutionController.php:323-339`) — cần xác minh thêm ở middleware nhóm route.

**Sai nghiệp vụ**
7. 🟠 Sửa task không xoá được giá trị về rỗng: mọi trường dùng `$request->x ?? $task->x` (`TaskService.php:496-519`) → bỏ Người duyệt, bỏ hạn, bỏ Giải pháp/Dự án/Meeting, xoá mô tả… đều bị giữ giá trị cũ im lặng.
8. 🟠 Không có ô nhập **Lý do** từ chối (7, 10) ở FE (grep `reject_reason` trong `pages/assign/tasks`, `components/assign/task`, `pages/assign/my-job` rỗng) dù BE lưu và đưa vào lịch sử.
9. 🟠 Trạng thái **9 Huỷ** không có đường chuyển nào (`Task.php:487-556`) → không huỷ được nhiệm vụ; chỉ xoá được khi còn Nháp.
10. 🟠 Tính năng **Lặp lại** lưu cấu hình nhưng không có job sinh nhiệm vụ (mục 11.3). Ngoài ra update chỉ nhận `repeat_type in:1,2,3` (`TaskUpdateRequest.php:123`) trong khi store/FE cho 4 "Tùy chỉnh" (`TaskStoreRequest.php:95`, `CreateTaskModal.vue:1635`) → task đã chọn Tùy chỉnh sửa lại là 422.
11. 🟠 Nghĩa của `progress_pct` mâu thuẫn: Nhập kết quả coi là **luỹ kế** (BE chặn giảm dần `TaskUpdateRequest.php:231-257`, FE hiện "Tiến độ hiện tại (max)" `ImportResultModal.vue:375`, lấy log mới nhất làm `progress_percent`) còn Daily report coi là **phần tăng** (tổng các ngày ≤ 100 — `TaskService.php:1004-1015`, `daily-report.vue:292-299`). Báo theo daily report thì không bao giờ đạt "100%" để chuyển hoàn thành (validate `progress_percent == 100`).
12. 🟠 Daily report: BE trả `errors[]` trong response 200 nhưng FE bỏ qua, luôn toast "Lưu tiến độ thành công" (`daily-report.vue:331-336`, `TaskService.php:1048-1051`).
13. 🟠 `task-upcoming-schedule` so `due_date` (DATE) `>= now()` (datetime) → task hạn **hôm nay** bị loại; comment ghi "hoặc quá hạn" nhưng query không lấy quá hạn (`MyJobService.php:517-522`).
14. 🟠 `today-tasks` lọc `start_date = hôm nay` (`MyJobService.php:698`) — `start_date` không sửa được trên form (ô đã comment), task tạo hôm qua hạn hôm nay không vào "hôm nay".
15. 🟠 `can_edit` không xét trạng thái (`Task.php:224-230`) → người tạo sửa được task đã Hoàn thành; nhưng lại chặn khi task có task con, trái với comment FE "Nhiệm vụ cha có nhiệm vụ con vẫn cho phép chỉnh sửa" (`CreateTaskModal.vue:2160`).
16. 🟠 Task con sinh tự động (`createChildrenAsTasks`) bỏ qua validate tạo mới: `estimated_hours` null (bắt buộc ở form), không người theo dõi, không gửi thông báo cho người được giao (`TaskService.php:805-840`). Cùng lúc FE gửi `children[].watchers` nhưng BE không dùng (`CreateTaskModal.vue:2866`).
17. 🟠 Không gửi thông báo khi tạo thẳng trạng thái 4 Đang thực hiện hoặc chuyển 5 Tạm dừng (`TaskService.php:1218-1287`).
18. 🟠 Nhắc báo cáo tiến độ chạy cố định 4 mốc, bỏ qua `send_time` user đặt trên form (`Kernel.php:52-55`, `NotifyTaskReport.php`).
19. 🟠 Nhãn bắt buộc lệch BE: Hạn hoàn thành/Giờ hạn có `*` nhưng BE `nullable`; Ưu tiên không `*` nhưng BE `required`; ImportResultModal đánh `*` Số giờ thực tế/Kết quả nhưng BE `nullable`. FE không validate client → bấm Lưu mới biết lỗi.
20. 🟠 Màn Sửa ở danh sách luôn mở `CreateTaskModal` kể cả trạng thái 4–9 (`index.vue:1275-1277`), trong khi Xem/Nhập KQ/Duyệt mở `ImportResultModal` — 2 khuôn khác nhau cho cùng bản ghi.
21. 🟠 Checklist bị xoá khỏi form không bị xoá ở BE (chỉ update/create, `TaskService.php:629-661`); tương tự `task_children`.

**Hiển thị / kỹ thuật**
22. 🟡 Quan hệ `priorityLevel()` luôn null (`Task.php:169-173`) nhưng `TodayTasks.vue:56-62` và `my-job/TaskUpcomingModal.vue:134-140` vẫn đọc `t.priorityLevel` → cột Ưu tiên luôn "—".
23. 🟡 Số "Quá hạn" ở my-job tính trên trang hiện tại và đếm cả task Hoàn thành (`my-job/components/TasksTab.vue:477`: `status !== 4 && !in_progress`).
24. 🟡 Màu trạng thái/ưu tiên ở 2 popup tự map ở FE, lệch BE (`CreateTaskModal.vue:1519-1523`, `:1667-1678`, `:2932-2951`).
25. 🟡 `seedDates` dùng `toISOString()` (UTC) → mở form trước 07:00 giờ VN ra ngày hôm qua (`CreateTaskModal.vue:2372`).
26. 🟡 Mã task sinh bằng `MAX+1` không khoá (`Task.php:342-351`) → 2 request đồng thời có thể trùng mã; luôn `NB`; comment mô tả nhầm "MET".
27. 🟡 Thông báo bình luận không theo template `[TASK] …` (`TaskCommentController.php:280`, `:302`, `:364`, `:386`) và mention so khớp `fullname` chính xác (trùng tên → gửi nhầm người đầu tiên, `:337`).
28. 🟡 `getEmployeesByCompany` ghép `name = "Mã phòng - Tên"` (`TaskController.php:98`), không theo chuẩn `Tên - Mã phòng - Mã NV`.
29. 🟡 `TaskController::updateStatus` + `TaskUpdateStatusRequest` là code chết (không có route).
30. 🟡 Popup tạo/sửa dựng bằng `b-modal` + nhiều `<input type="checkbox">`, `<label>`, `<button class="btn">` thô, `alert()` (`CreateTaskModal.vue:2434`), comment demo `seedDemoComments` (`:2968-2986`) và `DEMO_TASKS` (`:1514-1518`) còn sót.
31. 🟡 Export danh sách `->get()` toàn bộ + `DynamicExport` (`TaskController.php:240-265`) — chưa chia trang như quy ước export > 2s.
32. 🟡 Kích thước tệp: kiểm 50MB nhưng toast ghi ">20MB" (`CreateTaskModal.vue:2703-2706`).

---

## 15. Gợi ý cho thiết kế app

- Dùng `status_text/status_color`, `priority_name/priority_color`, `deadline_state_*` của BE; dùng `allowed_next_statuses` + 4 cờ `can_*` để quyết định nút — không tự suy luật trạng thái ở app.
- Màn chi tiết lấy `GET assign/tasks/{id}`; danh sách "của tôi" nên dùng `GET assign/tasks` + 4 lọc nhanh vai trò (có `overdue_total`, đã có phân quyền 3 tầng) thay vì `my-job/task-list` (không có overdue, sort hẹp).
- Luồng mobile ưu tiên: Xem · Đổi trạng thái (bắt đầu / tạm dừng / gửi duyệt / duyệt / từ chối) · Nhập kết quả · Báo cáo tiến độ hôm nay · Bình luận. Tạo nhanh chỉ cần nhóm trường chế độ Đơn giản (mục 3.1).
- Deep link thông báo đang là URL web `/assign/tasks?open_task={id}[&comment_id=]` và `/assign/tasks/daily-report`; app cần map 2 dạng này. Push đã có `assign/fcm-tokens`.
- Trước khi làm app nên chốt với user các điểm 1, 2, 7, 8, 9, 11 ở mục 14 vì ảnh hưởng trực tiếp tới luồng trên app (sửa trái phép, lý do từ chối, huỷ, ý nghĩa % tiến độ).
