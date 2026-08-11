# Design — Xuất CSV / Excel màn khách hàng (`/assign/customers`)

- Nhánh: `gop_db` (cả `hrm-api` + `hrm-client`) · Phụ trách: @khoipv · Ngày: 2026-08-10
- **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-10-customer-export-file-design.md`

## Mục tiêu

Thêm 2 nút **Xuất CSV** / **Xuất Excel** trên toolbar danh sách khách hàng, hành vi tương đương ERP
(`erp/.../Sale/CustomersController@exportCSV|exportExcel`). Không port Xuất PDF.

## Scope

- BE: 2 route export + `CustomerService::exportQuery()` + 2 class export (`app/ExcelExport/`)
  + thêm key quyền `export` vào `ErpPermissionHelper`
- FE: 2 nút + method `exportFile()` + tách `buildApiFilters()` trong `pages/assign/customers/index.vue`
- Không migration, không thêm permission vào `PermissionsTableSeeder` (dùng quyền ERP sẵn có)

## Quyết định lớn

| # | Quyết định |
| --- | --- |
| 1 | Excel **tải trực tiếp**, KHÔNG gửi mail như ERP (không phụ thuộc queue worker + SMTP) |
| 2 | Bộ cột giống ERP: **CSV 5 cột**, **Excel 20 cột** |
| 3 | Quyền ERP `Xuất dữ liệu khách hàng` (thêm key `export` vào `ErpPermissionHelper::CUSTOMER_PERMISSIONS`) |
| 4 | **Không giới hạn số dòng** — tối ưu bằng `FromQuery` + chunk 5.000 + chỉ select 26 cột cần (thay `customers.*` 59 cột) + cột phụ bằng JOIN/subquery + `StringValueBinder` + bỏ `ShouldAutoSize`. Đo trên 17.542 KH: CSV 25,3s→~13s, XLSX 60,2s→~32s |
| 5 | **Giữ luật che SĐT** của HRM trong file xuất (KH cá nhân không phải "của mình" → `-`), tránh export thành cửa hậu lộ SĐT |
| 6 | Không port Xuất PDF |

## Bug ERP phát hiện khi khảo sát (bản HRM làm đúng)

- `customer_export.blade.php`: **19 `<th>` cho 20 `<td>`** — thiếu header *Chức vụ liên hệ* → lệch cột.
- CSV ERP không có BOM UTF-8 → mở bằng Excel vỡ dấu tiếng Việt.
- Binder mặc định đổi SĐT/MST `"0912…"` thành số → mất số 0 đứng đầu (bản HRM dùng `StringValueBinder`).

## Bổ sung 2026-08-10 — mẫu Excel + Xuất PDF

- **Excel** theo chuẩn HRM: logo letterhead · tiêu đề `DANH SÁCH KHÁCH HÀNG` gộp ô đậm căn giữa ·
  header nền xám đậm có viền · dữ liệu có viền · đóng băng dòng header · autofilter.
  Chi phí: 17.544 KH từ ~32s lên ~44s, RAM 206 → 266 MB.
- **PDF**: cài `barryvdh/laravel-dompdf ^1.0` (team phải `composer install`). 5 cột như ERP,
  A4 ngang. Bắt buộc `font-family: "DejaVu Sans"` — font mặc định dompdf không có dấu tiếng Việt.
- ⚠️ **PDF không xuất nổi toàn bộ danh sách.** User chốt không giới hạn số dòng nên code không chặn,
  nhưng đo thật: trần ~3.000 dòng ở `memory_limit` 512M (đã nâng từ ~1.000 nhờ chia nhỏ bảng
  200 dòng/bảng để giảm Cellmap của dompdf). Xuất 17.544 KH sẽ chết request.
  Chờ user chọn: chặn số dòng / nâng memory_limit / queue + mail.

## Không đụng tới

`CustomerService::index()` · `CustomerListResource` · `config/excel.php` · `PermissionsTableSeeder`
