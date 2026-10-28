# Plan — Căn màn CHI TIẾT Phiếu xuất bán hàng mượn (PXBHM) khớp ERP

URL HRM: `/finance/borrow-sells/{id}` · tab "Thông tin phiếu" · khối "Thông tin chung".
ERP gốc: `warehouse/borrow_sells/show.blade.php` (tab "Thông tin chung").

## Bối cảnh (ảnh user chú thích, cùng phiếu PXBHM-04911)

> "hrm **thiếu** Phiếu xuất mượn, KD chịu vận chuyển / **Thừa** phần loại hợp đồng và chịu phí ship"

Đối chiếu ERP (đọc code, không suy từ UI):
- ERP **CÓ**: "Phiếu xuất mượn" = chips PYCXH (`form.product_export_requests`, link
  `product_export_requests/{id}/show`) — nguồn = `parent.product_export_requests` (phiếu YC cha).
- ERP **CÓ**: checkbox disabled "KD chịu vận chuyển" `ng-checked="form.bear_the_shipping == 1"`.
- ERP **KHÔNG CÓ** field "Loại hợp đồng" (text) và "Chịu phí ship" (text) — HRM tự thêm → gỡ.
- Lưu ý ngữ nghĩa: HRM đang map `bear_the_shipping==1 → "Khách hàng"` là SAI; ERP: `==1` = tích =
  "KD chịu vận chuyển". Thay field text bằng đúng checkbox disabled.

## Việc cần làm — ✅ DONE (2026-10-22)

- [x] BE `BorrowSellDetailResource.php`: thêm `source_export_requests` build từ pivot
      `borrow_sell_request_has_export_requests` where `borrow_sell_request_id = $this->borrow_sell_request_id`
      (mirror `BorrowSellRequestDetailResource::48-56`, đổi khoá sang cột cha). `bear_the_shipping`
      đã có sẵn (L71). `php -l` PASS.
- [x] FE `pages/finance/borrow-sells/_id/index.vue`:
  - [x] Gỡ field "Loại hợp đồng" + computed `contractTypeLabel`.
  - [x] Gỡ field text "Chịu phí ship" + computed `bearShippingLabel`.
  - [x] Thêm field "Phiếu xuất mượn" (chips/link PYCXH) — mirror markup
        `borrow-sell-requests/_id/index.vue:28-45` + computed `sourceExportRequests`.
  - [x] Thêm checkbox disabled "KD chịu vận chuyển" (`:value="!!data.bear_the_shipping"`) —
        pattern `product-arrived-notifies/import/_id.vue:43` (V2BaseCheckbox disabled label).
  - [x] Import + đăng ký `V2BaseCheckbox`.
- [x] Verify Playwright: phiếu 4911 KHÔNG có ở DB local (redirect về list) → test phiếu 4313
      (PXBHM-04313). Kết quả: thiếu/thừa đã sửa, "Phiếu xuất mượn" = link PYCXH-TESTBSR-01,
      checkbox "KD chịu vận chuyển" hiện (disabled), console 0 error.

## Vòng 2 — Khối "Danh sách hàng hoá" (ảnh chú thích 2, 2026-10-22) — ✅ DONE

- [x] Thêm dấu `(*)` ĐỎ vào tiêu đề tab "Hàng hoá" — bám ERP show.blade:197
      (`Hàng hóa <span class="text-danger">(*)</span>`). FE dùng slot `#title` của `<b-tab>`.
      Chỉ tab Hàng hoá, KHÔNG thêm cho tab Nhóm (giống ERP).
- [x] Cắt khoảng trắng lớn dưới bảng ít dòng: global `.table-responsive { min-height: 50vh }`
      (+ `.default-layout`/`.subsystem-page .table-responsive`, default.scss) dành cho bảng DANH SÁCH.
      Dùng tiện ích chung `table-auto-height` (vd warehouse-imports/_id) cho cả 4 `.table-responsive`
      của màn + scoped `.table-responsive.table-auto-height { min-height: 0 }` (selector ghép đè được
      rule layout 2-class). KHÔNG sửa global.
- [x] Verify Playwright 4313: tab "Hàng hoá (*)" đỏ, bảng cao theo nội dung (540px→155px), box tổng
      sát bảng, console 0 error.

## Vòng 3 — Bảng "Danh sách hàng hoá" khớp ERP (ảnh chú thích 3, 2026-10-22)

ERP gốc đọc: `warehouse/borrow_sells/show.blade.php` L208-410 (tab `hang_hoa` + `tab_product`) +
class JS `partials/classes/warehouse/BorrowSellProduct.blade.php` & `BorrowSell.blade.php` (công thức getter).

4 ý user:
1. **Thừa nguồn phiếu** — gỡ `<ul class="src-list">` "Nguồn phiếu mượn …" dưới tên hàng (ERP KHÔNG để
   dưới tên hàng, mà là cột "Chi tiết" = Phiếu mượn/Bán dạng dòng con).
2. **Chia cột 2 cấp** — header 2 tầng: nhóm "Số lượng" (Hợp đồng/Đã xuất kho/Bán hàng mượn) +
   nhóm "Chi tiết" (Phiếu mượn/Bán), dòng con mỗi `details` (rowspan như ERP).
