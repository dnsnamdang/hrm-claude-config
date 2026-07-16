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
