# banks-cut-mysql2 — Bỏ sync db_second màn Danh mục ngân hàng

- Người phụ trách: @khoipv
- Nhánh: `gop_db` (chỉ `hrm-api`, FE không đổi)
- Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-03-banks-cut-mysql2-design.md`

## Mục tiêu

DB HRM + ERP đã gộp thành 1 (`gop_db`) → bỏ toàn bộ code đồng bộ sang db_second (`mysql2`)
của màn `/human/banks`. Hiện `TpBank`/`TpBankBranch` đã mất `$connection = 'mysql2'`
(commit `931a192d6`) nên code sync đang **ghi trùng 2 lần vào cùng bảng** `banks`/`bank_branches`,
nhánh create có nguy cơ duplicate primary key khi `use_erp` bật.

## Quyết định đã chốt (user 2026-08-03)

1. Bỏ 8 khối sync `use_erp` trong 6 hàm của `BankService` (create/update/delete bank + branch, lock/unlock).
2. **GIỮ file** `TpBank.php`, `TpBankBranch.php` (thành entity mồ côi, không dùng cho code mới).
3. Fix luôn 2 vết sót trong `BankBranch.php`: xoá comment `// protected $connection = 'mysql2';`
   + xoá constructor override đang nuốt `parent::__construct()` (bug không fill attribute).
4. Sync CRM (`use_crm`) giữ nguyên — không phải db_second.
5. `use_erp` ở các màn khác ngoài phạm vi.
