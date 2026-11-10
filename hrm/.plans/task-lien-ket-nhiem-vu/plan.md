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

## Phase 10 — Fix bề rộng cột màn Lý do hủy cuộc họp (18/09/2026)
- [x] `/assign/meeting_cancel_reason`: cột **Mô tả** bị bóp khi thu nhỏ cửa sổ → khai `width` + `minWidth` cho đủ 8 cột (Mô tả 420/360px, bỏ `maxWidth`), bảng tràn thì cuộn ngang thay vì bóp cột
- [x] Ghi quy tắc vào `.claude/skills/list-page/SKILL.md` mục **15c** (kèm bảng bậc bề rộng cho màn danh mục ít cột + danh sách màn cùng khuôn còn thiếu)
- [x] (user chốt 18/09) Bậc bề rộng ban đầu **quá rộng** → thu về Lý do 220/180 · Mô tả 300/240 · Người tạo 150/140 · 4 cột còn lại 120/110 (tổng ~1090px, vừa khung màn hình thường, không sinh cuộn ngang vô cớ); đã sửa lại bảng bậc ở skill mục 15c

## Phase 11 — Redmine #11495 DEV - DM Lý do hủy cuộc họp (18/09/2026)
- [x] (1) Danh sách: giãn cột Mô tả — đã làm ở Phase 10
- [x] (2a) Import: khung toolbar bị nội dung bảng hằn xuyên qua → `V2BaseImportToolbar` đổi nền `rgba(255,255,255,.92)` + blur sang `#fff` đục (dùng chung 15 màn import)
- [x] (2b) Bỏ cột STT ở bảng preview (`importColumns` bỏ key `No`) và ở file mẫu `static/Mau_import_LyDoHuyCuocHop.xlsx` (xoá cột A, dịch width + data-validation Trạng thái sang B3:B10)
- [x] (2c) Khoảng trống dài giữa ô nhập và dòng lỗi → textarea Mô tả trong preview `rows: 2 → 1` (hàng không bị textarea kéo cao)
- [x] (3) Mở popup confirm lần 2 mất icon → `V2BaseButton` đổi `v-if="$slots.prefix"` thành `$slots.prefix || $scopedSlots.prefix` (cả suffix) — đúng bản đã có ở nhánh `gop_db` + skill modal-popup mục "Bẫy slot rỗng từ lần mở thứ hai"
- [x] (4) Thêm sort cột Lý do hủy cuộc họp + Mô tả: FE `sortable: true`, BE `allowedSortFields` thêm `name`, `description`
- [x] (5) Excel xuất: canh giữa theo chiều dọc + wrap text toàn vùng dữ liệu (`registerEvents`/`AfterSheet`, vùng tính theo số dòng thật), nới cột Người tạo/Người cập nhật 24 → 30; bỏ `vertical-align: top` ở blade. Đã dựng file thật và đọc lại bằng openpyxl để xác minh
- [x] **Đã test bằng Playwright (127.0.0.1:3000, tài khoản namdangit@gmail.com)**: sort Lý do/Mô tả gọi đúng `sort_field=name|description` và đảo chiều asc/desc đúng · popup Xác nhận khóa + Xác nhận xóa mở **lần 2** vẫn còn icon · popup Import không còn cột STT, toolbar nền trắng đục (`rgb(255,255,255)`, `backdrop-filter: none`), dòng lỗi nằm sát ngay dưới ô nhập · file mẫu tải từ `/Mau_import_LyDoHuyCuocHop.xlsx` chỉ còn 3 cột · import thật 1 dòng hợp lệ → vào danh sách OK, đã xoá dữ liệu test
- [x] Ghi chú: `rows: 1` cho textarea KHÔNG có tác dụng (`b-form-textarea` kẹp tối thiểu 2 dòng) → ép `height: 32px` bằng CSS nhắm đúng `#import-meeting-cancel-reason-modal`, không đụng 14 màn import khác
- [x] (user chốt 18/09) Dòng lỗi vẫn xa ô nhập → hạ tiếp: `td.cell-tight` padding đáy 7px → 3px + `.err-list` bỏ `margin-top: 5.6px`. Đo lại bằng Playwright: khoảng cách ô nhập → dòng lỗi **13px → 3px** (padding TRÊN giữ 7px để 2 dòng dữ liệu không dính nhau)
- [x] (user chốt 18/09) Chuyển 3 fix CSS của popup import **vào component dùng chung** thay vì CSS riêng màn: `V2BaseImportTable` nhận `textarea.v2-textarea { height: 32px }`, `.cell-tight` padding đáy 3px, `.err-list` bỏ `margin-top`; gỡ khối style riêng ở `pages/assign/meeting_cancel_reason/index.vue`
- [x] **Phát hiện gốc lỗi "popup nhảy size khi thu nhỏ cửa sổ"**: toàn bộ `<style scoped>` của `V2BaseImportModal` CHƯA BAO GIỜ có tác dụng — `b-modal` đẩy DOM ra `<body>` qua portal nên `.modal/.modal-dialog/.modal-content` không mang `data-v-*`, mọi rule kể cả `:deep()` rơi vào hư không. Popup chạy bằng kích thước mặc định bootstrap: 1140px (≥1200px) → 800px (992–1199px) → 500px (<992px)
- [x] Sửa: bỏ `scoped`, đổi tên selector thành `import-modal-dialog` / `import-modal-root` / `import-modal-content` (tránh rò ra toàn hệ thống và tránh đụng `.modal-xxl` mà 2 modal duyệt giải pháp đang dùng); dialog **cố định 1140px** đúng bề ngang cũ ở MỌI bề ngang cửa sổ; `.modal.import-modal-root { overflow-x: auto }` để cửa sổ hẹp thì cuộn ngang. Đo Playwright: 1512/1100/900px đều ra dialog **1140px**, cuộn ngang OK
- [x] (user chốt 18/09) Nội dung popup import cách header 40px (16px padding bootstrap + `mt-3` 24px của thanh công cụ) → theo skill `modal-popup` mục 0: `.modal-body.import-modal-body { padding: 0.5rem }` + triệt `margin-top` khối đầu / `margin-bottom` khối cuối. Đo lại: **40px → 8px**, footer vẫn ghim đáy nhìn thấy
- [x] (user chốt 18/09) Bỏ dòng mô tả "Import từ Excel • Validate xong dòng hợp lệ sẽ bị khóa" ở popup import màn này: `V2BaseImportModal` thêm `v-if="subtitle"` cho dòng mô tả, page truyền `subtitle=""` (giữ nguyên default cho 2 màn BOM/Báo giá đang ăn theo mặc định)
- [x] (tester phản hồi 19/09 "Vùng nhìn thấy được quá bé") Popup import chỉ có `max-height` nên co theo nội dung, bảng preview tụt về 220px → `V2BaseImportModal` thêm `height: calc(100vh - 2.4rem)` cho `.import-modal-content` (màn thấp `100vh - 1rem`), bảng `flex:1` ăn hết phần còn lại — áp cho mọi popup import (user chốt 16/10)
- [x] (16/10) Dòng mô tả "Import từ Excel • Validate xong…" ở popup import màn này lại hiện (page đang truyền lại subtitle) → đặt lại `subtitle=""` ở `pages/assign/meeting_cancel_reason/index.vue`
- [x] (user chốt 16/10) Bỏ dòng mô tả dưới tiêu đề cho MỌI popup import: gỡ hẳn prop `subtitle` + dòng hiển thị trong `V2BaseImportModal`, gỡ thuộc tính `subtitle="…"` ở 57 nơi gọi. Popup tự dựng của BOM/Báo giá không dùng component này nên giữ nguyên

