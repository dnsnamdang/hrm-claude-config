# Design — Báo cáo hàng có thể bán theo công ty

> Phụ trách: @junfoke · Tạo 2026-10-02 · nhánh `develop`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-02-lookup-stock-companies-design.md`

## Mục tiêu

Port màn ERP *Kinh doanh › Tra cứu tồn kho › Báo cáo hàng có thể bán theo công ty* sang HRM,
phân hệ **Thông báo** (`/lookup/stock-companies`). Màn chỉ đọc, không ghi DB.

## Phạm vi

- Bảng tồn theo công ty: SL có thể bán, KM, tổng tồn, hàng đang về, gửi, giữ, đang xuất + nhóm cột theo từng kho, dòng tổng
- Bộ lọc: công ty, kho, nhóm/tính chất/loại hàng, thương hiệu, hãng, model, hàng hóa + tìm nhanh
- Popup "Hàng đang về" (bấm số Tồn kho) — link phiếu HRM nếu đã port, còn lại mở ERP
- Xuất Excel (popup chọn trường)

## Quyết định chính (user 2026-10-02)

| Vấn đề | Chốt |
|---|---|
| Popup Hàng đang về | Làm luôn, link ERP cho màn chưa port |
| Quyền | Ai cũng xem được (như ERP) |
| Menu | Link vào "Hàng có thể bán theo công ty"; giữ mục "Báo cáo Tồn kho có thể bán,..." không link |
| Bảng | Tự dựng, tiêu đề gộp + dòng tổng như ERP |
| Công thức | Giữ nguyên ERP (kể cả mốc 2024-07-01); dòng tổng tính bằng SQL thay vì tải hết |

## Code

- BE: `Modules/Finance/Services/SellableStockReportService.php` + `Http/Controllers/V1/StockCompanyController.php`, route `/v1/finance/stock-companies`
- FE: `pages/lookup/stock-companies/` + `utils/stock-voucher-link.js`
