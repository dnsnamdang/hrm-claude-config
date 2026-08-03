# Plan — Quản lý kho (Warehouse Management)

> Design tóm tắt: `design.md` · Spec đầy đủ: `docs/superpowers/specs/2026-06-28-warehouse-management-design.md`
> Plan chi tiết Phase 1: `docs/superpowers/plans/2026-06-28-warehouse-management-phase1.md`
> @manhcuong · Module `Modules/Warehouse` + `pages/warehouse`

---

## Phase 1 — Engine + Nhập kho

### Backend
- [x] T1. Scaffold module `Warehouse` (module.json, providers, routes, register)
- [x] T2. Migrations engine: `stock_movements` + `inventories`
- [x] T3. Migrations nhập kho: `wh_receipts` + `wh_receipt_items`
- [x] T4. Entities: StockMovement, Inventory, WhReceipt, WhReceiptItem (+ HasStatusBadge, getNextCode PN-)
  - Minor (final review): WhReceiptItem thiếu numeric cast conversion_rate/quantity/quantity_base
- [x] T5. `StockService` (postMovement / getAvailable / assertEnough / setAbsolute) + smoke test
  - Fix wave 1: race INSERT inventory lần đầu (insertOrIgnore→lockForUpdate); message lỗi có tên hàng; docblock transaction/TOCTOU
- [x] T6. `WhReceiptService` (CRUD + submit/approve→ghi tồn/reject) + smoke test approve→tồn
  - Fix wave 1: submit() xoá reject_reason; set updated_by ở submit/approve/reject
  - Minor (final review): index() dùng array-access (style); conversionRate cast int; service không tự bọc transaction (Controller phải bọc store/update/approve)
- [x] T7. Request + Resources (list/detail) + Controller + Routes + permission 1124-1126
  - Fix wave 1: lockForUpdate trên receipt trong approve (chống cộng đôi tồn); eager-load employee ở submit/approve/reject
  - Resource extends Modules\Human\Transformers\ApiResource; permission type=10 (phân hệ Kho)
  - Lưu ý deploy: chưa insert permission 1124-1126 vào DB dev (chờ user duyệt) + gán role + cache-reset

### Frontend
- [x] T8. Store `warehouse-receipt` (actions: list/detail/save/update/remove/submit/approve/reject — khớp pattern sale-contract.js)
- [x] T9. Form nhập kho (create/edit) — master-detail, ProductPickerModal tái dùng, ĐVT quy đổi, validate inline
  - Fix: `:key` v-for dùng product_id (stable)
  - Minor (final): ProductPickerModal hardcode chữ "báo giá"; 422 chưa map inline từng field (nhất quán QuotationForm)
  - User test dev server: products getAll trả product_units.unit; receipt_date Y-m-d
