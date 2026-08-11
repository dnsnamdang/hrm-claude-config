# Plan — Xuất CSV / Excel màn khách hàng (`/assign/customers`)

Nhánh: `gop_db` (hrm-api + hrm-client) · Phụ trách: @khoipv
Design: `.plans/gop-db/customer-export-file/design.md`
Spec: `docs/superpowers/specs/gop-db/2026-08-10-customer-export-file-design.md`

---

## Phase 1 — Backend

- [x] BE `app/Helpers/ErpPermissionHelper.php` — thêm `'export' => 'Xuất dữ liệu khách hàng'` vào `CUSTOMER_PERMISSIONS`
- [x] BE `Modules/Assign/Services/CustomerService.php` — thêm `exportQuery(Request)`: gọi lại `index()` + cột phụ bằng JOIN/subquery (nhóm khách, hãng xe, công ty mẹ, thôn/xóm, người đại diện, liên hệ đầu tiên, người tạo/sửa) + select lại 26 cột cần thay `customers.*`
- [x] BE `app/ExcelExport/CustomerExportFormatter.php` — trait format dùng chung (clean ký tự rác, loại KH, địa chỉ, trạng thái, che SĐT)
- [x] BE `app/ExcelExport/CustomerCsvExport.php` — `FromQuery + WithHeadings + WithMapping + WithCustomCsvSettings(use_bom) + WithCustomChunkSize(5000) + StringValueBinder`, 5 cột
- [x] BE `app/ExcelExport/CustomerExcelExport.php` — như trên + `WithColumnWidths`, 20 cột (có `Chức vụ liên hệ`)
- [x] BE `Modules/Assign/Http/Controllers/Api/V1/CustomerController.php` — `exportCsv()` + `exportExcel()`
- [x] BE `Modules/Assign/Routes/api.php` — 2 route `export-csv` / `export-excel` đặt TRƯỚC `/{id}`, middleware `erpPermission:Xuất dữ liệu khách hàng`
- [x] BE verify `php -l` sạch toàn bộ file sửa

## Phase 2 — Frontend

- [x] FE `pages/assign/customers/index.vue` — tách `buildApiFilters()` dùng chung cho `loadData()` + export
- [x] FE — thêm computed `canExport` (từ `perm.export`) + `perm.export` trong data & `loadPermissions()`
- [x] FE — 2 nút `Xuất CSV` / `Xuất Excel` trong slot `#actions` (secondary + `ri-download-line`, theo button-convention), có cờ `exporting` chặn bấm liên tục
- [x] FE — method `exportFile(type)`: arraybuffer → blob download, `$nuxt.$loading`, toast, bỏ qua toast khi 403
- [x] FE verify parse sạch (vue-template-compiler + babel)

## Phase 3 — Verify tự động (đã chạy trên DB gop_db thật)

- [x] Route đăng ký đúng + đứng TRƯỚC `/{id}`, middleware `erpPermission:Xuất dữ liệu khách hàng` (script `check_routes.php`, vì `artisan route:list` chết ở route file Timesheet)
- [x] Xuất thật 17.542 KH: CSV 2,9 MB / 17.543 dòng ~13s · XLSX 2,1 MB ~32s, RAM đỉnh 206 MB
- [x] CSV có BOM UTF-8, tiếng Việt đọc đúng
- [x] XLSX: 20 header khớp 20 cột dữ liệu; SĐT `0948365335` giữ nguyên số 0 đứng đầu
- [x] Che SĐT khớp màn danh sách: KH 71/83/84 (cá nhân, người khác tạo) → cả list lẫn file đều ra `-` dù DB có số thật
- [x] Phân quyền: employee 13 (có quyền) → `export=true` + HTTP 200; employee 25 (không có quyền) → `export=false` + HTTP 403

## Phase 5 — Định dạng mẫu Excel + Xuất PDF (yêu cầu bổ sung 2026-08-10)

Chốt với user: mẫu Excel theo **chuẩn HRM** (logo + tiêu đề + header đậm có viền + dữ liệu có viền);
PDF **cài `barryvdh/laravel-dompdf`** như ERP; PDF **không giới hạn số dòng, giống ERP**
(user đã được cảnh báo dompdf khó kéo nổi 17.5k dòng và vẫn chọn giữ nguyên hành vi ERP —
sẽ đo và báo lại ngưỡng thực tế).

