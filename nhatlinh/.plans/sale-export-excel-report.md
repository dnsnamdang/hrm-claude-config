# Báo cáo: Thêm nút Xuất Excel — Báo giá bán & Hợp đồng

## Status: DONE

---

## Danh sách file tạo mới / sửa

### BE — Tạo mới
- `nhatlinh-api/Modules/Sale/Exports/SaleQuotationExport.php`
- `nhatlinh-api/Modules/Sale/Exports/SaleContractExport.php`

### BE — Sửa
- `nhatlinh-api/Modules/Sale/Http/Controllers/Api/V1/QuotationController.php` — thêm `use Excel`, `use SaleQuotationExport`, method `export()`
- `nhatlinh-api/Modules/Sale/Http/Controllers/Api/V1/SaleContractController.php` — thêm `use Excel`, `use SaleContractExport`, method `export()`
- `nhatlinh-api/Modules/Sale/Routes/api.php` — thêm `GET /quotations/export` và `GET /contracts/export` (đặt trước `/{id}`)

### FE — Sửa
- `nhatlinh-client/pages/sale/quotation/index.vue` — thêm nút Xuất Excel vào `#actions` (sau Tạo mới), thêm method `exportExcel()`
- `nhatlinh-client/pages/sale/contract/index.vue` — import + đăng ký `V2BaseButton`, thêm slot `#actions` với nút Xuất Excel, thêm method `exportExcel()`

---

## Resource list đã dùng + key cột

**SaleQuotationResource** (`Modules/Sale/Transformers/SaleQuotationResource/SaleQuotationResource.php`):
| Key Excel | Key Resource |
|-----------|-------------|
| Mã | `code` |
| Khách hàng | `customer_name` |
| Ngày báo giá | `quotation_date` |
| Tổng tiền | `total_amount` (number) |
| Trạng thái | `status_name` |
| Ngày tạo | `created_at` |
| Người tạo | `employee_create_name` |
| Ngày duyệt | `approved_at` |
| Người duyệt | `employee_approve_name` |

**SaleContractResource** (`Modules/Sale/Transformers/SaleContractResource/SaleContractResource.php`):
| Key Excel | Key Resource |
|-----------|-------------|
| Mã | `code` |
| Khách hàng | `customer_name` |
| Ngày hợp đồng | `contract_date` |
| Tổng tiền | `total_amount` (number) |
| Trạng thái | `status_name` |
| Ngày tạo | `created_at` |
| Người tạo | `employee_create_name` |
| Ngày duyệt | `approved_at` |
| Người duyệt | `employee_approve_name` |

---

## Kết quả php -l

- `SaleQuotationExport.php` — No syntax errors
- `SaleContractExport.php` — No syntax errors
- `QuotationController.php` — No syntax errors
- `SaleContractController.php` — No syntax errors
- `Routes/api.php` — No syntax errors

(Warning về imagick.so là lỗi môi trường local, không liên quan)

---

## Fix sau review (Reviewer Approved — Spec ✅, Quality ✅)

Áp 3 fix nhỏ:
1. **Ép kiểu số tổng tiền** — `map()` cột tổng tiền ở cả 2 Export: `(float) ($row['total_amount'] ?? 0)` để Excel chắc chắn nhận dạng số.
2. **Giải phóng Blob URL + dọn DOM** — thêm `document.body.removeChild(fileLink)` + `window.URL.revokeObjectURL(fileURL)` sau `fileLink.click()` ở cả 2 file FE.
3. **Blob có MIME type** — `new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })` ở cả 2 file FE.

php -l sau fix: 2 file Export — No syntax errors (sạch).

---

## Concerns

Không có concerns chặn. Một ghi chú nhỏ:
- `SaleQuotationResource::collection($data)->resolve()` gọi `toArray()` trên từng item, trong đó có `isCanEdit()`, `isCanDelete()`... — các trường này sẽ có trong `$rows` nhưng Export chỉ map đúng 10 cột cần thiết, các cột thừa bị bỏ qua hoàn toàn — không ảnh hưởng.
- `total_amount` ép `(float)` để Excel tính toán được.
