# Design — Hoạt động kho

> Phụ trách: @khoipv · Tạo 26/10/2026 · nhánh `develop` (con của `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-26-hoat-dong-kho-design.md`

## Mục tiêu

Port màn ERP *Kho › Hoạt động kho* (`warehouseInfo.activities`) sang HRM `/warehouse/activities`. Chỉ đọc: bảng theo dõi
Phiếu đề nghị xuất kho + Phiếu đề nghị nhập kho đang xử lý / nhận trong ngày của các kho mình là thủ kho.

## Quyết định chính (user chốt 26/10/2026)

| Vấn đề | Chốt |
|---|---|
| Quyền | KHÔNG chặn quyền, không checkPermission — y ERP |
| Phạm vi | Kho mình là thủ kho (`warehouse_stockers`); Super Admin mọi kho |
| Realtime | ERP chết (socket bị comment) → tự tải lại 60s; port lại ô tổng hợp + tô màu dòng theo thời gian chờ |
| Bộ HRM thêm | Ô tìm nhanh mã phiếu, Cấu hình cột, Xuất Excel; không phân trang, không lọc nâng cao |
| Link mã phiếu | Sang màn HRM đã port, tab mới |
