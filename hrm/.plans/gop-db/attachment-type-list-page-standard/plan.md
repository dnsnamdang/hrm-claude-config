# Plan — Chuẩn hoá màn Danh mục loại tài liệu theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `AttachmentTypeService::SORTABLE_COLUMNS` — nhận key cột FE (`typeCode` / `typeName` / `createdAt` / `updatedAt`), chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS` (trước: mã + tên + mô tả)
- [x] 1.4 `AttachmentTypeResource` — thêm `status_text`, `creator_name`, `updater_name`, `is_can_edit`; ngày `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry::COLUMNS['attachment_types']` (8 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 6 ô, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột `typeCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `typeName`
- [x] 2.4 **Bỏ bộ nút thao tác BỊ NHÂN ĐÔI** (cột gộp + cột actions) → 1 cột Hành động dùng `V2BaseRowActions`; bỏ "Xem"
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái vào cột Hành động
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderStatus`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật chuẩn — hiện hết cột mặc định
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading`
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 10 cột (1668px) + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Xuất xanh lá, `:interactable` thay `:disabled`, chữ `Khóa`/`Mở khóa`/`Xóa`
- [x] 2.13 Lệnh GHI (Xóa, Khóa/Mở khóa) bọc `$safeLoading` trong `finally`
- [x] 2.14 Bỏ computed `metaSummary` không nơi nào dùng; bỏ icon rỗng `<i class="mr-1 text-muted">` ở cột Ngày tạo

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index (8 dòng) / sort `typeCode` / keyword / export 200
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (8 = 8, 10 cột đủ width+minWidth)
- [ ] 3.4 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.
