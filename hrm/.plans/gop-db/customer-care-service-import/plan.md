# Plan — Import Excel màn Danh mục gói bảo dưỡng

**Feature:** customer-care-service-import · **@khoipv** · nhánh `gop_db`
**Design:** [design.md](design.md)

---

## Phase 1 — Backend

- [x] T1.1 `ServiceImportService.php` mới: `referenceData()`, `validateImportData()` (hàm thuần + snapshot), `import()`
- [x] T1.2 Luật validate sheet 1 (gói): mã/tên bắt buộc, ≤255, không trùng trong file + trong DB, công ty tồn tại, VAT 0–100, định mức đàm phán 0–99, hệ số giá bán 1–100
- [x] T1.3 Luật validate sheet 2 (cấp): mã gói phải có ở sheet 1, cấp tồn tại, không trùng cấp trong 1 gói, định mức công là số ≥ 0, mỗi gói ≥ 1 cấp
- [x] T1.4 Luật validate sheet 3 (nội dung kiểm tra): hạng mục có tên/ĐVT/SL ở dòng đầu, ĐVT tồn tại, cấp nằm trong tập cấp sheet 2, ghi chú kiểm tra tồn tại, mỗi hạng mục đủ mọi cấp
- [x] T1.5 Luật validate sheet 4 + 5: công ty/nhóm hàng/mã hàng tồn tại, hệ số 0–99.999.999,99, không trùng cặp
- [x] T1.6 `import()`: dựng payload theo khuôn `ServiceRequest` rồi gọi `ServiceService::store()`, mỗi gói 1 transaction + try/catch riêng
- [x] T1.7 Controller `validateImport()` / `import()` + 2 route (đặt TRƯỚC `/{service}`), middleware `checkPermission:Thêm danh mục gói bảo dưỡng`

## Phase 2 — Frontend

- [x] T2.1 `utils/import-multi-sheet-helper.js`: `parseWorkbookSheets()` + `buildMultiSheetTemplate()` (không đụng `import-helper.js`)
- [x] T2.2 `ServiceImportModal.vue`: tái sử dụng `V2BaseImportToolbar` + `V2BaseImportTable`, thêm khối chọn file PDF và 5 tab sheet
- [x] T2.3 Tải file mẫu 5 sheet, dựng thẳng ở FE (bỏ sheet `Danh mục tham chiếu` + API `import-references` — user chốt 22/09)
- [x] T2.4 Gọi validate/import, đổ lỗi về đúng tab + đúng dòng
- [x] T2.5 `services/index.vue`: nút Import (gate `canCreate`) + gắn modal + reload sau import

## Phase 3 — Kiểm thử

- [x] T3.1 Compile FE (vue-template-compiler + babel parse)
- [x] T3.2 Round-trip file mẫu: dựng 6 sheet -> điền -> đọc lại bằng parser của modal -> payload chạy qua `validateImportData()` + `groupByService()` (khớp key 2 đầu)
- [x] T3.3 Đối chiếu DB: `services`, `service_levels`, `service_maintains`, `service_maintain_levels`, `company_service_coefficients`, `service_has_products`, `catalog_histories`
- [x] T3.4 Ca lỗi: trùng mã trong file, trùng tên trong DB, công ty lạ, VAT>100, hệ số<1, PDF chưa chọn, mã gói lạ ở sheet con, hạng mục thiếu cấp, ghi chú lạ, gói không có cấp/hạng mục

## Phase 4 — Chuẩn hoá theo skill (user nhắc 22/09)

- [x] T4.1 Nút Import ở màn danh sách: `secondary status="warning"` + `ri-upload-line` + text "Import Excel", đặt sau Xuất Excel (button-convention 2b/3/4/5, bám 3 màn CSKH đã chuyển)
- [x] T4.2 Popup dựng lại trên khuôn dùng chung `V2BaseModal` (modal-popup mục 0) — bỏ `b-modal` tự khai + ~120 dòng CSS header/body/footer tự chế, chỉ giữ bề ngang 1140px qua `dialogClass`
- [x] T4.3 Footer popup: `tertiary` cho Làm mới + Đóng, Đóng đứng cuối, bỏ `light` (button-convention 2/5)
- [x] T4.4 `$safeLoadingStart()` / `$safeLoadingFinish()` trong `finally` + cờ `submitting` chống bấm 2 lần; lệnh đọc (Tải file mẫu) không bật lớp tải toàn trang (button-convention 6b)
- [x] T4.5 Gắn `unsavedModalMixin` — đóng popup khi đang dở dang thì hỏi "chưa lưu" (skill unsaved-changes 2b)
- [x] T4.6 Compile lại FE + chạy lại round-trip file mẫu sau khi đổi vỏ popup

---

