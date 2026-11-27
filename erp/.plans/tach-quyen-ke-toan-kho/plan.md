# Tách quyền "Kế toán kho" — Plan 2: ERP re-point (TanPhatDev) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Đổi **mọi** chỗ ERP (TanPhatDev) đang kiểm/định tuyến/thông báo/đếm theo quyền gộp cũ `accounting.ke_toan_kho.manage` (gồm cả chỗ tham chiếu bằng **tên** `'Kế toán kho'`) sang **36 quyền mới** per-màn/phiếu đã khai ở Plan 1 — map 1-1 theo design §5, chỗ gộp → **OR của mọi mã thành viên** theo §6 — để không ai mất quyền và mỗi khoá chỉ mở đúng phiếu của nó. Quyền cũ **vẫn còn**, chưa deprecate (bước §8.6 sau Plan 3).

**Architecture:** 36 mã mới đã có trong Catalog + bảng `permissions` (Plan 1 ✓). Plan này chỉ sửa **chỗ dùng** trong ERP: `->can('<code>')`, middleware route `checkPermission:<code>`, `Employee::withPermission('<code>')`, `NotificationHelper::sendNotifyWithPermission('<code>', …)`, `Warehouse::getForFilterByCurrentUser('<code>')`, nhánh đếm dashboard `HomeController`, và menu blade `@if(… ->can('…'))`. Mỗi lời gọi đổi sang mã mới của **đúng** màn/phiếu đó (design §5). Chỗ một `->can()` gộp nhiều phiếu (menu OR-chain, nhánh dashboard trải nhiều loại, danh sách tab) → thay bằng **OR tất cả mã thành viên** (§6), không chọn đại 1 mã. Mốc RED→GREEN toàn plan = một test **quét tĩnh** khẳng định không còn tham chiếu mã cũ/tên cũ ngoài Catalog+alias; mỗi nhóm thêm vài test hành vi gate đại diện (mã mới mở đúng cửa, chỉ-mã-cũ bị chặn).

**Tech Stack:** PHP 7.x, Laravel 6, Spatie permission qua `App\Support\Permissions\PermissionChecker`. PHPUnit với trait `DatabaseTransactions` + concern `Tests\Feature\Rbac\Concerns\ErpGateFixture` + seeder `Tests\Feature\Rbac\Concerns\AccountingCatalog`. DB test riêng `hrm_erp_rbac_test` (KHÔNG phải prod). Nhánh `develop_02`.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/tach-quyen-ke-toan-kho/design.md` (APPROVED) — plan này lập luận từ design đó; đọc §5 (36 mã + bản đồ gate ERP theo file:line), §6 (mặt cắt ngang: menu/realtime/notify/dashboard/filter/is_warehouse_accountant), §7 (rủi ro, nhất là §7.1 tham chiếu theo tên), §11 (verify). Phần "Gate ERP" của mỗi dòng §5 là **thẩm quyền map** cho plan này.

## Global Constraints

- **36 mã mới ĐÃ LIVE** trong `permissions` (Plan 1 ✓, commit hrm-api `78093712c`); mã cũ `accounting.ke_toan_kho.manage` **vẫn active** (chưa deprecate). Plan 2 **không** đụng Catalog hrm-api, **không** deprecate, **không** chạy `catalog-sync`, **không** push/deploy/gop_db.
- **Thẩm quyền map = design §5** (cột "Gate ERP", file:line) + **§6** (cross-cut). Mỗi lời gọi `ke_toan_kho` → mã mới của đúng màn/phiếu file đó xử lý. Nghi ngờ map chỗ nào → đối chiếu §5, không tự đoán.
- **Chỗ GỘP → OR mọi mã thành viên, KHÔNG chọn 1 mã** (§6): menu OR-chain, nhánh đếm dashboard trải nhiều phiếu, list/tab trả nhiều loại YC. Chỗ **đơn-phiếu** map 1-1.
- **Giữ nguyên toán hạng OR không phải `ke_toan_kho`** khi thay: `warehouse.thu_kho.manage`, `accounting.ke_toan_mua_hang.*` (#10,#11), `is_warehouse_accountant`, `xuat_hang_vuot_han_muc`, các mã `hang_muon_*` (dashboard 1006)… — chỉ thay toán hạng `ke_toan_kho`.
- **KHÔNG đụng `is_warehouse_accountant` / bảng `WarehouseAccountant` / `Employee::getAccoungtingWarehouses()`** — cờ tra bảng, độc lập quyền này (§6). Nhiều file dùng nó; để y nguyên.
- **KHÔNG đổi/không tách Redis channel chuỗi `"ke_toan_kho".$warehouse_id`** (`app/Console/Commands/BorrowWarning.php:108`, `PrepickWarning.php:113`, và các publish Prepick*/WarehouseImport/WarehouseExport; subscribe `server_node/server.js`) — tín hiệu "có phiếu mới, refresh" theo kho, coarse có chủ đích (§6). Grep `ke_toan_kho` bắt trúng các dòng này nhưng chúng **không phải** quyền → để nguyên.
- **Group route gate một phần (Nhóm I `warehouse_reports`)**: rà **từng dòng** route, KHÔNG gán cả group (route anh em 1584-1587,1589,1591-1598 không gate — giữ không gate). Xem §5 ⚠️ dưới bảng Nhóm I.
- **Tham chiếu theo TÊN `'Kế toán kho'`** (không phải code) phải grep riêng chuỗi; grep theo code bỏ sót (§7.1). ERP có ~9 file chứa chuỗi — phân biệt **nhãn hiển thị** (giữ) vs **cổng kiểm/alias** (đổi).
- **Fail-closed đã kiểm (design §7.5):** sau khi deprecate (Plan sau), chỗ sót → `->can('ke_toan_kho.manage')`=false ⇒ chặn (ồn ào), không âm thầm mở. Nên bỏ sót = anti-goal, nhưng không âm thầm nguy hiểm.
- **Test một tiến trình** trên `hrm_erp_rbac_test` (`DatabaseTransactions` tự rollback). Mã mới seed trong transaction qua `AccountingCatalog` — nếu không seed, cửa kiểm mã ném `UnknownPermissionCode` ở local/testing.
- Co-author trong commit message: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

## Review Focus

- **Chỗ OR-chain bị thay cả cụm bằng 1 mã** làm rớt đồng-chủ-thể hợp lệ (người có `thu_kho`/`ke_toan_mua_hang`/`is_warehouse_accountant`/`hang_muon_*` mất quyền thấy/làm): mỗi chỗ gộp phải là **OR đủ mã thành viên + giữ operand ngoài `ke_toan_kho`**. → Task 11 test `test_menu_or_chain_giu_operand_ngoai` + Task 2–10 test chỉ-mã-cũ-bị-chặn chạy trên gate **đã** đổi (không chạm operand khác).
- **Tham chiếu theo TÊN `'Kế toán kho'`** (alias/hằng), grep-code bỏ sót (§7.1): phải đổi chỗ **cổng kiểm/alias**, giữ chỗ **nhãn hiển thị**. → Task 1 liệt kê đủ (grep code **và** chuỗi tên) + Task 12 static-scan quét **cả** code lẫn chuỗi tên ở ngữ cảnh gate.
- **Group route `warehouse_reports` gán nhầm cả group** → gate luôn route lẽ ra mở (Nhóm I): → Task 2 test route anh em **không** gate vẫn mở cho người không có mã báo cáo.
- **Notify re-point sai mã** → đúng loại phiếu nhưng người nhận lệch (gửi theo mã phiếu khác): → Task 11 test `test_notify_resolver_dung_ma_tung_phieu` (người chỉ có mã phiếu X nhận thông báo phiếu X, không nhận phiếu Y).
- **Lỡ đổi/tách Redis channel** → realtime refresh gãy: → Task 12 static-scan `test_redis_channel_ke_toan_kho_giu_nguyen` assert chuỗi `"ke_toan_kho".` còn nguyên ở Console/publish (đây là ngoại lệ hợp lệ của quét tĩnh).

---

## File Structure

- `tests/Feature/Rbac/Concerns/AccountingCatalog.php` — **sửa**: thêm 36 mã mới `accounting.ke_toan_kho_*` vào `const MAP` (mỗi mã `[[], []]` = `scopes=[]`, `legacy=[]`), giữ mã cũ. (Để mọi test Plan 2 seed được mã mới.)
- `tests/Feature/Rbac/ErpKeToanKhoRepointTest.php` — **tạo**: test **quét tĩnh** toàn repo (mốc RED→GREEN của cả plan) + ngoại lệ Redis channel.
- `tests/Feature/Rbac/ErpKeToanKhoGateTest.php` — **tạo**: test hành vi gate đại diện cho 9 nhóm (seed mã mới, gán lẻ 1 mã → mở đúng cửa, chỉ-mã-cũ → chặn).
- `.plans/tach-quyen-ke-toan-kho/erp-mapping.md` — **tạo** (trong ERP/.plans): bảng map ĐẦY ĐỦ từng chỗ-dùng → mã mới (điều kiện ra của Task 1, có review).
- **Sửa (theo §5, không liệt lại ở đây):** `app/Model/**` (~30 dòng: *Request/Import/Export/Transfer/Allocation/Borrow\*/DeliveryPayment\*/Wr\*…*), `app/Http/Controllers/**` + `Middleware` (~18), `routes/web.php` (middleware `checkPermission:` + route group), `resources/views/layouts/topmenubar.blade.php` (14) + `topmenubar_old.blade.php` (11), `app/Http/Controllers/HomeController.php` (dashboard 1006/1020/1030/1380/2201).
- **KHÔNG sửa:** `app/Console/Commands/BorrowWarning.php`, `PrepickWarning.php` (Redis channel), mọi chỗ `is_warehouse_accountant`/`WarehouseAccountant`/`getAccoungtingWarehouses`, `topmenubar_old_2.blade.php` (0 chỗ).

---

### Task 1: Inventory đầy đủ + AccountingCatalog + mốc quét tĩnh RED

**Files:**
- Create: `.plans/tach-quyen-ke-toan-kho/erp-mapping.md` (ERP/.plans)
- Modify: `tests/Feature/Rbac/Concerns/AccountingCatalog.php`
- Create/Test: `tests/Feature/Rbac/ErpKeToanKhoRepointTest.php`

**Interfaces:**
- Produces:
  - `AccountingCatalog::MAP` chứa 37 mã (cũ + 36 mới); `AccountingCatalog::seed()` trả `code=>id` cho cả 36 mã mới (các task sau dùng).
  - `erp-mapping.md`: với **mỗi** chỗ-dùng (file:line) một hàng `file:line | dạng (can/middleware/notify/withPermission/filter/dashboard/menu) | mã mới đích (hoặc OR-set) | nhóm §5 | ghi chú`. Chỗ gộp ghi rõ OR-set. Chỗ theo-tên và chỗ cố-ý-giữ (Redis/is_warehouse_accountant) đánh dấu riêng.

- [x] **Step 1: Dựng danh sách chỗ-dùng đầy đủ.** Grep repo (trừ vendor/node_modules/storage/public/tests) **cả 2 kiểu**: code `ke_toan_kho` và chuỗi `'Kế toán kho'`. Phân loại mỗi hit: cổng kiểm (`->can`, `checkPermission:`, `hasPermissionTo`), notify (`sendNotifyWithPermission`, `withPermission`, `getForFilterByCurrentUser`, dashboard đếm), menu blade, **giữ-nguyên** (Redis channel, `is_warehouse_accountant`, nhãn hiển thị). Đối chiếu với design §5 — chỗ nào §5 chưa có thì map thêm, chỗ §5 có mà grep không thấy thì ghi chú (có thể đã đổi/đổi tên). Ghi tất cả vào `erp-mapping.md`.
- [x] **Step 2: Thêm 36 mã mới vào `AccountingCatalog::MAP`** — mỗi mã `[[], []]` (scopes rỗng, không alias tên). Danh sách 36 slug/kind lấy từ Plan 1 `KeToanKhoSplitMap::newCodes()` / design §5 (5 `.view` + 31 `.manage`). Giữ dòng mã cũ.
- [x] **Step 3: Viết test quét tĩnh (RED).** `ErpKeToanKhoRepointTest`:
```php
public function test_khong_con_cong_kiem_ma_cu()
{
    // grep app/ + resources/views/ cho các DẠNG cổng kiểm mã cũ:
    //   ->can('accounting.ke_toan_kho.manage'), checkPermission:accounting.ke_toan_kho.manage,
    //   withPermission('accounting.ke_toan_kho.manage', sendNotifyWithPermission('accounting.ke_toan_kho.manage'
    // assertSame([], $hits) — KÈM danh sách file:line khi fail.
}
public function test_khong_con_cong_kiem_theo_ten()
{
    // grep chuỗi 'Kế toán kho' trong NGỮ CẢNH cổng (hằng PERMISSION_*, alias lookup, ->can theo tên),
    // loại trừ nhãn hiển thị (view blade text, label menu). assertSame([], $hits).
}
public function test_redis_channel_ke_toan_kho_giu_nguyen()
{
    // assert chuỗi '"ke_toan_kho".' CÒN trong BorrowWarning.php + PrepickWarning.php (ngoại lệ hợp lệ — coarse signal).
}
```
- [x] **Step 4: Chạy — 2 test đầu FAIL (còn ~139 chỗ), test Redis PASS.**

