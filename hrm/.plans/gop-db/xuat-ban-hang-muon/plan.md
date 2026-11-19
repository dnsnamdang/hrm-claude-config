# Plan — Xuất bán hàng mượn (gop_db)

> Placeholder — task cụ thể sẽ fill sau khi brainstorming xong Phase 1.

## Phase 1 — Phiếu YC xuất bán hàng mượn (BorrowSellRequest)
- [x] Brainstorming + chốt design Phase 1
- [x] Viết spec chi tiết `docs/superpowers/specs/gop-db/2026-08-28-xuat-ban-hang-muon-phase1-design.md`
- [x] User review spec
- [x] writing-plans → `docs/superpowers/plans/2026-09-03-xuat-ban-hang-muon-phase1.md` (13 task: T1 seeder quyền, T2-3 entity + hợp nhất type-9, T4 calculator+unit test, T5 source service, T6 service store/duyệt/notify, T7 formrequest, T8 controller+resource+route, T9-12 FE, T13 QA)
- [~] Execute plan (SDD — subagent-driven, ledger: `.plans/gop-db/xuat-ban-hang-muon/sdd/progress.md`)
  - [x] T1–T8 BE (seeder quyền, entity, calculator+unit test, source service, service store/duyệt/notify, formrequest, controller+resource+route) — review sạch
  - [x] T9 FE api.js, T10 FE list `index.vue` — done
  - [x] T11a BE (2 endpoint nguồn: `GET export-requests` list phẳng, `GET export-requests/{id}`; siết `canBorrowSell`) — review SPEC✅/QUALITY APPROVED; fix round R-T11a-FIX-1 xong
  - [x] **T11b FE create page** — `create.vue` + `ContractPickerModal` + `ExportRequestPickerModal` + `BorrowSellRequestForm` — review SPEC PASS / QUALITY APPROVED (no load-bearing defects)
  - [x] T12 FE detail + print + deny/history modal — `_id/index.vue` + `_id/print.vue` + `BorrowSellRequestHistoryModal` + api.js `histories` — review SPEC PASS / QUALITY APPROVED
  - [x] T13 QA: unit test Calculator PASS (3 test/9 assert); doc update. **QA UI theo cấp quyền + type-9 regression = CẦN USER chạy trên browser** (không tự động hoá headless được)
  - [x] Review tổng nhánh (broad whole-branch, model mạnh) — verdict BLOCK: 1 defect D1 (escalation vượt hạn mức không kích hoạt)
  - [x] **Fix D1** — BE tự tính giá trị phiếu server-side (`computeAmounts()`) → `isOverLimit(int,float)` + persist 6 cột `sum_amount_*`; scoped re-review PASS. **FINAL REVIEW CLEAN.**
- [ ] (chưa) commit — chờ user yêu cầu

### Checkpoint — 2026-09-04 (b) — Final review clean
Vừa hoàn thành: **review tổng nhánh + fix D1**. Review tổng verdict BLOCK vì 1 defect load-bearing (D1: escalation vượt hạn mức không kích hoạt — `isOverLimit` đọc `sum_amount_after_extra_after_vat` từ request input mà FE không gửi → luôn 0). Fix: BE tự tính giá trị phiếu server-side (`computeAmounts()` port công thức ERP `BorrowSellRequestProduct`), truyền vào `isOverLimit(int,float)`, đồng thời persist 6 cột `sum_amount_*` (trước NULL). Scoped re-review PASS, no findings. **FINAL REVIEW CLEAN — toàn bộ code Phase 1 xong.**
Đang làm dở: (không) — chờ USER QA browser + quyết định commit.
Bước tiếp theo: (1) **USER QA trên browser** (checklist bên dưới); (2) hỏi user có commit không → nếu có: `finishing-a-development-branch`.
Blocked: (không).

### Checkpoint — 2026-09-04 (a)
Vừa hoàn thành: **toàn bộ code Phase 1** — T11a fix round (R-T11a-FIX-1) + T11b (FE create page) + T12 (FE detail/print/deny/history) + T13 (unit test Calculator PASS, doc update). Mọi task đều review SPEC PASS / QUALITY APPROVED, KHÔNG load-bearing defect. CHƯA commit (chờ user).
Đang làm dở: review tổng nhánh (broad whole-branch, model mạnh) đang chạy nền.
Bước tiếp theo: (1) nhận verdict review tổng → xử findings nếu có; (2) **USER QA trên browser**: đăng nhập từng cấp quyền tạo phiếu Firm/WrService/HĐ mới, vượt/không vượt hạn mức (TP→BGD), duyệt/từ chối, in, + xác nhận `account_details`/tồn KHÔNG đổi + regression type-9 (Nhập bán mượn trả lại); (3) hỏi user có commit không.
Cần lưu ý khi surface cuối: middleware gate qua canX (không checkPermission); fix bug escalation ERP; harden fail-closed (luôn chạy over-limit check); siết canBorrowSell; R-T11a-FIX-1 (list nguồn không scope HĐ, khớp ERP); R-T11b-FIX-2 (loadFirm default-all-tabs); R-T11b-3 (tabs[] deferred); R-T11b-4 (form create không dùng directive v-validate — không có trường Tên); R-T12-1 (histories stub []).
Blocked: (không) — chờ review tổng + QA user.

### Checkpoint — 2026-09-03 (đã qua)
Vừa hoàn thành: T11a (BE 2 endpoint nguồn + siết canBorrowSell), review sạch, KHÔNG commit (đúng ruling SDD).
Đã điều tra + giải quyết BLOCKER bằng ground-truth ERP (Explore đã xong, ghi trong ledger).
**Kết luận (đối chiếu code ERP borrow-sell):**
- ERP list phiếu nguồn **KHÔNG lọc theo HĐ** — chỉ self + type=3(XUAT_MUON) + status=5 + borrow_status=2(DA_MUON).
  HĐ khớp lúc LƯU, theo từng dòng sản phẩm (FirmContractTabProduct / WrServiceContractItem).
- `dataForBorrowSell` + `canBorrowSell` (4 đk AND) của T11a **khớp ERP → đúng**.
- **Defect T11a**: `searchExportRequests` lọc thừa `firm_contract_id|wr_service_contract_id` (ERP không có) →
  trả rỗng trên DB gộp (cột contract NULL). → Ruling R-T11a-FIX-1: bỏ filter + param contract, list phẳng,
  đổi route `GET /export-requests`.
Việc đầu tiên MAI (chi tiết ở ledger sdd/progress.md):
  1. Fix round T11a: sửa `searchExportRequests` (bỏ contract filter/param) + route `/export-requests` +
     rename controller `myExportRequests`; re-review scoped. KHÔNG đụng dataForBorrowSell/canBorrowSell.
  2. Thiết kế lại T11b theo linkage đúng (ContractPicker=header HĐ; ExportRequestPicker=list phẳng phiếu
     xuất mượn của user) → lưu `sdd/t11b-create-design.md` + `task-11b-brief.md` → dispatch implementer dựng
     create.vue + 2 picker modal + BorrowSellRequestForm + api.js (getExportRequests bỏ contractId, getExportRequestData).
  3. T12 (detail+print+deny/history), T13 (QA + review tổng nhánh).
Blocked: (không còn) — sẵn sàng vào fix round T11a rồi T11b.

### Task T11b-PARITY — Bảng "Chi tiết số lượng bán" đầy đủ như ERP (Hàng hóa tab)
User chốt (2026-09-05): port màn phải **đầy đủ giống ERP**, cấm rút gọn (memory `erp-port-must-match-full-not-simplified`). Bảng chi tiết hiện là grid phẳng 8 cột → dựng lại thành bảng lồng 2 cấp khớp tab "Hàng hóa" của `warehouse/borrow_sell_requests/form.blade.php`.
- [x] Sửa ô "SL bán" quá bé (nới cột + class `.qty-input`).
- [x] Refactor Section 3 `BorrowSellRequestForm.vue`: `gridRows` phẳng → `productGroups` gom theo SP-của-HĐ.
- [x] 17 cột: STT | Tên hàng hóa (tên+Model+Mã+Thương hiệu) | ĐVT(+hệ số) | SL[HĐ/Đã xuất/Bán mượn] | Chi tiết[Phiếu mượn/Đang mượn/Bán(input)] | Giá niêm yết | (Chiết khấu — chỉ WrService) | Đơn giá bán | Thành tiền | Đơn giá sau giảm | Thành tiền sau giảm | VAT | Thành tiền sau VAT.
- [x] Computed money getter khớp công thức class ERP (`borrow_sell_qty`=Σ detail.qty; price/price_after_extra/total_amount_after_extra/discount_price(Math.round)/total_amount_allocated/vat_cost/total_amount_allocated_after_vat) + 5 dòng tổng (Tổng tiền bán/Tổng giảm giá/Tổng trước thuế/Tiền VAT/Tổng sau thuế) + dòng Chiết khấu khi >0.
- [x] `buildPayload` gom theo `productGroups` (không đổi contract BE — `borrow_sell_qty`=Σ qty, tiền tính FE).
- [ ] User QA trên browser: tạo phiếu Firm + WrService, đối chiếu cột/tiền/tổng với ERP.

### Task T11b-UI — Đưa 5 dòng tổng ra "box tổng" ngoài bảng (2026-09-05)
User: 5 dòng tổng (Tổng tiền bán/giảm giá/trước thuế/VAT/sau thuế + Chiết khấu) đang là `<tr>` trong bảng cuộn ngang → xấu, kẹt. Redesign đưa ra ngoài thành box tổng đẹp giống màn Yêu cầu xuất hàng (`ProductExportRequestForm.vue` — `.pay-box`).
- [x] Bỏ block `<template v-if="productGroups.length">` 6 dòng tổng khỏi `<tbody>` `BorrowSellRequestForm.vue`.
- [x] Thêm `.pay-box` sau `</V2BaseTableScroll>`: 5 dòng tổng + dòng Chiết khấu (v-if `formRebatePrice > 0`), dòng "Tổng tiền sau thuế" class `pay-row--total`; dùng lại getter `sumAmountAfterExtra/saleInvoice/sumAmountAllocated/sumAmountAllocatedVat/sumAmountAllocatedAfterVat/formRebatePrice`.
- [x] Copy CSS `.pay-box/.pay-row/.pay-row--total` từ YCXH; dọn `labelColspan` computed + CSS `.bsr-total-row` (chỉ dùng cho dòng tổng cũ).
- [ ] User QA: box tổng hiện ngoài bảng, số khớp, dòng Chiết khấu chỉ hiện với HĐ dịch vụ.