### Checkpoint — 2026-09-22
Vừa hoàn thành: toàn bộ Phase 1 (BE) + Phase 2 (FE) + T3.1 (compile FE) + kiểm thử hàm thuần
`validateRows()` / `pickValidRows()` / `groupByService()` qua tinker (ca hợp lệ + 6 loại lỗi),
xác nhận 3 route đã đăng ký đúng middleware `checkPermission:Thêm danh mục gói bảo dưỡng`.
Đang làm dở: T3.2–T3.4 — chưa chạy ghi thật (`import()` -> `ServiceService::store()`), vì
`CmcS3Helper` trỏ bucket S3 THẬT (key hard-code trong `app/Helper/CmcS3Helper.php`), chạy thử sẽ
đẩy file rác lên bucket production.
Đã bổ sung: file mẫu dựng sẵn `Mau_import_goi_bao_duong.xlsx` (6 sheet, 884 dòng danh mục tham chiếu) ngay trong thư mục này.
Bước tiếp theo: user mở trình duyệt chạy thử luồng Tải file mẫu -> điền -> chọn Excel + PDF ->
Validate -> Import, rồi đối chiếu DB 6 bảng.
Blocked: không

### Checkpoint — 2026-09-22 (bổ sung)
Vừa hoàn thành: Phase 4 — rà lại toàn bộ nút/popup theo `button-convention`, `modal-popup`,
`unsaved-changes` (trước đó code xong mới đọc skill — user nhắc).
Bước tiếp theo: giữ nguyên, chờ user chạy thử trên trình duyệt.
Blocked: không

### Checkpoint — 2026-09-22 (bổ sung 2)
Vừa hoàn thành: bỏ sheet "Danh mục tham chiếu" khỏi file mẫu + gỡ luôn API
`GET import-references` (controller + route + `referenceData()`), đổi gợi ý các cột tra danh mục.
File mẫu trong thư mục này đã dựng lại còn 5 sheet.
Bước tiếp theo: user mở trình duyệt kiểm nút Import Excel + chạy thử luồng.
Blocked: không

## Phase 5 — Chạy thật trên trình duyệt (Playwright, 22/09)

- [x] T5.1 Import 3 gói `ZZTEST-GBD-A/B/C` (id 244/245/246) kèm 4 file PDF — đọc file, chọn PDF, Validate, Import
- [x] T5.2 **Lỗi tìm được khi chạy thật:** `service_levels.benefit_coefficient` NOT NULL → ô "Hệ số công nghệ" trống truyền `null` làm gói thứ 3 rớt (SQL 1048). Đã sửa: trống quy về 1
- [x] T5.3 Thử nhánh trùng mã: import lại cùng file → 2 gói báo "Mã/Tên gói đã tồn tại", 1 gói còn lại vẫn import được sau khi bấm "Bỏ dòng lỗi" + Validate lại
- [x] T5.4 Đối chiếu DB 6 bảng + `catalog_histories` (mỗi gói 1 bản ghi tạo mới) + mở màn chi tiết xem bảng cấp/hạng mục/hàng hoá/PDF
- [x] T5.5 Đổi tên cột sheet 2 cho khớp chữ trên màn (Hệ số công nghệ / Giá bán cơ sở / Gợi ý hàng hoá), giữ `aliases` tên cũ

### Checkpoint — 2026-09-22 (bổ sung 3)
Vừa hoàn thành: chạy thật trên trình duyệt, tìm và sửa 1 lỗi NOT NULL, dữ liệu 3 gói vào đủ 6 bảng.
Dữ liệu test còn trong DB: `ZZTEST-GBD-A` (244), `ZZTEST-GBD-B` (245), `ZZTEST-GBD-C` (246) — chờ
user quyết xóa hay giữ.
Bước tiếp theo: chờ user duyệt để dọn dữ liệu test.
Blocked: không

## Phase 6 — Bỏ phần đính kèm PDF khỏi import (user chốt 22/09)

- [x] T6.1 FE: bỏ khối chọn PDF, cột "File PDF đính kèm" ở sheet 1, state/method liên quan; Import gửi JSON thuần thay vì multipart
- [x] T6.2 BE: bỏ đối chiếu tên file trong `validateRows()`, bỏ tham số `$files` của `import()`, bỏ gom file ở controller
- [x] T6.3 Dựng lại file mẫu (sheet 1 còn 7 cột) + cập nhật tài liệu
- [x] T6.4 Chạy lại trên trình duyệt: import gói `ZZTEST-GBD-D` (id 248) không kèm file → vào đủ 2 cấp · 2 hạng mục · 4 dòng hạng mục×cấp · 1 hệ số công ty · 1 hàng hoá · `attachments = null`

### Checkpoint — 2026-09-22 (bổ sung 4)
Vừa hoàn thành: gỡ toàn bộ phần PDF khỏi luồng import, chạy lại trên trình duyệt xác nhận chạy đúng.
Dữ liệu test còn trong DB: id 244 (A), 245 (B), 247 (C), 248 (D) — chờ user quyết xóa.
Bước tiếp theo: chờ user duyệt dọn dữ liệu test; cân nhắc việc hiện Dung lượng file ở khối đính kèm
dùng chung (việc riêng, ngoài scope import).
Blocked: không

## Phase 7 — Định dạng lại file mẫu (user yêu cầu 22/09, tham khảo màn finance/type-accounts)

