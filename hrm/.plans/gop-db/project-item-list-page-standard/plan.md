# Plan — Chuẩn hoá màn Hạng mục dự án theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `ProjectItemService::SORTABLE_COLUMNS` — mở whitelist cho Tên / Ngày tạo / Ngày cập nhật, chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 `ProjectItemResource` — thêm `status_text`, `creator_name`, `updater_name`, `is_can_lock_update`; ngày `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry::COLUMNS['project_items']` (7 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 5 ô, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Cột định danh = **Tên hạng mục** (bảng không có mã) — `button.v2-cell-link` mở modal Xem, sticky+locked
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái vào cột Hành động
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderStatus` + `escapeHtml`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng — hiện hết cột mặc định
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả 6 chỗ trong luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `mounted` → `created`, `loadData()` chạy đầu tiên
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 10 cột (1542px) + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable`, "Xóa nhiều" `primary status="danger"`
- [x] 2.13 Lệnh GHI (Xóa, Xóa nhiều, Khóa/Mở khóa, Import) bọc `$safeLoading` trong `finally`
- [x] 2.14 Bỏ `—`; bỏ `page`/`per_page` khỏi `filters`; bỏ import `buildQuery` không còn dùng

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index (2 dòng) / sort `itemName` / export 200
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (7 = 7, 10 cột đủ width+minWidth)
- [x] 3.4 Đối chiếu id modal (`modal-project-item`) + tên hàm `$refs.projectItemModal.loadData/resetModal` với component thật — khớp
- [ ] 3.5 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.4.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.