### Task T11b-UI2 — Footer cố định giống Yêu cầu xuất hàng (2026-09-05)
User: footer đang là thanh trôi (`.v2-form-footer`) → đổi sang thanh hành động **cố định đáy màn** giống YCXH.
- [x] Thay `.v2-form-footer` → `.export-actionbar` (bê nguyên markup + CSS từ `ProductExportRequestForm.vue`): `position: fixed`, full-width, border-top, shadow, padding-left 80px chừa sidebar, `__hint` trái + `__btns` phải, responsive 1366px.
- [x] Root form thêm `min-vh-100` + `padding-bottom: 72px` để card cuối không bị thanh che.
- [x] Nút giữ thứ tự theo skill button-convention form page: **Lưu (primary) → Quay lại (light)**; icon Quay lại đổi `ri-arrow-left-line`; giữ `:interactable="canSubmit && !saving"` trên nút Lưu.
- [ ] User QA: thanh dính đáy khi cuộn, không che nội dung, nút Lưu vẫn khoá đúng điều kiện.

### Task T11b-UI3 — Bỏ dòng gợi ý "Nhấn vào một dòng để chọn hợp đồng" (2026-09-05)
User: dòng gợi ý `↖ Nhấn vào một dòng để chọn hợp đồng` trong modal chọn HĐ thừa → bỏ.
- [x] Xoá block `<div class="cp-hint">...</div>` (template) + CSS `.cp-hint` không còn dùng trong `ContractPickerModal.vue`.
- [ ] User QA: modal chọn HĐ không còn dòng gợi ý, click hàng vẫn chọn được HĐ.

### Task T11b-UI4 — Dựng lại màn CHI TIẾT khớp ERP + CSS như Yêu cầu xuất hàng (2026-09-05)
User: màn chi tiết `_id/index.vue` đang rút gọn (3 card `form-card` + bảng phẳng 8 cột) → thiếu nhiều thông tin so với ERP. Yêu cầu: xem ERP `warehouse/borrow_sell_requests/show.blade.php` có gì → sắp xếp lại + CSS giống màn Yêu cầu xuất hàng (`product-export-requests/_id/index.vue`: `.c-section`/`.kv-grid`/`.subpanel`/`.er-table`/`.pay-box`/`.export-actionbar`).
- [x] BE: mở rộng `BorrowSellRequestDetailResource` — thêm cột giá/tiền SP (`price, extra_price, allocated_price, rebate_price, net_price, returned_qty, exported_qty`), detail `product_export_request_code`, top-level `customer_code, customer_tax_code, department_name, need_repair, has_rebate_price, source_export_requests[]`. `exported_qty` đọc từ objectable (`firm_contract_tab_products`/`wr_service_contract_items`), code phiếu nguồn + KH + phòng ban join bảng gộp.
- [x] FE: viết lại `_id/index.vue` theo layout YCXH — card Thông tin chung (kv-grid: mã/loại/HĐ/trạng thái/người lập/ngày lập/ngày duyệt/cần lắp đặt/phòng ban + chips Phiếu xuất mượn + Ghi chú + Lý do từ chối) + subpanel Khách hàng (mã KH/tên/CMT-MST/ĐT/địa chỉ/liên hệ) + bảng hàng hoá lồng 2 cấp (SL: Hợp đồng/Đã xuất kho/Bán hàng mượn/Được duyệt; Chi tiết: Phiếu mượn/Bán/Được duyệt; cụm giá: Giá niêm yết/Chiết khấu(WrService)/Đơn giá bán/Thành tiền/Đơn giá sau giảm/Thành tiền sau giảm/VAT/Thành tiền sau VAT) + `.pay-box` 5 dòng tổng + Chiết khấu + `.export-actionbar` giữ nút Từ chối/TP duyệt/Chuyển BGD/BGD duyệt/In/Lịch sử/Quay lại (gated is_can_*). Công thức tiền copy đúng getter form.
- [ ] User QA: đối chiếu cột/tiền/tổng/nhóm-theo-tab với ERP; kiểm nút duyệt/từ chối/in/lịch sử hoạt động.

## Phase 2 — Phiếu xuất bán hàng mượn thực tế (BorrowSell / PXBHM) + hạch toán
- [x] Brainstorming + chốt design Phase 2 (scope hạch toán đầy đủ; 4 màn; quyền: list 4 cấp 100315-318 / view is_can_view / lập "Kế toán kho" 100080 / không edit-delete-approve; Hướng A tách trait; giữ accountingDeliveryTrip; bỏ nhánh KM; loại HĐ suy từ contractable_type)
- [x] Viết spec chi tiết `docs/superpowers/specs/gop-db/2026-09-07-xuat-ban-hang-muon-phase2-design.md`
- [x] writing-plans → `docs/superpowers/plans/2026-09-07-xuat-ban-hang-muon-phase2.md` (14 task)
- [ ] Execute plan (SDD — subagent-driven). Ledger: `.plans/gop-db/xuat-ban-hang-muon/sdd/progress.md`
  - [ ] T1 6 entity `BorrowSell*`
  - [ ] T2 entity `ActivityHasDeliveryTrip` (verify/tạo nếu thiếu)
  - [ ] T3 tách `SupportAccountingTrait` từ `ProductExportPostingService` (Hướng A — có regression test)
  - [ ] T4 `BorrowSellPostingService` nhánh Firm (giá vốn TK157)
  - [ ] T5 `BorrowSellPostingService` nhánh WrService (giá vốn TK1561×hệ số + chiết khấu 5211)
  - [ ] T6 `accountingDeliveryTrip` (chuyến xe 6427/3351 + CostDebt TVC)
  - [ ] T7 `BorrowSellService::store` (tạo + cập nhật SL atomic + hạch toán + duyệt phiếu YC cha DA_DUYET)
  - [ ] T8 `StoreBorrowSellRequest` FormRequest
  - [ ] T9 `BorrowSellController` + 3 Resource (Detail có tab Hạch toán) + routes (checkPermission Kế toán kho)
  - [ ] T10 FE store actions + nút "Lập phiếu bán" trên chi tiết phiếu YC
  - [ ] T11 FE list `index.vue` (gate 4 cấp quyền)
  - [ ] T12 FE `create.vue`
  - [ ] T13 FE `_id/index.vue` (tab Hạch toán) + `_id/print.vue` (mẫu XUAT_BAN_HANG_MUON)
  - [ ] T14 QA tích hợp (V1-V8: Nợ=Có, giá vốn nhánh, chiết khấu, SL atomic, duyệt cha, regression xuất thường, quyền, chuyến xe)

