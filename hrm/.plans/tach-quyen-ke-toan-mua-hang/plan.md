# Tách quyền `accounting.ke_toan_mua_hang.manage` → 3 mã theo màn — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development. Steps dùng checkbox `- [x]`.

**Goal:** Tách quyền-cờ dùng chung `accounting.ke_toan_mua_hang.manage` (ERP) thành 3 mã theo từng màn, không ai mất quyền, mã cũ giữ tới bước deprecate cuối.

**Architecture:** Thêm 3 mã vào Catalog (nguồn sự thật, sync bằng `permission:catalog-sync`); re-point 14 gate ERP; thêm 3 mã vào fixture RBAC ERP; lệnh grant copy pivot 1→3; test DB-free soi source. Bám nguyên khuôn task chị em `tach-quyen-ke-toan` (`KeToanSplit*`, `KeToanSplitMap`, `RbacGrantKeToanSplitCommand`).

**Tech Stack:** PHP 7.4, Laravel 8 (hrm-api) + Laravel 6 (ERP TanPhatDev), PHPUnit (test DB-free `PHPUnit\Framework\TestCase`).

**Spec:** `HRM/.plans/tach-quyen-ke-toan-mua-hang/design.md`

## Global Constraints

- **Không commit/push.** Không chạy lệnh ghi DB (ERP `.env` local trỏ prod DB). `catalog-sync`/grant/deprecate do user tự chạy.
- 3 mã mới: `platforms=['erp']`, `kind='action'`, `scopes=[]`, `depends_on=[]`, `legacy=[]`, `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `feature='Kế toán'`.
- Ở `canView` nhóm B & C chỉ thay **toán hạng** mua_hang, **GIỮ** toán hạng `ke_toan_kho_*` + mọi scope khác.
- **KHÔNG đụng** `CustomDeclaration.php:575` (`purchase.to_khai_hai_quan.approve`) và `app/Model/Common/Dashboard.php:9` (nhãn `KE_TOAN_MUA_HANG`).
- **KHÔNG đụng HRM** (file Phiếu tính giá HRM đang do session khác sửa).
- Mã cũ `accounting.ke_toan_mua_hang.manage` **giữ nguyên** trong Catalog tới sau rollout (deprecate ngoài phạm vi plan này).
- Test DB-free, tái dùng scanner `tests/Unit/Permission/KeToanSplitScan.php` (API per-file theo needle — truyền literal `'accounting.ke_toan_mua_hang.manage'`).
- Lệnh chạy test: từ `HRM/hrm-api`, `vendor/bin/phpunit --filter KeToanMuaHangSplit`. KHÔNG chạy 2 process phpunit song song (memory `hrm-phpunit-no-concurrent-shared-db`) — nhưng các test này không đụng DB nên an toàn.

## Review Focus

- **Re-point sót / thừa:** sau toàn bộ, `grep -rn "ke_toan_mua_hang" app resources routes tests` (ERP) chỉ còn `Dashboard.php:9` (nhãn) — mọi gate đã chuyển. (phủ bởi test mỗi nhóm `*_sach_ma_cu`.)
- **Over-grant ở canView B/C:** toán hạng `ke_toan_kho_*` còn nguyên sau khi thay. (phủ bởi test Task 4/5 assert kho-code vẫn còn.)
- **Đụng nhầm approve tờ khai:** `purchase.to_khai_hai_quan.approve` còn nguyên ở CustomDeclaration. (phủ bởi test Task 5.)
- **Fixture thiếu mã → suite RBAC ERP vỡ:** 3 mã có trong `AccountingCatalog::MAP`. (phủ bởi test Task 2.)
- **Thứ tự mã trong Map ≠ Catalog:** Map `newCodes()` khớp đúng thứ tự 3 entry Catalog. (phủ bởi test Task 1.)

---

### Task 1: Map class + 3 mã Catalog

**Files:**
- Create: `hrm-api/app/Support/Permissions/KeToanMuaHangSplitMap.php`
- Modify: `hrm-api/app/Support/Permissions/Catalog/accounting.php` (chèn sau block `ke_toan_mua_hang.manage`, sau dòng ~541)
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitMapTest.php`

**Interfaces:**
- Produces: `KeToanMuaHangSplitMap::OLD_CODE`, `::oldCode()`, `::newCodes()` (3 mã, đúng thứ tự Catalog), `::all()` (= [old, ...new]). Dùng ở Task 6.

- [x] **Step 1: Viết test** `KeToanMuaHangSplitMapTest` (mirror `KeToanSplitMapTest`):