3. **Thêm đủ cột như ERP** — tab Hàng hoá: STT, Tên hàng, ĐVT, [SL: HĐ/ĐãXK/BánHM], [CT: Phiếu mượn/Bán],
   Giá niêm yết(price), Đơn giá bán(price_after_extra), Thành tiền(total_amount_after_extra),
   [Chiết khấu(rebate_price) chỉ khi has_rebate_price], Đơn giá sau giảm(allocated_price),
   Thành tiền sau giảm(total_amount_allocated), VAT(vat_percent), Thành tiền sau VAT(total_amount_allocated_after_vat).
   Tab Nhóm cũng sửa đồng bộ: STT, Tên, ĐVT, Giá niêm yết, Giảm giá(discount_price), Đơn giá bán,
   [SL], [CT] — gỡ src-list.
4. **Tổng tiền chỉ các giá trị như ERP** — pay-box tab Hàng hoá: Tổng tiền bán(ΣtotalAfterExtra),
   (Tổng giảm giá=sale_invoice nếu >0 & !has_rebate), Tổng tiền trước thuế(Σtotal_amount_allocated),
   Tiền VAT(Σ vat theo allocated), Tổng tiền sau thuế(Σtotal_amount_allocated_after_vat),
   (Giảm giá/Chiết khấu khi has_rebate). Bỏ các dòng "sau phụ thu" + "phân bổ" cũ.

### Việc
- [x] BE `BorrowSellDetailResource.php`: thêm field dòng hàng CHÍNH `exported_qty`, `borrow_sell_qty`,
      `price_after_extra`, `total_amount_after_extra`, `total_amount_allocated`,
      `total_amount_allocated_after_vat`; + helper `buildMainExportedQtyMap()` (firm=Σ tab products theo
      product_id|unit_id; khác=objectable.exported_qty theo bảng map). Root tổng recompute LIVE như ERP
      getter: `total_sell/total_before_vat/total_vat/total_after_vat/sale_invoice/rebate_total`.
      (`vat_cost_allocated` DB = 0 vì ERP submit không set → KHÔNG dùng; dùng Σ live.) `php -l` PASS.
- [x] FE `pages/finance/borrow-sells/_id/index.vue` tab Hàng hoá: header 2 tầng (Số lượng{HĐ/ĐãXK/BánHM}
      + Chi tiết{Phiếu mượn/Bán}) + dòng con Chi tiết (rowspan `rowspanOf`), gỡ src-list, đủ cột
      (Giá niêm yết/Đơn giá bán/Thành tiền/[Chiết khấu khi has_rebate]/Đơn giá sau giảm/Thành tiền sau
      giảm/VAT/Thành tiền sau VAT), pay-box theo ERP (total_sell + sale_invoice/rebate_total theo cờ).
- [x] FE tab Nhóm: header 2 tầng + dòng con Chi tiết, gỡ src-list, cột như ERP tab_product
      (STT/Tên/ĐVT/Giá niêm yết/Giảm giá/Đơn giá bán/[SL]/[CT]).
- [x] Gỡ method `rowTotal` (không dùng) → thêm `rowspanOf`; xoá CSS `.src-list`.
- [x] Verify Playwright: 4313 (HĐ dịch vụ) — tab Hàng hoá 2 tầng, dòng con Phiếu mượn PYCXH-TESTBSR-01
      + Bán=1, pay-box = Tổng tiền bán/Tổng tiền trước thuế/Tiền VAT/Tổng tiền sau thuế (đúng ERP);
      + phiếu 1 (PXBHM-00001, HĐ hãng PINACO) — tab Nhóm 2 tầng + dòng con PYCXH-00080 + Bán=24/20,
      không src-list, 0 console error ở cả 2 phiếu.

## Vòng 4 — Bố cục tab + tiêu đề khối (ảnh chú thích 4-5, 2026-10-22)

ERP gốc `show.blade.php` L16-34: dòng người tạo (`form.creator - form.created_time`) nằm ở
`card-header d-flex > .ml-auto` **trên cùng, canh phải, trên dải tab**; tab đầu tên thẳng là
"Thông tin chung" (không có tiêu đề khối con bên trong); tab Hạch toán chỉ có bảng, KHÔNG tiêu đề.

- [x] **Ý 4** — Bỏ tiêu đề khối "Bút toán hạch toán" ở tab Hạch toán (ERP không có): thay
      `<V2BaseFormCard title="Bút toán hạch toán">` bằng `.v2-form-card.form-card > .form-card-body`
      (giữ khung trắng, bỏ thanh tiêu đề).
- [x] **Ý 5** — Bỏ tiêu đề khối "Thông tin chung" (trùng tên tab "Thông tin phiếu") + đẩy dòng người
      tạo lên NGANG dải tab, canh phải: dùng slot `#tabs-end` của `<b-tabs>` ngoài, `<li class="ml-auto
      v2-tabs-creator">` chứa `CreatorInfoLine`; khối thông tin chung đổi sang `.v2-form-card >
      .form-card-body` (không header bar). KHÔNG sửa component dùng chung V2BaseFormCard/CreatorInfoLine.
- [x] Verify Playwright 4313 — dải tab = [Thông tin phiếu | Hạch toán | (canh phải) "DNS Admin -
      07/09/2026 15:21"]; khối Thông tin chung KHÔNG còn header bar (hasHead=false) vẫn đủ 14 field +
      Mã phiếu PXBHM-04313; không còn `.form-card-title` "Thông tin chung"/"Bút toán hạch toán"; 0 console error.

## Ghi chú
- Chỉ sửa màn CHI TIẾT PXBHM (borrow-sells), không đụng borrow-sell-requests (Phase 1 đã OK).
- Branch: develop (cả 2 repo). KHÔNG commit/push khi user chưa yêu cầu.
