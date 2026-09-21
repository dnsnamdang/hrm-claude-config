# Hợp đồng mua (build thật) — Plan

@namdangit — 2026-07-20

Plan chi tiết (code mẫu + verify từng bước): `docs/superpowers/plans/2026-07-20-hop-dong-mua.md`
Spec: `docs/superpowers/specs/2026-07-20-hop-dong-mua-design.md`

## Cách thực thi: subagent-driven (mỗi task 1 subagent + review)

## Phase 1 — BE data layer
- [ ] Task 1: Migrations 4 bảng (purchase_contracts + products + payment_terms + progress)
- [ ] Task 2: Entities 4 (PurchaseContract + Product + PaymentTerm + Progress)

## Phase 2 — BE service/api
- [x] Task 3: StorePurchaseContractRequest + PurchaseContractService
- [ ] Task 4: Transformers (list + detail)
- [ ] Task 5: Controller + Routes + seed 3 quyền

## Phase 3 — FE menu + danh sách
- [ ] Task 6: MenuSupply + index.vue

## Phase 4 — FE form thêm/sửa
- [ ] Task 7: Khung form + Tab Thông tin chung + add/edit
- [ ] Task 8: Tab Hàng hóa + popup chọn hàng
- [ ] Task 9: Tab Mẫu in

## Phase 5 — FE xem/duyệt + E2E
- [ ] Task 10: Trang xem read-only + trang duyệt
- [ ] Task 11: E2E Playwright toàn luồng + kiểm log

## Fix bổ sung
- [x] Fix 1: Đồng bộ thông báo lỗi + validate khi lưu form thêm/sửa theo chuẩn `contract/contract/add` (2026-08-03, @namdangit)
    - Thêm `validateInstallments()` chặn lưu khi "Thương mại - theo đợt" tổng tỷ lệ ≠ 100%
    - Phân biệt mã lỗi 422 (formError + scrollToInputError) / 400 (message server) / khác ("Thao tác thất bại")
    - File: `pages/supply/purchase_contracts/components/PurchaseContractForm.vue`
- [x] Fix 2: Hiện lỗi 422 tại từng field (không chỉ toast chung) (2026-08-03, @namdangit)
    - Bổ sung `base-helper-error` cho các field còn thiếu: `supplier_phone`, `progress.N.time` (GeneralTab); `products.N.price`, `products.N.order_qty` (ProductsTab)
    - Tự động nhảy sang tab đang có lỗi (`focusErrorTab` + `v-model="activeTab"` trên b-tabs) rồi mới scrollToInputError
    - File: PurchaseContractForm.vue, GeneralTab.vue, ProductsTab.vue
- [x] Fix 3: Lỗi "tổng tỷ lệ đợt phải = 100%" (validate client-side) hiện tại chỗ thay vì toast (2026-08-03, @namdangit)
    - `validateInstallments` gán vào `formError['progress_total']`, hiện `base-helper-error` ngay dưới bảng đợt, nhảy tab + scroll, bỏ toast
- [x] Fix 4: Tách "Điều khoản thanh toán" thành tab riêng (2026-08-03, @namdangit)
    - Tạo `PaymentTab.vue` (di chuyển toàn bộ mục 4 + computed sumPct/sumAmt/hasExclusive/payTermRows + method onPctInput/addProgressRow/onToggleTerm...)
    - GeneralTab bỏ mục 4 và code chỉ dùng cho phần đó (giữ progressRows cho onSignChange)
    - Thứ tự tab: Thông tin chung → Hàng hóa → Điều khoản thanh toán; `focusErrorTab`: general→0, products→1, payment(progress*/payment_terms*/progress_total)→2
