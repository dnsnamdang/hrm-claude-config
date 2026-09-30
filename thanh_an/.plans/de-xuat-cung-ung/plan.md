# Plan — Phiếu đề xuất cung ứng (build thật)

> Phụ trách: @namdangit · Ngày: 2026-07-08
> Spec: `docs/superpowers/specs/2026-07-08-de-xuat-cung-ung-design.md`
> Plan chi tiết (11 task): `docs/superpowers/plans/2026-07-08-de-xuat-cung-ung.md`

## Phase 0 — Brainstorm & chốt design

- [x] 0.1 Chốt phạm vi (trọn phía đề xuất) + module mới Supply + bảng hàng hóa đầy đủ
- [x] 0.2 Chốt trạng thái / phân quyền / điều kiện xóa / thông báo
- [x] 0.3 Fill spec đầy đủ + design.md + plan chi tiết

## Phase 1 — Scaffold module Supply (BE)

- [x] 1.1 Khung module — review clean (Minor: web.php rỗng, ApiController import thừa mirror mẫu)

## Phase 2 — Migrations + Entities (BE)

- [x] 2.1 Migration 3 bảng — review clean 100%, DB migrated OK
- [x] 2.2 Entities + constants + relations + is_can_delete — owner-match = `created_by == auth()->user()->id` (users.id)

## Phase 3 — Permissions (BE)

- [ ] 3.1 Seed 3 quyền (512 Xem / 513 Lập / 514 Xử lý)

## Phase 4 — BE CRUD (gộp 4.1–4.4)

- [x] 4.1–4.4 Requests + Service + Resources + Controller + Routes — review Approved (opus). Verify tinker: vòng đời 1→3→7, code DXCU-2026-####, soft-delete OK.
  - Minor (để final review): N+1 index (nên `->with('employee_create.info')`); sort_by chưa whitelist; route dùng literal thay `PERM_*`.
  - ⚠️ shared BaseModel `employee_create_name` accessor không null-guard (rủi ro 500 nếu created_by mồ côi) — không sửa (hàm dùng chung).

## Phase 5 — Endpoint hỗ trợ FE (BE)

- [x] 5.1 customers + goods-pool — review Approved, tên cột khớp migration (Contract::DA_DUYET=3, sl_hd=root_qty, sl_pl=qty-root_qty, sl_th=exported_qty; products.product_name/internal_code/product_code). Pool type=1 ~2364 dòng (FE lọc client-side).

## Phase 6 — Thông báo (BE)

- [x] 6.1 notifyHandlers — review Approved + fix Important (bọc try/catch để lỗi notify không rollback gửi phiếu). Dùng cơ chế thật `notifications` polymorphic (`EmployeeInfoService::sendToAllNotification` + `listEmployeeInfoHasPermission`), type `supplyProposalHandle`. ⚠️ FE cần route được type thông báo mới (kiểm ở E2E).

## Phase 7 — FE wire phân hệ Supply

- [x] 7.1 MenuSupply.js + layouts/default.vue + dashboard + tile link — review Approved (mirror warehouse, không phá phân hệ khác). User verify UI.

## Phase 8 — FE danh sách

- [x] 8.1 supply_proposals/index.vue + constants.js — mirror acceptance_report list. Verify: `response.data.meta.total` đúng shape BE (apiPaginate lồng meta), `hasAPermission` mixin, actions Gửi/Xóa. Fix Important: badge dùng inline `:style` màu hex (BaseStatusColor chỉ nhận class-name). User verify UI.

## Phase 9 — FE form khối 1 + 2

- [x] 9.1 add.vue (chung + nội dung) + FileTable.vue — review Approved. Prefill khớp DetailResource, is_send edit = PUT update→PUT /send, uploadImage đọc `response.data.data`, xử lý 422 `{code,errors}` vs 400 `{code,message}`. User verify UI.

## Phase 10 — FE form khối 3 (hàng hóa)

- [x] 10.1 GoodsTable + GoodsPickerModal + ContractRefTab — review Approved (opus). Không mất field khi lưu. Fix: F1 dedup product_id khi chọn-all (Important), F2 clear products chiều →KH, F3 cap popup 200 dòng + Set. ⚠️ contract_code + số liệu nguồn trống khi mở lại (cùng nhóm "wire sau"). User verify UI.

## Phase 11 — Từ chối + tổng kiểm thử

- [x] 11.1 Modal từ chối (tái dùng `components/modal/ConfirmReasonDenyModal.vue`) + hiển thị reason_deny ở show (status=7) — review Approved. E2E do user verify UI.

## Checkpoint — 2026-07-08

Vừa hoàn thành: Toàn bộ 11 task (BE Phase 1-6 + FE Phase 7-11) — code xong, mỗi task đã review (nhiều task opus + đối chiếu BE thật). Final whole-branch review đang chạy.
Đang làm dở: (không) — chờ kết quả final review + user verify UI E2E.
Bước tiếp theo: User chạy `php artisan migrate` (nếu chưa) + `db:seed PermissionsTableSeeder` + `npm run dev`, verify UI theo checklist E2E (`scratchpad/task-11.1-report.md`). Gán quyền 512/513/514 cho user test.
Blocked: (để trống)

## Known limitations (có chủ đích — wire sau)

- Số liệu nguồn hàng hóa (SL tồn kho, đang mua, hàng vay/gửi/đổi) hiện `0`; `sl_con_lai_hd` + `contract_code` chỉ có khi chọn hàng, mở lại phiếu hiện `0`/trống (chưa persist/chưa có nguồn kho). Wire khi có module kho/nguồn.
- Click thông báo (type `supplyProposalHandle`) chưa chắc route tới màn chi tiết — tùy hệ thống notification hiện tại (kiểm ở E2E).
- Role "Admin Thành An" (id 4) chưa gán 3 quyền — gán thêm nếu user test dùng role đó.
- Phía "Xử lý cung ứng" (tạo Phiếu xử lý) là màn sau (status 9 để dành).

## Final whole-branch review (opus) — đã xử lý

- **B1 (Blocker) FIXED**: thêm owner-guard (`created_by == auth id`) vào `update()` + `send()` BE — chặn user khác sửa/gửi phiếu Nháp của người khác.
- **B2 (Blocker) FIXED**: thêm `can_edit` vào `SupplyProposalResource`; FE nút Sửa dùng `item.can_edit`.
- **G1 (Spec gap) FIXED**: `DetailResource` thêm `can_reject`; add.vue mode show + can_reject → nút Từ chối (tái dùng `ConfirmReasonDenyModal`).
- **N+1 FIXED**: `index()` eager load quan hệ người tạo.

## Chỉnh theo feedback UI (2026-07-08, sau verify)

- Số đề xuất: hiển thị mã tự sinh dự kiến khi tạo (BE `GET /supply-proposals/next-code` + FE prefill) thay placeholder "(tự sinh)".
- Popup chọn hàng: thêm bộ lọc **Phân loại** Nhập khẩu(1)/Phân phối lại(2) theo `products.import_type_id` + pill; goods-pool trả thêm `import_type_id`/`import_type_name` (cả nhánh HĐ + catalog).
- FileTable: upload có phản hồi rõ (spinner khi tải + chip thành công có icon + tên file + ✓ + link tải + nút Đổi tệp); khối "Nội dung & đính kèm" gọn đẹp hơn.

## Chỉnh theo feedback UI (2026-07-09) — Tab "Tham chiếu hợp đồng bán"

- Số HĐ trống khi mở lại phiếu: BE nạp lại (`contractRefMap()` — 1 query, không N+1) `contract_code` + số liệu (sl_hd/pl/th/còn lại) + meta HĐ từ HĐ gốc theo `contract_id`/`product_id`; `DetailSupplyProposalResource` trả các field này thay vì 0/trống.
- Thêm cột theo demo: **Thời gian ký** (`contract_sign_time`), **Thời gian kết thúc** (`contract_end_time`), **Cty thực hiện** (`main_company.name`) — BE `goodsPool()` + `contractRefMap()` trả (format d/m/Y); `GoodsPickerModal.confirm()` truyền thêm 3 field; `ContractRefTab.vue` thêm cột + ghi chú "SL còn lại = SL HĐ + SL phụ lục − SL đã thực hiện".

## Tối ưu bố cục form (2026-07-10)

- Màn Lập đề xuất: gộp "Thông tin chung" + "Nội dung" thành **2 cột cạnh nhau** (col-lg-6, card `h-100`, textarea `flex-grow` giãn đầy); "File đính kèm" tách card full-width gọn bên dưới. Thông tin chung dồn field col-md-6 (bỏ hàng nửa trống col-md-4). Giảm chiều cao dọc → tới bảng hàng hóa sớm hơn.
- Màn Lập xử lý: card thông tin chia 2 cột — 6 trường readonly (col-lg-7) trái, Nội dung đề xuất + File đính kèm (col-lg-5) phải.

## Nâng cấp đề xuất NỘI BỘ theo spec ảnh (2026-07-10, user chốt)

User chốt: nội bộ có luôn cột phân bổ (Xuất kho / Đề xuất đi mua) + Kết quả; thêm field Mục đích + Khách hàng sử dụng (lưu DB).
- BE: migration `2026_07_10_000001` — supply_proposals + `purpose`(1 Tặng/2 Mượn), `usage_customer_id/name`; supply_proposal_products + `alloc_xkho`, `alloc_mua` (đã migrate). Entity: PURPOSES + `purpose_name`. Service store/update persist (chỉ khi nội bộ) + syncProducts alloc. Request cho phép field mới. Resource (list+detail) trả purpose/purpose_name/usage_customer + product alloc. Endpoint `POST supply/supply-proposals/product-info` (dùng lại `SupplyHandlingService::productInfoMap`). DetailResource trả `created_by_name`.
- FE add.vue: field **Mục đích** (Tặng/Mượn) + **Khách hàng sử dụng** + **Người đề xuất** (chỉ hiện nội bộ trừ Người đề xuất); load productInfoMap; buildPayload/prefill field mới; validate purpose khi gửi nội bộ.
- FE GoodsTable rewrite type-aware: thêm cột **NK/PPL** + đổi "Tên hàng"→**Tên thương mại (dữ liệu phần mềm)**; **nội bộ** thêm nhóm "Xử lý cung ứng" (Xuất kho/Đề xuất đi mua) + "Kết quả" (Đã xử lý=xuất kho, Còn lại=SL đề xuất−xuất kho) + cột nguồn nội bộ (tồn kho/đang mua/tồn HĐ+đã tặng khi có KH sử dụng/mượn). KH giữ 6 cột nguồn cũ.
- FE tab mới **"Thông tin hàng hóa"** (ProductInfoTab, dùng chung): Tên thương mại HĐ/phần mềm · Quy cách · Hãng nước SX · Ghi chú đặc biệt · Hóa chất-thiết bị.
- Verify: migrate OK; tinker tạo phiếu nội bộ (purpose=Tặng, usage_customer, alloc_xkho/mua) lưu+đọc đúng; compile 3 file FE OK; route product-info trước wildcard.
- TODO: export/import Excel (chung với xử lý) để sau. Số liệu nguồn nội bộ mới (đã tặng/mượn/tồn HĐ) hiện = 0 (chưa wire).

