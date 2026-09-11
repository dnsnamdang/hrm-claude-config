# Plan — Chuẩn hoá màn "Yêu cầu làm giải pháp chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-request-solution-pending-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `RequestSolutionService::pending()` gọi `applySort()` (whitelist 15 khoá + chốt `id desc`)
      thay `orderBy($request->sort_field, $request->sort_dir)` nhận thẳng từ URL
- [x] 1.2 `pending()` eager load đủ 5 quan hệ như `index()`
      (`prospectiveProject.projectPhases.priorityLevel`, `receiveDepartment`, `receiver.info`,
      `solution`, `solution.pm.info`) — 4 cột vốn rỗng có dữ liệu, hết N+1
- [x] 1.3 `pending()` không quyền → trả **query rỗng** thay vì `[]`; bỏ đoạn kiểm tra quyền lặp 2 lần
      (`exportPending()` gọi `->get()` trên mảng là fatal 500)
- [x] 1.4 `pending()` thêm bộ lọc **Công ty / Phòng ban / Bộ phận** (theo đơn vị của người gửi yêu
      cầu, y hệt `index()`)
- [x] 1.5 `RequestSolutionResource` thêm cờ **`is_can_receive`** (entity đã có `isCanReceive()`,
      Resource chưa lộ ra)
- [x] 1.6 `exportPending()` chuyển sang `DynamicExport` + `ExportColumnRegistry::resolve('request_solutions')`,
      nhận `fields=a,b,c`, file `.xls` → `.xlsx`

## Phase 2 — Frontend (`pages/assign/request-solution/pending.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (5 mục, bỏ `title`/`subtitle`);
      nhóm `org` + `project_phase_id` render bằng slot
- [x] 2.2 **KHÔNG thêm ô lọc "Người tiếp nhận YC"** — định thêm vì BE nhận sẵn `receiver_by`,
      nhưng đo dữ liệu thật thì `receive_id` chỉ có từ trạng thái **Đã tiếp nhận** trở đi — màn này
      lọc cứng *Chờ tiếp nhận* nên ô đó luôn ra 0 kết quả. Bộ lọc còn **5 mục**
- [x] 2.3 Tách cột gộp "Mã • Tên yêu cầu" → `requestCode` (`nuxt-link`, sticky + locked) +
      `requestTitle`; gỡ 4 icon thao tác khỏi ô đó
- [x] 2.4 Cột `actions` **cuối bảng** + `V2BaseRowActions`: Tiếp nhận · Yêu cầu bổ sung thông tin;
      **bỏ "Xem"**, **bỏ "Từ chối" và "Hủy yêu cầu"** (chỉ đặt ở màn chi tiết — skill mục 1)
- [x] 2.5 Cột in cứng dấu gạch nay đọc dữ liệu thật: **Tiến trình YC** (badge màu BE) ·
      **Phòng tiếp nhận YC** · **Mức độ ưu tiên**. Riêng **Người tiếp nhận YC · Mã GP · PM làm GP**
      thì **BỎ HẲN cột** — đo trên dữ liệu thật: 4/4 phiếu *Chờ tiếp nhận* đều `receive_id = NULL`
      và 0 giải pháp gắn vào, tức 3 cột đó rỗng theo ĐỊNH NGHĨA của màn này
- [x] 2.6 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ **19 cột**; ô "MÃ - Tên" của đối
      tượng tham chiếu (dự án, khách hàng) ghép trên **1 dòng**
- [x] 2.7 Thêm 4 cột: Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật
- [x] 2.8 `columnCustomizationMixin` (`columnScreenKey: 'request_solutions_pending'`) +
      `ColumnCustomizationModal`
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` (trước tải thẳng file `.xls`)
- [x] 2.10 Sửa `handleFilterChange` nhận `{key, value}` (bản cũ spread cả payload → nhét khoá rác
      `key`/`value` vào `filters` rồi gửi lên API)
- [x] 2.11 `handleSort`/`handleReset` **không** gọi `loadData()` (deep watcher lo) + cờ
      `_restoringFilters` chặn gọi trùng; `ignoredFields` thành computed dùng `textFilterKeys`
- [x] 2.12 `loadSeq` chống response về trễ; `$nuxt.$loading` → `$safeLoadingStart/Finish`
- [x] 2.13 Nút toolbar chuyển từ slot `#toolbar` sang `#actions` (slot `toolbar` thay cả khối tiêu
      đề bảng); bỏ `V2BaseTitleSubInfo` / `V2BaseCodeTitle` khỏi các ô
- [x] 2.14 Bỏ sạch `'—'` / `'N/A'` / `font-weight-bold` / `v-html`; ô dữ liệu dùng
      `field-line text-dark font-weight-normal`, dòng phụ `project-sub v2-hint`
- [x] 2.15 `canReceive()` hard-code `true` → đọc cờ BE `is_can_receive`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel)
- [x] 3.2 Đối chiếu tự động: 19 cột đủ `width` = `minWidth` + có slot render; `exportFields` FE ↔
      registry BE khớp; 0 chỗ `'—'` / `'N/A'` / `font-weight-bold` / `field-line` trần
- [x] 3.3 Smoke test API bằng dữ liệu thật hoặc dữ liệu giả trong transaction rồi `ROLLBACK`:
      danh sách · sort whitelist (asc/desc/key lạ) · lọc org · cờ `is_can_receive` · export `fields=`
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- `RequestSolutionReceiveModal` (popup Tiếp nhận) — giữ nguyên.
- Màn chi tiết `_id/index.vue` — giữ nguyên (đã có đủ Tiếp nhận · Từ chối · Hủy yêu cầu).
- Hành động "Lịch sử" — module Assign chưa có `LogsCatalogHistory`, giữ đúng quyết định của màn
  `/assign/request-solution`.
- `App\ExcelExport\RequestSolutionPendingExport` giữ lại trên đĩa nhưng không còn nơi gọi.

### Checkpoint — 2026-09-08
Vừa hoàn thành: Phase 1 (6 việc BE) + Phase 2 (15 việc FE) + 3.1 → 3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/request-solution/pending` (task 3.4).
Blocked: không — DB dev có 4 phiếu *Chờ tiếp nhận*, tài khoản test thấy 3.