- [x] Fix 5: Khi lưu trả về TẤT CẢ lỗi validate cùng lúc, không chặn sớm ở FE (2026-08-03, @namdangit)
    - Đưa rule "tổng tỷ lệ đợt = 100%" xuống BE `StorePurchaseContractRequest::withValidator` (key `progress_total`), chỉ áp dụng Thương mại + theo đợt
    - FE bỏ `validateInstallments` + return sớm → gọi thẳng API, hiển thị đủ lỗi 422 (trường bắt buộc + progress_total) trong 1 lần, tự nhảy tab + scroll
    - File BE: `Modules/Supply/Http/Requests/StorePurchaseContractRequest.php`; FE: PurchaseContractForm.vue
- [x] Fix 6: "Mã hợp đồng" (disabled) tô nền xám cho dễ phân biệt (2026-08-03, @khoipv)
    - FE `GeneralTab.vue`: thêm scoped `/deep/ input:disabled { background-color:#f1f5f7; cursor:not-allowed }` (đồng bộ màu với GeneralTab đơn mua hàng). Áp cho các field disabled (Mã hợp đồng, Thời hạn HĐ).
- [x] Fix 7: Chi tiết HĐ mua bị từ chối chưa hiện lý do từ chối (2026-08-03, @khoipv)
    - BE vốn đã trả đủ (`DetailPurchaseContractResource` có `status` + `reason_deny`), chỉ thiếu chỗ hiển thị FE.
    - FE `_id/index.vue`: thêm banner `alert-danger` trên `<PurchaseContractForm>`, hiện khi `detail.status === STATUS.REJECTED (4) && detail.reason_deny` — giống hệt đơn mua/phiếu đề xuất. Import `STATUS` từ `../constants`, thêm vào data.

## Checkpoint
### Checkpoint — 2026-08-03 (fix thông báo lỗi + validate)
Vừa hoàn thành: chuẩn hóa `save()` + `validateInstallments()` trong PurchaseContractForm.vue theo contract/contract/add
Đang làm dở: (không)
Bước tiếp theo: user kiểm tra thử luồng lưu nháp / lưu và gửi + lỗi 422 trên UI
Blocked: (không)

### Checkpoint — 2026-07-20 (khởi tạo)
Vừa hoàn thành: brainstorming + spec đầy đủ + plan chi tiết + khung .plans/STATUS
Đang làm dở: chuẩn bị chạy Task 1 (migrations)
Bước tiếp theo: subagent code Task 1 → review → Task 2...
Blocked: (không)

- [x] Fix 8: Điều khoản thanh toán (Theo đợt) sửa giống Đơn mua hàng — nhập 2 chiều tỉ lệ↔số tiền (2026-08-05, @khoipv)
    - FE `purchase_contracts/components/PaymentTab.vue`: cột Số tiền dùng `currency-input` (sửa được), cột Tỷ lệ `base-input-field` + `onRowInput`; port logic calcAmount/calcPercent/maxAmount/rebalancePercents + watch totalAmount + created; nút "Thêm đợt" → `base-add-button` (ml-auto); thêm banner cảnh báo `.pay-warning` khi tổng ≠ 100%. GIỮ nhánh Nguyên tắc, disabledBeforeSign, base-helper-error (progress.N.time + progress_total).
    - FE `PurchaseContractForm.vue`: thêm `amount:null` vào progressRows mặc định + applyInitial. buildPayload vẫn gửi pct (BE không đổi).

## Fix 9: Cột Tên hàng hóa hiện danh sách NCC đã từng mua hàng này (2026-09-19, @khoipv)
Yêu cầu: ở bảng hàng hóa màn lập HĐ mua, dưới tên hàng hóa hiện tên NCC đã mua hàng này (tính cả **HĐ mua** lẫn **đơn mua hàng**), sắp theo lần mua gần nhất; nhiều NCC → hiện 1 NCC + link "Xem thêm (N)" mở popup liệt kê phần còn lại.

Chốt với user: trạng thái tính = **Chờ duyệt (2) + Đã duyệt (3)** · ngoài tên NCC **không** hiện thêm gì ở cột · popup **đầy đủ cột + link chi tiết** · **gộp theo NCC** (mỗi NCC 1 dòng, lấy lần mua gần nhất, kèm số lần mua).

- [x] BE-1: `PurchaseContractService::productSupplierMap(array $productIds, ?int $excludeContractId)` — union 2 nguồn, gộp theo NCC, sort ngày mua DESC
- [x] BE-2: Action `productSuppliers()` ở `PurchaseContractController` + route `POST /purchase-contracts/product-suppliers` (đặt TRƯỚC wildcard `/{purchaseContract}`)
- [x] FE-1: Component mới `purchase_contracts/components/SupplierHistoryModal.vue` (bảng: STT · Tên NCC · Loại · Mã chứng từ (nuxt-link target=_blank) · Ngày mua · Số lần mua · SL · Đơn giá gồm VAT)
- [x] FE-2: `ProductsTab.vue` — fetch map theo `product_id`, render dòng "Đã mua của: <NCC> — Xem thêm (N)" dưới tên hàng hóa, mở popup
- [x] FE-3: Nạp lại map khi thêm hàng từ `GoodsPickerModal` (watch danh sách product_id)

### Fix 14: Cột VAT + Chiết khấu trước cột Thành tiền (2026-09-19, @khoipv)
User: "thêm cho tôi cột VAT và cột Chiết khấu trước cột thành tiền cho tôi, chỗ này tự lấy và tự tính nhé"
→ 2 cột CHỈ XEM, không cho nhập tay.
**Quy ước đã chốt (tự quyết vì hệ thống chưa có dữ liệu chiết khấu bên mua — user xác nhận lại giúp):**
- VAT (%) = **tự lấy** theo cặp (hàng hóa × HĐ bán): `contract_products.vat_percent`, thiếu thì lùi
  về `bid_package_products.vat_percent` của gói thầu gốc. Dòng nhỏ bên dưới là **tiền thuế tự tính**
  (đơn giá đã gồm VAT → tách ngược: tiền × vat / (100 + vat)).
- Chiết khấu (VNĐ) = **tự tính** = Σ theo từng phiếu: SL mua × (đơn giá báo giá − đơn giá mua),
  chỉ tính phần mua RẺ HƠN báo giá; mua đắt hơn → 0.
- **KHÔNG trừ chiết khấu vào Thành tiền** (đơn giá nhập đã là giá sau chiết khấu → trừ nữa là trừ 2 lần).
- [x] BE-9: Migration `2026_09_19_000002_add_discount_amount_to_purchase_contract_products_table.php`
      (cột `discount_amount` bigint nullable, không khóa ngoại) — đã chạy migrate
- [x] BE-10: `ResolvesProductReferences` trả thêm `vat_percent` theo cặp (thêm `vatPercentMapByPair()`,
      không đụng `SupplyHandlingService::productInfoMap` dùng chung)
- [x] BE-11: `PurchaseContractService::syncProducts` lưu `vat_percent` + `discount_amount`
      (Nguyên tắc → discount null); `DetailPurchaseContractResource` trả 2 cột này về FE
- [x] FE-10: `ProductsTab` thêm 2 cột trước Thành tiền (`refVat`/`fmtVat`/`vatOf`/`vatAmountOfSub`,
      `discountOfPurpose`/`discountOf`/`totalDiscount`/`discountTip`), colspan 14→15 / 17→19,
      dòng TỔNG CỘNG thêm ô tổng chiết khấu
- [x] FE-11: `syncDerived()`/`syncAllDerived()` ghi `vat_percent` + `discount_amount` xuống dòng hàng
      (gọi sau khi nạp tham chiếu + mỗi lần đổi giá/SL/ĐVT) để payload mang đi lưu
- Ghi chú: đổi ĐVT thì đơn giá mua quy đổi theo hệ số nhưng đơn giá báo giá tham chiếu vẫn là
  theo ĐVT của HĐ bán → số chiết khấu chỉ chuẩn khi 2 bên cùng ĐVT (giống hạn chế sẵn có của
  cột "Đơn giá báo giá")

