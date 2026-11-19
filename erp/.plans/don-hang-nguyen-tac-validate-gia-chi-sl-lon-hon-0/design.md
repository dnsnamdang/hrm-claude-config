# Đơn hàng nguyên tắc — chỉ validate giá với hàng SL > 0

## Bối cảnh / Triệu chứng
Màn **Lập đơn hàng nguyên tắc** (`/admin/sale/principle-orders/create?firm_contract_id=...`) báo lỗi đỏ (tooltip):

> Hàng hoá `SGCB-SGHM002` chưa có giá "Đại lý cấp 7" tại CÔNG TY ... CHI NHÁNH VINH. Vui lòng lấy hàng về / cập nhật giá bán cho công ty này trên HRM.

Lỗi bắn ra kể cả khi dòng hàng đó **số lượng = 0** (dòng placeholder / hàng chưa chọn SL), chặn cả thao tác **Lưu nháp**.

## Nguyên nhân gốc
`Product::getPriceByUnitAndType()` → `ProductPriceService::priceOf()` **ném** `PriceNotFoundForCompany`
(extends `ModelNotFoundException`) khi công ty trên chứng từ chưa có giá bán của mặt hàng.

Hai nơi gọi hàm này **không chặn theo số lượng** trước khi gọi, nên dòng qty=0 cũng kích hoạt throw:

1. **FormRequest** `PrincipleOrderStoreRequest::rules()` — vòng lặp `foreach ($tab['products'])` gọi
   `getPriceByUnitAndType(...)->price` **vô điều kiện** ở đầu mỗi vòng; guard `if ($product['quantity'] > 0)`
   nằm **sau đó** và chỉ bọc phần sinh rule giá, không bọc lời gọi lookup. → đây là validator "sống" user thấy.
2. **Service** `PrincipleOrderService` (hàm lưu product) — `getPriceByUnitAndType(...)->sale_max_percent`
   vô điều kiện. Chốt chặn `if ($status == CHO_DUYET && quantity == 0) continue;` chỉ bỏ qua dòng qty=0
   **khi Gửi duyệt**; khi **Lưu nháp (DANG_TAO)** dòng qty=0 vẫn chạy tới lời gọi và throw.

Nơi thứ 3 — `PrincipleOrderService::validateDifferenceListPrice()` — **đã** gate `if ($prod['quantity'] > 0)`, không phải sửa.

Biến thể nha khoa (`ZTPrincipleOrderStoreRequest` + `ZTPrincipleOrderService`) có **y hệt** 2 lỗi trên.

## Quyết định đã chốt
- Chỉ validate/tra giá theo công ty với **hàng SL > 0**. Dòng qty≤0 bỏ qua hoàn toàn phần giá.
- Ở service: dòng qty>0 vẫn dùng `getPriceByUnitAndType` (ném lỗi như cũ để chặn đúng chỗ);
  dòng qty≤0 dùng `ProductPriceService::priceOrNull()` (trả null → `sale_max_percent = 0`, không ném).
- Sửa **cả** biến thể thường **và** biến thể nha khoa (zt) cho nhất quán — cùng nghiệp vụ, cùng class lỗi.

## Phạm vi file sửa
- `app/Http/Requests/Sale/Firm/Order/PrincipleOrderStoreRequest.php`
- `app/Services/Sale/Firm/Order/PrincipleOrderService.php`
- `app/Http/Requests/Sale/Firm/Order/ZTPrincipleOrderStoreRequest.php`
- `app/Services/Sale/Firm/Order/ZTPrincipleOrderService.php`
