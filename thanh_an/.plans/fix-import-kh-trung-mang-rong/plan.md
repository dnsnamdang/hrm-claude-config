# Fix: Import khách hàng báo trùng "mảng hàng hóa rỗng" — @khoipv

## Bối cảnh
Import Excel khách hàng (`pages/category/customer` → type `category-customer`), sheet 2 "Người phụ trách".
Lỗi thực tế: `Nhân viên "Hoàng Việt Phương" (NV.00006) và "Dương Thị Hiệu" (NV.00010) cùng phòng "Cung Ứng"
không được phụ trách cùng mảng hàng hóa "" cho khách hàng "CÔNG TY CỔ PHẦN VÂN LONG (Bệnh viện Cuộc Sống Điện Biên)".`

Root cause: `PersonChargeImport::validateDuplicateDepartmentProducts()` dòng 134 —
`explode(',', '')` trả về `['']` nên 2 nhân viên cùng phòng cùng để TRỐNG cột mảng hàng hóa
sẽ `array_intersect` ra `['']` → bị coi là trùng mảng.

Phần import thật (`CategoryCustomerImport::importPersonChargeData()`) đã `array_filter` và có sẵn nhánh
tạo người phụ trách với `array_product_id = null` → nghiệp vụ CHO PHÉP người phụ trách không có mảng.
Chỉ có validate là chặn nhầm.

## Phase 1 — BE
- [x] Lọc bỏ phần tử rỗng khi tách `phu_trach_mang_hang_hoa` trong `validateDuplicateDepartmentProducts()`
      (`Modules/Payroll/ExcelImports/PersonChargeImport.php:134`)
- [x] Verify: 2 người cùng phòng + cùng KH + mảng rỗng → KHÔNG báo lỗi
- [x] Verify không hồi quy: 2 người cùng phòng + cùng KH + trùng mảng thật → VẪN báo lỗi

## Phase 2 — FE
Không có. Chỉ sửa BE, không đụng API contract / migration / quyền.

### Checkpoint — 2026-09-16
Vừa hoàn thành: sửa `PersonChargeImport.php:134` — lọc bỏ mảng hàng hóa rỗng trước khi `array_intersect`.
Verify offline 6/6 ca: mảng rỗng 2 bên / khoảng trắng / dấu phẩy thừa → hết báo lỗi; trùng mảng thật vẫn báo lỗi; khác mảng vẫn OK.
Đang làm dở: không có.
Bước tiếp theo: user import lại file Excel thật để xác nhận (chỉ sửa BE → không cần build client, chỉ cần BE nhận file mới).
Blocked:
