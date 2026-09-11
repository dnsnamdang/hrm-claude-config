# Plan — Chuẩn hoá màn Danh sách BOM List theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-bom-list-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `BomList::getStatusList()` — **6/6 mã màu** nằm ngoài bảng 9 mã chuẩn, quy về đúng nhóm:
      Đang tạo `#FF9800` → `#64748B` · Hoàn thành `#4CAF50` → `#16A34A` ·
      Chờ duyệt `#2196F3` → `#D97706` · Đã duyệt `#9C27B0` → `#16A34A` ·
      Đã được tổng hợp `#9E9E9E` → `#6B7280` · Không duyệt `#F44336` → `#DC2626`
- [x] 1.2 `BomList::getTypeList()` — badge phân loại (không phải trạng thái) đổi sang 2 sắc trung
      tính để không tranh chú ý với badge trạng thái ở cột bên cạnh
- [x] 1.3 `BomList` — thêm `isCanEdit()` / `isCanDelete()` khớp đúng guard của
      `BomListService::update` (Đang tạo / Hoàn thành / Không duyệt + là người tạo) và `destroy`
      (Đang tạo + là người tạo)
- [x] 1.4 `BomListService::index()` — whitelist `SORTABLE_COLUMNS` + `applySort()` chốt `id desc`
      (trước là `orderBy($request->sort_field)` trần)
- [x] 1.5 `BomListListResource` — ngày `d/m/Y H:i` (trước hiện cả giây do `Helper::formatDateTime()`
      mặc định `d/m/Y H:i:s`); trả `is_can_edit` / `is_can_delete`
- [x] 1.6 `ExportColumnRegistry::COLUMNS['bom_lists']` — 23 cột
- [x] 1.7 `BomListController::exportList()` — chuyển sang `DynamicExport` + `resolve()`.
      Bỏ tham số `columns` (JSON do FE tự dựng) và blade `exports.bom_list_list` phải tự map từng
      khoá cột của bảng — đổi tên cột trên lưới là file ra rỗng đúng cột đó

## Phase 2 — Frontend (`pages/assign/bom-list/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`; nhóm Công ty/Phòng ban/Bộ phận
      khai thành MỘT field `org`; ô Giải pháp (chỉ đọc, tự điền theo dự án) và Khách hàng
      (select2 remote) render bằng slot — giữ nguyên cascade cũ
- [x] 2.2 `ignoredFields` thành computed dùng `textFilterKeys()`; options 2 dropdown chuyển
      `{value,label}` → `{id,name}` cho đúng khuôn panel mới
- [x] 2.3 Tách cột gộp `code_name` → `bomCode` (link `.v2-cell-link`) + `bomName`; gỡ tối đa
      6 icon thao tác khỏi ô
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa chính, Sao chép · In · Lịch sử
      vào `⋮`; bỏ "Xem chi tiết"
- [x] 2.5 Ô tham chiếu (Dự án TKT · Giải pháp · Khách hàng) ghép `MÃ - Tên` cùng 1 dòng
- [x] 2.6 Tách 3 thông tin khỏi dòng phụ / ô gộp thành cột riêng: **Phòng của người tạo**,
      **Người cập nhật**, **Ngày cập nhật** (ô "Cập nhật" cũ gộp ngày + "bởi <tên>")
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 17 cột theo 4 bậc
- [x] 2.8 `columnCustomizationMixin` thay logic merge tự viết (bản cũ trả thẳng cấu hình đã lưu →
      mất hết `width`/`align`/`sortable` khai trong code)
- [x] 2.9 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — **lần đầu có popup chọn
      trường xuất file** ở màn này
- [x] 2.10 `mounted` → `created`; 2 request `per_page=10000` (dự án + giải pháp) hoãn tới khi mở
      panel lọc (vẫn nạp sớm nếu bộ lọc đã lưu có dự án/giải pháp để hiện đúng nhãn); thêm `loadSeq`
- [x] 2.11 `handleSort` chỉ đổi `filters` (trước vừa gọi `loadData` vừa để watcher bắn → 2 request);
      `handleReset` cũng hết gọi 2 lần
- [x] 2.12 Bỏ `'—'` và `'N/A'` trong ô (0 chỗ còn lại); badge Loại BOM / Version dùng `V2BaseBadge`
      thay `span.badge-light`; màu chữ theo màn mẫu `/assign/customers`
- [x] 2.13 Xóa BOM bọc `$safeLoadingStart/Finish`, đọc câu lỗi từ `response.data.message`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC — OK
- [x] 3.2 Đối chiếu tự động: 17/17 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **23 = 23, cùng thứ tự**; 0 chỗ còn `'—'` / `'N/A'`
- [x] 3.3 Smoke test API trên 11 BOM thật: index 200 (32 query/10 dòng), `status_color` = `#16A34A`
      đúng bảng chuẩn, ngày `27/07/2026 11:50` (không còn giây), có `is_can_edit`/`is_can_delete`;
      sort `bomCode` và `bomName` cho thứ tự KHÁC nhau (đúng là sắp theo 2 cột khác nhau),
      key lạ về mặc định; export ra .xlsx **18 dòng = 11 dữ liệu + 7 dòng khung**;
      `fields=` lọc đúng, key lạ bị loại
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn này **đã có sẵn hành động "Lịch sử"** (`BomListLogModal`) nên không phải nợ như 8 màn trước.
- `App\ExcelExport\BomListListExport` + blade `exports/bom_list_list.blade.php` giữ lại trong repo
  (không còn được gọi) để đối chiếu khi cần.
- Nút "In BOM List" và popup cấu hình in giữ nguyên (`bomPrintMixin`).

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (13 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/bom-list` (task 3.4).
Blocked: không.
