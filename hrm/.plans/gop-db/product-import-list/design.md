# Phiếu nhập hàng — Bộ quyền 4 mức + Bộ lọc + Tùy chỉnh cột

## Mục tiêu
Đưa màn danh sách **Phiếu nhập hàng** (`Modules/Finance`) ngang bằng màn **Phiếu xuất hàng**:
1. Bổ sung **bộ quyền phân cấp đầy đủ 4 mức** (tổng công ty / công ty / phòng ban / bộ phận) — hiện chỉ có 3 và **chưa vào DB gộp** nên UI phân quyền không hiện nhóm "Phiếu nhập hàng".
2. Bổ sung nhánh lọc **bộ phận** vào `applyViewScope()` + `canView()`.
3. **Làm lại bộ lọc** màn danh sách (hiện chỉ keyword + status) → mirror màn xuất: keyword, công ty/phòng ban/bộ phận, người lập, loại, trạng thái, khoảng ngày.
4. Bổ sung **tùy chỉnh cột** (server-side per-user, dùng `ColumnCustomizationModal` + API `human/column-customizations`).

## Hiện trạng (đã điều tra)
- **Seeder** `PermissionsTableSeeder.php` có 3 dòng Phiếu nhập hàng: id 1543/1544/1545 (guard `api`, group `Phiếu nhập hàng`) — NHƯNG DB gộp max id = 1542 → **cả khối chưa được chèn**. Thiếu luôn mức **bộ phận**.
- **Code** `ProductImport` (trait `ChecksEmployeePermission`): `applyViewScope` chỉ có `isBigBoss`/`isBoss`/`isManager` (3 mức), **chưa có nhánh bộ phận**. `product_imports` CÓ cột `part_id`.
- Khuôn 4 mức đã có sẵn ở sibling `ProductImportRequest` (PERMISSION_VIEW_PART, `isPartManager`, `managePartIds`, `EmployeeManagePart`) → bê y hệt.
- **FE nhập** (`pages/finance/product-imports/index.vue`): filter dùng `V2BaseSmartFilterPanel` chỉ 2 field (keyword→code, status); **không có tùy chỉnh cột**; cột khai cứng. Cùng dùng `V2BaseDataTable` như màn xuất → tương thích port.
- **FE xuất** (mẫu): `V2BaseFilterPanel` + `V2BaseCompanyDepartmentFilter` + `ColumnCustomizationModal` (`table=finance_product_exports`), `filterStateMixin` (localStorage). Cột có `isVisible`/`locked`.

## Quyết định
- **Cách B**: đủ 4 mức. Thêm permission mới **id 1546** "Xem phiếu nhập hàng theo bộ phận" (sort_order 4), cùng chèn 1543-1546 vào DB.
- Sửa cả `seeder` (thêm 1546) và **chèn thẳng 1543-1546 vào DB gộp** (seeder không re-run được toàn bộ vì trùng id cũ).
- Table key tùy chỉnh cột: `finance_product_imports`.
- Bộ lọc mirror màn xuất, bỏ field không áp dụng cho nhập (contract_code, mã YCXH). Type options lấy từ `ProductImport::TYPE_NAMES`.

## Phạm vi KHÔNG đụng
- Không sửa hàm dùng chung toàn hệ thống. `applyViewScope`/`searchByFilter` là code riêng module Finance.
- Không đổi cơ chế trait role-18 bypass (giữ nguyên — super admin vẫn thấy hết).
