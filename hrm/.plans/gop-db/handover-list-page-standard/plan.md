# Plan — Chuẩn hoá màn Danh sách phiếu bàn giao theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-handover-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `Handover::STATUSES` — Từ chối `#B91C1C` → `#DC2626` (nhóm Từ chối – Quá hạn – Khoá);
      4 mã còn lại đã đúng bảng 9 mã chuẩn, giữ nguyên (kèm ghi chú vì sao "Đã duyệt" là `#2563EB`)
- [x] 1.2 `Handover::isCanEdit()` / `isCanDelete()` — chuyển **NGUYÊN** điều kiện đang nằm ở FE
      (`status ∈ {Nháp, Từ chối}` + là người tạo / `status = Nháp` + là người tạo) về BE
- [x] 1.3 `HandoverResource` — thêm `updated_by`, `updated_by_name`, `is_can_edit`, `is_can_delete`;
      `created_at`/`updated_at`/`approved_at`/`submitted_at` format `d/m/Y H:i` (trước còn giây)
- [x] 1.4 `HandoverService::index()` — whitelist `SORTABLE_COLUMNS` (13 khoá) + chốt `id desc`.
      ⚠️ Bản cũ `orderBy($request->sort_field, $request->sort_dir)` nhận thẳng chuỗi từ URL
- [x] 1.5 `HandoverService` — eager load `employee_update.info` ở `index()`, thêm
      `employee_update.info` + `approver.info` ở `pending()` (Resource đọc nhưng chưa nạp → N+1)
- [x] 1.6 `ExportColumnRegistry::COLUMNS['handovers']` — 19 cột
- [x] 1.7 **Route + `export()` MỚI** (`DynamicExport` + registry), đặt TRƯỚC route `/{handover}` —
      màn này trước giờ **không có xuất Excel**

## Phase 2 — Frontend (`pages/assign/handover/`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (5 mục / 6 ô)
- [x] 2.2 Tắt ô **Bộ phận** (`disable_part`) — bảng `handovers` KHÔNG có cột `part_id`, service
      cũng không đọc khoá đó → ô lọc chết
- [x] 2.3 **Sửa `handleFilterChange`**: panel phát `{ key, value }` nhưng hàm cũ viết
      `this.filters = { ...this.filters, ...filters }` → nhét 2 khoá rác `key`/`value` vào
      `filters` (và gửi lên API) trong khi ô lọc thật không được gán giá trị
- [x] 2.4 Tách ô gộp `handoverInfo` (mã + tên NV + 2 dòng phụ + 3 icon) → `handoverCode` (link,
      sticky, locked) + Nhân viên bàn giao + Phòng ban + Người cập nhật + Ngày cập nhật
- [x] 2.5 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa chính, Lịch sử vào `⋮`; bỏ "Xem";
      cờ quyền đọc `is_can_edit`/`is_can_delete` từ BE thay vì tự so `created_by`
- [x] 2.6 Thêm popup **`HandoverHistoryModal`** bọc `SystemInfoSection` (entity-type `handover`) —
      dùng chung với khối Lịch sử ở màn chi tiết, để 2 nơi không lệch nhau
- [x] 2.7 Thêm 5 cột: Ghi chú · Ngày gửi duyệt · Người duyệt · Ngày duyệt · Lý do từ chối
- [x] 2.8 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ 18 cột theo 4 bậc
- [x] 2.9 `columnCustomizationMixin` + `ColumnCustomizationModal` — **lần đầu màn này bật/tắt được
      cột** (bản cũ khai `isVisible` nhưng không có popup nào để đổi)
- [x] 2.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — **lần đầu có nút Xuất Excel**
- [x] 2.11 `filterStateMixin` — **lần đầu giữ bộ lọc** khi vào xem/sửa rồi quay lại
- [x] 2.12 Thêm `loadSeq` + `suppressFilterWatch`; `handleSort` chỉ đổi `filters` (deep watcher lo
      gọi API) thay vì gọi thẳng; Xóa bọc `$safeLoadingStart/Finish`
- [x] 2.13 Chuyển nút toolbar từ slot `toolbar` sang `actions` — `toolbar` thay cả khối tiêu đề nên
      màn đang **mất tiêu đề "Danh sách phiếu bàn giao"**
- [x] 2.14 Bỏ sạch `'—'` / `'N/A'` / `font-weight-bold` trong ô; 3 con số Đã nhận / Từ chối / Chờ
      nhận chuyển từ `style` nội tuyến sang class có tên

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK cho cả `index.vue` và popup mới
- [x] 3.2 Đối chiếu tự động: 18/18 cột đủ `width` = `minWidth`, có slot render, map được sang cột
      xuất file; `exportFields` FE ↔ registry BE **19 = 19, cùng thứ tự**; 0 chỗ
      `'—'`/`'N/A'`/`v-html`/`.status-pill`
- [x] 3.3 Smoke test: bảng `handovers` **rỗng** nên dựng **5 phiếu giả trong transaction rồi
      ROLLBACK**. Kết quả: index trả đủ 5 dòng; 5 trạng thái ra đúng bảng 9 mã màu (Nháp `#64748B`
      · Chờ duyệt `#D97706` · Đã duyệt `#2563EB` · Từ chối `#DC2626` · Hoàn tất `#16A34A`);
      cờ quyền đúng luật (Nháp = sửa+xóa · Từ chối = sửa · 3 trạng thái còn lại không thao tác);
      3 khoá sort đổi đúng thứ tự + key lạ về mặc định; lọc `status` / `reason` / `keyword` đều ăn;
      ngày ra `07/09/2026 16:05` (bỏ giây); export .xlsx **12 dòng = 5 dữ liệu + 7 dòng khung**,
      20 cột, `fields=` lọc còn 4 cột đúng thứ tự tick; rollback xong bảng về lại 0 dòng
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- `/assign/handover/pending` và `/assign/handover/receiving` dùng chung `HandoverResource` nên
  **hưởng lây** khoá mới + định dạng ngày, nhưng **giao diện chưa chuẩn hoá**.
- Màn chi tiết `_id/index.vue`, `_id/receive.vue`, form `add.vue` giữ nguyên.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (14 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/handover` (task 3.4).
Blocked: không — nhưng bảng `handovers` đang rỗng nên cần tạo vài phiếu thật để nhìn.
