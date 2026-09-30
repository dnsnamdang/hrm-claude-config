# Popup "Tìm kiếm hàng hóa" — 2 ô cùng nhãn "Loại hàng hóa"

Người phụ trách: @junfoke — Repo `TanPhatDev`, nhánh `master`.

## Hiện trạng (trước fix)

Modal dùng chung `resources/views/partials/modals/searchProduct.blade.php` (99 màn `@include`, trong đó có
popup chọn hàng khuyến mãi ở PI — tất cả luồng mua) có **2 ô select khác nhau nhưng cùng ghi "Loại hàng hóa"**:

| Ô | ng-model | Nguồn | Cột DB lọc | Multiple |
| --- | --- | --- | --- | --- |
| Ô đầu (hàng 1, trái) | `search.product_type` | hằng JS `PRODUCT_TYPES` (Máy móc thiết bị, Dụng cụ cầm tay, Phụ tùng ô tô, Vật tư, Dầu nhờn…) | `products.product_type` | ❌ chọn 1 |
| Ô dưới (hàng 4, w-40) | `search.product_cates` | hằng JS `cates` (Nhập thường xuyên, Hàng tiêu chuẩn, Bảo hành sửa chữa, Hàng cho thuê…) | `products.product_cate` | ✅ |

Không phải ô thừa — cả 2 đều gửi lên `SearchController::searchProduct()` và lọc thật. Đây là **lỗi đặt nhãn**:
2 tiêu chí nghiệp vụ khác nhau trùng tên nên user tưởng bị nhân đôi.

Tham chiếu cách đặt tên đúng đã có sẵn: `searchProductQuotation.blade.php:36` gọi ô này là **"T/chất hàng hóa"**.

## Quyết định (user chốt 11/09/2026 — phương án A)

Giữ **cả 2** ô lọc (không mất tiêu chí nào), chỉ:
1. Đổi nhãn ô đầu → **"Tính chất hàng hóa"**.
2. Cho ô đầu **chọn nhiều** (`multiple`), đổi `search.product_type` → `search.product_types` (mảng).

BE **không phải sửa**: `SearchController.php:573` đã có sẵn `whereIn('products.product_type', $request->product_types)`.
Vẫn giữ nguyên key `product_type` (đơn) trong `$scope.search` và trong payload để không phá màn nào đang tự set nó.

Không đụng layout (grid `w-20`/`w-40` cố định, dời ô sẽ vỡ hàng ở 99 màn).

## File đổi

- `resources/views/partials/modals/searchProduct.blade.php` — ô đầu: `multiple` + `data-placeholder` + `ng-value`.
- `resources/views/partials/modals/js/searchProductJs.blade.php` — thêm `product_types: []` vào `search`,
  gửi `d.product_types` ở 2 DataTable (searchProductTable + searchProductPromotionTable), thêm vào 2 hàm reset.
