# Plan — Chuẩn hoá màn Nguyên nhân thất bại dự án (`/assign/reason_project_failure`)

Phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (mức tối thiểu)

- [x] 1.1 `ReasonProjectFailureService`: `SORTABLE_COLUMNS` (trước chỉ có đúng 1 cột `updatedAt`)
      + tiebreak `id desc`
- [x] 1.2 `ReasonProjectFailureService`: subquery `creator_name` / `updater_name` (không leftJoin)
- [x] 1.3 `ReasonProjectFailureService`: ô tìm nhanh thêm **người tạo** (EXISTS)
- [x] 1.4 `ReasonProjectFailureResource`: thêm `status_text`, `creator_name`, `updater_name`,
      ngày `d/m/Y H:i`
- [x] 1.5 `ReasonProjectFailureResource`: bỏ `created_by_name` / `updated_by_name` — 2 accessor nạp
      lười employee + employee_info theo từng dòng (**43 query → 7**)
- [x] 1.6 `ExportColumnRegistry`: thêm nhóm `'reason_project_failures'` (7 cột)
- [x] 1.7 `ReasonProjectFailureController::export()`: `DynamicExport` + registry, `.xls` → `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 Thay `V2BaseFilterPanel` bằng `V2BaseSmartFilterPanel` + schema `filterFields` (5 ô)
      + thêm `handleFilterChange`
- [x] 2.2 Gắn `filterStateMixin` — màn này trước đây chưa nhớ bộ lọc khi rời trang
- [x] 2.3 Bật `fixed-layout`, khai `allColumns` đủ `width` + `minWidth` theo mục 15b
- [x] 2.4 Tách cột "Cập nhật" thành Người cập nhật + Ngày cập nhật
- [x] 2.5 Gắn `columnCustomizationMixin` + `ColumnCustomizationModal` (mặc định hiện hết cột)
- [x] 2.6 Gắn `exportFieldsMixin` + `ExportFieldsModal`, thay `exportExcel()` bằng `runExport()`
- [x] 2.7 Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderStatus()` / `escapeHtml()`; **gỡ nút
      Khoá/Mở khoá khỏi ô Trạng thái** (badge không được bấm)
- [x] 2.8 Cột Hành động dùng `V2BaseRowActions` thay 3 `<button>` style inline: Sửa + Xóa là 2 nút
      chính, Khoá/Mở khoá vào `⋮`; bỏ hành động "Xem" (bấm tên là mở modal Xem)
- [x] 2.9 Nút Sửa: `disabled` → **ẩn** khi bản ghi đang Khoá
- [x] 2.10 Toolbar theo `button-convention` (Tạo mới / Import / Xuất Excel / Cấu hình cột)
- [x] 2.11 Bỏ `page` / `per_page` và khoá `name` chết khỏi `filters`; `mounted` → `created`
      + cờ `_restoringFilters`; đổi lọc thì về trang 1
- [x] 2.12 Bọc `$safeLoadingStart/Finish` cho lệnh ghi + xuất file
- [x] 2.13 Dọn import thừa (`V2BaseLabel`, `V2BaseSelect`, `V2BaseDatePicker`,
      `V2BaseTitleSubInfo`, `buildQuery`)

## Phase 3 — Kiểm chứng

- [x] 3.1 `php -l` 4 file BE + compile SFC / parse `<script>` — sạch
- [x] 3.2 Đối chiếu định danh template bằng AST — không thiếu
- [x] 3.3 Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE khớp 7/7; 3 cột sortable có trong whitelist
- [x] 3.4 Modal id + `$refs...loadData()` / `resetModal()` khớp component thật
- [x] 3.5 Smoke test API trên dữ liệu thật (5 dòng) — 8/8 request trả 200; số query 43 → 7
- [ ] 3.6 User mở trình duyệt kiểm tra giao diện thực tế

## Ghi chú

- **Không** tự thêm `is_can_delete`: CLAUDE.md yêu cầu hỏi user điều kiện xoá trước. Hiện giữ
  nguyên hành vi cũ (luôn cho xoá) — nếu cần siết, báo điều kiện để bổ sung.
- `app/ExcelExport/ReasonProjectFailureExport.php` không còn nơi nào gọi. Chưa xoá — chờ user quyết.

### Checkpoint — 05/09/2026

Vừa hoàn thành: toàn bộ Phase 1 + Phase 2 + Phase 3 (trừ 3.6) của màn
`assign/reason_project_failure`.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/reason_project_failure`.
Blocked:
