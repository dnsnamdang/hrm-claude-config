# Design — Tinh chỉnh UI hàng cha-con (Báo giá & Hợp đồng hãng)

> Bổ sung cho feature `bao-gia-hop-dong-hang-cha-con`. Nhánh: `sync_quotation`.

## Mục tiêu
4 tinh chỉnh hiển thị cụm hàng 2 cấp cha-con trên form **Báo giá hãng** và **Hợp đồng hãng** (FirmQuotation / FirmContract).

## Phạm vi theo yêu cầu (đã chốt)
| # | Yêu cầu | Báo giá hãng | HĐ hãng |
|---|---|---|---|
| 1 | STT con dạng "1.1" | ✅ | ✅ |
| 2 | Tỉ lệ cha = 1 | ✅ | ❌ (không sửa) |
| 3 | Nút "+ con" về cột Tên hàng | ✅ | ❌ (HĐ khóa cụm, không thêm con) |
| 4 | Thành tiền con hiện thật, KHÔNG cộng tổng | ✅ | ✅ |

## Hiện trạng
- Báo giá (`firm/quotations/form.blade.php`): STT = `$index+1` (dòng 428); tỉ lệ cột riêng, cha = "-" (469); nút "+ con" ở **cột Thành tiền** (494-496); thành tiền con hiện `product.total_cost` (thật); tổng `FirmQuotation.total_cost` reduce mọi product (chưa lọc `is_child`); tab "Tổng hợp theo VAT" = `FirmQuotation.vatGroups` (~dòng 98).
- HĐ (`firm/contracts/form.blade.php`): STT = `$index+1`; tỉ lệ dạng text "(tỉ lệ X)" dưới tên (557), KHÔNG có cột; thành tiền con hardcode **"0"** (562); không có nút "+ con".

## Thiết kế chi tiết

### Req 1 — STT "1.1" (cả 2 form)
- Cha / hàng độc lập: số top-level tuần tự `1,2,3…`.
- Con: `<số cha>.<thứ tự con trong cụm>` (1.1, 1.2; cụm 2 → 2.1, 2.2).
- Thay `<% $index + 1 %>` ở cột STT bằng biểu thức tính từ danh sách đã sắp (cha kèm con ngay dưới — thứ tự này đã có ở `formJs` ordering). Cách tính: đếm số cha/độc lập tính đến dòng hiện tại cho số top-level; với con, lấy số cha + thứ tự con trong cụm.
- Dùng helper trên FE (Angular): thêm hàm/getter trả STT hiển thị theo product trong tab (ví dụ `tab.getDisplayIndex(product)`), tránh phụ thuộc `$index` thuần.

### Req 2 — Tỉ lệ cha = 1 (chỉ Báo giá)
- `form.blade.php` dòng 469: `<span ng-if="!product.is_child" class="text-muted">-</span>` → hiển thị **"1"**.

### Req 3 — Nút "+ con" về cột Tên hàng (chỉ Báo giá)
- Bỏ nút "+ con" khỏi cột Thành tiền (494-496).
- Thêm vào cột Tên hàng, sau khối Mã/Model/thuộc tính (sau dòng ~444), điều kiện giữ nguyên: `ng-if="!product.is_child && !form.isShow && !tab.combo_campaign_id"`, `ng-click="openChildPicker(tab, product)"`.

### Req 4 — Thành tiền con hiện thật, không cộng tổng (cả 2 form)
- **Hiển thị dòng con:**
  - Báo giá: giữ `product.total_cost` (đã thật). VAT dòng con (`vat_cost`, `total_cost_after_vat`) hiện như hiện tại.
  - HĐ (562): đổi `<span ng-if="product.is_child">0</span>` → hiển thị thành tiền thật của con (SL con × giá con) — dùng cùng getter total_cost như cha.
- **Loại con khỏi mọi tổng** (thêm điều kiện bỏ `is_child` trong reducer):
  - Tổng báo giá/HĐ: `FirmQuotation.total_cost` (Quotation/FirmQuotation class) + `FirmContract` tương ứng.
  - Tổng **tab hàng hóa** (FirmQuotationTab / FirmContractTab total).
  - **Tab Tổng hợp theo VAT**: `FirmQuotation.vatGroups` (~98) + FirmContract tương ứng — bỏ qua product `is_child` khi gom nhóm VAT.
- Chấp nhận: cộng dồn cột thành tiền tất cả dòng ≠ tổng cuối (đúng chủ đích — chỉ tính cha). Đây là điểm đã ghi trong design gốc mục 3.

## File tác động
- `resources/views/sale/firm/quotations/form.blade.php`
- `resources/views/sale/firm/contracts/form.blade.php`
- `resources/views/partials/classes/sale/firm/quotation/FirmQuotation*.blade.php` (total_cost, tab total, vatGroups)
- `resources/views/partials/classes/sale/firm/contract/FirmContract*.blade.php` (tương ứng)
- (form_show.blade.php của báo giá nếu hiển thị STT/thành tiền con tương tự — đồng bộ hiển thị read-only)

## Không làm
- Bản in (chỉ in cha) — giữ nguyên.
- Logic quỹ xuất cha-con, BE lưu trữ — không đổi (chỉ hiển thị + tổng FE).
- HĐ: req 2 & 3 không áp.

## Rủi ro / lưu ý
- STT "1.1" phải khớp với thứ tự sắp xếp cha-con hiện có (ordering ở `formJs`); dùng đúng danh sách đã sắp.
- Loại `is_child` khỏi tổng phải áp NHẤT QUÁN cả 3 chỗ (tổng chung, tab hàng hóa, tab VAT) + cả form_show để hiển thị đọc khớp.
- Kiểm tra tổng có được lưu/đẩy sang BE không (nếu BE tính lại total khi lưu → cần đảm bảo BE cũng chỉ tính cha; hiện design gốc mục 3 nói tổng chỉ theo cha — xác nhận khi thực thi).
