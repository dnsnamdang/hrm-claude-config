# Tách quyền "Kế toán kho" — Plan 3: HRM re-point Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Native — đã chốt) để thực thi từng task. Các step dùng checkbox (`- [x]`).
> **LƯU Ý:** `plan.md` trong thư mục này là **Plan 1** (nền quyền hrm-api, đã xong). Đây là **Plan 3** — tài liệu riêng.

**Goal:** Trỏ toàn bộ gate/Definition/route/service/FE của HRM (hrm-api + hrm-client) từ mã chung `accounting.ke_toan_kho.manage` **và** tên tiếng Việt `'Kế toán kho'` sang đúng 1 trong 36 mã per-screen (gộp → OR theo §6), để sau khi deprecate mã cũ không còn gate nào chết.

**Architecture:** Thuần **đổi chuỗi token** tại các chỗ kiểm quyền (code-form và name-form), bám bản đồ §5/§6 của design (APPROVED). Không đổi cơ chế `can()`/`isCurrentEmployeeHasPermission()`/`PermissionChecker` — 36 mã đã LIVE prod (Plan 1). Verify bằng **static-scan DB-free** (mirror Plan 2 ERP) + Playwright cho hành vi (§11). Mã cũ **giữ nguyên, chưa deprecate** trong plan này (deprecate là bước cuối §8.6, sau khi cả ERP+HRM xong + grep 0 ref).

**Tech Stack:** PHP 7.4 / Laravel 8 / nwidart Modules / Spatie permission (hrm-api); Nuxt 2 (Vue 2) (hrm-client). phpunit **không chạy song song** trên DB chung → mọi test là **static-scan DB-free** (đọc file nguồn), chạy đơn tiến trình `vendor/bin/phpunit --filter <Class>`.

**Spec:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/tach-quyen-ke-toan-kho/design.md` (APPROVED) — §5 bản đồ 36 mã (cột "Gate HRM"), §6 quy tắc xuyên suốt (OR gộp / menu giữ operand / Redis coarse), §7.1 rủi ro theo-tên, §8 trình tự, §11 verify.
**Inventory tham chiếu:** `…/scratchpad/hrm-ktk-gate-inventory.md` (61 live sites, dựng session này) — Task 1 dựng lại bằng grep tươi trong worktree rồi đối chiếu.
**Tiền lệ:** Ledger Plan 2 ERP `…/scratchpad/ktk-erp-ledger.md` (chiến lược test static-scan đã được review Opus chấp nhận).

## Global Constraints

- **Chỉ đổi token kiểm quyền.** Không sửa cơ chế `can()`/checker, không tái cấu trúc, không "nhân tiện" dọn thêm.
- **Giữ operand không-phải-ke_toan_kho** trong mọi chuỗi OR (menu, gate gộp): `thu_kho`, `xuat_hang_vuot_han_muc`, `is_warehouse_accountant`, `ke_toan_mua_hang`, `finance.hang_muon_*`… GIỮ NGUYÊN (§6).
- **Gate gộp** (1 gate phục vụ nhiều màn: dashboard counter, menu OR-chain, list đa-loại, trait/route dùng chung Tách+Gộp) → **OR của TẤT CẢ mã thành viên**, không chọn 1 mã (§6).
- **Redis channel `ke_toan_kho<warehouse_id>`** GIỮ NGUYÊN (coarse, 1/kho) — không tách (§6).
- **Name-form (§7.1):** mọi chỗ dùng chuỗi `'Kế toán kho'` làm **đối số quyền** (inline `isCurrentEmployeeHasPermission('Kế toán kho')`, hằng `PERMISSION_* = 'Kế toán kho'` phục vụ gate, menu FE `isShow:['Kế toán kho']`) phải đổi sang **mã mới**. KHÔNG đụng `'Kế toán kho'` dùng làm **nhãn hiển thị** (tên cột, text thông báo, tiêu đề) — những chỗ đó giữ nguyên.
- **Const-consumer tự giải:** đổi giá trị 1 hằng `const PERMISSION_* = '<code>'` tự cập nhật mọi consumer `self::CONST`/`Model::CONST` → consumer KHÔNG phải điểm sửa riêng, nhưng mọi consumer của hằng đó phải cùng giải về 1 màn (đã verify trong inventory).
- **Không push / gộp_db / deploy** khi chưa có yêu cầu. Commit TDD **local** per-task là một phần Native execution đã duyệt.
- **Tài liệu** chỉ ở `HRM/.plans/…` (symlink). Test code vào `hrm-api/tests/…` là CODE (được phép). Không tạo tài liệu trong repo code.
- Attribution commit: kết `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

## Review Focus

Những lớp dễ "cắn" mà test static-scan per-task không tự phủ hết — reviewer cuối soi từng cái:

1. **Name-form bỏ sót** (§7.1): một chỗ `'Kế toán kho'` gate còn sót → sau deprecate thành **gate chết, fail-closed chặn người dùng**. Rủi ro cao nhất, HRM-specific. → Task 1 `test_no_old_name_in_gate_context` phủ 7 site đã biết; reviewer tìm site name-form MỚI ngoài inventory.
2. **Gate gộp Tách/Gộp dùng chung static/trait** (#15/#16): nếu chỉ gán 1 mã thay vì OR → người chỉ có quyền màn kia bị chặn, hoặc bị nới quá. → Task "Tách/Gộp" test khẳng định OR cả 2 mã ở trait/route dùng chung.
3. **FE/BE lệch mã cùng 1 hành động** (#12): nút FE `product-export-requests` (754,763 / Form 2850,2860) và guard BE `ProductExportController` (1049,1155,1713,1732) phải CÙNG `de_nghi_xuat_kho` (§5 #12). Lệch → nút hiện mà API 403, hoặc ngược lại. → Task "Xuất hàng" test cả FE lẫn BE cùng mã.
4. **Const đổi giá trị nhưng còn consumer giải sang màn khác**: nếu 1 hằng có consumer thuộc 2 màn → đổi hằng làm lệch 1 màn. → mỗi Task khẳng định hằng + điểm danh consumer trong brief.
5. **Redis channel vô tình bị đổi**: replace_all chuỗi rộng có thể đụng `ke_toan_kho<id>`. → Task 1 `test_redis_channel_preserved`.

---

## File Structure

**hrm-api (test harness — tạo mới):**
- `tests/Unit/Permission/HrmKeToanKhoScan.php` — helper static-scan DB-free (đọc file nguồn hrm-api **và** hrm-client qua đường dẫn tương đối). Produces: `root($repo)`, `gateLines($file)`, `assertSourceHasCode($file,$codes)`, `assertSourceCleanOfOld($file)` (sạch cả code-form `'accounting.ke_toan_kho.manage'` lẫn name-form gate `'Kế toán kho'`), `assertKeepsOperand($file,$operand)`, `assertConstValue($file,$const,$code)`.
- `tests/Unit/Permission/HrmKeToanKhoRepointTest.php` — completeness scan: `test_no_old_code_in_gate_context` (RED→GREEN ở Task cuối), `test_no_old_name_in_gate_context` (7 site name-form), `test_redis_channel_preserved`.
- `tests/Unit/Permission/HrmKeToanKhoGateTest.php` — per-nhóm test (mỗi Task thêm 1 method).

**hrm-api (re-point — sửa):** Definitions/Controllers/Services/Models theo inventory Section A–E + routes `Modules/Assign/Routes/api.php`, `Modules/Finance/Routes/api.php`.
**hrm-client (re-point — sửa):** `pages/finance/product-export-requests/index.vue`, `pages/finance/product-exports/index.vue`, components form, `…/finance.js` (menu).

Mã mới dạng chuỗi: `accounting.ke_toan_kho_<slug>.manage` (prefix `accounting.ke_toan_kho_`, suffix `.manage`). Dùng helper nhỏ `code('<slug>')` trong script re-point (bám `ktk-task11-repoint.py` của ERP) hoặc Edit từng chỗ.

---

### Task 1: Dựng danh sách ĐẦY ĐỦ + harness static-scan (RED milestone)

**Files:**
- Create: `hrm-api/tests/Unit/Permission/HrmKeToanKhoScan.php`
- Create: `hrm-api/tests/Unit/Permission/HrmKeToanKhoRepointTest.php`
- Scan-only (không sửa): toàn repo hrm-api + hrm-client

**Interfaces:**
- Produces: lớp `HrmKeToanKhoScan` với các assert helper (Task 2–N CONSUME); file `hrm-ktk-site-map.md` trong scratchpad (bản đồ site→mã đầy đủ, đối chiếu inventory).
- Consumes: design §5/§6, inventory 61 site.

- [x] **Step 1: Grep tươi completeness** — trong worktree chạy (ghi ra scratchpad, KHÔNG để trong repo):
  - `grep -rn "accounting.ke_toan_kho.manage" hrm-api/app hrm-api/Modules hrm-api/routes` và `… hrm-client/pages hrm-client/components hrm-client/store hrm-client/utils hrm-client/static`
  - `grep -rn "'Kế toán kho'" hrm-api/app hrm-api/Modules` (name-form) và `grep -rn "Kế toán kho" hrm-client/…` (lọc gate vs nhãn)
  - Map từng chỗ về đúng 1/36 theo §5 (cột Gate HRM) + §6; đối chiếu với inventory 61 site; chênh lệch nào → Ruling vào ledger. Kết quả → `scratchpad/hrm-ktk-site-map.md`.

- [x] **Step 2: Viết `HrmKeToanKhoScan`** — plain static-scan, DB-free (không `RefreshDatabase`, không query). `root()` trả repo-root; đọc được cả hrm-api PHP lẫn hrm-client .vue/.js qua `dirname`. `gateLines($file)` = các dòng chứa `isCurrentEmployeeHasPermission(`/`hasAPermission(`/`checkPermission:`/`->can(`/`PERMISSION_`/`codes:`/`isShow:`. Hằng gate = dòng `const PERMISSION_… =` hoặc `public static $PERMISSION_… =`.

- [x] **Step 3: Viết `HrmKeToanKhoRepointTest`** (3 test):
```php
public function test_no_old_code_in_gate_context()  // RED bây giờ; GREEN ở Task cuối
// → assertSourceCleanOfOld cho MỌI file trong site-map (code-form), trừ Catalog accounting.php + docblock comment '//'/'*' được whitelist.
public function test_no_old_name_in_gate_context()
// → 7 site name-form phải SẠCH 'Kế toán kho' ở vị trí gate:
//   WarehouseInventoryExport.php:48 (const PERMISSION_ACCOUNTANT), WrImportResultNotifier.php:37 (const PERM_ACCOUNTING),
//   ProductExportRequest.php:433, WarehouseExportController.php:260, :305, WarehouseExportResource.php:23,
//   finance.js:712 (isShow:['Kế toán kho']). (RED bây giờ; GREEN khi các Task tương ứng xong.)
public function test_redis_channel_preserved()
// → chuỗi "ke_toan_kho" ghép warehouse_id ở các publisher GIỮ NGUYÊN (assert còn tồn tại).
```

- [x] **Step 4: Chạy — xác nhận RED đúng chỗ**
Run: `cd hrm-api && vendor/bin/phpunit --filter HrmKeToanKhoRepointTest`
Expected: `test_no_old_code_in_gate_context` **FAIL** (còn nhiều ref cũ — đây là mốc deliverable), `test_no_old_name_in_gate_context` **FAIL** (7 site còn name-form), `test_redis_channel_preserved` **PASS**.

- [x] **Step 5: Commit** `test(ktk-hrm): static-scan harness + completeness RED milestone`

---

### Task 2: Nhóm NHẬP (hrm-api) — #7 #8 #9 #18

**Files (Modify):** `Modules/Assign/.../ProductImportRequest*.php` (#7 `yc_nhap_hang` — const Def + inline), `ProductImport.php` + `ProductImportService.php:1667,2207` (#8 `phieu_nhap_mua`), `WarehouseImport.php:92` + `WarehouseImportRequest.php:35` + Definition (#9 `phieu_nhap_kho`), `ProductImportDirectTransfer.php:47` (#18 `dieu_chuyen_nhap_thang`).
**Test:** `HrmKeToanKhoGateTest::test_nhom_nhap_dung_ma`
**Interfaces:** Consumes `HrmKeToanKhoScan`. Produces: nhóm nhập sạch mã cũ.

- [x] **Step 1** Viết `test_nhom_nhap_dung_ma`: với mỗi file trên → `assertSourceHasCode(file, [<mã §5>])` + `assertSourceCleanOfOld(file)`; giữ OR `ke_toan_mua_hang` nếu §5 ghi (kiểm `assertKeepsOperand`). Const: `assertConstValue(Def, 'PERMISSION_…', code)`.
- [x] **Step 2** Run `--filter test_nhom_nhap_dung_ma` → Expected FAIL (file còn mã cũ).
- [x] **Step 3** Re-point: đổi giá trị hằng Definition (#7/#8/#9/#18) + inline code sites sang mã mới. Const-consumer tự theo.
- [x] **Step 4** Run → Expected PASS; chạy full `--filter HrmKeToanKhoGateTest` vẫn xanh.
- [x] **Step 5** Commit `refactor(ktk-hrm): nhóm nhập → #7/#8/#9/#18`.

---

### Task 3: Nhóm XUẤT HÀNG (hrm-api + hrm-client) — #12 #13 #14

Trọng tâm Review Focus #3 (FE/BE cùng mã) + resolve conflict inventory↔§5.
**Ruling (spec):** `ProductExportController.php:1049,1155,1713,1732` + FE `product-export-requests/index.vue:754,763` + `ProductExportRequestForm.vue:2850,2860` → **`de_nghi_xuat_kho` (#12)** theo §5 (gate theo màn thao-tác-từ = YCXH), **ĐÈ** đề xuất file-ownership (#13) của inventory. `ProductExport.php:1214` + `product-exports/index.vue:471` → **`phieu_xuat` (#13)**. Cả họ WarehouseExport/WarehouseExportRequest (ĐNXK) + routes `Assign/api.php:839-847,886-889` + `WarehouseExportRequestResource.php:36` → **`phieu_xuat_kho` (#14)**.

**Files (Modify):**
- #12: `ProductExportRequestDefinition.php:41` (const), `ProductExportController.php:1049,1155,1713,1732`, `ProductExportRequest.php:404` (code-form) **và `:433` (name-form)**; FE `product-export-requests/index.vue:754,763`, `ProductExportRequestForm.vue:2850,2860`.
- #13: `ProductExport.php:1214`; FE `product-exports/index.vue:471`.
- #14: `WarehouseExportDefinition.php:34`, `WarehouseExportRequestDefinition.php:34`, `WarehouseExportRequestController.php:594,751,766,910`, `WarehouseExportRequestResource.php:36`, routes `Assign/api.php:839,840,844,846,847,886,887,888,889`; **name-form:** `WarehouseExportController.php:260` (deny — giữ status + sameCompany), `:305` (pick/edit — giữ isDraftOwner OR), `WarehouseExportResource.php:23` (`$isAccountant`).
**Test:** `test_nhom_xuat_hang_dung_ma`.

- [x] **Step 1** Test: mỗi file #12/#13/#14 → `assertSourceHasCode` + `assertSourceCleanOfOld` (phủ CẢ code-form lẫn name-form). Khẳng định FE 754/763/2850/2860 **cùng** `de_nghi_xuat_kho` với BE 1049/1155/1713/1732. Giữ operand `status`/`sameCompany`/`isDraftOwner` ở WarehouseExportController (name-form) — `assertKeepsOperand`.
- [x] **Step 2** Run → Expected FAIL.
- [x] **Step 3** Re-point hrm-api (const + inline code + 3 name-form site) + routes + hrm-client 3 file.
- [x] **Step 4** Run → PASS; full gate test xanh.
- [x] **Step 5** Commit `refactor(ktk-hrm): nhóm xuất hàng → #12/#13/#14 (FE+BE+name-form)`.

---

### Task 4: Nhóm TÁCH / GỘP (hrm-api) — #15 #16 (gate gộp OR)

Review Focus #2. **Ruling (spec §6):** chỗ Definition tách riêng từng class → 1 mã; chỗ trait/support/route **dùng chung phục vụ CẢ tách+gộp** → **OR(`yc_tach_xuat`, `yc_gop_xuat`)**.

**Files (Modify):**
- Riêng được: `SplitExportRequestDefinition.php` → #15; `JoinExportRequestDefinition.php` → #16.
- Dùng chung → OR cả 2: `SplitJoinExportRequestCommon.php:35` (static `$PERMISSION_ACCOUNTANT`), `SplitJoinExportApprovalSupport.php:58,107,135`, `SplitJoinExportRequestController.php:22,229`; routes `Finance/api.php:2321,2323,2324` (foreach cả 2).
- Join-only: routes `Finance/api.php:2327,2328,2329` → **#16 `yc_gop_xuat`** (thao-tác-từ màn gộp).

**Step phụ (verify cơ chế OR của HRM TRƯỚC khi test):** kiểm chữ ký `isCurrentEmployeeHasPermission()`/`hasAPermission()`/middleware `checkPermission:` — chấp nhận **mảng** hay **chuỗi nối `|`** để biểu diễn OR? Ghi Ruling. Nếu static chỉ nhận 1 chuỗi → OR được biểu diễn bằng: (a) override hằng per-class nơi tách được, (b) chỗ thật-sự-chung đổi consumer thành `A || B` hoặc `checkPermission:codeA|codeB`. (Route `checkPermission:` nối `|` = OR — đã có trong CLAUDE.md.)

- [x] **Step 1** Test `test_nhom_tach_gop_dung_ma`: Def tách→#15, Def gộp→#16; file/route dùng chung → có CẢ #15 và #16 (OR), sạch mã cũ; route 2327-2329 → chỉ #16.
- [x] **Step 2** Run → FAIL.
- [x] **Step 3** Re-point theo Ruling cơ chế OR ở trên.
- [x] **Step 4** Run → PASS; full xanh.
- [x] **Step 5** Commit `refactor(ktk-hrm): tách/gộp → OR(#15,#16); route gộp → #16`.

---

### Task 5: Nhóm CHUYỂN / PHÂN BỔ (hrm-api) — #17 #21

**Files (Modify):** `ProductTransferRequest.php:31` + `ProductTransfer.php:61` (**#17 `yc_chuyen_hang`** — §5 #17 liệt kê ProductTransfer:61), `TransferProductAllocation.php:46` (**#21 `phan_bo_dieu_chuyen`**). (Các mã #19/#20 nếu không có site HRM live thì bỏ — xác nhận ở Task 1 map.)
**Test:** `test_nhom_chuyen_phan_bo_dung_ma`.

- [x] **Step 1** Test từng const/site → mã §5 + sạch cũ.
- [x] **Step 2** Run → FAIL. **Step 3** Re-point. **Step 4** Run → PASS. **Step 5** Commit `refactor(ktk-hrm): chuyển/phân bổ → #17/#21`.

---

### Task 6: Nhóm KIỂM KÊ (hrm-api) — #22 #23 #24 #25 (gồm name-form #24)

Review Focus #1 (name-form).
**Files (Modify):** `InventoryAuditReport.php:58` (#22 `bien_ban_kiem_ke`), `WarehouseInventoryImport.php:59` (#23 `nhap_dieu_chinh_kiem_ke`), **`WarehouseInventoryExport.php:48`** (#24 `xuat_dieu_chinh_kiem_ke` — hằng `PERMISSION_ACCOUNTANT = 'Kế toán kho'` **name-form**; consumers :87/:113/:125/:147 + `InventoryExportService:118` + `WriteService:394` tự theo), `SelfInventory.php:72` (#25 `tu_kiem_ke`).
**Test:** `test_nhom_kiem_ke_dung_ma` — đặc biệt `assertConstValue(WarehouseInventoryExport, 'PERMISSION_ACCOUNTANT', code('xuat_dieu_chinh_kiem_ke'))` (từ name → code).

- [x] **Step 1** Test. **Step 2** Run → FAIL. **Step 3** Re-point (đổi hằng name→code cho #24). **Step 4** Run → PASS. **Step 5** Commit `refactor(ktk-hrm): kiểm kê → #22/#23/#24(name→code)/#25`.

---

### Task 7: Nhóm HÀNG MƯỢN (hrm-api + hrm-client) — #26 #27 #28 #29 #30

**Files (Modify):** `BorrowSellRequest.php:63` (#26), `BorrowSell.php:35` (#27), `BorrowExportRequest.php:62` (#28), `BorrowExport.php:57` (#29), `BorrowExtendRequest.php:70` (#30 `yc_gia_han_hang_muon`, const `PERMISSION_KT_APPROVE`); FE **name-form** `finance.js:712` `isShow:['Kế toán kho']` + `:713` `codes:[...]` → #30 (giữ các operand menu không-KTK nếu có).
**Test:** `test_nhom_hang_muon_dung_ma` + khẳng định `finance.js` menu operand KTK đổi #30, operand khác giữ.

- [x] **Step 1** Test. **Step 2** Run → FAIL. **Step 3** Re-point (5 const + FE menu name-form). **Step 4** Run → PASS. **Step 5** Commit `refactor(ktk-hrm): hàng mượn → #26-#30 (+FE menu name-form)`.

---

### Task 8: Nhóm GIAO VIỆC / HẠCH TOÁN BỔ SUNG (hrm-api) — #34 #36 (gồm name-form #34)

**Files (Modify):** **`WrImportResultNotifier.php:37`** (#34 `ket_qua_giao_viec` — hằng `PERM_ACCOUNTING = 'Kế toán kho'` **name-form**; consumer :201 tự theo), `AdditionAccountingRequest.php:242` (#36 `yc_hach_toan_bo_sung`, const `PERMISSION_NOTIFY_TARGET`). (#35 không có site HRM live — xác nhận Task 1; nếu chỉ docblock thì bỏ.)
**Test:** `test_nhom_giao_viec_dung_ma` — `assertConstValue(WrImportResultNotifier, 'PERM_ACCOUNTING', code('ket_qua_giao_viec'))`.

- [x] **Step 1** Test. **Step 2** Run → FAIL. **Step 3** Re-point (name→code #34, const #36). **Step 4** Run → PASS. **Step 5** Commit `refactor(ktk-hrm): giao việc/hạch toán bổ sung → #34(name→code)/#36`.

---

### Task 9: Completeness xanh + verify §11 + review nhánh

**Files:** không sửa nguồn (trừ dọn docblock nếu cần để static-scan sạch).
**Interfaces:** Consumes mọi Task trước.

- [x] **Step 1** Chạy `vendor/bin/phpunit --filter HrmKeToanKhoRepointTest` → giờ **cả 3 PASS** (`test_no_old_code_in_gate_context` + `test_no_old_name_in_gate_context` chuyển GREEN). Nếu còn đỏ: còn site sót → tìm, map, re-point (có thể cần Ruling), không sửa test cho hợp.
- [x] **Step 2** Grep tổng (§11): `grep -rn "accounting.ke_toan_kho.manage"` và `grep -rn "'Kế toán kho'"` ở hrm-api + hrm-client → chỉ còn ở **Catalog `accounting.php`** (định nghĩa) + **nhãn hiển thị** (không phải gate). Ghi kết quả vào ledger.
- [x] **Step 3** Full suite liên quan: `vendor/bin/phpunit --filter HrmKeToanKhoGateTest` + `--filter HrmKeToanKhoRepointTest` xanh (đơn tiến trình, KHÔNG `-p`).
- [ ] **Step 4 (Playwright §11)** Với HRM đang chạy local (skill `run-hrm`): 1 tài khoản chỉ cấp **1 mã lẻ** (vd `phieu_xuat_kho`) → vào/thao tác đúng màn ĐNXK, các màn khác (nhập mua, kiểm kê…) bị chặn. Chụp bằng chứng vào scratchpad. (Nếu môi trường RBAC local chưa cấp được mã lẻ → Ruling DB-free như Plan 2, nêu rõ.)
- [x] **Step 5** Commit dọn (nếu có) `test(ktk-hrm): completeness GREEN + verify`.
- [x] **Step 6 — Final whole-branch review** (fresh reviewer, Opus): gói `review-package` MERGE_BASE..HEAD; Review Focus 1–5 verbatim; con trỏ tới ledger `Ruling:`. Re-grade theo hiệu ứng → Critical/Important vào 1 fix pass (mỗi fix RED→GREEN + suite xanh); Minor → ledger. Xong → `finishing-a-development-branch` (KHÔNG push/merge khi chưa xin phép).

---

## Self-Review

**1. Spec coverage (§5 cột Gate HRM):** #7/#8/#9/#18 (Task 2) · #12/#13/#14 (Task 3) · #15/#16 (Task 4) · #17/#21 (Task 5) · #22/#23/#24/#25 (Task 6) · #26-#30 (Task 7) · #34/#36 (Task 8). #1-6, #10/#11, #19/#20, #31-33, #35 = ERP-only hoặc docblock-only trong HRM → Task 1 xác nhận bằng grep; mã nào có site HRM live mà lọt → bắt ở Task 9 Step 1 (completeness GREEN là điều kiện ra). §6 (OR gộp/menu operand/Redis) phủ ở Task 3/4/7 + Task 1 Redis. §7.1 name-form (7 site) phủ ở Task 1 test + Task 3/6/7/8. §8.6 deprecate = NGOÀI plan (bước cuối sau cả 2 app).

**2. Step scan:** mỗi re-point step quyết 1 việc (đổi token tại file:line đã chỉ theo §5). Không có step "TBD"/"xử lý edge case". Cơ chế OR của HRM là ẩn số thật → Task 4 có Step phụ verify chữ ký trước khi chốt cách biểu diễn (không đoán).

**3. Type consistency:** helper `HrmKeToanKhoScan` định nghĩa 1 lần (Task 1), mọi Task gọi cùng tên (`assertSourceHasCode`/`assertSourceCleanOfOld`/`assertKeepsOperand`/`assertConstValue`). Mã: luôn `accounting.ke_toan_kho_<slug>.manage`.

**4. Review Focus:** 5 mục → test tương ứng: #1 name-form (Task1 `test_no_old_name…` + Task3/6/7/8), #2 OR tách/gộp (Task4), #3 FE/BE cùng mã (Task3), #4 const-consumer (brief mỗi Task điểm danh consumer), #5 Redis (Task1 `test_redis_channel_preserved`).

**5. Proportion:** plan ngắn hơn tổng nguồn sửa; không transcribe 61 site — trỏ §5/inventory, chỉ ghi file:line quyết định + mã + test. Đạt.

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Task 1–9 (trừ Step 4 Playwright) xong: re-point toàn bộ gate HRM sang 36 mã; §11 dual grep phân loại hết — 0 gate sống dùng mã/tên cũ; tests/Unit/Permission 30/30; final review PASS (0 Critical/0 Important). ✓push hrm-api develop `63aabe212..fda2058c3` (rebase trên 4 commit người khác, không conflict), hrm-client develop `..b19141357` (+ `d975d816f`).
Đang làm dở: Task 9 Step 4 (Playwright 1 tài khoản 1 mã lẻ) chưa chạy — verify DB-free.
Bước tiếp theo: Kiểm Playwright trên dev; prod: catalog-sync → grant dry-run → chạy thật → verify; deprecate mã cũ sau cùng.
Blocked: Không