Run: `vendor/bin/phpunit --filter ErpKeToanKhoRepointTest`
Expected: `test_khong_con_cong_kiem_ma_cu` + `test_khong_con_cong_kiem_theo_ten` FAIL (liệt kê chỗ còn lại); `test_redis_channel…` PASS.

- [x] **Step 5: Commit** (test RED + catalog + mapping doc).

```bash
git add tests/Feature/Rbac/Concerns/AccountingCatalog.php tests/Feature/Rbac/ErpKeToanKhoRepointTest.php
git commit -m "test(rbac): mốc quét tĩnh re-point ke_toan_kho (RED) + seed 36 mã + inventory"
```

> `erp-mapping.md` ở ERP/.plans (symlink hrm-claude-config), KHÔNG commit vào repo code.

---

### Task 2: Nhóm I — Màn báo cáo/tra cứu (route + Tồn đầu kỳ)

**Files:** Modify theo §5 Nhóm I: `routes/web.php:1574-1599,1687` (middleware `checkPermission:` từng dòng), controller báo cáo tương ứng. Test: `tests/Feature/Rbac/ErpKeToanKhoGateTest.php`.

**Interfaces:**
- Consumes: `AccountingCatalog::seed()`, `ErpGateFixture` (`buildGateFixture`, `makeEmployee`, `makeRole`, `grant`, `assignRole`, `loginErp`).
- Produces: route báo cáo #1–#5 gate bằng mã `.view` tương ứng; #6 `ke_toan_kho_ton_dau_ky.manage`.

- [x] **Step 1: Test gate route (RED).** Trong `ErpKeToanKhoGateTest`, cho 1 route đại diện mỗi mã #1–#6:
```php
public function test_the_kho_chi_mo_voi_ma_the_kho() {
    $this->seedAndLogin('ERPKTK1', ['accounting.ke_toan_kho_the_kho.view']);
    $this->assertRouteAllowed('GET', '<route #1>');           // có mã → 200/không 403
    $this->assertRouteForbidden('GET', '<route #2 bc_ban_hang>'); // mã khác → 403
}
public function test_route_anh_em_khong_gate_van_mo() {
    // route 1584-1587/1589/1591-1598: người KHÔNG có mã báo cáo vẫn vào được (không bị gán gate nhầm)
    $this->seedAndLogin('ERPKTK1b', []); // không mã ke_toan_kho
    $this->assertRouteAllowed('GET', '<route anh em không gate>');
}
```
- [x] **Step 2: Chạy — FAIL** (route đang gate bằng mã cũ / chưa gate). Run: `vendor/bin/phpunit --filter ErpKeToanKhoGateTest`. Expected: FAIL.
- [x] **Step 3: Đổi gate Nhóm I** — `routes/web.php` từng dòng 1574-1599 + 1687 đổi `checkPermission:accounting.ke_toan_kho.manage` → mã mới đúng route (bản đồ §5 Nhóm I). **Không** gán cả group `warehouse_reports`; route anh em không gate để nguyên.
- [x] **Step 4: Chạy — PASS.** Expected: PASS (cả `test_route_anh_em…`).
- [x] **Step 5: Commit** `feat(rbac): re-point Nhóm I báo cáo kế toán kho sang mã mới`.