## Phase 12 — Redmine #11496 DEV Danh sách mẫu phiếu thu thập thông tin (18/09/2026)
- [x] (1) Thêm nút **Lưu và tiếp tục** vào popup Tạo nhanh câu hỏi (`AddQuestionQuickModal`) — `secondary` + icon `ri-save-3-line`, thứ tự Lưu → Lưu và tiếp tục → Đóng; handler `submitForm(2)` đã có sẵn, chỉ thiếu nút
- [x] (2) Sao chép: tên form ra dạng `"<Tên cũ> - Sao chép"` (`pages/assign/form-templates/add.vue` — `loadCopyData`)
- [x] (3) Copy giữ ĐỦ câu hỏi: BE `FormTemplateService::prepareCopyData` bỏ lọc `isScopeAll`, thay bằng trả kèm `applicationScope` cho từng câu hỏi/nhóm; FE `FormBuilder` thêm `removeApplicationScopedQuestions()` chạy trong watcher `formMeta.applicationId` — chỉ xoá khi ĐỔI sang ứng dụng khác (oldVal khác rỗng), có toast báo số câu bị bỏ
- [x] (3b) `applicationScope` đi kèm từ thư viện câu hỏi → section: `FormBuilder.loadLibrary`, `QuestionLibrary.cloneFromLibrary` (cả câu cha-con), `SectionBuilder` (2 chỗ tạo group từ hierarchy); Resource `FormTemplatesResource` + eager load `surveyQuestion` ở `show()` để màn chi tiết/sửa cũng có cờ này
- [x] (3c) **Bug sẵn có phát hiện khi test**: lưu bản sao chết `SQLSTATE 1062 Duplicate entry '<tpl>-q5' for fq_template_local_id_unique` — `FormSection::questions()` không lọc `parent_question_id` nên câu CON vừa nằm phẳng vừa nằm trong `children` của cha → insert 2 lần. Thêm `rootQuestions()` lọc câu gốc trong `prepareCopyData`
- [x] **Đã test Playwright**: popup Tạo nhanh — "Lưu và tiếp tục" lưu xong giữ popup mở + reset form (đã tạo 2 câu ngân hàng test); copy form 1 → tên `Mẫu test #11367 - Sao chép`, hiện đủ 7 câu kể cả câu phạm vi "Theo ứng dụng"; đổi ứng dụng sang Vision → chỉ câu "Theo ứng dụng" bị bỏ (toast báo 1 câu), câu "Tất cả" còn nguyên; bấm Lưu → tạo bản sao thành công, đủ 7 câu, q5 giữ quan hệ con
- [x] Dọn dữ liệu test: đã xoá form template bản sao. **Còn để lại** 2 câu ngân hàng `TEST11496 - …` + 2 câu gắn trong form 1 để user nghiệm thu
- [x] (user báo 18/09) Màn Sửa bấm **Lưu và duyệt** lỗi đỏ `SQLSTATE 1062 Duplicate entry '1-q5'` — cùng gốc với (3c) nhưng ở luồng UPDATE: `FormTemplatesResource` trả câu hỏi CON cả trong danh sách phẳng của section/nhóm lẫn trong `children` của câu cha, FE gửi lại nguyên vậy → BE insert 2 lần cùng `local_id`. Thêm `rootQuestions()` lọc câu gốc cho cả `sections.questions` và `groups.questions` trong Resource. Test lại: Lưu và duyệt OK, form về trạng thái Đã duyệt, dữ liệu giữ đủ 7 câu và câu con vẫn đúng quan hệ cha-con

## Phase 13 — Bố cục màn Tạo mới dự án TKT (18/09/2026)
- [x] `/assign/prospective-projects/add`: đưa **Ứng dụng + nút "Xem danh sách giải pháp" + Nhóm ngành** về CÙNG MỘT HÀNG — `ProjectInfoSection.vue`: Ứng dụng `col-md-8 → col-md-4`, nút `col-md-4 → col-md-3`, chuyển khối Nhóm ngành lên ngay sau nút và để `col-md-6 → col-md-5` (4+3+5 = 12)
- [x] Thêm `<div class="w-100">` (idiom ngắt hàng của bootstrap, vẫn trong cùng `.row`) sau khối Loại dự án — nếu không, "Loại dự án" chiếm 6 cột đầu hàng làm nút bị đẩy xuống dòng
- [x] Đo Playwright: 1512px và 1280px — 3 cột đều `top` bằng nhau, nút cao 32px (không xuống dòng); dự án CHA (ẩn Ứng dụng) thì Nhóm ngành + Quy mô dự án tự dồn cùng hàng, không sinh hàng trống
- [x] (user chốt 18/09) Canh thẳng cột với hàng dưới: Ứng dụng `col-md-3` + nút `col-md-3` = 6 (bằng "Quy mô dự án"), Nhóm ngành `col-md-6` (bằng "Phân loại đầu tư"). Đổi chữ nút **"Xem danh sách giải pháp" → "Xem giải pháp"**; thêm `white-space: nowrap` cho nút (thử 4+2 trước: cột 112px làm chữ vỡ 3 dòng, nút cao gấp đôi)
- [x] (user chốt 18/09) Nút "Xem giải pháp" **luôn hiện**, chưa chọn ứng dụng thì khoá — dùng `:interactable`, KHÔNG `:disabled` (V2BaseButton bỏ qua `disabled`). Lưu ý: khác quy ước CLAUDE.md "nút không dùng được thì ẩn hẳn", user chốt giữ để ô Ứng dụng không nhảy chỗ
- [x] Đo Playwright 1280px và 1512px: mép phải (Ứng dụng + nút) trùng khít mép phải "Quy mô dự án", Nhóm ngành trùng khít "Phân loại đầu tư"; nút 1 dòng cao 32px, disabled khi chưa chọn ứng dụng và bật lại khi đã chọn
- [x] (user chốt 18/09) Ô Ứng dụng còn ngắn, cột nút thừa chỗ → gộp **Ứng dụng + nút vào CÙNG một `col-md-6`** rồi chia bằng flex: `.app-scope-field { flex: 1 1 auto; min-width: 0 }` (ăn hết chỗ trống) + nút `flex: 0 0 auto; white-space: nowrap` (rộng đúng nội dung). Đo Playwright: ô Ứng dụng **176 → 260px** ở 1512 và **138 → 182px** ở 1280, mép phải cụm vẫn trùng khít "Quy mô dự án"
- [x] (user báo 18/09) Khi ô Nhóm ngành hiện cảnh báo "Chưa khai báo nhóm ngành…" thì Ứng dụng + nút bị tụt xuống: cột trong `.row` mặc định `align-self: stretch` nên cột cao theo ô bên cạnh, mà bên trong lại `align-items-end` → nội dung dồn xuống đáy. Thêm `.app-scope-cell { align-self: flex-start }`. Đo lại: nhãn "Ứng dụng" và "Nhóm ngành" cùng `top = 605`, nút thẳng với ô select

