# Plan — Đơn mua hàng (build thật)

> Spec: `docs/superpowers/specs/2026-07-30-don-mua-hang-design.md`
> Plan chi tiết: `docs/superpowers/plans/2026-07-30-don-mua-hang.md` · @khoipv

## Trạng thái: ĐÃ CÓ PLAN CHI TIẾT — CHỜ CHỌN CÁCH THỰC THI

## Task list (14 task / 7 phase)

### Phase 1 — BE schema ✅
- [x] Task 1 — 4 migration (purchase_orders, _products +buyer_company_id/need_date, _payment_terms, _progress) → migrate OK, cột đủ
- [x] Task 2 — 4 Entity (PurchaseOrder + Product/PaymentTerm/Progress) → smoke quan hệ OK
- [x] Task 3 — PurchaseOrderPermissionSeeder (id 521/522/523) → seed OK, đếm = 3

### Phase 2 — BE logic ✅
- [x] Task 4 — PurchaseOrderService (generateCode DMH-, getList, store/update, sync*, approve/reject, notif) → generateCode=DMH-2026-0001
- [x] Task 5 — StorePurchaseOrderRequest (rules + messages, buyer_company_id required)
- [x] Task 6 — PurchaseOrderController (index/nextCode/store/show/update/approve/reject/destroy/companies/suppliers/goodsPool)
- [x] Task 7 — Routes /purchase-orders (static trước wildcard, checkPermission) → 11 route OK

### Phase 3 — BE transformer ✅
- [x] Task 8 — PurchaseOrderResource + DetailPurchaseOrderResource → smoke store OK (DMH-2026-0001|total=2000|lines=1)

### Phase 4 — FE khung ✅
- [x] Task 9 — constants.js + menu item "Đơn mua hàng" (dưới HĐ mua)
- [x] Task 10 — index.vue (danh sách, bộ lọc base-select2/date-picker) — verify Playwright ở Task 14

### Phase 5 — FE form ✅
- [x] Task 11 — PurchaseOrderForm + add.vue + _id/index.vue + _id/edit.vue
- [x] Task 12 — GeneralTab.vue (Thông tin đơn / NCC / Dư nợ placeholder / Điều khoản TT)

### Phase 6 — FE hàng hóa ✅
- [x] Task 13 — ProductsTab (cột Cty thực hiện mua base-select2 bắt buộc + <Required/> + Cty thực hiện bán + Ngày cần) + GoodsPickerModal (saleCompany)

### Phase 7 — Verify ✅
- [x] Task 14 — E2E: lập/gửi/duyệt/từ chối/sửa/xóa + regression HĐ mua → wrap up (Claude lái Playwright, JWT admin id=13)

### Phase 8 — Điều chỉnh sau nghiệm thu ✅
- [x] Task 15 — Popup "Chọn hàng hóa" CHỈ lấy hàng từ Báo cáo nhu cầu mua (bỏ nguồn danh mục chung `catalog`)
  - BE `PurchaseOrderController::goodsPool`: bỏ `SupplyProposalService::goodsPool(2)` + import, chỉ trả `demand` (giữ `catalog=>[]` cho FE an toàn). php -l OK. Verify API: demand=9, catalog=0.
  - FE `GoodsPickerModal.vue`: bỏ nhánh `catalog` trong `buildCandidates`, bỏ bộ lọc "Nguồn" + `source`/`sourceOptions`, search full-width (col-md-12), cột Nguồn luôn "Theo phiếu đề xuất". Verify UI: 9 hàng, không dropdown Nguồn, chọn→thêm vào đơn OK.

- [x] Task 16 — ProductsTab: chuyển cột "Cty thực hiện bán" xuống cạnh "Cty thực hiện mua" (cột 12 & 13). Sửa header + dòng TỔNG CỘNG (cột số dịch trái 1) + dòng dữ liệu + comment colspan. Vẫn 16 cột.

- [x] Task 17 — Thanh toán "Theo đợt" giống HĐ bán (/contract/contract/add): 2 chiều tỉ lệ↔số tiền
  - FE `GeneralTab.vue`: thêm `amount` vào progressRows; cột Số tiền dùng `currency-input` (base) cho sửa được; ô Tỷ lệ dùng base-input-field type=number. Logic 2 chiều copy từ `PaymentBlockCard.vue`: nhập % → ra tiền (cắt theo phần còn lại), nhập tiền → ra % (số tiền là gốc), `rebalancePercents` dồn lẻ vào đợt cuối. Nút thêm dùng `base-add-button`. Cảnh báo khi tổng ≠ 100%.
  - FE `PurchaseOrderForm.vue`: applyInitial suy ra `amount` từ pct×totalAmount khi nạp; dòng mặc định thêm `amount:null`. buildPayload vẫn gửi `pct` (BE `purchase_order_progress` chỉ có cột pct — giống HĐ mua/bán).

- [x] Task 18 — Tách "Điều khoản thanh toán" ra tab riêng (tab thứ 3)
  - Tạo `PaymentTab.vue`: bê nguyên section thanh toán (theo đợt 2 chiều + theo đơn + ghi chú) + toàn bộ logic (props form/progressRows/payTerms/totalAmount/readonly/formError, computed sumPct/sumAmt/roundedTotal/hasExclusive/payTermRows, watch totalAmount, created, methods 2 chiều + payTerm) + styles.
  - `GeneralTab.vue`: bỏ section 4 + props/computed/methods/watch/created/styles/constants liên quan thanh toán → chỉ còn Thông tin đơn/NCC/Giao nhận.
  - `PurchaseOrderForm.vue`: import + đăng ký PaymentTab; thêm `<b-tab title="Điều khoản thanh toán">`; bỏ progress-rows/pay-terms/total-amount khỏi GeneralTab. Không đổi BE/payload.

