# N77 — giá vốn lộ qua dữ liệu nhúng trang chứng từ ERP (soát 13/10/2026, chỉ đọc)

> ERP `wt-erp-2d1` @`3432ca97ac` (sau đợt C-a), DB `hrm_erp_giacty`. Không sửa source, không ghi DB.

## Kết luận: CÓ THẬT

- Bằng chứng: `RootOrderRequest::getDataForEdit(7692)` / `getDataForShow(7692)` (gọi với tư cách người lập) ⇒ JSON có
  `units[0].cost_price = "240000.00"` (+ `buy_price`, `sale_max_percent_…`, cờ chờ duyệt…). View
  `orders/root_order_requests/edit.blade.php:36` đổ nguyên `@json($object)` vào JS ⇒ ai mở được trang sửa/xem (người lập,
  người duyệt) xem mã nguồn trang là thấy giá vốn.
- Nguồn: `ProductPriceService::unitsInfoFor()` (accessor `units_info`, `Product::dataFor()`) LUÔN kèm 13 cột
  `product_company_units`. ~25 hàm dựng dữ liệu trang sửa/xem/sao chép gắn kết quả này vào chứng từ: YC đặt hàng
  (4 loại + tổng), HĐ mua trong nước / nhập khẩu / phụ lục, PI, hồ sơ nhập hàng, YC chuyển hàng, giữ hàng, tồn đầu kỳ kế toán,
  kiểm kê (2 màn), báo giá / HĐ DV BH-SC, khuyến mại / combo, CSKH, Tiếp nhận BH (danh sách: `grep unitsInfoFor\|units_info\|dataFor(` trong `app/`).
- Server KHÔNG đọc 13 cột này qua `units` của Product ở đâu cả (3 chỗ `units_info[0]->cost_price` là của `ProductInfo` /
  `ProductTemplate` — bảng khác). JS màn chứng từ cũng không đọc (chỉ form hàng hoá / màn giá / hàng tạm — đã chặn sang HRM).
  ⇒ sửa TẬP TRUNG được: `unitsInfoFor()` mặc định KHÔNG kèm 13 cột (giữ ĐVT + `prices`).
- Không có model nào `$appends` units ⇒ không có đường rò tự động khác.

## Điểm liên quan phát hiện thêm

| # | Việc | Ghi chú |
|---|---|---|
| N77-b | Màn **Chi tiết hàng hoá ERP** (`products/{id}/show`, quyền "Xem hàng hóa", KHÔNG bị chặn) hiện ô **Giá vốn** + Giá mua (`products/formShow.blade.php:782,789`), dữ liệu dựng riêng ở `Product::getDataForEdit` (join pcu tại chỗ, không qua `unitsInfoFor`) | ERP không có quyền xem giá vốn; HRM có (1045) ⇒ cần user chốt |
| N80 | Trang xem YC xuất hàng (`product_export_requests/{id}/show`) nhúng khối hiệu quả HỢP ĐỒNG có `cost_price` = tổng giá vốn HĐ (293.126.007 ở PYCXH-40338) | ngoài phạm vi hàng hoá (tài chính HĐ) — ghi lại, hỏi user |
| — | Kiểm hồi quy C-a: class JS `ProductUnit` / `ProductWithPrice` đọc `liquidation_sale_max_percent` từ ĐVT — chỉ dùng ở form hàng hoá + màn giá (không gọi `getData`); màn thúc đẩy bán dùng `rate_liquidation` (vẫn giữ) + định mức từ dòng HĐ cũ ⇒ **không hồi quy** | |

## Đề xuất sửa (đợt C-a2, ERP)

1. `ProductPriceService::unitsInfoFor($pid, $cid, bool $withCost = false)` — mặc định bỏ 13 cột pcu; `stripSensitive` giữ làm lớp thứ 2.
   Không tìm thấy chỗ nào cần `$withCost = true` (ghi rõ trong test). Test G3 R1 đổi: cột giá vốn kiểm qua `ProductPriceService` hàm đọc giá vốn riêng (R8), không qua `unitsInfoFor`.
2. Tuỳ chốt N77-b: ẩn ô Giá vốn / Giá mua ở màn chi tiết hàng hoá ERP và không đưa 2 cột này vào dữ liệu trang.
3. Kiểm: PHPUnit (test mới: `unitsInfoFor` / `units_info` / `dataFor` không có 13 cột; chứng từ mẫu `RootOrderRequest::getDataForEdit` không có `cost_price`), quét lại ~25 hàm bằng tinker (JSON không còn cột pcu), Playwright vài màn sửa/xem chứng từ (thêm hàng, lưu nháp không lỗi), checksum.

## Chốt 13/10
- N77-b: **ẩn ô Giá vốn + Giá mua** ở màn chi tiết hàng hoá ERP, không đưa 2 cột vào dữ liệu trang.
- N80: ghi riêng STATUS gop-db, làm sau.
- ✅ User cho "LÀM" C-a2 13/10/2026 (nhánh `feat/ca2-gia-von-trang-chung-tu`).

## Kết quả code C-a2 (13/10 — user "làm" + "làm" phần mở rộng `$hidden`)

ERP nhánh con `feat/ca2-gia-von-trang-chung-tu` 2 commit ⇒ merge `3f017e66dd` vào `feat/2d1-erp-khong-loi` — **ĐÃ PUSH 13/10**, nhánh con đã xoá.

| Commit | Nội dung |
|---|---|
| `8b23629e97` | `unitsInfoFor($pid, $cid, $withCost = false)` mặc định bỏ 13 cột pcu; `getDataForShow` không select giá vốn; `products/formShow` bỏ ô Giá vốn + Giá mua ngoài (2 ô còn lại `col-md-6`) |
| `60719788f8` | **Mở rộng** (phát hiện khi quét: `withUnits()` select `product_units.*` 87 chỗ + ~176 eager load `units` — 24.877/46.560 dòng `product_units` còn giá vốn CŨ): `ProductUnit::$hidden = PRICE_COLUMNS`; `makeVisible` có chủ đích ở `units_for_history` (cost/buy), `getDataForEdit` (dữ liệu phiên bản), `getProductsAndPrices` (cờ/ghi chú cho mọi người; cost + định mức thanh lý khi có quyền "Cập nhật nhanh giá hàng hóa") |

Soát trước khi sửa: server không đọc 13 cột qua `units` của Product (chỉ request input, model bảng khác); JS màn chứng từ không đọc (chỉ form hàng hoá / màn giá / hàng tạm — đã chặn); Biên bản kiểm kê lấy giá riêng (import/export price).

**Kiểm**: PHPUnit ERP 89 (CaPublicProductDataTest 8: unitsInfoFor mặc định / withCost, `$hidden` khi eager load `withUnits`, lịch sử vẫn ghi giá vốn) — chỉ đỏ sẵn `ExampleTest`.
Tinker quét JSON trên giacty: YC đặt hàng tổng #7692, YC đặt hàng trong nước #930 / mới #4990, BG DV BH-SC #11662 (edit/copy/show), **HĐ mua trong nước mới #2090 (trước 20 khoá ⇒ 0)**, YC xuất ghép #666, YC nhập #14033, combo #5173 ⇒ 0 cột pcu trong `units`; `getDataForVersion(3897)` vẫn có `cost_price` (đúng thiết kế); YC xuất hàng #40338 show còn 1 `cost_price` = tổng giá vốn HĐ (N80, làm sau).
Playwright (8090, role tạm `CA2_UAT_TMP` 117397 — đã gỡ): chi tiết hàng hoá 3897 — HTML 0 `cost_price`/`buy_price`, template hàng đầu 2 × `col-md-6`, không còn nhãn Giá vốn / Giá mua (phần ĐVT vốn không render do lỗi cũ **N51** `$parse:syntax` — đợt C-c; đo bố cục sau khi sửa N51); Hàng sắp điều chỉnh giá: không quyền ⇒ 20 ĐVT có cờ, 0 giá vốn; có quyền ⇒ 20/20 có giá vốn + định mức; YC xuất hàng / YC xuất ghép thêm hàng OK, xem YCXG-00666 OK, 0 pageerror.
Dữ liệu: CRC32 8 bảng (pup, pcu, pep, product_units, products, companies, versions, histories) trước = sau; roles 129 · rhp 18.418 · ehr 1.720; server tắt đúng PID; không log lỗi Laravel.

### Checkpoint — 2026-10-13 (C-a2)
Vừa hoàn thành: C-a2 (N77 + N77-b + mở rộng `$hidden`), merge LOCAL `3f017e66dd`.
Đang làm dở: không.
Bước tiếp theo: push khi user báo · đợt C-b (chặn ghi danh mục ERP: N76, N32, N33, N42, N78?) — khảo sát "thêm nhanh" + `pi-*` ⇒ plan ⇒ hỏi tồn ⇒ xin "làm". Lưu ý đo lại bố cục màn chi tiết hàng hoá sau khi sửa N51 (C-c).
Blocked: —
