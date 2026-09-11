# Plan — Chuẩn hoá màn Danh sách task theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-task-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `Task::STATUS` — **5/10 mã màu** lệch bảng 9 mã chuẩn, quy về đúng nhóm:
      Nháp `#94a3b8` → `#64748B` · Hoàn thành-Chờ duyệt `#7c3aed` → `#D97706` ·
      Từ chối kết quả `#ef4444` → `#DC2626` · Huỷ `#0f172a` → `#6B7280` ·
      Từ chối triển khai `#f43f5e` → `#DC2626` (5 mã còn lại chỉ viết hoa cho đồng bộ)
- [x] 1.2 `Task::PRIORITIES` — thang màu ưu tiên RIÊNG (Bình thường `#94A3B8` · Cao `#F97316` ·
      Khẩn cấp `#DC2626`) + 4 hàm `resolveStatusName/Color`, `resolvePriorityName/Color`
- [x] 1.3 `TaskResource` — thêm `status_color`, `priority_name`, `priority_color`,
      `deadline_state_text` + `deadline_state_color`; `created_at`/`updated_at` format `d/m/Y H:i`
      (trước còn giây); `due_time` cắt giây ngay ở BE; `updated_by_name` bỏ tiền tố mã nhân viên
      (`employee_update_name` của BaseModel ghép "MÃ NV - Họ tên", lệch kiểu với 4 cột người khác)
- [x] 1.4 `TaskResource` — bỏ N+1: 3 chỗ `Employee::find(...)->info->fullname` → đọc qua quan hệ
      + `optional()`; bỏ `->load('priorityLevel')` chạy trên từng dòng (phá luôn eager load)
- [x] 1.5 `Task::canEdit()/canDelete()` — nhớ kết quả `subtasks` (2 truy vấn/dòng → 0 khi đã eager
      load); `canStartApprove()` xét TRẠNG THÁI trước rồi mới hỏi quyền + nhớ quyền/phòng ban quản lý
- [x] 1.6 `TaskService` — whitelist `SORTABLE_COLUMNS` (12 khoá) + chốt `id desc`.
      ⚠️ Bản cũ `orderBy($request->sort_field, $request->sort_dir)` nhận thẳng chuỗi từ URL
- [x] 1.7 `TaskController` — hằng `LIST_RELATIONS` (15 quan hệ) dùng chung cho `index()` và
      `export()`; `index()` trước để trống hoàn toàn
- [x] 1.8 `ExportColumnRegistry::COLUMNS['tasks']` — 27 cột (+ khoá ảo `tags_text` ghép tên tag)
- [x] 1.9 `export()` — `DynamicExport` + registry thay `TaskExport` blade 13 cột cứng; `.xls` → `.xlsx`
- [x] 1.10 Hiệu năng: **325 → 67 truy vấn / 10 dòng**

## Phase 2 — Frontend (`pages/assign/tasks/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (15 mục / 17 ô); nhóm tổ chức và
      Tag render bằng slot; cascade Giải pháp → Dự án / Hạng mục / Version giữ nguyên
- [x] 2.2 Tách ô gộp `taskInfo` (mã + tên + 3 dòng phụ + chip tag + 6 icon) → `taskCode`
      (button mở popup Xem, sticky, locked) + `taskName` + `tags` + 4 cột người/ngày riêng
- [x] 2.3 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa chính, Nhập kết quả · Duyệt ·
      Lịch sử vào `⋮`; bỏ "Xem"
- [x] 2.4 Bỏ 4 hàm tô màu tự chế (`getTaskStatusLabel`, `getTaskStatusStyle`,
      `getPriorityLevelStyle`, `hexToRgb`) + `.priority-pill` → `V2BaseBadge` với màu BE trả
- [x] 2.5 Thêm cột **Tình trạng hạn** (trước là dòng phụ dựng bằng chuỗi HTML `isHtml: true` bên
      trong `V2BaseTitleSubInfo`), **Tag**, **Ngày tạo**, **Người cập nhật**, **Ngày cập nhật**