- [x] Task 19 — NCC: "Người liên hệ" thêm nhanh giống dự toán (sale/project) + SĐT auto theo người liên hệ
  - FE `GeneralTab.vue`: đổi "Người liên hệ" từ input text → `base-select2` danh sách liên hệ của NCC; thêm icon `mdi-plus-circle` mở `CustomerContactModal` (component dùng chung) để thêm nhanh; "Điện thoại liên hệ" thành read-only auto-fill từ liên hệ đã chọn (`form.supplier_phone`).
  - Nạp liên hệ qua endpoint dùng chung `category/customers/{supplier_id}` → `.contact` (giống sale/project, KHÔNG sửa BE `suppliers()`). `onSelectSupplier` bỏ auto-fill phone/representative, reset + load lại contacts; `created` khớp lại theo tên khi edit/show; `@reload` sau khi thêm liên hệ mới → load lại list.

- [x] Task 20 — Giao nhận: đổi "Địa chỉ giao hàng" → "Địa chỉ nhận hàng" + thêm nhanh giống HĐ bán (contract/contract/add)
  - FE `GeneralTab.vue`: đổi nhãn; "Địa chỉ nhận hàng" thành `base-select2` danh sách địa chỉ nhận của NCC + icon `mdi-plus-circle` mở `AddDeliveryModal` (component dùng chung của HĐ bán) để thêm nhanh.
  - Nạp địa chỉ qua endpoint dùng chung `category/customers/{supplier_id}/getReceiveAddress`; modal POST `category/contracts/delivery-address` với `customer_id = supplier_id`. `@reload` → nạp lại list + tự chọn địa chỉ mới nhất. `created` dispatch `optionsSelect/fetchNationsOptions` (modal cần danh mục QG/tỉnh/huyện) + khớp lại theo `full_address` khi edit/show.
  - Vẫn lưu `form.delivery_address` là chuỗi `full_address` (KHÔNG đổi BE — cột `delivery_address` giữ nguyên kiểu string). Địa chỉ nhận gắn theo NCC như một sổ địa chỉ per-NCC (tương tự HĐ bán gắn theo khách hàng).

- [x] Task 21 — Bảng hàng hóa: thêm 4 cột chỉ-xem "Đơn giá báo giá / Ghi chú báo giá / Ghi chú thầu / Ghi chú hợp đồng" (tham khảo supply/supply_handlings), lấy từ HĐ bán theo từng (mã hàng, HĐ bán)
  - BE `SupplyReportService::purchaseDemand()` (dùng chung — Báo cáo nhu cầu mua cũng dùng): CỘNG THÊM `contract_id` + `contract_code` vào mỗi dòng `lines[]` (build `codeByContract` từ cùng query Contract). Không đổi key/logic cũ.
  - BE `PurchaseOrderController::productInfo(Request)` + route `POST supply/purchase-orders/product-info`: nhận `items:[{product_id, contract_id}]`, gom theo contract_id gọi `SupplyHandlingService::productInfoMap()` từng nhóm (map key theo product_id) → trả map key `{product_id}_{contract_id}` gồm 4 field. KHÔNG sửa hàm dùng chung `productInfoMap`.
  - FE `GoodsPickerModal.vue`: thread `contract_id`/`contract_code` vào mỗi purpose (thay `saleContract:''` bằng `contract_code`) → purposes lưu vào JSON `purchase_order_products.purposes` (không cần migration).
  - FE `ProductsTab.vue`: thêm 4 cột chỉ-xem sau "Thành tiền"; mỗi dòng gộp lấy contract distinct từ purposes → hiển thị sub-line theo từng HĐ (giống cột Mục đích mua); nạp product-info ở created + sau khi thêm dòng. colspan 16→20, dòng TỔNG CỘNG +4 ô trống.

- [x] Task 22 — "Người lên đơn" tự lấy tên tài khoản đang đăng nhập (khi lập mới)
  - FE `PurchaseOrderForm.vue`: mounted nhánh `isAdd` set `form.creator_name = $store.state.current_employee_info.fullname`.
  - FE `GeneralTab.vue`: ô "Người lên đơn" thành read-only (`:disabled="true"`) — luôn phản ánh tài khoản tạo đơn, không sửa tay. BE không đổi (cột `creator_name` đã lưu qua payload).

- [x] Task 23 — "Ngày lập" mặc định ngày hiện tại, vẫn sửa được (khi lập mới)
  - FE `PurchaseOrderForm.vue`: import `dayjs`; nhánh `isAdd` set `form.order_date = dayjs().format('YYYY-MM-DD')` (khớp format Y-m-d BaseDatePicker dùng). Ô vẫn `:disabled="readonly"` → sửa được. BE không đổi.

- [x] Task 24 — Popup "Chọn hàng hóa": mỗi phiếu đề xuất (phiếu × mã) = 1 dòng riêng; gộp theo mã khi thêm ra ngoài
  - FE `GoodsPickerModal.vue::buildCandidates`: nổ `row.lines[]` → mỗi `line` thành 1 candidate với `purposes` 1 phần tử; "SL đề xuất mua"/`order_qty` = SL phiếu đó; `proposalText`/`customerText` là giá trị đơn (không join). Mã không có phiếu → 1 dòng không phiếu (SL = total_buy_qty).
  - Gộp khi ra ngoài: KHÔNG đổi — `ProductsTab.mergeLine` sẵn gộp theo mã (cộng proposed_qty + order_qty theo buySum + ghép purposes dedup proposal+customer). BE không đổi.

- [x] Task 25 — Thêm "Mã phiếu xử lý" (phiếu xử lý cung ứng) vào popup + bảng hàng hóa
  - BE không đổi: `SupplyReportService::purchaseDemand` lines[] đã có `handling_code`/`handling_id`.
  - FE `GoodsPickerModal.vue`: purpose thêm `handling: l.handling_code`; candidate thêm `handlingText`; GỘP 1 cột "Phiếu đề xuất / xử lý" (mã ĐX trên, `PXL <mã>` xanh dưới); search + placeholder gồm mã phiếu xử lý; colspan giữ 10.
  - FE `ProductsTab.vue`: sub-line "Mục đích mua" hiện `PXL {{ pp.handling }}` (badge xanh) sau mã phiếu đề xuất; `mergeLine` key chống trùng thêm `handling` (tránh mất dòng khi cùng phiếu ĐX+KH nhưng khác phiếu xử lý). Style `.pp-handling`.

