# Plan — Báo giá Vật tư - Hàng hoá - Thiết bị: bấm ảnh hàng mở ảnh gốc

**Người phụ trách:** @junfoke — 2026-10-28
Repo: `TanPhatDev`, nhánh `gop_db`

## Ngày 28/10/2026 (@junfoke)

- [x] 28/10/2026 — Báo giá 62438: bấm ảnh hàng chỉ mở ảnh 75×75 vì dòng báo giá lưu link `-thumbnail` lấy từ `Product::image` (app/Product.php:1384); ảnh gốc 971×669.
- [x] 28/10/2026 — Sửa `FirmQuotationTabProduct.blade.php`: link mở popup bỏ `-thumbnail` → mở ảnh gốc, ảnh nhỏ trong bảng giữ nguyên. Áp cho tạo / sửa / xem; báo giá cũ không phải sửa dữ liệu. Không sửa `Product::image` (dùng chung nhiều màn). Commit `b62ee11c13` trên `gop_db` (đã push).
- [ ] User kiểm trên trang thật (ERP bắt SSO, chưa xem được).
- [ ] Các màn HĐ / báo giá khác dựng popup ảnh y hệt (`ContractProduct`, `QuotationProduct`, `ProjectQuotationTabProduct`, `FirmContractProduct`…) — chờ user chốt có sửa đồng bộ không.