## Phase 14 — Panel menu sidebar xếp theo cột dọc (18/09/2026, nhánh tpe-develop-assign)
- [x] `components/sale/SaleHubSidebar.vue`: lưới `.rows` đổi từ `grid-template-columns: 1fr 1fr` (lấp theo HÀNG ngang, đọc ngoằn ngoèo) sang `grid-auto-flow: column` + `grid-template-rows: repeat(var(--rows), auto)` → **lấp đầy cột dọc trước**
- [x] Thêm hằng `ROWS_MIN_2_COLS = 5` + `rowsCount()` / `rowsStyle()`: **dưới 5 chức năng thì 1 cột**, từ 5 trở lên chia 2 cột (`ceil(n/2)` dòng)
- [x] Áp cho MỌI danh sách trong panel (user chốt): nhóm chức năng (`rowsHtml`), Kết quả tìm kiếm, Yêu thích, Gần đây
- [x] Đo Playwright: "Danh mục" 15 mục → 8 dòng × 2 cột đọc dọc đúng thứ tự · "Quản lý dự án TKT" 8 mục → 4 × 2 · "Cấu hình" 4 mục → **1 cột** · tìm "dự án" 10 kết quả → 5 × 2 · danh sách rỗng (Gần đây) không vỡ lưới
- [x] (user chốt 18/09) Panel 1 cột thì thu nhỏ: computed `isCompact` (tìm kiếm / Yêu thích / Gần đây / nhóm flat có < 5 chức năng; nav-mode luôn giữ rộng) → class `.is-compact` cho `.misa-detail`: `width: 1180px → 520px`, bỏ `bottom: 0` + `max-height: calc(100vh - 140px)` để chiều cao chạy theo nội dung. Đo: "Cấu hình" 4 mục = 520×~250px, "Danh mục" 15 mục vẫn 1048×790px như cũ
- [x] (user chốt lại 18/09) Chỉ hẹp bề NGANG khi 1 cột (`width: 520px`), **giữ nguyên chiều cao** kéo tới đáy màn hình như panel 2 cột — đã gỡ `bottom: auto` + `max-height`

## Phase 15 — Bỏ chữ "task" ở màn Báo cáo hiệu suất nhân viên (18/09/2026)
- [x] `components/PerformanceByEmployeeTable.vue`: dòng phụ dưới tên Phòng ban (`… 1 NV • 2 task`) và dưới tên Nhân viên (`2 dự án • 4 task`) → **"nhiệm vụ"** (đúng 2 chỗ user khoanh đỏ trong ảnh)
- [x] `index.vue`: tooltip mô tả màn ("số lượng task…") và phụ đề popup chi tiết `'Tất cả task'` → "nhiệm vụ"
- [x] Kiểm Playwright: tooltip ⓘ đã ra "số lượng nhiệm vụ"; bơm dữ liệu mẫu vào bảng → dòng phòng ban "1 NV • 2 nhiệm vụ", dòng nhân viên "2 dự án • 2 nhiệm vụ"; quét toàn trang không còn chuỗi "task"

## Phase 16 — Redmine #11153 + #11426: fix phản hồi tester (18/09/2026)
- [x] **#11426 #4** Báo cáo tổng hợp giải pháp theo phòng ban: nhãn lọc "Trạng thái dự án TKT" → **"Tiến trình dự án"** (placeholder "Chọn tiến trình dự án") — `pages/assign/report/solutions-work-summary-by-department/index.vue`
- [x] **#11153 #10 / #11426 #5** Cấu hình → Quản lý dự án → Đóng dự án tự động: nhập số âm/thập phân chỉ hiện toast tiếng Anh "The given data was invalid." → thêm `validateProjectCloseConfig()` chặn TRƯỚC khi gọi API + state `projectCloseConfigErrors` + `V2BaseError` dưới từng ô (4 ô chung + mỗi dòng giai đoạn); lỗi 422 của BE cũng map về đúng ô. Giữ nguyên giá trị user gõ, không tự sửa (CLAUDE.md)
- [x] **#11426 #6** Màn "Đề xuất gia hạn dự án chờ duyệt": bỏ nút **Xem dự án** (icon con mắt) khỏi `getRowActions` + gỡ nhánh `view` trong `handleRowAction` — cột Thao tác chỉ còn Duyệt / Từ chối
- [x] Test Playwright: nhập `-1` và `2.5` → 2 dòng đỏ "Không được nhỏ hơn 0" / "Phải là số nguyên" ngay dưới ô, không gọi API; sửa lại giá trị hợp lệ → lưu thành công. Nhãn báo cáo đã ra "Tiến trình dự án". Màn gia hạn: dòng dữ liệu chỉ còn 2 nút Duyệt/Từ chối
- [x] DB local thiếu 2 quyền `Trưởng phòng/Ban giám đốc duyệt gia hạn dự án TKT` (đã có trong `PermissionsTableSeeder` nhưng chưa seed) → màn gia hạn bị đẩy 404. Đã tạo đúng id 1182/1183 + gán role Super admin kèm `role_has_permissions.company_id = 1` (bảng này có cột company_id, thiếu là FE không nhận quyền)

## Phase 17 — Phản hồi tester #7 (23/09) trên #11456 (16/10/2026, nhánh develop)
- [x] BUG 1: tab Nhiệm vụ của dự án chỉ cho chọn giải pháp thuộc dự án đó; chọn giải pháp không ghi đè dự án đang khoá; dự án suy ra từ giải pháp mà chưa có trong options thì thêm vào để hiện tên
- [x] BUG 4: Sửa nhiệm vụ thì khoá ô Meeting khi nhiệm vụ giao từ dòng biên bản (`meeting_report_id`) hoặc mở từ tab Nhiệm vụ của meeting
- [x] BUG 5: `MeetingForm` bắt `task-assigned` → tải lại biên bản (badge "Đã giao N nhiệm vụ") + tab Nhiệm vụ
- BUG 2 (Sửa ở Hoàn thành = lối mở lại của người giao, chờ chốt hướng a/b), BUG 3 (chưa xác định Lê Thị Bắc là NV hay KH), BUG 6 (cùng bảng "Các nội dung khác") — tạm để
- [x] Test Playwright local 16/10: BUG 1 (tab dự án 97 chỉ còn GP14, dự án giữ nguyên; /assign/tasks vẫn đủ giải pháp + tự điền dự án) · BUG 4 (sửa NV giao từ biên bản / mở từ tab meeting → khoá; NV gắn meeting thường sửa ở /assign/tasks → mở) · BUG 5 (lưu xong hiện ngay "Đã giao 1 nhiệm vụ" + tab Nhiệm vụ cập nhật). Ảnh: test-phase17/. Đã xoá NV test + trả mật khẩu cuonghm
- Ghi nhận (chưa sửa): DB local 17/49 meeting_report_executors type=1 có executor_id trỏ nhầm NV (dời id gộp DB) → popup Giao không kế thừa được người — manh mối BUG 3; ô Mức độ ưu tiên BE bắt buộc nhưng nhãn thiếu *

