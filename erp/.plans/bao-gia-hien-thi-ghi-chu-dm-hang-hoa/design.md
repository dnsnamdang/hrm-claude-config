# Báo giá — Hiển thị Ghi chú DM hàng hóa dưới mỗi dòng hàng

**Task**: Redmine #11280 — @junfoke
**Repo**: `TanPhatDev` (ERP, Laravel + AngularJS) — nhánh `task_11280`

## Mục tiêu

Với **tất cả loại báo giá**, ở các màn **Thêm / Sửa / Xem chi tiết / Sao chép**, hiển thị
**Ghi chú của hàng hóa trong DM hàng hóa** (`products.note`) ngay **dưới dòng tên hàng**,
**màu đỏ**, dạng `Ghi chú nội bộ: <nội dung>`.

**KHÔNG** hiển thị ghi chú này trong **mẫu in (PDF)** và **file xuất Excel** báo giá.

## Phạm vi (4 loại báo giá — 2 codebase)

| Loại | Link | Codebase |
|------|------|----------|
| BGHH — Báo giá vật tư/hàng hóa/thiết bị | firm-quotations?type=all | `FirmQuotation` |
| BG HĐNT — Báo giá hợp đồng nguyên tắc | firm-quotations?quotation_type=3 | `FirmQuotation` |
| BGDA — Báo giá dự án | firm-quotations?quotation_type=2 | `FirmQuotation` |
| BGDV — Báo giá dịch vụ sửa chữa/bảo dưỡng/bảo trì | warranty_repair_service_quotations | `ServiceQuotation` |

## Nguồn dữ liệu

- Ghi chú lấy từ cột **`products.note`** (migration `2020_06_16_095517_add_note_to_products`,
  bind ở `products/form.blade.php:152` `product.note`). Ảnh 2 trong task minh hoạ trường "Ghi chú"
  ở màn chi tiết hàng hóa.

## Quyết định thiết kế then chốt

1. **KHÔNG dùng lại field `note`** trên FE row — `this.note` đã là **ghi chú nội bộ theo dòng**
   do user tự nhập ("Thêm Ghi Chú", lưu vào `*_products.note`). Ghi chú DM hàng hóa là trường KHÁC.
   → Đưa vào FE row bằng field mới **`catalog_note`** (đọc-only, không nằm trong `submit_data`).
2. `getProductsAndPrices` (nguồn khi Thêm/Sao chép — FirmQuotation) đã `select('p.note')` sẵn (dòng 2325).
   Vấn đề: constructor row copy mọi key → `p.note` sẽ đè `this.note`. Phải alias thành `catalog_note`
   ở nguồn (BE) hoặc lọc key (FE) để tránh nuốt per-line note.
3. Màn **Sửa/Chi tiết**: product rows nạp từ bản ghi báo giá đã lưu → BE resource của từng loại phải
   trả kèm `catalog_note` (join sang `products.note` theo `product_id`; hàng tạm/tmp_product không có → rỗng).
4. Chỉ hiển thị khi `catalog_note` khác rỗng (ẩn hẳn dòng nếu trống).
5. Print (pdf*.blade) + Excel export blades: KHÔNG thêm `catalog_note`.

## Files dự kiến đụng (xác nhận lại khi code)

**FirmQuotation (BGHH/HĐNT/BGDA)**
- FE class: `resources/views/partials/classes/sale/firm/quotation/FirmQuotationTabProduct.blade.php`
  → `getAttribute()` thêm dòng đỏ `Ghi chú nội bộ:`.
- Nguồn Thêm/Sao chép: `ProductsController::getProductsAndPrices` (alias note → catalog_note).
- Nguồn Sửa/Chi tiết/Sao chép: `FirmQuotationController` (edit/show/getDataForCopy) + resource product row.

**ServiceQuotation (BGDV)**
- FE class: `resources/views/partials/classes/sale/ServiceQuotationItemProduct.blade.php`
- Controller + nguồn product tương ứng.

**Loại trừ** (KHÔNG sửa để có note): `sale/firm/quotations/partials/pdf*.blade.php`,
`sale/firm/quotations/exports/quotation_excel*.blade.php`, và tương đương bên service.

## Chưa chốt / cần xác nhận
- Wording nhãn: dùng **"Ghi chú nội bộ:"** (theo mockup ảnh 3). Chờ user xác nhận.
- Làm đủ 4 loại/2 codebase trong 1 lượt, hay tách FirmQuotation trước → BGDV sau.
