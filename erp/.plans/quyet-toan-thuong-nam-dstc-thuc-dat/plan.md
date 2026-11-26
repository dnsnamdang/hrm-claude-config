# Plan — Quyết toán thưởng năm DSTC "phòng thực đạt" lấy đúng nguồn (ERP)

Redmine #10651. Xem `design.md`. Fix song song bên HRM (`HRM/.plans/quyet-toan-thuong-nam-dstc-thuc-dat/`).

## Tasks (ERP)

- [x] **T1 — BE: viết lại `getActualRevenue()` lấy từ nguồn quyết toán HĐ Firm** ✓ gỡ import `Account`/`AccountDetail` chết; query mới `SUM(scd.commission_sale)` qua fscd(type=2)→sc, lọc `sc.date_accounting`. `getRegisteredRevenue`+`calculateBonusFundDSTC` giữ nguyên.
  File: `app/Services/Accounting/BonusEndYearSettlementService.php` (method `getActualRevenue`, dòng 32-69)
  - Bỏ toàn bộ logic `Account` + `AccountDetail` (TK 511/5211/5212/5213).
  - Parse `$dateFrom`/`$dateTo` (d/m/Y) → Y-m-d như cũ.
  - Query mới:
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
  - Dọn import không còn dùng (`Account`, `AccountDetail`) nếu không nơi nào khác trong file dùng.
  - `getRegisteredRevenue` + `calculateBonusFundDSTC` KHÔNG đụng.

- [x] **T2 — Verify (đọc code + dữ liệu DB `erp_hrm_check`)** ✓
  - `php -l` OK.
  - tinker (gọi method HRM port y hệt): dept=55 2025 = **9,163,656,207.80** khớp số đã tính tay.
  - `getActualRevenue($departmentId,$from,$to)` chỉ gọi từ `calculateDepartmentDetail` (dòng 119, TYPE_DSTC) — grep repo xác nhận; các `getActualRevenue` khác là class khác, chữ ký khác.

## Checkpoint
- 2026-11-26: Fix + verify xong ERP. Viết lại `getActualRevenue` lấy nguồn quyết toán HĐ Firm
  (`fscd.type=2`, `sc.date_accounting ∈ [từ,đến]`, gom theo `scd.department_id`). Gỡ 2 import chết.
  `php -l` OK; số liệu khớp bản HRM. KHÔNG đụng registered revenue / quỹ thưởng. Chưa commit (chờ lệnh user).

### Checkpoint — 2026-11-26 (wrap up cuối ngày)
Vừa hoàn thành: push ERP develop_02 `7c5a91532f` (HRM song song `9977f2f63`); Redmine #10651 = Code xong chờ test.
Đang làm dở: (không)
Bước tiếp theo: gop_db khi user yêu cầu; chờ tester.
Blocked: (không) — CHƯA gop_db.
