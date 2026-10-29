# Plan — Seed `configs` cho công ty mới + backfill

## Tasks
- [x] Chẩn đoán root cause: công ty 9 thiếu dòng `configs` (verify prod `hrm_erp_gop`: chỉ cty 9 thiếu, 8 cty còn lại có)
- [x] Xác minh field store của tab congno: chỉ `debt_calculation_date` store=config (cột tồn tại) → backfill xong là lưu được
- [x] Backfill DATA công ty 9 (script `scratchpad/backfill_configs_company9.php`), dry-run → **ghi thật prod** (user chốt)
      → tạo `configs.id=9` + 1 `contract_rows`; tổng cty có configs = 9/9
- [x] Code Hướng B: `CompaniesController@store` gọi `seedDefaultConfig()` sau `$company->save()` + thêm private method (clone cty1, idempotent, try/catch report)
- [x] `php -l` sạch
- [x] Commit + push `origin/gop_db` = `c97fd91ef3` (2026-10-01)
- [ ] (TUỲ CHỌN, chưa làm) Hardening `RegulationConfigService::applyVersion` nhánh config-store tự tạo dòng khi thiếu thay vì abort — là sửa hàm dùng chung HRM, cần xác nhận riêng

## Checkpoint — 2026-10-01
Vừa hoàn thành: backfill data cty9 trên prod + sửa code seed khi tạo công ty mới (ERP CompaniesController), php -l sạch.
Đang làm dở: không.
Bước tiếp theo: chờ user yêu cầu commit (nhánh gop_db); hoặc chốt có hardening applyVersion không.
Blocked: không.
