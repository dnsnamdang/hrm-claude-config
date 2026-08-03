# Design tóm tắt: Chọn trường & loại giá khi xuất Excel — màn Quản lý giá hàng hóa

**@khoipv · 2026-06-29**

## Mục tiêu
Màn `category/product_unit_price` hiện xuất Excel cứng toàn bộ cột + toàn bộ loại giá.
Bổ sung modal cho người dùng **chọn trường thông tin** và **chọn loại giá** trước khi xuất.
Vẫn xuất FE bằng ExcelJS.

## Scope
- **Chỉ Frontend.** Không đổi Backend, không đụng `export-modal.vue` dùng chung của HR.
- Tạo component mới `export-product-price-modal.vue` (2 mục Select2 multiple + "Chọn tất cả").
- Sửa `product_unit_price/index.vue`: nút mở modal, `EXPORT_FIELDS`, `handleExport(selection)`,
  `generateWorkbook` dựng cột động.

## Quyết định lớn (đã chốt với user)
1. **Modal popup** khi bấm "Xuất excel" (theo idiom màn hồ sơ nhân sự).
2. **2 mục riêng**: "Chọn trường thông tin" (10 trường, đều chọn được) + "Chọn loại giá"
   (Giá vốn + price_types động).
3. **Mặc định tích hết** cả 2 mục khi mở.
4. **Validate mỗi mục ≥1**: thiếu trường hoặc thiếu loại giá → chặn xuất + báo đỏ.
5. **Tôn trọng bộ lọc hiện tại** (giữ `fetchAllPages`).
6. "Giá vốn" dùng id quy ước `'capital'`.
7. Không lưu cấu hình giữa các phiên (YAGNI).

## Tài liệu chi tiết
- Spec đầy đủ: `docs/superpowers/specs/2026-06-29-product-unit-price-export-fields-design.md`
- Plan chi tiết (5 task): `docs/superpowers/plans/2026-06-29-product-unit-price-export-fields.md`
- Plan tổng quát: `.plans/product-unit-price-export-fields/plan.md`