---

### Task 3: Nhóm II — Nhập kho (#7–#11)

**Files:** Modify §5 Nhóm II: `app/Model/Warehouse/ProductImportRequest.php`, `ProductImport.php`, `WarehouseImport.php`, `OrderImportRequest.php`, `CustomDeclaration.php`; controller `WarehouseImportRequestsController.php:235`; routes `web.php:1403,1459`.

**Interfaces:**
- Consumes: Task 2 interfaces.
- Produces: #7 `yc_nhap_hang`, #8 `phieu_nhap_mua`, #9 `phieu_nhap_kho`, #10 `yc_nhap_theo_don` (**OR** giữ `accounting.ke_toan_mua_hang.*`), #11 `to_khai_hai_quan` (**OR** giữ `ke_toan_mua_hang`).

- [x] **Step 1: Test gate (RED)** — đại diện: `test_phieu_nhap_mua_mo_dung_ma` (mã #8 mở, mã #9 không); `test_yc_nhap_theo_don_OR_ke_toan_mua_hang` (người chỉ có `ke_toan_mua_hang` **vẫn** qua #10 — giữ nhánh OR). Run → FAIL.
- [x] **Step 2: Đổi gate** — mỗi file đổi toán hạng `ke_toan_kho` → mã mới đúng phiếu; #10/#11 **giữ** nhánh `|| ...ke_toan_mua_hang`.
- [x] **Step 3: Chạy — PASS.** `vendor/bin/phpunit --filter ErpKeToanKhoGateTest`.
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm II nhập kho`.

---

### Task 4: Nhóm III — Xuất kho/xuất hàng (#12–#16)

**Files:** §5 Nhóm III: `ProductExportRequest.php`, `ProductExport.php`, `WarehouseExport.php`, `SplitExportRequest.php`, `JoinExportRequest.php`; `WarehouseExportRequestsController.php:311`.

**Interfaces:** Produces #12 `de_nghi_xuat_kho`, #13 `phieu_xuat`, #14 `phieu_xuat_kho`, #15 `yc_tach_xuat`, #16 `yc_gop_xuat`.

- [x] **Step 1: Test (RED)** — `test_phieu_xuat_vs_de_nghi_xuat_tach_bach` (mã #13 không mở #12 và ngược lại). Run → FAIL.
- [x] **Step 2: Đổi gate** theo §5.
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm III xuất kho/xuất hàng`.

---

### Task 5: Nhóm IV — Điều chuyển & phân bổ (#17–#21)

**Files:** §5 Nhóm IV: `ProductTransferRequest.php`, `ProductImportDirectTransfer.php`, `ProductAllocation.php`, `InlandProductAllocation.php`, `TransferProductAllocation.php`; controller `ProductTransfersController.php:117`, notify `ProductTransferRequestsController.php:223,326`, `…DirectTransferController.php:162,233`.

**Interfaces:** Produces #17 `yc_chuyen_hang`, #18 `dieu_chuyen_nhap_thang`, #19 `phan_bo_hang`, #20 `phan_bo_noi_dia`, #21 `phan_bo_dieu_chuyen`.

- [x] **Step 1: Test (RED)** — `test_phan_bo_ba_loai_tach_bach` (#19/#20/#21 mở riêng). Run → FAIL.
- [x] **Step 2: Đổi gate** (gồm cả nhánh notify controller trong nhóm). Chú ý **không** đụng `is_warehouse_accountant` nếu đứng cạnh (vd `ProductExportRequest`).
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm IV điều chuyển & phân bổ`.

---

### Task 6: Nhóm V — Kiểm kê (#22–#25) ⚠️ gồm chỗ theo-TÊN (#24 HRM, ERP theo code)

**Files:** §5 Nhóm V: `InventoryAuditReport.php`, `WarehouseInventoryImport.php`, `WarehouseInventoryExport.php`, `SelfInventoriesController.php:417`; `InventoryAuditReportsController.php:37`; notify `…ImportsController.php:190,260`, `…ExportsController.php:199,275`.

**Interfaces:** Produces #22 `bien_ban_kiem_ke`, #23 `nhap_dieu_chinh_kiem_ke`, #24 `xuat_dieu_chinh_kiem_ke`, #25 `tu_kiem_ke`.

- [x] **Step 1: Test (RED)** — `test_nhap_vs_xuat_dieu_chinh_kiem_ke_tach_bach` (#23 không mở #24). Run → FAIL.
- [x] **Step 2: Đổi gate.** Ở ERP `WarehouseInventoryExport` kiểm theo **code** → đổi như thường (chỗ theo-TÊN `'Kế toán kho'` thuộc **HRM** — Plan 3). Vẫn grep lại chuỗi tên trong 4 file nhóm này để chắc ERP không có hằng theo tên.
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm V kiểm kê`.

---

### Task 7: Nhóm VI — Hàng mượn (#26–#30)

**Files:** §5 Nhóm VI: `BorrowSellRequest.php`, `BorrowSell.php`, `BorrowExportRequest.php`, `BorrowExport.php`, `BorrowExtendRequest.php`; route group `web.php:1161,1189,1992`; notify `BorrowSellRequestsController.php:438`, `BorrowExportRequestController.php:291`; dashboard `HomeController.php:1006,1020` (gia hạn hàng mượn — **OR** với `hang_muon_*`).

**Interfaces:** Produces #26 `yc_ban_hang_muon`, #27 `ban_hang_muon`, #28 `yc_xuat_hang_muon`, #29 `xuat_hang_muon`, #30 `yc_gia_han_hang_muon`.

- [x] **Step 1: Test (RED)** — `test_gia_han_hang_muon_OR_truong_phong` (dashboard 1006: người có `finance.hang_muon_truong_phong.approve` **vẫn** thấy nhánh — giữ OR; người có #30 cũng thấy). Run → FAIL.
- [x] **Step 2: Đổi gate** — route group đổi middleware; dashboard 1006/1020 thay **chỉ** toán hạng `ke_toan_kho` bằng #30, giữ `|| hang_muon_*`.
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm VI hàng mượn`.

---

### Task 8: Nhóm VII — Thanh toán giao hàng (#31–#33)

**Files:** §5 Nhóm VII: `DeliveryPaymentRequest.php`, `EmployeeDeliveryPayment.php`, `OtherDeliveryPaymentRequest.php`.

**Interfaces:** Produces #31 `yc_thanh_toan_giao_hang`, #32 `thanh_toan_giao_hang_nv`, #33 `yc_thanh_toan_giao_hang_khac`.

- [x] **Step 1: Test (RED)** — `test_ba_loai_thanh_toan_giao_hang_tach_bach`. Run → FAIL.
- [x] **Step 2: Đổi gate.**
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm VII thanh toán giao hàng`.

---

### Task 9: Nhóm VIII — Hạch toán dịch vụ (#34–#35)

**Files:** §5 Nhóm VIII: `WrAssignTask.php`, `WrAccountingServiceRequest.php`; notify `WrApproveResultsController.php:396,1162`, `WrAccountingServiceRequestsController.php:155,203`; dashboard `HomeController.php:1380`.

**Interfaces:** Produces #34 `ket_qua_giao_viec`, #35 `yc_lam_dich_vu_ke_toan`.

- [x] **Step 1: Test (RED)** — `test_ket_qua_giao_viec_vs_yc_dich_vu_tach_bach`; dashboard 1380 đếm đổi mã. Run → FAIL.
- [x] **Step 2: Đổi gate + nhánh dashboard 1380.**
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm VIII hạch toán dịch vụ`.

---

### Task 10: Nhóm IX — YC hạch toán bổ sung (#36) + dashboard 2201

**Files:** §5 Nhóm IX: notify `AdditionAccountingRequestController.php:244,332`; dashboard `HomeController.php:2201`.

**Interfaces:** Produces #36 `yc_hach_toan_bo_sung`.

- [x] **Step 1: Test (RED)** — `test_hach_toan_bo_sung_dung_ma`. Run → FAIL.
- [x] **Step 2: Đổi gate + dashboard 2201.**
- [x] **Step 3: PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point Nhóm IX hạch toán bổ sung`.

---

### Task 11: Mặt cắt ngang §6 — menu, notify-resolver, dashboard gộp, Warehouse filter

**Files:** Modify `resources/views/layouts/topmenubar.blade.php` (14), `topmenubar_old.blade.php` (11); `HomeController.php:1030` (và mọi nhánh đếm gộp còn lại); mọi `Warehouse::getForFilterByCurrentUser('accounting.ke_toan_kho.manage')` (blade forAccounting); resolver `Employee::withPermission` / `sendNotifyWithPermission` chưa thuộc Task 2–10.

**Interfaces:** Consumes mọi mã #1–#36. Produces: menu `@if` = **OR mã thành viên** của các màn mục đó mở; notify-resolver trỏ mã đúng phiếu; filter kho theo mã màn; dashboard gộp = OR.

- [x] **Step 1: Test (RED).**
```php
public function test_menu_or_chain_giu_operand_ngoai() {
    // mục menu mở N màn: người có BẤT KỲ 1 mã thành viên → thấy mục; operand thu_kho/is_warehouse_accountant giữ nguyên
}
public function test_notify_resolver_dung_ma_tung_phieu() {
    // người chỉ có mã phiếu X nằm trong tập nhận-thông-báo phiếu X, KHÔNG nằm trong tập phiếu Y
    // (resolve qua Employee::withPermission / sendNotifyWithPermission đã đổi)
}
public function test_warehouse_filter_theo_ma_man() {
    // getForFilterByCurrentUser(<mã mới>) trả kho đúng theo người có mã màn đó
}
```
Run → FAIL.
- [x] **Step 2: Đổi menu blade** — mỗi `@if(… ->can('…ke_toan_kho.manage'))` → OR mã thành viên của mục; **giữ** operand ngoài (`is_warehouse_accountant`, `thu_kho`, `xuat_hang_vuot_han_muc`). **Đổi** mọi resolver notify/filter/dashboard-gộp còn lại sang mã đúng.
- [x] **Step 3: Chạy — PASS.**
- [x] **Step 4: Commit** `feat(rbac): re-point mặt cắt ngang menu/notify/dashboard/filter`.

---

### Task 12: Chốt quét tĩnh xanh + full suite

**Files:** không sửa sản phẩm (trừ chỗ sót test quét tĩnh lộ ra).

- [x] **Step 1: Chạy test quét tĩnh.** `vendor/bin/phpunit --filter ErpKeToanKhoRepointTest`. Expected: cả 3 PASS (`test_khong_con_cong_kiem_ma_cu`, `test_khong_con_cong_kiem_theo_ten` xanh; Redis vẫn xanh). Còn sót → quay lại nhóm tương ứng đổi nốt (đây là lưới an toàn).
- [ ] **Step 2: Full Rbac suite một tiến trình.** `vendor/bin/phpunit tests/Feature/Rbac` (nếu tràn bộ nhớ như Plan 1 → chạy theo từng class gồm `ErpKeToanKhoGateTest`, `ErpKeToanKhoRepointTest`, `AccountingScopeConversionTest`, `ErpGateTest`, `SuperAdminNoBypassTest`). Expected: xanh.
- [x] **Step 3: Grep tay xác nhận (verify §11).** `grep -rn "accounting.ke_toan_kho.manage" app resources routes` và `grep -rn "'Kế toán kho'" app resources routes` → chỉ còn ngữ cảnh hợp lệ (Redis channel, nhãn hiển thị). Ghi kết quả vào checkpoint.
- [x] **Step 4: Commit** (nếu Step 1 lộ chỗ sót) `fix(rbac): dọn nốt tham chiếu ke_toan_kho sót` — nếu không sót thì bỏ qua commit.

---

## Self-Review

**1. Spec coverage:** §5 Nhóm I→IX ↔ Task 2→10 (map 1-1 theo cột "Gate ERP"). §6 mặt cắt ngang ↔ Task 11 + các nhánh notify/dashboard đã gắn vào nhóm chủ (VI/VIII/IX). §7.1 theo-tên ↔ Task 1 (grep chuỗi) + Task 12 (scan). §7.2 group một phần ↔ Task 2 `test_route_anh_em…`. §7.5 fail-closed ↔ Global Constraints (không deprecate ở Plan 2). §11 verify ↔ Task 12. Redis/is_warehouse_accountant giữ nguyên ↔ Global Constraints + Task 12 Redis-exception test. **Gap kiểm:** con số §5 là file:line *đại diện* — Task 1 là điều kiện-ra dựng danh sách ĐẦY ĐỦ (design §10 yêu cầu), nên chỗ §5 chưa liệt được Task 1 bắt + Task 12 lưới chặn.

**2. Step scan:** mỗi task re-point: test RED (tên + assertion cụ thể) → đổi gate theo §5 (builder viết chữ, §5 quyết mã) → PASS → commit. Không bước trống. Thân đổi gate để builder (idiomatic Laravel 6), mã đích do §5 chốt.

**3. Type consistency:** `AccountingCatalog::seed()` (Task 1) ↔ mọi task dùng. Helper test `seedAndLogin`/`assertRouteAllowed`/`assertRouteForbidden` khai trong `ErpKeToanKhoGateTest` (Task 2) ↔ Task 3–11 dùng lại. `ErpGateFixture` API (`makeEmployee/makeRole/grant/assignRole/loginErp`, `$C1/$C2`) khớp chữ ký đã đọc. Mã mới dùng đúng tên Plan 1 `KeToanKhoSplitMap::newCodes()`.

**4. Review Focus:** 5 mục (OR-chain rớt đồng-chủ-thể, theo-tên, group một phần, notify lệch mã, Redis channel) đều có test sở hữu (Task 2/11/12). Mục trống = 0.

**5. Proportion:** plan **không** liệt lại 139 file:line (đã ở design §5) — dẫn chiếu §5 làm thẩm quyền map, mỗi task chỉ nêu nhóm file + mã đích + test. Task 1 sinh danh sách đầy đủ lúc chạy. Độ dài plan ≈ cân xứng spec.

---

## Execution Handoff

(điền khi bàn giao: chọn Subagent-driven hay Native)

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Plan 2 Task 1–12 xong: 12 commit re-point ERP `d21f108380`..`5a9345f0b3` ✓push origin/develop_02. ErpKeToanKhoGateTest 11 tests/325 assertions, ErpKeToanKhoRepointTest 3/3; final review Opus sạch.
Đang làm dở: Task 12 Step 2 (full `tests/Feature/Rbac`) KHÔNG chạy: DB `hrm_erp_rbac_test` không tồn tại ở máy này (user: chưa bao giờ chạy) → verify DB-free.
Bước tiếp theo: Rollout cùng HRM (catalog-sync → grant → verify → deprecate). Minor hoãn: back-fill AccountingInventoriesController:200→#22 vào design §5; `assertSourceGatedBy` kiểm substring. Chưa gop_db.
Blocked: Không
