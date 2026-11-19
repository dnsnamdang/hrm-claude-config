# Plan — Fix drift 0.01 tồn đầu kỳ gây crash tính giá vốn (phiếu PXH-42802)

Nhánh: `gop_db`. DB: `hrm_erp_gop` (remote). User chốt **Hướng A: chỉ fix data** (2026-10-16).

## Bối cảnh / nguyên nhân

Sửa/duyệt phiếu xuất PXH-42802 (type 99 điều chuyển nội bộ) ném 500:
`Trying to get property 'id' of non-object` tại `AccountingStockLog.php:49`
(`ProductExport::updateWarehouse` → `calculateValue` → `getValueDetails`).

- acc_stock **24206** (SP 50685 HKH-9846-0102, kho kế toán 62) có `qty=406.81`.
- Chỉ 1 log duy nhất id **166287** (tồn đầu kỳ `BeginningAccountingStock` 10217, 01/04/2023):
  `qty_before=0`, `change=406.80`, **`qty_after=406.81`** → log tự mâu thuẫn (0+406.80 ≠ 406.81).
- `beginning_accounting_stocks.qty` = 406.8 (ĐÚNG). Drift 0.01 chỉ nằm ở log `qty_after` + `acc_stock.qty`.
- FIFO `getValueDetails` cộng theo `change` (406.80) không phủ nổi `qty_before/after` 406.81 → đi ngược
  hết log → `$log` null → crash (dòng 49 thiếu guard null).
- Toàn DB chỉ **1 acc_stock lệch + 1 log mâu thuẫn** → cá biệt. 406.80 là giá trị đúng (khớp tồn đầu kỳ).
- KHÔNG do fix kiem-ke-xuat-vuot-giu (khác controller/model, phiếu không chứa SP 34686).

## Tasks

- [x] **D1.** Viết `\UpdateDB::fixAccountingStockDriftLog166287_20261016($dryRun=true)` (UpdateDB.php cuối
  class). Guard idempotent (chỉ sửa khi đang = 406.81), transaction, set log `qty_after` + acc_stock `qty`
  = `qty_before+change` = 406.80. Lint sạch.
- [x] **D2.** Dry-run OK: log 166287 qty_after 406.81→406.80, acc_stock 24206 qty 406.81→406.80.
- [x] **D3.** Chạy thật (2026-10-16) + verify DB: acc_stock 24206 qty=406.80; log 166287 qty_after=406.80;
  `qty == SUM(change)=406.80`; `inconsistent_logs` toàn DB = **0**.
- [x] **D4.** Verify: `AccountingStockLog::calculateValue('before'/'after')` cho acc_stock 24206 chạy OK,
  KHÔNG crash (after=120.710.903,04; before=0).

## Lưu ý
- Fix data thuần, KHÔNG sửa code (user chốt A). Không commit code.
- acc_stock 24206 chưa phát sinh log xuất nào → sửa không cascade.
