# Biên bản giao nhận hàng hóa (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-10-bien-ban-giao-nhan-hang-hoa-design.md`

## Mục tiêu
Port màn ERP `handoverAcceptanceProductRecord.index` (Kinh doanh › Đơn hàng - hợp đồng › Biên bản giao nhận hàng hóa `?type=all`)
sang HRM trọn bộ: danh sách, tạo / sửa / chi tiết, nhập seri, Lưu và duyệt (ghi serial vào danh mục), in mẫu BBGNHHVT, xuất Excel.

## Quyết định (user chốt 10/11/2026)
- Nguồn HĐ: HĐ hãng + HĐ BH-SC (y ERP) + **HĐ HRM** qua YCXH loại 21 "Xuất bán hợp đồng" (`emplement_contract_id`) — luồng xuất kho
  HRM đã gắn sẵn, không phải sửa.
- Phân quyền theo cấp y ERP, dùng lại mã `customer_care.bien_ban_giao_nhan.view` (thêm platform `hrm`); không mã Tạo.
- Sửa / Xóa: Đang tạo + người tạo (y ERP). In bằng mẫu `BBGNHHVT` trong DB, letterhead theo công ty của biên bản.
- Nháp xám (ERP vàng); File bắt buộc khi "Lưu và duyệt" (quy chuẩn Lưu nháp nới required).

## Phạm vi code
- BE `Modules/Sale`: `Entities/HandoverProductRecord/*`, `Services/ContractDeliveredQtyService` (dùng chung — SL theo HĐ / đã xuất /
  nhập trả / đã bàn giao), `HandoverProductRecord{Source,,Store,Print}Service`, `HandoverProductRecordRequest`, controller, route
  `/v1/sale/handover-product-records`.
- FE `pages/sale/handover-product-records/` + menu `components/subsystem-menu/sale-hub.js` (2 mục Bán hàng hóa / Bán dịch vụ › Khác).

## Rủi ro đã biết
- ERP đọc biên bản gắn HĐ HRM: `HandoverAcceptanceProductRecord::contract()` belongsTo FirmContract theo `contract_id` → hiện nhầm
  HĐ hãng trùng id — chờ user quyết vá ERP.
- DB local chưa `rbac:convert` → danh sách `type=all` / meta / xuất chưa kiểm được ở local.
