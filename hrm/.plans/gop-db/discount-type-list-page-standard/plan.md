# Plan — Chuẩn hoá màn Danh mục loại giảm giá (`/assign/discount-types`)

Phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (mức tối thiểu)

- [x] 1.1 `DiscountType`: thêm hằng `STATUSES` (chữ + mã màu 3 trạng thái theo bảng 9 màu chuẩn)
- [x] 1.2 `DiscountTypeService`: `SORTABLE_COLUMNS` (thêm Ngày tạo; giữ khoá cũ `code`/`name`)
      + tiebreak `id desc`
- [x] 1.3 `DiscountTypeService`: subquery `creator_name` / `updater_name` (không leftJoin)
- [x] 1.4 `DiscountTypeService`: ô tìm nhanh thêm **người tạo** (EXISTS)
- [x] 1.5 `DiscountTypeResource`: thêm `status_text` + `status_color` + `is_can_lock_update`,
      ngày `d/m/Y H:i`
- [x] 1.6 `DiscountTypeResource`: bỏ `created_by_name` / `updated_by_name` — accessor nạp lười
      employee + employee_info theo từng dòng, ảnh hưởng cả `getAll` của dropdown báo giá
- [x] 1.7 `ExportColumnRegistry`: thêm nhóm `'discount_types'` (7 cột)
- [x] 1.8 **Thêm mới** `DiscountTypeController::export()` (`DynamicExport` + registry)
- [x] 1.9 **Thêm mới** route `GET /assign/discount_types/export` — đặt TRƯỚC route wildcard
      `/{discountType}`, middleware `checkPermission:Quản lý danh mục loại giảm giá`

## Phase 2 — Frontend

- [x] 2.1 Thay `V2BaseFilterPanel` bằng `V2BaseSmartFilterPanel` + schema `filterFields` (4 ô)
      + thêm `handleFilterChange`
- [x] 2.2 Bật `fixed-layout`, khai `allColumns` đủ `width` + `minWidth` theo mục 15b
- [x] 2.3 Tách dòng phụ của ô Tên và ô "Cập nhật" thành 4 cột riêng
      (Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật)
- [x] 2.4 Gắn `columnCustomizationMixin` + `ColumnCustomizationModal` (mặc định hiện hết cột)
- [x] 2.5 **Thêm nút Xuất Excel** + `exportFieldsMixin` + `ExportFieldsModal` (màn này chưa từng có)
- [x] 2.6 Cột Trạng thái dùng `V2BaseBadge :color`; bỏ `renderStatus()` / `escapeHtml()`;
      **gỡ nút Khoá/Mở khoá khỏi ô Trạng thái**
- [x] 2.7 Cột Hành động dùng `V2BaseRowActions` thay 4 `<button>` style inline: Sửa + Xóa là 2 nút
      chính (giữ hiện + `disabledTitle` khi không dùng được), Duyệt / Khoá - Mở khoá vào `⋮`;
      bỏ hành động "Xem" (bấm Mã là mở modal Xem)
- [x] 2.8 Điều kiện hiện Khoá/Mở khoá lấy từ cờ BE `is_can_lock_update`, bỏ `status !== 3` viết cứng
- [x] 2.9 Toolbar theo `button-convention` (Xóa nhiều / Bỏ chọn / Tạo mới / Xuất Excel / Cấu hình cột)
- [x] 2.10 Bỏ `page` / `per_page` khỏi `filters`; `mounted` → `created` + cờ `_restoringFilters`
- [x] 2.11 Bọc `$safeLoadingStart/Finish` cho 4 lệnh ghi + xuất file
- [x] 2.12 Dọn import thừa (`V2BaseLabel`, `V2BaseSelect`, `V2BaseDatePicker`, `V2BaseTitleSubInfo`)

## Phase 3 — Kiểm chứng

- [x] 3.1 `php -l` 6 file BE + compile SFC / parse `<script>` — sạch
- [x] 3.2 Đối chiếu định danh template bằng AST — không thiếu
- [x] 3.3 Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE khớp 7/7; 4 cột sortable có trong whitelist
- [x] 3.4 Modal id + `$refs...loadData()` / `resetModal()` + prop `color` của `V2BaseBadge` khớp thật
- [x] 3.5 Smoke test API — 9/9 request trả 200 (kể cả `/export` mới), phủ đủ 3 trạng thái bằng dữ
      liệu tạm trong transaction rồi rollback; DB sau test vẫn 1 dòng
- [ ] 3.6 User mở trình duyệt kiểm tra giao diện thực tế

## Ghi chú

- Màn này **trước đây không có chức năng Xuất Excel** — phần route + controller export là **thêm
  mới**, nằm trong phạm vi "BE tối thiểu" đã chốt cho cả loạt.
- Giữ `status_label` trong Resource cho tương thích (không tốn query), dù FE mới dùng `status_text`.

### Checkpoint — 05/09/2026

Vừa hoàn thành: toàn bộ Phase 1 + Phase 2 + Phase 3 (trừ 3.6) của màn `assign/discount-types`.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/discount-types`.
Blocked:
