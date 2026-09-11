# Plan — Chuẩn hoá màn Loại hình hoạt động khách hàng theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `CustomerScopeGroupService::SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật, chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 `CustomerScopeGroup::isCanDelete()` — luật "chưa có lĩnh vực con" đưa từ FE về entity
- [x] 1.5 `CustomerScopeGroupResource` — thêm `status_text`, `creator_name`, `updater_name`, `is_can_delete`; ngày `d/m/Y H:i`
- [x] 1.6 `ExportColumnRegistry::COLUMNS['customer_scope_groups']` (9 cột) + `export()` dùng `DynamicExport`, đuôi `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 7 ô, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()` — ô Mã / Tên chờ Enter
- [x] 2.3 Tách cột `groupCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `groupName`
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái; lý do bị chặn đưa vào `title` badge
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderGroupStatus`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng — hiện hết cột mặc định
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả trong luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 11 cột (1838px) + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable`, chữ `Khóa`/`Xóa`
- [x] 2.13 Lệnh GHI (Xóa, Khóa/Mở khóa, Import) bọc `$safeLoading` trong `finally`
- [x] 2.14 Bỏ hết `—`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index (23 dòng) / sort `groupCode` / export 200; cờ `is_can_delete` trả đúng (dòng có 8 lĩnh vực con -> false)
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (9 = 9, 11 cột đủ width+minWidth)
- [x] 3.4 Đối chiếu **id modal** + **tên hàm gọi qua `$refs`** của cả 10 màn trong đợt với component thật
- [ ] 3.5 User mở trình duyệt kiểm tra

## Lỗi tự phát hiện khi kiểm chứng

Bản viết lại mở modal bằng `$bvModal.show('add-customer-scope-group')` trong khi `AddGroupModal.vue`
khai `id="add-group"` → bấm Tạo mới / Xem / Sửa sẽ **không có gì hiện ra**, không lỗi nào trên console.
Cùng họ với lỗi `loadData` vs `loadIndustryData` ở màn Nhóm giải pháp.

Đã sửa (3 chỗ) và rà **toàn bộ 10 màn** của đợt: đối chiếu mọi `$bvModal.show('<id>')` với `id=` khai
trong component modal, và mọi `$refs.<modal>.<method>()` với hàm thật — tất cả đều khớp.
