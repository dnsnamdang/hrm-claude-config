# Báo cáo phân công phòng phụ trách thương hiệu - hãng sản xuất (ERP → HRM)

**Người phụ trách:** @junfoke — 2026-11-16
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-16-bc-phan-cong-phong-thuong-hieu-design.md`

## Mục tiêu
Port báo cáo ERP `assign-department-brand.reportAssignDepartmentBrands`: mỗi cặp Thương hiệu – Hãng sản xuất đang do phòng /
người nào phụ trách (đại diện hãng, mua hàng), tổng hợp theo Thương hiệu hoặc Hãng, có lịch sử phân công. Giữ nghiệp vụ ERP,
giao diện theo khuôn `report-styles`.

## Quyết định đã chốt (user 16/11/2026)
1. Làm cả 2 lối như ERP, cùng 1 trang: Tra cứu › Thông báo (`?type=all`, ẩn In / Excel / Lịch sử) và Mua hàng › Báo cáo (đủ).
2. Lối `type=all` phải kiểm quyền — cả 2 lối cần mã Xem + áp phạm vi.
3. Báo cáo theo nhân viên (`reportAssignEmployeeBrands`): để sau.
4. Sửa lỗi ERP: lọc Người mua `orWhere`; bản in "theo Hãng" ghi sai "(N hãng)"; danh sách người không lọc theo phòng; bỏ nhánh
   phạm vi chết. Thêm (cùng loại sai rành rành): cặp có phiếu nháp mới hơn bị mất; dòng con không áp lọc/phạm vi; người phụ
   trách lấy dòng không xác định; ngày bắt đầu trong lịch sử sai.

## Scope
- BE `Modules/Purchase` (module đang trống): service, print service, controller, Excel, 2 blade, route + `checkPermission`.
- FE `pages/purchase/reports/assign-department-brands` + menu `lookup.js`, `purchase.js`.
- Không migration. Deploy: `permission:catalog-sync`.

## Còn mở
- Phân hệ Mua hàng ở HRM đang ẩn (`hidden` + `erpGhost`, user 17/09) → lối Mua hàng chưa có chỗ hiện. Chờ user chọn.