```php
private const OLD = 'accounting.ke_toan_mua_hang.manage';
private const NEW = [
    'accounting.ke_toan_phieu_tinh_gia.manage',
    'accounting.ke_toan_duyet_yc_nhap_theo_don.manage',
    'accounting.ke_toan_xem_to_khai_hai_quan.manage',
];
// test_old_code_dung: KeToanMuaHangSplitMap::OLD_CODE === OLD
// test_ba_ma_moi_dung_thu_tu: ::newCodes() === NEW
// test_all_4_phan_tu: count(::all())==4 && ::all()[0]===OLD
// test_catalog_khai_du_3_ma_va_giu_ma_cu: Catalog/accounting.php chứa "'code' => '<code>'" cho 3 mã mới + mã cũ
```

- [x] **Step 2: Chạy, xác nhận FAIL** (class chưa có): `vendor/bin/phpunit --filter KeToanMuaHangSplitMapTest`
- [x] **Step 3: Tạo `KeToanMuaHangSplitMap`** — clone `KeToanSplitMap`, đổi `OLD_CODE` và `newCodes()` sang 3 mã trên.
- [x] **Step 4: Thêm 3 entry Catalog** `accounting.php` (shape như §4 design; giữ platforms=['erp'], legacy=[]), chèn ngay sau block `ke_toan_mua_hang.manage`.
- [x] **Step 5: Chạy, xác nhận PASS.**
- [x] **Step 6: Commit.**

---

### Task 2: Fixture RBAC ERP

**Files:**
- Modify: `ERP/TanPhatDev/tests/Feature/Rbac/Concerns/AccountingCatalog.php` (`const MAP`)
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitRbacFixtureTest.php`

- [x] **Step 1: Viết test** (mirror `KeToanSplitRbacFixtureTest`): `KeToanSplitScan::erpSource('tests/Feature/Rbac/Concerns/AccountingCatalog.php')` chứa `"'<code>'"` cho cả 3 mã mới.
- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Thêm 3 dòng** vào `const MAP`: `'accounting.ke_toan_phieu_tinh_gia.manage' => [[], []],` (+ 2 mã còn lại), đặt gần cụm mã `ke_toan_*` sẵn có.
- [x] **Step 4: Chạy, xác nhận PASS.**
- [x] **Step 5: Commit.**

---

### Task 3: Re-point nhóm A — Phiếu tính giá → mã #1

**Files (ERP):**
- Modify: `app/Model/Order/PriceCalculateRequest.php:373,385,390,405`
- Modify: `app/Model/Order/PriceCalculate.php:300`
- Modify: `app/Model/Order/PriceCalculateResult.php:150`
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitPhieuTinhGiaTest.php`

- [x] **Step 1: Viết test** (mirror `KeToanSplitPhieuThuongKdTest`), `NEW_CODE='accounting.ke_toan_phieu_tinh_gia.manage'`, `OLD='accounting.ke_toan_mua_hang.manage'`:
  - `test_ba_file_dung_ma_moi`: 3 file ERP đều `assertStringContainsString(NEW_CODE, erpSource(...))`.
  - `test_ba_file_sach_ma_cu`: `assertSame([], erpGateHits(file, OLD))` cho cả 3 file.
- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Thay** `accounting.ke_toan_mua_hang.manage` → `accounting.ke_toan_phieu_tinh_gia.manage` tại 6 điểm (373,385,390,405 + PriceCalculate:300 + PriceCalculateResult:150). Chỉ đổi chuỗi mã, giữ nguyên logic.
- [x] **Step 4: Chạy, xác nhận PASS.**
- [x] **Step 5: Commit.**

---

### Task 4: Re-point nhóm B — YC nhập theo đơn → mã #2

**Files (ERP):**
- Modify: `app/Model/Warehouse/OrderImportRequest.php:698` (chỉ toán hạng), `:723`, `:731`
- Modify: `app/Http/Controllers/HomeController.php:1347`
- Modify: `resources/views/layouts/topmenubar.blade.php:2243`
- Modify: `resources/views/layouts/topmenubar_old.blade.php:2767`
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitYcNhapTheoDonTest.php`

- [x] **Step 1: Viết test**, `NEW_CODE='accounting.ke_toan_duyet_yc_nhap_theo_don.manage'`:
  - `test_5_file_dung_ma_moi`: 5 file đều chứa NEW_CODE (OrderImportRequest, HomeController, 2 blade — OrderImportRequest tính 1 file).
  - `test_5_file_sach_ma_cu`: `erpGateHits(file, OLD)===[]` cho cả 5 file.
  - `test_giu_toan_hang_kho` (QUAN TRỌNG): `assertStringContainsString('accounting.ke_toan_kho_yc_nhap_theo_don.manage', erpSource(OrderImportRequest))`.
- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Thay** toán hạng mua_hang → mã #2 tại 698 (giữ `ke_toan_kho_yc_nhap_theo_don` + scope), và thay tại 723, 731, HomeController:1347, 2 blade.
- [x] **Step 4: Chạy, xác nhận PASS.**
- [x] **Step 5: Commit.**

---

### Task 5: Re-point nhóm C — Tờ khai hải quan → mã #3

**Files (ERP):**
- Modify: `app/Model/Warehouse/CustomDeclaration.php:544` (chỉ toán hạng), `:583`
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitToKhaiHaiQuanTest.php`

- [x] **Step 1: Viết test**, `NEW_CODE='accounting.ke_toan_xem_to_khai_hai_quan.manage'`:
  - `test_file_dung_ma_moi`: CustomDeclaration chứa NEW_CODE.
  - `test_file_sach_ma_cu`: `erpGateHits(CustomDeclaration, OLD)===[]`.
  - `test_giu_toan_hang_kho`: chứa `accounting.ke_toan_kho_to_khai_hai_quan.manage`.
  - `test_giu_quyen_duyet_tkhq` (QUAN TRỌNG): chứa `purchase.to_khai_hai_quan.approve`.
- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Thay** toán hạng mua_hang → mã #3 tại 544 (giữ kho-code), và tại 583. KHÔNG đụng 575.
- [x] **Step 4: Chạy, xác nhận PASS.**
- [x] **Step 5: Commit.**

---

### Task 6: Lệnh grant 1→3

**Files:**
- Create: `hrm-api/app/Console/Commands/RbacGrantKeToanMuaHangSplitCommand.php`
- Test: `hrm-api/tests/Unit/Permission/KeToanMuaHangSplitGrantWiringTest.php`

**Interfaces:**
- Consumes: `KeToanMuaHangSplitMap` (Task 1).

- [x] **Step 1: Viết test** (mirror `KeToanSplitGrantWiringTest`):
  - `test_command_dung_map_va_signature`: source chứa `use App\Support\Permissions\KeToanMuaHangSplitMap;`, `KeToanMuaHangSplitMap::`, `'rbac:grant-ke-toan-mua-hang-split`.
  - `test_khong_con_dau_vet_ke_toan_split_cu`: KHÔNG chứa `KeToanSplitMap` (không lẫn map cũ), KHÔNG chứa `'rbac:grant-ke-toan-split'` (chuỗi signature cũ).
- [x] **Step 2: Chạy, xác nhận FAIL.**
- [x] **Step 3: Tạo command** — clone `RbacGrantKeToanSplitCommand`, đổi: `use ...KeToanMuaHangSplitMap`, mọi `KeToanSplitMap::`→`KeToanMuaHangSplitMap::`, signature `rbac:grant-ke-toan-mua-hang-split`, report dir `rbac-grant-ke-toan-mua-hang-split`, mô tả tiếng Việt tương ứng. Logic copy pivot giữ nguyên.
- [x] **Step 4: Chạy, xác nhận PASS.**
- [x] **Step 5: Commit.**

---

### Checkpoint cuối
- [x] Chạy `vendor/bin/phpunit --filter KeToanMuaHangSplit` — toàn bộ xanh.
- [x] `grep -rn "ke_toan_mua_hang" app resources routes tests` trong `ERP/TanPhatDev` → chỉ còn `app/Model/Common/Dashboard.php:9` (nhãn). Không còn gate.
- [ ] Deprecate mã cũ: **KHÔNG làm trong plan này** — chờ rollout prod (design §9–10).

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Task 1–6 + verify xong: 3 mã ERP-only `accounting.ke_toan_phieu_tinh_gia.manage` / `accounting.ke_toan_duyet_yc_nhap_theo_don.manage` (gồm dashboard HomeController:1347 + menu THCPNK) / `accounting.ke_toan_xem_to_khai_hai_quan.manage` (chỉ xem; duyệt vẫn `purchase.to_khai_hai_quan.approve`); fixture RBAC MAP seed 3 mã; lệnh `rbac:grant-ke-toan-mua-hang-split`. Test 12/12 (35 assertions); final review Opus sạch. ✓push ERP develop_02 `4ca08a73bc`, hrm-api develop `b0c879811`.
Đang làm dở: —
Bước tiếp theo: catalog-sync → grant dry-run → chạy thật → verify; deprecate mã cũ sau rollout; chưa gop_db. Minor hoãn: `PriceCalculateResult::canView()` `return true` (:148) → gate nhóm A là dead code, cân nhắc xử lý riêng.
Blocked: Không
