# Design — Thẻ kho

> Phụ trách: @khoipv · Tạo 22/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-22-the-kho-design.md`

## Mục tiêu

Port màn ERP *Kho › Báo cáo kho › Thẻ kho* sang HRM (`/warehouse/stock-card`, phân hệ Kho). Màn chỉ đọc.

## Phạm vi

- Bộ lọc: Hàng hóa (*), Tồn theo công ty (*), Kho, Công ty thuê kho, Thời gian, Loại báo cáo, Nhà/Dãy/Khoang/Vị trí + ô tìm nhanh
- Bảng: 5 dòng tổng hợp (ĐVT chọn được, tồn đầu, nhập, xuất, tồn cuối) + dòng chứng từ gộp theo lô, tiêu đề 2 tầng
- In (Đầy đủ / Rút gọn + chọn cột) và Xuất Excel (Đầy đủ / Rút gọn)

## Quyết định chính (user 22/10/2026)

| Vấn đề | Chốt |
|---|---|
| Quyền | Tên y ERP: "Thủ kho" (vào màn) + "Xem báo cáo tồn kho theo tổng công ty" (chọn công ty khác), type 21 |
| Lọc vị trí | Giữ 4 cột tick như ERP, dùng lại `ScopePicker` (thêm prop `optional`) |
| In / Excel | Giữ 2 kiểu Đầy đủ / Rút gọn |
| Số liệu | 1 nguồn BE cho màn + in + Excel; sửa các chỗ ERP tính lệch (xem spec mục "Khác ERP") |

## Code

- BE: `Modules/Finance/Services/StockCardReportService.php`, `StockCardPrintService.php`, `Http/Controllers/V1/StockCardController.php`, `Exports/StockCardExport.php`, views `exports/stock_card` + `prints/stock-card`, route `/v1/finance/stock-card`
- FE: `pages/warehouse/stock-card/index.vue` + `components/ExportModeModal.vue`, `components/voucher-link.js`