- [x] T7.1 Đổi phần ghi file mẫu từ SheetJS sang **ExcelJS** — SheetJS bản cộng đồng không ghi được style
- [x] T7.2 Header nền `D9E1F2` + đậm + canh giữa + viền + cao 30 (đúng màu file `static/Mau_import_loai_tai_khoan.xlsx`); cột bắt buộc chữ đỏ
- [x] T7.3 Dòng gợi ý nền `FFF2CC`, chữ nghiêng xám; đóng băng 2 dòng đầu + cột Mã gói ở 4 sheet con; bộ lọc trên dòng tiêu đề; độ rộng cột theo cấu hình
- [x] T7.4 Tách `buildTemplateWorkbook()` khỏi phần tải file để script sinh file mẫu kèm tài liệu dùng lại đúng hàm của FE
- [x] T7.5 Chạy lại round-trip (5/5 sheet khớp cột) + bấm thật nút "Tải file mẫu" trên trình duyệt, kiểm file tải về đúng định dạng

### Checkpoint — 2026-09-22 (bổ sung 5)
Vừa hoàn thành: file mẫu có định dạng theo khuôn màn Tài chính; file kèm tài liệu đã dựng lại.
Bước tiếp theo: chờ user duyệt dọn 4 gói test (244, 245, 247, 248).
Blocked: không

## Phase 8 — Ví dụ điền sẵn trong file mẫu → ĐÃ HUỶ (user chốt 22/09)

- [x] T8.1 Đã thêm sheet thứ 6 `Ví dụ 2 gói` rồi **gỡ bỏ theo yêu cầu user** — file mẫu quay về đúng 5 sheet dữ liệu
- [x] T8.2 Gỡ sạch code liên quan (`addExampleSheet()` ở helper, `EXAMPLE_ROWS`/`EXAMPLE_NOTES`/`exampleSheet` ở modal), không để lại code chết
- [x] T8.3 Dựng lại file mẫu kèm tài liệu + bấm thật nút "Tải file mẫu": file về đúng 5 sheet, parser đọc đúng

### Checkpoint — 2026-09-22 (bổ sung 6)
Vừa hoàn thành: file mẫu chốt ở 5 sheet có định dạng (không kèm sheet ví dụ).
Bước tiếp theo: chờ user duyệt dọn 4 gói test (244, 245, 247, 248).
Blocked: không

---

## Trạng thái chốt phiên 22/09/2026

**Code xong, chạy thật trên trình duyệt, CHƯA COMMIT.**

| Repo | File |
| --- | --- |
| hrm-api | `Modules/CustomerCare/Services/ServiceImportService.php` (mới) |
| hrm-api | `Modules/CustomerCare/Http/Controllers/V1/ServiceController.php` (+3 method, +1 helper) |
| hrm-api | `Modules/CustomerCare/Routes/api.php` (+2 route) |
| hrm-client | `pages/customer-care/services/components/ServiceImportModal.vue` (mới) |
| hrm-client | `utils/import-multi-sheet-helper.js` (mới) |
| hrm-client | `pages/customer-care/services/index.vue` (nút Import Excel + gắn modal + `handleImported`) |

> 4 file khác đang `M` trong git (`ServiceRequest.php`, `ServiceService.php`, `ServiceFormComponent.vue`,
> `V2BaseAttachmentSection.vue`) là việc `attachment_urls` đang làm dở TỪ TRƯỚC, **không phải của feature này**.

**Việc còn treo (chờ user quyết):**

1. **Dữ liệu test chưa xoá** — `ZZTEST-GBD-A` (244), `B` (245), `C` (247), `D` (248). A/B/C có file PDF
   đã đẩy lên bucket S3 production (hệ thống không có luồng xoá file S3).
2. **Cột "Dung lượng" ở khối đính kèm luôn hiện `—`** với file đã lưu — nợ có sẵn của
   `V2BaseAttachmentSection` (chỉ biết dung lượng file vừa chọn trong phiên), KHÔNG do import.
   3 hướng sửa đã nêu: BE `headObject` S3 khi mở chi tiết / lưu size lúc upload / FE gọi HEAD.
   Đụng component dùng chung 3 màn → việc riêng, ngoài scope import.
3. **Gói import xong chưa có PDF** → mở màn Sửa rồi Lưu thì `ServiceRequest` đòi đính kèm file.
   Muốn nới thì phải sửa rule bên form.
4. **Chọn lại file Excel trùng tên** không bắn `change` nên bảng giữ dữ liệu cũ (phải bấm Làm mới).
   Hành vi chung của mọi màn import; sửa được bằng cách xoá `input.value` sau mỗi lần đọc file.

**Lưu ý môi trường:** trong phiên này `V2BaseImportToolbar` / `V2BaseImportModal` / `V2BaseImportTable`
/ `CatalogImportMixin` bị người khác sửa trên đĩa (ẩn nhóm nút "Hiển thị" từ 21/09). Modal của feature
này dùng lại toolbar nên **nút "Chỉ dòng lỗi" cũng không còn hiện** — state `onlyErrors` vẫn giữ nguyên,
bật lại toolbar là chạy, không phải sửa gì bên này.
