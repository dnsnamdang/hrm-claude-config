# Plan — HĐ mua: cho nhập tay VAT (%) ở bảng hàng hóa

**Người phụ trách:** @khoipv
**Ngày:** 23/10/2026
**Màn:** `supply/purchase_contracts` (Lập / sửa HĐ mua)

## Yêu cầu
Cột **VAT (%)** ở bảng hàng hóa đang khóa (tự lấy `products.tax`, BE snapshot lại khi lưu) → cho người lập **tự nhập tay**.

## Quyết định
- Thêm dòng mới / đổi hàng: VAT gợi ý sẵn theo danh mục hàng hóa (`products.tax`), sửa tay được.
- Đã có % trên dòng (đã lưu hoặc đã nhập) → giữ nguyên, KHÔNG tự đè lại theo danh mục.
- Xóa trống ô → coi là 0%.
- BE: HĐ mua nhận `vat_percent` FE gửi (0–100); FE không gửi → fallback `products.tax`.
- KHÔNG sửa trait dùng chung `CalculatesPurchaseLineMoney::lineVat()` (Đơn mua hàng vẫn dùng) — viết hàm riêng trong `PurchaseContractService`.

## Task
### BE
- [x] B1. `StorePurchaseContractRequest`: validate `products.*.vat_percent` nullable numeric 0–100 + message
- [x] B2. `PurchaseContractService`: hàm `contractLineVat()` ưu tiên số FE gửi, fallback danh mục; thay 2 chỗ gọi `lineVat()` (calcTotalAmount + lưu dòng)

### FE (`components/ProductsTab.vue`)
- [x] F1. Cột VAT đổi sang ô nhập số (V2BaseInput như ô CK%), hiện lỗi 422
- [x] F2. `vatOf()` ưu tiên `p.vat_percent`, chưa có mới lấy `taxMap`; thêm `onVatInput()`
- [x] F3. Đổi hàng / bỏ đổi → reset `vat_percent` để gợi ý lại theo hàng mới

### Checkpoint — 23/10/2026
Vừa hoàn thành: B1, B2, F1, F2, F3 (php -l + compile template OK)
Đang làm dở:
Bước tiếp theo: user build client + test UI (thêm hàng → VAT gợi ý theo danh mục; sửa tay → tiền trước VAT/VAT/tổng đổi theo; lưu → mở lại giữ đúng %; nhập >100 → báo đỏ)
Blocked:

## Lưu ý downstream
- Đơn mua hàng vẫn chốt VAT theo danh mục (`lineVat()`), không kế thừa % nhập tay của HĐ mua.
- HĐ cũ mở sửa giờ GIỮ % đã lưu, không tự cập nhật theo danh mục mới nữa.
