# Plan — Khai tử chuỗi Chi phí lắp đặt gắn `App\Contract`

Spec: `./design.md` · Không commit/push · Không gộp DB.
Đây là task **GỠ BỎ** (không sinh hành vi mới) → không RED-GREEN; verify = `php -l` + grep + (tuỳ) chạy suite RBAC.

## Global constraints
- Không đổi `code` mã prod; gỡ quyền = gỡ entry Catalog để `catalog-sync` đặt `deprecated_at` (KHÔNG xoá dòng DB).
- Cờ phân quyền fail-closed; KHÔNG hard-code `=true`.
- Giữ fixture MAP ERP (code còn tham chiếu 4 mã) — KHÔNG động.
- Sửa Catalog ở `HRM/hrm-api/`; sửa nút ở `ERP/TanPhatDev/`; docs chỉ ở `ERP/.plans/`.

## Task 1 — Gỡ 4 entry Catalog (HARD REQ: biến khỏi picker)  [hrm-api]
- `app/Support/Permissions/Catalog/accounting.php`: xoá block `accounting.de_nghi_tam_ung_chi_phi_lap_dat.approve` + block `accounting.chi_phi_lap_dat.approve` (kèm comment `// ghi chú:` ngay trên mỗi block).
- `app/Support/Permissions/Catalog/customer_care.php`: xoá block `customer_care.lap_dat.manage` + block `customer_care.du_toan_chi_phi_lap_dat.create`.
- Verify: `php -l` 2 file; grep 4 code string → rỗng trong 2 file Catalog.
- STATUS: [x] xong (php -l sạch; grep 4 mã → RỖNG trong 2 file Catalog)

## Task 2 — Gỡ 3 nút lối vào (khai tử UI)  [TanPhatDev]
- `app/Datatables/Sale/ContractDatatable.php` (~438-440): bỏ `if ($contract->canInstallEstimate()) { ... 'Dự toán chi phí lắp đặt' ... }`.
- `app/Http/Controllers/Tech/InstallSummaryController.php` (~102-104): bỏ `if ($object->canAdvance()) { ... 'Đề nghị tạm ứng chi phí' ... }`.
- `app/Http/Controllers/Tech/InstallRequestController.php` (~98-100): bỏ `if ($object->canApprove()) { ... 'Giao lịch' ... }`.
- Verify: `php -l` 3 file; grep 3 chuỗi nút → rỗng.
- STATUS: [x] xong (php -l 3 file sạch; grep 3 chuỗi nút → RỖNG)

## Task 3 — Verify tổng + ledger
- `php -l` cả 5 file sửa sạch.
- grep: 4 mã KHÔNG còn trong Catalog; 3 nút KHÔNG còn; fixture MAP VẪN còn đủ 4 mã.
- (tuỳ DB) chạy `--filter CustomerCareScopeConversion` + Accounting fixture nếu `hrm_erp_rbac_test` sẵn → xanh.
- Ghi STATUS done vào plan này. KHÔNG commit/push.
- STATUS: [x] xong — xem Checkpoint dưới.

## Checkpoint — 2026-11-28
Vừa hoàn thành: cả 3 task (gỡ 4 entry Catalog + gỡ 3 nút lối vào + verify).
Đã verify:
- `php -l` sạch cả 5 file (2 Catalog hrm-api + 3 file ERP).
- grep 4 mã quyền → RỖNG trong 2 file Catalog.
- grep 3 chuỗi nút → RỖNG trong 3 file ERP.
- fixture MAP ERP (`AccountingCatalog.php`, `CustomerCareCatalog.php`) VẪN còn đủ 4 mã — KHÔNG đụng (đúng chủ ý).
- Suite `CustomerCareScopeConversion`: KHÔNG chạy được local vì thiếu DB `hrm_erp_rbac_test` (guard trả `:memory:` → 4 test fail-bằng-guard, không do thay đổi này). Fixture không đổi nên test vẫn xanh khi có DB.
Bước tiếp theo (user tự làm, ngoài scope session này):
- Chạy `php artisan permission:catalog-sync` (rollout) để 4 mã bị đặt `deprecated_at` → biến khỏi picker `/admin/roles`.
- Review & commit/push (chưa làm — theo quy tắc không tự commit).
Blocked:

## Ngoài scope (ghi rõ để khỏi tự ý làm)
- KHÔNG xoá route/URL (install_requests/plans/summaries/estimates/advances). install_summaries sẽ 403 toàn màn qua middleware sau deprecate (cascade).
- KHÔNG sửa `Contract.php`, model Install*, blade formJs — gate `can()` tự fail-closed.
- KHÔNG sửa fixture MAP.
- Rollout thật (catalog-sync) do user chạy sau; task này chỉ sửa code.

### Checkpoint — 2026-11-28 17:30 (wrap up cuối ngày)
Vừa hoàn thành: (xem Checkpoint 2026-11-28 ở trên). Quyết định đã chốt (user 11:11–11:26): coi luồng `App\Contract` + chuỗi lắp đặt cũ (InstallRequest → InstallPlan → InstallSummary → InstallEstimate → InstallAdvance) là KHÔNG dùng; gỡ cả 4 mã khỏi Catalog (`accounting.chi_phi_lap_dat.approve`, `accounting.de_nghi_tam_ung_chi_phi_lap_dat.approve`, `customer_care.du_toan_chi_phi_lap_dat.create`, `customer_care.lap_dat.manage`); giữ URL/route.
Đang làm dở: CHƯA commit/push — ERP develop_02 (`ContractDatatable.php`, `InstallSummaryController.php`, `InstallRequestController.php`); hrm-api develop (`Catalog/accounting.php` — chung file với đợt tách quyền Trưởng phòng KT, `Catalog/customer_care.php`). Chưa đếm phiếu `install_estimates`/`install_advances` trên prod (DB test = 0).
Bước tiếp theo: Commit + push khi user cho phép → `permission:catalog-sync` để 4 mã ẩn khỏi picker (install_summaries sẽ 403 toàn màn).
Blocked:
