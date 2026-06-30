# Report — Sửa 4 finding review (FIX #1, #3, #6, #7)

Ngày: 2026-06-20

## FIX #1 (CRITICAL — phồng tiền con) — DONE
File: `app/Services/Sale/Firm/Contract/FirmContractService.php`, method `syncTabsFromQuotation`.

Cách xác định dòng con: `$isChild = !empty($firm_quotation_product->child_parent_id);` (lấy từ BG gốc), đặt ở cả 2 vòng lặp product.

### Các biến tổng đã loại con (chỉ skip phần cộng cho con):
1. **`$total_extra`** (vòng lặp 1, trước đây dòng `$total_extra += $product['price_extra'] * $firm_quotation_product->quantity;`) — nay bọc `if (!$isChild)`. Biến này lan truyền tiếp xuống:
   - `$t_attributes['total_extra']` (tab) → `total_before_vat` của tab
   - `$contract->total_product_extra += $total_extra;`
   - `$contract->total_extra += $total_extra;`
   → Loại con khỏi gốc nên tất cả các tổng dẫn xuất này đều không còn tiền con.
2. **`$contract->total_product_cost += $product['total_cost'];`** (vòng lặp 2, ~dòng 700 cũ) — nay bọc `if (!$isChild)`.

### Các biến KHÔNG đụng (không accumulate per-product trong loop, lấy nguyên từ BG/FE — không bị phồng):
- `$t_attributes['total_cost']`, `total_after_vat`, `vat_cost`, `total_discount` (lấy từ `$firm_quotation_tab->attributesToArray()` và `$tab[...]` của FE).
- `$contract->total_product_vat`, `$contract->total_vat` (cộng `$firm_contract_tab->vat_cost`, là tổng tab chứ không per-product).

### Xác nhận giữ nguyên hành vi cho dòng con:
- `$product['total_cost']` vẫn được tính cho con (chỉ không cộng vào tổng).
- `$firm_contract_product->save();` nằm NGOÀI `if (!$isChild)` → dòng con VẪN được tạo + lưu.
- Map lượt 2: `$quotationToContract[$quotationProductId]` và `$contractByQuotationId[$quotationProductId]` ghi NGOÀI `if` → con vẫn vào map → vòng lặp remap cha-con (lượt 2) vẫn set `child_parent_id`/`child_ratio` đúng cho HĐ.

## FIX #3 (IMPORTANT — ép SL con server-side) — DONE
File: `app/Services/Sale/Firm/Quotation/FirmQuotationService.php`, method `syncProducts`.

Thứ tự thực hiện (đã đảm bảo ép quantity TRƯỚC khi tính total_cost):
1. Thêm map `$tmpToQty = [];` cạnh `$tmpToReal`.
2. Sau `$p->fill($pro)` + gán parent/firm_quotation: **dời block resolve cha-con lên trước** phần tính `total_cost`.
3. Với dòng con (resolve được `child_parent_tmp_id` qua `$tmpToReal`): nếu có `$tmpToQty[$child_parent_tmp_id]` và `child_ratio` → ÉP `$p->quantity = $tmpToQty[$child_parent_tmp_id] * (int)$p->child_ratio;`.
4. CHỈ SAU đó mới `$p->total_cost = $p->quantity * $p->price;` → total_cost của con tự recompute theo quantity đã ép. (Trong method này total_cost là field duy nhất phụ thuộc quantity.)
5. Sau `$p->save()`: lưu `$tmpToQty[$tmp_row_id] = $p->quantity;` để dòng con phía sau ép theo cha đã chốt.

Legacy-safe: dòng không phải con → `child_parent_id = null`, quantity giữ nguyên từ FE, total_cost như cũ. Đã xoá block resolve cha-con cũ (trùng lặp) ở cuối loop.

## FIX #6 (MINOR — ternary trùng) — DONE
File: `app/Http/Controllers/Warehouse/ProductExportRequestsController.php` (~dòng 647).
Thay 2 nhánh ternary giống hệt + xoá dòng `firstWhere` chỉ phục vụ ternary đó:
`$productLabel = "dòng HĐ #$fcpId";`

## FIX #7 (MINOR — comment sai) — DONE
File: `app/Model/Warehouse/ProductExport.php` (~dòng 1676).
Sửa comment cho đúng: ưu tiên (1) `firm_contract_tab_product_id` trực tiếp trên `$p` (cột đã tồn tại từ migration 100004), (2) qua bridge `ProductExportRequestTabProduct`, (3) khóa cũ legacy. KHÔNG đổi logic.

## VERIFY — php -l (4 file)
- FirmContractService.php → No syntax errors detected
- FirmQuotationService.php → No syntax errors detected
- ProductExportRequestsController.php → No syntax errors detected
- ProductExport.php → No syntax errors detected

## Concern
- FIX #3: ép quantity con dùng `(int) $p->child_ratio`. Nếu `child_ratio` là số thập phân (tỉ lệ < 1) thì ép int sẽ sai — nhưng theo code hiện tại `child_ratio` luôn `(int)` cast (cả ở quotation lẫn contract), nên giữ nhất quán. Nếu nghiệp vụ cần tỉ lệ thập phân thì cần đổi kiểu cột.
