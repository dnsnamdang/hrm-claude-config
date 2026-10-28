# Đối chiếu Tồn bán được + đo tốc độ API popup chọn hàng (A7 P4 bước 4.2 — 13/10/2026)

## 1. Đối chiếu Tồn bán được HRM ↔ ERP (DB `hrm_erp_giacty`, chỉ đọc)
- ERP (`wt-erp-2d1`): `App\Product::stockCompanies()` — tách `company_codes` / `in_stocks` theo công ty ⇒ 10.996 hàng có tồn, 5 công ty (1, 2, 3, 4, 8).
- HRM: `SellableStockReader::forProducts(ids, company)` cùng bộ hàng.
- **Kết quả: so 15.345 dòng (hàng × công ty) — lệch 0. HRM có tồn mà ERP không có: 0.**
- Đổi công thức ở ERP (`app/Product.php:5998-6079`) thì phải đổi `Modules/MasterData/Services/Product/SellableStockReader.php` và chạy lại đối chiếu.

## 2. Đo tốc độ (API dev 8031, 5 lượt/ca, công ty 1; ~0,26s là chi phí xác thực cố định mỗi request)
| Ca | Thời gian | Tổng |
|---|---|---:|
| Mặc định (chỉ hàng đã xếp catalog) | 0,32s | 21 |
| `include_uncataloged=1` | 0,39s | 28.371 |
| + `keyword=bom` | 0,43s | 708 |
| + `in_stock=1` | 0,64–0,68s | 5.794 |
| `tree-counts` (`include_uncataloged=1`) | 0,41s | 28.371 |
| `machine_id=22034` | 0,35s | 126 |
| `machine_id=22034&include_service_shared=1` | 0,40s (trước sửa: **> 60s, làm chết server dev**) | 126 |
| `include_uncataloged=1` + 3 cột tuỳ chọn + bảng giá | 0,40s | 28.371 |
| `items` 2 id | 0,32s | 1 |

**Sự cố đã sửa:** `productables` (46.863 dòng) chỉ có khoá chính ⇒ `EXISTS` tương quan trong nhánh `OR` (chế độ máy + công tắc dùng chung)
quét toàn bảng cho từng hàng. Đổi sang `products.id IN (subquery không phụ thuộc)`; test `loc_qua_productables_khong_dung_subquery_phu_thuoc`
đọc `EXPLAIN` chặn hồi quy. **Không cần migration index** ở bước 4.2 (mọi ca < 1s). Index N84 / `productables(product_id…)` vẫn là
việc tối ưu riêng, không chặn.

## 3. Ca chỉ có tồn ở kho khuyến mãi (sửa 13/10, user duyệt)
- Trước: HRM bỏ kho KM ở WHERE ⇒ hàng chỉ có tồn kho KM mất dòng ⇒ 0; ERP giữ dòng (tồn thường = 0) ⇒ đang giữ hàng/tạm giữ/YC xuất thì ra ÂM.
- Nay: HRM bỏ kho KM trong `SUM(CASE…)` như ERP ⇒ ra cùng số âm. Dữ liệu 13/10: 16 cặp (hàng, cty) chỉ có tồn kho KM, 0 cặp đang giữ hàng.
- Đối chiếu lại sau sửa: 15.345 dòng, lệch 0. Đo lại: search in_stock 0,66–0,91s; tree-counts in_stock 0,87–1,0s (sát mục tiêu 1s — theo dõi khi dữ liệu tăng).
