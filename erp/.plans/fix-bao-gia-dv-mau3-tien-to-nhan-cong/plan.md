# Fix — Báo giá dịch vụ mẫu số 3: đổi tiền tố công nhân công

## Yêu cầu
Mẫu in báo giá dịch vụ **mẫu số 3** (`print_type=service_quotation`, template `BGDV-02A`): dòng dịch vụ engineering_work đang auto tiền tố "Công tháo lắp sửa chữa thiết bị" → đổi thành "Chi phí nhân công".

## Vị trí
- `app/Services/PrintTemplate/WarrantyRepairServiceQuotationPrint.php` → `getServiceTable()` dòng 1639.
- Dispatch: `WarrantyRepairServiceQuotationsController@print` nhánh `service_quotation` → `getDataQuotationPrint()` → `getServiceTable()`.
- Mẫu 1 (`contract_1`) / mẫu 2 (`contract_2`) dùng `getTable()` — đã là "Chi phí nhân công", không đụng.

## Tasks
- [x] Đổi `$workName = 'Công tháo lắp sửa chữa thiết bị'` → `'Chi phí nhân công'` (dòng 1639). Giữ nguyên phần ` - device_error_name`.
- [ ] User in thử mẫu số 3 đối chiếu.

### Checkpoint — 2026-06-11
Vừa hoàn thành: sửa tiền tố ở getServiceTable (mẫu 3)
Bước tiếp theo: user in thử
Blocked:
