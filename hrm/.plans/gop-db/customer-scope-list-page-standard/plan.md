# Plan — Chuẩn hoá màn Lĩnh vực kinh doanh khách hàng theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `CustomerScopeService::SORTABLE_COLUMNS` — mở whitelist cho Mã / Tên / Ngày tạo / Ngày cập nhật, chốt `id desc` cuối
- [x] 1.2 Subquery `creator_name` / `updater_name` (chỉ TÊN, không leftJoin)
- [x] 1.3 Ô tìm nhanh tìm thêm theo **người tạo** bằng `EXISTS`
- [x] 1.4 `CustomerScopeResource` — thêm `status_text`, `creator_name`, `updater_name`; ngày `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry::COLUMNS['customer_scopes']` (9 cột) + `export()` dùng `DynamicExport`

## Phase 2 — Frontend

- [x] 2.1 `V2BaseSmartFilterPanel` + schema `filterFields` 7 ô, bỏ `title`/`subtitle`, placeholder chuẩn
- [x] 2.2 `ignoredFields` computed dùng `textFilterKeys()`
- [x] 2.3 Tách cột `scopeCode` (button `.v2-cell-link` mở modal Xem, sticky+locked) / `scopeName`
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`; bỏ "Xem"; ẩn nút thay vì disable
- [x] 2.5 Nút Khóa/Mở khóa rời khỏi ô Trạng thái vào cột Hành động
- [x] 2.6 Trạng thái dùng `V2BaseBadge` (bỏ `v-html` + `status-pill` + `renderScopeStatus` + `escapeHtml`)
- [x] 2.7 Cột Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật riêng — **hiện hết cột mặc định**
- [x] 2.8 `columnCustomizationMixin` + `ColumnCustomizationModal` (màn chưa từng có)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `$safeLoading` (cả trong luồng import)
- [x] 2.10 `filterStateMixin` + `mergeKnownFilters`; `loadData()` chạy đầu tiên
- [x] 2.11 Mục 15b: `fixed-layout` + `width`/`minWidth` đủ 11 cột theo 4 bậc + `clamp-2` + `:title`
- [x] 2.12 Button-convention: Import cam + `ri-upload-line`, Xuất xanh lá, `:interactable`, chữ `Khóa`/`Mở khóa`/`Xóa`
- [x] 2.13 Lệnh GHI (Xóa, Khóa/Mở khóa, Import) bọc `$safeLoading` trong `finally`
- [x] 2.14 Bỏ hết `—`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile FE + dò identifier template bằng AST
- [x] 3.2 Smoke test API: index (146 dòng) / sort `scopeCode` / keyword theo người tạo (2 dòng) / export 200
- [x] 3.3 Đối chiếu cột bảng ↔ cột file ↔ registry BE (9 = 9, 11 cột đều đủ width+minWidth, tổng 1888px)
- [ ] 3.4 User mở trình duyệt kiểm tra

### Checkpoint — 2026-09-05
Vừa hoàn thành: toàn bộ Phase 1-2, kiểm chứng 3.1-3.3.
Bước tiếp theo: user kiểm tra trên trình duyệt.
Blocked: không có.

## Ngày 16/11/2026 (@junfoke)
- [x] 16/11/2026 — Hỗ trợ check Lĩnh vực kinh doanh KH có dòng không người tạo / người cập nhật, ngày 24/04, trùng mã LVKDKH.0001–0059: 59 dòng (id 148–206, `created_by = 0`) là danh mục của ETEK GREEN (`company_id = 9`) chèn thẳng vào DB lúc gộp dữ liệu 24/04 — bỏ qua kiểm trùng ở form, bảng không có unique index trên `code`, không mang liên kết Loại hình hoạt động. Prod giống local, chưa khách hàng / dự án / giải pháp nào dùng. 7 dòng trùng tên danh mục Tân Phát, 52 dòng là lĩnh vực riêng của ETEK. Script `CleanupLegacyDuplicateCatalogsSeeder` (09/10) chỉ dọn Nhóm ngành + Nhóm giải pháp. Chưa sửa dữ liệu — chờ nghiệp vụ chốt: gộp vào bộ chuẩn (cấp mã từ LVKDKH.0150) hay khoá/xoá.