## Tách cột theo loại + luồng BGĐ duyệt nội bộ (2026-07-13, user chốt)

User chốt: (1) bảng hàng hóa đề xuất hiển thị cột khác nhau theo loại — bỏ cột phân bổ (Xuất kho/Đề xuất đi mua/Kết quả) khỏi nội bộ để khớp demo; (2) cung ứng nội bộ phải BGĐ duyệt mới vào danh sách xử lý — tạo permission mới, thêm status "Chờ BGĐ duyệt" (=2), BGĐ duyệt/từ chối ngay màn danh sách.

- [x] T1 FE GoodsTable: bỏ hẳn nhóm cột "Xử lý cung ứng" + "Kết quả" (nội bộ). Cột nguồn khác nhau: KH = 6 cột (còn lại HĐ / tồn kho a-b / đang mua / vay / gửi / đổi); nội bộ = 2 cột (tồn kho a-b khả dụng / đang mua) — đúng demo. Giữ DB alloc_xkho/alloc_mua (ẩn UI).
- [x] T2 BE entity: STATUS_CHO_BGD=2 ('Chờ BGĐ duyệt' #7C3AED); PERM_APPROVE_INTERNAL='Duyệt đề xuất cung ứng nội bộ'; accessor is_can_approve (nội bộ + status 2 + có quyền).
- [x] T3 BE service: store/send nội bộ → status CHO_BGD (thay DA_GUI); notifyApprovers (báo BGĐ) thay notifyHandlers; approve() CHO_BGD→DA_GUI + notifyHandlers; rejectByBoard() CHO_BGD→TU_CHOI + reason_deny.
- [x] T4 BE controller + routes: approve / reject-board (checkPermission mới, đặt trước wildcard).
- [x] T5 BE resource list: thêm can_approve = is_can_approve.
- [x] T6 BE seeder: thêm permission id 516 vào PermissionsTableSeeder (mọi thay đổi quyền chạy qua seeder chung này, không tạo seeder riêng).
- [x] T7 FE constants: STATUS.CHO_BGD=2 + option 'Chờ BGĐ duyệt'.
- [x] T8 FE index.vue: nút Duyệt/Từ chối khi can_approve (tái dùng ConfirmReasonDenyModal).

## Bổ sung màn Xử lý cung ứng nội bộ theo spec ảnh (2026-07-13, user chốt)

User chốt: áp dụng cho **Phiếu xử lý cung ứng (nội bộ)**; Dư nợ/Quá hạn nợ placeholder 0 (wire sau); 3 cột nguồn placeholder 0 (hiện khi có mã KH sử dụng); nút export/import để sau (chưa render). Tên cột theo đúng spec.

- [x] BE DetailSupplyHandlingResource: proposal sub-object trả thêm purpose/purpose_name/usage_customer_id/usage_customer_name.
- [x] FE handling add.vue: khối thông tin (chỉ nội bộ) thêm **Mục đích** (purpose_name), **Khách hàng sử dụng** (usage_customer_name), **Dư nợ** (Tổng nợ, placeholder 0), **Quá hạn nợ** (Tổng nợ quá hạn, placeholder 0). computed isInternal/usageCustomerSelected; data debtTotal/debtOverdue=0; fmtMoney; CSS .hd-sub.
- [x] FE HandlingGoodsTable: srcCols nội bộ theo spec — SL tồn kho (khả dụng/tổng tồn) · SL đang mua · [khi có mã KH: Số liệu tồn hợp đồng · Số lượng đã tặng] · Số lượng mượn · Đã XL trước. Prop usageCustomerSelected. (KH giữ nguyên).
- [x] Export Excel (2026-07-13): BE `App\ExcelExport\SupplyProposalGoodsExport` + `SupplyHandlingGoodsExport` (FromView, blade `exports/supply_proposal_goods` + `supply_handling_goods`); controller `exportGoods` + route `GET /{id}/export-goods` cả 2 phân hệ; FE nút "Export Excel" trên form (hiện khi phiếu đã lưu, tải blob arraybuffer). Verify tinker render xlsx OK.
- [ ] TODO còn lại: wire Dư nợ/Quá hạn nợ (cần module công nợ) + 3 cột nguồn (tồn HĐ/đã tặng/mượn) + IMPORT Excel.

## UI Polish (2026-07-13)

> Spec: `docs/superpowers/specs/2026-07-13-supply-ui-polish-design.md`

- [x] Polish `GoodsTable.vue`: bỏ nền pastel nhóm cột → nền xám + gạch chân 2px (nguồn=cam, SL đề xuất=xanh dương); căn số nhất quán (SL đề xuất + input căn phải, header căn giữa); thêm zebra/hover + viền mềm cho đồng bộ bảng xử lý. Verify Playwright (show + edit mode).
- [x] Export Excel đẹp + đủ cột: helper chung `utils/supply-excel-export.js` (ExcelJS, style theo Báo cáo bảo lãnh) + `buildProposalSrcCols` (constants, dùng chung component). Thêm Hàng hóa + Số liệu nguồn + header nhóm 2 tầng. Verify file: 9 cột, merge + tổng khớp.

## Bugfix

- [x] Nút Export Excel màn chi tiết "không hiện": ROOT CAUSE = theme đặt `$secondary: $white` → `variant="outline-secondary"` render viền + chữ TRẮNG trên nền card trắng = vô hình (nút vẫn có trong DOM). Fix: đổi về `variant="secondary"` (nền xanh nhạt, chữ xanh) + đặt nút trên hàng `d-flex justify-content-end mb-2` ngay trên `b-tabs`, gỡ CSS `.tabs-export-wrap/.tabs-export-btn`. Đã verify bằng Playwright trên :8001 — nút hiện rõ. Bài học: KHÔNG dùng `outline-secondary` trong dự án này.

## Minor còn để sau (không chặn)

- BE `sort_by` chưa whitelist (rủi ro thấp — FE chỉ gửi cột hợp lệ).
- BE route dùng literal chuỗi quyền thay `SupplyProposal::PERM_*` (cosmetic).

## Validate SL đề xuất (2026-07-31, @khoipv)

- [x] FE `supply/supply_proposals/add.vue` — hàm `validate()`: chặn submit (cả Lưu nháp & Gửi) khi có dòng hàng hóa `quantity` không > 0. Toast "SL đề xuất của hàng hóa phải lớn hơn 0."
- [x] FE `GoodsTable.vue` — báo lỗi inline ngay dưới ô SL đề xuất của dòng vi phạm (viền đỏ + chữ đỏ "SL đề xuất phải lớn hơn 0"). Prop `show-errors` do add.vue bật khi validate lỗi, tắt khi hợp lệ.

## Polish + validate (2026-08-01, @khoipv)

- [x] FE `supply/supply_proposals/add.vue` — "Ngày cần giao" chặn chọn ngày quá khứ (`disabled-date=disabledBeforeToday`).
- [x] BE `StoreSupplyProposalRequest` — `delivery_date` thêm `after_or_equal:today` khi tạo mới (edit không chặn), message tiếng Việt.
- [x] FE `supply/supply_proposals/index.vue` + `inbox.vue` — cột Khách hàng: loại nội bộ hiển thị `usage_customer_name`, loại KH hiển thị `customer_name`.
- [x] FE `supply/supply_proposals/add.vue` — mọi lỗi validate 422 hiển thị inline ngay dưới đúng trường (thêm `formError`, `handleSubmitError` map lỗi từng trường, `<base-helper-error>` dưới type/purpose/customer_id/usage_customer_id/delivery_date/note/content).

## HĐ mua — chặn tỉ lệ % (2026-08-01, @khoipv)

- [x] FE `purchase_contracts/components/GeneralTab.vue` — ô Tỷ lệ (%) đợt thanh toán: đổi sang native input `:value`+`@input="onPctInput"`, clamp [0,100] (âm→0, >100→100), đồng bộ lại ô khi bị chặn. Số tiền đợt = pct/100×tổng nên tự hết âm/vượt.
- [x] FE `GeneralTab.vue` — chặn ngày: Ngày ký không cho quá khứ (`disabledBeforeToday`); Ngày kết thúc + Ngày thanh toán không trước ngày ký (`disabledBeforeSign`); đổi ngày ký tự xóa các ngày đã chọn nếu sớm hơn (`onSignChange`).
- [x] BE `StorePurchaseContractRequest` — chặn ngày: `sign_time` after_or_equal:today (chỉ khi tạo mới); `end_time` after_or_equal:sign_time; `progress.*.time` after_or_equal:sign_time; message tiếng Việt.

## Chỉnh UI nhỏ (2026-08-03, @khoipv)

- [x] FE `supply/supply_proposals/add.vue` — ô "Ghi chú" thiếu placeholder → thêm `placeholder="Nhập ghi chú"`.

## Thu hồi đề xuất khi chờ xử lý (2026-09-08, @khoipv)

> Chủ phiếu được thu hồi phiếu đã gửi khi phòng tiếp nhận CHƯA lập phiếu xử lý.
> Chốt: về Nháp (sửa & gửi lại) · áp dụng cả status 2 (Chờ BGĐ duyệt) và 3 (Chờ xử lý) · không nhập lý do.

- [x] BE migration: thêm `recalled_at`, `recalled_by` vào `supply_proposals` (index, không khóa ngoại)
- [x] BE `SupplyProposal`: accessor `is_can_recall` (chủ phiếu + status ∈ {2,3} + chưa có PXL nào)
- [x] BE `SupplyProposalService::recall()`: check lại trong transaction, về status 1 + `sent_at=null` + ghi recalled_*
- [x] BE `SupplyProposalService::notifyRecall()`: status 3 → nhóm PERM_HANDLE; status 2 → nhóm PERM_APPROVE_INTERNAL
- [x] BE `SupplyProposalController::recall()` + route `PUT /{id}/recall` (middleware Lập phiếu đề xuất cung ứng)
- [x] BE `SupplyProposalResource` + `DetailSupplyProposalResource`: thêm `can_recall`
- [x] FE `supply_proposals/index.vue`: nút Thu hồi + confirm
- [x] FE `supply_proposals/add.vue`: nút Thu hồi màn chi tiết
- [x] Verify tinker (DB thanh_an_stag): 5 ca — status 3 chưa PXL → về Nháp + `sent_at=null` + ghi `recalled_by/at` (OK); status 2 → về Nháp (OK); có PXL (kể cả PXL bị từ chối duyệt) → chặn, status giữ nguyên 3 (OK); status 9 → chặn (OK); không phải chủ phiếu → chặn (OK). Dữ liệu test đã forceDelete, route `PUT .../recall` đã đăng ký.
- [ ] CHƯA verify click-through UI (không có tài khoản đăng nhập trong session) — mới xác nhận Nuxt compile 2 trang không lỗi
- Lưu ý (đã chốt lại 2026-09-08): nút Thu hồi **chỉ hiện với chủ phiếu**. Vd DXCU-2026-0015 ở "Chờ xử lý", chưa có PXL, nhưng `created_by=156` nên user 13 không thấy nút — đúng thiết kế, không phải bug. Phiếu test được của user 13: DXCU-2026-0005/0008/0009 (status 3) và 0019 (status 2).

## Popup chọn hàng — chỉ HĐ còn hiệu lực (2026-09-08, @khoipv)

- [x] BE `SupplyProposalService::goodsPool()` — thêm điều kiện HĐ còn hiệu lực: `contract_end_time IS NULL OR contract_end_time >= hôm nay` (giữ nguyên `approvedStatuses()` = 3 Đã duyệt + 9 Đã kết xuất, `record_type = HỢP ĐỒNG`, đúng customer). Ngày KT đã gồm gia hạn phụ lục đã duyệt nên so trực tiếp trên cột.
- [x] Verify tinker KH 1478 (9 HĐ: 3 hết hạn + 6 còn hạn) → pool chỉ còn contract_id [120,121,122,123,126,134] = đúng 6 HĐ còn hiệu lực; 146 dòng trong HĐ + danh mục ngoài HĐ giữ nguyên.
- Ghi chú: endpoint `supply/supply-proposals/goods-pool` DÙNG CHUNG với popup chọn hàng màn **phiếu xử lý cung ứng** (`supply_handlings/add.vue:782`) → điều kiện này áp dụng cho cả 2 màn.
- Ghi chú: ô tick "Chỉ hiện hàng còn SL theo HĐ" lọc theo `sl_con_lai_hd = contract_products.qty - exported_qty`; `exported_qty` chỉ cập nhật qua import Excel (type `exported-qty` → `ExpectedQtyImport`), KHÔNG tự trừ theo phiếu đề xuất/xử lý. Trên DB stag hiện 0/4704 dòng có exported_qty > 0.

## Cảnh báo SL đề xuất / SL đặt đơn vượt SL còn lại (2026-09-08, @khoipv)

> Yêu cầu: SL đề xuất (màn đề xuất) và SL đặt đơn (màn xử lý) vượt SL còn lại theo HĐ → bôi đỏ + note bên dưới.
> Chốt: cảnh báo mềm (KHÔNG chặn gửi/lưu) · chỉ áp dụng cho dòng `in_contract` và loại phiếu có cột "SL còn lại HĐ" (KH) · dòng ngoài HĐ không có mốc so sánh nên bỏ qua.

- [x] FE `supply_proposals/components/GoodsTable.vue` — `isOverContract(p)` = `in_contract && quantity > sl_con_lai_hd`; ô SL đề xuất + ô SL còn lại HĐ nền đỏ nhạt (`cell-over`), input viền đỏ (`is-over`), số ở chế độ xem đỏ đậm (`over-val`), note đỏ dưới ô: "Vượt SL còn lại (x)".
- [x] FE `GoodsTable.vue` — note tổng hợp dưới bảng: "Có N mặt hàng có SL đề xuất vượt SL còn lại theo hợp đồng (tên 3 mặt hàng đầu...)." — bỏ câu giải thích thêm phía sau theo yêu cầu.
- [x] FE `supply_handlings/components/HandlingGoodsTable.vue` — cùng logic cho cột `dat_don` (SL đặt đơn), style + note giống hệt màn đề xuất.
- [x] FE cả 2 bảng — bôi đỏ **cả hàng**, **1 màu duy nhất** (`tr.row-over` nền `#fdecea !important`, đè sọc ngựa vằn + hover). Đã bỏ: tô đậm riêng 2 ô SL đề xuất/đặt đơn + SL còn lại HĐ, viền đỏ input, số đỏ đậm ở chế độ xem (theo yêu cầu "để cùng 1 màu thôi").
- [x] Verify: Nuxt compile OK cả `/supply/supply_proposals/add` và `/supply/supply_handlings/add` (HTTP 200, không có marker lỗi compile).
- [ ] CHƯA verify click-through UI (không có tài khoản đăng nhập trong session)
- Ghi chú: banner cũ ở `supply_handlings/add.vue` (`overOrderRows` / `overContractRows`) giữ nguyên — kiểm tra phần **phân bổ xử lý** vượt đặt đơn / vượt HĐ, khác với cảnh báo mới (kiểm tra chính cột SL đặt đơn).
- Ghi chú: `sl_con_lai_hd` = `contract_products.qty - exported_qty`, lấy từ `DetailSupplyProposalResource` / popup chọn hàng; dòng ngoài HĐ có `sl_con_lai_hd = 0` nhưng `in_contract = false` nên không bị cảnh báo nhầm.

## Điều hướng bàn phím trong bảng hàng hóa (2026-09-08, @khoipv)

> Yêu cầu: thao tác bàn phím lên/xuống/trái/phải + Enter giữa các ô nhập số. Chốt: **giữ nguyên `input type="number"`**.

- [x] FE mixin dùng chung `pages/supply/gridKeyboardNav.js` — `onGridKeydown` + `focusGridCell/focusGridSibling/focusGridEl`; ô nhập gắn `data-grid-cell` + `:data-r` (dòng) + `:data-c` (cột nhập).
- [x] FE `supply_proposals/components/GoodsTable.vue` — gắn mixin, cột SL đề xuất = `data-c=0`.
- [x] FE `supply_handlings/components/HandlingGoodsTable.vue` — gắn mixin, SL đặt đơn = `data-c=0`, các cột phân bổ = `data-c=ci+1`.
- [x] Verify: Nuxt compile OK cả 2 trang (HTTP 200, không lỗi module/compile).
- [ ] CHƯA verify click-through UI (không có tài khoản đăng nhập trong session)

Hành vi phím:
- ↑ / ↓ — lên/xuống cùng cột (đã `preventDefault` để input number không tự tăng/giảm)
- Enter / Shift+Enter — xuống/lên cùng cột (đồng thời chặn submit form)
- ← / → — sang ô trái/phải cùng dòng; hết dòng thì nhảy sang dòng kế (kiểu Excel)
- Tab / Shift+Tab — giữ mặc định trình duyệt
- Ô được focus tự bôi đen giá trị để gõ đè

Đánh đổi đã biết: giữ `type="number"` nên trình duyệt (Chrome) chặn đọc `selectionStart` → không phân biệt được "con trỏ đang giữa số" hay "ở cuối số", vì vậy ←/→ LUÔN chuyển ô. Muốn sửa 1 ký tự giữa số thì click vào đúng vị trí trong ô.

## Ô nhập số để trống thay vì 0 (2026-09-08, @khoipv)

- [x] FE `GoodsTable.vue` + `HandlingGoodsTable.vue` — thêm method `inputVal(v)` = `Number(v) > 0 ? v : ''`, dùng cho `:value` của SL đề xuất / SL đặt đơn / các cột phân bổ. Giá trị thật trong `formSubmit.products` vẫn là số 0 (handler `onFieldInput`/`toNum` ép `'' → 0`) nên payload gửi BE không đổi.
- [x] Verify: Nuxt compile OK cả 2 trang (HTTP 200).
- Ghi chú: chỉ áp dụng cho 2 bảng hàng hóa của Cung ứng (đề xuất + xử lý). Các màn HĐ mua / đơn mua (`purchase_contracts`, `purchase_orders`) vẫn giữ `|| 0` như cũ — chưa có yêu cầu.

## Lưu nháp phiếu xử lý cung ứng (2026-09-08, @khoipv)

> Chốt: Nháp KHÔNG tính vào SL đã xử lý của đề xuất · Nháp VẪN chặn người đề xuất thu hồi · PXL nháp chỉ người tạo thấy trong danh sách · chỉ người tạo sửa/xóa nháp.
> Không cần migration (dùng lại cột `status`).

- [x] BE `SupplyHandling`: `STATUS_NHAP = 1` + vào `STATUSES` (Nháp, #6B7280); `is_can_edit` / `is_can_delete` cộng thêm trạng thái Nháp
- [x] BE `SupplyHandlingService::store()`: cờ `is_draft` → status 1 (giữ guard đề xuất phải đang Chờ xử lý)
- [x] BE `SupplyHandlingService::update()`: nháp + `is_draft=0` = gửi chính thức → check lại đề xuất, chuyển 5 (KH) / 3 (Nội bộ) + syncHandledStatus
- [x] BE loại nháp khỏi "đã xử lý": `SupplyProposal::hasActiveHandling()`, vòng tính handledQty trong entity, `SupplyProposalService::handledQtyByProduct()`
- [x] BE `SupplyHandlingService::index()`: phiếu Nháp chỉ hiện với người tạo
- [x] BE `StoreSupplyHandlingRequest`: thêm `is_draft` nullable boolean
- [x] FE `supply_handlings/constants.js`: `STATUS.NHAP` + option "Nháp" trong bộ lọc
- [x] FE `supply_handlings/add.vue`: nút "Lưu nháp" (bỏ qua validate bắt buộc hàng hóa/phân bổ), nút Lưu cũ = gửi chính thức
- [x] Verify tinker + compile FE

## Đưa cụm nút hành động vào trong card (2026-09-08, @khoipv)

> Yêu cầu: nút Lưu / Quay lại... đang nằm trần trên nền xám, đưa vào trong card giống màn Hợp đồng mua.

- [x] FE `supply_proposals/add.vue`: đưa cụm nút vào CUỐI `card-body` của card "Danh mục hàng hóa đề xuất" (`div.form-actions.text-right`); gộp luôn khối "Phản hồi xử lý" (trước là card riêng) vào cùng card đó để nút luôn ở dưới cùng
- [x] FE `supply_handlings/add.vue`: đưa cụm nút + 2 alert duyệt/từ chối vào cuối `card-body` của card tổng hợp
- [x] FE: scoped style `.form-actions { border-top: 1px solid #eee; padding-top: 10px }`
- [x] Verify compile FE (2 trang HTTP 200)

## Tab tham chiếu HĐ bán: đổi tiêu đề cột + link chi tiết HĐ (2026-09-09, @khoipv)

> Yêu cầu: cột "Số hợp đồng" → đổi tiêu đề thành "Mã hợp đồng"; giá trị gán link mở chi tiết hợp đồng bán.

- [x] FE `supply_proposals/components/ContractRefTab.vue` — đổi `<th>Số hợp đồng</th>` → `Mã hợp đồng`
- [x] FE `ContractRefTab.vue` — bọc `p.contract_code` bằng `<nuxt-link :to="/contract/contract/{contract_id}" target="_blank">` (pattern giống `reports/purchase-demand/index.vue`), giữ `—` khi không có mã
- [x] Verify compile Nuxt trang `/supply/supply_proposals/add` (HTTP 200, không marker lỗi compile)
- [ ] CHƯA verify click-through UI
- Ghi chú: `supply_handlings/components/HandlingSummaryTabs.vue:20` cũng có cột "Số hợp đồng" tương tự — chưa sửa vì ngoài phạm vi yêu cầu

## Bug: HĐ có nhiều dòng cùng mã nội bộ → SL không cộng dồn (2026-09-09, @khoipv)

> Ca thật: HĐ `HD-101/2026` (id 120, KH 1478 BVĐK Vân Đình) có 3 dòng `contract_products` (3802/3803/3804)
> cùng `product_id=86` + cùng mã nội bộ `HC-HH-084`, tên riêng thấp/trung bình/cao, mỗi dòng qty=20.
> Popup ra 3 dòng × 20; FE dedupe theo product_id giữ dòng ĐẦU, bỏ im lặng 2 dòng → phiếu ra 20 thay vì 60.
> `contractRefMap()` key `contractId_productId` bị ghi đè, giữ dòng CUỐI → tab tham chiếu cũng 20.
> Phạm vi: 12 cặp (HĐ, hàng hóa) trùng dòng trên 11 HĐ; cả 12 đều cùng mã nội bộ; 0 ca cùng mã nội bộ khác mã hàng hóa.
> Chốt với @khoipv: gộp thành 1 dòng, SL cộng dồn = 60 · CHỈ gộp khi cùng mã nội bộ · sửa cả màn HĐ kết xuất.

- [x] BE `SupplyProposalService::contractProductRows()` — gộp theo (product_id + internal_code) trong cùng HĐ, cộng dồn root_qty/qty/exported_qty (hàm dùng chung: goodsPool + RenderedContractService::prefill — @khoipv đã duyệt sửa cả 2)
- [x] BE `SupplyProposalService::contractRefMap()` — cộng dồn thay vì ghi đè key `contractId_productId`
- [x] Verify tinker: goodsPool(1, 1478) ra ĐÚNG 1 dòng HC-HH-084, sl_hd=60 / sl_con_lai_hd=60
- [x] Verify tinker: contractRefMap['120_86'] ra sl_hd=60 / sl_con_lai_hd=60
- [x] Regression: quét 193 HĐ đã duyệt (4597 dòng) — số dòng sau gộp khớp số nhóm (product_id, internal_code) trong DB, 0 lệch; đối chiếu số liệu 11 HĐ có dòng trùng, 0 lỗi
- [x] Smoke test `RenderedContractService::prefill()` (HĐ 179) — chạy OK, không HĐ nào đã kết xuất đang có dòng trùng
- [x] Verify compile FE `/supply/supply_proposals/add` HTTP 200 (không đổi file FE nào)
- [ ] CHƯA verify click-through UI
- Ghi chú: tên dòng gộp giữ theo dòng HĐ đầu tiên để popup còn tìm được bằng tiếng Việt; bảng hàng hóa vẫn hiện cột "Tên thương mại" từ `products.trade_name` nên không mất thông tin
- Phát hiện kèm (CHƯA sửa, ngoài phạm vi): `excludeIds`/`onPickConfirm` dedupe chỉ theo `product_id`, bỏ qua `contract_id` → không thể đề xuất cùng 1 mã hàng từ 2 HĐ khác nhau trong 1 phiếu, và bị bỏ im lặng không cảnh báo

## Bug: gộp dòng HĐ khác ĐVT phải quy đổi về ĐVT chính (2026-09-09, @khoipv)

> Lỗ hổng của bản gộp ở mục trên: cộng thẳng số lượng mà không kiểm tra `unit_id`.
> Ca thật: HĐ `HD-002/2025` (id 2), mã nội bộ `HC-HH-024` (product_id 26) có 2 dòng —
> id 86 = 12 **Hộp** (unit 3), id 136 = 250 **mL** (unit 4). Cộng thô ra 262 (sai).
> ĐVT chính = `products.unit_id` = Hộp; hệ số quy đổi từ ĐV cơ bản (`product_package_informations.conversion_factor`):
> mL = 1, Hộp = 50 → 1 Hộp = 50 mL. Đúng phải là 12 + 250/50 = **17 Hộp**.
> Quy tắc chốt: cùng ĐVT → cộng thẳng giữ nguyên ĐVT · khác ĐVT → quy đổi `qty_M = qty_A × f(A) / f(M)`
> rồi mới cộng, ĐVT dòng gộp thành ĐVT chính · thiếu hệ số → KHÔNG gộp (trả từng dòng như cũ).

- [x] BE `SupplyProposalService::unitConversionMap()` (mới) — 2 query dựng map `product_id => [main_unit_id, main_unit_name, main_factor, factors, names]`; ưu tiên `products.unit_id`, fallback `is_usually` (12 hàng hóa có nhiều dòng `is_usually=1` mâu thuẫn)
- [x] BE `SupplyProposalService::aggregateContractLines()` (mới) — cộng dồn + quy đổi 1 nhóm, trả `ok=false` khi thiếu hệ số
- [x] BE `SupplyProposalService::contractRow()` (mới) — tách khuôn 1 dòng hàng, dùng chung cho nhánh gộp và nhánh không gộp
- [x] BE `contractProductRows()` — nhận thêm tham số `$unitMap`, gom nhóm trước rồi mới cộng qua `aggregateContractLines()`
- [x] BE `goodsPool()` — tính `unitConversionMap()` 1 lần cho toàn bộ HĐ (tránh N+1), truyền xuống `contractProductRows()`
- [x] BE `contractRefMap()` — gộp theo product_id + quy đổi ĐVT y hệt goodsPool, fallback cộng thô khi thiếu hệ số (không load quan hệ `unit` → không N+1)
- [x] Verify tinker: HĐ 2 / HC-HH-024 ra **17 Hộp** (12 + 250/50), HĐ 120 / HC-HH-084 vẫn **60 Lọ**
- [x] Verify tinker: `goodsPool(1, 2)` và `goodsPool(1, 1478)` ra đúng 1 dòng, số liệu khớp
- [x] Verify tinker: `contractRefMap['2_26']` = 17, `contractRefMap['120_86']` = 60
- [x] Regression 193 HĐ / 4597 dòng: 0 HĐ rơi vào nhánh không gộp được, 0 lệch giữa `contractProductRows()` và `contractRefMap()` trên cả 4 cột SL
- [x] Kiểm tra dữ liệu: 0 ca cùng `product_id` nhưng khác `internal_code` trong cùng HĐ → key `contractId_productId` của refMap vẫn tương đương key gộp
- [x] Smoke test `prefill()` HĐ 179 OK; 11 HĐ có dòng trùng đều chưa kết xuất nên không có ca prefill thật
- [x] `php -l` sạch
- [ ] CHƯA verify click-through UI
- Ghi chú: chỉ 1/12 nhóm trùng trong toàn DB thực sự khác ĐVT (HĐ 2) — 11 nhóm còn lại cùng ĐVT, hành vi không đổi
- Ghi chú: 5 cặp (hàng hóa, ĐVT) trong DB thiếu hệ số quy đổi (pid 5/20/205/23 ở HĐ 2, pid 2783 ở HĐ 87) nhưng không cặp nào nằm trong nhóm cần gộp

## Popup chọn hàng: tách lại từng dòng HĐ, phiếu vẫn gộp (2026-09-10, @khoipv)

> Nối tiếp 2 mục bug ngày 2026-09-09. Gộp ở BE chữa được số (60) nhưng popup mất 3 tên riêng
> (thấp / trung bình / cao của `HC-HH-084`, HĐ 120) → không biết đang chọn cái gì.
> Chốt với @khoipv: **popup hiện từng dòng `contract_products`**, còn **bảng hàng hóa của phiếu vẫn gộp**
> (DB `supply_proposal_products` chỉ lưu `(contract_id, product_id)`, không có chỗ ghi dòng HĐ).
> Tick 1 dòng → 20 · tick 2 → 40 · tick cả 3 → 60. Không migration, không đụng phiếu xử lý cung ứng.

- [x] BE `groupUnitTarget()` (mới) — tách phần "chọn ĐVT đích + hệ số quy đổi từng dòng" ra khỏi `aggregateContractLines()`, dùng chung cho cả 2 nhánh gộp/không gộp
- [x] BE `aggregateContractLines()` — refactor dùng `groupUnitTarget()`, kết quả không đổi
- [x] BE `contractProductRows()` — thêm tham số `$merge = true`; `false` = trả từng dòng HĐ kèm `contract_product_id`, `merge_key`, `can_merge`, `main_unit_id/_name`, `sl_*_main` (số của dòng đã quy đổi về ĐVT chính)
- [x] BE `goodsPool()` — gọi với `$merge = false`
- [x] BE `RenderedContractService::prefill()` — giữ mặc định `true`, hành vi không đổi (@khoipv đã duyệt sửa hàm dùng chung theo cách thêm tham số mặc định)
- [x] BE `contractRefMap()` — giữ nguyên gộp (phiếu vẫn lưu 1 dòng)
- [x] FE `GoodsPickerModal.vue` — định danh dòng theo `contract_product_id` thay vì `product_id`
- [x] FE `add.vue onPickConfirm()` — gom dòng đã tick theo `merge_key`: 1 dòng giữ số + ĐVT dòng đó, nhiều dòng cộng bằng `sl_*_main` + ĐVT chính; `can_merge = false` mà tick >1 → toast chặn
- [x] FE `add.vue excludeIds` — loại theo `contract_product_id` khi biết dòng nguồn, fallback `(contract_id, product_id)` cho phiếu load từ DB
- [x] FE tick thêm dòng của mã đã có trong phiếu → cộng dồn vào dòng sẵn có (hiện đang bỏ im lặng)
- [x] Verify tinker: `goodsPool(1, 1478)` ra 3 dòng × 20 (HĐ 120); `goodsPool(1, 2)` ra 2 dòng 12 Hộp / 250 mL kèm số quy đổi 12 và 5
- [x] Verify tinker: `prefill()` HĐ 179 + regression 193 HĐ không đổi
- [x] Verify compile FE: template 2 component compile 0 lỗi; harness Node chạy thẳng `GoodsPickerModal.confirm()` → `add.onPickConfirm()` với data BE thật → 20 / 40 / 60 Lọ, 12 Hộp + 250 mL → 17 Hộp, dòng cùng mã khác HĐ bị khóa ngay ở popup — 8/8 assertion đạt
- [ ] @khoipv click-through UI trên trình duyệt (hard refresh sau khi FE build lại)

### Checkpoint — 2026-09-10
Vừa hoàn thành: tách dòng HĐ trong popup chọn hàng — BE `groupUnitTarget()` / `contractProductRows($merge)` / `goodsPool()`, FE `excludeKeys` / `rowMergeKey` / `buildProductRow` / `onPickConfirm`; verify tinker + regression 193 HĐ 0 sai lệch + harness FE 8/8 đạt
Đang làm dở: không có — code-complete
Bước tiếp theo: @khoipv click-through trên trình duyệt (Phiếu đề xuất cung ứng → thêm mới → chọn hàng HĐ HD-101/2026, mã HC-HH-084)
Blocked:
