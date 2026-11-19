# Nhóm máy lấy từ danh mục Loại SP — phía ERP (10/11/2026)

HRM đổi liên kết "dùng cho nhóm máy" sang Loại SP (`productable_type = Modules\MasterData\Entities\ProductClassification\ProductType`,
id = product_types.id); dòng Group cũ bị xoá. Xem HRM/.plans/nhom-may-theo-loai-sp/plan.md.

Worktree: ERP/TanPhatDev-nmlsp (nhánh fix/nhom-may-loai-sp từ origin/develop_02).

## Tasks
- [x] E1 SearchController: lọc theo máy (product->group_id) → product->product_type_id + kiểu mới (2 chỗ)
- [x] E2 SearchController: lọc group_id_use → kiểu mới (4 chỗ)
- [x] E3 Ô "Dùng cho nhóm máy" ở các view lấy danh sách product_types thay groups
  - 2 ô: product_infos/searchProductInfo (dùng trong sync_products) + common/warehouse_warnings/form — render @foreach product_types status=1
- [x] E4 Product::filter group_id_use → productables kiểu mới (hằng Product::MACHINE_GROUP_TYPE)
  - Không sửa groupsUse()->sync ở form hàng hoá ERP: route lưu đã chặn productMovedToHrm
  - Không sửa ProductTemplate (bảng riêng product_templateables, HRM không đụng)
