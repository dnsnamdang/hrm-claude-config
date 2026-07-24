# Đồng bộ popup "Thêm hàng hoá" báo giá theo popup ERP — Tóm tắt

> Phụ trách: @manhcuong · Ngày: 2026-07-03 · Trạng thái: **CODE DONE** (4 phase, final review READY, Playwright 12/12 — chưa commit, chờ user review; việc còn lại xem plan.md)

## Mục tiêu

Popup "Thêm hàng hoá" ở màn tạo/sửa **báo giá trực tiếp** (`/assign/quotations/create`) có đầy đủ **bộ lọc + cột giống popup "Tìm kiếm hàng hóa" của ERP** (firm-quotations), chỉ khác: có thêm cột **Nguồn** và button **Thêm hàng tạm** (cả 2 đã có sẵn ở HRM, giữ nguyên).

## Quyết định lớn

| Vấn đề | Quyết định |
|---|---|
| Nguồn dữ liệu search | **Proxy qua ERP API nội bộ** (pattern `v1/.../sync-from-hrm` không api-key + `ErpApiService`) — tái dùng `searchProductStockBuyerApi` của ERP, KHÔNG port logic tồn kho `stockCompanies()` sang HRM |
| Bộ lọc | Đủ **19 bộ lọc giống ERP** (tính chất/loại HH, thương hiệu, hãng SX, xuất xứ, lĩnh vực→chương→nhóm CV→cụm CV, nhóm HH, dùng cho máy/nhóm máy, 4 filter xe, model, tên/mã, tồn kho) |
| Cột bảng | Cột ERP (Ảnh, Loại HH, Tên, Model, Mã, Giá niêm yết kèm ĐVT, Bảo hành, VAT%, Định mức đàm phán %, SL tồn/KM/lắp ráp tách theo công ty, Ghi chú, Tính chất) + cột **Nguồn**. BỎ cột ĐVT + Số lượng — apply `qty=1`, chỉnh SL ở bảng chi tiết |
| Component FE | Modal MỚI `QuotationProductSearchModal.vue` cho báo giá — **không sửa** `BomBuilderAddProductModal.vue` (BOM dùng chung) |
| Interface | Giữ emit `apply(items, parentRowId, groupId)` → `edit.vue::onAddProductApply` không đổi, flow hàng con công thức không đổi |
| Thêm hàng tạm | Copy overlay hiện tại sang modal mới, hành vi không đổi (source NEW) |
| Search UX | Auto-search deep watcher + debounce (convention team), phân trang server-side 20/trang |
| Permission | Không thêm quyền mới; giá vốn vẫn gate quyền `Xem giá vốn hàng hoá` |

## Thành phần mới

- **ERP**: `Api\HrmProductSearchController` + 2 route nội bộ `GET /api/v1/hrm/products/search|catalogs`
- **HRM BE**: `ErpProductSearchService` + 2 route `assign/quotations/erp-product-search|erp-product-catalogs`
- **HRM FE**: `pages/assign/quotations/components/QuotationProductSearchModal.vue`, đổi import trong `_id/edit.vue`

## Spec chi tiết

→ `docs/superpowers/specs/2026-07-03-quotation-product-popup-erp-design.md` (có 4 câu hỏi mở chờ user, mục 6)
