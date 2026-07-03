# Design — Fix validate vượt SL HĐ giữa phiếu mượn & YCXH

## Mục tiêu
Chặn tạo phiếu khi tổng cam kết theo item vượt SL hợp đồng — tính gộp CẢ "Yêu cầu xuất bán HĐ hàng" (XUAT_BAN_HD_HANG) và "Yêu cầu xuất bán hàng mượn" (BorrowSellRequest) đang in-flight.

## Root cause
Hai luồng validate độc lập, không chia sẻ quỹ:
- `getExportingQty` (FirmContractTabProduct) chỉ đếm YCXH + warehouse, bỏ qua phiếu mượn.
- Validate phiếu mượn (`BorrowSellRequestsController@store`) chỉ trừ `exported_qty`, bỏ qua YCXH in-flight và phiếu mượn in-flight.

## Quyết định (chốt sau khi hỏi user)
- [ ] Quỹ chung mượn + xuất bán theo từng item HĐ
- [ ] Danh sách status phiếu mượn tính là "đang chiếm quỹ"
- [ ] Trả hàng mượn có hoàn quỹ không
- [ ] Enforce ở store (và/hoặc approve)

## Phạm vi dự kiến
- `app/Model/Sale/Firm/Contract/FirmContractTabProduct.php` — `getExportingQty` (cộng phiếu mượn) — HÀM DÙNG CHUNG
- `app/Http/Controllers/Warehouse/BorrowSellRequestsController.php` — validate store
- FE thông báo lỗi inline
