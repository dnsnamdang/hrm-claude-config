# customer-scope-single-group — Design (tóm tắt)

@manhcuong — 2026-06-15

## Mục tiêu

Đổi quan hệ **Lĩnh vực khách hàng (customer_scopes) ↔ Nhóm lĩnh vực (customer_scope_groups)**
từ **n-n** (pivot `customer_scope_group_members`) trở lại **1-n** (mỗi lĩnh vực thuộc đúng 1 nhóm).
Form Tạo/Sửa Lĩnh vực KH chỉ cho **chọn 1 nhóm**. Sửa toàn bộ phần phụ thuộc cho đúng.

## Bối cảnh

- Trước 2026-06-03 vốn là 1-n (cột `customer_scopes.customer_scope_group_id`).
- Migration `2026_06_03_000001_customer_scope_to_groups_many_to_many.php` đã đổi sang n-n.
- Yêu cầu mới = revert về 1-n. Pivot đang dùng chung nhiều nơi → phải sửa hết.

## Quyết định chính

- **DB**: thêm lại cột `customer_scopes.customer_scope_group_id` (unsignedBigInteger **nullable**),
  backfill từ pivot lấy `MIN(customer_scope_group_id)` mỗi lĩnh vực, **drop** pivot
  `customer_scope_group_members`. Required ép ở FormRequest, không ở DB.
- **Quan hệ Entity**: `CustomerScope::group()` belongsTo; `CustomerScopeGroup::customerScopes()` hasMany.
- **API field**: đổi `customer_scope_group_ids` (mảng) + `customer_scope_group_names` →
  `customer_scope_group_id` (số) + `customer_scope_group_name` (chuỗi) ở Resource/getAll.
- **Import Excel**: chỉ nhận **1 mã nhóm**; nhập >1 → lỗi. Vẫn tùy chọn (cho trống).
- **Khóa nhóm**: giữ rule `isCanLockUpdate` của Nhóm (không còn lĩnh vực Hoạt động mới cho khóa) — chạy qua hasMany.

## Phạm vi ảnh hưởng (đều sửa)

| Lớp | Nơi |
|---|---|
| DB | migration revert |
| BE catalog | CustomerScope entity, CustomerScopeGroup entity, CustomerScopeService, CustomerScopeRequest, 2 Resource, Import |
| BE phụ thuộc | CustomerScopeGroupService (count), Customer Save/UpdateRequest (validate scope∈group) |
| FE catalog | AddScopeModal.vue, customer-scopes/index.vue |
| FE phụ thuộc | customers (human+assign CustomerForm, CustomerScopeSelect), prospective-projects (add/edit/index/CustomerInfoSection), meeting (GeneralInfo/MeetingProject), customers/index.vue |

## Ngoài phạm vi (flag)

- **ERP** (TanPhatDev) đọc catalog scope↔group từ HRM qua remote DB — nếu ERP đọc pivot
  `customer_scope_group_members` sẽ hỏng sau khi drop. Cần rà soát ERP riêng (không thuộc 2 repo này).

## Spec chi tiết

`docs/superpowers/specs/2026-06-15-customer-scope-single-group-design.md`