### Phase 2.1 — Bổ sung UI "thông tin chung" màn Lập phiếu bán (parity ERP)
- [ ] BE `StoreBorrowSellRequest`: thêm rule `note` (nullable|string|max:255) + `bear_the_shipping` (nullable|boolean)
- [ ] BE `BorrowSellRequestDetailResource`: thêm khối `accounts` (định khoản hiển thị, kho động 157 Firm / 1561 WrService)
- [ ] FE `BorrowSellForm.vue`: mở rộng Section 1 read-only (Người yêu cầu, Phòng yêu cầu, Phiếu xuất mượn chips, Địa chỉ giao hàng) + khối định khoản + input Ghi chú + checkbox "KD chịu vận chuyển"; payload gửi kèm note/bear_the_shipping; snapshot unsaved

### Phase 2.2 — Fix ô "SL bán" luôn = 0 (bug qty)
- Gốc rễ: `loadRequest()` lấy `d.approved_qty` (Phase 1 set cứng 0, không populate lại) làm default + max → mọi phiếu hiện 0. ERP lấy `d.qty` của dòng chi tiết.
- [ ] FE `BorrowSellForm.vue` `loadRequest()`: default + max ô "SL bán" lấy `d.qty` thay cho `d.approved_qty` (BE `store` vẫn hard-validate tồn/returning_qty thật)
- [ ] TODO (tab — bàn sau): port UI tab từ ERP cho phiếu YC firm CÓ tab (form lập phiếu bán hiện render phẳng, chưa có UI tab)

### Phase 2.3 — Bảng "Bút toán hạch toán" (màn chi tiết) parity ERP 100%
- Hiện thiếu cột Tên TK, có dòng value 0 → xấu hơn ERP.
- [ ] BE `BorrowSellDetailResource::enrichAccounting()`: lọc bỏ vế `intval(value)<=0` (khớp saveAccountDetail) + enrich mỗi dòng: `name` (accounts.identify_number→name), `object_code/object_name` (customer→employee→product theo thứ tự ERP show.blade), `work_code/work_name` (works). Gom id theo loại (tránh N+1).
- [ ] FE `_id/index.vue`: đổi bảng bút toán sang 8 cột ERP: Tên TK | Số TK | Nợ | Có | Mã đối tượng | Tên đối tượng | Mã vụ việc | Tên vụ việc; sửa colspan dòng Tổng cộng

## Phase 3 — Hỗ trợ HĐ HRM (`hrm_contracts`) cho borrow-sell
Spec: `docs/superpowers/specs/gop-db/2026-09-07-xuat-ban-hang-muon-phase3-hrm-contract-design.md`
Port đối xứng nhánh Firm; nhánh contractable_type thứ 3 `CONTRACT_HRM = Modules\Assign\Entities\Contract\Contract`.
- [x] Brainstorming + chốt design Phase 3 (Q1 port firm / Q2 Cách A thêm cột / Q3 Cách 1 nhóm=đợt)
- [x] Viết spec chi tiết + tóm tắt design.md
- [x] Execute plan (SDD — ledger scratchpad `sdd-phase3/progress.md`). Task thực thi (đặt tên lại U1-U7+U5b):
  - [x] T1 migration: thêm `exported_qty` + `returned_qty` vào `hrm_contract_product_prices` (guard hasColumn)
  - [x] T2 hằng số: `CONTRACT_HRM` (BorrowSellRequest + BorrowSell), `OBJECTABLE_HRM`, `type=3`, `$typeNames` các Resource
  - [x] T3 BE `loadContract`/searchContracts: nhánh HRM `hrm_contracts` (type_name 'HĐ HRM')
  - [x] T4 BE store: nhánh `$isHrm` khớp `hrm_contract_product_prices` theo `erp_product_id`; objectable HRM; SL `qty_needed`
  - [x] T5 BE source service: `loadHrm()` dựng grid nguồn từ `hrm_contract_product_prices`; còn lại = qty_needed − exported_qty − in-flight; money map R5 (price=allocated=quoted, extra=rebate=0)
  - [x] T6 BE FormRequest + `loadContract` nhánh HRM (eligibility yêu cầu has_support_accounting như Firm/WrService)
  - [x] T7 BE ghi ngược (`BorrowSellService`): `$objectableTable` 3-way map OBJECTABLE_HRM → `hrm_contract_product_prices` (increment ATOMIC); guard cấp-2 chỉ WrService
  - [x] T8 BE posting (`BorrowSellPostingService`): nhánh CONTRACT_HRM tái dùng `firmBranch()` + `resolveContract` (Contract::find thật, KHÔNG shim; gắn SupportAccounting scope CONTRACT_HRM). Giá vốn 157
  - [x] T8b (U5b+R12b) 6 Resource: `$isHrm`/`$isFirmLike`/3-way `$table`/contract_type='hrm'/has_rebate_price=!isFirmLike/kho 157 (gồm cả BorrowSellPrintResource + buildExportedQtyMap OBJECTABLE_HRM)
  - [x] T9 FE `ContractPickerModal`: nút lọc "HĐ HRM" (type=3)
  - [x] T10 FE `BorrowSellRequestForm`: computed `isHrm`/`isFirmLike`; 4 site `!isFirm`→`!isFirmLike`; strict isFirm giữ (tabs/firm_tab_ids). **Lệch spec (R11): phase này KHÔNG có group-picker, FE render phẳng, KHÔNG gửi `hrm_group_ids` (loadHrm nhận `$groupIds=[]` — provision sẵn cho sau)**
  - [x] T11 FE Phase 2 (`BorrowSellForm` không đổi + `_id/index.vue` contractTypeLabel thêm key 'hrm')
  - [ ] T12 QA (user chạy trình duyệt): xem checklist bên dưới
