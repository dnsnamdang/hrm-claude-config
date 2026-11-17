# Báo cáo số lượt sửa chữa - bảo dưỡng cho 1 khách hàng (ERP → HRM)

**Người phụ trách:** @junfoke — 2026-11-16
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-16-bc-so-luot-sc-bd-khach-hang-design.md`

## Mục tiêu
Port `report.warrantyRepairServiceByCustomer`: với 1 khách hàng, mỗi thiết bị (hàng + serial) đã sửa chữa / bảo dưỡng bao nhiêu
lượt, giá trị bao nhiêu trong kỳ. Nghiệp vụ theo ERP, giao diện khuôn `report-styles` (bám Báo cáo bán hàng theo từng mặt hàng).

## Quyết định đã chốt (user 16/11/2026)
1. Bắt buộc có 1 trong 2 mã quyền (ERP ai cũng vào).
2. Ẩn thiết bị chỉ bảo hành (không có lượt SC/BD).
3. Sửa lỗi ERP sai rành rành: SL ghi đè, nhân đôi khi có cả vật tư + dịch vụ, bảo dưỡng chỉ tính 1 dịch vụ, NCC luôn "Khác",
   mất ngày cuối kỳ / In-Excel sai ngày, phạm vi Bộ phận hỏng — chi tiết spec mục 3.

## Scope
- BE `Modules/Sale`: service, print service, controller, Excel, blade in + Excel, route + `checkPermission`; Catalog thêm `hrm`.
- FE `pages/sale/warranty-repair-by-customer-report` + link menu `sale-hub.js`.
- Không migration. Deploy: `permission:catalog-sync`.
