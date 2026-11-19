# Đóng màn Lịch sử chỉnh sửa hàng hoá ERP — Design

> 29/10/2026 · repo `TanPhatDev`, nhánh `gop_db` · commit `a58d3e8c1f` (đã push).

## Bối cảnh
- Sau gộp DB, mọi route GHI hàng hoá ở ERP đã chặn bằng middleware `productMovedToHrm` (trang "Chức năng đã chuyển sang HRM").
- Route đọc `productHistory` (`GET admin/products/{id}/history`) được **cố ý giữ** theo H4 của
  `HRM/.plans/gop-db/quan-ly-hang-hoa/lich-su-hang-hoa/design.md`: HRM chỉ ghi lịch sử từ go-live 21/10, log cũ ERP
  (`product_histories` ~324k dòng, `product_versions` ~117k) xem ở màn ERP này.

## Quyết định (user chốt 29/10)
- Đóng hẳn màn này — **chấp nhận không còn xem log ERP trước 21/10** ở đâu (đảo H4). Không chuyển dữ liệu cũ sang HRM.
- Đích link trên trang báo: `product-show` ⇒ màn chi tiết hàng hoá HRM `/master-data/products/{id}` (có popup Lịch sử từ 21/10).

## Thay đổi
| File | Nội dung |
|---|---|
| `routes/web.php` | `productHistory` + `->middleware('productMovedToHrm:product-show')` trước `checkPermission` |
| `app/Http/Controllers/ProductsController.php` | Bỏ mục "Xem lịch sử chỉnh sửa" ở cột action của 2 DataTable hàng hoá; menu dòng vẫn còn "In barcode" nên không rỗng |

Không đụng: `Product2Controller.php:214` (chuỗi không gán `$data` — code chết), `products/show.blade.php` (màn show đã chặn).
`ProductsController@history` giữ nguyên (route chặn trước khi vào).

## Liên quan
- Dữ liệu `product_histories` có version mồ côi (117326–175610) — không còn màn nào đọc, chưa xử lý.
