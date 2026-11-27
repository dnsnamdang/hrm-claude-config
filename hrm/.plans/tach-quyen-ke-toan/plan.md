# Tách quyền "Kế toán" thành 3 quyền theo màn — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Tách quyền gộp `accounting.ke_toan.manage` ("Kế toán") thành **3 quyền-cờ riêng theo từng màn/chứng từ**, re-point mọi gate ERP+HRM sang mã mới, cấp-lại tự động để không ai mất quyền — mô phỏng đúng đợt tách "Kế toán kho" đã xong.

**Architecture:** 3 mã mới khai DUY NHẤT trong Catalog (`accounting.php`, dùng chung ERP+HRM), đồng bộ DB qua `permission:catalog-sync` — KHÔNG seeder/migration. Gate ERP (`->can()`/notify/blade) đổi token tại 7 điểm; HRM đổi 1 hằng (6 consumer đọc hằng theo tên → lan tự động). Lệnh cấp-lại `rbac:grant-ke-toan-split` nhân 1→3 pivot (role + employee) của mã cũ sang 3 mã mới (idempotent, clone nguyên `rbac:grant-ke-toan-kho-split`). Deprecate mã cũ = bước CUỐI, ngoài plan. Kiểm chứng bằng test DB-free soi source (scanner gate-context) — bám mẫu `HrmKeToanKho*`.

**Tech Stack:** ERP = Laravel 6 / PHP 7.4 / Blade + AngularJS (`develop_02`). HRM = Laravel 8 / PHP 7.4 / nwidart Modules / Spatie permission 5.4 (`develop`). DB **gộp** `hrm_erp_gop` dùng chung 2 app. Test = PHPUnit `PHPUnit\Framework\TestCase` (DB-free, không `-p`).

**Spec:** `HRM/.plans/tach-quyen-ke-toan/design.md` — plan lập luận từ design; executor đọc cả hai.

## Global Constraints

- Catalog là nguồn sự thật DUY NHẤT: `hrm-api/app/Support/Permissions/Catalog/accounting.php`. Đồng bộ DB bằng `php artisan permission:catalog-sync` (thêm/deprecate, KHÔNG xoá cứng). **KHÔNG seeder, KHÔNG migration** cho quyền.
- Mã mới theo quy ước: `accounting.ke_toan_<slug>.manage`, `subsystem_group='Kinh doanh - Tài chính'`, `subsystem='Kế toán'`, `feature='Kế toán'`, `kind='action'`, `scopes=[]`, `depends_on=[]`, `legacy=[]` (mã mới chưa ai có → không cần alias; quyền đến từ lệnh cấp-lại).
- 3 mã mới (đúng thứ tự, nhãn verbatim):
  1. `accounting.ke_toan_phieu_thuong_kd.manage` — "Kế toán — Phiếu thưởng kinh doanh" — `platforms=['erp']`
  2. `accounting.ke_toan_phieu_loi_nhuan.manage` — "Kế toán — Phiếu lợi nhuận" — `platforms=['erp']`
  3. `accounting.ke_toan_yc_hach_toan_bo_sung.manage` — "Kế toán — Yêu cầu hạch toán bổ sung (phối hợp)" — `platforms=['erp','hrm']`
- Mã cũ `accounting.ke_toan.manage` (nhãn "Kế toán") GIỮ NGUYÊN trong Catalog suốt plan (deprecate là bước sau, ngoài plan).
- KHÔNG đổi `code` đã lên prod; KHÔNG bypass Super Admin (HRM); cờ quyền FE fail-closed.
- KHÔNG sửa hrm-client (Nuxt chỉ đọc cờ BE, không gate bằng mã này).
- KHÔNG commit/push khi chưa xin phép. KHÔNG chạy lệnh prod (`catalog-sync`/grant/deprecate) — user tự chạy, chỉ viết + test ở local/dev.
- Mọi tài liệu chỉ trong `HRM/.plans|docs|.superpowers`. KHÔNG tạo file lạ trong `hrm-api`/`TanPhatDev` ngoài file code/test mà plan nêu.

## Review Focus

Năm tình huống spec hàm ý nhưng test từng task không tự chạm — mỗi dòng đã gắn test về task sở hữu code:
1. **OR của `:276` bị phá** (xoá nhầm operand `ke_toan_thanh_toan` khi thay operand kia) → DS YC HTBS chờ duyệt rỗng với kế toán thanh toán. → Task 5 có assert giữ `finance.ke_toan_thanh_toan.manage` TẠI `:276`.
2. **Dashboard `:1422` mất mục "Đề nghị thu tiền chờ duyệt"** do xoá nhầm cả operand `ke_toan_thanh_toan` thay vì chỉ operand `ke_toan`. → Task 5 assert `:1422` CÒN `finance.ke_toan_thanh_toan.manage` và SẠCH mã cũ.
3. **Site ẩn dùng mã cũ bị bỏ sót** (gate "ma" sau khi mã cũ deprecate) → chức năng chặn nhầm. → Task 8 Step 2 grep tổng 2 repo + ERP, chỉ còn ở 3 file whitelist.
4. **HRM đổi hằng nhưng nhầm hằng `:236`/`:242`** (sửa `PERMISSION_ACCOUNTANT` ke_toan_thanh_toan hoặc `PERMISSION_NOTIFY_TARGET` ke_toan_kho) → lệch vai. → Task 6 assert CHỈ `:239` đổi, `:236`+`:242` giữ nguyên giá trị cũ.
5. **Comment provenance bị tính nhầm là gate** (docblock HRM `:20`, ERP ghi chú) khiến test đỏ giả / hoặc đổi nhầm docblock làm sai nghĩa. → Task 2 scanner tự-test loại comment; Task 6 cập nhật docblock `:20` đúng nghĩa mới.

---

### Task 1: Catalog 3 mã mới + lớp map

**Files:**
- Modify: `HRM/hrm-api/app/Support/Permissions/Catalog/accounting.php` (thêm 3 entry sau block mã cũ `accounting.ke_toan.manage`, dòng ~475)
- Create: `HRM/hrm-api/app/Support/Permissions/KeToanSplitMap.php`
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitMapTest.php`

**Interfaces:**
- Produces: `App\Support\Permissions\KeToanSplitMap` với `::OLD_CODE` (string `'accounting.ke_toan.manage'`), `::oldCode(): string`, `::newCodes(): string[]` (3 mã đúng thứ tự Global Constraints), `::all(): string[]` (= `[oldCode, ...newCodes]`, 4 phần tử). Mẫu 1:1 theo `App\Support\Permissions\KeToanKhoSplitMap`.
- Consumes: — (đầu chuỗi)

- [x] **Step 1: Viết test đỏ** `KeToanSplitMapTest` (extends `PHPUnit\Framework\TestCase`):
  - `test_old_code_dung`: `assertSame('accounting.ke_toan.manage', KeToanSplitMap::OLD_CODE)`.
  - `test_ba_ma_moi_dung_thu_tu`: `assertSame(['accounting.ke_toan_phieu_thuong_kd.manage','accounting.ke_toan_phieu_loi_nhuan.manage','accounting.ke_toan_yc_hach_toan_bo_sung.manage'], KeToanSplitMap::newCodes())`.
  - `test_all_la_4_phan_tu`: `assertCount(4, KeToanSplitMap::all())` và `assertSame(KeToanSplitMap::OLD_CODE, KeToanSplitMap::all()[0])`.
  - `test_catalog_khai_du_3_ma_moi_va_giu_ma_cu`: đọc `file_get_contents(.../Catalog/accounting.php)`; với mỗi mã trong `newCodes()` → `assertStringContainsString("'code' => '$code'", $src)`; và `assertStringContainsString("'code' => 'accounting.ke_toan.manage'", $src)` (mã cũ còn nguyên).

- [x] **Step 2: Chạy test → đỏ.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplitMapTest`. Expected: FAIL ("Class KeToanSplitMap not found" / Catalog chưa có mã).

- [x] **Step 3: Tạo `KeToanSplitMap`** — copy cấu trúc `KeToanKhoSplitMap.php`, đổi `OLD_CODE`, `newCodes()` trả đúng 3 mã (Global Constraints), docblock ngắn nêu "tách `accounting.ke_toan.manage` → 3 cờ, Catalog là nguồn, lệnh cấp-lại + test đọc chung lớp này".

- [x] **Step 4: Thêm 3 entry Catalog** vào `accounting.php` ngay SAU block mã cũ `accounting.ke_toan.manage` (kết thúc ~dòng 475). Mỗi entry theo shape Global Constraints (mirror block `accounting.ke_toan_kho_phieu_nhap_mua.manage` dòng 113–124: `legacy => []`). Thứ tự khớp `newCodes()`.

- [x] **Step 5: Chạy test → xanh.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplitMapTest`. Expected: PASS.

- [x] **Step 6: Commit.** `test(ke-toan-split): Catalog 3 mã + KeToanSplitMap`.

---

### Task 2: Scanner DB-free (ERP + HRM)

**Files:**
- Create: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitScan.php`
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitScanTest.php`

**Interfaces:**
- Produces: `Tests\Unit\Permission\KeToanSplitScan` — oracle cho mọi task re-point:
  - `const OLD_CODE = 'accounting.ke_toan.manage'`
  - `apiSource(string $rel): string` — đọc file dưới `HRM/hrm-api/`
  - `erpSource(string $rel): string` — đọc file dưới `ERP/TanPhatDev/` (gốc = `dirname(hrmApiRoot, 2) . '/ERP/TanPhatDev'`)
  - `apiGateHits(string $rel, string $needle): string[]` / `erpGateHits(string $rel, string $needle): string[]` — các dòng GATE (không comment) trong 1 file chứa `$needle`, trả `["rel:line: text"]`; `[]` nếu sạch.
  - Logic nhận diện gate + bỏ comment/`//`-cuối-dòng: **copy nguyên** từ `HrmKeToanKhoScan` (GATE_PATTERNS, `isCommentLine`, `stripTrailingLineComment`, `isGateLine`). GATE_PATTERNS phải gồm `->can\s*\(`, `const\s+\w*PERM\w*\s*=`, `[Cc]urrentEmployeeHasPermission`, và notify helper — thêm pattern `/sendNotify\w*Permission\s*\(/` cho gate ERP.
- Consumes: — (công cụ độc lập)

- [x] **Step 1: Viết test đỏ** `KeToanSplitScanTest` (extends `PHPUnit\Framework\TestCase`) — chốt scanner đáng tin TRƯỚC khi dùng làm oracle:
  - `test_phat_hien_dong_can`: dựng chuỗi nhiều dòng gồm `if ($u->can('accounting.ke_toan.manage'))`, một docblock `* dùng accounting.ke_toan.manage trước đây`, và `// accounting.ke_toan.manage`; qua `fileGateHits`-style assert: dòng `->can(...)` ĐƯỢC tính, hai dòng comment KHÔNG. (Dùng 1 file fixture tạm trong scratchpad hoặc assert qua một file thật đã biết — ưu tiên fixture.)
  - `test_doc_duoc_erp_va_api`: `assertStringContainsString('class HomeController', KeToanSplitScan::erpSource('app/Http/Controllers/HomeController.php'))` và `assertStringContainsString('PERMISSION_ACCOUNTANT', KeToanSplitScan::apiSource('Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php'))`.

- [x] **Step 2: Chạy test → đỏ.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplitScanTest`. Expected: FAIL ("Class KeToanSplitScan not found").

- [x] **Step 3: Tạo `KeToanSplitScan`** — copy `HrmKeToanKhoScan`, rút gọn về per-file API ở trên (bỏ quét toàn cây), thêm `erpRoot()`/`erpSource()`/`erpGateHits()`, thêm pattern notify. Giữ nguyên bộ lọc comment.

- [x] **Step 4: Chạy test → xanh.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplitScanTest`. Expected: PASS.

- [x] **Step 5: Commit.** `test(ke-toan-split): scanner DB-free ERP+HRM`.

---

### Task 3: ERP re-point — Phiếu thưởng kinh doanh (#1)

**Files:**
- Modify: `ERP/TanPhatDev/app/Http/Controllers/Accounting/BillBonusBusinessController.php:112`
- Modify: `ERP/TanPhatDev/resources/views/accounting/bill_bonus_business/index.blade.php:80`
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitPhieuThuongKdTest.php`

**Interfaces:**
- Consumes: `KeToanSplitScan` (Task 2), mã `accounting.ke_toan_phieu_thuong_kd.manage` (Task 1).

- [x] **Step 1: Viết test đỏ** `KeToanSplitPhieuThuongKdTest`:
  - `test_controller_va_blade_dung_ma_moi`: `assertStringContainsString("accounting.ke_toan_phieu_thuong_kd.manage", KeToanSplitScan::erpSource('app/Http/Controllers/Accounting/BillBonusBusinessController.php'))`; tương tự với blade `resources/views/accounting/bill_bonus_business/index.blade.php`.
  - `test_hai_file_sach_ma_cu`: `assertSame([], KeToanSplitScan::erpGateHits('app/Http/Controllers/Accounting/BillBonusBusinessController.php', KeToanSplitScan::OLD_CODE))` và tương tự blade.

- [x] **Step 2: Chạy → đỏ.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplitPhieuThuongKdTest`. Expected: FAIL.

- [x] **Step 3: Re-point.** Controller `:112` `!auth()->user()->can('accounting.ke_toan.manage')` → `...ke_toan_phieu_thuong_kd.manage`. Blade `:80` `can('accounting.ke_toan.manage')` → `...ke_toan_phieu_thuong_kd.manage` (chỉ đổi mã, giữ nguyên logic `create_link`).

- [x] **Step 4: Chạy → xanh.** Run: như Step 2. Expected: PASS.

- [x] **Step 5: Commit.** `feat(erp): phiếu thưởng KD dùng ke_toan_phieu_thuong_kd`.

---

### Task 4: ERP re-point — Phiếu lợi nhuận (#2)

**Files:**
- Modify: `ERP/TanPhatDev/app/Http/Controllers/IncomeExpenditure/BillProfitsController.php:132`
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitPhieuLoiNhuanTest.php`

**Interfaces:**
- Consumes: `KeToanSplitScan`, mã `accounting.ke_toan_phieu_loi_nhuan.manage`.

- [x] **Step 1: Viết test đỏ** `KeToanSplitPhieuLoiNhuanTest`:
  - `test_controller_dung_ma_moi`: `assertStringContainsString("accounting.ke_toan_phieu_loi_nhuan.manage", KeToanSplitScan::erpSource('app/Http/Controllers/IncomeExpenditure/BillProfitsController.php'))`.
  - `test_file_sach_ma_cu`: `assertSame([], KeToanSplitScan::erpGateHits('app/Http/Controllers/IncomeExpenditure/BillProfitsController.php', KeToanSplitScan::OLD_CODE))`.

- [x] **Step 2: Chạy → đỏ.** Run: `vendor/bin/phpunit --filter KeToanSplitPhieuLoiNhuanTest`. Expected: FAIL.

- [x] **Step 3: Re-point.** `:132` `can('accounting.ke_toan.manage')` → `...ke_toan_phieu_loi_nhuan.manage`.

- [x] **Step 4: Chạy → xanh.** Expected: PASS.

- [x] **Step 5: Commit.** `feat(erp): phiếu lợi nhuận dùng ke_toan_phieu_loi_nhuan`.

---

### Task 5: ERP re-point — YC hạch toán bổ sung (#3) + dashboard

**Files:**
- Modify: `ERP/TanPhatDev/app/Model/IncomeExpenditure/AdditionAccountingRequest.php:276` (OR scope) và `:520` (`canApproveSupport`)
- Modify: `ERP/TanPhatDev/app/Services/Sale/Firm/Settlement/SettlemenHandleAdditionalAccountingService.php:244` (notify)
- Modify: `ERP/TanPhatDev/app/Http/Controllers/HomeController.php:1422` (dashboard — BỎ operand)
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitYcHachToanBoSungTest.php`

**Interfaces:**
- Consumes: `KeToanSplitScan`, mã `accounting.ke_toan_yc_hach_toan_bo_sung.manage`.
- Lưu ý `:276` và `:1422` là biểu thức OR 2 operand — chỉ đụng operand `accounting.ke_toan.manage`, operand `finance.ke_toan_thanh_toan.manage` PHẢI còn.

- [x] **Step 1: Viết test đỏ** `KeToanSplitYcHachToanBoSungTest` (mỗi assert soi `erpSource` của đúng file):
  - `test_scope_276_doi_operand_giu_or`: source `AdditionAccountingRequest.php` chứa chuỗi khối `:276` có CẢ `finance.ke_toan_thanh_toan.manage` VÀ `accounting.ke_toan_yc_hach_toan_bo_sung.manage` (assert chứa cả 2 token).
  - `test_canApproveSupport_520_ma_moi`: chứa `can('accounting.ke_toan_yc_hach_toan_bo_sung.manage')`.
  - `test_notify_244_ma_moi`: source `SettlemenHandleAdditionalAccountingService.php` chứa `sendNotifyWithToDiffrentCompanyPermission('accounting.ke_toan_yc_hach_toan_bo_sung.manage'`.
  - `test_dashboard_1422_giu_thanh_toan_bo_ma_cu`: source `HomeController.php` chứa `finance.ke_toan_thanh_toan.manage` và `assertSame([], KeToanSplitScan::erpGateHits('app/Http/Controllers/HomeController.php', KeToanSplitScan::OLD_CODE))`.
  - `test_ba_file_sach_ma_cu`: `erpGateHits(OLD_CODE)` = `[]` cho cả 3 file `AdditionAccountingRequest.php`, `SettlemenHandleAdditionalAccountingService.php`, `HomeController.php`.

- [x] **Step 2: Chạy → đỏ.** Run: `vendor/bin/phpunit --filter KeToanSplitYcHachToanBoSungTest`. Expected: FAIL.

- [x] **Step 3: Re-point (4 điểm).**
  - `:276` — đổi operand 2: `... || $user->can('accounting.ke_toan_yc_hach_toan_bo_sung.manage')` (GIỮ operand 1 `finance.ke_toan_thanh_toan.manage` + toán tử `||`).
  - `:520` `can('accounting.ke_toan.manage')` → `...ke_toan_yc_hach_toan_bo_sung.manage` (giữ nguyên `&& in_array(... company_ids)`).
  - `:244` đối số 1 của `sendNotifyWithToDiffrentCompanyPermission` → `...ke_toan_yc_hach_toan_bo_sung.manage`.
  - `:1422` — **xoá** ` || $logged_user->can('accounting.ke_toan.manage')`, còn lại chỉ `if ($logged_user->can('finance.ke_toan_thanh_toan.manage'))`.

- [x] **Step 4: Chạy → xanh.** Expected: PASS (Review Focus #1, #2 chốt ở đây).

- [x] **Step 5: Commit.** `feat(erp): YC hạch toán bổ sung + dashboard tách khỏi ke_toan.manage`.

---

### Task 6: HRM re-point — hằng + docblock

**Files:**
- Modify: `HRM/hrm-api/Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php:239` (hằng) — KHÔNG đụng `:236`, `:242`
- Modify: `HRM/hrm-api/Modules/ApprovalCenter/Definitions/Finance/AdditionAccountingRequestDefinition.php:20` (docblock provenance — chỉnh nghĩa)
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitHrmConstTest.php`

**Interfaces:**
- Consumes: `KeToanSplitScan`, mã `accounting.ke_toan_yc_hach_toan_bo_sung.manage`.
- 6 consumer HRM đọc hằng `PERMISSION_ACCOUNTANT_SUPPORT` **theo tên** (`:343`, `:716`, `:749 isSupportAccountant`, `Services/AdditionAccountingRequestService.php:146`, `ApprovalCenterDefinition :59, :141`) → đổi GIÁ TRỊ hằng là đủ, KHÔNG sửa consumer.

- [x] **Step 1: Viết test đỏ** `KeToanSplitHrmConstTest`:
  - `test_const_support_dung_ma_moi`: `assertStringContainsString("const PERMISSION_ACCOUNTANT_SUPPORT = 'accounting.ke_toan_yc_hach_toan_bo_sung.manage';", KeToanSplitScan::apiSource('Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php'))`.
  - `test_const_thanh_toan_va_notify_giu_nguyen` (Review Focus #4): cùng source CÒN `const PERMISSION_ACCOUNTANT = 'finance.ke_toan_thanh_toan.manage';` và `const PERMISSION_NOTIFY_TARGET = 'accounting.ke_toan_kho_yc_hach_toan_bo_sung.manage';`.
  - `test_file_sach_ma_cu_o_gate`: `assertSame([], KeToanSplitScan::apiGateHits('Modules/Finance/Entities/AdditionAccountingRequest/AdditionAccountingRequest.php', KeToanSplitScan::OLD_CODE))`.
  - `test_definition_docblock_khong_con_ma_cu`: `assertStringNotContainsString('accounting.ke_toan.manage', KeToanSplitScan::apiSource('Modules/ApprovalCenter/Definitions/Finance/AdditionAccountingRequestDefinition.php'))` (docblock đã nêu mã mới).

- [x] **Step 2: Chạy → đỏ.** Run: `vendor/bin/phpunit --filter KeToanSplitHrmConstTest`. Expected: FAIL.

- [x] **Step 3: Re-point.**
  - `:239` giá trị hằng `PERMISSION_ACCOUNTANT_SUPPORT` → `'accounting.ke_toan_yc_hach_toan_bo_sung.manage'` (tên hằng giữ nguyên).
  - Docblock `AdditionAccountingRequestDefinition.php:20`: đổi cụm "Lập phiếu cần `accounting.ke_toan.manage`" → "...cần `accounting.ke_toan_yc_hach_toan_bo_sung.manage`" (giữ nguyên câu còn lại).

- [x] **Step 4: Chạy → xanh.** Expected: PASS.

- [x] **Step 5: Commit.** `feat(hrm): PERMISSION_ACCOUNTANT_SUPPORT dùng ke_toan_yc_hach_toan_bo_sung`.

---

### Task 7: Lệnh cấp-lại 1→3

**Files:**
- Create: `HRM/hrm-api/app/Console/Commands/RbacGrantKeToanSplitCommand.php`
- Test: `HRM/hrm-api/tests/Unit/Permission/KeToanSplitGrantWiringTest.php`

**Interfaces:**
- Consumes: `App\Support\Permissions\KeToanSplitMap` (Task 1).
- Produces: lệnh `rbac:grant-ke-toan-split` với flags `--dry-run`, `--verify`, `--report-dir=` — nhân 1→3 pivot `role_has_permissions` + `employee_has_permissions` của mã cũ sang 3 mã mới, idempotent (md5 chữ ký), tiền-kiểm 4 mã có-mặt-không-deprecate. **Clone nguyên** `RbacGrantKeToanKhoSplitCommand`, đổi: dùng `KeToanSplitMap`, signature, description, tên file CSV (`cap-ma-ke-toan.csv` / `doi-chieu-ke-toan.csv`), thư mục báo cáo mặc định `rbac-grant-ke-toan-split/`.

- [x] **Step 1: Viết test đỏ** `KeToanSplitGrantWiringTest` (DB-free, soi source — tránh DB thật non-transactional):
  - `test_command_dung_map_va_signature`: source lệnh chứa `use App\Support\Permissions\KeToanSplitMap;`, `KeToanSplitMap::` (không còn `KeToanKhoSplitMap`), và `'rbac:grant-ke-toan-split`.
  - `test_command_khong_con_dau_vet_ke_toan_kho`: `assertStringNotContainsString('ke-toan-kho', $src)` và `assertStringNotContainsString('KeToanKhoSplitMap', $src)`.

- [x] **Step 2: Chạy → đỏ.** Run: `vendor/bin/phpunit --filter KeToanSplitGrantWiringTest`. Expected: FAIL (file chưa có).

- [x] **Step 3: Tạo lệnh** — copy `RbacGrantKeToanKhoSplitCommand.php`, thay class name + map + signature/description + tên CSV + thư mục báo cáo như Interfaces. Thân (`grant`/`verify`/`srcRows`/`existingSigs`/`sig`) giữ nguyên (logic đã kiểm thực chiến đợt ke_toan_kho).

- [x] **Step 4: Chạy → xanh.** Run: như Step 2. Expected: PASS.
  - Sanity (không ghi DB): `php artisan rbac:grant-ke-toan-split --dry-run --report-dir=<scratchpad>` chạy không lỗi khi 4 mã đã sync local; nếu DB local chưa sync 3 mã → lệnh in "chạy permission:catalog-sync trước" và exit 1 (đúng tiền-kiểm). Ghi kết quả vào ledger, KHÔNG coi là test bắt buộc.

- [x] **Step 5: Commit.** `feat(rbac): lệnh rbac:grant-ke-toan-split cấp-lại 1→3`.

---

### Task 8: Completeness + verify toàn cục

**Files:** không sửa nguồn (trừ dọn comment nếu cần để grep sạch).

**Interfaces:** Consumes mọi task trước.

- [x] **Step 1: Suite split xanh.** Run: `cd HRM/hrm-api && vendor/bin/phpunit --filter KeToanSplit` (một tiến trình, KHÔNG `-p`). Expected: tất cả PASS. Còn đỏ → còn site sót: tìm, map, re-point (có thể cần Ruling), KHÔNG sửa test cho vừa.
- [x] **Step 2: Grep tổng (Review Focus #3).** `grep -rn "accounting.ke_toan.manage"` trên `ERP/TanPhatDev/app ERP/TanPhatDev/resources ERP/TanPhatDev/routes` và `HRM/hrm-api/app HRM/hrm-api/Modules HRM/hrm-client` → chỉ còn ở **3 file whitelist**: `Catalog/accounting.php` (định nghĩa mã cũ, chưa deprecate), `KeToanSplitMap.php`, `RbacGrantKeToanSplitCommand.php` (nếu gián tiếp qua map thì 0). Mọi hit khác = gate sót → xử lý. Ghi kết quả vào ledger.
- [x] **Step 3: Final whole-branch review** (fresh reviewer, model mạnh nhất): gói `review-package` MERGE_BASE..HEAD; Review Focus 1–5 verbatim; con trỏ tới ledger `Ruling:`. Re-grade theo hiệu ứng → Critical/Important vào 1 fix pass (mỗi fix RED→GREEN + suite xanh); Minor → ledger. Xong → `superpowers:finishing-a-development-branch` (KHÔNG push/merge khi chưa xin phép).
- [ ] **Step 4 (ghi chú rollout — KHÔNG chạy):** prod do user chạy theo design §7: deploy → `catalog-sync` (qua `~/build_tpe.sh`) → `rbac:grant-ke-toan-split --dry-run`→thật→`--verify` → sau khi live + grep sạch mới gỡ mã cũ khỏi Catalog (deprecate, bước cuối ngoài plan).

---

## Self-Review

**1. Spec coverage (design §5–§7):** §5 ba mã → Task 1. §6 ERP: `:112`+blade→Task3, `:132`→Task4, `:276`/`:520`/`:244`/`:1422`→Task5 (thêm blade `index.blade.php:80` phát hiện lúc grep, cùng màn #1). §6 HRM hằng `:239` + lan tự động + giữ `:242`→Task6. §6 Catalog+cấp-lại→Task1+Task7; deprecate = §7 bước cuối, ghi chú Task8 Step4 (ngoài plan, đúng design §8.). §7 rollout→Task8 Step4. Không gap.

**2. Step scan:** mỗi re-point step đổi đúng token tại file:line đã chỉ; mỗi test step có tên + assert cụ thể. Không "TBD"/"xử lý edge case". Grant command không viết lại thân (clone proven) → step chỉ nêu token đổi, không transcribe ~250 dòng.

**3. Type consistency:** `KeToanSplitMap` (Task1) dùng nguyên tên ở Task7. `KeToanSplitScan::{apiSource,erpSource,apiGateHits,erpGateHits,OLD_CODE}` định nghĩa Task2, mọi task sau gọi đúng tên đó. Mã luôn `accounting.ke_toan_<slug>.manage` khớp Global Constraints.

**4. Review Focus:** #1 OR `:276`→Task5 `test_scope_276_doi_operand_giu_or`; #2 dashboard→Task5 `test_dashboard_1422...`; #3 grep sót→Task8 Step2; #4 nhầm hằng→Task6 `test_const_thanh_toan_va_notify_giu_nguyen`; #5 comment provenance→Task2 self-test + Task6 docblock. Đủ 5, mỗi dòng có test ở task sở hữu.

**5. Proportion:** plan ngắn hơn tổng nguồn sửa; không chép thân map/command/scanner (trỏ file mẫu ke_toan_kho), chỉ ghi file:line + token + tên test. Đạt.

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Task 1–8 (SDD) xong; final whole-branch review (Opus) ra 1 Critical (fixture ERP `AccountingCatalog::MAP` thiếu 3 mã mới → `UnknownPermissionCode`) đã fix RED→GREEN; suite `--filter KeToanSplit` 23 tests/45 assertions xanh. ✓push hrm-api develop `866054ddc`, ERP develop_02 `52b7fdcdeb`. Quyết định user: 3 mã (phiếu thưởng KD / phiếu lợi nhuận / YC hạch toán bổ sung); dashboard 1422 bỏ operand mã cũ, chỉ giữ `finance.ke_toan_thanh_toan.manage`.
Đang làm dở: —
Bước tiếp theo: Rollout (Task 8 Step 4, user chạy): deploy → catalog-sync → `rbac:grant-ke-toan-split` dry-run → chạy thật → verify → deprecate mã cũ sau cùng. Chưa gop_db. Khi deprecate: grep mở rộng sang `tests/` (Important của review).
Blocked: Không
