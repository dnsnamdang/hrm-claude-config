# Tách quyền `truong_phong_ke_toan.approve` theo màn — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (inline, TDD). Steps use checkbox (`- [ ]`).

**Goal:** Tách mã-cờ ERP `accounting.truong_phong_ke_toan.approve` thành 2 mã theo màn, không ai mất quyền, không đổi hành vi runtime.

**Architecture:** Khai 2 mã mới ở Catalog hrm-api (shared ERP+HRM) → re-point gate ở 4 file ERP → thêm fixture MAP → lệnh cấp-lại 1→2 + test Unit DB-free. Mirror sibling `ke_toan_mua_hang` (đã push 2026-11-27).

**Tech Stack:** ERP Laravel 6 / Blade / AngularJS; hrm-api Laravel 8; test `PHPUnit\Framework\TestCase` (DB-free).

**Spec:** `ERP/.plans/tach-quyen-truong-phong-ke-toan/design.md`

## Global Constraints
- 2 mã mới (đúng thứ tự Catalog & Map):
  1. `accounting.truong_phong_ke_toan_phieu_xuat_giu.approve` — tên "Trưởng phòng kế toán — Phiếu xuất giữ"
  2. `accounting.truong_phong_ke_toan_de_nghi_xuat_kho.view` — tên "Trưởng phòng kế toán — Xem đề nghị xuất kho"
- Mã cũ `accounting.truong_phong_ke_toan.approve` **GIỮ** trong Catalog + fixture MAP (deprecate sau rollout — ngoài phạm vi).
- Entry Catalog cả 2: `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `feature='Kế toán'`, `scopes=[]`, `depends_on=[]`, `platforms=['erp']`, `legacy=[]`. `kind`: mã①=`approve`, mã②=`view`.
- Re-point CHỈ các gate mã cũ; KHÔNG thêm gate mới, KHÔNG đụng toán hạng OR (`finance.giu_hang_ban_kiem_soat.approve`, `finance.phieu_hang_giu.view`, `is_warehouse_accountant`).
- KHÔNG sửa `KeToanSplitScan.php` (helper dùng chung — reuse).
- KHÔNG commit/push (chưa được phép).

## Review Focus
- Sót 1 occurrence mã cũ ở file màn ① (HomeController có 2 chỗ lồng nhau, blade có 2 @if) → test `erpGateHits(file, OLD) === []` bắt.
- Thêm nhầm/đổi nhầm toán hạng OR khi sửa → test `assertStringContainsString` cho OR operand ở WarehousePrepickRequest/HomeController.
- Quên thêm mã mới vào fixture MAP → suite RBAC ERP ném `UnknownPermissionCode`; test fixture bắt (DB-free).

---

### Task 1: Catalog 2 mã mới + SplitMap (hrm-api)

**Files:**
- Modify: `hrm-api/app/Support/Permissions/Catalog/accounting.php` (chèn 2 entry ngay sau entry mã cũ `truong_phong_ke_toan.approve`, dòng ~526)
- Create: `hrm-api/app/Support/Permissions/TruongPhongKeToanSplitMap.php`
- Test: `hrm-api/tests/Unit/Permission/TruongPhongKeToanSplitMapTest.php`

**Interfaces:**
- Produces: `TruongPhongKeToanSplitMap::OLD_CODE` = `'accounting.truong_phong_ke_toan.approve'`; `::newCodes()` = 2 mã (đúng thứ tự trên); `::oldCode()`; `::all()` = `[old, ...new]` (3 phần tử).

- [x] **Step 1: Viết test** `TruongPhongKeToanSplitMapTest` (mirror `KeToanMuaHangSplitMapTest`): `test_old_code_dung` (assertSame OLD_CODE), `test_hai_ma_moi_dung_thu_tu` (assertSame 2 mã), `test_all_la_3_phan_tu` (assertCount 3, phần tử[0]=OLD_CODE), `test_catalog_khai_du_2_ma_moi_va_giu_ma_cu` (đọc `accounting.php`, assert chứa `'code' => '<mã①>'`, `'code' => '<mã②>'`, và `'code' => 'accounting.truong_phong_ke_toan.approve'`).
- [x] **Step 2: Chạy test → FAIL** (class Map chưa tồn tại). Run: `cd hrm-api && vendor/bin/phpunit --filter TruongPhongKeToanSplitMapTest`
- [x] **Step 3: Tạo `TruongPhongKeToanSplitMap`** (mirror `KeToanMuaHangSplitMap`: const OLD_CODE, oldCode(), newCodes()=2 mã, all()=array_merge).
- [x] **Step 4: Thêm 2 entry Catalog** vào `accounting.php` ngay sau block mã cũ (sau dòng 526), mỗi entry theo shape Global Constraints (mã① kind=approve, mã② kind=view), kèm comment `// tách từ accounting.truong_phong_ke_toan.approve theo từng màn`.
- [x] **Step 5: Chạy test → PASS.** Run: `cd hrm-api && vendor/bin/phpunit --filter TruongPhongKeToanSplitMapTest`

