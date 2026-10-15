# Vô hiệu hoá CRM Mate-sync (CRM ngừng dùng)

**Nhánh:** `gop_db`. Ngày: 2026-08-01. Thuộc Gộp DB.

## Bối cảnh
CRM = tích hợp đồng bộ HRM → hệ ngoài Mate/odoo (`Modules/CRM`, không route/màn, gate cờ `use_crm`). Đã ngừng dùng. Các bảng `customer_*`/`quotations`/`delivery_places` KHÔNG phải CRM (tính năng Khách hàng của Assign — GIỮ).

## Quyết định (user chọn (b) — vô hiệu hoá tối thiểu)
- Tắt cờ `use_crm` (hiện đã = '0' → boot-hook 9 entity Human đã inert).
- **Drop `hrm_module_mappings`** (1601 dòng — chỉ CRM sync dùng). GIỮ `module_mappings` (TpModuleMapping/mysql2/use_erp, 229338 dòng, phục vụ Gộp DB).
- **GIỮ code `Modules/CRM/`** (không xóa) — an toàn vì cờ off.

## Tasks
- [x] Script re-runnable `disable_crm.php` (idempotent, DRY_RUN, nối pipeline sau `reconcile_auth.php`).
- [x] Backup `hrm_module_mappings` → chạy thật trên `erp_hrm_check` → verify drop + module_mappings còn.

## Lưu ý
- Nếu sau này muốn dọn hẳn (option a): xóa boot-hook `use_crm` trong 9 entity Human (`Employee, EmployeeInfo, Company, Department, Part, Bank, BankBranch, WorkingPosition, EmployeeBankAccount`) + xóa `Modules/CRM/` + seeder CRM.
- `crm_id` trên provinces/districts/wards độc lập — không đụng.

## Checkpoint — 2026-08-01
Vừa hoàn thành: script + chạy thật trên local
Đang làm dở: (không)
Bước tiếp theo: chạy `disable_crm.php` trên môi trường gộp khác khi cần
Blocked:
