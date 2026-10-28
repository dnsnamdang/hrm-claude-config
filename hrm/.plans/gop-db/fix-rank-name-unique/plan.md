# Fix: Tạo ngạch lương lỗi 500 do trùng tên cấp bậc

## Phase 1
### BE
- [x] Migration `2026_10_28_000001_drop_unique_name_on_ranks_table` bỏ `ranks_name_unique` (giữ `ranks_code_unique`) — chạy thử local OK (up/down/up)
- [x] Deploy PROD 28/10/2026 (commit 7cc66c003, build_tpe.sh) — index đã gỡ

## Phase 2 — Chuẩn hoá tên/mã cấp bậc cũ + mã unique theo công ty (chốt 28/10/2026)
### BE
- [x] Migration `2026_10_28_000002_normalize_rank_names_and_unique_code_per_company`: đổi trường đúng kiểu FE cũ "<ngạch> <N>" sang kiểu hiện tại (PROD dry-run 56 dòng; giữ tên tự đặt "(ETEK GREEN)"; bỏ qua mồ côi + bậc thừa), `ranks_code_unique` → `ranks_company_code_unique(company_id, code)`
- [x] `RankService::save` gán `ranks.company_id` theo công ty của ngạch (trước lấy công ty gốc người tạo)
- [x] `SaveRankRequest`: mã/tên ngạch unique theo công ty; mã cấp bậc trùng trong công ty → 422 ở ô Mã ngạch thay vì 500
- [x] Test local in-process 6 case (rollback) + migrate local 56 dòng
- [x] Deploy PROD 28/10/2026 (commit a98c82515) — đổi 56 dòng, index ranks_company_code_unique; backup trước khi chạy: ~/ranks_backup_20261028.json trên hrm-prod
