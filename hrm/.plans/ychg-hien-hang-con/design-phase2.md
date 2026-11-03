# Design Phase 2 — Con hàng tạm sửa được (YCHG)

## Quy tắc nghiệp vụ (user chốt 2026-10-30)
1. **Chỉ hỏi giá cấp CHA.** Mọi hàng con (ERP lẫn hàng tạm) KHÔNG vào `product_ids`, KHÔNG được hỏi giá.
2. Con hàng **ERP**: chỉ show (Phase 1 — xong).
3. Con hàng **tạm**: show dưới cha + nút **Sửa** để nhập đủ thông tin cho hàng tạm con; con vẫn không hỏi giá.
4. **Chặn gửi duyệt**: còn hàng tạm con chưa đủ thông tin → phiếu KHÔNG gửi được + thông báo rõ.

## Dữ kiện mô hình (đã khảo sát)
- Hàng tạm = `products` + `product_company_coefficients.status = 6`; không cha–con nội tại.
- Con tái sử dụng = cây `bom_list_products.parent_id` / `quotation_product_prices.parent_id`, lấy qua `GET assign/product-projects/reuse-children`. Con có thể đã gắn `erp_product_id` (đã là product/hàng tạm) hoặc chưa (`null`).
- `recipe_products(base_product_id→product_id, qty, is_main, unit_id)` = cấu trúc combo/định mức. Phase 1 đã đọc bảng này để show con ERP chỉ-đọc. Hàng tạm tạo từ YCHG hiện KHÔNG sinh `recipe_products` (không gửi `recipes`).
- YCHG writer (`PriceAskingRequestWriter::save`) chỉ đọc `note` + `product_ids` (phẳng, unique, intval). `price_asking_request_products` KHÔNG có `parent_id`.
- "Đủ thông tin" hàng tạm (required `ProductRequest::commonRules` + `TempProductRequest`): `name, model_id, brand_id, manufacture_id, origin_id, product_type_id` (+ đủ cây Loại SP), `vat_percent_tax_rate_id`, ≥1 `unit` (unit_id/is_base/coefficient). FE hằng `YCHG_REQUIRED` khớp đúng.

## Quyết định thiết kế (đề xuất — CHỜ user duyệt)

### QĐ-P2-1: Lưu con tạm = bản ghi hàng tạm riêng, link cha qua `recipe_products`
- Khi thêm 1 hàng tạm (cha) CÓ con từ nguồn tái sử dụng:
  - Tạo hàng tạm **cha** (status 6) → vào `product_ids` (được hỏi giá) — như hiện tại.
  - Mỗi **con**: tạo 1 hàng tạm (status 6) từ dữ liệu con của `reuse-children`, rồi ghi `recipe_products(base_product_id = cha, product_id = con, qty, unit_id, is_main=0)`. Con **KHÔNG** vào `product_ids`.
- Lợi: tái dùng đúng bảng Phase 1 đang đọc; con là product thật nên sửa được qua `master-data/temp-products/{id}` và kiểm "đủ thông tin" bằng required fields sẵn có; không cần thêm cột `parent_id` vào bảng phiếu.
- Con đã có `erp_product_id` (đã là product/hàng tạm) → link thẳng id đó, không tạo trùng.

### QĐ-P2-2: Reader mở rộng — con tạm cũng trả về, kèm cờ sửa/đủ
- `PriceAskingProductReader`: bỏ điều kiện loại trừ temp ở `recipe_children`; với CHA là hàng tạm, trả con kèm thêm: `product_id`, `is_temp=true`, `is_complete` (đủ required?), `editable=true`. CHA là hàng ERP giữ nguyên con chỉ-đọc (`is_temp=false, editable=false`).
- `is_complete` = kiểm các cột required của hàng tạm con trên `products` (+ ≥1 `product_units`).

### QĐ-P2-3: FE — dòng con tạm có nút Sửa + cờ thiếu
- `PriceAskingRequestForm.vue`: dòng con khi `editable` → thêm nút **Sửa** (mở `openTempEdit(child.product_id)` sẵn có). Con thiếu thông tin → chip xám-cảnh báo "Thiếu thông tin" (KHÔNG đỏ, đỏ chỉ cho lỗi validate). Con ERP giữ chỉ-đọc.
- Nút **Lưu và gửi duyệt**: nếu còn con tạm `is_complete=false` → chặn client + `$confirm`/thông báo liệt kê con thiếu; KHÔNG gọi API gửi.

### QĐ-P2-4: BE chặn gửi (defense-in-depth)
- `PriceAskingRequestWriter::save` khi `send=true`: với mỗi hàng tạm (status 6) trong `product_ids`, lấy con qua `recipe_products` → kiểm mọi con tạm đủ required; thiếu → ném `ValidationException` (422) message nghiệp vụ liệt kê con thiếu. Không dựa vào FE ẩn.

