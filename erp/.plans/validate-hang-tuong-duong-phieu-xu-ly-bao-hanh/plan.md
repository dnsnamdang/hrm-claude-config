# Validate bắt buộc chọn hàng hóa tương đương cho thiết bị nhập tay (phiếu xử lý bảo hành)

## Bug
Màn phiếu xử lý YC bảo hành (warranty_repair_handle_requests): thiết bị nhập tay
(product_no_sale_name) phải chọn hàng hóa tương đương (product_id) nhưng hệ thống cho pass
khi bỏ trống.

## Root cause
FormRequest WarrantyRepairHandleStoreRequest: `products.*.product_id => nullable` → không bắt buộc.

## Fix
- [x] BE (WarrantyRepairHandleStoreRequest::rules): thêm rule động — nếu product_no_sale_name có giá trị
      thì products.{i}.product_id = required|exists:products,id.
- [x] BE (messages): message động "Cần chọn hàng hóa tương đương cho thiết bị {product_no_sale_name}".
- [x] FE (warranty_repair_handle_requests/form.blade): thêm span invalid-feedback cho
      errors['products.'+$index+'.product_id'] cạnh chỗ hiển thị "Thiết bị tương đương".
- [x] Xác nhận cơ chế: BaseRequest::failedValidation trả 200 {success:false,errors} → FE $scope.errors (create+edit).
- [ ] User test: tạo/sửa phiếu xử lý có thiết bị nhập tay, để trống tương đương → phải chặn + hiện cảnh báo.

## Áp dụng cho cả store (create) và update (edit) — cùng FormRequest.
## Branch: master
