# Design: Bomlist - Quotation

## Mục đích
Hoàn thiện chức năng quản lý BOM List trong module Giao việc. BOM List quản lý danh mục hàng hoá/vật tư theo Hạng mục hoặc Giải pháp của dự án TKT, phục vụ cho báo giá sơ bộ.

## Scope

### Làm:
- **Danh sách BOM List** (FE): trang index hiển thị, tìm kiếm, lọc theo dự án/giải pháp/khách hàng
- **Xoá BOM List**: thêm endpoint DELETE ở BE + nút xoá ở FE
- **Xuất Excel**: endpoint export BE + nút export FE
- **Import Excel**: kết nối BomBuilderImportModal (đã có UI) với backend import
- **Trang chi tiết** (view-only): xem BOM List không cần vào chế độ edit

### Không làm:
- Thay đổi cấu trúc BomListProduct / BomListRelation hiện tại
- Chức năng báo giá chính thức (chỉ báo giá sơ bộ)
- Phân quyền phức tạp riêng cho BOM (dùng chung phân quyền module Assign)

## Hiện trạng (đã có)
- **BE**: CRUD store/show/update/index/getAll — thiếu delete, export, import
- **FE**: add + edit page, 10 BomBuilder components — thiếu index, detail
- **Entity**: BomList (code: BOM-YYYY-NNNNN), BomListProduct (hỗ trợ parent-child), BomListRelation (quan hệ cha-con giữa các BOM)
- **Loại BOM**: COMPONENT (1) = linh kiện, AGGREGATE (2) = tổng hợp

## Module liên quan
- `docs/assign.md`: luồng Giải pháp → Hạng mục, nơi BOM List được gắn vào
- BOM thuộc về: prospective_project + solution + solution_module (optional) + customer

## Quyết định thiết kế
1. **Danh sách**: dùng V2BaseDataTable + V2BaseFilterPanel theo style chung module Assign
2. **Export**: tạo class Excel export riêng (Laravel Excel), xuất theo filter đang chọn
3. **Import**: parse Excel → validate → tạo BomListProduct hàng loạt, dùng BomBuilderImportModal đã có
4. **Delete**: soft delete, kiểm tra BOM không đang được reference trong hồ sơ trình duyệt trước khi xoá
5. **Detail page**: reuse BomBuilderEditor ở chế độ readonly (disabled)
6. **Mã BOM**: giữ nguyên format `BOM-{YYYY}-{NNNNN}` tự tăng

## Câu hỏi cần xác nhận
1. Khi xoá BOM List, cần kiểm tra ràng buộc gì? (đang reference trong giải pháp/hạng mục đã duyệt thì có cho xoá không?)
2. Export Excel gồm những cột nào? Chỉ thông tin BOM hay bao gồm cả danh sách product bên trong?
3. Import Excel: template mẫu cần cung cấp sẵn hay user tự tạo file?
4. Trang danh sách cần hiển thị BOM của tất cả dự án hay chỉ trong context 1 giải pháp cụ thể?
5. Có cần phân quyền riêng cho BOM (ai được tạo/sửa/xoá) hay dùng chung quyền của giải pháp/hạng mục?

