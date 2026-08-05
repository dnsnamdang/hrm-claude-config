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
