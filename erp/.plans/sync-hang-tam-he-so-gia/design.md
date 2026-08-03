# Design — Sửa hệ số/giá các loại giá khi đồng bộ hàng tạm HRM → ERP

## Mục tiêu
Khi đồng bộ hàng tạm từ báo giá HRM sang ERP, set đúng **hệ số + giá công thức + định mức đàm phán** cho TẤT CẢ loại giá (không chỉ Bán lẻ), để sản phẩm sau khi duyệt không còn 0/0/0 ở các loại giá ngoài Bán lẻ.

## Hiện trạng (bug)
`TmpProductRequestSyncService::createFromHrm()` chỉ tạo **1 dòng giá Bán lẻ** (`price = quoted_price`, `coefficient = 1`). 5 loại giá còn lại (Đại lý 1/2/3, theo lô, online) không được tạo → form draft/duyệt hiện 0 → SP thật bị **0/0/0**.

## Bối cảnh kỹ thuật
- Bảng `tmp_product_unit_prices`: mỗi loại giá 1 dòng, cột `price` (= "giá công thức"), `coefficient` (= "hệ số", `decimal(5,2)`), `sale_max_percent` (= "định mức đàm phán giá %"). "Giá bán" là giá dẫn xuất, không lưu cột riêng.
- `price_types`: 6 loại — 1=Bán lẻ, 2=Đại lý cấp 1, 3=Đại lý cấp 2, 4=Đại lý cấp 3, 5=Bán theo lô, 6=TMĐT online.
- Luồng duyệt: `TmpProductsController::approve()` → `Product::createRecord($request)` lấy giá từ **form người duyệt submit**, mà form nạp từ các dòng giá của hàng tạm. → Chỉ cần sync tạo đủ dòng giá ở tmp là chảy đúng sang product thật. **Không sửa luồng approve.**

## Mapping field HRM (xác nhận qua form chi tiết báo giá HRM)
- **giá nhập** = cột "Giá nhập (VND)" = payload `estimated_price`
- **giá bán trước chiết khấu** = cột "Giá bán (VND)" = payload `quoted_price`

## Quy tắc mới (mỗi hàng tạm — base unit)
Đặt `giaNhap = estimated_price`, `giaBan = quoted_price`. Tạo 1 dòng `TmpProductUnitPrice` cho **mỗi** loại giá trong `price_types`:

| Loại giá | price (công thức) | coefficient (hệ số) | sale_max_percent |
|---|---|---|---|
| **Bán lẻ (id=1)** | `giaBan` | `giaNhap > 0 ? round(giaBan / giaNhap, 2)` (cap 999.99) `: 1` | `0` |
| **Các loại khác** | `1` | `1` | `1` |

### Edge cases
- `giaNhap = 0` hoặc null → hệ số Bán lẻ = **1** (tránh chia 0).
- Hệ số làm tròn **2 chữ số thập phân**; nếu > 999.99 → cap **999.99** (giới hạn `decimal(5,2)`).
- Lấy danh sách loại giá bằng query `price_types` (không hardcode) → thêm loại giá mới sau này tự động = 1/1/1 (trừ Bán lẻ).

## File thay đổi
- `app/Services/Sale/TmpProductRequestSyncService.php` — sửa khối tạo giá trong `createFromHrm()` (hiện dòng 64–70).

## Không đụng tới
- `approve()` / `CreateProductService`.
- `cost_price` / `buy_price` của unit (vẫn = `estimated_price`).

## Branch
`sync_quotation` (local).
