# Plan — Chuẩn hoá màn Danh sách báo giá theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-quotation-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `Quotation::getStatusList()` — **6/7 mã màu** lệch bảng 9 mã chuẩn, quy về đúng nhóm:
      Đang tạo `#9E9E9E` → `#64748B` · Chờ TP duyệt `#673AB7` → `#D97706` ·
      Chờ BGĐ duyệt `#E91E63` → `#D97706` · Đã duyệt `#009688` → `#16A34A` ·
      Dừng `#EF4444` → `#DC2626` · Trúng thầu `#D4AF37` → `#7C3AED`
- [x] 1.2 `Quotation::getSummaryStatusList()` (báo giá tổng) — quy chuẩn tương tự; giữ
      "Đã tạo hợp đồng" `#0EA5E9` và "Hết hiệu lực"/"Đóng" `#6B7280` vì đã đúng bảng
- [x] 1.3 `Quotation::getTypeList()` — badge phân loại đổi sang 2 sắc trung tính;
      thêm hằng `APPROVAL_LEVEL_COLORS` cho badge Cấp duyệt
- [x] 1.4 `QuotationService` — whitelist `QUOTATION_SORTABLE_COLUMNS` + `applyQuotationSort()`
      chốt `id desc` (trước là `orderBy($filters['sort_field'])` trần)
- [x] 1.5 `QuotationResource` — `updated_at` format `d/m/Y H:i` (trước trả THÔ ra chuỗi ISO);
      thêm `updater_name`, `approval_level_color`, và 4 khoá PHẲNG `bom_code` / `bom_name` /
      `project_code` / `project_name` (blade xuất file không đọc được mảng lồng)
- [x] 1.6 `ExportColumnRegistry::COLUMNS['quotations']` — 20 cột
- [x] 1.7 Route + `exportList()` mới (`DynamicExport` + `resolve()`), đặt TRƯỚC route `/{id}`.
      ⚠️ Khác hẳn `exportExcel()` sẵn có = xuất CHI TIẾT 1 báo giá ra file để sửa rồi nạp lại

## Phase 2 — Frontend (`pages/assign/quotations/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`; nhóm Công ty/Phòng ban/Bộ phận/
      Người lập khai thành MỘT field `org`; 3 select2 remote + Giai đoạn dự án render bằng slot
- [x] 2.2 `ignoredFields` thành computed dùng `textFilterKeys()`; options 3 dropdown chuyển
      `{value,label}` → `{id,name}` cho đúng khuôn panel mới
- [x] 2.3 Tách cột gộp `code_name` → `quotationCode` (link) + `bomInfo` + `pricing_request_code`;
      gỡ 6 icon thao tác khỏi ô
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa chính, Sao chép · In · Lịch sử
      phê duyệt vào `⋮`; bỏ "Xem chi tiết"
- [x] 2.5 Ô tham chiếu (BOM list · Dự án TKT) ghép `MÃ - Tên` cùng 1 dòng
- [x] 2.6 Thêm 3 cột: Giai đoạn dự án · Người cập nhật · Ngày cập nhật
- [x] 2.7 Cấp duyệt + Đồng bộ ERP đổi sang `V2BaseBadge` (bỏ 3 class CSS `.badge-level-*` nền đậm
      chữ trắng và cụm icon tự chế); nhãn cấp duyệt trong bộ lọc ghi rõ "Cấp 2 — TP duyệt"…
- [x] 2.8 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 20 cột theo 4 bậc
- [x] 2.9 `columnCustomizationMixin` thay logic merge tự viết (bản cũ trả thẳng cấu hình đã lưu →
      mất hết `width`/`align`/`sortable` khai trong code)
- [x] 2.10 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — **lần đầu có nút Xuất Excel
      danh sách** ở màn này
- [x] 2.11 Thêm `loadSeq`; Xóa bọc `$safeLoadingStart/Finish`
- [x] 2.12 **Sửa lỗi "Làm mới" ném TypeError** (`this.loadData()` + `this.resetLoadDedupe()` đều
      không tồn tại, tên đúng là `fetchData`). Rà bằng
      `grep -rn "this.loadData()" pages/assign/` rồi đối chiếu tên hàm thật của từng màn → phát
      hiện **màn thứ ba cùng lỗi: `/assign/quotations/pending-approval`**, đã sửa luôn
      (`pages/assign/quotations/pending-approval/index.vue`)
- [x] 2.13 Bỏ `'—'` / `'N/A'` / `.text-muted` trong ô (0 chỗ còn lại); màu chữ theo màn mẫu
      `/assign/customers`

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC — OK
- [x] 3.2 Đối chiếu tự động: 20/20 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **20 = 20, cùng thứ tự**; 0 chỗ `'—'`/`'N/A'`/`.text-muted`
- [x] 3.3 Smoke test API trên **75 báo giá thật**: index 200 (57 query/10 dòng); trả đủ 4 khoá
      phẳng + `updater_name` + `approval_level_color`; `updated_at` = `27/07/2026 16:55`
      (trước là chuỗi ISO); 5 trạng thái xuất hiện đều đúng bảng 9 mã màu
      (Đang tạo `#64748B` · Chờ TP duyệt `#D97706` · Đã duyệt `#16A34A` · Trúng thầu `#7C3AED` ·
      Đóng `#6B7280`); 3 khoá sort đổi đúng thứ tự + key lạ rơi về mặc định;
      export ra .xlsx **82 dòng = 75 dữ liệu + 7 dòng khung**; `fields=` lọc đúng
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn `/assign/quotations/pending-approval` và `/assign/summary-quotations` dùng chung
  `QuotationResource` nên **hưởng lây** phần sửa màu + `updated_at` + khoá phẳng, nhưng **giao diện
  chưa chuẩn hoá**.
- `QuotationController::exportExcel()` (xuất chi tiết 1 báo giá để re-import) giữ nguyên.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (13 việc FE) + 3.1→3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/quotations` (task 3.4).
Blocked: không.
