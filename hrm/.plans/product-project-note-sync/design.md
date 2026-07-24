# Fix cột "Ghi chú" — Hàng hóa dự án (đồng bộ note từ báo giá/BOM)

**Người phụ trách:** @manhcuong
**Loại:** Bug fix (mở rộng thành nối luồng feature)

## Mục tiêu
Cột "Ghi chú" ở màn Hàng hóa dự án (`/assign/product-project`) đang luôn trống. Fix để hiển thị ghi chú của từng hàng hóa, đồng bộ từ báo giá tự lập đã duyệt và BOM tổng hợp đã duyệt.

## Nguyên nhân
UI cả 2 luồng (modal thêm hàng ở Báo giá và BOM builder) **đã có sẵn ô "Ghi chú"** nhưng:
1. Object emit khi Áp dụng/Tạo hàng **bỏ rơi field `note`** → không tới BE.
2. 2 bảng nguồn `quotation_product_prices` + `bom_list_products` **không có cột `note`**.
3. BE transform trả `note = null` (báo giá hardcode null; BOM đọc cột không tồn tại).

## Nguồn giá trị note (mỗi dòng hàng hóa)
- **Chọn hàng từ danh mục ERP** → snapshot `note` của sản phẩm ERP (`ErpProductSearchService` đã trả `note`).
- **Thêm hàng tạm** → `note` người dùng nhập trong modal.
- Note lưu trực tiếp trên dòng (`*.note`) → transform trả về → cột hiển thị + export.

## Phạm vi
- 2 nguồn: Báo giá tự lập + BOM tổng hợp.
- Thêm cột DB, nối FE emit + payload, BE lưu + transform.
- **Ngoài scope:** luồng copy BOM→báo giá khi "làm giá" (báo giá gắn `bom_list_id` bị loại khỏi màn này).

## Điểm chạm chính
- DB: 2 migration thêm `note` TEXT nullable.
- FE: `QuotationProductSearchModal.vue`, `quotations/_id/edit.vue`, `BomBuilderAddProductModal.vue`, `BomBuilderEditModal.vue`, `BomBuilderEditor.vue`.
- BE: `QuotationService::upsertPrices`, `BomListService::mapProductPayload`, `ProductProjectController::transformQuotationItem`.

Spec chi tiết: `docs/superpowers/specs/2026-07-06-product-project-note-sync-design.md`
