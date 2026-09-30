# Fix YCLDBG — đổi khách hàng nhưng không reset Người liên hệ

Người phụ trách: @junfoke · Repo: `hrm-cursor/TanPhatDev` (bản B) · Nhánh: `master`

## Hiện tượng
Màn tạo/sửa Phiếu yêu cầu lắp đặt, bàn giao (`/admin/customer-care/assembly_requests/create`):
chọn Khách hàng A → chọn Người liên hệ của A → đổi sang Khách hàng B
→ ô "Người liên hệ", "SĐT" vẫn giữ người liên hệ của A, không bị xoá để chọn lại
→ Lưu và gửi duyệt vẫn thành công ⇒ phiếu lưu sai người liên hệ (phiếu 87: khách ETEK GREEN nhưng người liên hệ TRƯƠNG VĂN KHIẾT của khách SKT).

## Nguyên nhân
`resources/views/customercare/assembly_requests/formJS.blade.php` — `$scope.setCustomer()` khi đổi
khách chỉ xoá `firm_contract_*` / `exportable_*`, KHÔNG xoá `customer_contact_id` /
`customer_contact_name` / `customer_contact_phones` / `delivery_place*`.
Ô hiển thị và `submit_data` (`AssemblyRequest.blade.php:229-231`) đều có fallback
`form.customer.contact.fullname || form.customer_contact_name` nên giá trị cũ "sống sót" và được gửi lên BE.
BE `AssemblyRequestStoreRequest` chỉ validate `customer_contact_name` `required_if:customer_type,2`
nên tên cũ vẫn qua validate.

## Task
- [x] Trace nguyên nhân (FE, không phải BE)
- [x] `setCustomer()`: đổi khách hàng → clear `customer_contact_id/name/phones`, `delivery_place`,
      `delivery_place_id`, `exportables` cùng với `firm_contract_*` (theo pattern `clearDataObject()`
      của `partials/classes/delivery_requests/DeliveryRequest.blade.php:140`)
- [x] Chuẩn hoá `submit_data` phones cùng thứ tự fallback với id/name
- [x] Verify bằng Playwright trên dev-erp: đổi khách → ô Người liên hệ + SĐT rỗng, mở lại modal thấy
      danh bạ của khách mới, lưu ra đúng người liên hệ

### Checkpoint — 2026-09-18
Vừa hoàn thành: sửa `formJS.blade.php` + `AssemblyRequest.blade.php`.
Đã verify Playwright trên bản B local (:8001): trước fix, đổi khách vẫn giữ 'NGUYEN VAN A' + 'Kho A';
sau fix, ô Người liên hệ/SĐT/Địa điểm giao rỗng; khách Cá nhân vẫn tự điền đúng người của chính khách đó.
Bước tiếp theo: commit + deploy dev-erp để QA nghiệm thu lại.
