# Phiếu xuất hàng — nhóm hàng hiển thị dạng TAB giống ERP

Yêu cầu (2026-10-10): loại 14 (và mọi loại có nhóm) đang tách 2 bảng rời → làm giống ERP: 1 khối "Chi tiết" chia tab.
User chọn phương án A (đầy đủ như ERP).

## Quyết định
- Nhóm lấy từ CHỨNG TỪ NGUỒN (PXK `warehouse_export_tabs` / YCXH `product_export_request_tabs`), không từ HĐ hãng.
- Tạo PXH lưu `product_export_tabs` + `product_export_tab_products` (như ERP `ProductExport::syncTabs`), BE tự dựng từ nguồn — FE không gửi.
- Tab chỉ lưu product_id/unit_id/SL; tên/ĐVT/giá lấy từ dòng hàng chính khớp product_id + unit_id (như ERP).
- Bỏ cột "SL HĐ / Còn lại" cũ.

## Tasks
- [x] BE `ProductExportService::sourceTabs()` + `syncTabs()`; gọi ở `createFromWarehouseExport` / `createFromProductExportRequest`
- [x] BE `ProductExportController`: 2 endpoint dữ liệu tạo dùng `sourceTabs`, `detailForShow` trả `tabs`; bỏ `buildFirmContractTabs`
- [x] FE `components/ProductExportGroupTabs.vue` viết lại: bảng 1 nhóm, cột ERP (STT, Mã, Tên, Model, ĐVT, [Giá niêm yết, Giảm giá, Đơn giá bán, Thành tiền bán], SL đề nghị, SL thực xuất)
- [x] FE `create.vue`: khối "Chi tiết" b-tabs — "Hàng hoá *" (icon cảnh báo khi lỗi) + tab mỗi nhóm
- [x] FE `_id/index.vue`: cùng bố cục tab, cột giá theo `is_sale`
- [x] Kiểm: tinker (PXK-30213 → 2 nhóm, syncTabs lưu/đọc lại khớp, rollback); Playwright tạo từ PXK-30138 + chi tiết PXH 34520

### Checkpoint — 2026-10-10
Vừa hoàn thành: toàn bộ task trên, chưa commit
Đang làm dở: —
Bước tiếp theo: chờ user review / yêu cầu commit
Blocked:
