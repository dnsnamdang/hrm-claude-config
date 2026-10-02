# Fix: Phiếu tính giá hiển thị "Giá mới" sai (vẽ đè bằng giá công thức)

@junfoke — Repo `TanPhatDev` (bản B, `d:\CompanyProject\hrm-cursor\TanPhatDev`). Nguồn: KT báo qua chị Thuý, anh HD chốt "fix phía FE của phiếu tính giá, xem cả yêu cầu hỏi giá" (2026-09-07).

## Hiện tượng

Phiếu `PTG-03082` (GYSP-S97027) KT nhập & lưu giá mới **10,500,000** nhưng màn chi tiết hiện **10,714,200** (= giá công thức). Phiếu `PTG-03086` (DCAR-DC-G6410) lưu **2,500,000**, hiện **2,059,900**. Lịch sử giá hàng hoá KHÔNG có giá công thức đó → dữ liệu ghi nhận đúng.

## Kết luận điều tra

**Lỗi hiển thị thuần FE, DB đúng.** SQL trên prod xác nhận `price_calculate_product_prices.price` = đúng giá KT nhập; giá đã duyệt đẩy sang danh mục hàng hoá cũng đúng.

Phạm vi: gần như MỌI phiếu (KT luôn làm tròn tay nên phiếu nào cũng lệch công thức), không riêng 2 phiếu được báo. Cùng lỗi ở 3 màn dùng chung class `PriceCalculateProduct`:
- Chi tiết/Sửa **phiếu tính giá**
- Chi tiết **yêu cầu hỏi giá** (bảng giá khi `status = 4`, `form.price_calculate.chosen_products`)
- Chi tiết **kết quả tính giá** (nặng hơn: bảng result không có `cost_price` → công thức ra 0 → hiện giá 0)

## Nguyên nhân

Commit `542b97637e` (17/04/2026, nguyentrancu97) thêm `recalcAllPrices()` vào `after()` của `resources/views/partials/classes/order/PriceCalculateProduct.blade.php`. Ý định ban đầu chỉ phục vụ màn Tạo mới (giá seed từ danh mục hàng hoá), nhưng `after()` chạy cho MỌI lần khởi tạo → phiếu đã lưu bị tính lại `price = round(hệ số × giá nhập kho /100)*100` và ghi đè giá KT nhập. Giá TMDT (type 6) còn bị ép về công thức ở tầng getter `ProductPrice.shouldUseDatabaseEcommerceValue` do cờ `is_price_calculate_context`.

Rủi ro kèm theo (chưa xảy ra trên prod): phiếu trạng thái **Đang tạo** nếu mở Sửa rồi Lưu sẽ ghi giá công thức thật vào DB, vì `submit_data` lấy chính giá trị đã bị đè. Phiếu **Đã duyệt** không sửa được (`canEdit()` chỉ cho status = Đang tạo) nên dữ liệu prod an toàn.

## Cách fix

Chỉ recalc khi bản ghi CHƯA lưu:
- `PriceCalculateProduct`: thêm getter `is_saved_record` (form cha có `id`, hoặc dòng giá có `price_calculate_id`) → `after()` chỉ gọi `recalcAllPrices()` khi `false`.
- `ProductPrice.shouldUseDatabaseEcommerceValue()`: bản ghi đã lưu → luôn dùng giá DB (kể cả giá TMDT). Getter này dùng chung với màn cập nhật nhanh giá hàng hoá, nhưng ở đó `parent.is_saved_record` là `undefined` → không đổi hành vi.

Không đụng BE, không sửa data.

## File thay đổi

- `resources/views/partials/classes/order/PriceCalculateProduct.blade.php`
- `resources/views/partials/classes/sale/ProductPrice.blade.php`

## Verify (local :8001, DB `erp_dev_30_01_26`)

| Màn | Bản ghi | DB | Trước fix | Sau fix |
|---|---|---|---|---|
| Chi tiết phiếu tính giá | PTG-00007 | 3,600,000 | 3,660,000 | **3,600,000** |
| Sửa phiếu tính giá | PTG-00002 (Đang tạo) | 6,000,000 | 16,666,700 | **6,000,000** (submit_data cũng 6,000,000 → lưu không đè) |
| Chi tiết yêu cầu hỏi giá | PYCHG-00013 | 3,600,000 / 3,366,000 | 3,660,000 | **đúng DB** |
| Chi tiết kết quả tính giá | id 6 | 3,600,000 / 3,366,000 | 0 | **đúng DB** |
| Tạo mới (không hồi quy) | PYCTG-00016 | — | — | vẫn recalc: 100,000 (hệ số 1 × 100,002), TMDT 230,000 |

---

# Phần 2 — #11334: Tab Tính giá hiển thị sai Đơn giá (07/09/2026)

Redmine: http://quanly.dnsmedia.vn/issues/11334 — "[Kế toán] Phiếu tính giá: Tab tính giá - Hiển thị sai đơn giá", khẩn cấp, phân công Trần Cư. Kiểm thử: PTG-03046 (JONN-JA-960:01, thuế NK 25%).

## Yêu cầu
Cột **Đơn giá VNĐ** ở tab Tính giá phải lấy theo **Thành tiền sau thuế (VNĐ)** của tab Hàng hoá, không phải đơn giá trước thuế.

- Tab Hàng hoá: Giá NCC 82.5 USD × 26,600 = 2,194,500 → thuế NK 25% → **Thành tiền sau thuế 2,743,125**
- Tab Tính giá trước fix: Đơn giá VNĐ hiện **2,194,500** (`supplier_price_exchange`, chưa thuế)

## Quyết định nghiệp vụ (user chốt 07/09/2026)
**Giá nhập kho cũng cộng theo Thành tiền sau thuế.** Trước đây `cost_price = supplier_price_exchange + tổng chi phí + chi phí khác` → không gồm thuế NK, nên nếu chỉ sửa cột Đơn giá thì 3 cột trên bảng không cộng ra Giá nhập kho.

Hệ quả đã thông báo và được chấp nhận:
- Giá công thức (= giá nhập kho × hệ số) **TĂNG** với hàng có thuế NK > 0.
- Giá mới đã lưu **không đổi** (nhờ fix Phần 1).
- Giá vốn đẩy sang `product_units.cost_price` khi duyệt (`PriceCalculate::updatePriceWithApproval`) từ nay gồm cả thuế NK — chỉ áp cho phiếu duyệt MỚI, phiếu cũ giữ cột `price_calculate_products.cost_price` đã lưu trong DB.
- Thuế NK không nằm trong tab Chi phí (`costs` là chi phí vận chuyển/khác do user thêm) nên không có rủi ro tính trùng.

## File thay đổi
- `resources/views/orders/price_calculates/form.blade.php:267` — cột Đơn giá VNĐ tab Tính giá: `supplier_price_exchange` → `amount_exchange_after_tax` (dòng 154 tab Hàng hoá giữ nguyên vì đó đúng là cột "Đơn giá VNĐ" trước thuế)
- `resources/views/partials/classes/order/PriceCalculateProduct.blade.php` — getter `cost_price` cộng từ `amount_exchange_after_tax`

## Verify (local :8001, PTG-00002, nhập thử thuế NK 25%)
| | Thuế NK 0% | Thuế NK 25% |
|---|---|---|
| Đơn giá VNĐ | 11,111,111 | **13,888,888.75** |
| Giá nhập kho | 11,111,111 | **13,888,888.75** (khớp Đơn giá + Tổng CP + CP khác) |
| Giá công thức | 16,666,666.5 | 20,833,333.125 (tăng theo, đúng thiết kế) |
| Giá mới đã lưu | 6,000,000 | 6,000,000 (không đổi) |

DOM tab Tính giá đã đọc lại: header đúng cột, dòng 1 hiển thị 13,888,888.75 ở cả Đơn giá VNĐ lẫn Giá nhập kho.

## ĐIỂM MỞ — phiếu CŨ có thuế NK > 0 hiển thị Giá nhập kho lệch số đã lưu

`PriceCalculate::getDataForShow()` / `getDataForEdit()` **không select cột `cost_price`** (PriceCalculate.php:75 và :111) → FE không nhận giá nhập kho đã lưu, luôn tự tính bằng getter. Sau khi đổi công thức `cost_price`, mở lại phiếu cũ:

- Phiếu thuế NK = 0 (đa số, gồm PTG-03082 / 03086): **không đổi gì**.
- Phiếu thuế NK > 0 (vd PTG-03046): Đơn giá VNĐ + Giá nhập kho + Giá công thức hiện theo công thức MỚI, **khác cột `price_calculate_products.cost_price` đã lưu** và khác giá vốn đã đẩy sang danh mục lúc duyệt. Giá mới (giá bán) không đổi.

**Không ảnh hưởng dữ liệu / bán hàng**: màn xem không ghi DB; giá bán ở danh mục lấy từ giá đã duyệt. Đường ghi giá vốn mới chỉ có 2: tạo phiếu mới rồi duyệt, hoặc sửa & lưu phiếu đang ở trạng thái *Đang tạo* (phiếu Đã duyệt bị `canEdit()` chặn).

**Trạng thái: user hoãn quyết định (07/09/2026) — "chờ phương án sau".** Hiện đang chạy theo hướng để phiếu cũ hiển thị theo công thức mới. Phương án thay thế nếu sau này muốn giữ số đã lưu: BE select thêm `cost_price` ở 2 method trên + FE ưu tiên giá trị đã lưu khi ở mode `show` (màn Sửa vẫn tính lại). Lưu ý phiếu tạo trước migration `2026_02_24_260014_add_cost_price_to_price_calculate_products_table` có `cost_price = 0` → phải fallback tính lại, không thì hiện 0.

