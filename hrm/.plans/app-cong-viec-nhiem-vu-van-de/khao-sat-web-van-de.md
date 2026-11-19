# Khảo sát chức năng Vấn đề (Issue) — bản web HRM, nhánh `gop_db`

> Ngày khảo sát: 29/10/2026. Chỉ đọc code, không chạy app. Module `Modules/Assign` của hrm-api không lệch
> `origin/gop_db` (`git diff --stat origin/gop_db -- Modules/Assign` rỗng); các file FE đọc đều không nằm
> trong danh sách sửa local.
> Viết tắt: **FE** = `HRM/hrm-client`, **BE** = `HRM/hrm-api/Modules/Assign`.
> Trên giao diện gọi là "Vấn đề", còn mã, API và tên quyền vẫn dùng chữ `issue`.

## Mục lục

1. [Màn, popup và hành động](#1-màn-popup-và-hành-động)
2. [Trường của form Tạo/Sửa](#2-trường-của-form-tạosửa)
3. [Vòng đời trạng thái](#3-vòng-đời-trạng-thái)
4. [Danh sách: cột, lọc, sắp xếp, phân trang, thống kê](#4-danh-sách-cột-lọc-sắp-xếp-phân-trang-thống-kê)
5. [Quan hệ với đối tượng khác](#5-quan-hệ-với-đối-tượng-khác)
6. [Phân quyền xem và thông báo](#6-phân-quyền-xem-và-thông-báo)
7. [API app dùng được](#7-api-app-dùng-được)
8. [Điểm lạ / bug / fail-open](#8-điểm-lạ--bug--fail-open)
9. [Gợi ý cho bản app](#9-gợi-ý-cho-bản-app)

---

## 1. Màn, popup và hành động

### 1.1 Lối vào

| Lối vào | File | Ghi chú |
|---|---|---|
| Menu "Vấn đề" → `/assign/issues` | `components/menu-sidebar.js:49`, `components/subsystem-menu/presale.js:78` | Màn chính, layout `default-sidebar` (`pages/assign/issues/index.vue:368`) |
| Link thông báo `/assign/issues?open_issue={id}&comment_id={cid}` | `pages/assign/issues/index.vue:1240-1258` | Mở popup Xem, cuộn tới bình luận rồi xoá query |
| Công việc của tôi → tab "Issue" | `pages/assign/my-job/index.vue:72,138,292-296` | `IssuesTab.vue` nhận mảng `issues` từ cha |
| Giải pháp → Quản lý → tab Vấn đề | `pages/assign/solutions/components/manager/IssueTab.vue` | Lọc cố định theo `solution_id` |
| Giải pháp → Quản lý → thẻ "Vấn đề sắp đến hạn" | `pages/assign/solutions/_id/manager.vue:146,846`, `.../manager/IssueUpcomingModal.vue` | Popup chỉ có hành động Xem |
| Hạng mục → tab Vấn đề | `pages/assign/solution-modules/_id/components/IssueTab.vue` | Lọc cố định theo `module_id` |
| My-todo (lịch việc) | `pages/assign/my-todo/index.vue:111,346-349,540-552` | Tạo nhanh có điền sẵn `due_date`; xem / sửa / xử lý / lịch sử |
| Bàn giao (handover) | `pages/assign/handover/add.vue:35,183-225`, `_id/index.vue`, `_id/receive.vue` | Vấn đề là 1 loại mục bàn giao (`itemable_type = Issue`) |
| Báo cáo hiệu suất NV | `pages/assign/report/employee-work-performance/components/WorkDrillModal.vue`, `WorkTable.vue` | Chỉ đọc/drill |
| Tab Tệp của giải pháp / hạng mục | `solutions/components/manager/FilesTab.vue`, `solution-modules/_id/components/FilesTab.vue` | Mở popup Vấn đề từ file đính kèm |

### 1.2 Màn danh sách `/assign/issues` (`pages/assign/issues/index.vue`)

| Hành động | Điều kiện hiện | API | Căn cứ |
|---|---|---|---|
| **Tạo Vấn đề** | Luôn hiện, không gate quyền | `POST assign/issues` | `index.vue:51-56`, `1210-1212` |
| **Xuất Excel** (popup chọn cột) | Luôn hiện | `GET assign/issues/export?fields=...` | `index.vue:59-71`, `593-620` |
| **Cấu hình cột** | Luôn hiện | `human/column-customizations` (mixin) | `index.vue:72-80` |
| Bấm **Mã Vấn đề** → popup Xem | Mọi dòng | `GET assign/issues/{id}` | `index.vue:124-128`, `1213-1215` |
| **Sửa** | `item.can_edit === true` | `PUT assign/issues/{id}` | `index.vue:1171-1174` |
| **Xóa** (popup xác nhận) | `item.can_delete === true` | `DELETE assign/issues/{id}` | `index.vue:1175-1181`, `1226-1238` |
| **Xử lý** (menu ⋮) | `item.can_handle === true` | `PUT assign/issues/{id}` | `index.vue:1182`, `1222-1224` |
| **Lịch sử** (menu ⋮) | Luôn hiện, không gate quyền | `GET assign/system-logs/issue/{id}` | `index.vue:1183-1185`, `IssueHistoryModal.vue:13,33-36` |
| Lọc nhanh 4 nút vai trò | Luôn hiện | thêm tham số vào `GET assign/issues` | `index.vue:415-420`, `1110-1126` |

Màn này **không có** nhập Excel, đổi trạng thái hàng loạt hay xoá hàng loạt.

### 1.3 Popup `CreateIssueModal.vue` (Tạo / Sửa / Xem / Xử lý)

`open(issue, readOnly, isHandling, initialData, commentId, options)`: `CreateIssueModal.vue:1045-1069`.

| Chế độ | Cách gọi | Ô nào sửa được |
|---|---|---|
| Thêm mới | `open()` hoặc `open(null,false,false,{solution_id,...,lockSolution...})` | Mọi ô. Trạng thái chỉ có `new` hoặc `assigned` (`:968-975`) |
| Sửa | `open(item)` | Mọi ô. Trạng thái = `allowed_next_statuses` do BE trả |
| Xem | `open(item, true)` | Không ô nào sửa được. Footer có Sửa / Xử lý / Xóa theo `can_edit/can_handle/can_delete` (`:765-778`, `isViewMode` `:940-942`) |
| Xử lý | `open(item, true, true)` | Chỉ **Trạng thái** (`:527-538`), **Lý do từ chối** (`:556-564`) và **Tệp đính kèm** (thêm/đổi/xoá dòng: `:378-385`, `isReadOnly && !isHandling`) |

Ngay trong popup có:
- **Bình luận**: `comment-thread type="issue"`, hiện khi `isEdit && form.id` nên ở chế độ Xem cũng có (`:734-740`). Hỗ trợ trả lời tối đa 3 cấp, đính kèm file, sửa/xoá bình luận của chính mình, thả emoji, nhắc tên `@[Họ tên]` (BE `IssueCommentController.php`).
- **Lịch sử**: `SystemInfoSection entity-type="issue"`, thu gọn mặc định (`:746-748`).
- Nút **Làm mới** xoá trắng form (`:27-29`, `resetForm` `:1093-1101`).
- Từ chế độ Xem chuyển sang Sửa / Xử lý tại chỗ: `switchToEdit` / `switchToHandle` (`:1265-1272`). Xoá dùng `$confirm` (`:1273-1295`).

Popup **không có** nút đóng/mở lại riêng. Mọi chuyển trạng thái đều làm bằng cách chọn ô "Trạng thái Vấn đề" rồi bấm **Lưu** (`PUT`). Màn web không gọi endpoint `PATCH /status`.

### 1.4 Ai được làm gì (BE `Entities/Issue.php`)

| Cờ | Luật | Căn cứ |
|---|---|---|
| `can_edit` | Người đăng nhập là **người tạo** và trạng thái khác `closed` / `completed` | `Issue.php:145-151` |
| `can_delete` | Là **người tạo** và trạng thái đang `new` | `Issue.php:153-156` |
| `can_handle` | **Người xử lý** khi trạng thái là `assigned` / `in_progress` / `rejected` / `reopened`; hoặc **người duyệt** khi `resolved`; hoặc **người tạo / người xử lý** khi `completed` (để mở lại) | `Issue.php:158-183` |
| `allowed_next_statuses` | Xem mục 3 | `Issue.php:205-306` |

Khi PUT, `IssueService::update` cho qua nếu có `canEdit` **hoặc** `canHandle`. Người chỉ có `canHandle` thì chỉ ghi được `status` và `assignee_id` (`IssueService.php:419-447`). Ngoài các cờ trên không có permission hệ thống nào gate tạo / sửa / xoá / xử lý. Bốn quyền có trong hệ thống chỉ dùng để mở rộng phạm vi **xem danh sách** (mục 6).

---

## 2. Trường của form Tạo/Sửa

Form chia 2 cột: bên trái có 4 khối (Thông tin Vấn đề · Ghi nhận phát sinh · Đánh giá ảnh hưởng · Tệp đính kèm), bên phải có 3 khối (Thông tin xử lý · Liên kết & phân loại · Kế hoạch xử lý). Giá trị mặc định: `CreateIssueModal.vue:1006-1044`. Validate FE: `:1193-1215`, chạy hết một lượt nên báo lỗi mọi ô cùng lúc. Validate BE: `Http/Requests/Issue/IssueStoreRequest.php`, `IssueUpdateRequest.php`.

| # | Nhãn | Field | Kiểu | Mặc định | Bắt buộc FE | Luật BE store / update | Nguồn danh mục | Dòng FE |
|---|---|---|---|---|---|---|---|---|
| 1 | Tiêu đề Vấn đề | `title` | text | '' | Có | `required\|string\|max:255` (cả 2) | — | 60 |
| 2 | Giải pháp | `solution_id` | chọn 1 (tìm theo mã/tên) | null | Không | `nullable` / `nullable\|integer` | `GET assign/solutions/getAll?per_page=10000[&id=]`. FE chỉ giữ giải pháp có status ∈ {5,7,9,11,13,15} (`:287-295`, `:1122-1124`) | 72 |
| 3 | Dự án/Nhóm | `project_id` | chọn 1 | null | Không | `nullable` / `nullable\|integer` | `GET assign/prospective-projects/getAll?per_page=10000[&id=]` | 88 |
| 4 | Hạng mục / Module | `module_id` | chọn 1 | null | Có, khi giải pháp có `has_modules` | `required` nếu giải pháp `has_modules` (không tìm thấy giải pháp → coi như có) | Lấy từ `solutions[].modules`, lọc module status ∈ {2,6} (`:982-989`) | 105 |
| 5 | Loại Vấn đề | `issue_type` | chọn 1 | `bug` | Có | store `required`, update `nullable\|string` | Danh sách cứng 9 giá trị (`:861-871`) | 125 |
| 6 | Nhóm nguyên nhân | `root_cause_group` | chọn 1 | null | Không | update `nullable\|string` | Danh sách cứng 9 giá trị | 140 |
| 7 | Mức độ ưu tiên | `priority` | chọn 1 | `medium` | Có | store `required`, update `nullable\|string` | low/medium/high/critical | 155 |
| 8 | Mức độ ảnh hưởng | `impact_level` | chọn 1 | `personal` | Có | store `required`, update `nullable\|string` | 8 giá trị (`:889-898`) | 171 |
| 9 | Mô tả Vấn đề | `description` | textarea | '' | Có | store `required`, update `required\|string` | — | 188 |
| 10 | Nguồn phát hiện | `detected_from` | chọn 1 | `self` | Có | store `required`, update `nullable\|string` | 7 giá trị (`:899-907`) | 212 |
| 11 | Người phát hiện | `detected_by` | chọn NV | null | Không | update `nullable\|integer` | `store.state.allEmployeesOptions` (`:953-958`) | 227 |
| 12 | Ngày giờ phát hiện | `detected_at` | datetime | `new Date().toISOString()` | Không | update `nullable\|date`; BE `Carbon::parse` | — | 241 |
| 13 | Nhiệm vụ chính liên kết | `task_id` | chọn 1 | null | Không | update `nullable\|integer` | `GET assign/tasks/getAll` (mọi task không phải nháp, **không lọc theo giải pháp**) | 254 |
| 14 | Hạn xử lý | `due_date` | date `YYYY-MM-DD` | null | Không | update `nullable\|date` | — | 268 |
| 15 | Giờ hạn | `due_time` | time | `17:00` | Không | update `nullable\|string` | — | 280 |
| 16 | Người duyệt đóng | `approver_id` | chọn NV | null | Không | **không có luật** | allEmployeesOptions | 285 |
| 17 | Ảnh hưởng tiến độ | `affect_schedule` | chọn 1 | `no` | Không | — | no/minor/major | 313 |
| 18 | Ảnh hưởng chất lượng | `affect_quality` | chọn 1 | `no` | Không | — | no/minor/major | 327 |
| 19 | Ảnh hưởng khách hàng | `affect_customer` | chọn 1 | `no` | Không | — | no/minor/major | 341 |
| 20 | Ghi chú ảnh hưởng | `impact_note` | textarea | '' | Không | — | — | 357 |
| 21 | Tệp đính kèm / chứng cứ | `attachments[]` {name, attachment_type_id, file_name, file_path, file_size} | bảng nhiều dòng | [] | Không | update `nullable\|array` | Loại tài liệu: `GET assign/attachment-types/getAll`. File upload trước qua `POST files/upload` (form-data `attachments[]`) → trả URL | 375, 1312-1404 |
| 22 | Trạng thái Vấn đề | `status` | chọn 1 | `new` | Có | store không có luật; update không có luật (chỉ PATCH /status mới có `required`) | Tạo: new/assigned. Sửa/Xử lý: `allowed_next_statuses` | 527 |
| 23 | Lý do từ chối | `rejected_reason` → gửi thêm `reason` | textarea | null | Có khi status = `rejected` (chỉ hiện ở chế độ Xử lý) | PUT: lưu `rejected_reason = reason`. PATCH: `reason required` khi rejected | — | 556, 1235-1237 |
| 24 | Phòng ban xử lý | `handling_department_id` | chọn 1 | null | Có khi **chưa** chọn Người phụ trách | `required\|exists:departments,id` khi không có `assignee_id` | `store.state.departments` | 568 |
| 25 | Bộ phận xử lý | `handling_part_id` | chọn 1 | null | Không. Khoá khi chưa chọn phòng ban; đổi phòng ban thì xoá bộ phận (`:1176-1180`) | `nullable\|exists:parts,id` | `store.state.parts` lọc theo `department_id` (`:947-952`) | 589 |
| 26 | Người phụ trách xử lý | `assignee_id` | chọn NV | null | Có khi status = `assigned` | store `required\|exists:employees,id` khi status=assigned, ngược lại `nullable\|exists`; update `nullable\|integer` | allEmployeesOptions | 604 |
| 27 | Người theo dõi | `watcher_ids[]` | chọn nhiều NV | [] | Không | update `nullable\|array`; sync bảng `issue_watchers` | allEmployeesOptions | 618 |
| 28 | Người phối hợp | `supporter_ids[]` | chọn nhiều NV | [] | Không | sync `issue_supporters` | allEmployeesOptions | 630 |
| 29 | SLA xử lý | `sla` | chọn 1 | `1d` | Không | — | 4h/8h/1d/2d/custom (`:920-926`) | 642 |
| 30 | Tags | `tags[]` | gõ rồi Enter, có nút "Xóa" hết | [] | Không | Lưu vào cột JSON `tags`, đồng thời `firstOrCreate` bảng `tags` + sync `issue_tags` (`IssueService.php:580-597`) | — | 668, 1299-1311 |
| 31 | Kế hoạch xử lý | `handle_plan` | textarea | '' | Không | — | — | 708 |
| 32 | Điều kiện đóng Vấn đề | `close_condition` | textarea | '' | Không | — | — | 716 |

**Phụ thuộc giữa các trường**
- Chọn Giải pháp → Dự án tự lấy theo `solution.prospective_project_id`. Nếu `resetModule` thì Hạng mục bị xoá (`:1184-1192`). Ô Dự án bị khoá khi đã chọn giải pháp qua `lockSolution`.
- Hạng mục bị khoá khi chưa có giải pháp hoặc giải pháp không có `has_modules` (`:114` ở template).
- Phải có **Người phụ trách** hoặc **Phòng ban xử lý**. Trạng thái `assigned` bắt buộc có Người phụ trách.
- Mở từ tab Giải pháp: điền sẵn `solution_id` và `project_id`, khoá cả 2. Mở từ tab Hạng mục: điền sẵn và khoá thêm `module_id`. Xem `solutions/.../IssueTab.vue:574-581`, `solution-modules/.../IssueTab.vue:510-519`.
- Khi tạo, BE tự gán `issue_code` = `ISS-YYYYMM-NNNN` (`Issue.php:425-442`), `creator_id = auth()->id()`, `solution_version_id/code` và `module_version_id/code` lấy theo version hiện tại (`IssueService.php:378-417`).
- File đính kèm: chỉ nhận jpg/jpeg/png/doc/docx/xls/xlsx/pdf/ppt/pptx, tối đa 20MB (FE `:1341-1356`). Upload xong mới lưu `file_path` vào bảng `files` (`table='issues'`) qua `TableFileHelper::syncForTable` (`IssueService.php:599-627`).
- Cột có trong DB nhưng form không có: `steps_to_reproduce`, `expected_result`, `actual_result`, `severity`, `version`, `deadline`, `resolution`, `closed_reason`.

**Nhãn enum** (BE là nguồn chuẩn: `Transformers/IssueResource/DetailIssueResource.php:216-295`)
- `issue_type`: bug=Lỗi phần mềm, business=Vướng nghiệp vụ, change_request=Yêu cầu thay đổi, missing_data=Thiếu dữ liệu, risk=Rủi ro, infrastructure=Hạ tầng / tích hợp, missing_input=Thiếu thông tin đầu vào, customer_change=Yêu cầu thay đổi từ phía khách hàng, other=Khác.
- `root_cause_group`: validate, spec, data, integration, logic, product_catalog, product_drawing, product_specs, technology_change.
- `impact_level`: personal, team, module, project, customer, low, high, medium.
- `detected_from`: self, pm, leader, tester, client, meeting, employee.
- `priority` (kèm màu `Issue::PRIORITY_DATA` `Issue.php:138-143`): low #94a3b8 Thấp · medium #f59e0b Trung bình · high #f97316 Cao · critical #dc2626 Khẩn cấp.

---

## 3. Vòng đời trạng thái

`Issue::STATUS_DATA` (`Issue.php:95-136`) là nguồn chữ và màu cho danh sách, file xuất và lịch sử.

| Mã | Nhãn | Màu BE |
|---|---|---|
| `new` | Mới ghi nhận | #64748b |
| `assigned` | Đã phân công | #0ea5e9 |
| `in_progress` | Đang xử lý | #2563eb |
| `resolved` | Đã xử lý xong | #16a34a |
| `completed` | Hoàn thành | #16a34a |
| `rejected` | Từ chối | #dc2626 |
| `closed` | Đã đóng | #6b7280 |
| `reopened` | Mở lại | #d97706 |

Chuyển hợp lệ theo `getAllowedNextStatuses` (`Issue.php:205-306`). Danh sách trả về luôn gồm cả trạng thái hiện tại.

| Từ | → Sang | Ai |
|---|---|---|
| new | assigned | Người tạo |
| new | in_progress | Người xử lý |
| new | closed | Người tạo / Người xử lý |
| assigned | in_progress | Người xử lý |
| assigned | closed | Người tạo / Người xử lý |
| in_progress | resolved (khi **có** người duyệt) hoặc completed (khi **không có** người duyệt) | Người xử lý |
| in_progress | closed | Người tạo / Người xử lý |
| resolved | completed / rejected | Người duyệt |
| resolved (khi không có người duyệt; trên thực tế không vào được nhánh này) | in_progress | Người tạo / Người xử lý |
| resolved | closed | Người tạo / Người xử lý |
| rejected | in_progress (xoá `rejected_at`, `rejected_reason`) | Người xử lý |
| rejected | closed | Người tạo / Người xử lý |
| completed | reopened | Người tạo / Người xử lý |
| reopened | assigned | Người tạo |
| reopened | in_progress | Người xử lý |
| reopened | closed | Người tạo / Người xử lý |
| closed | — (trạng thái cuối) | — |

Khi đổi trạng thái, BE ghi thêm mốc thời gian (`IssueService.php:449-476`, `506-546`): `resolved_at`, `completed_at`, `rejected_at + rejected_reason`, `closed_at + closed_reason`.

"Tình trạng hạn" (`IssueResource.php:90-108`) tính theo `due_date + due_time`, nếu không có giờ thì lấy 23:59:59. Kết quả là "Trong hạn" #16a34a hoặc "Quá hạn" #dc2626. Trạng thái resolved / closed / completed thì để trống.

---

## 4. Danh sách: cột, lọc, sắp xếp, phân trang, thống kê

### 4.1 Màn `/assign/issues`

**Cột** (`index.vue:661-893`; mặc định hiện hết, có popup cấu hình cột, `columnScreenKey='issues'`): STT (cố định) · Mã Vấn đề (cố định, sort, bấm để mở Xem) · Tiêu đề Vấn đề · Nhãn (tối đa 3 chip, còn lại hiện "+n") · Giải pháp (Mã - Tên) · Version giải pháp · Dự án · Hạng mục/Module · Loại Vấn đề · Người xử lý · Bộ phận xử lý (`handling_part_name || handling_department_name`) · Hạn xử lý (sort) · Tình trạng hạn (badge) · Mức độ ưu tiên (badge) · Người theo dõi · Người phối hợp · Người duyệt · Nguồn phát hiện · Người phát hiện · Ngày phát hiện (sort) · Người cập nhật · Ngày cập nhật (sort) · Người tạo · Ngày tạo (sort) · Trạng thái (badge) · Hành động (cố định).

**Tìm nhanh** `keyword`: tìm theo mã, tiêu đề và họ tên người tạo (`IssueService.php:51-66`).

**Bộ lọc nâng cao** (`index.vue:496-578`; danh mục chỉ nạp khi mở panel; bộ lọc lưu localStorage `assign_issues` trong 10 phút):

| Ô | Tham số | Giá trị / nguồn |
|---|---|---|
| Công ty – Phòng ban – Bộ phận | `company_id`, `department_id`, `part_id` | `V2BaseCompanyDepartmentFilter`. Lọc qua bảng `issue_org_units`: khớp khi **bất kỳ** người giữ vai trò nào thuộc đơn vị đó (`IssueService.php:236-241`) |
| Giải pháp | `solution_id` | `assign/solutions/getAll`. Đổi giải pháp thì xoá version / hạng mục / dự án |
| Dự án | `project_id` | Chỉ có giá trị khi đã chọn giải pháp (`:470-477`) |
| Hạng mục/Module | `module_id` | Theo giải pháp |
| Version giải pháp | `solution_version_id` | `assign/solutions/{id}/versions`, hiển thị dạng "V" + code |
| Loại Vấn đề | `issue_type` | 9 giá trị |
| Người thực hiện | `assignee_id` | allEmployeesOptions |
| Người tạo | `created_by` (BE lọc theo `creator_id`) | allEmployeesOptions |
| Người duyệt | `approver_id` | allEmployeesOptions |
| Trạng thái | `status` | 8 giá trị (`:421-430`) |
| Mức độ ưu tiên | `priority` | 4 giá trị |
| Ngày tạo | `from_date`, `to_date` | Khoảng ngày theo `created_at` |

BE còn nhận thêm các tham số FE không gửi: `detected_by`, `watching_id`, `handling_department_id`, `handling_part_id`, `module_version_id` (`IssueService.php:84-127`).

**Lọc nhanh theo vai trò** (`index.vue:415-420`), mỗi lần chỉ bật 1 nút, bấm lại để tắt: Tôi phụ trách xử lý (`assignee_id`) · Tôi phát hiện (`detected_by`) · Tôi theo dõi (`watching_id`) · Tôi duyệt đóng (`approver_id`). Giá trị gửi lên là `current_employee.id`.

**Thống kê** (`index.vue:89-94`): "Tổng" = `meta.total`, "Quá hạn" = `overdue_total` do BE tính trên cùng bộ lọc. Quá hạn nghĩa là có `due_date` < hiện tại và trạng thái không thuộc resolved / closed / completed (`IssueController.php:35-39`).

**Sắp xếp**: `sort_field` ∈ whitelist {issueCode, issue_code, deadline→due_date, detectedAt, updatedAt, createdAt, created_at}, `sort_dir` asc/desc. Khoá lạ thì về `created_at desc`. Luôn chốt thêm `id desc` (`IssueService.php:23-31,137-143`).

**Phân trang**: `page`, `per_page` (mặc định 20). Response trả `meta.current_page/per_page/total/last_page/from/to`.

**Xuất Excel**: `GET assign/issues/export` dùng cùng bộ lọc với danh sách nhưng không phân trang. `fields` lọc theo whitelist `ExportColumnRegistry::COLUMNS['issues']` (`app/ExcelExport/ExportColumnRegistry.php:1077`). File ra `danh_sach_issue.xlsx`.

### 4.2 Tab "Issue" ở Công việc của tôi (`my-job/components/IssuesTab.vue`)
- Dữ liệu là mảng do trang cha nạp một lần qua `GET assign/my-job/my-issues?page=1&per_page=10` (`my-job/index.vue:292-296`). Tab tự lọc / phân trang trên mảng đó ở client, 10 dòng/trang (`IssuesTab.vue:202-238`).
- BE `MyJobService::getMyIssues` (`Services/MyJobService.php:852-902`): lấy issue mà mình là người tạo, người xử lý, người theo dõi hoặc người phối hợp. **Không** tính người phát hiện và người duyệt. Bỏ trạng thái `closed`. Sắp xếp: có `due_date` trước, rồi `due_date asc`.
- Cột: STT · Tên Vấn đề · Module · Ưu tiên · Vai trò của tôi (`my_role`) · Trạng thái · Hạn xử lý (`IssuesTab.vue:248-267`).
- Lọc: từ khoá (tiêu đề hoặc mã), Ưu tiên, Trạng thái (chỉ 5 giá trị: new/assigned/in_progress/resolved/reopened).
- Hành động: Xem · Sửa (`can_edit`) · Xử lý (`can_handle`) · Lịch sử · Xoá (`can_delete`) (`IssuesTab.vue:344-392`). Có nút Tạo (`:310`). Xuất Excel gọi `GET assign/my-job/issue-list/export`.

### 4.3 Tab Vấn đề của Giải pháp / Hạng mục
- Đều gọi `GET assign/issues`, cố định thêm `solution_id` (`solutions/.../IssueTab.vue:503-516`) hoặc `module_id` (`solution-modules/.../IssueTab.vue:442-452`). Vì vậy vẫn chịu phạm vi quyền xem ở mục 6.
- Nút "Tạo mới" chỉ hiện khi giải pháp có status ∈ {5,7,9,11,13,15} (`solutions/.../IssueTab.vue:209-216,327-329`), hoặc khi hạng mục có status ∈ {2,6} và chưa đóng (`solution-modules/.../IssueTab.vue:190,301-304`).
- Lọc nhanh 3 nút: Tôi làm (`assignee_id`) · Tôi báo cáo (`created_by`) · Tôi theo dõi (`watching_id`).
- Xuất Excel: `GET assign/solutions/{id}/manager/issues/export`, `GET assign/solution-modules/{id}/manager/issues/export`.
- Popup "Vấn đề sắp đến hạn": `GET assign/solutions/{id}/manager/issues-upcoming` (`SolutionService.php:1019-…`). Lấy `due_date` trong khoảng [hôm nay, hôm nay + `general_regulations.issue_due_days`], bỏ resolved / closed. Lọc được theo keyword, status, `solution_module_id`, assignee_id, created_by, priority.

---

## 5. Quan hệ với đối tượng khác

| Quan hệ | Cột / bảng | Ghi chú |
|---|---|---|
| Vấn đề → Giải pháp | `issues.solution_id`, kèm snapshot `solution_version_id/code` | `Issue.php:392-395` |
| Vấn đề → Hạng mục | `issues.module_id` → `solution_modules`, kèm `module_version_id/code` | `Issue.php:397-400` |
| Vấn đề → Dự án tiền khả thi | `issues.project_id` → `prospective_projects` | `Issue.php:370-382` |
| Vấn đề → Nhiệm vụ | `issues.task_id` ("Nhiệm vụ chính liên kết"), **1 chiều** | `Issue.php:402-405`. Không có chỗ nào tạo Vấn đề từ Nhiệm vụ, hay tạo Nhiệm vụ từ Vấn đề. Entity Task không có quan hệ ngược về issues |
| Vấn đề → Phòng ban / Bộ phận xử lý | `handling_department_id`, `handling_part_id` | `Issue.php:331-342` |
| Phân loại suy ra | `scope_text`: có giải pháp → "Vấn đề giải pháp"; có dự án → "Vấn đề dự án"; còn lại → "Vấn đề phòng ban" | `Issue.php:347-358`, không lưu cột |
| Người | `creator_id`, `assignee_id`, `approver_id`, `detected_by`, `issue_watchers`, `issue_supporters` | Đều là `employees.id` |
| Snapshot tổ chức | `issue_org_units` (issue_id, employee_id, company/department/part) | Đồng bộ lại sau mỗi lần store/update (`IssueService.php:247-313`). Dùng cho phân quyền tầng 3 và bộ lọc tổ chức |
| Bàn giao | `handover_items.itemable_type = Issue` | `Services/HandoverService.php:216-297` |
| My-todo | `MyTodoService::getAssignedIssues` bỏ closed/completed/rejected | `Services/MyTodo/MyTodoService.php:470-482` |
| Meeting | Không có khoá ngoại. Chỉ có giá trị `detected_from = 'meeting'` và loại tài liệu "Biên bản meeting" (mảng `fileTypeList` khai trong `CreateIssueModal.vue:928-935` nhưng không dùng) | — |
| Tags | Cột JSON `issues.tags`, đồng thời có `issue_tags` ↔ `tags` | Hiển thị đọc từ cột JSON |
| Tệp | Bảng `files` (`table='issues'`, `table_id`) | `Issue.php:412-417` |
| Bình luận | Bảng `comments` (package actuallymab, polymorphic), `comment_attachments`, `comment_reactions` | `IssueCommentController.php` |
| Lịch sử | `issue_history` (action create/update/change_status, old/new JSON theo nhãn, `note`, `is_subset`) | `Services/IssueHistoryService.php`; đọc qua `SystemLogService::issueLogs` (`:1279-1290`) |

---

## 6. Phân quyền xem và thông báo

### 6.1 Bốn quyền (group "Vấn đề", `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1167-1173`)

| Tên quyền (name) | Hiển thị | Tác dụng ở `GET assign/issues` |
|---|---|---|
| `Xem danh sách issue theo tổng công ty` | Xem danh sách Vấn đề theo tổng công ty | Thấy tất cả, không giới hạn (`IssueService.php:161-163`) |
| `Xem danh sách issue theo công ty` | … theo công ty | Tầng 3: issue có người giữ vai trò thuộc công ty đang làm (`current_company_role`) |
| `Xem danh sách issue theo phòng ban` | … theo phòng ban | Tầng 3: thuộc phòng ban hoặc bộ phận mình quản lý (`listManageDepartmentIds/PartIds`) |
| `Xem danh sách issue theo bộ phận` | … theo bộ phận | Tầng 3: thuộc bộ phận mình quản lý |

Ai không có quyền nào vẫn thấy các issue thuộc **tầng 1** và **tầng 2** (`IssueService.php:158-202`):
- Tầng 1: mình là người tạo, phát hiện, xử lý, duyệt, theo dõi hoặc phối hợp.
- Tầng 2: issue thuộc giải pháp mình tham gia (`TaskLinkScopeHelper::mySolutionIds`), hoặc thuộc dự án mình là thành viên (bảng `prospective_project_support_department_employees` hoặc dự án của giải pháp mình tham gia).

FE chỉ dùng 4 quyền này để quyết định hiện ô Công ty / Phòng ban / Bộ phận trong bộ lọc (`index.vue:896-903`).

Route nhóm `/assign/issues` (`Routes/api.php:1100-1115`) chỉ có `auth:api`. Riêng `POST /` có thêm middleware `solutionMemberActive`: thành viên đã bị khoá khỏi giải pháp `solution_id` thì không tạo được (`app/Http/Middleware/CheckSolutionMemberActive.php`).

### 6.2 Thông báo (`EmployeeInfoService::sendNotification`, url luôn là `/assign/issues?open_issue={id}[&comment_id=]`)

| Sự kiện | Người nhận | type | Căn cứ |
|---|---|---|---|
| Tạo / đổi đơn vị xử lý mà **chưa có người phụ trách** | Trưởng bộ phận (nếu không có thì Trưởng phòng ban), trừ khi chính người tạo là trưởng đơn vị | `issue` ("Tạo mới") | `IssueService.php:694-748` |
| Chuyển sang `resolved` | Người duyệt | `issue` ("Chờ duyệt") | `:636-656` |
| Chuyển sang `rejected` | Người xử lý (kèm lý do) | `issue` ("Từ chối") | `:658-683` |
| Bình luận gốc | Người tạo, xử lý, duyệt, theo dõi, phối hợp (trừ người gửi) | `issue_comment` | `IssueCommentController.php:217-276` |
| Trả lời bình luận | Tác giả bình luận cha | `issue_comment_reply` | `:278-298` |
| Nhắc tên `@[Họ tên]` | Người được nhắc (tìm theo `employee_infos.fullname`) | `issue_comment_mention` | `:300-351` |
| Thả emoji | Tác giả bình luận | `issue_comment_react` | `:353-372` |

Các trường hợp **không** có thông báo: giao cho đích danh một người phụ trách, chuyển sang completed / closed / reopened.

---

## 7. API app dùng được

Mọi API đều có tiền tố `/api/v1`, cần `auth:api` (JWT). Phản hồi danh sách dùng `apiGetList`: `{ data: [...], meta: {current_page, per_page, total, last_page, from, to}, ...extra }`. Phản hồi đơn dùng `responseJson`: `{ message, code, data }`.

| Method | Path | Tham số chính | Trả về |
|---|---|---|---|
| GET | `/assign/issues` | `keyword, status, priority, issue_type, solution_id, project_id, module_id, solution_version_id, module_version_id, assignee_id, created_by, approver_id, detected_by, watching_id, handling_department_id, handling_part_id, company_id, department_id, part_id, from_date, to_date, sort_field, sort_dir, page, per_page` | `data[]` theo `IssueResource` (id, code, title, status, status_text, status_color, priority(_text/_color), issue_type(_text), due_date d/m/Y, due_time, due_status_text/color, in_progress, solution/project/module names, assignee_name, approver_name, creator_name, handling_*_name, watcher_names, supporter_names, tags[], scope_text, can_edit, can_delete, can_handle, my_role, created_at, updated_at) + `overdue_total` |
| GET | `/assign/issues/{id}` | — | `DetailIssueResource`: mọi field thô + quan hệ (creator, assignee, approver, detectedBy, project, solution, module, task, watchers, supporters, attachments, history) + `watcher_ids, supporter_ids, can_edit, can_delete, can_handle, allowed_next_statuses[{id,name,color}]`. **Không có** `status_text`/`status_color` |
| POST | `/assign/issues` | Body là các field ở mục 2 + `attachments[]` + `watcher_ids[]` + `supporter_ids[]` + `tags[]` | Detail |
| PUT | `/assign/issues/{id}` | Như POST. Khi `status=rejected` thì gửi thêm `reason`. Người chỉ có quyền xử lý thì chỉ `status` và `assignee_id` được ghi | Detail |
| PATCH | `/assign/issues/{id}/status` | `status` (bắt buộc), `reason` (bắt buộc khi rejected). Có kiểm `allowed_next_statuses` | Detail, message "Cập nhật trạng thái thành công". Web không dùng, nhưng **app nên dùng** cho các thao tác đổi trạng thái |
| DELETE | `/assign/issues/{id}` | — | Chỉ người tạo, khi status `new`. Xoá cứng |
| GET | `/assign/issues/export` | Bộ lọc như trên + `fields=a,b,c` | File xlsx |
| GET | `/assign/issues/{id}/comments` | — | Cây bình luận: `[{id, parent_id, comment, created_at, commentator{id,name,avatar}, attachments[], reactions{emoji:[{id,name}]}, children[]}]` |
| POST | `/assign/issues/{id}/comments` | multipart: `comment` (bắt buộc, ≤5000), `parent_id`, `files[]` (≤50MB/file) | Bình luận vừa tạo |
| PUT | `/assign/issues/{id}/comments/{cid}` | `comment` | Chỉ tác giả |
| DELETE | `/assign/issues/{id}/comments/{cid}` | — | Chỉ tác giả |
| POST | `/assign/issues/{id}/comments/{cid}/react` | `emoji` (≤20) | Bấm lại cùng emoji thì gỡ; message là `added`, `changed` hoặc `removed` |
| GET | `/assign/system-logs/issue/{id}` (+ `/filter-options`) | — | Dòng lịch sử: action_label, changes, note, actor, created_at |
| GET | `/assign/my-job/my-issues` | `keyword, status, priority, sort_field (due_date/created_at/updated_at), sort_dir, page, per_page` | IssueResource phân trang |
| GET | `/assign/my-job/issue-list/export` | như trên | xls |
| GET | `/assign/solutions/{id}/manager/issues-upcoming` | `keyword, status, solution_module_id, assignee_id, created_by, priority, sort_*` | IssueResource phân trang |
| POST | `/files/upload` | form-data `attachments[]` | `data: [url]` dùng làm `file_path` |
| GET | `/assign/attachment-types/getAll` | — | Loại tài liệu |
| GET | `/assign/solutions/getAll?per_page=10000` | — | Giải pháp kèm `modules[]`, `has_modules`, `status`, `prospective_project_id` |
| GET | `/assign/prospective-projects/getAll?per_page=10000` | — | Dự án |
| GET | `/assign/tasks/getAll` | `keyword, project_id` | `[{id, code, name}]`. Lưu ý: trả `name`, không phải `title` |
| GET | `/assign/solutions/{id}/versions` | — | Version giải pháp |

Danh mục nhân viên, phòng ban, bộ phận trên web lấy từ store (`allEmployeesOptions`, `departments`, `parts`), được nạp lúc lấy user-profile. App cần nguồn tương đương.

---

## 8. Điểm lạ / bug / fail-open

> Chỉ ghi nhận, chưa sửa. Mức độ chỉ là đánh giá sơ bộ.

**Quyền / fail-open**
1. **Xem chi tiết không kiểm phạm vi.** `GET /assign/issues/{id}` (`IssueController.php:78-96`) không gọi `applyPermissionScope`. Ai đăng nhập cũng đọc được mọi Vấn đề nếu biết id, kèm lịch sử và đính kèm. Tương tự với `GET /{id}/comments`, `POST /{id}/comments` (`IssueCommentController.php:22-94`) và `GET /assign/system-logs/issue/{id}`.
2. **`issues-upcoming` không kiểm phạm vi** (`SolutionService.php:1019+`). Đọc được Vấn đề của bất kỳ giải pháp nào.
3. **PUT bỏ qua kiểm tra chuyển trạng thái.** `IssueService::update` không đối chiếu với `getAllowedNextStatuses`. Người tạo có `can_edit` gửi thẳng `status=completed` (hoặc bất kỳ giá trị nào) là được ghi (`IssueService.php:446`). FE chỉ giới hạn bằng danh sách lựa chọn trong ô.
4. **Nhánh chỉ có quyền xử lý vẫn sửa được nhiều hơn mong muốn.** BE chỉ lấy `status` và `assignee_id` (`:442-444`), nhưng ngay sau đó `saveRelatedData` vẫn sync `watcher_ids`, `supporter_ids`, `tags`, `attachments` (`:478`). Người duyệt hoặc người xử lý gọi API là đổi được người theo dõi, người phối hợp, tags, và gán lại người phụ trách.
5. **Store không giới hạn `status`.** `IssueStoreRequest` không có luật cho `status`, còn `store()` dùng `Issue::create($request->all())` (`IssueService.php:380-388`). Qua API có thể tạo ngay một Vấn đề ở trạng thái `completed`, gán `approver_id`, `completed_at`… tuỳ ý.
6. Không có quyền hệ thống nào gate tạo / sửa / xoá. Tạo chỉ bị chặn khi là thành viên đã bị khoá khỏi giải pháp.

**Logic / dữ liệu**
7. **Người xử lý ở trạng thái `new` không có nút Xử lý.** `canHandle` không chứa `STATUS_NEW` (`Issue.php:164-169`), trong khi `getAllowedNextStatuses` cho người xử lý chuyển new → in_progress (`:220-222`). Vấn đề tạo ở trạng thái "Mới" mà đã chọn người phụ trách thì người đó không thấy nút Xử lý, chỉ người tạo mới đổi được.
8. Nhánh `resolved` khi không có người duyệt (`Issue.php:257-261`) không bao giờ xảy ra, vì `in_progress → resolved` chỉ mở khi có người duyệt.
9. **Không có thông báo khi giao đích danh người phụ trách.** Cũng không báo khi completed / closed / reopened (mục 6.2).
10. **Đóng không có lý do.** FE không có ô lý do đóng, nên `closed_reason` luôn null khi đóng từ web (chỉ khi rejected FE mới gửi `reason`, `CreateIssueModal.vue:1235-1237`).
11. **Ô Nhiệm vụ liên kết hiển thị sai.** BE `TaskService::getAll` trả `tasks.title as name` (`Services/TaskService.php:865-869`), còn FE map `title: t.title` (`CreateIssueModal.vue:1156-1160`) nên `title` luôn undefined. SearchPicker chỉ hiện mã và không tìm được theo tên. Picker cũng không lọc theo giải pháp, dự án hay quyền xem: lấy mọi task không phải nháp trong hệ thống.
12. **Popup Vấn đề sắp đến hạn lỗi khi bấm Xem.** Gọi `this.$refs.createIssueModal.view(item)` (`IssueUpcomingModal.vue:425`), nhưng `CreateIssueModal` không có method `view`, nên bấm là lỗi JS.
13. `issues-upcoming` lọc `created_by` theo cột `created_by` chứ không theo `creator_id`, khác màn chính. Danh sách này cũng vẫn chứa completed / rejected (chỉ bỏ resolved / closed).
14. **Màu trạng thái lệch giữa FE và BE.** Header popup tự map màu (`CreateIssueModal.vue:1447-1459`): completed #22c55e, rejected #f97316, closed #94a3b8, reopened #ef4444, khác `Issue::STATUS_DATA`. Nhãn resolved trong `DetailIssueResource::ENUM_MAPS` là "Đã xử lý", còn STATUS_DATA là "Đã xử lý xong".
15. **Tab Issue ở Công việc của tôi chỉ có tối đa 10 dòng.** Trang cha gọi `my-issues?page=1&per_page=10` một lần, tab phân trang client trên 10 dòng đó. `IssuesTab` emit `refresh` sau khi lưu, nhưng `my-job/index.vue:72` không nghe sự kiện này nên lưu xong không tải lại. Bộ lọc trạng thái của tab cũng thiếu completed / rejected.
16. Phạm vi `my-issues` (tạo / xử lý / theo dõi / phối hợp) lệch với màn chính (thêm phát hiện / duyệt). Người duyệt không thấy Vấn đề đang chờ mình duyệt trong tab này.
17. **Lọc nhanh có thể gửi sai id.** Tab Hạng mục lấy `auth.user.employee_info_id` làm id người đăng nhập (`solution-modules/.../IssueTab.vue:298-299`). Màn chính fallback sang `employee_info_id` khi thiếu `current_employee` (`index.vue:463-465`). Trong khi `assignee_id` / `creator_id` là `employees.id`. Nếu 2 id khác nhau trên DB gộp thì lọc nhanh ra sai. Cần kiểm dữ liệu.
18. `CreateIssueModal` ghi thẳng vào prop `lockModule/lockSolution/lockProject` (`:1052-1054`, `:1098-1100`). Vue cảnh báo mutate prop.
19. **Xoá cứng.** Bảng `issues` không có `deleted_at` (migration `2026_03_16_000001_create_issues_tables.php`). `destroy` gọi `$issue->delete()` và không dọn `issue_history`, `issue_watchers`, `issue_supporters`, `issue_org_units`, `files`, `comments`.
20. **`generateCode()` không chống trùng khi tạo đồng thời.** Hàm lấy bản ghi cuối rồi +1 (`Issue.php:425-442`), trong khi cột `issue_code` có unique. Hai request tạo cùng lúc có thể bị lỗi 500.
21. **Tags lưu 2 nơi.** Cột JSON `tags` và bảng `issue_tags`. `DetailIssueResource` trả `$this->tags`, tức cột JSON (vì attribute đè quan hệ). Quan hệ `tags` có eager load nhưng không được dùng.
22. My-todo sinh URL `/assign/issue/{id}` (`MyTodoService.php:749-750`). Route này không tồn tại, vì web dùng `/assign/issues?open_issue=`.
23. `detected_at` mặc định là `new Date().toISOString()` (giờ UTC) và BE `Carbon::parse` thẳng. Cần kiểm xem có bị lệch 7 tiếng không.
24. Store không validate `due_date`, `detected_at`, `approver_id` (`exists`), `watcher_ids`. Update không validate `approver_id`.
25. Tên file và tiêu đề xuất Excel còn dùng chữ "issue" ("Danh sách issue", "Mã issue"), lệch với nhãn "Vấn đề" trên giao diện.

---

## 9. Gợi ý cho bản app

Phần này là gợi ý thiết kế, không có căn cứ trong code.

- **Danh sách**: dùng `GET /assign/issues`. Lọc nhanh 4 vai trò dùng `employees.id`. Đặt badge từ `status_color`, `priority_color`, `due_status_color`. Thẻ thống kê: Tổng, Quá hạn (`overdue_total`).
- **Chi tiết**: dùng `GET /assign/issues/{id}`. Màu trạng thái lấy theo `Issue::STATUS_DATA` (danh sách trả sẵn; chi tiết thì map theo bảng mục 3). Nút hành động theo `can_edit`, `can_handle`, `can_delete`. Đổi trạng thái nên dùng `PATCH /status` (có kiểm chuyển hợp lệ), các lựa chọn lấy từ `allowed_next_statuses`.
- **Form tạo**: tối thiểu gồm Tiêu đề, Loại, Ưu tiên, Ảnh hưởng, Mô tả, Nguồn phát hiện, Người phụ trách hoặc Phòng ban xử lý, Hạng mục (khi giải pháp có hạng mục). Các trường còn lại cho vào khối thu gọn.
- **Bình luận + lịch sử**: dùng lại API comments và system-logs.
- **Deep link thông báo**: `/assign/issues?open_issue={id}&comment_id={cid}` và 5 `type` ở mục 6.2.
- Nên chốt với user trước khi làm app: các mục 1, 3, 4, 7, 9, 11, 15, 16 ở phần 8.