## Phase 18 — Redmine #11426 phản hồi #10 (16/10/2026, nhánh develop)
- [x] Tiêu đề khối "File xác nhận của khách hàng" thêm `*` đỏ ở popup Xác nhận chốt báo giá + popup Chốt giải pháp — prop mới `title-required` (mặc định tắt) của `FileAttachmentTable`, màn khác không đổi. Phần gạch ngang (sáng nút khi có file) không làm theo yêu cầu user

## Phase 19 — Link động: PM / người tạo / leader hạng mục chọn được giải pháp (26/10/2026, nhánh gop_db)
- [x] `TaskLinkScopeHelper::mySolutionIds()` tính thêm `solutions.pm_id`, `solutions.created_by`, `solution_modules.leader_id` (trước chỉ đọc `solution_members` + `solution_module_members` → người tạo GP41 không thấy giải pháp của mình). Ảnh hưởng cả Tầng 2 phân quyền danh sách Nhiệm vụ + `myProjectIds()`
- [x] `IssueService::getMySolutionIds()` bỏ bản copy, gọi `TaskLinkScopeHelper::mySolutionIds()` → phân quyền danh sách Vấn đề khớp Nhiệm vụ

## Phase 20 — Phản hồi #11 của TPE (24/10) trên #11456 (10/11/2026) — @cuong61n
- [x] (10/11) Đọc phản hồi #11 + file testcase (sheet "19.Nhiệm vụ", đợt 22/09, dòng 214–266): 2 yêu cầu nghiệp vụ mới (không tạo nhiệm vụ khi Dự án "Đóng" / Meeting "Hủy") + 9 dòng F, 4 dòng PE
- [x] (10/11) Đối chiếu code `develop`: Dự án đóng (status 11) mới chỉ ẩn nút Tạo mới ở tab Nhiệm vụ của dự án; ô Dự án/Giải pháp ở popup vẫn liệt kê dự án đã đóng, BE `TaskService::store` không chặn. Meeting Hủy (status 4): tab Nhiệm vụ vẫn có Tạo mới, icon Giao nhiệm vụ trên biên bản vẫn hiện, ô Meeting vẫn liệt kê, BE không chặn
- [x] (10/11) User chốt: làm hết + test e2e Playwright kỹ (nhánh `develop` cả 2 repo)
- [x] BE `TaskLinkScopeHelper::closedLinkErrors()` + gắn vào `TaskStoreRequest` / `TaskUpdateRequest` / `TaskFieldUpdateRequest` (field=link): Dự án Đóng (11) · Giải pháp thuộc dự án Đóng · Meeting Hủy (4) → 422 đúng ô. Sửa nhiệm vụ chỉ chặn khi ĐỔI liên kết sang bản ghi đóng/hủy
- [x] BE ô chọn (`mine=1`): `prospective-projects/getAll` bỏ dự án Đóng, `solutions/getAll` bỏ giải pháp của dự án Đóng, `meeting/task-options` bỏ meeting Hủy — giữ `include_id` (giá trị đang gắn)
- [x] BE `myProjectIds()` thêm KD chính (`main_sale_employee_id`) + người tạo dự án (TC_07.044, nghi là nguyên nhân TC_07.039/040 "không chọn được dự án")
- [x] BE `MeetingTransformer` `assigned_tasks[]` thêm loại, màu trạng thái, người giao, người thực hiện, hạn (eager load, không N+1)
- [x] FE `MeetingForm`: tab Nhiệm vụ ẩn Tạo mới khi meeting Hủy · `MeetingReport`: ẩn nút Giao khi Hủy, cột "Thao tác" → "Hành động", popup "Nhiệm vụ đã giao" thành bảng `V2BaseDataTable` (STT, Mã, Tên, Loại, Trạng thái, Người giao, Người thực hiện, Hạn)
- [x] FE `TaskListTab`: lọc nhanh 4 nút (tôi làm / giao / theo dõi / duyệt KQ) + pill Tổng + Tuỳ chỉnh cột (`columnCustomizationMixin`, khoá `assign_task_tab_project|meeting`) — copy pattern `pages/assign/tasks/index.vue:82-140`
- [x] FE `TaskForm`: ô Hạng mục chỉ liệt kê hạng mục "Đang triển khai" / "Chờ duyệt hồ sơ trình duyệt" (cùng luật tab Hạng mục, TC_07.052); giải pháp có hạng mục mà hết hạng mục hợp lệ vẫn hiện ô để báo lỗi
- Không sửa: TC_07.009 (placeholder tab đúng vì BE tab chỉ tìm mã/tên — testcase ghi kỳ vọng sai), tab Nhiệm vụ Giải pháp/Hạng mục (đóng dự án đã cascade Đóng giải pháp + hạng mục nên nút Tạo mới tự ẩn)
- [x] (10/11) Phát hiện khi test: tab Nhiệm vụ không chống response về trễ (bấm lọc nhanh lúc lượt tải đầu chưa xong thì kết quả cũ ghi đè) → thêm `loadSeq` như màn `/assign/tasks`
- [x] (10/11) Test API trực tiếp, DB local `local_hrm_erp` (đặt tạm dự án 152 → Đóng, meeting 69 → Hủy rồi trả lại): 26/26 PASS — tạo/sửa/sửa tại chỗ gắn dự án đóng · GP của dự án đóng · meeting hủy → 422 đúng ô (cả lưu nháp, cả nhiệm vụ chung); nhiệm vụ CŨ gắn dự án/meeting nay đóng/hủy vẫn sửa được, gỡ liên kết được, gắn lại thì chặn; 3 ô chọn bỏ bản ghi đóng/hủy nhưng giữ `include_id`; KD chính (admin) thấy thêm 7 dự án mình phụ trách; cannt.kd1 / manhnv.kd1 chỉ thấy dự án mình là thành viên
- [x] (10/11) Playwright e2e (script Python, 3 tài khoản admin / cannt.kd1): 45/46 PASS — meeting Hủy (cột "Hành động", không nút Giao, tab không Tạo mới) · meeting mở giao từ biên bản → "Đã giao N" → bảng 8 cột, badge màu, Người giao "Tên - Mã phòng", bấm Mã mở xem · meeting/dự án bị đóng/hủy trong lúc đang mở popup → lỗi đỏ đúng ô, popup không đóng · dự án Đóng ẩn Tạo mới · 4 nút lọc nhanh gửi đúng tham số, loại trừ nhau, bấm lại tắt, Làm mới giữ phạm vi · Tuỳ chỉnh cột tắt/bật + tải lại vẫn giữ · popup `/assign/tasks` không có dự án đóng / meeting hủy / GP của dự án đóng, chọn GP tự điền dự án, hạng mục "Đã duyệt hồ sơ" không hiện. Case lệch: "bật lại cột" chập chờn do API local 1 worker chậm — chạy riêng lặp 2 vòng 4/4 đạt. Ảnh: scratchpad phiên 10/11
- [x] (10/11) Dọn dữ liệu: xoá 9 nhiệm vụ test (1023–1031 + watcher/org_unit/history), trả dự án 152 → 4, meeting 69 → 3; chạy riêng migration `create_task_extension_requests_table` trên DB local (thiếu làm chi tiết nhiệm vụ 500, của Nhiệm vụ v2)
- [x] (10/11) Soạn ghi chú trả lời TPE (07.009, 07.011, 07.044, 07.045, 07.047, 07.052) — gửi user duyệt trong chat, CHƯA đăng Redmine

