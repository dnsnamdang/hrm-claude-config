# Tăng tốc popup "Thêm hàng hoá" (báo giá / BOM) — @namdangit

## Phase 1 — Tối ưu search hàng hoá ERP
### BE
- [x] TanPhatDev `SearchController::searchProductStockBuyerApi`: cờ opt-in `hrm_lazy_stock` — bỏ join subquery tồn kho toàn bảng khi không lọc theo tồn + hint `JOIN_PREFIX(products)` (caller khác giữ nguyên)
- [x] TanPhatDev `HrmProductSearchController`: gửi cờ khi không lọc tồn kho, tự tính tồn kho cho đúng các dòng của trang (`fillPageStocks`)
- [x] hrm-api migration `2026_10_03_000001_add_search_indexes_to_products_tables`: index `products.created_at` + `product_unit_prices(product_unit_id, price_type_id)`
- [x] Đối chiếu kết quả cũ/mới 7 bộ lọc (giống hệt) + tồn kho 10 hàng có tồn (khớp); ERP 678ms → 136ms, mở popup 2,2s → ~1,1s (local)

### Checkpoint — 2026-10-03
Vừa hoàn thành: Phase 1 + deploy PROD (ERP search mặc định ~0,6s, đường cũ ~3,6s)
Đang làm dở:
Bước tiếp theo: (không) — đã lên PROD 03/10: ERP 9adfffe888 (merge 8257830ac4), hrm-api 3d95e2f06 (merge e5dfa1b23, đã migrate)
Blocked:
