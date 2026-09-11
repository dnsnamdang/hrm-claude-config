# Plan — Chuẩn hoá màn Danh sách yêu cầu làm giải pháp theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-request-solution-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `RequestSolution::STATUSES` — 5 mã màu lệch bảng 9 mã chuẩn quy về đúng nhóm:
      Yêu cầu bổ sung `#DC2626` → **`#F59E0B`** (đỏ là ngôn ngữ của từ chối, không phải "cần bổ sung"),
      Từ chối `#B91C1C` → `#DC2626`, Đang thực hiện `#0891B2` → `#2563EB`,
      Đã hủy `#9CA3AF` → `#6B7280`, Đã chốt giải pháp `#4F46E5` → `#7C3AED`
- [x] 1.2 `RequestSolution` — thêm quan hệ `receiveDepartment()` · `receiver()` · `solution()`;
      thêm `isCanEdit()` / `isCanDelete()` (khớp guard controller, siết thêm quyền sở hữu)
- [x] 1.3 `RequestSolutionService::index()` — whitelist `SORTABLE_COLUMNS` + `applySort()` chốt
      `id desc` (trước là `orderBy($request->sort_field)` trần)
- [x] 1.4 `RequestSolutionService::index()` — eager load đủ quan hệ Resource đọc tới
- [x] 1.5 `RequestSolutionResource` — trả `solution_code` / `solution_pm_name` / `solution_pm_phone`
      (**2 cột trên bảng vốn in cứng dấu gạch**), `is_can_edit`, `is_can_delete`
- [x] 1.6 `RequestSolutionResource` — Người tạo/cập nhật chỉ còn **TÊN** (accessor dùng chung của
      `BaseModel` ghép "mã - tên"); ngày `d/m/Y H:i` (trước hiện cả giây)
- [x] 1.7 `ExportColumnRegistry::COLUMNS['request_solutions']` — 24 cột; `export()` chuyển
      `DynamicExport` + `resolve()`, `.xls` → `.xlsx`

## Phase 2 — Hiệu năng (đo bằng số, không đoán)

- [x] 2.1 Resource gọi `ProspectiveProject::find()` + `Department::find()` + `Employee::find()`
      cho TỪNG DÒNG → đọc qua quan hệ đã eager load
- [x] 2.2 `$project->projectPhases->load('priorityLevel')` gọi mỗi dòng dù service đã eager load
      → bỏ `->load()`
- [x] 2.3 `isCanReceive()` (chạy qua `is_can_reject` / `is_can_cancel`) gọi
      `isCurrentEmployeeHasPermission()` + `Solution::departmentsManager()` MỖI DÒNG → cache static
      trong request
- [x] 2.4 `isCanDelete()` dùng quan hệ `solution` đã nạp thay vì `->exists()` mỗi dòng
- [x] 2.5 Kết quả đo trên 10 dòng: **115 → 54 truy vấn**, **5,4s → 0,28s**

## Phase 3 — Frontend (`pages/assign/request-solution/index.vue`)

- [x] 3.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`; nhóm Công ty/Phòng ban/Bộ phận
      khai thành MỘT field `org`; Giai đoạn dự án dùng slot (`ProjectPhaseSelect` có icon Info)
- [x] 3.2 `ignoredFields` thành computed dùng `textFilterKeys()`
- [x] 3.3 Tách cột gộp `request` → `requestCode` (link `.v2-cell-link`) + `requestTitle`
      (kèm dòng hạn xử lý màu do BE tính); gỡ 4 icon thao tác khỏi ô
- [x] 3.4 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa · Làm giải pháp · Hủy yêu cầu;
      bỏ hành động "Xem"
- [x] 3.5 Ô tham chiếu (Dự án TKT, Khách hàng) ghép `MÃ - Tên` cùng 1 dòng
- [x] 3.6 **2 cột "Mã GP" / "PM làm GP"** render dữ liệu thật (Mã GP là link sang màn giải pháp)
- [x] 3.7 Thêm 4 cột Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật
- [x] 3.8 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 22 cột theo 4 bậc
- [x] 3.9 `columnCustomizationMixin` thay logic merge tự viết (bản cũ trả thẳng cấu hình đã lưu →
      mất hết `width`/`align`/`sortable` khai trong code)
- [x] 3.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` dùng `downloadExcel` và
      `$safeLoadingStart/Finish`; nút Xuất màu `success`, khoá bằng `:interactable`
- [x] 3.11 `created()`: `loadData()` bắn đầu tiên (trước `await getFields()` chặn); thêm `loadSeq`;
      `handleSort` chỉ đổi `filters` (trước vừa gọi `loadData` vừa để watcher bắn → 2 request);
      `handleReset` cũng hết gọi 2 lần
- [x] 3.12 Bỏ `'—'` trong ô; màu chữ theo màn mẫu `/assign/customers`; dòng phụ dùng `v2-hint`;
      xoá hàm chết `deleteOne()` (dùng `confirm()` trình duyệt + toast giả "(demo)") và khối
      `summary` + CSS `.due-pill` không còn ai gọi

## Phase 4 — Kiểm chứng

- [x] 4.1 Compile SFC — OK
- [x] 4.2 Đối chiếu tự động: 22/22 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **24 = 24, cùng thứ tự**
- [x] 4.3 Smoke test API trên **18 yêu cầu thật**: index 200; trả đủ `solution_code` /
      `solution_pm_name` / Người tạo chỉ còn tên / ngày không còn giây; 4 khoá sort đổi đúng thứ tự
      + key lạ rơi về mặc định; export ra .xlsx **25 dòng = 18 dữ liệu + 7 dòng khung**;
      `fields=` lọc đúng, key lạ bị loại
- [x] 4.4 Kiểm cờ quyền 2 chiều trên phiếu **nháp**: chính chủ → sửa/xoá/huỷ = true;
      người khác → tất cả false (fail-closed)
- [ ] 4.5 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Hành động **"Lịch sử"** — module Assign chưa có `LogsCatalogHistory`.
- Màn `/assign/request-solution/pending` (danh sách chờ tiếp nhận) dùng chung Resource nên **hưởng
  lây** phần sửa màu + tên người tạo + 2 trường giải pháp, nhưng **giao diện chưa chuẩn hoá**.
- Accessor `employee_create_name` / `employee_update_name` của `BaseModel` vẫn ghép "mã - tên";
  đây là hàm dùng chung nên chỉ né ở Resource của màn này, không sửa (CLAUDE.md).

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (5 việc hiệu năng) + Phase 3 (12 việc FE) + 4.1→4.4.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/request-solution` (task 4.5).
Blocked: không.