- [x] BE `CustomerExcelExport` — `WithCustomStartCell('A3')` + `WithEvents::AfterSheet`: logo dòng 1, tiêu đề gộp `A2:T2` đậm 16 căn giữa, header nền `D9D9D9` đậm có viền, dữ liệu có viền, `freezePane A4`, `setAutoFilter A3:T3`
- [x] BE đo lại Excel sau khi thêm định dạng: **~32s → ~44s**, RAM 206 → 266 MB (vẽ viền ~350k ô)
- [x] BE cài `barryvdh/laravel-dompdf ^1.0` (composer.json + lock — team phải `composer install`)
- [x] BE `app/PdfExport/CustomerPdfExport.php` — dùng chung trait `CustomerExportFormatter`, `rowChunks()` cắt 200 dòng/bảng
- [x] BE blade `resources/views/exports/customers_pdf.blade.php` — 5 cột như ERP, A4 ngang, logo + tiêu đề, `font-family: "DejaVu Sans"`
- [x] BE `CustomerController::exportPdf()` + route `export-pdf` (trước `/{id}`, `erpPermission:Xuất dữ liệu khách hàng`)
- [x] BE đo PDF nhiều mức dữ liệu → xác định ngưỡng thực tế (bảng số ở checkpoint)
- [x] FE nút **Xuất PDF** (secondary, `ri-file-pdf-line`) + nhánh `pdf` trong `exportFile()`
- [x] Verify Excel: 20/20 header, tiêu đề gộp ô đậm căn giữa, header nền xám có viền, dữ liệu có viền tới dòng cuối (17.547), đóng băng `A4`, autofilter `A3:T3`, 1 logo ở `A1`
- [x] Verify PDF: nhúng `DejaVuSans` + `DejaVuSans-Bold`, rút text ra đúng dấu tiếng Việt ("NGUYỄN TUẤN ANH", "Tỉnh Đắk Lắk", "Phường Đống Đa")
- [x] Verify 3 route export đăng ký đúng, đứng trước `/{id}`, đúng middleware

---

### Checkpoint — 2026-08-10 (Phase 5)
Vừa hoàn thành: định dạng mẫu Excel theo chuẩn HRM + chức năng Xuất PDF.

**⚠️ Số đo PDF (`memory_limit = 512M`) — user chọn KHÔNG giới hạn số dòng nên code không chặn:**

| Số dòng | 1 bảng lớn | Nhiều bảng 200 dòng (đang dùng) |
| --- | --- | --- |
| 1.000 | 15,9s · 326 MB | 8,4s · 182 MB |
| 2.000 | vỡ bộ nhớ | 30,2s · 308 MB |
| 3.000 | vỡ bộ nhớ | 30,7s · 436 MB |
| 4.000 | vỡ bộ nhớ | vỡ bộ nhớ |

Chia nhỏ bảng nâng trần từ ~1.000 lên **~3.000 dòng**. **Không xuất nổi toàn bộ 17.544 KH**
(ước tính cần ~2,5 GB RAM, thời gian tăng phi tuyến). Bấm Xuất PDF khi không lọc sẽ chết request —
memory exhausted là fatal error, `try/catch` không bắt được. Đã báo user, chờ quyết định:
chặn số dòng / nâng memory_limit riêng cho action / đẩy queue + mail.

Đang làm dở: không có.
Bước tiếp theo: user build FE → test tay; quyết hướng xử lý ngưỡng PDF.
Blocked: không có.

## Phase 4 — Test tay (user)

- [x] Bấm Xuất CSV / Xuất Excel trên UI → file tải về đúng tên, mở được
- [x] Đặt bộ lọc rồi xuất → số dòng trong file khớp tổng của bảng
- [x] Đăng nhập user không có quyền `Xuất dữ liệu khách hàng` → không thấy 2 nút

---

### Checkpoint — 2026-08-10
Vừa hoàn thành: toàn bộ Phase 1 + 2 + 3 (BE + FE + verify tự động trên DB thật).
Đang làm dở: không có.
Bước tiếp theo: user build FE (`npm run dev` hrm-client) → test tay Phase 4.
Blocked: không có.

---

### Checkpoint — 2026-08-11 (HOÀN THÀNH)
Vừa hoàn thành: user test trình duyệt xong Phase 4 (CSV / Excel / PDF) → **feature HOÀN THÀNH**.
Đang làm dở: không có.
⚠️ CÒN NỢ (không chặn nghiệm thu): ngưỡng **Xuất PDF ~3.000 dòng** vẫn để ngỏ theo quyết định
"không giới hạn số dòng" — bấm Xuất PDF khi không lọc (17.544 KH) sẽ chết request vì memory exhausted.
Khi nào muốn xử lý thì chọn 1 trong 3: chặn số dòng / nâng `memory_limit` riêng cho action / queue + mail.
Bước tiếp theo: không có (đã chuyển sang mục "Hoàn thành" ở `.plans/gop-db/STATUS.md`).
Blocked: không có.