- [x] Task 26 — Click mã phiếu (DXCU + PXL) → popup chi tiết (giống demo `demo-tao-don-mua-hang.html`)
  - Chốt: cả DXCU (phiếu đề xuất) + PXL (phiếu xử lý) clickable; ở CẢ popup "Chọn hàng hóa" LẪN bảng hàng hóa (cột Mục đích mua). Tái dùng endpoint show sẵn có (`supply/supply-proposals/{id}`, `supply/supply-handlings/{id}`) — KHÔNG thêm BE.
  - FE mới `SupplyDocDetailModal.vue`: props kind('proposal'|'handling')+docId+docCode; fetch on show; header grid (dd-grid) + bảng hàng hóa. Proposal: type 1 KH/2 nội bộ, purpose_name, usage_customer, delivery_date, content, products[quantity/alloc_mua]. Handling: type_name/status_name/created_at/approved_at/proposal.code, products[dat_don/alloc_mua].
  - FE `GoodsPickerModal.vue`: purpose thêm `proposal_id`/`handling_id` (từ demand lines BE sẵn có); candidate thêm proposalId/handlingId; DXCU+PXL thành `<a>` mở modal (nhúng SupplyDocDetailModal, @click.stop tránh chọn dòng).
  - FE `ProductsTab.vue`: sub-line DXCU+PXL thành link (chỉ khi có id) → mở SupplyDocDetailModal. purposes JSON persist proposal_id/handling_id (BE json_encode nguyên mảng — không migration).

