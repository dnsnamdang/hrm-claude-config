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

## Phase 3 — Chuyển kho — *chưa lên task*
## Phase 4 — Kiểm kê — *chưa lên task*
## Phase 5 — Báo cáo Tồn kho + Thẻ kho — *chưa lên task*

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
