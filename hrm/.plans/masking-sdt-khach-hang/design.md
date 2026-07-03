# Che mờ SĐT khách hàng — Meeting & Dự án TKT (tóm tắt)

**@manhcuong** · 2026-06-23 · Module Giao việc (Assign)
Spec chi tiết: `docs/superpowers/specs/2026-06-23-masking-sdt-khach-hang-design.md`

## Mục tiêu
Che (`-`) SĐT phía khách hàng với người KHÔNG sở hữu/không quản lý bản ghi, để thành phần tham gia/thành viên/sales khác không tự lấy SĐT KH. Đồng bộ list + detail + edit + tab TKT trong meeting + export Excel. Số thật không nằm trong response → mask ở Backend.

## Quy tắc full (thỏa 1 trong các điều)
1. Mình là người tạo (`created_by`)
2. Quyền "theo tổng công ty"
3. Quyền "theo công ty" + cùng `company_id`
4. Quyền "theo phòng ban" + `department_id`/`part_id` thuộc mình quản lý
5. Quyền "theo bộ phận" + `part_id` thuộc mình quản lý
→ Ngoài ra: che `-`.

## Field che (chỉ SĐT khách hàng)
- Meeting: `customer_contact_phone`, `customer_members[].phone`, `customer.mobile`, `customer.contacts[].phones`, `projects[].customer_contact_phone` (tab TKT — tính theo quyền TKT)
- TKT: `customer_phone`, `customer_contact_phone`, `meetings[].customer_contact_phone`, `customer.contacts[].phones`
- KHÔNG che: SĐT nhân viên nội bộ (company_members, solution_employee, support).

## Kiến trúc
Helper `app/Helper/CustomerPhoneVisibility.php` (`canView` + `apply`) → áp ở 5 Resource/Transformer + `MeetingService::getDataForShow` + 2 blade export. FE không sửa. Unit test 6 nhánh.