### Task 2: ERP re-point màn ① Phiếu xuất giữ (3 file) + fixture MAP

**Files:**
- Modify: `ERP/TanPhatDev/app/Model/Warehouse/WarehousePrepickRequest.php:248,270`
- Modify: `ERP/TanPhatDev/app/Http/Controllers/HomeController.php:2140,2143`
- Modify: `ERP/TanPhatDev/resources/views/layouts/topmenubar_old.blade.php:1439,1454`
- Modify: `ERP/TanPhatDev/tests/Feature/Rbac/Concerns/AccountingCatalog.php` (MAP: thêm 2 dòng `'<mã①>' => [[], []],` và `'<mã②>' => [[], []],` sau dòng mã cũ `truong_phong_ke_toan.approve` ~dòng 59)
- Test: `hrm-api/tests/Unit/Permission/TruongPhongKeToanSplitPhieuXuatGiuTest.php`, `TruongPhongKeToanSplitRbacFixtureTest.php`

**Interfaces:**
- Consumes: `TruongPhongKeToanSplitMap` (Task 1) cho hằng mã trong test.

- [x] **Step 1: Viết test** `TruongPhongKeToanSplitPhieuXuatGiuTest` (mirror `KeToanMuaHangSplitPhieuTinhGiaTest`): OLD=mã cũ, NEW=`<mã①>`, FILES = 3 file trên. `test_moi_file_dung_ma_moi_va_khong_con_ma_cu`: mỗi file `assertStringContainsString(NEW)` + `assertSame([], erpGateHits(file, OLD))`. Thêm `test_giu_toan_hang_or`: WarehousePrepickRequest + HomeController `assertStringContainsString('finance.giu_hang_ban_kiem_soat.approve')` và `assertStringContainsString('finance.phieu_hang_giu.view')`; blade `assertStringContainsString('is_warehouse_accountant')`.
- [x] **Step 2: Viết test** `TruongPhongKeToanSplitRbacFixtureTest` (mirror sibling): NEW_CODES=2 mã, đọc `erpSource(FIXTURE)` assert chứa cả 2 mã.
- [x] **Step 3: Chạy 2 test → FAIL.** Run: `cd hrm-api && vendor/bin/phpunit --filter "TruongPhongKeToanSplitPhieuXuatGiu|TruongPhongKeToanSplitRbacFixture"`
- [x] **Step 4: Re-point 3 file ERP** — đổi cả 2 occurrence mỗi file từ `accounting.truong_phong_ke_toan.approve` → `<mã①>` (giữ nguyên dấu nháy đơn/kép hiện có từng chỗ, giữ nguyên toán hạng OR). Dùng `replace_all` thận trọng (HomeController 2 chỗ lồng — đổi cả 2).
- [x] **Step 5: Thêm 2 dòng fixture MAP** vào `AccountingCatalog.php` sau dòng 59.
- [x] **Step 6: Chạy 2 test → PASS.** Run như Step 3.

### Task 3: ERP re-point màn ② Đề nghị xuất kho (WarehouseExportRequest)

**Files:**
- Modify: `ERP/TanPhatDev/app/Model/Warehouse/WarehouseExportRequest.php:1033`
- Test: `hrm-api/tests/Unit/Permission/TruongPhongKeToanSplitDeNghiXuatKhoTest.php`

- [x] **Step 1: Viết test** `TruongPhongKeToanSplitDeNghiXuatKhoTest`: OLD=mã cũ, NEW=`<mã②>`, FILE=WarehouseExportRequest. `test_dung_ma_moi_va_khong_con_ma_cu`: `assertStringContainsString(NEW)` + `assertSame([], erpGateHits(FILE, OLD))`. `test_giu_cac_gate_khac`: assert còn `isWarehouseStocker` và `'Xem đề nghị xuất kho theo tổng công ty'` (canView không bị hỏng chỗ khác).
- [x] **Step 2: Chạy test → FAIL.** Run: `cd hrm-api && vendor/bin/phpunit --filter TruongPhongKeToanSplitDeNghiXuatKho`
- [x] **Step 3: Re-point** dòng 1033: `accounting.truong_phong_ke_toan.approve` → `<mã②>` (giữ `$this->status != 3 && ... return true;`).
- [x] **Step 4: Chạy test → PASS.** Run như Step 2.

### Task 4: Lệnh cấp-lại 1→2 + wiring test (hrm-api)

**Files:**
- Create: `hrm-api/app/Console/Commands/RbacGrantTruongPhongKeToanSplitCommand.php`
- Test: `hrm-api/tests/Unit/Permission/TruongPhongKeToanSplitGrantWiringTest.php`

**Interfaces:**
- Consumes: `TruongPhongKeToanSplitMap` (Task 1).

- [x] **Step 1: Viết test** `TruongPhongKeToanSplitGrantWiringTest` (mirror `KeToanMuaHangSplitGrantWiringTest`): `apiSource(FILE)` assert chứa `use App\Support\Permissions\TruongPhongKeToanSplitMap;`, `TruongPhongKeToanSplitMap::`, `'rbac:grant-truong-phong-ke-toan-split`; và KHÔNG chứa `KeToanMuaHangSplitMap::` / `KeToanSplitMap::` (không lẫn sibling).
- [x] **Step 2: Chạy test → FAIL.** Run: `cd hrm-api && vendor/bin/phpunit --filter TruongPhongKeToanSplitGrantWiring`
- [x] **Step 3: Tạo command** mirror `RbacGrantKeToanMuaHangSplitCommand` (copy nguyên logic 1→N, đổi: class name, `use ...TruongPhongKeToanSplitMap`, signature `rbac:grant-truong-phong-ke-toan-split`, report-dir `rbac-grant-truong-phong-ke-toan-split`, tên CSV `cap-ma-truong-phong-ke-toan.csv`/`doi-chieu-truong-phong-ke-toan.csv`, description). Logic 1→N không đổi (chạy đúng cho 2 mã).
- [x] **Step 4: Chạy test → PASS.** Run như Step 2.
- [x] **Step 5: Chạy toàn bộ suite split → xanh.** Run: `cd hrm-api && vendor/bin/phpunit --filter TruongPhongKeToanSplit`

## Ngoài phạm vi (user tự chạy sau)
`permission:catalog-sync` (prod qua build_tpe.sh) → cấp 2 mã ở `/admin/roles` → `rbac:grant-truong-phong-ke-toan-split --dry-run` rồi chạy thật → gop_db → deprecate mã cũ sau rollout.

### Checkpoint — 2026-11-28 17:30 (wrap up cuối ngày)
Vừa hoàn thành: 4 task (Inline/executing-plans, TDD). Quyết định đã chốt 09:21: tách đôi; giữ điểm ĐNXK thành mã `.view`; giữ tiền tố `truong_phong_ke_toan_`. Mã mới `accounting.truong_phong_ke_toan_phieu_xuat_giu.approve` (6 chỗ: WarehousePrepickRequest ×2, HomeController ×2, topmenubar_old ×2) + `accounting.truong_phong_ke_toan_de_nghi_xuat_kho.view` (WarehouseExportRequest::canView). Fixture MAP +2. Lệnh `rbac:grant-truong-phong-ke-toan-split`. Suite `--filter TruongPhongKeToanSplit` 9/9 (26 assertions); final review Opus 0 Critical/0 Important/4 Minor (deferred, xem progress.md).
Đang làm dở: **CHƯA commit/push** — ERP TanPhatDev develop_02 (`WarehousePrepickRequest.php`, `HomeController.php`, `topmenubar_old.blade.php`, `WarehouseExportRequest.php` hunk ~1033, `tests/Feature/Rbac/Concerns/AccountingCatalog.php`); hrm-api develop (`Catalog/accounting.php`, `TruongPhongKeToanSplitMap.php`, `RbacGrantTruongPhongKeToanSplitCommand.php`, 5 test `TruongPhongKeToanSplit*`). Lưu ý `WarehouseExportRequest.php` + `accounting.php` dính chung thay đổi việc khác (cờ dính lắp đặt; khai tử chi phí lắp đặt).
Bước tiếp theo: Commit + push (chọn đúng hunk) khi user cho phép → `permission:catalog-sync` → cấp 2 mã `/admin/roles` → `rbac:grant-truong-phong-ke-toan-split` (hoặc lệnh tổng `rbac:grant-all-ke-toan-splits`) → gop_db → deprecate mã cũ.
Blocked:
