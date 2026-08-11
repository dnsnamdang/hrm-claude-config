# Plan — Thêm cột "Quy cách" / bỏ "Đơn vị tính" ở file xuất Excel (tab Thông tin bổ sung, Danh mục hàng hóa)

**Người phụ trách:** @khoipv
**Màn:** `category/product/{id}/edit` → tab **Thông tin bổ sung**
**File:** `hrm-thanhan-client/pages/category/product/components/AdditionalInfo.vue` (chỉ FE, không đụng BE)

## Bối cảnh

4 bảng trong tab có nút "Xuất Excel", tất cả gọi chung hàm `exportAdditionalInfoList()`:

| Bảng | Hàm | Cột đo lường hiện tại |
|---|---|---|
| Vật tư, phụ kiện thay thế sửa chữa | `exportReplacementAttachment` | Số lượng |
| Hàng hóa rời kèm máy | `exportAccessoryOther` | Số lượng |
| Hóa chất sử dụng | `exportChemical` | **Đơn vị tính** |
| Thiết bị sử dụng | `exportDevice` | **Đơn vị tính** |

## Yêu cầu

1. Thêm cột **Quy cách** vào cả 4 file Excel — nguồn `products.specification`, lấy kèm trong lời gọi `category/products/getData` đang có sẵn (đang lấy `content_no_html` cho cột Thông số kỹ thuật).
2. Bảng nào có cột **Đơn vị tính** (Hóa chất, Thiết bị) → **bỏ** cột đó khỏi file Excel. Cột "Số lượng" của 2 bảng còn lại giữ nguyên.
3. Chỉ đổi file xuất Excel, KHÔNG đổi bảng hiển thị trên UI.

## Cột sau khi sửa

- Vật tư / Hàng hóa rời: STT · Mã nội bộ · Mã phụ kiện · Tên phụ kiện · Model · Hãng, nước sản xuất · **Quy cách** · Số lượng · Thông số kỹ thuật
- Hóa chất / Thiết bị: STT · Mã nội bộ · Mã hóa chất(thiết bị) · Tên · Model · Hãng, nước SX (chủ sở hữu) · **Quy cách** · Thông số kỹ thuật (~~Đơn vị tính~~)

## Task

- [x] T1 — `exportAdditionalInfoList`: lấy thêm `specification` từ response `getData` vào `specificationMap`
- [x] T2 — Dựng cột động (mảng có `getValue`/`center`) thay mảng cứng, bỏ index cứng `i === 6` khi canh lề
- [x] T3 — Thêm cột "Quy cách" sau cột hãng/nước
- [x] T4 — Thêm option `showMeasure`; `exportChemical` + `exportDevice` truyền `showMeasure: false` để bỏ cột Đơn vị tính
- [x] T5 — Rà lại 4 hàm export (chỉ sửa `<script>`, template không đổi)

### Checkpoint — 2026-08-07
Vừa hoàn thành: T1–T5, sửa duy nhất `AdditionalInfo.vue` (3 chỗ: `exportChemical`/`exportDevice`, `specificationMap`, mảng `columns` + vòng ghi dữ liệu).
Đang làm dở: không có.
Bước tiếp theo: user mở `category/product/3767/edit` → tab Thông tin bổ sung → bấm Xuất Excel ở cả 4 bảng để verify.
Blocked:

## Ghi chú

- Không migration, không sửa BE (`DetailProductResource` đã trả sẵn `specification`).
- Không phân quyền theo cấp.
