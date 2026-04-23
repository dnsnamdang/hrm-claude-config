# Design: Select người liên hệ cho đơn hàng nguyên tắc

## Bối cảnh

Form đơn hàng nguyên tắc hiện copy người liên hệ từ hợp đồng nguyên tắc (3 input disabled). Yêu cầu: đổi sang dropdown select từ danh sách `customer_contacts` của khách hàng, auto-fill địa chỉ (từ customer) + điện thoại (từ contact). Default selected = contact đã chọn ở hợp đồng nguyên tắc.

## Thay đổi

### Migration
- Thêm `customer_contact_id` bigint nullable vào `firm_contracts`

### View — `sale/firm/orders/form.blade.php`
- Thay 3 input disabled thành: select contact (ng-model `form.customer_contact_id`, ng-change fill tên/địa chỉ/SĐT) + 2 input disabled (địa chỉ, SĐT auto-fill)

### JS — `sale/firm/orders/formJs.blade.php`
- Load contacts từ `form.customer.contacts` (eager loaded)
- `onChangeContact()`: tìm contact theo id → fill `customer_contact_name`, `contact_address` (= customer.address), `customer_contact_phone` (= contact.phones)
- Default: match `parent_contract.customer_contact_name` → auto-select `customer_contact_id`

### Controller — `PrincipleOrderController`
- `store()` + `update()`: thêm `customer_contact_id`, `customer_contact_name`, `contact_address`, `customer_contact_phone` vào `$request->only([...])`

### Service — `FirmContractService`
- `getDataForPrincipleOrder()`: eager load `customer.contacts`
- Không merge contact từ parent_contract nữa — lấy từ request

## Không thay đổi
- Form hợp đồng nguyên tắc — giữ nguyên input text
- Form báo giá — không đụng
- Bảng `customer_contacts` — không thêm cột
