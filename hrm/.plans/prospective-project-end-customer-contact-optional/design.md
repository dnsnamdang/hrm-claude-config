# Bỏ bắt buộc "Người liên hệ" của KH thụ hưởng cuối

**Người phụ trách:** @khoipv

## Mục tiêu
Trên màn Tạo mới/Chỉnh sửa **Dự án tiền khả thi** (module Assign — `prospective-projects`), khi người dùng tick **"KH thương mại dịch vụ"** (`is_intermediary_customer = true`) và hiện nhóm **"Khách hàng thụ hưởng cuối"**:
- Trường **"Người liên hệ"** của KH thụ hưởng cuối **không còn bắt buộc**: bỏ dấu `*` đỏ + bỏ validation require.
- Người dùng có thể để trống và lưu bình thường.

## Phạm vi
- **CHỈ** trường "Người liên hệ" của **KH thụ hưởng cuối**.
- Giữ nguyên bắt buộc: Khách hàng thụ hưởng cuối (picker), Email, Loại hình/Lĩnh vực của KH cuối.
- Giữ nguyên: "Người liên hệ" của **KH trực tiếp** vẫn bắt buộc (khi là doanh nghiệp).

## Thay đổi
### FE
- `CustomerBlock.vue`: thêm prop `requiredContact` (default `true`); label "Người liên hệ" dùng `:required="requiredContact"` thay vì `requiredCustomer`.
- `CustomerInfoSection.vue`: block `benefit` truyền `:required-contact="false"`. Block `direct` để mặc định (`true`).
- Áp dụng cho cả `add.vue` và `_id/edit.vue` (dùng chung `CustomerInfoSection`).

### BE — `ProspectiveProjectRequest.php`
- Bỏ rule `sometimes(['customer_benefit_contact_name','customer_benefit_contact_phone'], 'required...')`.
- Xóa method dead code `benefitCustomerRequiresContact()`.
- Giữ nguyên rule require contact cho KH trực tiếp.
- Các field `customer_benefit_contact_*` vốn đã `nullable` trong `rules()`.

## Kiểm thử
1. Tick "KH thương mại dịch vụ" → chọn KH thụ hưởng cuối là doanh nghiệp → để trống Người liên hệ → **Lưu thành công**, không lỗi inline.
2. Trường "Người liên hệ" của KH thụ hưởng cuối **không** còn dấu `*`.
3. KH trực tiếp (doanh nghiệp) để trống Người liên hệ → **vẫn báo lỗi bắt buộc** như cũ.