- [x] Final whole-branch review (model mạnh): tìm **1 blocker** (R5 money map đứt ở `BorrowSellService::store` do dùng strict `$isFirm` → HRM doanh thu=0, mất công nợ 1311) + 1 minor (buildExportedQtyMap thiếu HRM) → **đã fix + scoped re-review RESOLVED**. Minor `returned_qty` dead column giữ chủ đích (R14).

### Checkpoint — 2026-09-07
Vừa hoàn thành: toàn bộ code Phase 3 (BE+FE) + final review; 1 blocker tài chính đã phát hiện và sửa (đối xứng Phase 1 `computeAmounts($request,$firmLike)`), verify RESOLVED.
Đang làm dở: (không)
Bước tiếp theo: **user QA T12 trên trình duyệt** (đặc biệt V-tiền: lập phiếu bán từ HĐ HRM → kiểm Nợ=Có, có đủ doanh thu 5111 + công nợ 1311 + giá vốn 632/157, tổng tiền màn chi tiết ≠ 0); sau khi QA đạt → user quyết định commit.
Blocked: chờ user QA + lệnh commit

- [ ] (chưa) commit — chờ user yêu cầu

## Phase 4 — Sửa chức năng IN phiếu xuất bán hàng mượn (parity màn `prepick-cancels`)
Bối cảnh: màn `finance/borrow-sells` đang IN theo kiến trúc cũ (trang `/print` riêng + JSON resource + `$printPreview(:src)` iframe) → 3 lỗi: (1) nút "In" thiếu ở cột Hành động màn danh sách; (2) màn chi tiết bấm In không ra popup như các màn khác; (3) bản in `/borrow-sells/4312/print` font/căn chỉnh xấu vì không dùng CSS in dùng chung. Mẫu chuẩn: `finance/prepick-cancels` (BE render HTML blade qua `_layout` → `responseJson(['template'=>$html])`; FE `reportPrintPreviewMixin.openPrintDetail` + `ReportPrintPreviewModal`). Approach A (user chốt): tái dùng template/layout/CSS/font chung của prepick-cancels, chỉ khác nội dung bảng hàng.
- [x] BE blade `Modules/Finance/Resources/views/prints/borrow-sell.blade.php` (include `finance::prints._layout`; bảng: STT, Mã SP, Tên sản phẩm, Model, ĐVT, Số lượng, Đơn giá, Thành tiền + Tổng thành tiền; signers `['Người lập phiếu','Trưởng phòng','Ban giám đốc']`)
- [x] BE `BorrowSellService::renderPrint(BorrowSell $object): string` (dùng trait `ResolvesCompanyLetterhead::letterheadUrl($object->borrowSellRequest->company_id)`; reuse `numText`/`contractCodeOf`; infoRows mirror `BorrowSellPrintResource`)
- [x] BE `BorrowSellController::printData` → `responseJson('', 200, ['template' => renderPrint(...)])`; `with()` thêm `borrowSellRequest` + `employee_create.info`; bỏ import `BorrowSellPrintResource`
- [x] FE `borrow-sells/index.vue`: thêm row action `print` + nhánh handler; đăng ký `reportPrintPreviewMixin` + `ReportPrintPreviewModal`
- [x] FE `borrow-sells/_id/index.vue`: `printPage()` → `openPrintDetail('finance/borrow-sells', requestId, ...)`; đăng ký mixin + modal (giữ gate `is_can_view`)
- [x] Cleanup: xóa `_id/print.vue`, export `printData()` trong `api.js`, `BorrowSellPrintResource.php`
- [x] Test BE `BorrowSellApiTest::test_render_print_returns_html_from_shared_layout` thay test resource cũ → PHPUnit 5/5 xanh (1 skip auth như cũ)
- [x] Verify Playwright MCP (`http://127.0.0.1:3000`): nút In ở danh sách → popup OK; chi tiết In → popup như prepick-cancels OK; font/căn chỉnh = `_layout` chung (Times New Roman, viền bảng, số `155,293`/`416,618`); letterhead ẩn ở local (ERP_URL không host logo — env, không phải code — xem memory [[gopdb-print-logo-404-local-and-ycxh-creator-company-deviation]])

