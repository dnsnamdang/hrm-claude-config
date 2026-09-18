# Plan — Liên kết Nhiệm vụ với Dự án, Meeting, Phòng ban (#11456)

## Phase 1 — DB + BE nền tảng
- [x] Migration `add_meeting_link_to_tasks_table`: `solution_id` nullable + `meeting_id` + `meeting_report_id` (nullable, index), DDL trần không transaction
- [x] `Task.php`: `$fillable` += `meeting_id`, `meeting_report_id`; quan hệ `meeting()`, `meetingReport()`
- [x] `TaskStoreRequest` / `TaskUpdateRequest`: `project_id`/`solution_id` nullable; `solution_module_id` required chỉ khi có solution có hạng mục; += `meeting_id`, `meeting_report_id`
- [x] `TaskService::store/createSingleTask/update`: ghi 2 field mới
- [x] `TaskService::index`: filter `meeting_id`
- [x] `TaskResource` + `DetailTaskResource`: trả `meeting_id`, `meeting_code`, `meeting_name`, `meeting_report_id`

## Phase 2 — BE link động + biên bản
- [x] `getMySolutionIds` / `getMyProjectIds` chuyển thành helper dùng chung
- [x] `prospective-projects/getAll?mine=1` lọc theo thành viên
- [x] `solutions/getAll?mine=1` lọc theo thành viên giải pháp / hạng mục
- [x] `meetings/getAll?mine=1` lọc theo `meeting_employees` ∪ `created_by`
- [x] Resource biên bản meeting: mỗi dòng trả `assigned_task_count` + `assigned_tasks[]` (withCount, không N+1)

## Phase 3 — FE component chung + màn dự án
- [x] `components/assign/task/TaskListTab.vue`: bảng nhiệm vụ theo scope (`project_id` | `meeting_id`), UI bám `/assign/tasks`, nút Thêm nhiệm vụ mở `CreateTaskModal` với `lockedDefaults`
- [x] `prospective-projects/_id/manager.vue`: tab `tasks` đổi sang `TaskListTab({ project_id })`, bỏ điều kiện phải có giải pháp (⇒ ẩn tab Nhiệm vụ giải pháp)

## Phase 4 — FE form task (nhiệm vụ phòng ban)
- [x] `CreateTaskModal`: bỏ `*` + required FE ở Giải pháp / Dự án; Dự án chọn tự do khi chưa chọn Giải pháp
- [x] `CreateTaskModal`: thêm ô Meeting (không bắt buộc) + `lockedDefaults.meeting_id` + payload `meeting_id`/`meeting_report_id`
- [x] Nguồn options dự án / giải pháp / meeting thêm `mine=1`

## Phase 5 — FE meeting
- [x] `MeetingForm.vue`: thêm tab "Nhiệm vụ" (chỉ khi `isShow && form.id`) → `TaskListTab({ meeting_id })`
- [x] `MeetingReport.vue`: icon "Giao nhiệm vụ" mỗi dòng (chỉ `isShow`), mở `CreateTaskModal` điền sẵn tên/người/hạn/meeting, loại nhiệm vụ theo số người
- [x] `MeetingReport.vue`: badge "Đã giao N nhiệm vụ" + popup danh sách task của dòng, reload sau khi tạo

### Checkpoint — 2026-09-18
Vừa hoàn thành: **CODE XONG 5 PHASE (BE + FE)** trên nhánh `tpe-develop-assign`.
- Migration `2026_09_18_000001_add_meeting_link_to_tasks_table` đã chạy trên DB dev `hrm_prod_6_6`
  (`solution_id` nullable + `meeting_id` + `meeting_report_id`).
- Kiểm thử BE bằng tinker (dữ liệu test đã dọn, tasks trở lại 22 bản ghi):
  · Nhiệm vụ phòng ban không dự án/giải pháp → tạo được, `solution_id`/`project_id` NULL.
  · Giao từ dòng biên bản 2 người → 2 bản ghi cùng `batch_id`, cùng `meeting_id`+`meeting_report_id`.
  · Filter `meeting_id` / `prospective_project_id` trả đúng; Resource trả `meeting_code`.
  · Biên bản trả `assigned_task_count` + `assigned_tasks[]` đúng dòng.
  · Link động: dự án 268 → 0 (không là thành viên), giải pháp 28 → 0, meeting chỉ 1;
    tham số `id=` giữ đúng giá trị đang chọn (2 dòng).
- FE: kiểm cú pháp template + script 5 file bằng vue-template-compiler + esbuild → sạch;
  CRLF của `CreateTaskModal.vue` và `MeetingReport.vue` giữ nguyên (số dòng = số \r).
Đang làm dở: không có.
Bước tiếp theo: user kiểm thử giao diện (tab Nhiệm vụ ở chi tiết dự án + chi tiết meeting, icon
Giao nhiệm vụ trên biên bản, tạo nhiệm vụ phòng ban không chọn dự án/giải pháp).
Blocked: không có.