- [x] Task 27 — Cột "Mục đích mua": phần HĐ bán hiển thị MÃ hợp đồng (contracts.code, vd HD-002/2025) thay vì SỐ HĐ (contracts.number); click mã → popup chi tiết HĐ bán
  - BE `PurchaseOrderController::productInfo`: build `contractCodes = Contract::whereIn(id, groups)->pluck('code','id')` → thêm `contract_code` (mã thật) vào mỗi entry map. KHÔNG đổi hàm dùng chung `SupplyReportService::purchaseDemand` (vẫn trả số HĐ ở lines[].contract_code) → mã lấy qua endpoint DMH riêng, sửa luôn đơn đã lưu (order #7).
  - BE mới `PurchaseOrderController::saleContractInfo(Contract)` + route `GET supply/purchase-orders/sale-contracts/{contract}`: đọc trực tiếp `contracts` + `contract_products` (join `units`) — KHÔNG dùng `ContractDetailResource` (nặng + snapshot v0 không tin). Trả header (mã/số/loại/trạng thái/KH/cty thực hiện/ngày ký-KT-duyệt/giá trị) + products[] (mã nội bộ/mã HH/tên/ĐVT/SL/đơn giá/thành tiền). status map thủ công (model không có accessor); ngày trả raw cho FE format (model không cast date).
  - FE mới `ContractDetailModal.vue`: b-modal xl, prop contractId+contractCode; fetch `sale-contracts/{id}` on show; grid header (cd-grid) + bảng hàng hóa.
  - FE `ProductsTab.vue`: helper `saleContractCode(p,pp)` = mã thật `refOf(p,pp.contract_id).contract_code` (fallback `pp.saleContract`); phần HĐ bán thành link `.pp-doc-link-contract` (tím) → `openContract(pp.contract_id, mã)` mở ContractDetailModal (chỉ khi có contract_id). Nhúng modal + state contractVisible/contractId/contractCode.

- [x] Task 28 — Lập đơn mua trực tiếp từ Báo cáo tổng hợp nhu cầu mua (giống nút Lập HĐ mua)
  - FE `reports/purchase-demand/index.vue`: nút "Lập đơn mua" (hiện khi tick "Chỉ mã chưa có HĐ mua") đổi từ mô phỏng `openLapHdMua('don')` → `goToCreateOrder()` thật.
  - `goToCreateOrder`: gom dòng đã tick → `buildOrderLine(row)` (shape ProductsTab DMH, mỗi mã 1 dòng gộp nhiều purposes; kèm proposal_id/handling_id/contract_id/contract_code/saleCompany để 4 cột tham chiếu + link popup hoạt động) → `sessionStorage.purchase_order_seed` → `$router.push('/supply/purchase_orders/add')`. DMH `add.vue` đọc sẵn seed → `PurchaseOrderForm.applySeedProducts` (mounted, isAdd).
  - Bỏ mock: modal `pdr-hdmua-modal` + method `openLapHdMua`/`confirmLapHdMua` + data `hdMuaForm` (không còn ai gọi). `goToCreateContract`/`buildContractLine` (HĐ mua) giữ nguyên.
  - Timing OK: `v-if="loading"` bọc tabs → ProductsTab chỉ created sau khi mounted set products → loadProductRefs nạp mã HĐ đúng. BE không đổi (tái dùng goods-pool/product-info/store DMH).

- [x] Task 29 — Nút "Duyệt" ở màn danh sách HĐ mua + Đơn mua hàng: duyệt trực tiếp tại list (đồng nhất với đề xuất cung ứng), thay vì điều hướng sang chi tiết
  - FE `purchase_orders/index.vue` + `purchase_contracts/index.vue`: icon check thêm `text-success` (xanh, giống DXCU); `onApproveClick` đổi từ `$router.push(chi tiết)` → msgBoxConfirm (title "Xác nhận duyệt", okTitle "Duyệt", okVariant success) → `apiPutMethod` `.../{id}/approve` → toast → `getData()` refresh list. Endpoint tái dùng của màn chi tiết. Không thêm nút Từ chối (user chỉ yêu cầu nút Duyệt).

- [x] Task 30 — Đưa 3 quyền đơn mua hàng (521 Xem / 522 Lập / 523 Duyệt) vào seeder CHUẨN `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (ngay sau HĐ mua 518-520, cùng style `Permission::create`), thay cho seeder riêng. Xóa `Modules/Supply/Database/Seeders/PurchaseOrderPermissionSeeder.php` (thừa, không được gọi ở đâu). Quyền đã có sẵn trong DB + đã gán role Admin từ trước.

- [x] Task 31 — Popup xác nhận từ chối dùng chung `components/modal/ConfirmReasonDenyModal.vue`: thêm label "Lý do từ chối `<Required/>`" + validate bắt buộc nhập lý do.
  - FE `ConfirmReasonDenyModal.vue`: thêm `<label>Lý do từ chối <Required /></label>`; textarea thêm `:class="{'is-invalid': showError}"` + `@input="showError=false"`; `<div class="invalid-feedback d-block">Vui lòng nhập lý do từ chối</div>` khi lỗi; `@show` reset showError.
  - `deleteTimeShift()` chặn emit khi `reason_deny` trống/whitespace (set showError=true, return) → parent không gọi API. Bỏ `v-b-modal.modal-close_visit` thừa ở nút Đồng ý. Ảnh hưởng 11 màn dùng chung modal này (user chốt sửa tại component dùng chung).

- [x] Task 32 — Thu gọn khoảng trắng/layout "rộng" toàn module Cung ứng (rà soát bằng Explore agent → sửa các khe dọc lớn + gutter ngang thừa)
  - FE `supply_proposals/add.vue` (Chi tiết/Lập phiếu đề xuất): 2 card `mt-3→mt-2`, cột `mb-3→mb-1`, tabs `mt-3→mt-1`; thêm CSS `.top-compact` giảm gutter ngang 15px→6px giữa 2 cột (Thông tin chung / Nội dung & đính kèm).
  - FE `supply_handlings/add.vue` (Chi tiết/Lập phiếu xử lý): card khối 1 & 2 `mt-3→mt-2`, footer nút `mt-3 mb-4→mt-2 mb-3`, các banner alert `mt-3→mt-2`, cột nội dung đề xuất `mb-3→mb-2`.
  - FE `PurchaseOrderForm.vue` + `PurchaseContractForm.vue`: thêm class `.form-body-row` + CSS `> .col-md-12 {padding 0}` triệt padding ngang ~15px thừa hai mép khung ngoài (`row col-12 > col-md-12`).
  - FE `purchase_contracts/components/GeneralTab.vue` (Điều khoản TT thương mại): gộp nút "Thêm đợt" lên cùng dòng dropdown "Hình thức thanh toán" (`ml-auto`, bỏ dòng riêng), `mb-3→mb-2` — đồng nhất với PaymentTab đơn mua.
  - FE `PaymentTab.vue` (đơn mua, đã làm trước đó cùng mạch): gộp nút thêm đợt lên dòng dropdown, bỏ dòng riêng.
  - KHÔNG đụng: `.category-card` global (shared), `.row.g-2 > col {margin-bottom:10px}` (khe field), padding bảng/card-body đã gọn, 5 trang list (khung đã ổn), dashboard placeholder rỗng (py-5 — ưu tiên thấp, để nguyên).

- [x] Task 33 — Đồng bộ thông báo lỗi + validate khi lưu (giống HĐ mua): trả TẤT CẢ lỗi cùng lúc, hiện tại từng field, tự nhảy tab (2026-08-03, @khoipv)
  - BE `StorePurchaseOrderRequest::withValidator`: thêm rule "tổng tỷ lệ đợt = 100%" (key `progress_total`), chỉ áp dụng khi `payment_mode === 'dot'`; thiếu đợt hoặc tổng ≠ 100% → lỗi validate cùng bộ (không còn cho lưu sai). php -l OK.
  - FE `PaymentTab.vue`: thêm `base-helper-error :error="formError['progress_total']"` ngay dưới bảng đợt (cạnh cảnh báo tổng ≠ 100%).
  - FE `PurchaseOrderForm.vue`: `b-tabs` thêm `v-model="activeTab"` (+ data `activeTab:0`); import `scrollToInputError`; `save()` catch 422 → gán formError + `focusErrorTab` (general→0, products→1, payment[progress*/payment_terms*/progress_total]→2) + toast "Vui lòng kiểm tra lại dữ liệu nhập" + scroll tới ô lỗi đầu.
  - GeneralTab + ProductsTab đã có sẵn `base-helper-error` cho các field BE validate (order_date/order_type/supplier_id/supplier_address; products + products.N.*), không cần sửa.

- [x] Task 34 — Field disabled tô nền xám cho dễ nhận biết (2026-08-03, @khoipv)
  - FE `GeneralTab.vue` (đơn mua): thêm scoped `/deep/ input:disabled { background-color:#f1f5f7 !important; cursor:not-allowed }` → Mã đơn, Người lên đơn, Điện thoại liên hệ (field tự sinh/read-only) có nền xám GIỐNG select2 disabled thay vì trắng.
  - Lưu ý: dùng `/deep/` (không phải `::v-deep`) theo convention project (custom-form/custom-assign.scss); màu `#f1f5f7` lấy từ `custom-theme.scss` `.select2-container--disabled` để đồng bộ với ô "Người liên hệ".

- [x] Task 35 — Căn thẳng field có nút "thêm nhanh" (2026-08-03, @khoipv)
  - FE `GeneralTab.vue` (đơn mua): icon `.plus-icon` (mdi-plus-circle, 16px) làm cao dòng label → input "Người liên hệ" / "Địa chỉ nhận hàng" bị thụt xuống so với field khác. Thêm `line-height:0; vertical-align:middle` cho `.plus-icon` → icon không đội cao label, các field căn thẳng bằng nhau. Không đụng label khác.

- [x] Task 35 — "Địa chỉ nhận hàng" bắt buộc nhập (2026-08-03, @khoipv)
  - Chốt: GIỮ auto-fill khi có dữ liệu, để trống nếu chưa có, cả 2 ô địa chỉ đều bắt buộc. "Địa chỉ lấy hàng" (supplier_address) đã required sẵn → không đổi.
  - BE `StorePurchaseOrderRequest`: thêm rule `'delivery_address' => ['required','string']` + message "Vui lòng chọn hoặc nhập địa chỉ nhận hàng." php -l OK.
  - FE `GeneralTab.vue`: label "Địa chỉ nhận hàng" thêm `<Required />`; thêm `base-helper-error :error="formError['delivery_address']"` dưới base-select2. Lỗi rơi vào tab Thông tin chung (focusErrorTab → 0). Auto-fill/để-trống hiện tại giữ nguyên (onSelectSupplier reset về '' rồi nạp list, không tự chọn).

- [x] Task 36 — Fix "Địa chỉ nhận hàng" tự hiện option "(blank)" (2026-08-03, @khoipv)
  - Nguyên nhân: `receiveAddressOptions` map thẳng `text: a.full_address`; nếu NCC có dòng địa chỉ rác (full_address null/'') thì select2 render option "(blank)". (Không phải do allowClear — ô "Người liên hệ" cũng allowClear mà không lỗi vì tên luôn có giá trị.)
  - FE `GeneralTab.vue`: `receiveAddressOptions` thêm `.filter(a => a && a.full_address)` bỏ dòng rỗng; logic tự chọn địa chỉ mới nhất sau modal thêm cột `&& a.full_address` để không tự chọn phải dòng rỗng.

- [x] Task 37 — Chi tiết đơn mua hàng bị từ chối không hiện lý do từ chối (2026-08-03, @khoipv)
  - Nguyên nhân: BE lưu + trả `reason_deny` đầy đủ (rejectApprove ghi cột reason_deny, DetailPurchaseOrderResource trả reason_deny + status) nhưng trang chi tiết FE không render lý do ở đâu (chỉ dùng reason_deny trong modal từ chối).
  - FE `_id/index.vue`: thêm banner `alert-danger` phía trên `<PurchaseOrderForm>`, hiện khi `detail.status === STATUS.REJECTED (4) && detail.reason_deny` — đúng pattern phiếu đề xuất/xử lý (`supply_proposals/add.vue`). Import `STATUS` từ `../constants`, thêm vào data.

- [x] Task 38 — Badge trạng thái danh sách đơn mua (nhất là "Nháp") nhìn xấu (2026-08-03, @khoipv)
  - Nguyên nhân: cột trạng thái dùng `<b-badge :variant="status_color">` → badge đặc; "Nháp" = secondary (xám đậm, nặng, có shadow) trông xấu.
  - FE `index.vue`: đổi sang `<span class="badge status-badge badge-soft-${status_color}">` (theme có sẵn `badge-soft-*` cho mọi màu trong $theme-colors: secondary/warning/success/danger/dark) → badge nền nhạt, chữ màu, bỏ shadow. Thêm style `.status-badge` dạng pill (bo tròn, padding, font 12/600).

- [x] Task 40 — Thêm placeholder ô "Mã NCC" + "MST" (2026-08-03, @khoipv)
  - FE `GeneralTab.vue` (đơn mua): 2 ô thiếu placeholder → thêm "Tự lấy theo nhà cung cấp" (2 ô này auto-fill từ NCC khi chọn nhà cung cấp, đồng bộ cách diễn đạt với các ô auto-fill khác).

- [x] Task 39 — Badge trạng thái đơn mua giống pill của contract/contract (2026-08-03, @khoipv)
  - User revert Task 38 (soft badge), yêu cầu dùng đúng style pill pastel của danh sách HĐ bán.
  - FE `index.vue`: dùng component dùng chung `BaseStatusColor` (:status + :colorMap) thay `b-badge`. colorMap map 5 trạng thái sang class pill giống contract: 1 Nháp→pj-status-blue (giống "Đang tạo"), 2 Chờ duyệt→pj-status-yellow, 3 Đã duyệt→pj-status-green, 4 Từ chối→pj-status-red, 5 Hủy→pj-status-rose. Không đổi BE, không sửa component dùng chung.

### Checkpoint — 2026-08-03 (Task 38f — root cause dấu "—" lệch cao 4 cột tham chiếu)
Vừa hoàn thành: Tìm ra và sửa root cause thật (sau 5 lần fix CSS hụt): newline template + `pre-line` tạo dòng trống trong 3 cột ghi chú → dấu "—" cột Đơn giá báo giá cao hơn. Fix: span.ref-val bao sát giá trị (pre-line chỉ ở value), td ghi chú về white-space normal. Repro Playwright đo pixel xác nhận trước/sau.
Đang làm dở: (không)
Bước tiếp theo: user reload supply/purchase_orders/add, thêm dòng hàng có HĐ bán nhưng chưa có báo giá → dấu "—" 4 cột tham chiếu phải thẳng hàng; ghi chú nhiều dòng vẫn xuống dòng đúng.
Blocked:

### Checkpoint — 2026-08-03 (Task 38 — badge trạng thái soft/pill)
Vừa hoàn thành: Danh sách đơn mua hàng đổi badge trạng thái sang dạng "soft" nền nhạt + pill bo tròn — "Nháp" (secondary) nhẹ nhàng, đồng bộ đẹp cho cả 5 trạng thái.
Đang làm dở: (không)
Bước tiếp theo: user reload supply/purchase_orders → xem badge trạng thái mới; nếu ưng có thể áp dụng tương tự cho list HĐ mua (đang dùng badge đặc y hệt).
Blocked:

### Checkpoint — 2026-08-03 (Task 37 — hiện lý do từ chối ở chi tiết đơn mua)
Vừa hoàn thành: Trang chi tiết đơn mua hàng bị từ chối giờ hiện banner đỏ "Lý do từ chối: ..." ở đầu trang (lấy từ detail.reason_deny). BE vốn đã trả đủ, chỉ thiếu chỗ hiển thị FE.
Đang làm dở: (không)
Bước tiếp theo: user mở lại supply/purchase_orders/8 (đơn đã từ chối) → phải thấy banner đỏ với lý do đã nhập.
Blocked:

### Checkpoint — 2026-08-03 (Task 36 — fix "(blank)" địa chỉ nhận hàng)
Vừa hoàn thành: Bỏ option "(blank)" ở select2 "Địa chỉ nhận hàng" (đơn mua) — lọc dòng địa chỉ có full_address rỗng khỏi danh sách chọn + không auto-chọn dòng rỗng sau khi thêm nhanh.
Đang làm dở: (không)
Bước tiếp theo: user reload màn Lập đơn mua hàng, chọn NCC → dropdown địa chỉ nhận hàng không còn dòng "(blank)"; test thêm nhanh địa chỉ → tự chọn địa chỉ mới hợp lệ.
Blocked:

- [x] Task 36 — Ẩn giá trị rác "(blank)" khi auto-fill NCC (2026-08-03, @khoipv)
  - FE `GeneralTab.vue` (đơn mua): NCC có `address` lưu là chuỗi rác `(blank)` (do import Excel) → ô "Địa chỉ lấy hàng" hiện "(blank)". Thêm helper `cleanText(v)` (trim + lowercase == '(blank)' → ''); `onSelectSupplier` bọc `cleanText` cho code/name/address/tax → coi "(blank)" như rỗng. supplier_address required vẫn chặn khi trống (user phải nhập địa chỉ thật).

### Checkpoint — 2026-08-03 (Task 33 — đồng bộ báo lỗi/validate khi lưu)
Vừa hoàn thành: Màn Lập đơn mua hàng (supply/purchase_orders/add) giờ báo lỗi validate giống HĐ mua — lưu 1 lần thấy TẤT CẢ lỗi (trường bắt buộc + tổng tỷ lệ đợt = 100% ở BE), lỗi hiện ngay tại field, tự nhảy sang tab có lỗi + cuộn tới ô đầu tiên.
Đang làm dở: (không)
Bước tiếp theo: user test — lập đơn Thanh toán theo đợt tổng ≠ 100% + bỏ trống vài trường bắt buộc → phải thấy tất cả lỗi cùng lúc, đúng tab. Rồi commit BE + FE.
Blocked:

### Checkpoint — 2026-07-31 (Task 32)
Vừa hoàn thành: Rà soát & thu gọn layout "rộng" toàn module Cung ứng. Explore agent quét 15+ file → xác định các khe DỌC lớn (mt-3/mb-4 giữa card khối) + gutter NGANG thừa (row col-12 > col-md-12, khe 2 cột card) → sửa ở 5 file form/chi tiết (2 phiếu đề xuất/xử lý + 2 form đơn/HĐ mua + GeneralTab HĐ mua). Trang list/báo cáo/dashboard đã gọn, không cần sửa. Không đụng class/style dùng chung.
Đang làm dở: (không)
Bước tiếp theo: user verify UI các màn chi tiết/lập của Cung ứng (đề xuất, xử lý, đơn mua, HĐ mua) — kiểm tra bố cục sát hơn, không hụt lề + commit FE.
Blocked:

### Checkpoint — 2026-07-31 (Task 31)
Vừa hoàn thành: `ConfirmReasonDenyModal.vue` (popup xác nhận từ chối dùng chung) — thêm dấu * bắt buộc (`<Required/>`) + thông báo validate inline "Vui lòng nhập lý do từ chối", chặn xác nhận khi bỏ trống lý do. Áp dụng cho toàn bộ 11 màn dùng chung.
Đang làm dở: (không)
Bước tiếp theo: user verify UI (mở popup từ chối bất kỳ màn nào → bấm Đồng ý khi trống → hiện thông báo đỏ, không đóng) + commit FE.
Blocked:

### Checkpoint — 2026-07-31 (Task 30)
Vừa hoàn thành: Chuyển khai báo 3 quyền đơn mua hàng vào PermissionsTableSeeder.php chuẩn (521/522/523, group Cung ứng, type 7) — 1 nguồn duy nhất giống HĐ mua. Xóa seeder riêng PurchaseOrderPermissionSeeder.php. php -l OK.
- DB hiện tại đã có 521-523 + đã gán role Admin (kiểm tra trực tiếp DB) → menu "Đơn mua hàng" hiển thị bình thường với Admin.
Đang làm dở: (không)
Bước tiếp theo: user commit BE. Khi seed lại môi trường mới → quyền đơn mua hàng ra cùng batch với các quyền Cung ứng khác.
Blocked:

### Checkpoint — 2026-07-31 (Task 29)
Vừa hoàn thành: Nút Duyệt ở 2 màn danh sách (HĐ mua + Đơn mua hàng) giờ duyệt ngay tại list (confirm dialog → gọi API approve → refresh), đồng nhất với màn đề xuất cung ứng. Icon check chuyển xanh (text-success). Trước đó chỉ điều hướng sang chi tiết.
Đang làm dở: (không)
Bước tiếp theo: user verify (bấm Duyệt ở list → confirm → trạng thái đổi Đã duyệt) + commit FE.
Blocked:

### Checkpoint — 2026-07-31 (Task 28)
Vừa hoàn thành: Nút "Lập đơn mua" ở Báo cáo tổng hợp nhu cầu mua giờ tạo đơn THẬT (giống Lập HĐ mua) — seed hàng đã tick sang form DMH qua sessionStorage, không còn mô phỏng.
- FE `reports/purchase-demand/index.vue`: `goToCreateOrder` + `buildOrderLine` (shape DMH đầy đủ purposes có proposal_id/handling_id/contract_id/contract_code); bỏ mock modal + hdMuaForm.
- Tái dùng `add.vue` + `PurchaseOrderForm.applySeedProducts` sẵn có (đọc `purchase_order_seed`). BE không đổi.
Đang làm dở: (không)
Bước tiếp theo: user verify — vào Báo cáo nhu cầu mua, tick "Chỉ mã chưa có HĐ mua", chọn mã, bấm "Lập đơn mua" → sang form DMH có sẵn hàng. Rồi commit FE.
Blocked:

### Checkpoint — 2026-07-31 (Task 27)
Vừa hoàn thành: Cột "Mục đích mua" — phần HĐ bán đổi từ số HĐ sang MÃ HĐ (contracts.code) + click mở popup chi tiết HĐ bán.
- BE `productInfo`: thêm `contract_code` (mã thật, pluck từ contracts) vào map product-info (DMH riêng — không đụng `purchaseDemand` dùng chung). Đơn đã lưu (order #7) cũng hiển thị mã đúng vì mã resolve từ contract_id qua endpoint này.
- BE mới `saleContractInfo` + route `GET .../sale-contracts/{contract}`: header + products đọc thẳng contracts/contract_products (join units), không dùng ContractDetailResource nặng. php -l OK.
- FE mới `ContractDetailModal.vue` + wiring `ProductsTab.vue` (saleContractCode + openContract + link tím + nhúng modal).
Đang làm dở: (không)
Bước tiếp theo: user tự verify UI (click mã HĐ ở cột Mục đích mua → popup) + commit BE+FE. Có thể chạy Playwright kiểm chứng nếu cần.
Blocked:

### Checkpoint — 2026-07-31 (Task 26)
Vừa hoàn thành: Click mã phiếu DXCU + PXL → mở popup chi tiết (cả popup "Chọn hàng hóa" lẫn bảng hàng hóa cột Mục đích mua).
- FE mới `SupplyDocDetailModal.vue`: b-modal xl, props kind('proposal'|'handling')+docId+docCode; fetch on show từ `supply/supply-proposals/{id}` hoặc `supply/supply-handlings/{id}`; header `dd-grid` 3 cột (proposal: số ĐX/loại/trạng thái/KH/mục đích/KH sử dụng/người ĐX/ngày giao/nội dung; handling: số PXL/loại/trạng thái/KH/người lập/ngày lập/ngày duyệt/phiếu ĐX/ghi chú) + bảng hàng hóa (STT/mã nội bộ/tên/ĐVT/SL đề xuất|đặt đơn/SL đi mua).
- FE `GoodsPickerModal.vue`: purpose thêm `proposal_id`/`handling_id` (từ demand lines BE sẵn có); candidate thêm `proposalId`/`handlingId`; DXCU+PXL trong cột "Phiếu đề xuất / xử lý" thành `<a>` `@click.stop.prevent="openDoc(...)"`; nhúng SupplyDocDetailModal + state docVisible/docKind/docId/docCode.
- FE `ProductsTab.vue`: sub-line Mục đích mua — DXCU + PXL thành link (chỉ khi có id) mở SupplyDocDetailModal; nhúng modal + openDoc; style `.pp-doc-link`/`.pp-doc-link-handling`.
- BE KHÔNG đổi: tái dùng show endpoint sẵn có; purposes JSON persist proposal_id/handling_id (json_encode nguyên mảng — không migration).
Đang làm dở: (không)
Bước tiếp theo: user tự verify UI (Tasks 22-26) + commit FE. Có thể chạy Playwright kiểm chứng nếu cần.
Blocked:

### Checkpoint — 2026-07-30 (Task 18)
Vừa hoàn thành: Tách điều khoản thanh toán thành tab thứ 3 (Thông tin chung · Hàng hóa · Điều khoản thanh toán). Component mới `PaymentTab.vue` giữ nguyên logic 2 chiều; GeneralTab gọn lại 3 khối đầu; Form thêm tab + wire props. Data flow không đổi (progressRows/payTerms/totalAmount vẫn ở Form, truyền xuống PaymentTab).
Đang làm dở: (không)
Bước tiếp theo: user tự verify UI 3 tab + commit FE.
Blocked:

### Checkpoint — 2026-07-30 (Task 17)
Vừa hoàn thành: Thanh toán "Theo đợt" nhập 2 chiều tỉ lệ↔số tiền giống HĐ bán.
- `GeneralTab.vue`: cột Số tiền dùng `currency-input` (sửa được), ô Tỷ lệ dùng `base-input-field type=number`, nút thêm `base-add-button`, cảnh báo khi tổng≠100%. Logic copy PaymentBlockCard: `calcAmount/calcPercent/otherAmount/maxAmount/onRowInput/rebalancePercents` (số tiền là gốc, dồn lẻ vào đợt cuối). watch `totalAmount`+`created` để cân lại %.
- `PurchaseOrderForm.vue`: applyInitial suy `amount = pct×totalAmount` khi nạp (products set trước progress nên totalAmount sẵn sàng); dòng mặc định +`amount:null`. buildPayload vẫn gửi `pct`.
- BE không đổi: `purchase_order_progress` chỉ có cột pct (giống HĐ mua/bán) → amount là giá trị UI dẫn xuất.
Đang làm dở: (không)
Bước tiếp theo: user tự verify UI + commit FE.
Blocked:

### Checkpoint — 2026-07-30 (Task 15)
Vừa hoàn thành: Popup chọn hàng chỉ còn nguồn Báo cáo nhu cầu mua (bỏ catalog danh mục chung). Verify BE (demand=9/catalog=0) + FE (9 hàng, bỏ filter Nguồn, chọn+thêm OK).
Đang làm dở: (không)
Bước tiếp theo: chờ user tự commit BE+FE.
Blocked:

## Checkpoint
### Checkpoint — 2026-07-30 (HOÀN TẤT 14/14 task)
Vừa hoàn thành: Task 14 — E2E acceptance qua Playwright (Claude lái). Đã verify toàn bộ vòng đời:
- Menu "Đơn mua hàng" nằm cạnh "Hợp đồng mua" ✓; list + API 200 ✓
- Lập đơn: next-code DMH-2026-####, validate FE, tab Hàng hóa + <Required/>, GoodsPicker (3180 hàng) + saleCompany ✓
- buyer_company_id bắt buộc → 422 ✓; tạo Nháp/Chờ duyệt ✓; Duyệt→3 ✓; Từ chối→4 + lý do ✓; Sửa (total tính lại) ✓; Xóa Nháp→200, xóa đã duyệt→400 ✓
- UTF-8 tiếng Việt lưu đúng ✓; màn chi tiết read-only đầy đủ ✓; regression HĐ mua → 200 ✓
Fix nhỏ trong lúc verify: thêm `:disabled="readonly"` cho 3 input native (SL mua/Đơn giá/Ghi chú) ở ProductsTab — trước đó chỉ khóa bằng CSS pointer-events, Tab+gõ được (dù không lưu được). Nay read-only trọn vẹn.
Đang làm dở: (không)
Bước tiếp theo: Feature hoàn tất — chờ user review UI cuối + tự commit (không auto-commit theo quy tắc). Dữ liệu test đã dọn sạch (remaining=0).
Blocked:

- [x] Task 37 — Fix mất cột "Trạng thái" ở danh sách đơn (2026-08-03, @khoipv)
  - Nguyên nhân: index.vue tự chế `<span class="badge status-badge" :class="badge-soft-${status_color}">`. Với đơn Nháp (status_color='secondary'), `badge-soft-secondary` cho nền + chữ xám nhạt gần trắng → chữ "Nháp" chìm, nhìn như trống. Đơn "Đã duyệt" (success=xanh) vẫn thấy. BE trả đúng (status=1, name='Nháp', color='secondary' — đã verify bằng Resource + DB).
  - Sửa: dùng `<b-badge :variant="item.status_color">{{ item.status_name }}</b-badge>` giống hệt màn HĐ mua (purchase_contracts/index.vue:122) → đồng bộ toàn hệ thống, mọi trạng thái luôn hiện rõ. Xóa style `.status-badge` không còn dùng.

- [x] Task 38 — Canh đều dấu "—" 4 cột tham chiếu (Đơn giá báo giá / Ghi chú báo giá / Ghi chú thầu / Ghi chú hợp đồng) ở ProductsTab (2026-08-03, @khoipv)
  - Trước: cột Đơn giá báo giá `td.num` (text-align:right → dấu dạt phải), 3 cột ghi chú text-align:left + min/max-width + pre-line (dấu dạt trái) → nhìn cái cao cái thấp, lệch hàng.
  - Sửa: `.ref-none` thành `display:block; width:100%; text-align:center` → dấu "—" cả 4 cột căn giữa ngang; `td vertical-align:middle` sẵn có lo giữa dọc → 4 dấu thẳng hàng.

- [x] Task 38b — Canh đều dấu "—" (lần 2, dứt điểm) 4 cột tham chiếu ở ProductsTab (2026-08-03, @khoipv)
  - Task 38 (chỉ sửa .ref-none) không đủ: dấu "—" trong ảnh nằm ở nhánh `v-if` (.ref-line, giá trị refPrice/refNote='—'), không phải .ref-none. Cột Đơn giá báo giá còn `td.num` (text-align:right) → dấu dạt phải, lệch với 3 cột ghi chú căn trái.
  - Sửa: bỏ class `num` ở cả `<th>` lẫn `<td>` cột "Đơn giá báo giá" → 4 cột tham chiếu đều căn trái, cùng .ref-line (line-height 1.5) + td vertical-align:middle → dấu "—" thẳng hàng ngang + dọc. `.ref-none` đổi về căn trái + line-height:1.5 cho khớp .ref-line.

- [x] Task 38c — Canh giữa DỌC nội dung 4 cột tham chiếu bằng flex wrapper (2026-08-03, @khoipv)
  - Gốc rễ: các `.ref-line`/`.ref-none` là block con của td → `td vertical-align:middle` KHÔNG middle được block con (chỉ áp inline/table-cell). Dòng cao thấp khác nhau → dấu "—" dính top, lệch giữa các dòng.
  - Sửa: bọc nội dung mỗi ô 4 cột vào `<div class="ref-wrap">` (flex-column, justify-center, height:100%) → nội dung căn giữa dọc thật theo chiều cao ô. Dấu "—" / dòng ref-line 4 cột thẳng hàng ngang (đều căn trái từ 38b) + dọc.

- [x] Task 38d — Hack height:1px cho td.cell-ref để .ref-wrap flex căn giữa dọc ăn thật (2026-08-03, @khoipv)
  - 38c thêm .ref-wrap{height:100%} nhưng KHÔNG ăn: trong <td>, height:100% của con = auto vì td không có chiều cao xác định → nội dung vẫn dính top.
  - Sửa: `td.cell-ref { height: 1px }` làm "mồi" (trình duyệt coi là min-height, ô vẫn cao theo nội dung) → .ref-wrap{height:100%} giãn full ô → justify-content:center căn giữa dọc thật. Kỹ thuật chuẩn cho vertical-center trong table cell.

- [x] Task 38e — Căn giữa dọc bằng inline-block + vertical-align:middle (bỏ flex/height hack) (2026-08-03, @khoipv)
  - 38d (height:1px + flex height:100%) vẫn KHÔNG ăn trong b-table sticky (border-collapse:separate) → cột Đơn giá báo giá vẫn cao hơn.
  - Sửa dứt điểm: `td.cell-ref { vertical-align:middle; text-align:center }` + `.ref-wrap { display:inline-block; vertical-align:middle; text-align:left }`. Cơ chế căn giữa dọc CHUẨN cho table cell (không phụ thuộc height:100% vốn không hoạt động trong td). Khối nội dung được td căn giữa cả dọc lẫn ngang; text bên trong vẫn trái. 4 cột thẳng hàng.

- [x] Task 38f — ROOT CAUSE THẬT của dấu "—" lệch cao (systematic-debugging, có repro đo pixel) (2026-08-03, @khoipv)
  - 38a–38e đều fix CĂN GIỮA nhưng gốc rễ là NỘI DUNG 2 Ô KHÔNG CAO BẰNG NHAU: Vue compiler của Nuxt (không set `whitespace` → mặc định preserve) giữ nguyên newline template quanh `{{ refNote(...) }}` → text node trong `.ref-line` là `"\n    —\n"`. 3 cột ghi chú có `td white-space: pre-line` → newline render thành DÒNG TRỐNG trên dấu "—" (ô cao 2 dòng, dấu nằm dòng dưới); cột Đơn giá báo giá `nowrap` → 1 dòng căn giữa → dấu "—" cao hơn. Đã chứng minh bằng chính `vue-template-compiler` của client (render fn chứa `_v("\n  "+_s(refNote...)+"\n ")`) + repro HTML đo Playwright: bug ref-line 35px vs 17px, sau fix cả hai 17px cùng vị trí.
  - Sửa `ProductsTab.vue`: (1) template — bao sát giá trị 3 cột ghi chú bằng `<span class="ref-val">{{ refNote(...) }}</span>` (mustache dính liền tag, không newline trong span); (2) CSS — `td.cell-ref-note` đổi `pre-line → normal` (newline template collapse thành space, vẫn wrap trong max-width 240px), thêm `.ref-val { white-space: pre-line }` → newline THẬT trong dữ liệu ghi chú vẫn xuống dòng (verify repro: ghi chú 2 dòng vẫn 2 dòng). Nhánh rỗng `.ref-none` không đổi. Compile template 0 errors.