### Checkpoint — 2026-10-10
Vừa hoàn thành: Phase 4 (sửa IN borrow-sells parity prepick-cancels) — toàn bộ BE/FE/cleanup/test/verify xong.
Đang làm dở: không.
Bước tiếp theo: chờ user nghiệm thu; sau đó quay lại "commit và push" đợt product-import-form-rework đang hoãn.
Blocked: 

## Phase 5 — Đổi nhãn nút "Lưu" → "Lưu và gửi duyệt" (màn Tạo YCXBHM) + thêm popup xác nhận
Bối cảnh: store() của YCXBHM luôn set status 2 (Chờ kế toán kho) / 10 (Chờ TP duyệt) — tức BẤM LƯU LÀ GỬI THẲNG VÀO LUỒNG DUYỆT, không có nháp. Nút hiện ghi "Lưu" (icon `ri-save-3-line`) gây hiểu nhầm là lưu tạm. User yêu cầu đổi thành "Lưu và gửi duyệt".
Theo `button-convention`: "Lưu và gửi duyệt" thuộc nhóm "Gửi đi để duyệt" → nhãn chuẩn, màu `primary` (teal) GIỮ NGUYÊN, icon chuẩn = `ri-send-plane-line` (khớp V2Footer dòng 27-28), và BẮT BUỘC có popup xác nhận (§2b/§6c). Màn này dùng actionbar tự chế (không V2Footer) nên phải tự gọi `this.$confirm()`.
- [x] FE đổi nhãn nút "Lưu" → "Lưu và gửi duyệt", icon `ri-save-3-line` → `ri-send-plane-line` (`BorrowSellRequestForm.vue` footer)
- [x] FE thêm `this.$confirm()` đầu `save()` (title "Xác nhận lưu và gửi duyệt", textAccept "Lưu và gửi duyệt", không danger) — hỏi TRƯỚC lớp tải
- [x] Verify Playwright MCP (`http://127.0.0.1:3000/finance/borrow-sell-requests/create`, 2026-10-27): nút footer hiện đúng "Lưu và gửi duyệt" + icon `ri-send-plane-line`, màu primary teal; gọi `save()` → popup "Xác nhận lưu và gửi duyệt" / "Bạn đồng ý lưu và gửi duyệt phiếu yêu cầu xuất bán hàng mượn này?" / nút nhận "Lưu và gửi duyệt" + "Hủy"; **Hủy** → `buildPayload` KHÔNG gọi (không POST), `saving=false`, ở lại màn; **Đồng ý** → đi tiếp tới `buildPayload` (nhánh submit) — chặn POST thật bằng guard throw khi verify

### Checkpoint — 2026-10-27
Vừa hoàn thành: Phase 5 — đổi nhãn "Lưu" → "Lưu và gửi duyệt" (icon `ri-send-plane-line`) + thêm popup xác nhận `$confirm` đầu `save()`; verify Playwright 2 nhánh Hủy/Đồng ý OK.
Đang làm dở: không.
Bước tiếp theo: chờ user nghiệm thu + lệnh commit.
Blocked:

- [ ] (chưa) commit — chờ user yêu cầu

## Phase 6 — Sửa UI popup "Chọn hợp đồng" (màn Tạo YCXBHM) theo khuôn `bill-adjust-depts/create`
Bối cảnh: popup `ContractPickerModal.vue` của màn borrow-sell-requests đang tự chế (`b-modal` thô + bảng tay + nhóm nút lọc loại HĐ + live-search). User yêu cầu restyle theo popup "Chọn đơn hàng / hợp đồng" của `finance/bill-adjust-depts/create` (dùng `V2BaseModal` + hàng tìm kiếm Tìm kiếm/Làm mới + `V2BaseDataTable`), đồng thời annotation ảnh: **thêm cột Ngày tạo + thêm sort vào Số hợp đồng và Ngày tạo**.
Scope đã chốt với user (2026-10-27): (1) BỎ nhóm nút lọc loại HĐ; (2) GIỮ cột Khách hàng → cột = `STT | Số HĐ | Khách hàng | Loại HĐ | Ngày tạo`; (3) THÊM cột Ngày tạo + sort Số HĐ & Ngày tạo (cần sửa BE). Khác bill-adjust: borrow-sell KHÔNG có đối tượng chọn trước → KHÔNG hiện dòng "Đối tượng" ở header.
- [x] BE `BorrowSellRequestService::searchContracts()`: thêm `created_at` vào 3 subquery UNION + output row; nhận `sort_by` (whitelist `code`|`created_at`) + `sort_dir` (`asc`|`desc`), default type ASC → id DESC (sort có id DESC tie-break); format `created_at` kiểu `d/m/Y H:i`
- [x] FE viết lại `ContractPickerModal.vue`: vỏ `V2BaseModal` (icon `ri-file-list-3-line`, title "Chọn hợp đồng", KHÔNG subtitle); hàng tìm kiếm `V2BaseLabel` + `V2BaseInput` + nút `Tìm kiếm`(primary, `ri-search-line`) + `Làm mới`(tertiary, `ri-refresh-line`) — bấm nút/Enter mới tìm (bỏ debounce live-search); `V2BaseDataTable` cột `STT|Số HĐ|Khách hàng|Loại HĐ|Ngày tạo`, cột Số HĐ link `contract-link`, sort Số HĐ+Ngày tạo; click dòng để chọn; GIỮ hợp đồng prop `show` + emit `select`/`close` (watcher show→`$refs.modal.show/close`, `@hidden`→emit close) cho parent `BorrowSellRequestForm.vue`
- [x] Verify Playwright MCP (`http://127.0.0.1:3000/finance/borrow-sell-requests/create`, 2026-10-27): popup render đúng khuôn bill-adjust (header "Chọn hợp đồng" KHÔNG dòng "Đối tượng", hàng Tìm kiếm/Làm mới, bảng 5 cột, Số HĐ link ERP firm-contracts, Ngày tạo `28/07/2026 09:46`, phân trang 19490, KHÔNG còn nút lọc loại); sort "Ngày tạo" ASC → 02/08/2025 lên đầu OK; tìm "HOÀN HẢO" → 13 KH khớp OK (sort giữ); click dòng → đóng popup + điền mã HĐ/khách/loại OK; mở lại → reset keyword rỗng + về trang 1 + thứ tự mặc định OK