### QĐ-P2-5: Shared component `QuotationProductSearchModal.vue` (ĐỤNG HÀM DÙNG CHUNG — cần duyệt)
- Luồng YCHG tái sử dụng hiện chỉ tạo 1 hàng tạm phẳng. Cần mở rộng: khi dòng nguồn có con (`reuse-children` trả về), sau khi tạo/sửa cha thì tạo kèm con + link `recipe_products`.
- Cách làm an toàn (không ảnh hưởng BOM/Báo giá): thêm nhánh RIÊNG trong `saveTemp`/`useReuseRow` chỉ chạy khi `isYchg`, tận dụng `fetchReuseChildren()` sẵn có; nhánh `addSelectedReuse` (BOM/Báo giá) giữ nguyên.
- Hoặc dời việc tạo con sang BE: FE chỉ gửi `source {type,id}` (đã có trong `buildTempPayload`), BE `TempProductService` khi tạo hàng tạm từ YCHG tự đọc `reuse-children` của source và tạo con + link. → **ít đụng FE dùng chung hơn, gom logic 1 chỗ BE**. (Đề xuất chọn hướng này.)

## Quyết định user chốt 2026-10-30
- **A = BE tự tạo con.** FE gửi `source {type,id}` (đã có trong `buildTempPayload`). `TempProductService` khi tạo hàng tạm cha từ YCHG tự đọc con của source → tạo hàng tạm con + link `recipe_products`. → **KHÔNG phải sửa `QuotationProductSearchModal` dùng chung** (chỉ dùng lại `source` sẵn gửi). Cần xác minh `source.id` = id dòng cha (bom_list_products/quotation_product_prices) mà `reuse-children` nhận.
- **B = chỉ 1 cấp con trực tiếp.** Bỏ qua cấp sâu hơn.

→ Chốt QĐ-P2-5 theo hướng A: gom ở BE, không thêm nhánh FE trong modal.

## Vướng mắc DB phát hiện khi code (2026-10-30) + cách giải — CHỐT
Khi hiện thực hướng A (BE tự tạo con) lộ ràng buộc dữ liệu:
- `products.manufacture_id` **NOT NULL** (cùng `code, name, brand_id, origin_id`). `product_type_id, model_id, vat_percent_tax_rate_id` NULLABLE.
- `bom_list_products` / `quotation_product_prices` **KHÔNG có cột** `manufacture_id`, `product_type_id`, `vat_percent_tax_rate_id`. Con chỉ có `brand_id, model_id, origin_id, unit_id, qty_needed, name, code, erp_product_id, vat_percent`.
- `ProductWriteService::store` → `generateCode()` cần `manufacture_id` HOẶC `model_id` để sinh mã (có model là sinh được).

Dữ liệu thật: con BOM 48/57 đã có `erp_product_id`, 9 con THÔ chưa; con báo giá 311/311 đã có. 9 con thô đều có đủ name/brand/model/origin/unit, chỉ thiếu manufacture + loại SP + VAT.

**Cách giải (CHỐT, trung thành yêu cầu):**
- Con đã có `erp_product_id` → **CHỈ link** `recipe_products(base=cha, product=erp_product_id, qty, unit_id, is_main=0)`, KHÔNG tạo mới.
- Con THÔ (`erp_product_id IS NULL`) → tạo 1 hàng tạm (status 6) qua `ProductWriteService::store`, truyền `manufacture_id = manufacture_id CỦA CHA` làm **placeholder bắt buộc để INSERT** (không có nguồn manufacture nào khác cho con). Sau tạo: set `erp_product_id` của dòng nguồn = id con (như `linkSourceLines`, chống tạo trùng lần sau) + ghi `recipe_products`.
- **An toàn placeholder**: con thô luôn thiếu `product_type_id` + `vat_percent_tax_rate_id` ⇒ `is_complete=false` ⇒ **chặn gửi** (QĐ-P2-4) ⇒ user BẮT BUỘC mở Sửa và rà lại mọi field, trong đó có Hãng SX kế thừa. Manufacture kế thừa KHÔNG bao giờ đi thẳng vào phiếu gửi mà chưa qua mắt user.

**Lệch plan Task 4**: KHÔNG tách logic từ `ProductProjectController@reuseChildren` (nó load nhiều quan hệ cho FE hiển thị). Thay bằng query gọn TRỰC TIẾP bảng nguồn lấy đúng cột cần tạo — ít rủi ro, không đụng module Assign, và vì con chỉ hiện SAU khi lưu (qua reader), không có preview FE nào phải khớp.

## Checkpoint
Đã duyệt hướng A + B. Vướng manufacture_id NOT NULL đã giải bằng kế thừa-từ-cha + chặn-gửi ép rà soát. Bắt đầu code.

---

# Item 4 — Bổ sung 2 cột hiển thị nguồn gốc & trạng thái giá (THUẦN HIỂN THỊ)

## Yêu cầu
Thêm 2 cột vào bảng "Hàng hoá hỏi giá" (`/sale/price-asking-requests/add`):
1. **Nguồn gốc hàng tạm**: "Từ Báo giá - <trạng thái: Trúng thầu/Chờ phê duyệt>: BG-xxxxxx" HOẶC "Từ BOM dự án".
2. **Trạng thái dữ liệu giá** (badge): "Đã có sẵn giá từ BG" (xanh #16A34A — CHỈ khi báo giá **Trúng thầu** AND có giá > 0) HOẶC "Hàng tạm mới - Cần tính giá" (cam #D97706).

## User chốt (AskUserQuestion, trước compaction)
- **Phạm vi = Thuần hiển thị**: KHÔNG mang giá từ BG vào phiếu; chỉ hiển thị nhãn + badge.
- **"Lập từ" = Thay bằng cột mới**: bỏ dòng ghi chú `temp-from-note` cũ, thay bằng 2 cột mới.
- **Dòng con = Chỉ dòng cha**: con (ERP lẫn tạm) để trống 2 cột mới; dòng hàng ERP (đang kinh doanh) cũng để trống.
- Giữ nguyên thứ tự ưu tiên BOM-trước-rồi-Báo-giá.

## Logic badge (BE quyết text + màu, FE chỉ hiển thị)
- `won = quotation.status === Quotation::STATUS_TRUNG_THAU (7)`
- `hasPrice = won && quoted_price > 0`
- BOM → luôn "Từ BOM dự án" + badge cam (NEW, chưa có giá).
- Báo giá: source_text "Từ Báo giá - " + (won ? "Trúng thầu" : "Chờ phê duyệt") + ": " + doc_code; badge = hasPrice ? xanh "Đã có sẵn giá từ BG" : cam "Hàng tạm mới - Cần tính giá".

## Hiện thực
- BE `PriceAskingProductReader.php`: import `Quotation`; 4 hằng text/màu; `tempSources()` trả `[id => [temp_from, source_text, source_tooltip, price_text, price_color]]` (BOM trước, báo giá phần còn lại); `enrich()` emit `temp_source_text/_tooltip`, `price_data_text/_color`, giữ `temp_from` cũ (shape không đổi).
- BE `PriceAskingRequestService.php` `lineRow()` (đường show/detail): emit 4 field mới chỉ khi `is_temp`.
- FE `PriceAskingRequestForm.vue`: +2 `<th>`; bỏ block `temp-from-note`; dòng CHA +2 `<td>` (span text title=tooltip + `V2BaseBadge :color`); dòng con +2 `<td></td>` trống; `colCount` 7/8 → 9/10; CSS `.temp-source-cell`.

## Verify (2026-11-02)
- **php -l** pass cả 2 file BE. **Zero-regression**: git-stash 2 file BE, chạy `TempProductApiTest` → 6 fail/11 pass GIỐNG HỆT khi có thay đổi ⇒ 6 fail là do bảng `inherited_price_factors` thiếu local (code path khác), không phải từ thay đổi này.
- **Reflection trên data dev thật**: pid 8310 (quotation Trúng thầu status7, giá>0) → "Từ Báo giá - Trúng thầu: BG-2026-00001" + xanh #16A34A "Đã có sẵn giá từ BG"; pid 30370 (status2) → cam "Chờ phê duyệt"; pid 31913 (BOM) → "Từ BOM dự án" + cam.
- **Playwright live** (DNS Admin, cty 1, `/add`): chọn BT3D-CH-CUONDAYHOI (hàng tạm, báo giá status 4) + CH-MN-H-CUONDAYHOI (đang kinh doanh). Kết quả đúng:
  - Hàng tạm: "Từ Báo giá - Chờ phê duyệt: BG-2026-00075" + badge CAM "Hàng tạm mới - Cần tính giá".
  - Hàng ERP đang kinh doanh: 2 cột mới TRỐNG.
  - Nhánh xanh "Trúng thầu + Đã có sẵn giá" không hiện được live (3 hàng tạm local đều link báo giá status 4) — đã chứng minh qua reflection.

## Setup phụ (không phải test data)
- Chạy migration `2026_10_29_000002_create_inherited_price_factors_table.php` trên `erp_hrm_check` local để app không 500 (bảng module chưa migrate local). Là setup hợp lệ, không phải dữ liệu test.

## Trạng thái: XONG hiện thực + verify. CHƯA commit/push (chờ user yêu cầu).