- [x] 2.6 Ghép "MÃ - Tên" của Giải pháp / Dự án vào 1 dòng; PM dự án xuống dòng phụ `v2-hint`
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ 22 cột theo 4 bậc; bỏ đoạn tự gán
      `sticky: index < 3` (cột kéo đi đâu cũng ghim → offset `left` tính sai)
- [x] 2.8 Chuyển khối lọc nhanh + 2 số tổng từ slot `toolbar` sang `left-actions` — **màn đang mất
      tiêu đề bảng** vì `toolbar` thay thế cả khối tiêu đề
- [x] 2.9 `columnCustomizationMixin` thay logic merge tự viết (bản cũ trả thẳng cấu hình đã lưu →
      mất hết `width`/`align`/`sortable` khai trong code)
- [x] 2.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — lần đầu có popup chọn cột
      xuất file ở màn này; đổi `buildQueryString` → `buildQuery` cho URL xuất file
      (**lọc nhiều tag trước đây chỉ gửi được tag cuối**)
- [x] 2.11 Thêm `loadSeq` + `suppressFilterWatch`; `handleSort`/`setScope`/`clearScope` chỉ đổi
      `filters` (deep watcher lo gọi API) thay vì gọi thẳng; `loadData()` là request ĐẦU TIÊN
      (bản cũ chờ `getFields()` + 2 dropdown `per_page=10000` xong mới nạp danh sách)
- [x] 2.12 Xoá ~450 dòng code chết: tìm khách hàng (input + dropdown + listener document),
      `getNameScale`, `getStatusLabel`, `getProgressClass`, `getNameInvestmentType`,
      `getNameFundingSource`, `formatDate`, `viewMeetings`, `createProject`, `isSoonDue`,
      `departmentOptions`, `salesOptions` — không nơi nào gọi
- [x] 2.13 Bỏ sạch `'—'` / `.text-muted` / `font-weight-bold` trong ô; màu chữ theo 3 mức của
      skill mục 3b-2b

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK
- [x] 3.2 Đối chiếu tự động: 22/22 cột đủ `width` = `minWidth`, có slot render, map được sang cột
      xuất file; `exportFields` FE ↔ registry BE **27 = 27, cùng thứ tự**; 0 chỗ
      `'—'`/`'N/A'`/`.text-muted`/`v-html`/`.status-pill`
- [x] 3.3 Smoke test trên **14 task thật**: index 200 / **67 truy vấn** (trước 325); trả đủ
      `status_color`, `priority_name`+`priority_color`, `deadline_state_*`, `updated_by_name`
      (bỏ tiền tố mã NV), `due_time` = `17:00`, `created_at` = `27/07/2026 11:41`;
      4 trạng thái trong dữ liệu ra đúng bảng chuẩn (Chờ bắt đầu `#64748B` · Đang thực hiện
      `#2563EB` · Hoàn thành-Chờ duyệt `#D97706` · Hoàn thành `#16A34A`), 3 mức ưu tiên đúng thang
      riêng; 4 khoá sort đổi đúng thứ tự + key lạ về mặc định; lọc `status` / `priority` /
      `tags[]` đều ăn; export .xlsx **21 dòng = 14 dữ liệu + 7 dòng khung**, 28 cột,
      `fields=` lọc còn 5 cột theo đúng thứ tự user tick
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn `/assign/tasks/daily-report` (báo cáo tiến độ hằng ngày) — chưa đụng.
- 3 popup `CreateTaskModal` / `ImportResultModal` / `TaskHistoryModal` giữ nguyên.
- `TaskExport` + blade `exports/tasks.blade.php` không còn được `export()` gọi nhưng vẫn để lại.
- `TaskResource` còn dùng ở `MyJobController` / báo cáo → hưởng lây khoá mới + định dạng ngày.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (10 việc BE) + Phase 2 (13 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/tasks` (task 3.4).
Blocked: không.
