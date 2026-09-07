# Plan — Chuẩn hoá màn Mẫu phiếu thu thập thông tin (`/assign/form-templates`)

Phụ trách: @khoipv · Nhánh: `gop_db`

## Phase 1 — Backend (mức tối thiểu)

- [x] 1.1 `FormTemplateService`: `SORTABLE_COLUMNS` thay cho map 4 cột cũ (thêm Mã + Ngày tạo)
      + tiebreak `id desc`
- [x] 1.2 `FormTemplateService`: subquery `creator_name` / `updater_name` (không leftJoin)
- [x] 1.3 `FormTemplateService`: ô tìm nhanh thêm **người tạo** (EXISTS) + dùng `escapeLikeKeyword`
- [x] 1.4 `FormTemplatesResource`: sửa lỗi `whenLoaded('sections')` luôn truthy → nạp lười cả cây
      section cho TỪNG dòng danh sách
- [x] 1.5 `FormTemplatesResource`: `questions_count` lấy từ `withCount`, bỏ `$this->questions->count()`
- [x] 1.6 `FormTemplatesResource`: thêm `status_text`, `creator_name`, `updater_name`, ngày `d/m/Y H:i`
- [x] 1.7 `FormTemplate`: thêm hằng `STATUS_NAMES`
- [x] 1.8 `ExportColumnRegistry`: thêm nhóm `'form_templates'` (9 cột)
- [x] 1.9 `FormTemplateController::export()`: chuyển sang `DynamicExport` + registry, `.xls` → `.xlsx`

## Phase 2 — Frontend

- [x] 2.1 Thay `V2BaseFilterPanel` bằng `V2BaseSmartFilterPanel` + schema `filterFields` (6 ô)
- [x] 2.2 Tách ô "Mẫu phiếu" thành các cột riêng: Mã (link chi tiết) · Tên · Người tạo · Ngày tạo
- [x] 2.3 Bật `fixed-layout`, khai `allColumns` đủ `width` + `minWidth` theo mục 15b
- [x] 2.4 Gắn `columnCustomizationMixin` + `ColumnCustomizationModal` (mặc định hiện hết cột)
- [x] 2.5 Gắn `exportFieldsMixin` + `ExportFieldsModal`, thay `exportExcel()` bằng `runExport()`
- [x] 2.6 Cột Trạng thái dùng `V2BaseBadge`; bỏ `renderTemplateStatus()` / `escapeHtml()`
- [x] 2.7 Cột Hành động riêng dùng `V2BaseRowActions`: Sửa + Xoá là 2 nút chính; Sao chép / In /
      Khoá-Mở khoá vào `⋮`; bỏ hành động "Xem mẫu" (đã có link ở cột Mã)
- [x] 2.8 Toolbar theo `button-convention` (Tạo mẫu phiếu / Xuất Excel / Cấu hình cột)
- [x] 2.9 Gộp `mounted` vào `created` + cờ `_restoringFilters`; đổi lọc thì về trang 1
- [x] 2.10 Bọc `$safeLoadingStart/Finish` cho lệnh ghi + xuất file
- [x] 2.11 Bỏ `console.log` sót trong `confirmToggleLock`; dọn import `V2BaseTitleSubInfo`

## Phase 3 — Kiểm chứng

- [x] 3.1 `php -l` 5 file BE + compile SFC / parse `<script>` — sạch
- [x] 3.2 Đối chiếu định danh template bằng AST — không thiếu (chạy lại cả 13 màn của loạt)
- [x] 3.3 Cột bảng ↔ slot ↔ trường xuất FE ↔ registry BE khớp 9/9; 5 cột sortable có trong whitelist
- [x] 3.4 Đo số query: 4 query/dòng → 0; endpoint danh sách còn **7 query cố định**
- [x] 3.5 Smoke test API bằng dữ liệu tạm trong transaction rồi rollback — 8/8 request trả 200,
      DB sau test vẫn 0 dòng
- [ ] 3.6 User mở trình duyệt kiểm tra giao diện thực tế

## Ghi chú

- Bảng `form_templates` **rỗng trên DB local** → không kiểm chứng được bằng dữ liệu thật;
  đã bù bằng dữ liệu tạm trong transaction.
- `app/ExcelExport/FormTemplatesExport.php` + `resources/views/exports/form_templates.blade.php`
  giờ không còn nơi nào gọi. Chưa xoá — chờ user quyết.

### Checkpoint — 05/09/2026

Vừa hoàn thành: toàn bộ Phase 1 + Phase 2 + Phase 3 (trừ 3.6) của màn `assign/form-templates`.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/form-templates`.
Blocked:
