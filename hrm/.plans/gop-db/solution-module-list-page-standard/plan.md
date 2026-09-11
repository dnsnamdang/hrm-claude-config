# Plan — Chuẩn hoá màn Danh sách hạng mục dự án theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-solution-module-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `SolutionModule::STATUSES` — 2 mã màu lệch bảng 9 mã chuẩn: "Chờ duyệt hồ sơ trình duyệt"
      `#F59E0B` → **`#D97706`** (nhóm Chờ xử lý; `#F59E0B` là nhóm Cảnh báo, khác nghĩa),
      "Đã duyệt hồ sơ trình duyệt" `#10B981` → **`#16A34A`**.
      ("Chưa duyệt" và "Đóng" giữ `#6B7280` — đúng bảng, nhóm Đã đóng – Không áp dụng)
- [x] 1.2 `SolutionModuleService::index()` — whitelist `SORTABLE_COLUMNS` + `applySort()` chốt
      `id desc` (trước là `orderBy($request->sort_field ?? ...)` trần)
- [x] 1.3 `SolutionModuleService::index()` — eager load `employee_create.info` / `employee_update.info`
- [x] 1.4 `SolutionModuleListResource` — trả `creator_name`, `updater_name`, `updated_at`;
      tên chỉ lấy `fullname` (accessor dùng chung của `BaseModel` ghép "mã - tên")
- [x] 1.5 `ExportColumnRegistry::COLUMNS['solution_modules']` — 13 cột
- [x] 1.6 Route + `export()` mới (`DynamicExport` + `resolve()`), đặt TRƯỚC route
      `/{solutionModule}` kẻo bị nuốt thành id

## Phase 2 — Frontend (`pages/assign/solution-modules/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`; nhóm Công ty/Phòng ban/Bộ phận
      khai thành MỘT field `org`
- [x] 2.2 `ignoredFields` thành computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột gộp `solutionModuleInfo` → `moduleCode` (link `.v2-cell-link` vào màn quản lý)
      + `moduleName`; gỡ 3 icon thao tác khỏi ô
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions` (Sửa · Lưu và duyệt, cả 2 khai `to`);
      **bỏ hành động "Quản lý"** — trùng với link ở cột Mã
- [x] 2.5 Ô "Dự án (giải pháp)" ghép `MÃ - Tên` cùng 1 dòng
- [x] 2.6 Thêm 4 cột Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 13 cột theo 4 bậc (Mã hạng mục lấy
      bậc L 260px vì mã dài tới 35 ký tự)
- [x] 2.8 `columnCustomizationMixin` — màn này **chưa từng có** popup Cấu hình cột
- [x] 2.9 **Thêm nút Xuất Excel** + `exportFieldsMixin` + `ExportFieldsModal` + `runExport()`
- [x] 2.10 `created()`: `loadData()` bắn ĐẦU TIÊN. Bản cũ `await loadFilterOptions()` trước —
      hàm đó tải `assign/solutions/getAll?per_page=10000`, tức là bảng chờ một request 10.000 dòng
      mới bắt đầu tải, chỉ để đổ options cho 1 ô lọc trong panel đang thu gọn.
      Nay options hoãn tới khi mở panel, `per_page` hạ 10.000 → 1.000
- [x] 2.11 Thêm `loadSeq`; `handleSort` chỉ đổi `filters` (trước vừa gọi `loadData` vừa để watcher
      bắn → 2 request); `handleReset` cũng hết gọi 2 lần
- [x] 2.12 Bỏ `'—'` trong ô; bỏ `font-weight-bold`; màu chữ theo màn mẫu `/assign/customers`
- [x] 2.13 Bỏ `@row-click` điều hướng — cột Mã đã là link, giữ cả hai thì bấm nhầm vào ô bất kỳ
      cũng nhảy trang

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC — OK
- [x] 3.2 Đối chiếu tự động: 13/13 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **13 = 13, cùng thứ tự**
- [x] 3.3 Smoke test API trên dữ liệu thật (5 hạng mục): index 200, trả đủ `creator_name` /
      `updater_name` / `updated_at`, `status_color` đúng bảng chuẩn; export ra .xlsx
      **10 dòng = 3 dữ liệu + 7 dòng khung**; `fields=` lọc đúng, key lạ bị loại
- [x] 3.4 Sắp xếp kiểm bằng tài khoản thấy 3 dòng: `moduleCode` asc → HM01/HM02/HM03,
      `moduleName` asc → thứ tự KHÁC (đúng là sắp theo tên), key lạ → về mặc định `created_at desc`
- [ ] 3.5 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Hành động **"Lịch sử"** — module Assign chưa có `LogsCatalogHistory`.
- ⚠️ **Không tài khoản nào đang có 4 quyền "Xem danh sách hạng mục dự án theo tổng công ty / công ty
  / phòng ban / bộ phận"** (kiểm bằng SQL). Mọi người hiện chỉ thấy hạng mục mình liên quan
  (leader / thành viên / PM / người tạo). Không phải lỗi của đợt này, nhưng nếu nghiệp vụ cần thì
  phải gán quyền cho vai trò tương ứng.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (6 việc BE) + Phase 2 (13 việc FE) + 3.1→3.4.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/solution-modules` (task 3.5).
Blocked: không.