- [x] T10. Danh sách + Chi tiết (workflow footer) + Menu sidebar
  - Menu wired 3 nơi (checkPermission.js / Sidebar.vue / default.vue) theo pattern saleItems, không phá module khác
  - Bổ sung: mục "Quản lý kho" → /warehouse/receipt trong popup chọn phân hệ topbar (`components/BasicSubsystem.vue`); icon riêng `assets/images/icon_kho.svg` (32×32, fill #018944, glyph nhà kho + cửa cuốn, khớp style icon_sale.svg). Pencil MCP không dùng được (app desktop chưa kết nối) → hand-author SVG theo lựa chọn user.
  - Bổ sung: màn phân quyền `components/setting/Permission.vue` thêm accordion "Phân hệ quản lý kho" = `filterPermission(10)` (giống type=9 kinh doanh) → hiển thị nhóm "Nhập kho" (3 quyền 1124-1126). BE đã seed type=10 nên không cần sửa BE.
  - Fix: confirm trước Duyệt (BaseConfirmModal)
  - Minor (final): isCascading thừa; double-emit close (idempotent)

---

## Phase 2 — Xuất kho (gắn HĐ / tự do)
> Design: design-phase2.md · Plan chi tiết: docs/superpowers/plans/2026-06-29-warehouse-management-phase2.md
> Chốt: gắn HĐ (ĐVT khoá theo dòng HĐ) HOẶC tự do; chặn vượt tồn + vượt HĐ khi duyệt; "đã xuất" accessor động.

### Backend
- [x] T1. Migration `wh_issues` + `wh_issue_items` (+contract_id/contract_item_id/issue_type/receiver/reason)
- [x] T2. Entities WhIssue (PX-, ISSUE_TYPE_*) + WhIssueItem (contractItem)
- [x] T3. `WhIssueService` (CRUD + approve: assertEnough + assertContractRemaining + postMovement −) + contractRemaining + smoke test
  - Fix wave 1 (Critical): assertContractRemaining gộp theo contract_item_id (chống bypass quota khi trùng dòng); clamp remaining≥0. Smoke test quota HĐ PASS (block 14>10, allow=10).
  - Minor (final): N+1 trong assertContractRemaining/contractRemaining (read, chấp nhận); conversion_rate INT theo schema
- [x] T4. Request + Resource + Controller + Routes (+remaining) + permission 1127-1129
  - Fix wave 1: eager-load đầy đủ ở store/update (chống N+1); validate contract_item_id `exists:sale_contract_items` (đóng gap quota)
  - 9 route /issues (remaining trước /{id}); tên quyền khớp seeder; permission 1127-1129 type=10 group "Xuất kho" (chưa seed DB — chờ chạy seeder)
  - Minor (final): issue_type_name inline ở Resource; reject() dùng isCanApprove (nhất quán Phase 1)
- [x] T5. Sale: accessor `quantity_issued` (động) + DetailSaleContractResource (tab "Thông tin xuất hàng") — additive, smoke ISSUED=5 PASS

### Frontend
- [x] T6. Store `warehouse-issue` (+contractRemaining) — mirror warehouse-receipt.js
- [x] T7. Form xuất kho (radio Theo HĐ/Tự do; HĐ→load dòng còn lại còn lại)
  - Fix wave 1: type=1 cho xoá dòng + bỏ qua qty=0 (giải kẹt remaining=0); contractRemaining lỗi → cảnh báo b-alert không kẹt ngầm; type=2 payload lọc qty>0
  - Minor (final): 422 chưa map inline từng field (nhất quán WhReceiptForm/QuotationForm — giữ)
  - Lưu ý: subagent đầu mất kết nối nhưng file đã ghi; quota vẫn được BE chặn ở bước Duyệt
- [x] T8. List + Detail + menu "Xuất kho" (giữ "Nhập kho")
  - Descope có chủ đích: filter theo Hợp đồng ở list (giá trị thấp, cần dropdown tải toàn bộ HĐ) — giữ filter Kho/Loại xuất/Trạng thái/ngày/keyword. Có thể bổ sung sau nếu cần.
  - Nút Xoá chỉ ở danh sách (đúng design Phase 1, detail không có) — by design.
### Checkpoint — 2026-06-29 (CODE HOÀN THÀNH Phase 2 + FINAL REVIEW PASS)
Vừa hoàn thành: **Toàn bộ 8 task Phase 2 (Xuất kho) BE+FE**, subagent-driven (implementer+reviewer+fix). Final review opus: **SẴN SÀNG BÀN GIAO, 0 Critical**. Chưa commit.
- BE: wh_issues/wh_issue_items; WhIssue/WhIssueItem; WhIssueService (approve: assertEnough + assertContractRemaining gộp theo contract_item_id + postMovement âm, trong transaction + lockForUpdate); Controller/Request(required_if+exists)/2 Resource/9 route (+contract/{}/remaining); permission 1127-1129. Sale: accessor `quantity_issued` (động) + DetailSaleContractResource (tab "Thông tin xuất hàng" nay ra số thật). Smoke test: free-issue tồn 100→70 + chặn vượt tồn; quota HĐ block 14>10 / allow=10; quantity_issued=5.
- FE: store warehouse-issue; WhIssueForm (radio Theo HĐ/Tự do, HĐ→contractRemaining→dòng còn lại, xoá dòng, validate ≤ remaining); create/edit; list (filter Kho/Loại xuất/Trạng thái/ngày/keyword) + detail (workflow gate quyền) + menu "Xuất kho".
- Permission DB: ĐÃ chạy seeder (612 quyền) + gán role 1 đủ 1124-1129 + cache clear.
- **TOCTOU race — ĐÃ FIX (user duyệt sửa hàm chung)**: `StockService::assertEnough` đọc tồn bằng `lockForUpdate` + sort product_id (chống deadlock); `WhIssueService::assertContractRemaining` khoá dòng SaleContractItem. Serialize duyệt đồng thời, chống tồn âm/vượt quota. Smoke test free-issue + quota vẫn PASS. Áp dụng cho mọi nghiệp vụ gọi assertEnough (xuất/chuyển/kiểm kê sau này).
- CÒN (user dev server): restart + re-login → test menu Xuất kho; E2E tạo phiếu xuất (HĐ/tự do)→duyệt→tồn giảm + "đã xuất" trên HĐ ra số; commit 2 repo. Descope: filter HĐ ở list.
Bước kế tiếp: Phase 3 — Chuyển kho (chờ user).

### Checkpoint — 2026-06-29 (Chuyển Danh mục Kho sang phân hệ Quản lý kho)
- FE: chuyển trang `pages/category/warehouses/` → `pages/warehouse/category/` (route `/category/warehouses` → `/warehouse/category`, sửa pathsToKeep; API path `category/warehouses` GIỮ nguyên vì BE ở Category). Bỏ mục "Kho" khỏi `category.js`, thêm "Danh mục kho" vào `warehouse.js` (icon ri-store-2-line, quyền 1103/1104).
- Quyền 1103/1104: đổi type 8→10 + group "Danh mục kho" (seeder + reseed DB, role 1 vẫn giữ). Màn Role: accordion "Phân hệ quản lý kho" nay có 3 nhóm (Danh mục kho, Nhập kho, Xuất kho).
- BE giữ nguyên (WarehouseController/entity ở Modules/Category, API /v1/category/warehouses không đổi) — theo quyết định user.
- User test: re-login → menu Quản lý kho có "Danh mục kho" → vào /warehouse/category CRUD chạy; màn Role hiện nhóm Danh mục kho dưới phân hệ kho.

### Checkpoint — 2026-06-29 (E2E Playwright API-level — XANH 7/7)
- Setup: `nhatlinh-client/e2e/` (`@playwright/test 1.61.1`, Node 20 qua nvm — độc lập app Node 12; browser cache global). Config baseURL API :8000 + globalSetup.
- `nhatlinh-api/database/e2e_provision.php` (idempotent: tạo user E2E `e2e_warehouse@test.local`/`Password@123` qua employee_infos→employees→company_employees→employee_has_roles role 1 Admin; + fixtures warehouse E2E_WH/product E2E_PROD 2 ĐVT/contract E2E_HD status=3; in E2E_JSON) + `e2e_teardown.php`.
- `e2e/global-setup.js` (chạy provision → login JWT key `access_token` → ghi `.auth/state.json`), `e2e/tests/warehouse.spec.js`.
- **7/7 PASS** (verify độc lập): P1 nhập 100 base; P2 xuất tự do→70; chặn vượt tồn (71>70)→422; xuất theo HĐ remaining 30→0 + issued 30 + chặn vượt HĐ→422; auth không token→401.
- Chạy lại: `cd nhatlinh-client/e2e && nvm use 20 && npx playwright test` (BE phải đang serve :8000).
- **BE issue phát hiện (pre-existing, KHÔNG phải kho)**: bảng `customer_categories` chưa migrate trên DB dev → `GET /sale/contracts/{id}` 500 (eager-load customer.representatives). E2E né bằng cách assert `issued`/`remaining` qua endpoint warehouse. Cần lưu ý cho team Sale.
- Dọn rác smoke test cũ (2 user @test.internal + kho "Smoke WH Quota").

### Checkpoint — 2026-06-29 (UI E2E Playwright + fix bug danh mục kho)
- Khảo sát/sửa setup UI E2E của user (`./e2e/`): (1) bug config — project `setup` không chạy vì `login.setup.ts` ngoài `testDir` → thêm `testDir: './auth'`; (2) `.env` creds sai (422) → chuyển sang user E2E `e2e_warehouse@test.local`. Login FE OK, storageState tạo được.
- Cập nhật skill `playwright-setup` (hrm-claude-config): mô hình auth thật (bảng employees/status=1/employee_has_roles), recipe tạo user E2E, lưu ý ô mật khẩu show/hide, E2E API-level, 4 row troubleshooting.
- **UI E2E phân hệ Kho** (`e2e/pages/Warehouse{Category,Receipt}Page.ts` + `tests/warehouse/receipt.spec.ts`): **3 PASS + 1 skip** — danh mục kho list, tạo phiếu Nhập (Nháp), (gửi duyệt+duyệt gate E2E_SUBMIT=1). Chạy: `cd e2e && nvm use 20 && npx playwright test tests/warehouse`.
- **BUG BE đã FIX**: drift bảng `warehouses` còn cột cũ `manager_id`, code dùng `manager_ids` (json) → tạo/sửa kho lỗi "Unknown column 'manager_ids'". Migration `Modules/Category/.../2026_06_30_000010_fix_warehouses_manager_ids.php` (thêm json `manager_ids`, drop `manager_id`); migrate dev OK; verify tạo Warehouse manager_ids=[1,2] lưu+cast đúng. Deploy VPS: chạy migrate.

### Checkpoint — 2026-06-29 (E2E hợp nhất + mở rộng — 12 PASS)
- GỘP toàn bộ E2E kho vào 1 project `./e2e/` (xoá `nhatlinh-client/e2e`). Config 4 project: `setup` (UI login storageState), `api-setup` (provision + login JWT → `.auth/api.json`), `chromium` (UI, testIgnore api.spec), `api` (request-only).
- **UI** (`tests/warehouse/`): tạo kho E2E mới (xác nhận fix manager_ids chạy thật trên UI), tạo phiếu Nhập (Nháp), **Gửi duyệt + Duyệt → Đã duyệt** (đã bật), tạo phiếu Xuất tự do (Nháp). POM: WarehouseCategory/Receipt/IssuePage.
- **API** (`tests/warehouse/api.spec.ts`): nhập 100, xuất 30→70, chặn vượt tồn 422, xuất theo HĐ remaining/issued/chặn vượt HĐ 422, auth 401.
- **Kết quả (verify độc lập): 12 passed + 1 skipped** (quotation submit gate E2E_SUBMIT). Chạy: `cd e2e && nvm use 20 && npx playwright test`.
- Lưu ý kỹ thuật: vue2-datepicker form xuất không nhận fill sau khi Select2 đóng → test set qua `page.evaluate(vm.form.issue_date)` (điểm yếu nhỏ: không test datepicker qua thao tác thật). Config có `retries:1` (ổn định dev server).
- Vệ sinh: api fixtures tự dọn theo marker mỗi lần provision; phiếu/kho do UI test tạo (KHO.E2E<ts>) tích luỹ trên DB dev — có `e2e_teardown.php` cho user+api fixtures, chưa dọn UI-created.

### Checkpoint — 2026-06-29 (WRAP UP cuối session)
Vừa hoàn thành: Phase 1 (Nhập) + Phase 2 (Xuất) BE+FE đầy đủ + final review PASS; chuyển Danh mục Kho sang phân hệ Quản lý kho; vá race tồn (StockService lockForUpdate); fix bug BE `warehouses.manager_ids` (migration); bộ E2E Playwright hợp nhất `./e2e/` (UI+API) **12 passed**; cập nhật skill `playwright-setup`. Permission DB dev đã seed + gán role 1 (1103/1104 type=10, 1124-1129).
Đang làm dở: Không có — dừng ở mốc bàn giao theo yêu cầu user (user tự test).
Bước tiếp theo: User tự test FE + chạy E2E (`cd e2e && nvm use 20 && npx playwright test`); commit khi đạt (chưa commit — CLAUDE.md). Feature tiếp: Phase 3 — Chuyển kho (chờ user).
Blocked:

## Phase 2.1 — Loại nhập + Đơn giá nhập + Fix bug chữ trắng
> Bổ sung theo yêu cầu: phiếu nhập có loại nhập (HĐ mua delay / KH trả lại / Nhập khác), đơn giá nhập (ghi nhận giá vốn, KHÔNG ảnh hưởng tồn), ngày nhập mặc định hôm nay; fix mã hàng chữ trắng.

### Bug
- [x] B1. Mã hàng hoá chữ trắng (báo giá/nhập/xuất): nguyên nhân theme override `$secondary:$white` → `.text-secondary`=trắng. Fix: thay `text-secondary` bằng `color:#6b7280` ở QuotationForm/WhReceiptForm/WhIssueForm. (Contract render plain → không bị.)

### Backend
- [x] B2. Migration alter `wh_receipts` (+receipt_type default 3, +contract_id, +total_amount) + `wh_receipt_items` (+contract_item_id, +unit_price, +amount). Đã migrate dev.
- [x] B3. Entity WhReceipt (RECEIPT_TYPE_* 1/2/3 + RECEIPT_TYPES + accessor receipt_type_name + relation contract + fillable/cast) ; WhReceiptItem (fillable + casts float + relation contractItem).
- [x] B4. WhReceiptService: headerData(+receipt_type/contract_id), syncItems(+unit_price/amount/contract_item_id), refreshTotal (sum amount→total_amount), method saleContractItems($contractId) (dòng HĐ bán đã duyệt + đơn giá).
- [x] B5. WhReceiptRequest: receipt_type required in:1,2,3; contract_id required_if=2; items.*.unit_price nullable; items.*.contract_item_id nullable exists.
- [x] B6. Resource list (+receipt_type/name, total_amount) + detail (+receipt_type_name, contract_code, total_amount, item unit_price/amount/contract_item_id). Route GET sale-contract/{id}/items (trước /{id}). Controller saleContractItems + eager-load contract.
- Smoke test tinker: type=3 total=5000 (qty5×1000) OK; saleContractItems trả dòng + đơn giá OK.

### Frontend
- [x] B7. store warehouse-receipt: action saleContractItems.
- [x] B8. WhReceiptForm rework: radio Loại nhập (1 disable+alert "đang phát triển" + khoá nút lưu; 2 KH trả lại→select HĐ bán→load dòng+đơn giá read-only, SL nhập; 3 Nhập khác→picker, đơn giá nhập tay); ngày nhập default hôm nay (valueType Y-m-d); cột Đơn giá+Thành tiền + Tổng tiền footer.
- [x] B9. Detail page: +Loại nhập, +Hợp đồng, cột Đơn giá/Thành tiền + dòng Tổng tiền. List page: +cột "Loại nhập" (receipt_type_name).

### Validate SL nhập trả (KH trả lại)
- [x] B10. KH trả lại không được nhập trả vượt SL **đã xuất bán còn lại** của HĐ. BE: `saleContractItems` trả thêm `issued`+`returnable` (returnable = đã xuất bán − đã trả, quy ĐVT dòng HĐ); `approve` gọi `assertReturnRemaining` (lock dòng HĐ, gộp theo contract_item_id, trừ đã trả ở phiếu khác đã duyệt) → ValidationException nếu vượt; helper issuedBase/returnedBase + relation WhReceiptItem::receipt(). FE: cột "Có thể trả" (returnable), validate inline SL≤returnable, filter dòng returnable>0, fillForm edit reload+merge. Smoke test: vượt(31>30) CHẶN, đúng(30) duyệt OK tồn+30, trả hết→returnable=0. PASS.

### Checkpoint — 2026-06-30 (Loại nhập + đơn giá + fix chữ trắng)
Vừa hoàn thành: BE (2 migration đã migrate dev, entity/service/request/resource/route/controller) + FE (store, form rework 3 loại nhập, detail, list) + fix bug mã hàng chữ trắng 3 form. Smoke test BE PASS. Branch `quotation` (cả 2 repo). Chưa commit.
Đang làm dở: Không.
Bước tiếp theo: User restart dev server + re-login → test FE (tạo phiếu Nhập khác có đơn giá→tổng; KH trả lại chọn HĐ→load dòng+giá+"Có thể trả", chặn nhập trả vượt SL đã xuất bán; HĐ mua disable; mã hàng hết trắng ở 4 màn). Lưu ý deploy VPS: chạy migrate (2 migration mới).
Blocked:

## Phase 2.2 — Loại xuất + Đơn giá xuất + validate net
> Yêu cầu: phiếu xuất có loại xuất (Xuất bán theo HĐ / Xuất khác); xuất theo HĐ load TOÀN BỘ dòng + checkbox chọn/bỏ + chọn-all, mặc định chọn + SL=còn lại; đơn giá+thành tiền theo đơn giá HĐ; validate SL đã xuất (net = tổng đã xuất + lần này − đã nhập trả lại) ≤ SL HĐ.

### Backend
- [x] C1. Migration wh_issues +total_amount; wh_issue_items +unit_price/amount. Đã migrate dev.
- [x] C2. WhIssue: ISSUE_TYPES (1 "Xuất bán theo hợp đồng", 2 "Xuất khác") + accessor issue_type_name + fillable total_amount + cast. WhIssueItem: fillable +unit_price/amount + casts.
- [x] C3. WhIssueService: syncItems +unit_price/amount + refreshTotal; contractRemaining +unit_price + remaining **net** (trừ returnedBase); assertContractRemaining dùng netIssued = đã xuất − đã trả lại; helper returnedBase (WhReceiptItem approved type=2).
- [x] C4. WhIssueResource list (+total_amount, issue_type_name accessor) + DetailWhIssueResource (+total_amount, item unit_price/amount).
- Smoke test: contractRemaining trả unit_price; trả lại 10 → remaining 0→10 (net OK); issue store total=35; chặn vượt (đã có ở quota cũ + net). PASS.

### Frontend
- [x] C5. WhIssueForm: label "Xuất bán theo hợp đồng"/"Xuất khác"; HĐ→load TOÀN BỘ dòng (bỏ filter remaining>0), checkbox/row + "Chọn tất cả"/"Bỏ chọn tất cả" + header checkbox, mặc định chọn (remaining>0) + SL=còn lại, cột Đơn giá+Thành tiền + Tổng tiền, validate SL≤còn lại (chỉ dòng chọn), payload chỉ dòng chọn + unit_price. fillForm edit: selected=dòng đã lưu.
- [x] C6. Issue detail page (+Đơn giá/Thành tiền/Tổng); issue list filter/cột loại xuất đổi label mới.

### Bổ sung phân hệ
- [x] C7. Thêm thẻ "Quản lý kho" (icon_kho.svg → /warehouse/receipt) vào **màn chọn phân hệ sau login** `pages/index.vue` (sau thẻ Kinh doanh), đồng nhất pattern các thẻ khác (không gate quyền). Trước đó mới có ở popup topbar BasicSubsystem.vue.

### Tinh chỉnh form xuất (UX)
- [x] C8. Đưa select Hợp đồng lên header (sau Loại xuất, trước Người nhận); section dưới đổi tên "Chi tiết xuất" + gợi ý khi chưa chọn HĐ. Option HĐ = "Số HĐ - Khách hàng - Người lập" (code - customer_name - employee_create_name; list resource đã có sẵn các field này → không sửa BE).

- [x] C9. Tinh chỉnh form xuất (UX): (1) option HĐ — Số HĐ in HOA + đầu dòng (user chọn cách này thay vì sửa V2BaseSelect dùng chung để bold); (2) redesign nút "Chọn tất cả"/"Bỏ chọn tất cả" (btn pill + màu) + badge "Đã chọn X / Y hàng hoá" (computed selectedCount); (3) "Xuất khác" thêm cột Đơn giá (nhập tay) + Thành tiền + Tổng tiền (onPickProducts/fillForm/payload +unit_price; BE issue đã hỗ trợ unit_price/amount/total). totalAmount: type 1 tính dòng đã chọn, type 2 tính tất cả.

- [x] C10. (1) Ngày xuất mặc định = hôm nay (WhIssueForm todayStr + valueType Y-m-d), cho chọn lại; ngày nhập đã default sẵn. (2) Nút "Lưu & Duyệt" trên form tạo/sửa cả nhập+xuất: hiện khi user có quyền duyệt (CheckPermission mixin: hasAPermission('Duyệt phiếu nhập kho'|'Duyệt phiếu xuất kho')) → submitForm('approve') = save→submit→approve liên tiếp. submitForm refactor action 'save'|'submit'|'approve'. BE vẫn enforce middleware checkPermission ở route approve (an toàn 2 lớp).

### Checkpoint — 2026-06-30 (Loại xuất + đơn giá xuất + validate net)
Vừa hoàn thành: BE (2 migration migrate dev; entity/service net+đơn giá/2 resource) + FE (form load-all+checkbox+chọn-all+giá+tổng, detail, list label). Smoke test BE PASS (net remaining, total). Branch `quotation`, chưa commit.
Đang làm dở: Không.
Bước tiếp theo: User restart dev + re-login → test FE (xuất bán theo HĐ load toàn bộ dòng, chọn/bỏ/chọn-all, SL mặc định=còn lại, đơn giá+thành tiền+tổng, chặn vượt SL net; xuất khác giữ nguyên). Deploy VPS: chạy 2 migration mới. Lưu ý: validate xuất nay TRỪ số đã nhập trả lại (net) — khác trước.
Blocked:

## Phase 3 — Chuyển kho
> Chuyển hàng giữa 2 kho nội bộ. CHỈ số lượng (không giá). Tồn đổi khi DUYỆT: giảm kho nguồn + tăng kho đích. 1 lần duyệt.

### Backend
- [x] T1. Migration `wh_transfers` (from/to_warehouse_id, transfer_date, status, approved/reject, company/dept/part) + `wh_transfer_items` (product, unit, conversion_rate, quantity, quantity_base). Đã migrate dev.
- [x] T2. Entity WhTransfer (HasStatusBadge, getNextCode `PC-`, relations from/to warehouse + employee, isCan*) + WhTransferItem.
- [x] T3. WhTransferService: CRUD + submit/approve/reject. **approve**: assertEnough(kho nguồn) gộp theo product → mỗi dòng 2 movement OUT(− type4 nguồn)+IN(+type3 đích), transaction+lockForUpdate. `warehouseStock(id)` trả map tồn khả dụng (base).
- [x] T4. Request (from/to required + `different`, qty>0) + 2 Resource + Controller (+warehouseStock) + routes /v1/warehouse/transfers (+ warehouse/{id}/stock trước /{id}) middleware 1131/1132.
- [x] T5. Seeder permission **1130 Xem / 1131 Thêm sửa / 1132 Duyệt** type=10 nhóm "Chuyển kho". DB dev: ĐÃ seed + gán role 1 + cache clear (insert an toàn, không truncate).
- Smoke test tinker: nạp tồn 100 → chuyển 30 (nguồn 100→70, đích 0→30) OK; warehouseStock map đúng; chặn vượt tồn (71>70) 422. PASS.

### Frontend
- [x] T6. store `warehouse-transfer` (+warehouseStock).
- [x] T7. WhTransferForm: kho nguồn/đích (đích loại kho nguồn + validate `sameWarehouse`), ngày chuyển **default hôm nay**, ProductPickerModal (chặn mở khi chưa chọn kho nguồn), cột **Tồn khả dụng** (quy về ĐVT dòng) + **validate SL ≤ tồn** inline, đổi kho nguồn → reload tồn. Footer: Lưu / Lưu & Gửi duyệt / **Lưu & Duyệt** (CheckPermission 'Duyệt phiếu chuyển kho').
- [x] T8. Pages transfer/ (index list + create + _id/index detail workflow + _id/edit) + menu "Chuyển kho" (ri-arrow-left-right-line) vào warehouseItems (dùng chung guard/sidebar/layout).

### Bổ sung UI phân hệ kho
- [x] T9. Thẻ "Quản lý kho" (icon_kho.svg → /warehouse/receipt) vào **màn chọn phân hệ sau login** `pages/index.vue`.
- [x] T10. **Icon + title header sidebar** phân hệ kho: `layouts/default-sidebar.vue` thêm block `firstUri==='warehouse'` (classLogo `ri-store-2-line`, urlLogo `/warehouse/receipt`, titleTopbar "QUẢN LÝ KHO") — trước đó header trống khi ở /warehouse/*.

### Checkpoint — 2026-07-01 (CODE HOÀN THÀNH Phase 3 Chuyển kho)
Vừa hoàn thành: BE (2 migration migrate dev; entity/service 2-movement/request/2 resource/controller/route; permission 1130-1132 seed+gán role 1) + FE (store, WhTransferForm tồn khả dụng+validate, 4 page, menu). Smoke test BE PASS. Branch `quotation`, chưa commit.
Bước tiếp theo: User restart dev + re-login (role 1 đã có 1130-1132) → test menu "Chuyển kho", tạo phiếu (chọn kho nguồn→tồn khả dụng hiện, chặn vượt tồn, kho đích≠nguồn), Lưu & Duyệt → tồn 2 kho đổi. Deploy VPS: migrate 2 bảng + seed/gán quyền 1130-1132. Feature kế: Phase 4 Kiểm kê.
Blocked:

## Phase 4 — Kiểm kê — *chưa lên task*
## Phase 5 — Báo cáo Tồn kho + Thẻ kho
> Spec §5+§7 (đã chốt). 2 báo cáo read-only + export Excel. Không CRUD, không đổi tồn.
> - **Tồn kho**: list `inventories` join product/warehouse, lọc kho/loại hàng/keyword + ẩn tồn 0; mỗi dòng = (kho × hàng hoá) tồn ĐVT cơ bản + cột "Tổng toàn hệ thống" (SUM mọi kho theo hàng).
> - **Thẻ kho**: chọn hàng hoá (bắt buộc) + kho (tùy) + khoảng ngày → tồn đầu kỳ (SUM movement < từ_ngày), list movement trong kỳ (ngày/loại/số phiếu link/nhập/xuất/tồn luỹ kế), tồn cuối kỳ. Running balance ở BE.

### Backend
- [x] R1. Permission **1136 Xem báo cáo tồn kho / 1137 Xem thẻ kho** type=10 nhóm "Báo cáo kho" (seeder; 1133-1135 chừa Kiểm kê). Seed DB dev + gán role 1 (insertOrIgnore, không truncate).
- [x] R2. `WhReportService`: `inventoryPaginated/inventoryRows($f)` (rows kho×hàng + total_system per product, sort mã hàng, ẩn tồn 0 mặc định) · `stockCard($productId,$warehouseId,$from,$to)` (opening = SUM movement < from, rows running balance, closing, resolve số phiếu + route theo source_type). +relations Inventory→product/warehouse.
- [x] R3. `WhReportController`: inventory / inventoryExport / stockCard / stockCardExport (stock-card thiếu product_id → 422).
- [x] R4. Exports: `InventoryExport`, `StockCardExport` (FromCollection+WithHeadings+WithMapping+ShouldAutoSize; thẻ kho có dòng Tồn đầu/cuối kỳ).
- [x] R5. Routes `/v1/warehouse/reports/inventory(+/export)` · `/stock-card(+/export)` middleware checkPermission. `InventoryReportResource` trả nguyên array (giữ meta phân trang).
- **E2E test (auth role 1)**: inventory 200 total=5; stock-card p64 opening 0→closing 40 (in 1140/out 1100, 10 dòng); thiếu product 422; 2 export ra xlsx hợp lệ (Microsoft Excel 2007+). PASS.

### Frontend
- [x] R6. store `warehouse-report.js` (inventory / stockCard / inventoryExport / stockCardExport qua apiExportExcel).
- [x] R7. `pages/warehouse/report/inventory.vue` (filter Kho/Loại hàng/keyword + checkbox ẩn tồn 0 + V2BaseDataTable phân trang + cột Tồn tại kho/Tổng toàn hệ thống + nút Xuất Excel).
- [x] R8. `pages/warehouse/report/stock-card.vue` (chọn hàng hoá bắt buộc + kho + range ngày + nút Xem; summary Tồn đầu/nhập/xuất/cuối + bảng ledger running balance + số phiếu link + Xuất Excel).
- [x] R9. Menu `warehouse.js` +"Báo cáo tồn kho" (ri-bar-chart-box-line) +"Thẻ kho" (ri-file-list-3-line). Màn Role tự hiện nhóm "Báo cáo kho" (filterPermission(10)).
- Lưu ý API component: V2BaseButton dùng `interactable`/`isShowLoading` (không có block/loading/disabled) — đã map đúng. V2BaseDatePicker default Y-m-d. V2BaseCheckbox single-mode dùng prop `label`.

### UI polish
- [x] UI2. Redesign file Excel 2 báo cáo (tồn kho + thẻ kho) đẹp + in A4: chuyển FromCollection → **FromView (blade) + WithEvents**. Banner công ty (tải ảnh `companies.header` S3 về file tạm → nhúng `<img>` local), tiêu đề lớn, dòng bộ lọc rõ ràng (kho/loại hàng/từ khoá/ẩn tồn 0 hoặc kỳ), bảng border inline, font Times New Roman, **PageSetup A4 portrait fitToWidth**. Trait chung `Exports/Concerns/ReportPageSetup` (A4 + width cột + download banner). Controller lấy công ty qua `current_company_role`. Test E2E: 2 file 200, có `xl/media` banner + `paperSize=9`/`fitToWidth=1`, tiêu đề+bộ lọc render đúng. PASS.
- [x] UI1. Redesign trang Thẻ kho hiện đại: header gọn nền trắng (mã hàng badge + tên; ĐVT/kho/kỳ dạng text nhỏ) — bỏ hero gradient theo yêu cầu; 4 stat card có icon + màu (tồn đầu/nhập/xuất/cuối), bảng ledger tinh gọn (badge loại GD theo màu type, +nhập xanh/−xuất đỏ, số phiếu link chip, hover, dòng Tồn đầu/cuối kỳ nổi bật), empty/intro state. Chỉ FE (`report/stock-card.vue`), không đổi logic/API.

### Bug fix
- [x] BUG. Datepicker ngày nhập/xuất/chuyển sai token `valueType="Y-m-d"` (kiểu PHP) → vue2-datepicker không parse được `todayStr()` (mất giá trị mặc định) + chọn ngày mới nhảy về đầu năm. Sửa cả 3 form (WhReceiptForm/WhIssueForm/WhTransferForm) → `valueType="YYYY-MM-DD"` (đúng token, khớp todayStr + BE Y-m-d).

### Checkpoint — 2026-07-01 (CODE HOÀN THÀNH Phase 5 Báo cáo kho)
Vừa hoàn thành: BE (WhReportService + Controller + 2 Export + Resource + 4 route; permission 1136/1137 seed+gán role 1) + FE (store, 2 trang report inventory/stock-card, menu 2 mục). E2E backend auth PASS (inventory/stock-card/422/2 export xlsx). Branch `quotation`, chưa commit.
Bước tiếp theo: User restart dev + re-login (role 1 đã có 1136/1137) → test menu "Báo cáo tồn kho"/"Thẻ kho"; lọc + xuất Excel; thẻ kho chọn hàng hoá→số phiếu link về phiếu. Deploy VPS: chạy seeder (hoặc insert 1136/1137) + gán quyền. Feature kế: Phase 4 Kiểm kê.
Blocked:

---

### Checkpoint — 2026-06-29 (lập plan Phase 1)
Vừa hoàn thành: Brainstorming + spec đầy đủ + plan chi tiết Phase 1 (10 task).
Đang làm dở: Chưa code. Chờ chọn cách thực thi (subagent-driven vs inline).
Bước tiếp theo: Thực thi Task 1 (scaffold module Warehouse).
Blocked:

### Checkpoint — 2026-06-29 (CODE HOÀN THÀNH Phase 1 + FINAL REVIEW PASS)
Vừa hoàn thành: **Toàn bộ 10 task Phase 1 (Engine + Nhập kho) BE+FE**, subagent-driven (mỗi task implementer + reviewer + fix khi cần). Final review opus: **SẴN SÀNG BÀN GIAO, 0 Critical/Important**. Chưa commit (CLAUDE.md).
- **BE** (`Modules/Warehouse`): module scaffold; 4 migration (stock_movements, inventories, wh_receipts, wh_receipt_items) đã migrate; 5 Entity (HasStatusBadge, getNextCode PN-); `StockService` (postMovement insertOrIgnore→lockForUpdate, getAvailable, setAbsolute, assertEnough→ValidationException 422); `WhReceiptService` (CRUD + submit/approve→ghi tồn/reject, quy đổi quantity_base, reject_reason clear); Request + 2 Resource + Controller (transaction + lockForUpdate approve + rethrow ValidationException) + 8 route gắn checkPermission; permission 1124-1126 type=10 trong seeder. Smoke test tinker PASS (engine cộng dồn/chặn tồn; approve→tồn quy đổi đúng; chặn duyệt lại).
- **FE** (`nhatlinh-client`): store warehouse-receipt; WhReceiptForm (ProductPickerModal tái dùng, ĐVT quy đổi, validate inline) + create/edit; list (filter + V2BaseBadge + sort) + detail (workflow footer: Gửi duyệt/Duyệt confirm/Từ chối modal, gate quyền) + 2 modal; menu nhóm "Quản lý kho" wired 3 nơi (checkPermission/Sidebar/default) theo pattern saleItems.
- **Minor còn (tech-debt, không chặn)**: duplicate index receipt_id; WhReceiptItem thiếu cast (Resource đã float); ProductPickerModal chữ "báo giá"; 422 chưa map inline từng field.
Permission DB dev: **ĐÃ XONG** — chạy `PermissionsTableSeeder` (truncate+reseed, theo yêu cầu user để dùng làm nguồn deploy VPS), permissions 606→609 (1124-1126 type=10 group "Nhập kho"); role_has_permissions giữ nguyên 606; gán 1124-1126 cho role 1 (Admin, nay 609 quyền); cache:clear. Deploy VPS: chỉ cần chạy seeder rồi gán quyền cho role qua màn Role (hoặc pivot).
Bước tiếp theo (cần USER trên dev server, FE Node v12 không build ở đây):
  1. Restart dev server, re-login (Admin role 1) → test menu "Quản lý kho"/"Nhập kho" hiện; test 403/route-guard với user thiếu quyền.
  3. Test E2E: tạo phiếu nhập (chọn kho/NCC/hàng hoá/ĐVT) → Lưu & Gửi duyệt → Duyệt (confirm) → kiểm tồn tăng (qua tinker `inventories`); test Từ chối→sửa→gửi lại; test chặn sửa/xoá khi đã duyệt.
  4. Commit 2 repo khi đạt.
Bước kế tiếp (feature): brainstorm/triển khai **Phase 2 — Xuất kho** (gắn HĐ + cập nhật "Số lượng đã xuất").
Blocked:
