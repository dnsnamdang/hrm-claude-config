# Plan — Đơn giá có VAT tách theo khách hàng (Đơn mua hàng)

@khoipv — 2026-09-10

## Chốt với user
- Cấp tách giá: **theo KHÁCH HÀNG** (không phải theo HĐ bán, không phải theo từng phiếu ĐX)
- Hiển thị: **nhiều ô nhập trong 1 dòng** (giữ gộp theo mã hàng), thẳng hàng với cột Mục đích mua
- User: "bạn cứ làm đi sai tôi sửa sau" → được phép sửa `SupplyReportService` (hàm dùng chung) để bổ sung `customer_id`

## Phase 1 — BE

- [x] 1. `SupplyReportService::purchaseDemand()` — thêm `customer_id` vào `lines[]` (query đã select `sh.customer_id`, chỉ chưa đẩy xuống). Thuần bổ sung field, không đổi field cũ.
- [x] 2. `PurchaseOrderService::calcTotalAmount()` — tính theo `Σ(purposes[].buyQty × purposes[].price)`, fallback `price × order_qty` khi dòng không có purposes.
- [x] 3. `PurchaseOrderService::syncProducts()` — `amount` theo công thức mới; `price` ghi = **bình quân gia quyền** `round(Σ(buyQty×price)/Σ buyQty)` để danh sách/`total_amount` không vỡ.
- [x] 4. `StorePurchaseOrderRequest` — `withValidator` bắt mỗi khách phải có giá > 0, gắn lỗi vào key `products.<idx>.price` để FE hiện đúng ô.

## Phase 2 — FE

- [x] 5. `GoodsPickerModal.vue` — purpose thêm `customer_id` + `price: 0`.
- [x] 6. `ProductsTab.vue` — thêm `customersOf(p)` (khách distinct từ purposes, khuôn giống `contractsOf`).
- [x] 7. `ProductsTab.vue` — cột "Đơn giá có VAT" render `v-for` theo `customersOf(p)`; ≥2 khách thì hiện nhãn tên khách; dòng mua ngoài phiếu (không khách) giữ 1 ô như cũ.
- [x] 8. `ProductsTab.vue` — `onPriceInput` ghi giá vào **mọi** purpose cùng khách; `amountOf()` = `Σ(buyQty × price)`.
- [x] 9. `PurchaseOrderForm.vue` — `totalAmount` dùng chung công thức mới.
- [x] 10. Tương thích đơn cũ: purposes chưa có `price` → fallback `p.price`. Không backfill data.

## Phase 3 — Verify

- [x] 11. `php -l` các file BE; `vue-template-compiler` + `node --check` các file FE
- [x] 12. Test tính tiền: 1 khách / 2 khách / dòng không phiếu / đơn cũ đã lưu

## Rủi ro đã biết
- Cột "Đơn giá báo giá" tham chiếu tách theo **HĐ bán**, ô nhập tách theo **khách hàng** → 1 khách nhiều HĐ sẽ lệch số dòng giữa 2 cột. Đã báo user, chấp nhận.

## Phát sinh ngoài plan

- [x] 13. `pages/supply/reports/purchase-demand/index.vue` — `buildOrderLine()` cũng dựng `purposes` (đường đi thật của user: Báo cáo nhu cầu mua → Lập đơn mua hàng), phải thêm `customer_id` + `price` y như `GoodsPickerModal`. Sót file này thì đơn seed từ báo cáo sẽ không tách được giá.
- [x] 14. Quy tắc **0-1 khách giữ công thức cũ `price × order_qty`** (chỉ từ 2 khách trở lên mới cộng theo `Σ buyQty × price`). Lý do: ô "SL mua" cấp dòng vẫn sửa tay được và có thể khác `Σ buyQty`; nếu luôn dùng `Σ buyQty × price` thì sửa tay SL mua sẽ bị bỏ qua. Quy tắc này nhân bản ở 3 nơi và đã test khớp số: `ProductsTab::amountOf`, `PurchaseOrderForm::lineAmount`, `PurchaseOrderService::lineTotals`.

## Phase 4 — Gom dòng cùng khách hàng (yêu cầu 2026-09-10)

- [x] 15. `ProductsTab::purposesOf()` — sắp xếp các dòng phiếu đề xuất theo **thứ tự khách hàng xuất hiện** (khớp `customersOf`), giữ nguyên thứ tự gốc trong cùng 1 khách. Chỉ đổi thứ tự HIỂN THỊ, không đụng mảng `p.purposes` để payload BE và các ô nhập không bị ảnh hưởng.
- [x] 16. Thêm gạch phân cách giữa 2 nhóm khách trong cột "Mục đích mua" (`isCustomerStart` + class `pp-cusgap`) để nhìn thấy ranh giới nhóm.
- [x] 17. Verify: compile template + `node --check` + test `purposesOf` với mã `315-448` (4 phiếu / 3 khách, dòng khách id 2 đang bị tách rời).

## Kết quả verify

- `php -l` sạch 3 file BE; `vue-template-compiler` + `node --check` + `node-sass` sạch 4 file FE; tất cả file giữ **CRLF**
- **BE `lineTotals` 6/6 PASS** (chạy thật qua Reflection): 1 khách 2 phiếu · 2 khách khác giá · mua ngoài phiếu · đơn cũ chưa có price · 2 khách đơn cũ · 1 khách sửa tay SL mua
- **FE `amountOf` + `lineAmount` 7/7 PASS** — 6 case trên ra **đúng cùng con số** với BE, cộng 1 case ghi giá: nhập giá cho khách B → ghi vào **cả 2 phiếu** của B, không đụng phiếu của A, `p.price` = bình quân gia quyền 125.625
- **Validate**: thiếu giá 1 khách → lỗi gắn đúng key `products.0.price` với message "Vui lòng nhập đơn giá cho khách hàng BV B."
- **API báo cáo** trả `customer_id` thật: mã `315-448` có 4 phiếu / **3 khách** (id 2 ×2, 3217, 3219), mã `XSYS0061` có 2 khách (3216, 3219)

## Phase 5 — Tách hẳn thành dòng riêng theo khách hàng (yêu cầu 2026-09-10)

- [x] 18. `ProductsTab.vue` — 1 hàng hóa cắt thành **N dòng `<tr>`**, mỗi khách hàng 1 dòng. 18/20 cột chung dùng `rowspan` (STT, mã, tên, quy cách, ĐVT, nước SX, SL đề xuất, SL mua, thành tiền, 4 cột tham chiếu, cty bán/mua, ngày cần, ghi chú, xóa); chỉ 2 cột đổi theo dòng con: **Mục đích mua** và **Đơn giá có VAT**. Nhờ vậy đường kẻ của bảng chạy **thẳng qua các cột**, không còn gạch đứt trong ô.
- [x] 19. Thêm `rowGroupsOf(p)` (gom purposes theo khách, luôn trả ≥ 1 nhóm) + `visibleRows` gắn sẵn `groups`; bỏ `isCustomerStart` / `.pp-cusgap` / `.price-line` / `.price-hd` (không còn dùng vì mỗi khách đã là 1 dòng và tên khách đã có trong cột Mục đích mua).
- [x] 20. `tr.grp-sub > td` tô nền nhạt cho dòng con thứ 2 trở đi.

- [x] 21. Cột **Cty thực hiện bán** cũng tách theo dòng con (bỏ `rowspan`): thêm `saleCompanyOfPurposes(list)`, `saleCompanyOf(p)` gọi lại helper này. Còn 17 cột `rowspan`, 3 cột đổi theo khách: Mục đích mua · Đơn giá có VAT · Cty thực hiện bán.

- [x] 22. Cột **Cty thực hiện mua** và **Ghi chú** cũng tách theo dòng con. Giá trị lưu trong `purposes[].buyer_company_id` / `purposes[].note` (cột JSON — không cần migration); cột `buyer_company_id` / `note` cấp dòng vẫn được đồng bộ (`syncRowBuyer` lấy giá trị phiếu đầu tiên, `syncRowNote` nối các ghi chú khác nhau bằng " | ") để BE validate và các màn cũ đọc được như trước. Còn **15 cột `rowspan`**, **5 cột đổi theo khách**: Mục đích mua · Đơn giá có VAT · Cty thực hiện bán · Cty thực hiện mua · Ghi chú.
- [x] 23. `fillPurposeField(p, field, base)` — chốt giá trị đang hiển thị của các khách khác TRƯỚC khi ghi, nếu không giá trị của họ sẽ trôi theo giá trị cấp dòng vừa bị đồng bộ lại. Lỗi này đã gặp khi test (sửa cty mua của BV B làm BV A đổi theo) và đã sửa.
- [x] 24. `StorePurchaseOrderRequest` — viết lại khối validate: gom phiếu theo khách rồi soát **giá trị hiệu lực** của từng khách (giá trị trong `purposes[]`, không có thì lấy giá trị cấp dòng — đúng như FE hiển thị), soát cả đơn giá lẫn cty thực hiện mua. Cách này đồng thời sửa lỗi tiềm ẩn của Phase 1-3: đơn cũ có `purposes[]` chưa có `price` sẽ bị báo thiếu giá oan khi lưu lại.

- [x] 25. **Ghi chú tách theo HỢP ĐỒNG BÁN**, không phải theo khách: cùng 1 khách vẫn có thể có 2 HĐ. Dòng con giờ là cặp **khách × hợp đồng** (`withContractSubs` + `contractKey`, khóa theo `contract_id`, không có thì `contract_code`, không có nữa thì `#nc`). Cột **Mục đích mua** và **Ghi chú** đổi theo từng HĐ; **Đơn giá**, **Cty thực hiện bán**, **Cty thực hiện mua** vẫn gộp theo khách bằng `rowspan="g.subs.length"`; 15 cột chung dùng `rowspan="row.subCount"`. Tổng 15 + 3 + 2 = 20 cột.
- [x] 26. Validate BE giữ nguyên (đơn giá + cty mua vẫn soát theo khách — đúng cấp). Ghi chú không cần validate.

## Phase 7 — Tổng hợp tiền theo công ty thực hiện mua

- [x] 28. Thêm khối **"Tổng tiền theo công ty thực hiện mua"** ngay dưới bảng hàng hóa (`ProductsTab.vue`). Vì cty thực hiện mua tách theo KHÁCH HÀNG (Phase 5) nên tiền phải cộng theo **từng dòng con**, không phải theo cả dòng hàng hóa: dòng từ 2 khách trở lên → `amountOfGroup(p, g)` = Σ `buyQty × priceOfPurpose`; dòng 0-1 khách → dùng luôn `amountOf(p)` (giữ hiệu lực của ô "SL mua" sửa tay) → **tổng các cty luôn khớp TỔNG CỘNG của bảng**.
- [x] 29. Dòng chưa chọn cty mua gom vào nhóm **"Chưa chọn công ty thực hiện mua"** (chữ đỏ, xếp cuối); các cty còn lại xếp theo tiền giảm dần. `companyName(id)` hiện "MÃ — Tên"; id không có trong danh sách công ty thì hiện "Công ty #id" thay vì để trống.

- [x] 30. Bỏ dạng bảng (user không muốn thêm 1 bảng nữa dưới bảng hàng hóa) → gộp thành **1 dòng gọn** ngay dưới bảng: nhãn + các chip "Tên cty **số tiền**", chip "Chưa chọn công ty" tô đỏ. Không lặp lại TỔNG CỘNG vì bảng đã có sẵn. Cách tính không đổi.

- [x] 31. Giữ **dạng cột** (mã cty bên trái, tiền căn phải thẳng hàng, có dòng TỔNG CỘNG) nhưng dựng bằng `flex` chứ không dùng `<table>`. Cột công ty chỉ hiện **MÃ** (`companyCode`) cho gọn, đồng bộ với cột "Cty thực hiện mua" trong bảng; tên đầy đủ đưa vào tooltip (`companyFullName`).

- [x] 32. Đẩy khối tổng hợp sang **mép phải** (`margin-left: auto`) cho thẳng hàng với cột "Thành tiền" của bảng.

### Kết quả verify Phase 7

- Template compile sạch, script parse sạch, SCSS sạch (6.816 bytes), file vẫn **CRLF**
- Test `buyerTotals` 5 ca, **tổng các cty = `totalAmount` ở cả 5 ca**: 2 khách/2 cty mua (AP 50.000 · TA 15.000) · mua ngoài phiếu + dòng chưa chọn cty (TA 21.000 · Chưa chọn 3.000) · đơn cũ (purposes chưa có giá/cty → fallback cấp dòng) · cty không có trong options → "Công ty #99" · bảng rỗng → không hiện khối

## Phase 6 — Popup xác nhận khi xóa hàng hóa

- [x] 27. `ProductsTab::removeRow` đang dùng `confirm()` mặc định của trình duyệt (hộp thoại xám của Chrome). Đổi sang `this.$bvModal.msgBoxConfirm` — đúng chuẩn các màn khác trong module Cung ứng (`purchase_orders/index.vue`, `supply_proposals/index.vue`, `TncnTaxConfigSection.vue`): title `Xác nhận`, okTitle `Xóa`, cancelTitle `Hủy`. Kèm luôn tên hàng hóa vào câu hỏi cho dễ đối chiếu; dòng chưa có tên thì hiện “hàng hóa này”. `msgBoxConfirm` trả Promise nên phần `splice` chuyển vào `.then`.

### Kết quả verify Phase 6

- Template compile sạch, script parse sạch, SCSS sạch (6.126 bytes), file vẫn **CRLF**; không còn `confirm()` native trong file
- Test `removeRow` với `$bvModal` giả: bấm **Xóa** → đúng 1 dòng bị xóa (còn lại "Hàng B") · bấm **Hủy** → mảng giữ nguyên 2 dòng
- Câu hỏi hiện đúng: `Bạn có chắc muốn xóa hàng hóa "Hàng A" khỏi đơn mua hàng?`; dòng không có tên → `...xóa hàng hóa này khỏi...`

### Kết quả verify Phase 5

- Template + SCSS + `node --check` sạch; file vẫn **CRLF**; số `<th>` = 20 = số `<td>` dòng đầu = `colspan` 20
- Test ghi chú theo HĐ: 1 khách (BV A) 2 HĐ + 1 khách (BV B) 1 HĐ / 4 phiếu → **3 dòng con**; HĐ 11 gộp P1+P4, HĐ 22 có P3, ô đơn giá của BV A gộp 2 dòng; sửa ghi chú riêng từng HĐ → ghi đúng vào các phiếu của HĐ đó, không đụng HĐ kia
- Ca biên: 1 khách 2 HĐ → 2 dòng · mua ngoài phiếu → 1 dòng (`#one` / `#none`) · phiếu không có HĐ → 1 dòng khóa `#nc`
- Test cty mua / ghi chú theo dòng (3 phiếu / 2 khách): đơn cũ → cả 2 dòng fallback về giá trị cấp dòng · sửa riêng dòng BV B → BV A **giữ nguyên** · sửa tiếp BV A → 2 dòng độc lập, `purposes[]` mang đúng giá trị từng khách, cấp dòng = `buyer` phiếu đầu + `note` nối " | " · mua ngoài phiếu → ghi thẳng vào cấp dòng
- Validate BE **6/6 PASS**: đủ giá + đủ cty mua → không lỗi · thiếu giá khách B → `products.0.price` · thiếu cty mua khách B → `products.0.buyer_company_id` · **đơn cũ (purposes chưa có giá/cty, cấp dòng có) → không lỗi** · khách SL=0 thiếu hết → bỏ qua · mua ngoài phiếu → không lỗi
- Test cty bán theo dòng: 3 phiếu / 2 khách, BV A (2 phiếu) → "CT TNHH An Phat", BV B → "CT CP Thanh An"; mua ngoài phiếu → rỗng (hiện `—`)
- Test `rowGroupsOf` 4 ca: 3 khách/4 phiếu → **3 dòng** (BV A gộp 2 phiếu) · 1 khách 2 phiếu → **1 dòng** · mua ngoài phiếu → **1 dòng** (ô nhập giá thường) · 2 khách + 1 phiếu không rõ khách → **3 dòng**, phiếu không rõ khách nằm dòng cuối, không có ô nhập giá

## Kết quả verify Phase 4

- Template compile sạch, `node --check` sạch, `node-sass` sạch (6.560 bytes), file vẫn **CRLF**
- Test `purposesOf` với ca thật mã `315-448` (PDX-01/BV A, PDX-02/BV B, PDX-03/BV A, PDX-04/BV C): ra **PDX-01 · PDX-03 · PDX-02 · PDX-04** — 2 phiếu của BV A đã nằm cạnh nhau, gạch phân cách ở dòng 2 và 3, thứ tự khách khớp `customersOf` (BV A | BV B | BV C)
- **Mảng gốc `p.purposes` không đổi** → payload gửi BE và các ô nhập SL/giá không bị ảnh hưởng
- Ca biên: 0 phiếu / 1 phiếu trả về nguyên trạng; dòng thiếu tên khách vẫn được gom chung một cụm
- **1 khách = 1 ô nhập giá** (yêu cầu bổ sung): `customersOf()` khử trùng theo `customerKey` nên mỗi khách chỉ sinh 1 ô; `onCustomerPriceInput()` ghi giá đó vào **mọi** phiếu của khách — đã có sẵn từ Phase 1-3, không phải sửa thêm

### Checkpoint — 2026-09-10
Vừa hoàn thành: toàn bộ Phase 1-3 + 2 việc phát sinh
Đang làm dở: (không)
Bước tiếp theo: @khoipv build lại client + hard refresh, test tay trên trình duyệt
Blocked: (không)
