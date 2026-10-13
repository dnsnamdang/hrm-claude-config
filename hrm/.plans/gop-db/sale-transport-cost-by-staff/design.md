# Design — Báo cáo chi phí vận chuyển theo nhân viên kinh doanh

> Phụ trách: @junfoke · Tạo 2026-10-05 · nhánh `develop`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-05-sale-transport-cost-by-staff-design.md`

## Mục tiêu

Port báo cáo ERP `report.transportByStaff` sang hub Bán hàng (`/sale/transport-cost-by-staff`): cước vận chuyển
(phiếu hạch toán chuyến xe) theo Phòng ban › Nhân viên KD › Chuyến. Chỉ đọc.

## Quyết định chính (user 2026-10-05)

| Vấn đề | Chốt |
|---|---|
| Cước không mã công việc | Giữ như ERP (loại) |
| Quyền | 3 cấp thống nhất, không quyền → của mình; ai cũng vào màn |
| Ngày/bộ lọc | Thống nhất theo ngày hạch toán, lọc áp xuống chi tiết |
| Excel | Popup chọn trường, xuất FE |

## Code

- BE: `Modules/Finance/Services/TransportCostByStaffReportService.php` + `Http/Controllers/V1/TransportCostByStaffController.php`, route `/v1/finance/transport-cost-by-staff`
- FE: `pages/sale/transport-cost-by-staff/`
- Quyền 1680-1682 (type 23, Bán hàng)