### Fix 14b: Đơn giá báo giá quy đổi theo ĐVT đang chọn (2026-09-19, @khoipv)
User: "đơn giá báo giá cũng phải tính lại theo đơn vị cho tôi chứ"
`contract_products.price_quotation` là giá theo ĐVT của HĐ BÁN → phải quy về ĐVT đang chọn
của dòng hàng mới so sánh được với Đơn giá có VAT và mới tính đúng Chiết khấu.
- [x] BE-12: `ResolvesProductReferences` — gộp `vatPercentMapByPair` thành `saleContractMetaByPair`,
      trả thêm `price_unit_id` + `price_unit_name` (tên ĐVT lấy từ bảng `units`)
- [x] FE-12: `refPriceRaw` / `refPriceUnitId` / `refPriceValue` / `refPriceConverted` / `refPriceTip`
      — quy đổi qua mốc ĐVT cơ bản: giá(B) = giá(A)/f(A) × f(B); tooltip ghi rõ giá gốc + ĐVT gốc
- [x] FE-13: `discountOfPurpose` dùng giá ĐÃ quy đổi; `loadProductUnits` gọi `syncAllDerived()`
      sau khi có hệ số (map hệ số về sau map tham chiếu)
- [x] FE-14: Thiếu hệ số của ĐVT gốc → giữ số gốc, tô class `.ref-warn` + tooltip cảnh báo
      (không bịa số quy đổi)

### Fix 15: Chốt bề rộng cột bảng hàng hóa (2026-09-19, @khoipv)
User: "các cột nó đang bị giãn ra nhiều quá nếu nội dung dài, cố định lại, dài quá thì xuống dòng"
Nguyên nhân: `td { white-space: nowrap }` + `table width: auto` → nội dung dài kéo giãn cả bảng.
- [x] FE-15: Gắn class `cell-spec` (Quy cách) / `cell-origin` (Hãng, nước SX) / `cell-purpose-h`
      cho th + td để bám được CSS
- [x] FE-16: Các cột chữ (`cell-name`, `cell-spec`, `cell-origin`, `cell-purpose`) chuyển
      `white-space: normal` + `word-break: break-word` + chốt min/max-width
      (200-280 / 100-150 / 110-160 / 240-320 px)
- [x] FE-17: `.pp-line` (Mục đích mua) đổi `flex-wrap: nowrap` → `wrap`; `.sup-line` bỏ max-width
      cứng 280px về 100%; th tiêu đề dài cho xuống dòng

### Fix 14c: Bề rộng cột bảng hàng hóa (2026-09-19, @khoipv)
User: "cột tên hàng hóa cho rộng ra chút nữa, cột mục đích mua để như cũ"
- [x] FE-15: `.cell-name` min 200→260px, max 280→380px
- [x] FE-16: Trả cột Mục đích mua về đúng như trước: bỏ class `cell-purpose-h` ở `<th>`,
      bỏ chốt min/max-width 240/320px, `td.cell-purpose` quay lại `white-space: nowrap`

### Checkpoint — 2026-09-19
Vừa hoàn thành: Fix 13 + Fix 13b + Fix 14 (cột VAT & Chiết khấu) — đã `php -l`, chạy migrate, compile template Vue + parse script OK
Đang làm dở: không
Bước tiếp theo: user build lại client rồi click-test màn lập/sửa HĐ mua — đổi ĐVT, 4 cột tham chiếu, ghi chú theo từng HĐ bán (kiểm tra `quotation_tab_products.note_supply`), và xác nhận quy ước 2 cột VAT / Chiết khấu ở Fix 14
Blocked: chờ user duyệt việc tách 3 trait dùng chung (đụng file màn đơn mua hàng) + chốt lại công thức Chiết khấu
