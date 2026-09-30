# Design tóm tắt — Chuẩn hóa UI V2 cho phân hệ Cung ứng

> Phụ trách: @khoipv · Ngày: 2026-09-28
> Spec đầy đủ: [docs/superpowers/specs/2026-09-28-ui-v2-cung-ung-design.md](../../docs/superpowers/specs/2026-09-28-ui-v2-cung-ung-design.md)

## Mục tiêu
Đưa chuẩn UI V2 (component `V2Base*` + skill) của hrm sang dns, rồi chuyển phân hệ Cung ứng sang V2.

## Quyết định lớn
- Port component/utils **cùng đường dẫn** như hrm; chỉ thêm file, không sửa hàm dùng chung.
- `.v2-styles` bọc trang → màn cũ không bị ảnh hưởng, chuyển dần từng màn.
- Bỏ `V2BaseCompanyDepartmentFilter` + `V2BaseFieldCategoryApplicationFilter` (nghiệp vụ riêng hrm, cung ứng chưa cần).
- Port BE `filter_customizations` để `V2BaseSmartFilterPanel` lưu cấu hình bộ lọc theo user.
- Skill viết lại cho dns: `button-convention`, `list-page`, `modal-popup`, `form-validate`, `select-and-input-state`.
- Thí điểm: **Danh sách Đơn mua hàng**; user duyệt rồi mới chuyển các màn khác.

## Chờ user quyết
- Q1: cập nhật plugin select2 dùng chung theo bản hrm?
- Q2: chuyển BE cấu hình cột sang bảng key-value `user_column_settings`?
