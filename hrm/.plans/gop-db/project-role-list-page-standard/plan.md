# Plan — Chuẩn hoá màn danh sách Vai trò dự án (`/assign/project_role`)

Phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (mức tối thiểu)

- [x] 1.1 `ProjectRolesService`: thêm `SORTABLE_COLUMNS` + tiebreak `id desc`
      (trước đây `sort_field` bị bỏ qua, luôn sắp theo `updated_at`)
- [x] 1.2 `ProjectRolesService`: subquery `creator_name` / `updater_name` (không leftJoin)
- [x] 1.3 `ProjectRolesService`: ô tìm nhanh `keyword` = tên vai trò + tên người tạo (EXISTS)
- [x] 1.4 `ProjectRolesResource`: thêm `status_text`, `creator_name`, `updater_name`;
      ngày giờ về `d/m/Y H:i`
- [x] 1.5 `ExportColumnRegistry`: thêm nhóm `'project_roles'` (9 cột)
- [x] 1.6 `ProjectRolesController::export()`: chuyển sang `DynamicExport` + registry, file `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 Thay `V2BaseFilterPanel` bằng `V2BaseSmartFilterPanel` + schema `filterFields`
- [x] 2.2 Bật `fixed-layout`, khai `allColumns` đủ `width` + `minWidth` theo mục 15b
- [x] 2.3 Bỏ cột chết "Dùng ở dự án" (`project_id` — Resource không trả)
- [x] 2.4 Gắn `columnCustomizationMixin` + `ColumnCustomizationModal` (mặc định hiện hết cột)
- [x] 2.5 Gắn `exportFieldsMixin` + `ExportFieldsModal`, thay `exportExcel()` bằng `runExport()`
- [x] 2.6 Gắn `filterStateMixin` (nhớ bộ lọc), `created()` khôi phục bộ lọc + cờ `_restoringFilters`
- [x] 2.7 Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderStatus()` / `escapeHtml()`
- [x] 2.8 Cột Hành động dùng `V2BaseRowActions`: Sửa + Xóa là 2 nút chính, Khóa/Mở khóa vào `⋮`
- [x] 2.9 Tooltip `lockBlockedReason()` trên badge Trạng thái giải thích vì sao chưa khóa/mở khóa được
- [x] 2.10 Toolbar theo `button-convention` (Tạo mới / Import / Xuất Excel / Cấu hình cột)
- [x] 2.11 Bỏ `page` / `per_page` khỏi `filters`; `loadData()` tự ghép từ `pagination`
- [x] 2.12 Bọc `$safeLoadingStart/Finish` cho các lệnh ghi + xuất file
- [x] 2.13 Dọn import thừa (`V2BaseLabel`, `V2BaseSelect`)

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC + parse `<script>` — sạch
- [x] 3.2 Đối chiếu định danh template bằng AST — không thiếu
- [x] 3.3 Cột bảng ↔ trường xuất FE ↔ registry BE khớp 9/9; mọi cột đủ `width` + `minWidth`
- [x] 3.4 Smoke test API (index / sort / keyword / status / khoảng ngày / export) — 200 cả 6
- [ ] 3.5 User mở trình duyệt kiểm tra giao diện thực tế

## Việc phát hiện thêm (đã sửa luôn)

- [x] `pages/assign/project_items/index.vue`: `ignoredFields` bị khai **cả trong `data` lẫn
      `computed`** → Vue 2 lấy bản trong `data`, computed bị che (chỉ cảnh báo trong console).
      Đã bỏ dòng trong `data`. Hiện tại 12/12 màn `assign/*` không còn lỗi này.

### Checkpoint — 05/09/2026

Vừa hoàn thành: toàn bộ Phase 1 + Phase 2 + Phase 3 (trừ 3.5) của màn `assign/project_role`;
sửa thêm lỗi `ignoredFields` bị che ở `assign/project_items`.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/project_role` (và `/assign/project_items`).
Blocked:
