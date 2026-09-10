# Plan — Chuẩn hoá màn Danh sách meeting theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-meeting-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `Meeting` — thêm `STATUS_COLORS` (5 trạng thái quy về bảng 9 mã màu chuẩn), hằng
      `MODES` (Trực tiếp `#64748B` · Online `#7C3AED`) và 2 hàm `resolveStatusName()` /
      `resolveStatusColor()`. Trước đây `STATUS` chỉ có `color_by_project = 'text-brand'`
      (tên class CSS), không dùng được cho badge
- [x] 1.2 `MeetingResource` — thêm `status_name`, `status_color`, `mode_name`, `mode_color`,
      `updater_name`, `has_minutes`; `created_at`/`updated_at` format `d/m/Y H:i` (bỏ giây);
      null-guard `creator` bằng `optional()` (meeting của nhân viên đã xoá quan hệ gây 500)
- [x] 1.3 `MeetingController::index()` — **sửa lỗi biến `$sortMapping` KHÔNG tồn tại**, thay bằng
      whitelist `SORTABLE_COLUMNS` (9 khoá) + chốt `orderByDesc('id')`
- [x] 1.4 `MeetingCriteria` — **bỏ khối sắp xếp**: criteria chạy trước nên `orderByDesc('updated_at')`
      ở đây luôn thắng, mọi `orderBy` của controller chỉ là khoá phụ (bấm sort cột Tên/Mã không ăn)
- [x] 1.5 `ExportColumnRegistry::COLUMNS['meetings']` — 21 cột
- [x] 1.6 `export()` — chuyển sang `MeetingResource::collection()->resolve()` + `DynamicExport` +
      registry (chọn cột động), tự sắp xếp như `index()`, đổi tên file `.xls` → `.xlsx`
- [x] 1.7 Hiệu năng: eager load 8 quan hệ ở `index()` + bỏ `TpCustomer::find(null)` khi meeting
      không gắn khách hàng → **175 → 70 truy vấn / 10 dòng**

## Phase 2 — Frontend (`pages/assign/meeting/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (11 mục / 13 ô); nhóm tổ chức,
      Loại meeting, 2 ô ngày render bằng slot
- [x] 2.2 Tắt ô **Nhân viên** của `V2BaseCompanyDepartmentFilter` (ghi vào `employee_id` mà BE
      không đọc → ô lọc chết); thêm ô **Người tạo** (`created_by`) đúng khoá BE xử lý
- [x] 2.3 `initialStateForm`: `company_name` → `company_id` (khoá component thật sự ghi vào — bản
      cũ bấm "Làm mới" không xoá được ô Công ty)
- [x] 2.4 Nhãn `statusOptions` đồng bộ `Meeting::STATUS` (ô lọc và badge trước đây gọi tên khác nhau)
- [x] 2.5 Tách ô gộp `meetingInfo` (mã + tên + 3 dòng phụ + 6 icon) → `meetingCode` (link, sticky,
      locked) + `meetingName` + 4 cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật
- [x] 2.6 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa chính, In biên bản · Tạo phiếu
      công tác khác · Lịch sử vào `⋮`; bỏ "Xem"
- [x] 2.7 Bỏ toàn bộ `v-html` + 4 hàm dựng HTML (`renderStatus`/`renderMode`/`renderType`/
      `renderMinutes`) và listener `document.addEventListener('click')` → `V2BaseBadge` + `<button>`
- [x] 2.8 Tách `typeMode` thành 2 cột Loại meeting / Hình thức; thêm cột **Địa điểm** (37/40 dòng
      có dữ liệu, đã có sẵn trong file xuất)
- [x] 2.9 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ 18 cột theo 4 bậc
- [x] 2.10 `columnCustomizationMixin` thay logic merge tự viết; `exportFieldsMixin` +
      `ExportFieldsModal` + `runExport()` (lần đầu có popup chọn trường xuất file ở màn này)
- [x] 2.11 Thêm `loadSeq` + `suppressFilterWatch`; `handleSort` chỉ đổi `filters` (deep watcher lo
      gọi API) thay vì gọi thẳng; `loadData()` là request ĐẦU TIÊN (bản cũ chờ `getFields()` và
      `loadFilterOptions()` — trong đó có `customers/search?limit=20000` — xong mới nạp danh sách)
- [x] 2.12 Bỏ sạch `'—'` / `'N/A'` / `.text-muted` / `font-weight-bold` trong ô; màu chữ theo
      3 mức của skill mục 3b-2b

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK
- [x] 3.2 Đối chiếu tự động: 18/18 cột đủ `width` = `minWidth`, có slot render, map được sang cột
      xuất file; `exportFields` FE ↔ registry BE **21 = 21, cùng thứ tự**; 0 chỗ
      `'—'`/`'N/A'`/`.text-muted`/`v-html`/`status-pill`
- [x] 3.3 Smoke test trên **37 meeting thật** (gọi thẳng controller): index 200 / 70 query;
      trả đủ `status_name`+`status_color`, `mode_name`+`mode_color`, `updater_name`, `has_minutes`,
      `duration_minutes` (11:00–17:30 = 390 phút), `created_at` = `27/07/2026 10:25`;
      4 trạng thái trong dữ liệu ra đúng bảng chuẩn (Lên lịch `#0EA5E9` · Chốt lịch `#2563EB` ·
      Hoàn thành `#16A34A` · Hủy `#6B7280`); 4 khoá sort đổi đúng thứ tự + key lạ về mặc định;
      3 bộ lọc (status / mode_id / has_minutes) ra đúng số dòng; export .xlsx **44 dòng = 37 dữ
      liệu + 7 dòng khung**, `fields=` lọc còn đúng 3 cột, lọc + sort truyền vào export chạy đúng
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn Lịch (`calendar`), màn chi tiết meeting, `MeetingExport` cũ (không còn dùng ở `export()`
  nhưng file vẫn nằm đó) — chưa đụng.
- `MeetingResource` còn dùng chung ở `MyJobController`, `SolutionController`,
  `SolutionModuleController` → 3 màn đó **hưởng lây** phần thêm khoá + sửa định dạng ngày, nhưng
  giao diện chưa chuẩn hoá.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (12 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/meeting` (task 3.4).
Blocked: không.
