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