SQL đo phạm vi (đã gửi user):

```sql
SELECT pc.code AS phieu, pc.created_at, pcp.code AS ma_hang, pcp.import_tax,
       pcp.supplier_price_exchange   AS don_gia_truoc_thue,
       pcp.amount_exchange_after_tax AS don_gia_sau_thue,
       pcp.cost_price                AS gia_nhap_kho_da_luu,
       pcp.amount_exchange_after_tax - pcp.supplier_price_exchange AS chenh_lech_se_tang
FROM price_calculates pc
JOIN price_calculate_products pcp ON pcp.parent_id = pc.id AND pcp.chosen = 1
WHERE pcp.import_tax > 0
ORDER BY pc.created_at DESC;
```

## Số liệu prod kiểm chứng (07/09/2026) — đã loại rủi ro tính trùng thuế

Nghi vấn ban đầu: danh mục chi phí có mục **id 60 "Thuế nhập khẩu"** → nếu KT nhập thuế NK thành một dòng ở tab Chi phí thì `sum_cost` đã gồm thuế, cộng thêm `amount_exchange_after_tax` sẽ tính thuế 2 lần.

Kết quả chạy trên prod:
- Query liệt kê dòng chi phí có tên chứa "Thuế" ở các phiếu `import_tax > 0`: **rỗng** → không phiếu nào nhập thuế qua tab Chi phí. **Bỏ nghi vấn tính trùng.**
- Phân loại 1.484 dòng hàng hoá có `import_tax > 0`:

| Giá nhập kho đã lưu khớp công thức | Số dòng |
|---|---|
| TRƯỚC thuế + chi phí (công thức cũ) | **1.107** |
| SAU thuế + chi phí | 7 (trùng ngẫu nhiên, chi phí tình cờ bằng phần thuế — vd PTG-03081) |
| Không khớp công thức nào | 377 (nghi phiếu trước migration `cost_price` 24/02/2026 nên cột = 0 — đang chờ query xác nhận) |

Kết luận: `cost_price` xưa nay **chưa từng gồm thuế NK**; đổi công thức là thay đổi có chủ đích, không cộng trùng, không đụng dữ liệu cũ. Lịch sử code cũng khớp: bản trước commit `355df8dd5d` (31/01/2026) là `exchanged_price + sum_cost + other_cost` với `exchanged_price` = giá NCC × tỉ giá (không thuế).

Quy mô ảnh hưởng hiển thị: **1.107 dòng phiếu cũ** sẽ hiện Giá nhập kho cao hơn số đã lưu đúng bằng phần thuế NK (giá mới + DB + bán hàng không đổi) — xem mục ĐIỂM MỞ ở trên.

---

# Phần 3 — #11335: Thiếu link xem chi tiết Yêu cầu tính giá (07/09/2026)

Redmine: http://quanly.dnsmedia.vn/issues/11335 — "[Kế toán] Phiếu tính giá: Thiếu link xem chi tiết Yêu cầu tính giá", ưu tiên Cao, kiểm thử PTG-03086.

Ô **Chọn yêu cầu tính giá** ở đầu màn phiếu tính giá chỉ là `<input disabled>` hiện mã PYCTG-xxxxx, không mở được chi tiết yêu cầu.

**Fix theo pattern có sẵn** (không tự nghĩ kiểu mới): copy khuôn ô "Phiếu yêu cầu" ở `resources/views/orders/firm_warrantys/form.blade.php:16` — thay input disabled bằng `<div class="form-control">` chứa `<a class="p-0" target="_blank">`. Bổ sung thêm so với khuôn gốc: `ng-if` để màn Tạo mới (chưa chọn yêu cầu) hiện chữ placeholder xám thay vì thẻ link rỗng.

File: `resources/views/orders/price_calculates/form.blade.php` (dùng chung cho create/edit/show, ~7 dòng). Route đích `PriceCalculateRequest.show` đã có sẵn (routes/web.php:2275). File này là **CRLF** — đã giữ nguyên, diff 7+/2-.

## Verify (local :8001)
- Chi tiết PTG-00007: hiện `PYCTG-00009`, href `/admin/orders/price_calculate_requests/9/show`, `target=_blank`; fetch link trả **HTTP 200**, title "Chi tiết yêu cầu tính giá PYCTG-00009".
- Màn Tạo mới khi chưa chọn: hiện placeholder "Yêu cầu tính giá...", **không render thẻ link rỗng**; sau khi chọn PYCTG-00016 thì link đổi đúng sang `/16/show`.