## Phase 6 — Sửa lỗi phát hiện khi kiểm thử giao diện (18/09/2026)
- [x] Cột "Hạn dự kiến" ở bảng biên bản bị bóp còn `col-1` (hiện "28/") do lấy chỗ cho cột Thao tác → thu cột "Nội dung" (`col-3` → `col-2` khi ở màn chi tiết), trả Hạn về `col-2`
- [x] **`getMyProjectIds()` luôn trả RỖNG** — `prospective_project_support_department_employees.prospective_project_id` = 0 ở CẢ 164/164 dòng, dự án thật nằm ở bảng cha `..._support_departments`. Lỗi có sẵn, ảnh hưởng cả Tầng 2 phân quyền xem danh sách Nhiệm vụ lẫn link động mới → join qua bảng cha (vẫn cộng thêm cột trực tiếp nếu sau này ghi đúng)
- [x] Tham số giữ giá trị đang chọn: `id` ở `prospective-projects/getAll` và `solutions/getAll` là LỌC CỨNG → dùng nó ở màn Sửa thì danh sách chỉ còn 1 lựa chọn. Tách sang `include_id` (FE + BE)
- [x] Mở Tạo mới từ tab Nhiệm vụ của **Giải pháp**: `mine=1` giao với `id=` ra rỗng → ô Giải pháp/Dự án trống trơn. Sửa: trong nhánh `mine`, `$keepId = include_id ?: id`
- [x] Dự án **đã đóng** vẫn hiện nút "Tạo mới" ở tab Nhiệm vụ → truyền `:can-create="!isProjectClosed"`

### Checkpoint — 2026-09-18 (sau kiểm thử UI)
Vừa hoàn thành: **KIỂM THỬ GIAO DIỆN PASS** trên :3000 (DB `hrm_prod_6_6`), 4 tài khoản khác quyền:
DNS Admin (13), Nguyễn Đức Tuân (24), Chu Khương Duy (27), Thiều Quốc Đạt (341).
Case đã chạy: tab Nhiệm vụ ở chi tiết dự án (ẩn tab Nhiệm vụ giải pháp) · tạo nhiệm vụ gắn dự án không
giải pháp · tab Nhiệm vụ + icon Giao nhiệm vụ ở chi tiết meeting · kế thừa 1 người → Nhiệm vụ cụ thể ·
2 người → Nhiệm vụ chung sinh 2 bản ghi cùng `batch_id` · dòng chỉ có người ngoài → bỏ qua, ô trống ·
màn Tạo meeting không có tab/icon · nhiệm vụ phòng ban thuần (mọi liên kết NULL) · gán + giữ meeting ở
màn Sửa · link động 4 tài khoản · phân quyền chéo (user không liên quan thấy 0, meeting lạ trả 404) ·
bộ lọc Loại nhiệm vụ 5→3→reset 5 · xoá qua popup `$confirm` · dự án không giải pháp vẫn có tab ·
dự án đã đóng ẩn nút Tạo mới. 5 lỗi phát hiện đã sửa hết (Phase 6) và test lại.
Dữ liệu test đã dọn sạch (tasks về 22 bản ghi, 2 dòng biên bản test đã xoá).
Đang làm dở: không có.
Bước tiếp theo: user duyệt → chốt 2 điểm nghiệp vụ còn treo (xem mục "Cần user quyết" trong design.md),
sau đó commit.
Blocked: không có.

## Phase 7 — Chuẩn hoá UI tab Nhiệm vụ theo skill `list-page` (18/09/2026)
- [x] Port `components/V2BaseRowActions.vue` từ nhánh `gop_db` (chỉ phụ thuộc `V2BaseIconButton`) — nhánh `tpe-develop-assign` chưa có
- [x] Cột **Hành động riêng ở CUỐI bảng** (căn giữa, 140px) thay cho chùm nút nhét trong ô đầu; tối đa 3 nút, dư vào menu `⋮`; điều kiện hiện/ẩn qua `visible` (không disable)
- [x] **Bỏ hành động "Xem"** — cột **Mã nhiệm vụ** là `button.v2-cell-link` mở popup Xem (mục 3a: nhiệm vụ không có route chi tiết)
- [x] **Tách cột Mã / Tên** (trước gộp "Mã-Tên nhiệm vụ"); Mã ghim trái + sortable, Tên chữ thường `text-wrap`
- [x] Thứ tự cột theo mục 4: STT → Mã → Tên → Loại nhiệm vụ → Giải pháp|Dự án → Người thực hiện → Hạn hoàn thành → Ưu tiên → **Người tạo → Ngày tạo → Trạng thái → Hành động**
- [x] Màu chữ đúng 3 mức (`field-line text-dark font-weight-normal`), bỏ mọi `font-weight-bold`
- [x] **Ô rỗng để trống**, bỏ hết dấu `—` trong dữ liệu hiển thị
- [x] Badge trạng thái lấy **màu từ BE** (`:color="item.status_color"`); Resource trả thêm `status_color`
- [x] **`Task::STATUS` chỉnh về bảng 9 mã màu chuẩn** (mục 3c-2): Nháp `#64748B`, Hoàn thành-Chờ duyệt `#D97706`, Từ chối kết quả + Từ chối triển khai `#DC2626`, Huỷ `#6B7280`; các mã còn lại viết hoa cho đồng bộ
- [x] Thang **Mức độ ưu tiên riêng** (`#F59E0B` / `#F97316` / `#DC2626`), không dùng màu trạng thái
- [x] Bộ lọc: bỏ `title`/`subtitle` riêng → dùng mặc định "Bộ lọc danh sách"; nhãn **floating**; **gộp "Hạn hoàn thành từ/đến" thành MỘT ô range** (`V2BaseFloatingField variant="range"`), 2 key gửi BE giữ nguyên
- [x] Filter auto-search bằng deep watcher (`handleReset`/`handleSort` chỉ đổi `filters`)
- [x] Căn lề + bề rộng theo mục 15 (STT 60 center, Trạng thái 130 center, Hành động 140 center, Ưu tiên center)
- [x] Sửa lỗi sort không đổi chiều: prop `sortBy` phải là **khoá cột** (`sortKey`) chứ không phải tên cột DB — thêm `sortKey` tách khỏi `filters.sort_field`

### Checkpoint — 2026-09-18 (chuẩn hoá UI theo skill)
Vừa hoàn thành: viết lại `TaskListTab.vue` theo skill `list-page`, kiểm thử lại trên :3000 (DNS Admin):
cột đúng thứ tự · bấm Mã mở popup Chi tiết (chỉ đọc) · badge Nháp `#64748B` / Đang thực hiện `#2563EB`
đúng mã chuẩn lấy từ BE · lọc Loại nhiệm vụ 4→3→Làm mới 4 · ô "Hạn hoàn thành" là 1 ô range 2 datepicker
+ dấu → cao 36px · sort Mã asc/desc đúng cả 2 chiều (đã kiểm URL request) · tab Meeting hiện cột "Dự án" ·
Hạn hoàn thành & Ngày tạo có giờ phút, không giây.
Đang làm dở: không có.
Bước tiếp theo: user quyết 1 điểm còn treo — dòng đếm dưới bảng vẫn in đuôi "nhiệm vụ"
("Hiển thị 1–4 / 4 nhiệm vụ") vì `V2BaseDataTable` ở nhánh này chưa bỏ `{{ itemLabel }}` (bản `gop_db`
đã bỏ). Sửa được nhưng là component dùng chung của mọi màn danh sách → chờ user đồng ý.
Blocked: không có.

## Phase 8 — Dữ liệu demo + hướng dẫn nghiệm thu (18/09/2026)
- [x] Tạo dữ liệu demo `[DEMO 11456]` trên DB `hrm_prod_6_6`: 4 nhiệm vụ ở dự án **253** (1 có giải pháp · 1 chỉ dự án · 1 nhiệm vụ chung 2 bản ghi · 1 phòng ban thuần)
- [x] Tạo cuộc họp demo **id 152** `TPE.MET.NB.26.0139` — thành phần gồm DNS Admin + Tuân + Duy, 3 dòng biên bản đúng 3 tình huống (1 người · 2 người · chỉ người ngoài), hạn dự kiến đều ở tương lai
- [x] Viết `.plans/task-lien-ket-nhiem-vu/huong-dan-test.md`: 4 nhóm kịch bản A/B/C/D (28 bước), bảng tài khoản kèm số liệu link động thực đo, phần ngoài phạm vi và câu lệnh dọn dữ liệu
- [x] Ghi rõ cảnh báo mở đúng cổng **3000** (cổng 3005 là worktree nhánh `tpe`, không có code task này)

## Phase 9 — Fix nhãn floating bị cắt ở bộ lọc tab Nhiệm vụ (18/09/2026)
- [x] Nhãn floating (vd "Loại nhiệm vụ") **bị cắt cụt** khi ô có giá trị: `.advanced-filters` của `V2BaseFilterPanel` để `overflow: hidden`, mà nhãn nhô lên ~5,5px phía trên viền ô → thêm `.advanced-filters { overflow: visible }` trong `<style scoped>` (không `!important` để animation thu gọn panel vẫn clip đúng)
- [x] Khoảng cách 2 hàng ô lọc: bỏ `mb-2` ở 7 ô, dùng `.filter-grid { row-gap: 18px }` — `mb-2` (8px) làm nhãn hàng dưới chỉ cách viền đáy hàng trên 2,5px, nhìn như dính vào ô trên
- [x] Cách sửa copy từ màn mẫu `pages/assign/prospective-projects/index.vue`
- [x] (user chốt 18/09) Thu `row-gap` **18px → 7px** cho bằng khoảng cách "ô tìm nhanh → hàng lọc đầu"; đo lại: quick→hàng1 = 7px, hàng1→hàng2 = **7px**, nhãn hàng 2 vẫn hiện đủ chữ. Điểm này CỐ Ý khác màn mẫu (18px) — ghi trong design.md
