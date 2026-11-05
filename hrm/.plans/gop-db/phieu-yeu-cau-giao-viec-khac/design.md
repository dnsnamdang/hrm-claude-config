# Phiếu yêu cầu giao việc khác (ERP → HRM)

> Port màn ERP `assignOtherRequest.index?type=all` (Bán hàng › Lắp đặt - BH - SC). Nhánh `develop` (từ `gop_db`).
> Phụ trách: @khoipv · Bắt đầu: 2026-11-05
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-05-phieu-yeu-cau-giao-viec-khac-design.md`

## Mục tiêu
Phiếu yêu cầu giao việc khác là 1 trong 3 nguồn tạo Phiếu giao việc (type 5, PGV đã port). Port trọn màn: danh sách · tạo · sửa ·
chi tiết · xoá · từ chối · lịch sử · xuất Excel.

## Quyết định (user chốt 05/11/2026)
- Phân quyền theo cấp y ERP — 3 quyền xem mới `type 23` (Bán hàng), tên nguyên văn ERP; không có quyền Tạo (y ERP).
- Xoá y ERP: người tạo + (Đang tạo / Từ chối).
- Ô Hợp đồng: CẢ 2 nguồn (HĐ hãng + HĐ HRM) trong 1 popup; thêm cột `hrm_contract_id` (nullable) vào bảng ERP.
- Nghiệp vụ y ERP; khác có chủ ý: nháp đổi xám, nháp chỉ bắt 3 cột NOT NULL, Từ chối có ở danh sách + kiểm quyền, phòng tiếp nhận
  thấy phiếu gửi về mình trong danh sách, báo người tạo khi bị từ chối, lọc ngày theo Ngày tạo (ERP lọc cột không tồn tại → lỗi).

## Phạm vi code
- BE `Modules/CustomerCare`: entity `AssignOtherRequest` (sẵn có, bổ sung), service danh sách / chi tiết / lưu / nguồn HĐ / thông báo,
  FormRequest, controller, route `/v1/customer-care/assign-other-requests`, migration `hrm_contract_id`, quyền seeder, registry xuất +
  lịch sử.
- FE `pages/customer-care/assign-other-requests/` (index, create, `_id/index`, `_id/edit`) + form + popup chọn HĐ + popup từ chối;
  menu Bán hàng; đổi link ERP → HRM ở PGV / Phiếu nhập kết quả.