### Checkpoint — 2026-10-27 (Phase 6)
Vừa hoàn thành: Phase 6 — restyle popup chọn HĐ màn YCXBHM theo khuôn `bill-adjust-depts/create` (V2BaseModal + Tìm kiếm/Làm mới + V2BaseDataTable), bỏ nút lọc loại HĐ, thêm cột Ngày tạo + sort Số HĐ/Ngày tạo (sửa BE `searchContracts` thêm `created_at` + param sort). Verify Playwright đủ: render/sort/tìm/chọn/reset OK.
Đang làm dở: không.
Bước tiếp theo: chờ user nghiệm thu + lệnh commit (cả Phase 5 + Phase 6 chưa commit).
Blocked:

### Phase 6b — Đổi chuẩn popup sang khuôn YCXH "xuất bán hãng" (2026-10-27)

User phản hồi: "chưa đứng giao diện" → đổi chuẩn từ `bill-adjust-depts/create` sang popup **"Chọn hợp đồng hãng"** của màn Phiếu yêu cầu xuất hàng (YCXH), loại xuất bán hãng (`finance/product-export-requests/components/FirmContractSearchModal.vue`).

- [x] Viết lại `borrow-sell-requests/components/ContractPickerModal.vue` bám khuôn `FirmContractSearchModal.vue`: `b-modal` full-width (`modal-full-width-bsr-contract` 95vw/94vh), header icon tròn + "Chọn hợp đồng" + X, **2 ô lọc riêng Số hợp đồng + Khách hàng**, `b-table` `no-local-sorting` + scroll-sync trên/dưới (`utils/scrollSync`), sort icon `ri-arrow-*`, `V2BasePagination` + footer "Đóng" ghim đáy.
- [x] Cột: `STT | Ngày tạo (sort) | Số hợp đồng (sort) | Khách hàng | Loại hợp đồng`. GIỮ cột "Loại hợp đồng" vì borrow-sell đa nguồn (hãng/dịch vụ/HRM); BỎ các cột chỉ có ở HĐ hãng (Tổng thanh toán/Ngày duyệt/Người duyệt). Link Số HĐ: HĐ HRM → `nuxt-link`, HĐ hãng/dịch vụ → `<a href>` ERP (`utils/contract-link`).
- [x] Giữ hợp đồng với parent: prop `show` + emit `select`/`close` (BorrowSellRequestForm không đổi).
- [x] BE `searchContracts`: thêm param `code` + `customer` riêng (ô lọc 2 cột), giữ `keyword` fallback; dùng `$applyFilter` closure chung cho 3 subquery. `php -l` PASS.
- [x] Verify Playwright MCP (`127.0.0.1:3000/finance/borrow-sell-requests/create`, 2026-10-27): popup đúng khuôn YCXH (full-width, header icon tròn, 2 ô Số HĐ/Khách hàng, Tìm kiếm/Làm mới, bảng 5 cột sort `ri-arrow`, phân trang 19490, footer Đóng); lọc ô **Khách hàng** riêng "HOÀN HẢO" → 13 HĐ khớp; sort Ngày tạo ASC → 08/11/2025 lên đầu (server-side, giữ bộ lọc); click dòng → đóng popup + điền Số HĐ `HĐ_TPE_HN_KDTM_25_0338_0811` / KH `CÔNG TY TNHH HOÀN HẢO HT` / loại `HĐ hãng`; console chỉ lỗi socket.io môi trường.

- [ ] (chưa) commit — chờ user yêu cầu

## Phase 7 — Bổ sung đủ thông tin màn Tạo YCXBHM theo ERP (khối KH + Cần lắp đặt + lọc VAT/Nhóm hàng + bảng CONTRACT-DRIVEN)
Bối cảnh: user báo "hrm thiếu rất nhiều thông tin, k tạo được => check lại toàn bộ màn hình" (2 ảnh so ERP vs HRM). Rà soát: (1) bảng chi tiết HRM đang SOURCE-DRIVEN — rỗng cho tới khi chọn phiếu nguồn; ERP CONTRACT-DRIVEN — chọn HĐ là hiện ngay toàn bộ hàng của HĐ, phiếu nguồn chỉ bơm dòng con "đang mượn". (2) Khối "Thông tin chung" HRM thiếu: block khách hàng (Mã KH, CMT/MST, SĐT, Địa chỉ, + Người liên hệ/Điện thoại khi customer_type>1), radio "Cần lắp đặt" (need_repair), và với HĐ hãng thì "Nhóm VAT" + "Chọn nhóm hàng hóa". BE 3 loader (loadFirm/loadWrService/loadHrm) KHÔNG trả metadata khách hàng.
Scope đã chốt với user (AskUserQuestion): Q1 = "Bám ERP: hiện ngay hàng của HĐ"; Q2 = "Đủ như ERP (khối KH + Cần lắp đặt + VAT/Nhóm hàng)".
Tham chiếu ERP: `app/Services/Sale/Firm/Contract/FirmContractBorrowSellService::getDataForBorrowSell`, `resources/views/warehouse/borrow_sell_requests/{create,form}.blade.php`.
- [x] BE `BorrowSellRequestSourceService`: thêm `contractMeta($contract, $type)` trả block KH `{id, code, customer_code, customer_name, identity_card_number, customer_mobile, customer_address, customer_contact_name, customer_contact_phone, customer_type}` + (firm) `vat_percent_options` (distinct `firm_contract_tab_products.vat_percent`); include `'contract' => $meta` vào return của loadFirm/loadWrService/loadHrm. Firm `tab_options` lấy từ `tabs` trả về (id+name).
- [x] BE `StoreBorrowSellRequestRequest`: thêm rule `need_repair` nullable `in:0,1` (store() đã đọc `$request->need_repair ?? 0`).
- [x] FE `BorrowSellRequestForm.vue` — viết lại `rebuildGrid()` CONTRACT-DRIVEN: tạo 1 group / mỗi `contractProducts`, phân bổ breakdown phiếu nguồn vào `details[]` group khớp (product_id + unit), group KHÔNG có details vẫn render (sub-row placeholder; rowspan = max(1, details.length)).
- [x] FE thêm vào "Thông tin chung": block KH read-only (`V2BaseInput disabled`, guard `customer_type>1` cho 2 ô liên hệ); radio "Cần lắp đặt" `V2BaseRadio` (need_repair Có=1/Không=0) tương tác được; (firm) `V2BaseSelect` "Nhóm VAT" (firm_tab_vat_percent) + "Chọn nhóm hàng hóa" multi (firm_tab_ids) → đổi thì gọi lại loadContractProducts với vat_percent/tab_ids.
- [x] FE `buildPayload()` thêm `need_repair`; `save()` thêm confirm need_repair kiểu ERP (câu Có/Không — xem create.blade.php:180-182). Lưu contractMeta vào data + bind block KH. **+ Fix redirect: sau save `$router.push('/finance/borrow-sell-requests')` (về DANH SÁCH, bỏ push sang chi tiết — đúng quy ước HRM).**
- [x] Verify Playwright MCP (`127.0.0.1:3000/finance/borrow-sell-requests/create`): chọn HĐ → bảng hiện ngay hàng HĐ; block KH điền đủ; radio Cần lắp đặt bấm được; HĐ hãng hiện lọc VAT+Nhóm hàng; chọn phiếu nguồn → dòng con "đang mượn" bơm vào đúng group.
- [ ] (chưa) commit — chờ user yêu cầu

### Checkpoint — 2026-10-27 (Phase 7 — VERIFIED trên browser)
Toàn bộ scope Phase 7 đã chạy đúng end-to-end trên Playwright MCP (HĐ hãng #24935 `HĐ_TPE_HN_DAU_26_1242`, KH Duy Anh, customer_type>1):
- **Bảng CONTRACT-DRIVEN**: chọn HĐ → hiện ngay hàng của HĐ (dòng "Dầu thủy lực Eneos Super Hyrando 68", cột HĐ=10 / Đã xuất=1 / Đang mượn=1). Chưa chọn phiếu nguồn vẫn render dòng placeholder.
- **Khối KH read-only đủ**: Mã KH `29TPHPNG-26`, CMT/MST `0108839168`, Địa chỉ, **Người liên hệ `Chị Hương` + Điện thoại liên hệ `0966399330`** (2 ô này chỉ hiện vì customer_type>1 — guard chạy đúng).
- **Radio "Cần lắp đặt"** bấm được (test để "Không").
- **HĐ hãng**: "Nhóm VAT" + "Chọn nhóm hàng hóa" (multi "Nhóm 1") hiện; đổi lọc → gọi lại `borrow-sell-data` với `tab_ids[]`/`vat_percent` (GET #41 → 200).
- **Chọn phiếu nguồn** `PYCXH-TESTBSR-01` → dòng con "Đang mượn=1" bơm đúng group; nhập Bán=1 → tổng VAT 8% tính đúng (1,390,000 → sau VAT 1,501,200).
- **Confirm need_repair kiểu ERP**: câu "Không" khớp verbatim ERP create.blade.php ("…**không** tích lắp đặt đều không được tạo yêu cầu lắp đặt bàn giao…").
- **POST** `/finance/borrow-sell-requests` → **200 OK** (req #77).
- **Redirect về DANH SÁCH** `/finance/borrow-sell-requests` (title "Yêu cầu xuất bán hàng mượn"), list reload `?type=all&page=1` → 200 — fix redirect PASS, KHÔNG còn đẩy sang màn chi tiết.
- Ghi chú: 40 "errors" console đều là `socket.io` (`:8891`) connection-refused (server thông báo websocket không chạy local) — KHÔNG phải exception JS của màn.
- Nghiệp vụ: lưu phiếu YCXBHM TIÊU THỤ qty "đang mượn" của phiếu nguồn → load lại `available` giảm (đúng, không phải bug). Record test đã xóa subtree để trả lại availability khi re-verify.
- CHƯA commit — chờ user yêu cầu.
