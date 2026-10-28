# Design — Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa

> Phụ trách: @khoipv · Tạo 25/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-25-bao-cao-hang-thua-thieu-sau-tong-kiem-ke-design.md`

## Mục tiêu

Port màn ERP *Kho › Báo cáo kho › Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa* (`warehouseReport.selfInventoryReport`) sang HRM
`/warehouse/self-inventory-report`. Chỉ đọc: mỗi dòng hàng của phiếu kiểm kê theo hàng hóa ĐÃ HOÀN THÀNH có chênh lệch ≠ 0 → SL thừa / SL thiếu.

## Quyết định chính (user chốt 25/10/2026)

| Vấn đề | Chốt |
|---|---|
| Quyền | KHÔNG chặn quyền — như ERP (đoạn quyền ERP bị comment) |
| Phạm vi | Giữ y ERP: ô Kho chỉ liệt kê kho của công ty đăng nhập, nhưng không chọn kho → phiếu của mọi công ty |
| Khối tổng hợp | Thừa (số dòng · tổng SL) · Thiếu (số dòng · tổng SL) · số phiếu kiểm kê; trên toàn tập đã lọc; dòng TỔNG đầu bảng |
| Số liệu | Y ERP `SelfInventory::reportSearchData()` |
| In / Excel | In xem trước (popup chọn cột) + Excel tải thẳng, 7 cột như ERP, khối ký "Người lập" |
