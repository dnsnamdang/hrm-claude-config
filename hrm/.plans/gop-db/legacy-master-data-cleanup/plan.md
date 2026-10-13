# Plan — Dọn bộ danh mục cũ trùng mã

## Phase 1 — Seeder dọn dữ liệu
### BE
- [x] Điều tra nguyên nhân (API prod + dev, Redmine #11303, MasterDataPl8Seeder)
- [x] Viết `CleanupLegacyDuplicateCatalogsSeeder` (nhận diện theo tiêu chí, đếm tham chiếu, backup, xoá/khoá, transaction)
- [x] Test local: dựng bộ giả trong transaction rồi rollback (DB local không có bộ cũ)
- [x] Thử đổi tiêu chí sang trùng TÊN → user cho revert, giữ tiêu chí trùng MÃ
- [x] Fix: dev-hrm gõ yes vẫn ra "Chưa xác nhận" → bỏ confirm(), dùng ask() + lọc ký tự điều khiển, in câu trả lời nhận được khi từ chối
- [ ] Chạy trên prod `hrm.eteksofts.com` → kiểm lại API 2 màn
- [ ] Chạy trên dev `dev-hrm.eteksofts.com` → kiểm lại API 2 màn
- [ ] (Chờ quyết) unique index `industries.code`, `hrm_scopes.code`

### Checkpoint — 2026-10-09
Vừa hoàn thành: seeder `CleanupLegacyDuplicateCatalogsSeeder` + test local (bộ giả trong transaction, rollback): xoá/khoá đúng, pivot đúng, lần 2 no-op, không xác nhận thì không đổi gì
Đang làm dở: —
Bước tiếp theo: chạy trên prod `hrm.eteksofts.com` (interactive, xem báo cáo trước khi gõ yes) → kiểm lại API → dev
Blocked: cần người có quyền SSH server chạy seeder
