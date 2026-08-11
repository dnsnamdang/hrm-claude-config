# Plan — Import Excel Khách hàng (`/assign/customers`)

Nhánh `gop_db` · @khoipv · Spec: `docs/superpowers/specs/gop-db/2026-08-10-customer-import-excel-design.md`

## Phase 0 — Khảo sát

- [x] Liệt kê toàn bộ import Excel bên ERP (routes/web.php + app/ExcelImports)
- [x] Liệt kê import hiện có bên HRM (routes Modules/* + V2BaseImportModal usages)
- [x] Đối chiếu → chốt gap = Khách hàng / Quốc gia / Thôn-xóm; user chọn Khách hàng
- [x] Đọc `CustomerService::save()` + `SaveCustomerRequest` + `TpCustomer::sync*`
- [x] Đọc mẫu tham chiếu: `ApplicationService::parseCustomerScopePairs()`, `BomListController::importTemplate()`, `pages/assign/application/index.vue`
- [x] Đọc `V2BaseImportModal` + `utils/import-helper.js` (phát hiện: `requiredFields`/`validationRules` là prop chết; `handleImport` lọc theo `__isValid`)

## Phase 1 — Backend

- [x] Tạo `Modules/Assign/Services/CustomerImportService.php`
  - [x] `groupRows()` — gom cha/con theo cột Tên, giữ `rowIndex` gốc, tách dòng con mồ côi
  - [x] Preload danh mục 1 lần + cache trong request (`$catalogMaps`)
  - [x] `validateImportData()` — trả rows 1:1, `isValid` đồng bộ theo nhóm
  - [x] `buildPayload()` / `buildDeputies()` / `buildContacts()` / `buildAccounts()`
  - [x] `importCustomers()` — mỗi nhóm 1 try/catch, gọi `CustomerService::save()`
  - [x] `assertImporterReady()` — chặn sớm khi user chưa gắn nhân sự
  - [x] `templateSampleRows()` / `scopeCatalogRows()` — dòng mẫu lấy danh mục THẬT
- [x] `CustomerController`: `validateImport()`, `import()`, `importTemplate()` + 2 helper dựng sheet phụ
- [x] `Modules/Assign/Routes/api.php`: 3 route đặt TRƯỚC `/{id}`, middleware `erpPermission:Thêm khách hàng`
- [x] `php -l` 3 file BE — PASS

## Phase 2 — Frontend

- [x] `pages/assign/customers/index.vue`: nút Import (secondary, `ri-upload-line`, sau nút Tạo mới, `v-if="canCreate"`)
- [x] Gắn `V2BaseImportModal` + `importColumns` 25 cột + `importRequiredFields` + `importValidationRules`
- [x] 4 method: `mapImportRows`, `handleValidateImportData`, `handleImportCustomers`, `handleDownloadImportTemplate` (+ `handleImportError`, `openImportModal`)
- [x] Tải file mẫu bằng axios + Bearer token (endpoint nằm trong nhóm auth, không dùng thẻ `<a>` trực tiếp)
- [x] Verify parse SFC (@babel/parser) + compile template (vue-template-compiler) — PASS

## Phase 3 — Verify

- [x] Đối chiếu 25 cột FE ↔ `TEMPLATE_HEADERS` BE bằng đúng `normKey()` của import-helper — 25/25 khớp, đúng thứ tự
- [x] Validate file mẫu chuẩn (3 dòng: cha tổ chức + con + cá nhân) → 3/3 hợp lệ
- [x] Validate 8 ca lỗi: dòng con mồ côi · sai nhóm KH + sai tỉnh · thiếu MST · sai/không tồn tại cặp mã lĩnh vực · thiếu người liên hệ · SĐT cá nhân sai định dạng · đối tượng không hợp lệ → bắt đúng từng ca
- [x] Trùng MST trong chính file → báo đúng số dòng đối chiếu
- [x] Trùng MST / CCCD với dữ liệu đã có trên hệ thống → bắt đúng
- [x] Sai phân cấp địa danh (xã không thuộc huyện) → bắt đúng
- [x] Nhóm không bị xé đôi: cha hợp lệ + con lỗi → cả 2 dòng `isValid=false`
- [x] Import thật (bọc transaction rồi rollback): 2 KH từ 3 dòng · 1 nhóm KH · 1 đại diện · **2 liên hệ** · **2 tài khoản NH** · 1 loại hình · 1 lĩnh vực · mã KH tự sinh (`50TPHXBI-277`)
- [x] `bank_id` + `bank_province_id` resolve đúng khi tên ngân hàng khớp danh mục
- [x] Loại hình suy ra đúng từ vế trái cặp mã (không có cột Loại hình riêng)
- [x] Rollback sạch, không sót bản ghi nào
- [x] File mẫu tải về: 3 sheet (Data / Loại hình - Lĩnh vực 179 dòng / Hướng dẫn), 25 header, dòng mẫu dùng danh mục thật
- [ ] User test trên trình duyệt: mở `/assign/customers` → Import → tải mẫu → nhập → validate → import → soi lại danh sách
- [ ] Kiểm tra KH import xong hiện đúng ở màn ERP `admin/customers/{id}/edit` (2 trường Loại hình / Lĩnh vực)

---

### Checkpoint — 2026-08-10
Vừa hoàn thành: CODE DONE + VERIFY BE toàn bộ Import Excel khách hàng cho `/assign/customers`.
- BE: `CustomerImportService` (mới, ~900 dòng) + 3 endpoint trên `CustomerController` + 3 route đặt trước `/{id}`.
  Import gọi lại đúng `CustomerService::save()` nên tự sinh mã, ghi pivot loại hình/lĩnh vực, người đại diện,
  người liên hệ, tài khoản ngân hàng y hệt tạo tay. Không migration, không permission mới.
- FE: nút Import + `V2BaseImportModal` 25 cột + 6 method trong `pages/assign/customers/index.vue`.
- Verify: 9 ca test chạy thật qua tinker (bọc transaction + rollback, không để lại dữ liệu rác);
  đối chiếu header FE↔BE 25/25; SFC parse + template compile PASS; `php -l` PASS.
Đang làm dở: (không)
Bước tiếp theo: user build FE (`npm run dev` hoặc build) → test trình duyệt luồng 4 bước → xác nhận KH mới hiện đúng ở cả HRM và ERP.
Blocked: (không)

### Checkpoint — 2026-08-10 (sửa theo góp ý)
Vừa hoàn thành: Gộp 2 cột Loại hình + Lĩnh vực thành **1 cột duy nhất** cho đúng cách màn
`/assign/application` — bỏ hẳn cột `Loại hình hoạt động khách hàng`, loại hình suy ra từ vế trái của
cặp `MãLoạiHình:MãLĩnhVực`. File mẫu 26 → **25 cột**.
- BE: bỏ `parseActivityTypeCodes()`, bỏ key `activityTypeCode`, sửa `TEMPLATE_HEADERS` +
  `templateSampleRows()` + sheet Hướng dẫn.
- FE: bỏ cột `ActivityTypeCode` khỏi `importColumns` và `mapImportRows`.
- Verify chạy lại toàn bộ 9 ca: PASS; header FE↔BE 25/25; file mẫu 25 cột đọc lại đúng.
Đánh đổi đã báo user: KH chỉ có Loại hình mà không có Lĩnh vực nào thì không khai được qua import.
Bước tiếp theo: user build FE + test trình duyệt.

## Phase 4 — Làm đẹp file mẫu

- [x] `TEMPLATE_LAYOUT` + `TEMPLATE_GROUP_FILLS` + `TEMPLATE_TEXT_COLUMNS` trong service
- [x] Tách `buildImportDataSheet()` khỏi `importTemplate()` cho dễ đọc
- [x] Header: nhóm cột theo màu nền, dấu * đỏ bằng RichText, cao 42, wrap, viền mảnh
- [x] Dòng 2 ghi chú nền vàng nhạt gộp `A2:Y2`; dòng con mẫu nghiêng + nền `FFFBF0` + comment ở `A4`
- [x] Ép `NumberFormat` Text cho 6 cột SĐT/CCCD/MST/Fax/SĐT liên hệ/Số TK + ghi ô bằng `setCellValueExplicit`
- [x] Dropdown Đối tượng: 1 `DataValidation` cho `B3:B1000` qua `setSqref` (không lặp 198 ô)
- [x] `freezePane('C3')` · autofilter · ẩn gridline · độ rộng cột khai cứng · in khổ ngang lặp dòng 1-2
- [x] Sheet tra mã: thêm cột "Chuỗi dán vào cột Lĩnh vực" ghép sẵn cặp mã, kẻ dòng xen kẽ, freeze + filter
- [x] Sheet Hướng dẫn: tiêu đề nền xanh chữ trắng, mục đánh số in đậm nền nhạt, freeze dòng đầu
- [x] Tab color 3 sheet

### Checkpoint — 2026-08-10 (làm đẹp file mẫu)
Vừa hoàn thành: dựng lại file mẫu cho tử tế.
- Sửa 1 lỗi API khi làm: `SheetView::setShowGridLines()` không tồn tại → đúng là `Worksheet::setShowGridlines()`.
- Verify trên file .xlsx sinh thật: 25/25 header đọc lại khớp nguyên văn dù dùng RichText (quan trọng —
  RichText mà lệch là FE báo "File không đúng mẫu"); FE map cột từ chính file đó PASS 25/25;
  freeze `C3`; autofilter `A1:Y1`; 6 cột định dạng `@`; đúng 1 thẻ `dataValidation` cho `B3:B1000`;
  `showGridLines="false"` có trong XML (reader của PhpSpreadsheet không đọc lại được attribute này,
  đã soi raw XML để xác nhận). File 38,9 KB.
Bước tiếp theo: user build FE + test trình duyệt.

### Checkpoint — 2026-08-10 (kẻ bảng nhập)
Vừa hoàn thành: user phản hồi "bên dưới các dòng không có table" — đúng, do đã tắt gridline nên vùng
dưới 3 dòng mẫu trắng trơn.
- Kẻ thêm **40 dòng trống có viền** (bảng chạy tới dòng 45) + viền ngoài `MEDIUM` bo khối bảng.
- Nhân tiện gọn lại: chuyển ép định dạng Text từ dải ô `D3:D1000` sang **style cấp cột** `D:D`
  → `HighestRow` 1000 → 45, file 41,2 KB → **25,8 KB**, mà vẫn phủ mọi dòng user dán vào.
- Verify: mô phỏng đúng `parseExcelFile` trên file sinh thật → đọc 45 dòng, bỏ 42 dòng trống,
  giữ đúng **3 dòng** dữ liệu (cha tổ chức / dòng con / cá nhân). Viền dừng đúng dòng 45, dòng 46 sạch.
  Chạy lại toàn bộ test validate + import: PASS, rollback sạch.
Bước tiếp theo: user build FE + test trình duyệt.

### Checkpoint — 2026-08-11 (HOÀN THÀNH)
Vừa hoàn thành: user test trình duyệt xong (tải file mẫu → 4 bước import → dữ liệu vào đúng)
→ **feature HOÀN THÀNH**.
Đang làm dở: không có.
Bước tiếp theo: không có (đã chuyển sang mục "Hoàn thành" ở `.plans/gop-db/STATUS.md`).
Blocked: không có.
