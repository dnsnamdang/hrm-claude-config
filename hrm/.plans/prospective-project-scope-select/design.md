# Loại hình/Lĩnh vực KH ở màn Dự án tiền khả thi — chọn 1 + append hồ sơ KH

@namdangit — 2026-07-02

## Mục tiêu

Chuẩn hoá cách chọn **Loại hình hoạt động** + **Lĩnh vực kinh doanh** của khách hàng trên màn Tạo/Sửa Dự án tiền khả thi (`/assign/prospective-projects/add`, `_id/edit`), và tự bổ sung giá trị đã chọn vào hồ sơ khách hàng (ERP) khi lưu.

## Phạm vi & quyết định

1. **Dropdown dùng style như màn khách hàng nhưng CHỌN 1** (không multi). Component mới `CspSingleSelect.vue` (2 chế độ: phẳng + 2 cấp).
2. **Options = TOÀN BỘ danh mục** (như màn tạo KH), không giới hạn theo scope KH đã khai. Load 1 lần ở `CustomerInfoSection` qua `customer-scope-groups/getAll` + `customer-scopes/getAll`.
3. **Lĩnh vực hiển thị 2 cấp** (nhóm Loại hình = header + lĩnh vực con thụt lề) giống màn khách hàng.
4. **Mapping 2 chiều**: chọn Lĩnh vực trước → tự điền Loại hình cha; chọn Loại hình → lọc Lĩnh vực + reset nếu không tương thích.
5. **Tick xanh** cạnh giá trị KH đã khai sẵn (phân biệt giá trị mới sẽ được thêm).
6. **Append hồ sơ KH khi lưu dự án** (cả Lưu nháp + Lưu, cả KH trực tiếp + KH thụ hưởng cuối): nếu Loại hình/Lĩnh vực đã chọn chưa có trong hồ sơ KH ở ERP → thêm mới. **CHỈ THÊM, không ghi đè/xoá**. Không tạo mục danh mục master mới.
7. Bỏ hint "Chọn Khách hàng + Loại hình + Lĩnh vực... để lọc ứng dụng" ở `ProjectInfoSection`.

## Quyết định kỹ thuật

- Hồ sơ scope KH lưu ở **ERP** (mysql2): `customer_activity_types` (customer_id, customer_scope_group_id), `customer_business_fields` (customer_id, customer_scope_group_id, customer_scope_id). ID danh mục HRM ≡ ERP → ghi thẳng.
- Append idempotent (exists-check trước insert). Bọc try/catch + log; lỗi ghi ERP KHÔNG chặn lưu dự án. Không yêu cầu quyền "Sửa khách hàng" riêng.

## Chi tiết

Xem `docs/superpowers/specs/2026-07-02-prospective-project-scope-select-design.md`.