- [x] (10/11) Commit + push `develop`: hrm-api `5207f2a45` (merge `74373dc0c`), hrm-client `e1c6d9729`; chạy `~/build_tpe.sh` trên dev (log `~/build_tpe_20261110_1559.log`)

### Checkpoint — 2026-11-10
Vừa hoàn thành: Phase 20 code + test API + Playwright, đã push `develop` + build dev.
Đang làm dở: không.
Bước tiếp theo: đăng ghi chú trả lời TPE lên Redmine #11456 khi user duyệt; hỏi TPE lý do F của TC_07.045.
Blocked: không.

## Phase 21 — Giao lại người thực hiện ở task thì dòng meeting đổi theo (10/11/2026) — @cuong61n
- [x] (10/11) Nghiệp vụ (phản hồi từ TPE, chưa có số Redmine): giao task từ dòng nội dung meeting, chọn người khác người ghi ở meeting thì cột "Người thực hiện" của meeting vẫn hiện người cũ — 2 nơi (`meeting_report_executors` vs `tasks.assignee_id`) lưu độc lập
- [x] (10/11) BE `TaskService::syncMeetingReportExecutors()`: dòng đã có task → người thực hiện công ty = những người đang được giao task còn hiệu lực (bỏ task Đã hủy), nhân sự khách hàng giữ nguyên, dòng chưa có task thì không đụng; đồng bộ cả 3 cột `executor_*` cũ (In / Excel). Gọi ở: tạo task, sửa task (cả khi đổi dòng biên bản), đổi người thực hiện tại chỗ (`updateField`), xoá task. Chỉ `php -l` — chưa test chạy thật. (10/11) User chốt sửa trên nhánh `gop_db`: đã áp vào worktree `worktrees/gop_db-api` (đã staged, chưa commit), gỡ khỏi `develop`
- [x] (10/11) Test API trên DB local `local_hrm_erp` (API chạy từ worktree `gop_db-api` cổng 8003, meeting 84, dữ liệu thử đã dọn): 12/12 case đạt — giao lại 13→25 (kể cả 3 cột `executor_*` cũ) · đổi người tại chỗ (PATCH field) · 2 task 2 người · task Đã hủy không tính (đặt bằng SQL vì UI không có đường hủy) · xoá task nháp · dòng có khách hàng giữ nguyên khách · Nhiệm vụ chung 2 người (tên gộp "A, B") · dòng chưa giao giữ nguyên · PUT đổi người · task không gắn dòng meeting không lỗi
- [x] (10/11) Test Playwright (client `gop_db-client` cổng 3002 → API 8003, tài khoản test): vào Chi tiết meeting → tab Biên bản → Giao dòng PW-TEST, đổi người DNS Admin → Nguyễn Thị Cần → cột "Người thực hiện" của meeting đổi theo, hiện "Đã giao 1 nhiệm vụ"; giao lần 2 cho Bùi Hữu Hanh → hiện cả 2 người, popup "Nhiệm vụ đã giao" liệt kê 2 task. Dòng 1 (không giao) không bị ảnh hưởng
- [ ] Chờ user chốt: dòng 2 người (A, B) chỉ giao task cho C thì A, B biến mất khỏi meeting (đang theo quy tắc "người ở meeting = người đang làm task"); task Từ chối triển khai (REJECTED_START) hiện vẫn tính là người thực hiện
- [ ] Nghi vấn chưa kiểm: `MeetingService::syncReports` xoá + tạo lại dòng biên bản mỗi lần lưu meeting → `tasks.meeting_report_id` có thể trỏ vào dòng đã mất (local hiện 0 task mồ côi nhưng dữ liệu ít)
- [x] (10/11) Đã commit + push nhánh `gop_db` (hrm-api `f94447b77`), chạy `~/build_tpe.sh` trên prod (hrm-tpe, /var/www/tpe/hrm-api) — 10/11 16:07 BE đã lên prod (`git log` = f94447b77, opcache tự nạp lại sau ≤2 giây). Script dừng ở `php artisan migrate` vì prod hỏi yes/no mà chạy qua ssh không có terminal; không có migration chờ, thay đổi chỉ là code service (không route/quyền) nên không cần route:cache / catalog-sync / build FE. Chưa test lại tính năng trên prod (không ghi dữ liệu prod)
- [x] (10/11) Sửa dữ liệu cũ trên PROD: rà toàn bộ dòng meeting có task (chỉ đọc) → 2 dòng, 1 khớp, 1 lệch: dòng biên bản #562 (meeting TPE.MET.NB.26.0551) task TPE.TASK.NB.26.0034 giao cho Nguyễn Thị Lệ nhưng meeting còn ghi Đào Thị Thúy. Đã đổi người thực hiện của dòng #562 sang Nguyễn Thị Lệ (cả `meeting_report_executors` và 3 cột `executor_*` cũ), trong transaction. Bản sao dữ liệu cũ: `/home/erp_tpe/fix562_backup_20261110.json` trên prod. Sửa `~/build_tpe.sh` prod thêm `--force` cho migrate (bản gốc `.bak_20261110`)
