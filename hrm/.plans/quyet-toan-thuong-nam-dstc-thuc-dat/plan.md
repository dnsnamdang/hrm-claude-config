# Plan — Quyết toán thưởng năm DSTC "phòng thực đạt" lấy đúng nguồn (HRM)

Redmine #10651. Xem `design.md` (+ bản ERP). Fix song song bên ERP.

## Tasks (HRM)

- [x] **T1 — BE: viết lại `getActualRevenue()` port công thức mới từ ERP** ✓ gỡ const `REVENUE_ACCOUNT_NUMBERS` + import `Account`/`AccountDetail`; giữ `normalizeToIso`; query mới `SUM(scd.commission_sale)` literal `App\Model\Sale\Firm\Contract\FirmContract`. Cập nhật docblock lớp.
  File: `Modules/Finance/Services/BonusEndYearSettlement/BonusEndYearSettlementService.php` (method `getActualRevenue`, dòng 69-96)
  - Bỏ logic `Account::selfAndChildIds()` + `AccountDetail` (TK 511/5211/5212/5213).
  - Giữ `normalizeToIso($dateFrom)` / `normalizeToIso($dateTo)`.
  - Query mới (query builder):
    ```php
    $total = DB::table('settlement_contract_departments as scd')
        ->join('firm_settlement_contract_detail as fscd', 'fscd.id', '=', 'scd.firm_settlement_contract_detail_id')
        ->join('settlement_contracts as sc', 'sc.id', '=', 'fscd.settlement_contract_id')
        ->where('fscd.type', 2)
        ->where('scd.contractable_type', 'App\Model\Sale\Firm\Contract\FirmContract')
        ->where('scd.department_id', $departmentId)
        ->whereBetween('sc.date_accounting', [$from, $to])
        ->sum('scd.commission_sale');
    return (float) $total;
    ```
  - Xóa const `REVENUE_ACCOUNT_NUMBERS` + import `Account`/`AccountDetail` nếu thành code chết.
  - KHÔNG đụng `calculateDepartmentDetail` / `recomputeDetailForSave` (chỉ tiêu thụ con số).

- [x] **T2 — Verify (code + tinker)** ✓
  - `php -l` OK.
  - tinker gọi thẳng `getActualRevenue(55,...)`: d/m/Y = Y-m-d = **9,163,656,207.80** (normalizeToIso OK, 2 định dạng ra cùng số). Khớp ERP.
  - 2 nơi gọi (`calculateDepartmentDetail` dòng 131 + `recomputeDetailForSave` dòng 190) không đổi chữ ký → cùng hưởng.
  - ⏳ Chưa đối chiếu trên MÀN thật (Playwright) — số liệu đã khớp ở tầng service; làm khi user cần UI check.

## Checkpoint
- 2026-11-26: Fix + verify (service+tinker) xong HRM. Port y hệt ERP. Gỡ const + 2 import chết, giữ
  `normalizeToIso`. dept=55 2025 = 9,163,656,207.80 khớp ERP. KHÔNG đụng calculateDepartmentDetail/
  recomputeDetailForSave/quỹ thưởng. Chưa commit, chưa gop_db (chờ lệnh user). Còn: UI check qua Playwright nếu cần.

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: push hrm-api develop `9977f2f63` (ERP `7c5a91532f`); Redmine #10651 = Code xong chờ test.
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; UI check Playwright nếu cần.
Blocked: (không) — CHƯA gop_db.
