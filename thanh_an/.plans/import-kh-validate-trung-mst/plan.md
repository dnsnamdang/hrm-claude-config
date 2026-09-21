# Fix: Import khách hàng không validate trùng mã số thuế — @khoipv

## Bối cảnh
Form thêm/sửa khách hàng (`Modules/Category/Http/Requests/StoreCategoryCustomerRequest.php:26`) đã chặn trùng MST
bằng rule `unique:category_customers,tax_code,{id}`.

Nhưng luồng **import Excel** (`Modules/Payroll/ExcelImports/CategoryCustomerImport.php`) thì không:
- `createOrUpdateCustomer()` dòng 255 dò bản ghi cũ bằng **tên khách hàng**, không phải MST
- dòng 294 gán thẳng `$customer->tax_code = $data['ma_so_thue']` mà không kiểm tra trùng
- `validateRow()` cũng không có rule nào cho `ma_so_thue`

→ Import 2 khách hàng khác tên nhưng cùng MST vẫn vào được DB, lọt qua rule của form.
Bảng `category_customers` cũng **không có unique index** trên `tax_code` nên DB không cản.

## Phase 1 — BE
- [x] Thêm `validateDuplicateTaxCode()` vào `CategoryCustomerImport`: chặn trùng MST giữa các dòng trong file
      và trùng với khách hàng đã có trên hệ thống
- [x] Gộp lỗi MST vào vòng validate sheet 1 trong `validateAllSheets()` (giữ nguyên cơ chế all-or-nothing + bảng lỗi trả về)
- [x] Verify: cùng MST khác tên trong file → báo lỗi; MST đã có trên hệ thống của KH khác → báo lỗi
- [x] Verify không hồi quy: cập nhật KH cũ giữ nguyên MST của chính nó → KHÔNG báo lỗi; MST để trống → bỏ qua

## Phase 2 — FE
Không có. Chỉ sửa BE, không đụng API contract / migration / quyền.

## Quyết định
- MST rỗng thì bỏ qua check (import hiện KHÔNG bắt buộc MST — `requiredFields` đang comment dòng `ma_so_thue`).
  Giữ nguyên, không tự thêm bắt buộc.
- Khớp KH cũ vẫn theo **tên** như logic import sẵn có → cùng tên = cùng khách hàng, được giữ MST của mình.
- Không thêm unique index DB (dữ liệu cũ có thể đã trùng) — chỉ chặn ở tầng application.

### Checkpoint — 2026-09-21
Vừa hoàn thành: thêm `validateDuplicateTaxCode()` vào `Modules/Payroll/ExcelImports/CategoryCustomerImport.php`
(sau `validateRow()`, ~dòng 110) và gộp lỗi vào vòng validate sheet 1 trong `validateAllSheets()`.
Verify bằng tinker trên DB `thanhan_stag_07052026`, 7/7 ca đạt:
trùng MST giữa 2 dòng khác tên → báo lỗi cả 2 dòng · MST thuộc KH khác trên hệ thống → báo lỗi ·
đổi MST của KH cũ sang MST của KH cũ khác → báo lỗi · KH cũ giữ MST của chính nó → không lỗi ·
MST để trống → bỏ qua · MST mới → không lỗi.
Đang làm dở: không có.
Bước tiếp theo: user import lại file Excel thật để xác nhận (chỉ sửa BE → không cần build client).
Blocked:
