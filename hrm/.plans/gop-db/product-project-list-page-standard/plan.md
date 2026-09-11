# Plan — Chuẩn hoá màn Danh sách hàng hoá làm dự án theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-product-project-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `ProductProjectController` — whitelist `SORTABLE_COLUMNS` (Mã hàng / Tên hàng / Ngày tạo)
      + `resolveSortKey()`. Trước đây `sort_field` bị **bỏ qua hoàn toàn**, bấm sort cột nào cũng
      chỉ đổi chiều theo ngày tạo
- [x] 1.2 Thêm `p.name as sort_name` vào 2 sub-query khoá để sắp xếp được theo Tên hàng
- [x] 1.3 `dedupUnionRows()` nhận khoá sắp xếp + **chốt `row_id desc`** ở cuối (thiếu thì 2 dòng
      cùng giá trị có thứ tự không xác định, lật trang thấy bản ghi lặp/mất)
- [x] 1.4 2 hàm transform trả thêm `erp_sync_status_color` (3 mã màu chuẩn) và
      `product_attributes_text` (TSKT hạ HTML về chữ cho file Excel)
- [x] 1.5 `ExportColumnRegistry::COLUMNS['product_projects']` — 19 cột
- [x] 1.6 `export()` → `DynamicExport` + `ExportColumnRegistry::resolve()`, `.xls` → `.xlsx`

## Phase 2 — Frontend (`pages/assign/product-project/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` + schema `filterFields` (7 ô,
      3 ô select remote render bằng slot), bỏ `title`/`subtitle`, placeholder "Chọn <trường>"
- [x] 2.2 `ignoredFields` thành computed dùng `textFilterKeys()`
- [x] 2.3 Bật `fixed-layout`; khai `width` = `minWidth` cho ĐỦ 17 cột theo 4 bậc, **đo trên 181
      dòng thật của màn** (max + phân vị 95), không ước lượng
- [x] 2.4 Ô tham chiếu (Dự án · Giải pháp · Hàng hoá cha) ghép `MÃ - Tên` cùng 1 dòng qua
      `joinCodeName()`; ô chữ dài `text-wrap clamp-2` + `:title`
- [x] 2.5 Thêm cột **Ngày tạo**; Trạng thái đồng bộ đổi từ `.pp-chip` tự chế sang `V2BaseBadge`
      + `:color="item.erp_sync_status_color"`
- [x] 2.6 `columnCustomizationMixin` (`columnScreenKey: 'product_projects'`) thay logic merge tự viết
- [x] 2.7 Xuất Excel: `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` dùng `downloadExcel`
      và `$safeLoadingStart/Finish`; nút màu `success`, khoá bằng `:interactable`
- [x] 2.8 `created()`: `loadData()` bắn đầu tiên; thêm `loadSeq`; khôi phục bộ lọc trước khi gọi;
      options bộ lọc hoãn tới khi mở panel; watcher reset trang 1; `handleSort` chỉ đổi `filters`;
      `handleReset` không gọi API 2 lần
- [x] 2.9 Bỏ sạch `'—'` (15 chỗ), bỏ in đậm trong ô, xoá CSS chết `.pp-chip` / `.pp-code-badge` /
      `.pp-icon-btn` / `.row-actions` / `.text-wrap-title`
- [x] 2.10 Mã BOM đổi từ `.pp-code-badge` (chữ đậm 700, nền xám) sang `.v2-cell-link` chuẩn

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel) — OK
- [x] 3.2 Đối chiếu tự động: 17/17 cột đủ `width`+`minWidth`, có slot hoặc khoá khớp API, map được
      sang cột xuất file; `exportFields` FE ↔ registry BE **19 = 19, cùng thứ tự**
- [x] 3.3 Smoke test API: `index` 200 (181 dòng, trả đủ `erp_sync_status_color` /
      `product_attributes_text` / `created_at`); sort `productCode` / `productName` / `createdAt`
      đổi đúng thứ tự, key lạ rơi về mặc định; `export` 200 ra .xlsx thật (chữ ký `504b`);
      `export?fields=...` chỉ ra đúng 3 cột + STT, key lạ bị loại
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- **Không có cột Hành động**: màn chỉ đọc (routes chỉ có `index` + `export` + endpoint picker),
  không có Sửa / Xóa / Khoá để đặt vào. Cần thêm thao tác thì mở lại.
- Hành động **"Lịch sử"** — module Assign chưa có `LogsCatalogHistory`.
- TSKT trong file Excel nối các dòng bằng " · ": blade dùng chung `exports/dynamic.blade.php` in
  bằng `{{ }}` nên HTML reader nuốt `\n` thành khoảng trắng. Muốn ô Excel xuống dòng thật thì phải
  sửa blade dùng chung thành `{!! nl2br(e($value)) !!}` — **đụng file chung của 18 màn, cần hỏi trước**.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (6 việc BE) + Phase 2 (10 việc FE) + 3.1/3.2/3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/product-project` (task 3.4).
Blocked: không.

## Cập nhật 2026-09-07 — Đồng bộ MÀU CHỮ trong ô bảng với màn mẫu `/assign/customers`

- [x] Mọi ô dữ liệu đổi từ `class="field-line"` trần sang **`class="field-line text-dark font-weight-normal"`**
      — đúng như màn mẫu `/assign/customers` và `/assign/solutions` đang dùng. `.field-line` trần
      chỉ có `color: #475569` (xám) nên chữ nhạt hơn hẳn các màn khác, nhìn cạnh nhau là lộ.
- [x] Dòng phụ trong ô (Người liên hệ, SĐT PM…) gắn thêm class **`v2-hint`** (`color: #6b7280`)
      khai trong `<style scoped>` của màn — cùng cách làm với màn Giải pháp, thay cho việc đè màu
      thẳng vào `.project-sub`.
- [x] Kiểm lại 4 màn: customers 18 ô chuẩn · solutions 21 · prospective-projects 10 · product-project 13;
      không còn ô nào dùng `.field-line` trần (trừ 1 chỗ có chủ ý ở màn khách hàng: người không có
      quyền xem thì mã KH là chữ thường, không phải link).
